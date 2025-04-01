import pytest
from tkinter import Tk
from src.gui_app import StegoApp, encrypt_message, decrypt_message
import tkinter.ttk as ttk

@pytest.fixture
def tk_root():
    root = Tk()
    yield root
    root.destroy()

def test_encryption():
    key = "testkey123"
    msg = "secret"
    encrypted = encrypt_message(msg, key)
    assert decrypt_message(encrypted, key) == msg

def test_ui_creation(tk_root):
    app = StegoApp(tk_root)
    
    # Verify main window properties
    assert "CryptoStego" in tk_root.title()
    
    # Verify widgets exist
    assert isinstance(app.mode_var, tk.StringVar)
    assert isinstance(app.type_var, tk.StringVar)
    assert isinstance(app.encrypt_var, tk.BooleanVar)
    
    # Test mode switching
    app.mode_var.set("decode")
    assert app.msg_frame.winfo_ismapped() == False
    
    app.mode_var.set("encode")
    assert app.msg_frame.winfo_ismapped() == True
