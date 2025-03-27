from hashlib import sha256
from Crypto.Cipher import AES 
from Crypto.Protocol.KDF import PBKDF2 
import hashlib
from base64 import b64encode, b64decode

# Enter salt here in ******* field. Enter binary string.
salt = b'\xa2\x93\xb8\xb0\x0f\x9e\xb4\xae\xd1\xfd\xc0Z\xb2\xf0\xa1b'




def query_master_pwd(master_password, second_FA_location): 

    # Enter password hash in ******** field. Use PBKDF2 and Salt from above. Use master_password_hash_generator.py to generate a master password hash.
    master_password_hash = "7fe2d7c9b42608c8b3cf36e430370228b780621e4b3ae9c78507c54873dc4ec1"

    compile_factor_together = hashlib.sha256(master_password + second_FA_location).hexdigest()

    if compile_factor_together == master_password_hash:
        return True

def encrypt_password(password_to_encrypt, master_password_hash):

    key = PBKDF2(str(master_password_hash), salt).read(32)

    data_convert = str.encode(password_to_encrypt)

    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(data_convert)

    add_nonce = ciphertext + nonce

    encoded_ciphertext = b64encode(add_nonce).decode()

    return encoded_ciphertext

def decrypt_password(password_to_decrypt, master_password_hash):

    if len(password_to_decrypt) % 4:

     password_to_decrypt += '=' * (4 - len(password_to_decrypt) % 4)

    convert = b64decode(password_to_decrypt)

    key = PBKDF2(str(master_password_hash), salt).read(32)

    nonce = convert[-16:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(convert[:-16])

    return plaintext

