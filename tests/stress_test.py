import os
import time
from src.stego import encode_image, decode_image

def test_large_message():
    """Test with maximum capacity message"""
    with open("large.txt", "w") as f:
        f.write("A" * 1_000_000)  # 1MB message
    
    start = time.time()
    encode_image("test.png", open("large.txt").read(), "stress.png")
    encode_time = time.time() - start
    
    start = time.time() 
    decoded = decode_image("stress.png")
    decode_time = time.time() - start
    
    assert len(decoded) == 1_000_000
    print(f"Encoded 1MB in {encode_time:.2f}s, decoded in {decode_time:.2f}s")
    os.remove("stress.png")

def test_file_types():
    """Test different file formats"""
    for ext in [".png", ".wav", ".pdf"]:
        test_file = f"test{ext}"
        if os.path.exists(test_file):
            encode_func = globals()[f"encode_{ext[1:]}"]
            decode_func = globals()[f"decode_{ext[1:]}"]
            
            encode_func(test_file, "stress test", f"out{ext}")
            assert decode_func(f"out{ext}") == "stress test"
            os.remove(f"out{ext}")

if __name__ == "__main__":
    test_large_message()
    test_file_types()
