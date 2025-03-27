from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode

# Salt generated from master_password_hash_generator.py (must match!)
salt = b's2u\xd2\xf1\xe2\xda\xf3\xc4nW>$\x7f\x9e\x89'

def query_master_pwd(master_password, second_FA_location):
    # Paste your generated PBKDF2 hash here
    master_password_hash = "3db231aa0582fa4361191a12c84382c77fb375e1cc360fc10cf6307a0c8a68fd"
    # Recreate the PBKDF2 hash from input password + salt
    compile_factor_together = PBKDF2(
        master_password + second_FA_location,
        salt,
        dkLen=32,
        count=100000,
        hmac_hash_module=SHA256
    ).hex()

    if compile_factor_together == master_password_hash:
        return True
    return False

def encrypt_password(password_to_encrypt, master_password_hash):
    # Generate the encryption key from the master password hash
    key = PBKDF2(str(master_password_hash), salt).read(32)
    data_convert = str.encode(password_to_encrypt)
    
    # Encrypt using AES in EAX mode
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data_convert)
    
    # Add the nonce to the ciphertext and encode it in base64
    add_nonce = ciphertext + nonce
    encoded_ciphertext = b64encode(add_nonce).decode()
    
    return encoded_ciphertext

def decrypt_password(password_to_decrypt, master_password_hash):
    # Handle padding for base64 decoding if necessary
    if len(password_to_decrypt) % 4:
        password_to_decrypt += '=' * (4 - len(password_to_decrypt) % 4)

    # Decode the base64-encoded ciphertext
    convert = b64decode(password_to_decrypt)
    
    # Generate the decryption key from the master password hash
    key = PBKDF2(str(master_password_hash), salt).read(32)
    
    # Extract the nonce from the end of the ciphertext
    nonce = convert[-16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    
    # Decrypt the password
    plaintext = cipher.decrypt(convert[:-16])
    
    return plaintext


