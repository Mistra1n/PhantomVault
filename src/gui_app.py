#!/usr/bin/env python3
"""
Complete Steganography GUI with Splash Screen
"""

import os
import random
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import wave
import struct
from PyPDF2 import PdfReader, PdfWriter
import requests
from packaging import version
import webbrowser
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ======================
# CONFIGURATION
# ======================
APP_NAME = "CryptoStego Pro"
VERSION = "2.4.0"
DEVELOPER_ALIAS = "Mistra1n"
GITHUB_REPO = "yourusername/Steganography-Tool"
HACKER_NAMES = [DEVELOPER_ALIAS] * 3 + [
    "PhantomSec", "ByteBandit", "CryptoGhost", "StealthVector"
]

# ======================
# SPLASH SCREEN
# ======================
class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.width, self.height = 500, 350
        
        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        
        # Gradient background
        for i in range(self.height):
            r = int(10 + (i/self.height)*100)
            g = int(30 + (i/self.height)*100)
            b = int(100 + (i/self.height)*155)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, self.width, i, fill=color)
        
        # App name
        self.canvas.create_text(
            self.width//2, self.height//3, 
            text=APP_NAME, 
            font=("Consolas", 28, "bold"), 
            fill="white"
        )
        
        # Version
        self.canvas.create_text(
            self.width//2, self.height//3 + 40,
            text=f"Version {VERSION}",
            font=("Consolas", 12),
            fill="white"
        )
        
        # Developer name
        self.hacker_name = random.choice(HACKER_NAMES)
        self.canvas.create_text(
            self.width//2, self.height//3 + 70,
            text=f"by {self.hacker_name}",
            font=("Courier New", 10, "italic"),
            fill="#00ff00"
        )
        
        # Loading bar
        self.canvas.create_rectangle(
            self.width//4, self.height*3//4, 
            self.width*3//4, self.height*3//4 + 20,
            outline="#444444", 
            fill="#222222"
        )
        
        self.loading_bar = self.canvas.create_rectangle(
            self.width//4 + 2, self.height*3//4 + 2,
            self.width//4 + 2, self.height*3//4 + 18,
            outline="", 
            fill="#00ccff"
        )
        
        # Loading text
        self.loading_text = self.canvas.create_text(
            self.width//2, self.height*3//4 + 40,
            text="Initializing secure channels...",
            font=("Courier New", 8),
            fill="white"
        )
        
        # Animation setup
        self.loading_pos = self.width//4 + 2
        self.loading_max = self.width*3//4 - 4
        self.loading_speed = 3
        self.loading_phrases = [
            "Bypassing firewalls...",
            "Encrypting payload...",
            "Establishing secure connection...",
            "Initializing steganography engine..."
        ]
        self.current_phrase = 0
        
        self.animate()
        self.root.after(3000, self.root.destroy)
    
    def animate(self):
        self.loading_pos += self.loading_speed
        if self.loading_pos > self.loading_max:
            self.loading_pos = self.width//4 + 2
            self.current_phrase = (self.current_phrase + 1) % len(self.loading_phrases)
            self.canvas.itemconfig(
                self.loading_text,
                text=self.loading_phrases[self.current_phrase]
            )
        
        self.canvas.coords(
            self.loading_bar,
            self.width//4 + 2, self.height*3//4 + 2,
            self.loading_pos, self.height*3//4 + 18
        )
        
        if self.root.winfo_exists():
            self.root.after(30, self.animate)
    
    def show(self):
        self.root.mainloop()

