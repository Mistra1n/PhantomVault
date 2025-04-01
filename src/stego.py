#!/usr/bin/env python3
"""
Advanced Steganography Tool with File Validation
Supports: PNG, WAV, PDF with full error checking
"""

import argparse
import os
import struct
import wave
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from utils import encrypt_message, decrypt_message, generate_key

def validate_image(filepath):
    """Validate image file is supported format"""
    try:
        with Image.open(filepath) as img:
            if img.format not in ['PNG', 'BMP']:
                raise ValueError(f"Unsupported image format: {img.format}. Use PNG or BMP")
            return img
    except Exception as e:
        raise ValueError(f"Invalid image file: {str(e)}")

def validate_wav(filepath):
    """Validate WAV file meets requirements"""
    try:
        with wave.open(filepath, 'rb') as wav:
            if wav.getnchannels() != 1:
                raise ValueError("Only mono WAV files supported")
            if wav.getsampwidth() != 2:
                raise ValueError("Only 16-bit WAV files supported")
            if wav.getframerate() not in [44100, 48000]:
                print(f"Warning: Non-standard sample rate {wav.getframerate()}")
            return wav.getparams()
    except wave.Error as e:
        raise ValueError(f"Invalid WAV file: {str(e)}")

def validate_pdf(filepath):
    """Validate PDF is not password protected"""
    try:
        with open(filepath, 'rb') as f:
            reader = PdfReader(f)
            if reader.is_encrypted:
                raise ValueError("Encrypted PDFs are not supported")
            return len(reader.pages)
    except Exception as e:
        raise ValueError(f"Invalid PDF file: {str(e)}")

def encode_image(image_path, secret_msg, output_path, encrypt=False):
    """Hide message in image with validation"""
    img = validate_image(image_path)
    
    if encrypt:
        key = generate_key()
        print(f"ENCRYPTION KEY (SAVE THIS): {key.decode()}")
        secret_msg = encrypt_message(secret_msg, key)

    binary_msg = ''.join(format(ord(c), '08b') for c in secret_msg)
    binary_msg += '1111111111111110'  # Delimiter
    
    if len(binary_msg) > img.width * img.height * 3:
        raise ValueError(f"Message too large for image (max: {img.width*img.height*3//8} chars)")
    
    pixels = list(img.getdata())
    new_pixels = []
    msg_index = 0
    
    for pixel in pixels:
        if msg_index < len(binary_msg):
            new_pixel = []
            for color in pixel[:3]:  # Only modify RGB channels
                if msg_index < len(binary_msg):
                    new_color = (color & 0xFE) | int(binary_msg[msg_index])
                    new_pixel.append(new_color)
                    msg_index += 1
                else:
                    new_pixel.append(color)
            
            if len(pixel) == 4:  # Preserve alpha
                new_pixel.append(pixel[3])
                
            new_pixels.append(tuple(new_pixel))
        else:
            new_pixels.append(pixel)
    
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)

def decode_image(image_path, decrypt=False, key=None):
    """Extract message from image with validation"""
    validate_image(image_path)
    
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_msg = ""
    
    for pixel in pixels:
        for color in pixel[:3]:  # Check RGB channels
            binary_msg += str(color & 1)
    
    delimiter = '1111111111111110'
    if delimiter in binary_msg:
        binary_msg = binary_msg.split(delimiter)[0]
    
    secret_msg = ""
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        secret_msg += chr(int(byte, 2))
    
    if decrypt:
        if not key:
            key = input("Enter encryption key: ").encode()
        secret_msg = decrypt_message(secret_msg, key)
    
    return secret_msg

def encode_audio(audio_path, secret_msg, output_path, encrypt=False):
    """Hide message in WAV with validation"""
    params = validate_wav(audio_path)
    
    if encrypt:
        key = generate_key()
        print(f"ENCRYPTION KEY (SAVE THIS): {key.decode()}")
        secret_msg = encrypt_message(secret_msg, key)

    with wave.open(audio_path, 'rb') as audio:
        frames = audio.readframes(audio.getnframes())
    
    binary_msg = ''.join(format(ord(c), '08b') for c in secret_msg)
    binary_msg += '1111111111111110'
    
    frame_list = list(struct.unpack(f'{len(frames)}B', frames))
    
    if len(binary_msg) > len(frame_list):
        max_chars = len(frame_list) // 8
        raise ValueError(f"Message too large for audio (max: {max_chars} chars)")
    
    for i in range(len(binary_msg)):
        frame_list[i] = (frame_list[i] & 0xFE) | int(binary_msg[i])
    
    new_frames = struct.pack(f'{len(frame_list)}B', *frame_list)
    with wave.open(output_path, 'wb') as output:
        output.setparams(params)
        output.writeframes(new_frames)

def decode_audio(audio_path, decrypt=False, key=None):
    """Extract message from WAV with validation"""
    validate_wav(audio_path)
    
    with wave.open(audio_path, 'rb') as audio:
        frames = audio.readframes(audio.getnframes())
    
    binary_msg = ''.join(str(byte & 1) for byte in struct.unpack(f'{len(frames)}B', frames))
    
    delimiter = '1111111111111110'
    if delimiter in binary_msg:
        binary_msg = binary_msg.split(delimiter)[0]
    
    secret_msg = ""
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        secret_msg += chr(int(byte, 2))
    
    if decrypt:
        if not key:
            key = input("Enter encryption key: ").encode()
        secret_msg = decrypt_message(secret_msg, key)
    
    return secret_msg

def encode_pdf(pdf_path, secret_msg, output_path):
    """Hide message in PDF metadata"""
    validate_pdf(pdf_path)
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    writer.add_metadata({
        '/HiddenMessage': secret_msg,
        '/Creator': 'Steganography Tool'
    })
    
    with open(output_path, 'wb') as f:
        writer.write(f)

def decode_pdf(pdf_path):
    """Extract message from PDF metadata"""
    validate_pdf(pdf_path)
    
    reader = PdfReader(pdf_path)
    metadata = reader.metadata
    return metadata.get('/HiddenMessage', 'No hidden message found')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Secure Steganography Tool with File Validation",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-e", "--encode", action="store_true", help="Encode mode")
    parser.add_argument("-d", "--decode", action="store_true", help="Decode mode")
    parser.add_argument("-t", "--type", choices=['image','audio','pdf'], 
                      required=True, help="File type to process")
    parser.add_argument("-x", "--encrypt", action="store_true", help="Enable encryption")
    parser.add_argument("-i", "--input", required=True, help="Input file path")
    parser.add_argument("-o", "--output", help="Output file path (encode mode)")
    parser.add_argument("-m", "--message", help="Message to hide (encode mode)")
    parser.add_argument("-k", "--key", help="Encryption key (decode mode)")
    
    args = parser.parse_args()
    
    try:
        if args.encode:
            if not args.message or not args.output:
                parser.error("Encode mode requires --message and --output")
            
            if args.type == 'image':
                encode_image(args.input, args.message, args.output, args.encrypt)
            elif args.type == 'audio':
                encode_audio(args.input, args.message, args.output, args.encrypt)
            elif args.type == 'pdf':
                if args.encrypt:
                    print("Warning: PDF encryption not supported, using metadata only")
                encode_pdf(args.input, args.message, args.output)
            
            print(f"Message encoded successfully in {args.output}")
            
        elif args.decode:
            if args.type == 'image':
                result = decode_image(args.input, args.encrypt, args.key)
            elif args.type == 'audio':
                result = decode_audio(args.input, args.encrypt, args.key)
            elif args.type == 'pdf':
                result = decode_pdf(args.input)
            
            print("Decoded message:", result)
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
