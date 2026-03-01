#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, Menu
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import threading
import struct
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SALT_SIZE  = 16
KEY_LENGTH = 32
CHUNK_SIZE = 1024 * 1024            # 1 MB plaintext per chunk
SCRIPT_DIR = Path(__file__).parent  # always relative to this file, not cwd
SALT_PATH  = SCRIPT_DIR / "salt.bin"

# ---------------------------------------------------------------------------
# Key derivation
# ---------------------------------------------------------------------------

def derive_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(SALT_SIZE)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=480_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def save_salt(salt: bytes) -> None:
    SALT_PATH.write_bytes(salt)


def load_salt() -> bytes | None:
    if not SALT_PATH.exists():
        return None
    return SALT_PATH.read_bytes()


# ---------------------------------------------------------------------------
# Chunked I/O helpers
#
# BUG FIX: Fernet tokens are variable-length (plaintext + ~73 bytes overhead).
# Reading fixed-size chunks from an encrypted file cuts mid-token → InvalidToken.
#
# Fix: prefix every encrypted chunk with its 4-byte big-endian length so the
# decryptor always reads exactly one complete Fernet token per iteration.
#
# Format per chunk:  [4 bytes: token length][token bytes]
# ---------------------------------------------------------------------------

def write_chunk(dst, encrypted_chunk: bytes) -> None:
    dst.write(struct.pack(">I", len(encrypted_chunk)))
    dst.write(encrypted_chunk)


def read_chunk(src) -> bytes | None:
    """Read one length-prefixed chunk. Returns None at EOF."""
    header = src.read(4)
    if len(header) < 4:
        return None
    length = struct.unpack(">I", header)[0]
    return src.read(length)


# ---------------------------------------------------------------------------
# GUI Application
# ---------------------------------------------------------------------------

class CryptoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("LEXCRYPT")
        self.root.geometry("1200x800")
        self.root.configure(bg="#000000")
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._setup_style()

        self.custom_key: bytes | None = None

        self._create_widgets()
        self._create_menu()

    # ------------------------------------------------------------------ style

    def _setup_style(self) -> None:
        bg     = "#000000"
        fg     = "#00ffff"
        accent = "#00ffff"
        dark   = "#001f1f"

        self.style.configure(".", background=bg, foreground=fg, font=("Arial", 10))
        self.style.configure("TButton", padding=10, font=("Arial", 11))
        self.style.map("TButton",
                       background=[("active", accent), ("pressed", "#00cccc")],
                       foreground=[("active", "black")])
        self.style.configure("Header.TLabel", font=("Arial", 28), foreground=accent)
        self.style.configure("Sub.TLabel",    font=("Arial", 11), foreground="#00cccc")
        self.style.configure("Card.TFrame",   background=dark, relief="flat")
        self.style.configure("Progress.TProgressbar",
                             thickness=6, background=accent, troughcolor="#003333")

    # ---------------------------------------------------------------- widgets

    def _create_widgets(self) -> None:
        header = tk.Frame(self.root, bg="#000000")
        header.pack(fill=tk.X, pady=20)
        tk.Label(header, text="LEXCRYPT",
                 font=("Arial", 32), fg="#00ffff", bg="#000000").pack()

        main = tk.Frame(self.root, bg="#000000")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        left = tk.Frame(main, bg="#000000")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        actions = [
            ("Set Master Password", self.set_master_password, "Create vault"),
            ("Load Key",            self.load_key,            "Import .key file"),
            ("Encrypt Message",     self.encrypt_message,     "Encrypt text → file"),
            ("Decrypt Message",     self.decrypt_message,     "Decrypt file → text"),
            ("Encrypt Files",       self.encrypt_files,       "Encrypt files"),
            ("Decrypt Files",       self.decrypt_files,       "Decrypt .enc files"),
        ]

        for text, cmd, desc in actions:
            card = tk.Frame(left, bg="#001f1f", bd=1, relief="solid")
            card.pack(pady=10, fill=tk.X)
            ttk.Button(card, text=text, command=cmd).pack(pady=5)
            tk.Label(card, text=desc, fg="#00cccc", bg="#001f1f").pack()

        right = tk.Frame(main, bg="#000000")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        info_card = tk.Frame(right, bg="#001f1f", bd=1, relief="solid")
        info_card.pack(fill=tk.X, pady=10)
        tk.Label(info_card, text="Status", fg="#00ffff", bg="#001f1f").pack()
        self.status_label = tk.Label(info_card, text="Ready",
                                     fg="#00ffff", bg="#001f1f")
        self.status_label.pack()

        self.progress = ttk.Progressbar(right, mode="determinate")
        self.progress.pack(fill=tk.X, pady=10)
        self.progress.pack_forget()

        log_frame = tk.Frame(right, bg="#001f1f", bd=1, relief="solid")
        log_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(log_frame, text="Log", fg="#00ffff", bg="#001f1f").pack()

        self.log = tk.Text(log_frame, state=tk.DISABLED,
                           bg="#000000", fg="#00ffff", font=("Arial", 10))
        self.log.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.config(yscrollcommand=scrollbar.set)

    def _create_menu(self) -> None:
        menubar = Menu(self.root)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Decrypt Files", command=self.decrypt_files)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    # ---------------------------------------------------------------- logging

    def log_message(self, msg: str, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f"[{timestamp} | {level}] {msg}\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def update_status(self, msg: str) -> None:
        self.status_label.config(text=msg)

    # ------------------------------------------------------------------- keys

    def set_master_password(self) -> None:
        # Warn user if vault already exists — new salt = old files unreadable
        if SALT_PATH.exists():
            if not messagebox.askyesno(
                "Warning",
                "A vault already exists.\n"
                "Creating a new password changes the key — "
                "files encrypted with the old password will be unreadable.\n\n"
                "Continue?"
            ):
                return

        pwd1 = simpledialog.askstring("Setup", "Password:", show="*")
        if not pwd1 or len(pwd1) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return

        pwd2 = simpledialog.askstring("Confirm", "Confirm password:", show="*")
        if pwd1 != pwd2:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        salt = os.urandom(SALT_SIZE)
        save_salt(salt)
        self.custom_key = None
        self.log_message("Vault created — salt.bin saved.", "SUCCESS")
        self.update_status("Ready")

    def get_key(self) -> bytes | None:
        if self.custom_key:
            return self.custom_key
        if not SALT_PATH.exists():
            messagebox.showwarning("No Vault", "Set a master password first.")
            return None
        password = simpledialog.askstring("Unlock", "Password:", show="*")
        if not password:
            return None
        salt = load_salt()
        key, _ = derive_key(password, salt)
        return key

    def load_key(self) -> None:
        file = filedialog.askopenfilename(title="Load Key File")
        if not file:
            return
        try:
            key = Path(file).read_bytes()
            Fernet(key)                   # validate before storing
            self.custom_key = key
            self.log_message("Key loaded successfully.", "SUCCESS")
            self.update_status("Custom key active")
        except Exception as exc:
            messagebox.showerror("Error", f"Invalid key file:\n{exc}")

    # ----------------------------------------------- message encrypt/decrypt

    def encrypt_message(self) -> None:
        key = self.get_key()
        if not key:
            return
        msg = simpledialog.askstring("Input", "Message to encrypt:")
        if not msg:
            return
        token = Fernet(key).encrypt(msg.encode())
        save_path = filedialog.asksaveasfilename(
            title="Save Encrypted Token", defaultextension=".enc")
        if save_path:
            Path(save_path).write_bytes(token)
            self.log_message(f"Message encrypted → {os.path.basename(save_path)}", "SUCCESS")

    def decrypt_message(self) -> None:
        key = self.get_key()
        if not key:
            return
        token_path = filedialog.askopenfilename(title="Select Encrypted Token")
        if not token_path:
            return
        token = Path(token_path).read_bytes()
        try:
            msg = Fernet(key).decrypt(token).decode()
        except InvalidToken:
            messagebox.showerror("Error",
                                 "Decryption failed — wrong password or corrupted file.")
            return
        save_path = filedialog.asksaveasfilename(
            title="Save Decrypted Message", defaultextension=".txt")
        if save_path:
            Path(save_path).write_text(msg, encoding="utf-8")
            self.log_message(f"Message decrypted → {os.path.basename(save_path)}", "SUCCESS")

    # ------------------------------------------------- file encrypt/decrypt

    def encrypt_files(self) -> None:
        key = self.get_key()
        if not key:
            return
        files = filedialog.askopenfilenames(title="Select Files to Encrypt")
        if not files:
            return
        # Collect save paths on MAIN thread before spawning worker
        pairs = self._collect_save_paths(files, encrypt=True)
        if not pairs:
            return
        self._start_progress(len(pairs))
        threading.Thread(target=self._process_files,
                         args=(key, pairs, True), daemon=True).start()

    def decrypt_files(self) -> None:
        key = self.get_key()
        if not key:
            return
        files = filedialog.askopenfilenames(title="Select Files to Decrypt")
        if not files:
            return
        pairs = self._collect_save_paths(files, encrypt=False)
        if not pairs:
            return
        self._start_progress(len(pairs))
        threading.Thread(target=self._process_files,
                         args=(key, pairs, False), daemon=True).start()

    def _collect_save_paths(
        self, files: tuple, encrypt: bool
    ) -> list[tuple[str, str]]:
        """
        Ask for a save path per file. Must run on the main thread.
        Returns list of (src, dst) pairs.
        """
        pairs = []
        mode  = "Encrypt" if encrypt else "Decrypt"
        for src in files:
            base    = os.path.basename(src)
            default = (base + ".enc") if encrypt else base.removesuffix(".enc")
            dst = filedialog.asksaveasfilename(
                title=f"{mode}: {base}", initialfile=default)
            if dst:
                pairs.append((src, dst))
        return pairs

    def _process_files(
        self, key: bytes, pairs: list[tuple[str, str]], encrypt: bool
    ) -> None:
        """
        Worker thread — encrypts or decrypts each (src, dst) pair.

        Uses length-prefixed chunks so decryption reads exactly one
        complete Fernet token per iteration (fixes the InvalidToken bug).
        """
        fernet  = Fernet(key)
        success = 0
        mode    = "Encrypt" if encrypt else "Decrypt"

        for i, (src, dst) in enumerate(pairs):
            base = os.path.basename(src)
            try:
                with open(src, "rb") as src_f, open(dst, "wb") as dst_f:
                    if encrypt:
                        while chunk := src_f.read(CHUNK_SIZE):
                            write_chunk(dst_f, fernet.encrypt(chunk))
                    else:
                        while (enc_chunk := read_chunk(src_f)) is not None:
                            dst_f.write(fernet.decrypt(enc_chunk))
                success += 1
                self.root.after(0, self.log_message,
                                f"{mode}ed: {base}", "SUCCESS")
            except InvalidToken:
                self.root.after(0, messagebox.showerror, "Error",
                                f"Wrong password or corrupted file:\n{base}")
            except Exception as exc:
                self.root.after(0, messagebox.showerror, "Error",
                                f"{base}:\n{exc}")
            finally:
                self.root.after(0, self._update_progress, i + 1)

        self.root.after(0, messagebox.showinfo, "Complete",
                        f"{success}/{len(pairs)} files {mode.lower()}ed.")
        self.root.after(0, self._stop_progress)

    # ----------------------------------------------------------- progress bar

    def _start_progress(self, total: int) -> None:
        self.progress["maximum"] = total
        self.progress["value"]   = 0
        self.progress.pack(fill=tk.X, pady=10)
        self.update_status("Processing…")

    def _update_progress(self, value: int) -> None:
        self.progress["value"] = value

    def _stop_progress(self) -> None:
        self.progress.pack_forget()
        self.update_status("Ready")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
