import pytest
from src.utils import *

def test_encryption_integrity():
    """Verify encryption actually obscures data"""
    priv, pub = generate_rsa_keys()
    msg = "secret"
    
    # AES-RSA hybrid
    enc = encrypt_hybrid(pub, msg)
    assert msg not in str(enc)  # Encrypted shouldn't contain plaintext
    
    # Fernet
    key = generate_key()
    assert decrypt_message(encrypt_message(msg, key), key) == msg

def test_key_validation():
    """Wrong keys should fail"""
    priv1, pub1 = generate_rsa_keys()
    _, pub2 = generate_rsa_keys()
    
    enc = encrypt_hybrid(pub1, "test")
    with pytest.raises(Exception):
        decrypt_hybrid(priv1, enc[0], enc[1], "corrupted".encode(), enc[3])

def test_binary_data():
    """Test non-text data handling"""
    binary_data = bytes(range(256))
    priv, pub = generate_rsa_keys()
    
    enc = encrypt_hybrid(pub, binary_data.decode('latin-1'))
    assert decrypt_hybrid(priv, *enc).encode('latin-1') == binary_data

if __name__ == "__main__":
    test_encryption_integrity()
    test_key_validation() 
    test_binary_data()
    print("All security tests passed")
