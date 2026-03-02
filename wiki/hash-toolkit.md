# hash-toolkit — v1.0

Menu-driven Python utility for hash identification, generation, comparison, and file integrity verification. No external dependencies.

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | Identify Hash Type | Detects algorithm by format and length — supports 20+ types |
| 2 | Generate Hash | Hashes any string with 9 algorithms; optional salt support |
| 3 | File Integrity Checker | Generate checksums for a file, or verify against a known hash |
| 4 | Compare Two Hashes | Constant-time comparison with mismatch character count |
| 5 | Hash a File | Hash any file with a chosen algorithm; shows size and timing |

---

## Supported Algorithms

| # | Algorithm | Digest |
|---|-----------|--------|
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

Identifies: MD5, SHA family, SHA3, BLAKE2b, bcrypt, Argon2, scrypt, PBKDF2, NTLM, MySQL323, MySQL5, DES(Unix), Cisco PIX, LDAP SHA-1, Salted LDAP SHA-1.

---

## Usage

```bash
python3 hash_toolkit.py
```

No root required. No external packages needed.

---

## Security Notes

- Hash comparison uses `hmac.compare_digest` — safe against timing-based side-channel attacks.
- File integrity auto-detects algorithm from known hash length.

---

→ [View source](../Scripts/hash-toolkit/) | [← Home](Home)
