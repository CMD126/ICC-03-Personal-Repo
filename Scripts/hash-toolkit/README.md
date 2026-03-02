# Hash Toolkit — v1.0

A menu-driven Python utility for hash identification, generation, comparison, and file integrity verification. Uses only Python's standard library — no external dependencies.

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | **Identify Hash Type** | Detects hash algorithm by format and length — supports MD5, SHA family, SHA3, BLAKE2b, bcrypt, Argon2, NTLM, MySQL, LDAP, and more |
| 2 | **Generate Hash** | Hashes any string with 9 algorithms (MD5 → SHA3-512 → BLAKE2b); optional salt support |
| 3 | **File Integrity Checker** | Generate all checksums for a file, or verify a file against a known hash — uses `hmac.compare_digest` to prevent timing attacks |
| 4 | **Compare Two Hashes** | Constant-time hash comparison with mismatch character count |
| 5 | **Hash a File** | Hash any file with a chosen algorithm; shows file size and computation time |

---

## Usage

```bash
python3 hash_toolkit.py
```

No root required. No external packages needed.

---

## Supported Algorithms

| # | Algorithm | Digest Length |
|---|-----------|--------------|
| 1 | MD5 | 32 hex |
| 2 | SHA-1 | 40 hex |
| 3 | SHA-224 | 56 hex |
| 4 | SHA-256 | 64 hex |
| 5 | SHA-384 | 96 hex |
| 6 | SHA-512 | 128 hex |
| 7 | SHA3-256 | 64 hex |
| 8 | SHA3-512 | 128 hex |
| 9 | BLAKE2b-256 | 64 hex |

---

## Hash Identifier Coverage

The identifier matches against format and length to detect:

- MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512
- SHA3-256, SHA3-512, BLAKE2b
- bcrypt (`$2a$`, `$2b$`, `$2y$`)
- Argon2 (`$argon2i$`, `$argon2d$`, `$argon2id$`)
- scrypt, PBKDF2-SHA256/512
- NTLM, MySQL323, MySQL5
- DES(Unix), Cisco PIX MD5
- LDAP SHA-1 (`{SHA}`), Salted LDAP SHA-1 (`{SSHA}`)

---

## Notes

- Hash comparison uses `hmac.compare_digest` — safe against timing-based side-channel attacks.
- File integrity checking auto-detects the algorithm from the known hash length.
- Salt is prepended to the input string when generating hashes (`salt + text`).
