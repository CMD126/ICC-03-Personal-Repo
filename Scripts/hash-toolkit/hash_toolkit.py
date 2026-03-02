#!/usr/bin/env python3
"""
Hash Toolkit — v1.0
Identify, generate, compare hashes and verify file integrity.
"""

import hashlib
import hmac
import os
import re
import sys
import time

# ── Colours ────────────────────────────────────────────────────────────────────
R = "\033[0;31m"; G = "\033[0;32m"; Y = "\033[0;33m"
B = "\033[0;34m"; C = "\033[0;36m"; W = "\033[1;37m"; N = "\033[0m"

BANNER = f"""{C}
  ██╗  ██╗ █████╗ ███████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗
  ██║  ██║██╔══██╗██╔════╝██║  ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
  ███████║███████║███████╗███████║       ██║   ██║   ██║██║   ██║██║
  ██╔══██║██╔══██║╚════██║██╔══██║       ██║   ██║   ██║██║   ██║██║
  ██║  ██║██║  ██║███████║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
{N}{W}  Hash Toolkit v1.0  —  Identify · Generate · Compare · Verify{N}
"""

# ── Hash signatures ─────────────────────────────────────────────────────────
HASH_SIGNATURES = [
    (r"^\$2[aby]\$\d{2}\$.{53}$",               "bcrypt"),
    (r"^\$argon2(i|d|id)\$",                    "Argon2"),
    (r"^\$scrypt\$",                            "scrypt"),
    (r"^\$pbkdf2-sha(256|512)\$",              "PBKDF2"),
    (r"^[0-9a-fA-F]{128}$",                    "SHA-512"),
    (r"^[0-9a-fA-F]{96}$",                     "SHA-384"),
    (r"^[0-9a-fA-F]{64}$",                     "SHA-256"),
    (r"^[0-9a-fA-F]{56}$",                     "SHA-224"),
    (r"^[0-9a-fA-F]{40}$",                     "SHA-1 / RipeMD-160"),
    (r"^[0-9a-fA-F]{32}$",                     "MD5 / MD4 / NTLM"),
    (r"^[0-9a-fA-F]{16}$",                     "MySQL323 / DES(Unix)"),
    (r"^[a-fA-F0-9]{8}:[a-fA-F0-9]{8}$",       "Cisco PIX MD5"),
    (r"^\{SHA\}[A-Za-z0-9+/=]{28}$",           "SHA-1 (LDAP)"),
    (r"^\{SSHA\}[A-Za-z0-9+/=]{40}$",          "Salted SHA-1 (LDAP)"),
    (r"^[A-Za-z0-9./]{13}$",                   "DES(Unix)"),
    (r"^\*[0-9A-F]{40}$",                      "MySQL5 SHA-1"),
]

ALGORITHMS = {
    "1": ("MD5",     hashlib.md5),
    "2": ("SHA-1",   hashlib.sha1),
    "3": ("SHA-224", hashlib.sha224),
    "4": ("SHA-256", hashlib.sha256),
    "5": ("SHA-384", hashlib.sha384),
    "6": ("SHA-512", hashlib.sha512),
    "7": ("SHA3-256",hashlib.sha3_256),
    "8": ("SHA3-512",hashlib.sha3_512),
    "9": ("BLAKE2b", lambda: hashlib.blake2b(digest_size=32)),
}

# ── Helpers ──────────────────────────────────────────────────────────────────
def separator(char="─", width=60):
    print(f"{B}{char * width}{N}")

def pause():
    input(f"\n{Y}Press Enter to return to menu...{N}")

def hash_bytes(data: bytes, algo_fn) -> str:
    return algo_fn(data).hexdigest()

def hash_string(text: str, algo_fn) -> str:
    return hash_bytes(text.encode(), algo_fn)

def hash_file(path: str, algo_fn) -> str:
    h = algo_fn()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# ── Feature 1: Identify hash ─────────────────────────────────────────────────
def identify_hash():
    separator()
    print(f"{W}  HASH IDENTIFIER{N}")
    separator()
    h = input(f"\n{C}Enter hash: {N}").strip()
    if not h:
        print(f"{R}No input.{N}")
        pause(); return

    matched = []
    for pattern, name in HASH_SIGNATURES:
        if re.match(pattern, h):
            matched.append(name)

    print()
    if matched:
        print(f"{G}Possible hash type(s):{N}")
        for m in matched:
            print(f"  {Y}→{N}  {W}{m}{N}")
        print(f"\n  Length: {len(h)} characters")
    else:
        print(f"{R}Unknown hash format.{N}")
        print(f"  Length: {len(h)} characters")
    pause()

# ── Feature 2: Generate hash ─────────────────────────────────────────────────
def generate_hash():
    separator()
    print(f"{W}  HASH GENERATOR{N}")
    separator()
    print(f"\n{W}Available algorithms:{N}")
    for k, (name, _) in ALGORITHMS.items():
        print(f"  {Y}{k}{N}. {name}")
    print()
    choice = input(f"{C}Select algorithm [1-9]: {N}").strip()
    if choice not in ALGORITHMS:
        print(f"{R}Invalid choice.{N}"); pause(); return

    name, fn = ALGORITHMS[choice]
    text = input(f"{C}Enter text to hash: {N}")
    salt = input(f"{C}Add salt? (leave blank to skip): {N}").strip()

    data = (salt + text) if salt else text
    digest = hash_string(data, fn)

    print(f"\n{G}Algorithm : {N}{name}")
    if salt:
        print(f"{G}Salt      : {N}{salt}")
    print(f"{G}Input     : {N}{text}")
    print(f"{G}Hash      : {N}{W}{digest}{N}")
    pause()

