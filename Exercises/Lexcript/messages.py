#!/usr/bin/python3

from cryptography.fernet import Fernet

# KEY GENERATION 

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("Key generated and saved to key.key")

def load_key():
    return open("key.key", "rb").read()


# ENCRYPT MESSAGE 

def encrypt_message():
    key = load_key()
    f = Fernet(key)

    msg = input("Enter message to encrypt: ")
    encrypted = f.encrypt(msg.encode())

    print("\nEncrypted message (send this to your partner):")
    print(encrypted.decode())

# DECRYPT MESSAGE 

def decrypt_message():
    key = load_key()
    f = Fernet(key)

    ciphertext = input("Paste the received encrypted message: ").encode()
    decrypted = f.decrypt(ciphertext)

    print("\nDecrypted message:")
    print(decrypted.decode())

# Menu
print("1 - Generate key")
print("2 - Encrypt message")
print("3 - Decrypt message")
option = input("Choose an option: ")

if option == "1":
    write_key()
elif option == "2":
    encrypt_message()
elif option == "3":
    decrypt_message()
else:
    print("Invalid option.")
