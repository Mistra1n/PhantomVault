from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

def generate_rsa_keys():
    """Generate RSA key pair"""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_hybrid(public_key, message):
    """Encrypt with RSA+AES hybrid approach"""
    # Generate random AES key
    aes_key = get_random_bytes(16)
    
    # Encrypt message with AES
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())
    
    # Encrypt AES key with RSA
    recipient_key = RSA.import_key(public_key)
    encrypted_aes_key = recipient_key.encrypt(aes_key, None)[0]
    
    # Return all components
    return base64.b64encode(encrypted_aes_key).decode(), \
           base64.b64encode(cipher_aes.nonce).decode(), \
           base64.b64encode(ciphertext).decode(), \
           base64.b64encode(tag).decode()

def decrypt_hybrid(private_key, encrypted_aes_key, nonce, ciphertext, tag):
    """Decrypt RSA+AES hybrid message"""
    # Decrypt AES key with RSA
    key = RSA.import_key(private_key)
    aes_key = key.decrypt(base64.b64decode(encrypted_aes_key))
    
    # Decrypt message with AES
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=base64.b64decode(nonce))
    message = cipher_aes.decrypt_and_verify(
        base64.b64decode(ciphertext), 
        base64.b64decode(tag)
    )
    
    return message.decode()
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())

def decrypt_message(encrypted_msg, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_msg).decode()
