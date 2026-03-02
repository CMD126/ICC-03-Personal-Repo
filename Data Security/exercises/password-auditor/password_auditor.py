#!/usr/bin/env python3
"""
Password Auditor - Hash Analysis & Dictionary Attack Simulator
ICC-03 Cybersecurity Program | Module 3: Data Security

Demonstrates:
- Common hashing algorithms (MD5, SHA-1, SHA-256, SHA-512)
- How unsalted hashes are vulnerable to dictionary attacks
- The importance of salting passwords
- Speed differences between algorithms (why bcrypt/PBKDF2 matters)
"""

import hashlib
import os
import time

BANNER = """
╔═══════════════════════════════════════╗
║        PASSWORD AUDITOR v1.0          ║
║  Hash Analysis & Dictionary Attack    ║
║        Educational Use Only           ║
╚═══════════════════════════════════════╝
"""

# Built-in wordlist simulating a common passwords dictionary
WORDLIST = [
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "abc123", "monkey", "dragon", "111111",
    "baseball", "iloveyou", "trustno1", "sunshine", "master",
    "welcome", "shadow", "login", "princess", "passw0rd",
    "starwars", "hello", "freedom", "whatever", "qazwsx",
    "michael", "football", "superman", "batman", "charlie",
]


def hash_password(password: str, algorithm: str, salt: bytes = None) -> tuple:
    """Hash a password using the specified algorithm, with optional salt."""
    data = password.encode()
    if salt:
        data = salt + data

    if algorithm == "md5":
        digest = hashlib.md5(data).hexdigest()
    elif algorithm == "sha1":
        digest = hashlib.sha1(data).hexdigest()
    elif algorithm == "sha256":
        digest = hashlib.sha256(data).hexdigest()
    elif algorithm == "sha512":
        digest = hashlib.sha512(data).hexdigest()
    else:
        print(f"[!] Unknown algorithm: {algorithm}")
        return None, salt

    return digest, salt


def menu_hash_password():
    """Hash a password and display results across all algorithms."""
    password = input("\nEnter password to hash: ").strip()
    if not password:
        print("[!] No password entered.")
        return

    print(f"\n  {'Algorithm':<10} {'Hash'}")
    print("  " + "-" * 80)
    for algo in ["md5", "sha1", "sha256", "sha512"]:
        digest, _ = hash_password(password, algo)
        print(f"  {algo.upper():<10} {digest}")

    print("\n  [!] MD5 and SHA-1 are considered cryptographically broken.")
    print("  [!] Use SHA-256 or stronger for any security-sensitive purpose.")


def menu_hash_with_salt():
    """Demonstrate salted hashing and why it defeats rainbow tables."""
    password = input("\nEnter password to hash: ").strip()
    if not password:
        print("[!] No password entered.")
        return

    salt = os.urandom(16)
    digest_unsalted, _ = hash_password(password, "sha256")
    digest_salted, _ = hash_password(password, "sha256", salt)

    print(f"\n  Password         : {password}")
    print(f"  SHA-256 (no salt): {digest_unsalted}")
    print(f"  Salt (hex)       : {salt.hex()}")
    print(f"  SHA-256 (salted) : {digest_salted}")
    print()
    print("  [+] Two users with the same password produce DIFFERENT salted hashes.")
    print("  [+] Without the salt, precomputed rainbow tables are useless.")
    print("  [+] Each login attempt must recompute: hash(salt + password).")


def menu_dictionary_attack():
    """Simulate a dictionary attack against an unsalted hash."""
    print("\n  Available algorithms: md5 / sha1 / sha256 / sha512")
    algorithm = input("  Algorithm used: ").strip().lower()
    if algorithm not in ("md5", "sha1", "sha256", "sha512"):
        print("[!] Invalid algorithm.")
        return

    target_hash = input("  Target hash: ").strip().lower()
    if not target_hash:
        print("[!] No hash entered.")
        return

    print(f"\n  [*] Running dictionary attack ({len(WORDLIST)} words)...\n")
    start = time.time()
    found = None

    for word in WORDLIST:
        candidate, _ = hash_password(word, algorithm)
        if candidate == target_hash:
            found = word
            break

    elapsed = time.time() - start

    if found:
        print(f"  [+] Password CRACKED: '{found}'")
        print(f"  [+] Time taken: {elapsed:.4f}s")
    else:
        print(f"  [-] Password not found in wordlist ({elapsed:.4f}s).")
        print("  [-] Try a larger wordlist or check the algorithm.")

    print()
    print("  [!] This shows why common passwords are dangerous even when hashed.")
    print("  [!] Real attackers use millions of words, rules, and GPU acceleration.")
    print()

    if not found:
        print("  TIP — Try hashing one of these with the chosen algorithm above:")
        for w in WORDLIST[:5]:
            digest, _ = hash_password(w, algorithm)
            print(f"    {w:<15} -> {digest}")


def menu_compare_speed():
    """Compare hashing speed across algorithms to show cost differences."""
    password = "benchmark_test_password"
    iterations = 200_000

    print(f"\n  Hashing '{password}' {iterations:,} times per algorithm...\n")

    for algo in ["md5", "sha1", "sha256", "sha512"]:
        start = time.time()
        for _ in range(iterations):
            hash_password(password, algo)
        elapsed = time.time() - start
        rate = iterations / elapsed
        print(f"  {algo.upper():<8}  {elapsed:.3f}s   ({rate:>12,.0f} hashes/sec)")

    print()
    print("  [!] Fast hashing = BAD for passwords.")
    print("  [!] Attackers exploit high hash rates to brute-force credentials.")
    print("  [!] bcrypt, PBKDF2, and Argon2 are intentionally slow — that's the point.")


def main():
    print(BANNER)
    while True:
        print("  === MENU ===")
        print("  1) Hash a password (MD5 / SHA-1 / SHA-256 / SHA-512)")
        print("  2) Hash with salt — why salting matters")
        print("  3) Dictionary attack simulation")
        print("  4) Compare hashing speed across algorithms")
        print("  5) Exit")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            menu_hash_password()
        elif choice == "2":
            menu_hash_with_salt()
        elif choice == "3":
            menu_dictionary_attack()
        elif choice == "4":
            menu_compare_speed()
        elif choice == "5":
            print("\n  Exiting. Stay secure!\n")
            break
        else:
            print("  [!] Invalid option.\n")


if __name__ == "__main__":
    main()
