# LEXCRYPT

Desktop app for symmetric encryption using Fernet (Python Cryptography).

## Assignment Requirements (ICC-03: Task 06)

**Objective**: Explore symmetric encryption with Fernet for secure messaging and file encryption.

### Tasks Implemented:
1. **Secure Messaging System**:
   - Generate key via password + PBKDF2.
   - Encrypt text message.
   - Decrypt received message.

2. **Secure File Encryption**:
   - Encrypt any file type.
   - Decrypt `.enc` files.
   - Support for multiple files.

3. **Bonus Challenges**:
   - GUI with Tkinter.
   - PBKDF2 key derivation (no direct key storage).
   - Chunked processing (1MB) for large files.
   - Threaded operations (non-blocking UI).

---

## How to Use

### Requirements
```bash
pip install cryptography
```
*(Tkinter is included with Python)*

### Usage
1. Run:
   ```bash
   python lexcrypt.py
   ```

2. **Set Master Password**:
   - Click "Set Master Password".
   - Enter and confirm a password (min. 8 chars).
   - Generates `salt.bin` and derives key using PBKDF2.

3. **Encrypt/Decrypt**:
   - **Messages**: Use "Encrypt Message" / "Decrypt Message".
   - **Files**: Use "Encrypt Files" / "Decrypt Files" (multiple files supported).

4. **Custom Key (Optional)**:
   - Click "Load Key" to import a `.key` file.

---

## Notes
- Encrypted files get `.enc` extension.
- Uses 480,000 PBKDF2 iterations (secure).
- GUI includes log, progress bar, and animation.
- No direct key storage — only `salt.bin`.