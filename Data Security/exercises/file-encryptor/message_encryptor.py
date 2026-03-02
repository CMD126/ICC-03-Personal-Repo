#!/usr/bin/python3
from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken


# ---------------------------------------------------------------------------
# Key Management
# ---------------------------------------------------------------------------

def write_key():
    """Generate a Fernet key and save it to key.key."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("[+] Key generated and saved to key.key")


def load_key() -> bytes | None:
    """Load key.key from disk. Returns None if the file does not exist."""
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("[!] key.key not found. Generate one first (option 1).")
        return None


# ---------------------------------------------------------------------------
# Encrypt / Decrypt
# ---------------------------------------------------------------------------

def encrypt_message():
    key = load_key()
    if key is None:
        return
    f = Fernet(key)
    msg = input("Enter message to encrypt: ")
    encrypted = f.encrypt(msg.encode())
    print("\n[+] Encrypted message (share this):")
    print(encrypted.decode())


def decrypt_message():
    key = load_key()
    if key is None:
        return
    f = Fernet(key)
    ciphertext = input("Paste the encrypted message: ").encode()
    try:
        decrypted = f.decrypt(ciphertext)
        print("\n[+] Decrypted message:")
        print(decrypted.decode())
    except InvalidToken:
        print("[!] Decryption failed — wrong key or corrupted message.")


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def main():
    print("\n1 - Generate key")
    print("2 - Encrypt message")
    print("3 - Decrypt message")
    option = input("Choose an option: ").strip()

    if option == "1":
        write_key()
    elif option == "2":
        encrypt_message()
    elif option == "3":
        decrypt_message()
    else:
        print("[!] Invalid option.")


if __name__ == "__main__":
    main()
