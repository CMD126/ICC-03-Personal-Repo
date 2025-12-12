# ransomware_py

Educational ransomware simulation written in Python.  
This project is for learning and cybersecurity training only, demonstrating file discovery, encryption, and UI behaviors in a controlled environment.

---

## Disclaimer

**Do not run this script on a real machine.  
Use only inside a virtual machine or isolated test environment.**

The script modifies files and can change system wallpaper.  
It is intended solely for educational, defensive, and research purposes.

---

## About the Project

This project simulates the core behavior of a basic ransomware:

- Scanning directories  
- Encrypting individual files or entire folders  
- Encrypting/decrypting messages  
- Generating a “README” wallpaper  
- Showing a fullscreen popup to simulate a lockscreen

The goal is to help students understand ransomware mechanics, cryptography usage, and basic GUI manipulation, improving defensive and analytical skills.

---

## Menu Functions

| Option | Function Name           | Description |
|--------|------------------------|-------------|
| 1      | `encrypt_message()`     | Encrypts a text message input by the user. |
| 2      | `decrypt_message()`     | Decrypts a previously encrypted message. |
| 3      | `encrypt_file()`        | Encrypts a single file, creating a `.enc` version. |
| 4      | `decrypt_file()`        | Decrypts a previously encrypted `.enc` file. |
| 5      | `encrypt_folder()`      | Recursively encrypts all files in a folder (skipping `.enc` files). |
| 6      | `decrypt_folder()`      | Recursively decrypts all `.enc` files in a folder. |
| 7      | `generate_readme_wallpaper()` & `show_popup()` | Creates a wallpaper with "README please" and shows a fullscreen popup window. |
| 8      | Exit                     | Closes the program safely. |

---

## Dependencies

Install required Python libraries via pip:

```bash
pip install cryptography pillow
