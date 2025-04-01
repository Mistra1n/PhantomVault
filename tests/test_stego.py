import pytest
import os
from src.stego import encode_image, decode_image, encode_audio, decode_audio
from src.utils import generate_rsa_keys, encrypt_hybrid, decrypt_hybrid

# Test images/audio should be in examples/ folder
TEST_IMAGE = os.path.join(os.path.dirname(__file__), "../examples/test.png")
TEST_AUDIO = os.path.join(os.path.dirname(__file__), "../examples/test.wav")

@pytest.fixture
def clean_up():
    # This will run after each test
    yield
    for temp_file in ["temp.png", "temp.wav"]:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_image_encoding(clean_up):
    """Test basic image steganography"""
    secret = "Hello World!"
    encode_image(TEST_IMAGE, secret, "temp.png")
    assert decode_image("temp.png") == secret

def test_audio_encoding(clean_up):
    """Test basic audio steganography"""
    secret = "Audio secret"
    encode_audio(TEST_AUDIO, secret, "temp.wav")
    assert decode_audio("temp.wav") == secret

def test_hybrid_crypto():
    """Test RSA+AES encryption"""
    priv, pub = generate_rsa_keys()
    message = "Top secret"
    encrypted = encrypt_hybrid(pub, message)
    assert decrypt_hybrid(priv, *encrypted) == message
