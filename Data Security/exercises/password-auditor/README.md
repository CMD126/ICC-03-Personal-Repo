# Password Auditor

**Module 3 — Data Security**

An educational Python tool that demonstrates how password hashing works, why unsalted hashes are weak, and how dictionary attacks crack them. Built to understand the security principles behind password storage.

---

## Features

| Option | Description |
|--------|-------------|
| Hash a password | Computes MD5, SHA-1, SHA-256, and SHA-512 hashes side-by-side |
| Hash with salt | Shows how salting produces different hashes for the same password |
| Dictionary attack | Attempts to crack a given hash using a built-in wordlist |
| Speed comparison | Benchmarks hash algorithms to show why fast hashing is bad for passwords |

---

## Usage

```bash
python3 password_auditor.py
```

No external dependencies — uses only Python's built-in `hashlib` and `os` modules.

---

## Example — Dictionary Attack

1. Hash a password using option 1: e.g., hash `password` with SHA-256
2. Copy the resulting hash
3. Go to option 3, choose `sha256`, paste the hash
4. Watch it crack instantly

---

## Concepts Demonstrated

| Concept | Explanation |
|---------|-------------|
| **MD5 / SHA-1** | Broken algorithms — fast to compute, vulnerable to collision and brute-force |
| **SHA-256 / SHA-512** | Stronger, but still too fast for password storage without key stretching |
| **Salting** | Appending random bytes before hashing — defeats rainbow tables and precomputed attacks |
| **Dictionary Attack** | Testing known passwords against a target hash |
| **Hash Speed** | High hash rates (millions/sec) allow attackers to brute-force quickly — bcrypt/PBKDF2/Argon2 slow this down intentionally |

---

## Why This Matters

Storing plaintext passwords is catastrophic. But storing unsalted MD5/SHA-1 hashes is nearly as bad — public databases like [CrackStation](https://crackstation.net) contain billions of precomputed hashes. Proper password storage uses:

- A slow algorithm (bcrypt, PBKDF2, Argon2)
- A unique random salt per user
- A high iteration/cost factor

---

## Requirements

- Python 3.6+
- No external packages needed
