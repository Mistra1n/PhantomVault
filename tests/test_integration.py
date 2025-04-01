import pytest
from src.stego import *
from src.utils import *
import os

@pytest.fixture
def test_image():
    return "examples/test.png"

@pytest.fixture
def test_wav():
    return "examples/test.wav"

def test_image_stego(test_image):
    msg = "test message"
    encode_image(test_image, msg, "temp.png")
    assert decode_image("temp.png") == msg
    os.remove("temp.png")

def test_audio_stego(test_wav):
    msg = "audio test"
    encode_audio(test_wav, msg, "temp.wav")
    assert decode_audio("temp.wav") == msg
    os.remove("temp.wav")

def test_hybrid_crypto():
    priv, pub = generate_rsa_keys()
    msg = "secure message"
    parts = encrypt_hybrid(pub, msg)
    assert decrypt_hybrid(priv, *parts) == msg
