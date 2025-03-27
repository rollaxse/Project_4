import password_generator
import sql_statements as sql
import db_connect
import psycopg2
import argparse
import master_password
import getpass
import sys
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

def main():
    my_parser = argparse.ArgumentParser(
        description="Password Manager Vault: Create, Add, and Delete URL, Usernames, and Passwords",
        usage="[options]"
    )

    # Get master password input
    master_password_input = getpass.getpass("Master Password: ").encode()

    # Disable second factor authentication by using empty bytes
    second_FA_location = b""

    # Authenticate using query_master_pwd
    if master_password.query_master_pwd(master_password_input, second_FA_location) is True:
        print("\nSuccessfully Authenticated.\n")

        # Derive the PBKDF2 hash again for encryption/decryption
        master_password_hash = PBKDF2(
            master_password_input + second_FA_location,
            master_password.salt,
            dkLen=32,
            count=100000,
            hmac_hash_module=SHA256
        ).hex()

        connection = db_connect.connection_db()
    else:
        print("Failed to authenticate into server. Run the program again.")
        sys.exit()

    # Set up command line arguments
    my_parser.add_argument("-a", "--add", type=str, nargs=2, metavar=("[URL]", "[USERNAME]"))
    my_parser.add_argument("-q", "--query", type=str, nargs=1, metavar=("[URL]"))
    my_parser.add_argument("-l", "--list", action="store_true")
    my_parser.add_argument("-d", "--delete", type=str, nargs=1, metavar=("[URL]"))
    my_parser.add_argument("-ap", "--add_password", type=str, nargs=3, metavar=("[URL]", "[USERNAME]", "[PASSWORD]"))
    my_parser.add_argument("-uurl", "--update_url", type=str, nargs=2, metavar=("[NEW_URL]", "[OLD_URL]"))
    my_parser.add_argument("-uuname", "--update_username", type=str, nargs=2, metavar=("[URL]", "[NEW_USERNAME]"))
    my_parser.add_argument("-upasswd", "--update_password", type=str, nargs=2, metavar=("[URL]", "[NEW_PASSWORD]"))

    args = my_parser.parse_args()
    cursor = connection.cursor()
    connection.commit()

    if args.add:
        URL = args.add[0]
        username = args.add[1]
        password = password_generator.password_gen(20)
        password_official = master_password.encrypt_password(password, master_password_hash)
        cursor.execute(sql.insert_db_row(), (URL, username, password_official))
        print(f"Record Added:\n URL: {URL}, Username: {username}, Password: {password} (Plaintext)")
        print(f"Record Added:\n URL: {URL}, Username: {username}, Password: {password_official} (Encrypted)")

    if args.query:
        URL = args.query[0]
        cursor.execute(sql.select_db_entry(), (URL,))
        record = cursor.fetchone()
        if record:
            password_field = record[2]
            decrypted = master_password.decrypt_password(password_field, master_password_hash)
            print(f"Record:\n URL: {record[0]}, Username: {record[1]}, Password: {decrypted.decode('utf-8')}")
            print(f"Encrypted Record:\n URL: {record[0]}, Username: {record[1]}, Password: {record[2]}")
        else:
            print(f"Could not find record matching the value of '{URL}'")

    if args.delete:
        URL = args.delete[0]
        cursor.execute("DELETE FROM Vault WHERE URL = %s", (URL,))
        print("Record deleted.")

    if args.add_password:
        URL = args.add_password[0]
        username = args.add_password[1]
        password = args.add_password[2]
        password_official = master_password.encrypt_password(password, master_password_hash)
        cursor.execute(sql.insert_db_row(), (URL, username, password_official))
        print("Record added with custom password.")

    if args.update_url:
        new_URL = args.update_url[0]
        old_URL = args.update_url[1]
        cursor.execute(sql.update_db_url(), (new_URL, old_URL))

    if args.update_username:
        new_username = args.update_username[0]
        URL = args.update_username[1]
        cursor.execute(sql.update_db_usrname(), (new_username, URL))

    if args.update_password:
        new_password = args.update_password[0]
        URL = args.update_password[1]
        cursor.execute(sql.update_db_passwd(), (new_password, URL))

    if args.list:
        cursor.execute("SELECT * from Vault")
        records = cursor.fetchall()
        for record in records:
            print("----------")
            print("URL:", record[0])
            print("Username:", record[1])
            decrypted = master_password.decrypt_password(record[2], master_password_hash)
            print("Password:", decrypted.decode('utf-8'))

    connection.commit()
    cursor.close()

main()