# ── Feature 3: File integrity ─────────────────────────────────────────────────
def file_integrity():
    separator()
    print(f"{W}  FILE INTEGRITY CHECKER{N}")
    separator()
    print(f"\n  {Y}1{N}. Generate checksum for a file")
    print(f"  {Y}2{N}. Verify file against known checksum")
    print()
    sub = input(f"{C}Choice [1-2]: {N}").strip()

    if sub == "1":
        path = input(f"\n{C}File path: {N}").strip().strip('"')
        if not os.path.isfile(path):
            print(f"{R}File not found.{N}"); pause(); return
        print(f"\n{W}Generating checksums...{N}\n")
        for k, (name, fn) in ALGORITHMS.items():
            if k in ("1","2","4","6"):   # MD5, SHA-1, SHA-256, SHA-512
                t0 = time.time()
                digest = hash_file(path, fn)
                elapsed = time.time() - t0
                print(f"  {Y}{name:<10}{N}  {digest}  {B}({elapsed*1000:.1f}ms){N}")

    elif sub == "2":
        path = input(f"\n{C}File path: {N}").strip().strip('"')
        if not os.path.isfile(path):
            print(f"{R}File not found.{N}"); pause(); return
        known = input(f"{C}Known hash: {N}").strip().lower()
        length = len(known)
        if length == 32:
            fn = hashlib.md5; alg = "MD5"
        elif length == 40:
            fn = hashlib.sha1; alg = "SHA-1"
        elif length == 64:
            fn = hashlib.sha256; alg = "SHA-256"
        elif length == 128:
            fn = hashlib.sha512; alg = "SHA-512"
        else:
            print(f"{Y}Unknown hash length ({length}). Using SHA-256.{N}")
            fn = hashlib.sha256; alg = "SHA-256"

        print(f"\n{W}Verifying with {alg}...{N}")
        actual = hash_file(path, fn)
        match = hmac.compare_digest(actual, known)
        print(f"\n  Expected : {known}")
        print(f"  Actual   : {actual}")
        if match:
            print(f"\n  {G}[PASS] Hashes match — file integrity verified.{N}")
        else:
            print(f"\n  {R}[FAIL] Hashes do NOT match — file may be corrupted or tampered.{N}")
    else:
        print(f"{R}Invalid choice.{N}")
    pause()

# ── Feature 4: Compare hashes ─────────────────────────────────────────────────
def compare_hashes():
    separator()
    print(f"{W}  HASH COMPARATOR{N}")
    separator()
    h1 = input(f"\n{C}Hash 1: {N}").strip().lower()
    h2 = input(f"{C}Hash 2: {N}").strip().lower()
    match = hmac.compare_digest(h1, h2)
    print()
    if match:
        print(f"  {G}[MATCH] Hashes are identical.{N}")
    else:
        print(f"  {R}[MISMATCH] Hashes differ.{N}")
        diffs = sum(a != b for a, b in zip(h1, h2)) + abs(len(h1) - len(h2))
        print(f"  Differing characters: {diffs} / {max(len(h1),len(h2))}")
    pause()

# ── Feature 5: Hash a file with chosen algorithm ──────────────────────────────
def hash_file_menu():
    separator()
    print(f"{W}  HASH A FILE{N}")
    separator()
    path = input(f"\n{C}File path: {N}").strip().strip('"')
    if not os.path.isfile(path):
        print(f"{R}File not found.{N}"); pause(); return

    print(f"\n{W}Algorithm:{N}")
    for k, (name, _) in ALGORITHMS.items():
        print(f"  {Y}{k}{N}. {name}")
    choice = input(f"\n{C}Select [1-9]: {N}").strip()
    if choice not in ALGORITHMS:
        print(f"{R}Invalid choice.{N}"); pause(); return

    name, fn = ALGORITHMS[choice]
    size = os.path.getsize(path)
    t0 = time.time()
    digest = hash_file(path, fn)
    elapsed = time.time() - t0

    print(f"\n{G}File      : {N}{path}")
    print(f"{G}Size      : {N}{size:,} bytes")
    print(f"{G}Algorithm : {N}{name}")
    print(f"{G}Hash      : {N}{W}{digest}{N}")
    print(f"{G}Time      : {N}{elapsed*1000:.2f}ms")
    pause()

# ── Menu ──────────────────────────────────────────────────────────────────────
def menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER)
        separator()
        print(f"  {Y}1{N}.  Identify Hash Type")
        print(f"  {Y}2{N}.  Generate Hash (string)")
        print(f"  {Y}3{N}.  File Integrity Checker")
        print(f"  {Y}4{N}.  Compare Two Hashes")
        print(f"  {Y}5{N}.  Hash a File")
        separator()
        print(f"  {Y}0{N}.  Exit")
        separator()
        choice = input(f"\n{C}Select option: {N}").strip()
        if   choice == "1": identify_hash()
        elif choice == "2": generate_hash()
        elif choice == "3": file_integrity()
        elif choice == "4": compare_hashes()
        elif choice == "5": hash_file_menu()
        elif choice == "0":
            print(f"\n{G}Goodbye.{N}\n"); sys.exit(0)
        else:
            print(f"{R}Invalid option.{N}"); time.sleep(1)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n\n{Y}Interrupted.{N}\n")
        sys.exit(0)
