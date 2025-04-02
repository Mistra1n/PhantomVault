# 🔐 PhantomVault - Advanced Steganography Toolkit  
*Hide messages in images, audio, and PDFs with military-grade encryption* 

## 🌟 Features  
- **Multi-format stealth** - Hide data in PNGs, WAV audio, and PDF metadata  
- **AES-256 + RSA encryption** - Automatic key generation with `-x` flag  
- **Zero footprint** - No visible file size or quality changes  
- **Dual interfaces** - Graphical UI and command-line support 
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
git clone https://github.com/mistra1n/PhantomVault.git
cd PhantomVault
pip install -r requirements.txt
```

## GUI

```python
python src/gui_app.py  
```
Steps:

1 **Select mode (Encode/Decode)**

2 **Choose file type**

3 **Input secret message or load file**

4 **Toggle encryption**

GUI Screenshot
## CLI

```python 
# Encode with encryption  
python src/stego.py -e -t image -i cat.png -o secret.png -m "Kenya Zimmerman" -x  

# Decode  
python src/stego.py -d -t image -i secret.png -k YOUR_KEY  
```
## Usage Guide
**Supported  Formats**
______________________
```
Format         Requirements       Max Capacity
-----------------------------------------------
Images         PNG/BMP, 24-bit     3 bits per pixel
Audio          WAV,16-bit mono     1KB per second
PDF            Unencrypted         Metadata only
```

 Command Reference
```
Flag   Description's

-e	    Encode mode
-d	    Decode mode
-t	    Type (image,audio,pdf)
-i	    Input file path
-o	    Output file path
-m	    Message to hide
-x	    Enable encryption
-k	    Decryption key
```



## ⚠️ Legal Disclaimer
This tool is for authorized security testing and educational purposes only.

❗ Unauthorized use may violate:

1 **Computer Fraud and Abuse Act (CFAA)**

2 **General Data Protection Regulation (GDPR)**

3 **Local privacy laws**

Always obtain written permission before testing on systems you don't own.

## 💡 Pro Tips
Bulk Processing
```python
# Encode all images in a folder (Linux/Mac)  
find ./documents/ -name "*.png" | parallel python src/stego.py -e -t image -i {} -o ./secrets/{}  
```
Debugging
```python
# Verbose output  
python src/stego.py -e -t audio -i song.wav -vvv    
```
