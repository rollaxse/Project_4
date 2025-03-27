from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import os

def master_password_gen():
    # Prompt the user for the master password and encode it to bytes
    password = input("Enter your master password: ").encode()

    # Generate a secure 16-byte salt
    salt = os.urandom(16)
    
    # Display the salt in both binary and hexadecimal formats
    print("Salt (binary):", salt)
    print("Salt (hex):", salt.hex())

    # Generate the PBKDF2 hash using the password, salt, and SHA-256
    master_hash = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
    
    # Print the derived master password hash in hexadecimal format
    print("Master Password Hash:", master_hash.hex())

# Call the function to test it
master_password_gen()