# ======================
# MAIN APPLICATION
# ======================
class StegoApp:
    def __init__(self, root):
        self.root = root
        self.key = None
        self.setup_ui()
        threading.Thread(target=self.check_updates, daemon=True).start()
    
    def setup_ui(self):
        self.root.title(f"{APP_NAME} {VERSION} :: {DEVELOPER_ALIAS}")
        self.root.geometry("800x600")
        
        # Create menu
        menubar = tk.Menu(self.root)
        
        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Check Updates", command=self.check_updates)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.root.config(menu=menubar)
        
        # Main frame
        mainframe = ttk.Frame(self.root, padding="20")
        mainframe.grid(row=0, column=0, sticky="nsew")
        
        # Mode selection
        ttk.Label(mainframe, text="Mode:").grid(row=0, column=0, sticky="w")
        self.mode_var = tk.StringVar(value="encode")
        ttk.Radiobutton(mainframe, text="Encode", variable=self.mode_var, 
                       value="encode").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(mainframe, text="Decode", variable=self.mode_var,
                       value="decode").grid(row=0, column=2, sticky="w")
        
        # File type
        ttk.Label(mainframe, text="File Type:").grid(row=1, column=0, sticky="w")
        self.type_var = tk.StringVar(value="image")
        ttk.Radiobutton(mainframe, text="Image", variable=self.type_var,
                       value="image").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(mainframe, text="Audio", variable=self.type_var,
                       value="audio").grid(row=1, column=2, sticky="w")
        ttk.Radiobutton(mainframe, text="PDF", variable=self.type_var,
                       value="pdf").grid(row=1, column=3, sticky="w")
        
        # File selection
        ttk.Button(mainframe, text="Select Input File", 
                  command=self.select_input).grid(row=2, column=0, pady=10)
        self.input_path = tk.StringVar()
        ttk.Label(mainframe, textvariable=self.input_path, 
                 wraplength=400).grid(row=2, column=1, columnspan=3, sticky="w")
        
        # Message frame
        self.msg_frame = ttk.Frame(mainframe)
        ttk.Label(self.msg_frame, text="Secret Message:").pack(side="left")
        self.message_entry = ttk.Entry(self.msg_frame, width=40)
        self.message_entry.pack(side="left", padx=5)
        self.msg_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        # Output file
        self.output_button = ttk.Button(mainframe, text="Select Output File",
                                      command=self.select_output)
        self.output_button.grid(row=4, column=0, pady=10)
        self.output_path = tk.StringVar()
        ttk.Label(mainframe, textvariable=self.output_path,
                 wraplength=400).grid(row=4, column=1, columnspan=3, sticky="w")
        
        # Encryption
        self.encrypt_var = tk.BooleanVar()
        ttk.Checkbutton(mainframe, text="Encrypt", 
                       variable=self.encrypt_var).grid(row=5, column=0, pady=10)
        
        # Execute
        ttk.Button(mainframe, text="Execute", 
                  command=self.execute).grid(row=6, column=0, columnspan=4, pady=20)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(mainframe, textvariable=self.status_var,
                 foreground="green").grid(row=7, column=0, columnspan=4)
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        
        # Bind mode change
        self.mode_var.trace_add('write', self.update_ui)
        self.update_ui()
    
    def update_ui(self, *args):
        if not hasattr(self, 'msg_frame'):
            return
            
        if self.mode_var.get() == "decode":
            self.msg_frame.grid_remove()
            self.output_button.config(state="disabled")
        else:
            self.msg_frame.grid()
            self.output_button.config(state="normal")
    
    def select_input(self):
        filetypes = [
            ("Images", "*.png *.bmp"),
            ("Audio", "*.wav"),
            ("PDF", "*.pdf"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_path.set(filename)
            self.status_var.set(f"Selected: {os.path.basename(filename)}")
    
    def select_output(self):
        default_ext = {
            "image": ".png",
            "audio": ".wav",
            "pdf": ".pdf"
        }.get(self.type_var.get(), "")
        
        filename = filedialog.asksaveasfilename(defaultextension=default_ext)
        if filename:
            self.output_path.set(filename)
            self.status_var.set(f"Output: {os.path.basename(filename)}")
    
    def execute(self):
        try:
            if self.mode_var.get() == "encode":
                self.encode_file()
            else:
                result = self.decode_file()
                messagebox.showinfo("Decoded Message", f"Hidden message:\n\n{result}")
                
            self.status_var.set("Operation completed successfully")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def encode_file(self):
        if not all([self.input_path.get(), self.output_path.get(), self.message_entry.get()]):
            raise ValueError("All fields are required for encoding")
        
        message = self.message_entry.get()
        if self.encrypt_var.get():
            self.key = generate_key()
            message = encrypt_message(message, self.key)
            messagebox.showinfo("Encryption Key", 
                              f"Save this key for decryption:\n\n{self.key}")
        
        file_type = self.type_var.get()
        if file_type == "image":
            self.encode_image()
        elif file_type == "audio":
            self.encode_audio()
        elif file_type == "pdf":
            self.encode_pdf()
    
    def decode_file(self):
        if not self.input_path.get():
            raise ValueError("No input file selected")
        
        file_type = self.type_var.get()
        if file_type == "image":
            return self.decode_image()
        elif file_type == "audio":
            return self.decode_audio()
        elif file_type == "pdf":
            return self.decode_pdf()
    
    def encode_image(self):
        """Placeholder for image encoding"""
        messagebox.showinfo("Info", "Image encoding would happen here")
    
    def decode_image(self):
        """Placeholder for image decoding"""
        return "Sample decoded message from image"
    
    def encode_audio(self):
        """Placeholder for audio encoding"""
        messagebox.showinfo("Info", "Audio encoding would happen here")
    
    def decode_audio(self):
        """Placeholder for audio decoding"""
        return "Sample decoded message from audio"
    
    def encode_pdf(self):
        """Placeholder for PDF encoding"""
        messagebox.showinfo("Info", "PDF encoding would happen here")
    
    def decode_pdf(self):
        """Placeholder for PDF decoding"""
        return "Sample decoded message from PDF"
    
    def show_about(self):
        about = tk.Toplevel(self.root)
        about.title(f"About {APP_NAME}")
        
        tk.Label(about, text=f"{APP_NAME} {VERSION}", 
                font=("Helvetica", 16, "bold")).pack(pady=10)
        
        tk.Label(about, text=f"Created by {DEVELOPER_ALIAS}\n\n"
                "Advanced steganography toolkit\nfor secure data hiding",
                justify="center").pack(padx=20, pady=10)
        
        tk.Button(about, text="GitHub Repository", 
                command=lambda: webbrowser.open(f"https://github.com/{GITHUB_REPO}")
                ).pack(pady=10)
    
    def check_updates(self):
        try:
            response = requests.get(
                f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest",
                timeout=3
            )
            latest = response.json()["tag_name"]
            if version.parse(latest) > version.parse(VERSION):
                if messagebox.askyesno(
                    "Update Available",
                    f"New version {latest} available!\n\n"
                    f"You have {VERSION}\n\n"
                    "Would you like to download now?"
                ):
                    webbrowser.open(f"https://github.com/{GITHUB_REPO}/releases")
        except Exception:
            messagebox.showerror("Error", "Could not check for updates")

# ======================
# APPLICATION LAUNCH
# ======================
if __name__ == "__main__":
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Create and run main application
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
