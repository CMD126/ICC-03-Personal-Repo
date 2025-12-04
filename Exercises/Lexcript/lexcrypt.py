#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, Menu
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import threading
import math
from datetime import datetime

SALT_SIZE = 16
KEY_LENGTH = 32
CHUNK_SIZE = 1024 * 1024  # 1MB

def derive_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(SALT_SIZE)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def save_salt(salt: bytes):
    with open("salt.bin", "wb") as f:
        f.write(salt)

def load_salt() -> bytes:
    if not os.path.exists("salt.bin"):
        return None
    with open("salt.bin", "rb") as f:
        return f.read()

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEXCRYPT")
        self.root.geometry("1200x800")
        self.root.configure(bg="#000000")
        self.root.resizable(True, True)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.setup_style()
        
        self.progress_value = 0
        self.anim_id = None
        self.custom_key = None
        
        self.create_widgets()
        self.create_menu()
        self.root.after(100, self.start_animation)

    def setup_style(self):
        bg = "#000000"
        fg = "#00ffff"
        accent = "#00ffff"
        secondary = "#001f1f"
        
        self.style.configure(".", background=bg, foreground=fg, font=("Arial", 10))
        self.style.configure("TButton", padding=10, font=("Arial", 11))
        self.style.map("TButton",
                       background=[('active', accent), ('pressed', '#00cccc')],
                       foreground=[('active', 'black')])
        self.style.configure("Header.TLabel", font=("Arial", 28), foreground=accent)
        self.style.configure("Sub.TLabel", font=("Arial", 11), foreground="#00cccc")
        self.style.configure("Card.TFrame", background=secondary, relief="flat")
        
        self.style.layout("Progress.TProgressbar", [
            ('Horizontal.Progressbar.trough',
             {'children': [('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'nswe'})],
              'sticky': 'nswe'})
        ])
        self.style.configure("Progress.TProgressbar", thickness=6, background=accent, troughcolor="#003333")

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#000000")
        header.pack(fill=tk.X, pady=20)
        tk.Label(header, text="LEXCRYPT", font=("Arial", 32), fg="#00ffff", bg="#000000").pack()

        main = tk.Frame(self.root, bg="#000000")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        left = tk.Frame(main, bg="#000000")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        actions = [
            ("Set Master Password", self.set_master_password, "Create vault"),
            ("Load Key", self.load_key, "Import key"),
            ("Encrypt Message", self.encrypt_message, "Encrypt text"),
            ("Decrypt Message", self.decrypt_message, "Decrypt text"),
            ("Encrypt Files", self.encrypt_files, "Encrypt files"),
            ("Decrypt Files", self.decrypt_files, "Decrypt files")
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
        self.status_label = tk.Label(info_card, text="Ready", fg="#00ffff", bg="#001f1f")
        self.status_label.pack()

        self.progress = ttk.Progressbar(right, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)
        self.progress.pack_forget()

        log_frame = tk.Frame(right, bg="#001f1f", bd=1, relief="solid")
        log_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(log_frame, text="Log", fg="#00ffff", bg="#001f1f").pack()
        
        self.log = tk.Text(log_frame, state=tk.DISABLED, bg="#000000", fg="#00ffff", font=("Arial", 10))
        self.log.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.config(yscrollcommand=scrollbar.set)

    def create_menu(self):
        menubar = Menu(self.root)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Decrypt Files", command=self.decrypt_files)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def start_animation(self):
        self.animate_glow(0)

    def animate_glow(self, phase):
        self.root.after(50, self.animate_glow, phase + 0.1)

    def log_message(self, msg, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f"[{timestamp} | {level}] {msg}\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def update_status(self, msg):
        self.status_label.config(text=msg)

    def set_master_password(self):
        pwd1 = simpledialog.askstring("Setup", "Password:", show='*')
        if not pwd1 or len(pwd1) < 8:
            messagebox.showerror("Error", "Invalid")
            return
        pwd2 = simpledialog.askstring("Confirm", "Confirm:", show='*')
        if pwd1 != pwd2:
            messagebox.showerror("Error", "Mismatch")
            return
        salt = os.urandom(SALT_SIZE)
        save_salt(salt)
        self.custom_key = None
        self.log_message("Vault set", "SUCCESS")
        self.update_status("Ready")

    def get_key(self):
        if self.custom_key:
            return self.custom_key
        if not os.path.exists("salt.bin"):
            messagebox.showwarning("No Vault", "Set password")
            return None
        password = simpledialog.askstring("Unlock", "Password:", show='*')
        if not password:
            return None
        salt = load_salt()
        key, _ = derive_key(password, salt)
        return key

    def load_key(self):
        file = filedialog.askopenfilename(title="Load Key")
        if file:
            try:
                with open(file, "rb") as f:
                    key = f.read()
                Fernet(key)
                self.custom_key = key
                self.log_message("Key loaded", "SUCCESS")
                self.update_status("Key active")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def encrypt_message(self):
        key = self.get_key()
        if not key: return
        msg = simpledialog.askstring("Input", "Message:")
        if not msg: return
        f = Fernet(key)
        token = f.encrypt(msg.encode())
        path = filedialog.asksaveasfilename(title="Save Token")
        if path:
            with open(path, "wb") as f:
                f.write(token)
            self.log_message("Encrypted", "SUCCESS")

    def decrypt_message(self):
        key = self.get_key()
        if not key: return
        path = filedialog.askopenfilename(title="Select Token")
        if not path: return
        with open(path, "rb") as f:
            token = f.read()
        f = Fernet(key)
        try:
            msg = f.decrypt(token).decode()
            save_path = filedialog.asksaveasfilename(title="Save Message")
            if save_path:
                with open(save_path, "w") as f:
                    f.write(msg)
                self.log_message("Decrypted", "SUCCESS")
        except InvalidToken:
            messagebox.showerror("Error", "Invalid")

    def encrypt_files(self):
        key = self.get_key()
        if not key: return
        files = filedialog.askopenfilenames(title="Select Files")
        if not files: return
        self.start_progress(len(files))
        threading.Thread(target=self._process_files, args=(key, files, True)).start()

    def decrypt_files(self):
        key = self.get_key()
        if not key: return
        files = filedialog.askopenfilenames(title="Select Files")
        if not files: return
        self.start_progress(len(files))
        threading.Thread(target=self._process_files, args=(key, files, False)).start()

    def _process_files(self, key, files, encrypt):
        f = Fernet(key)
        success = 0
        mode = "encrypt" if encrypt else "decrypt"
        
        for i, path in enumerate(files):
            try:
                base = os.path.basename(path)
                ext = ".enc" if encrypt else ""
                init = base + ext if encrypt else base.replace(".enc", "")
                
                save_path = filedialog.asksaveasfilename(title=f"Save {mode}: {base}", initialfile=init)
                if not save_path:
                    continue

                with open(path, "rb") as src, open(save_path, "wb") as dst:
                    while True:
                        chunk = src.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        if encrypt:
                            dst.write(f.encrypt(chunk))
                        else:
                            dst.write(f.decrypt(chunk))
                success += 1
                self.log_message(f"{mode.capitalize()}ed {base}", "SUCCESS")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.root.after(0, self.update_progress, i + 1)

        self.root.after(0, messagebox.showinfo, "Complete", f"{success} files {mode}ed")
        self.root.after(0, self.stop_progress)

    def start_progress(self, total):
        self.progress['maximum'] = total
        self.progress['value'] = 0
        self.progress.pack(fill=tk.X, pady=10)
        self.update_status("Processing...")

    def update_progress(self, value):
        self.progress['value'] = value

    def stop_progress(self):
        self.progress.pack_forget()
        self.update_status("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()