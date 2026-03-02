# Data Security

Encryption, hashing, key management, and data protection techniques.

---

## Notes

### Encryption Types

| Type | Description | Examples |
|------|-------------|---------|
| Symmetric | Same key for encrypt/decrypt | AES, ChaCha20 |
| Asymmetric | Public/private key pair | RSA, ECC |
| Hybrid | Asymmetric key exchange + symmetric encryption | TLS, PGP |

### Hashing

| Algorithm | Length | Use |
|-----------|--------|-----|
| MD5 | 128-bit | Legacy only — broken |
| SHA-1 | 160-bit | Deprecated |
| SHA-256 | 256-bit | General purpose |
| SHA-512 | 512-bit | High security |
| bcrypt | Variable | Password storage |
| Argon2 | Variable | Password storage (recommended) |

### Data Classification

| Level | Description |
|-------|-------------|
| Public | No restrictions |
| Internal | Company-only |
| Confidential | Limited access, business-sensitive |
| Restricted | Highly sensitive, legal/regulatory requirements |

→ [View full cheat sheet](../Data%20Security/notes/README.md)

---

## Exercises

> **Note:** The ransomware simulator must only be run in a controlled VM environment.

### file-encryptor
Python GUI app for file and message encryption/decryption.
- Key derivation: PBKDF2-SHA256
- Cipher: Fernet (AES-128-CBC)
- Supports large files with chunked I/O

→ [View exercise](../Data%20Security/exercises/file-encryptor/)

### password-auditor
Demonstrates why weak hashing is dangerous.
- Compares MD5, SHA-1, SHA-256, SHA-512, bcrypt speed
- Shows salting in practice
- Simulates a dictionary attack

→ [View exercise](../Data%20Security/exercises/password-auditor/)

### ransomware-simulator ⚠️
Educational ransomware simulation — VM only.
- Encrypts files in a target directory
- Generates a ransom wallpaper
- Fullscreen popup with decrypt key input

→ [View exercise](../Data%20Security/exercises/ransomware-simulator/)

---

[← Home](Home)
