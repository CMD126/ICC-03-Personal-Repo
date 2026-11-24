#!/usr/bin/env python3
"""
File Permissions Auditor — Educational Exercise
Demonstrates Linux file permission concepts: ownership, SUID/SGID,
world-writable files, and identifying privilege escalation risks.
"""

import os
import stat
import sys

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║           FILE PERMISSIONS AUDITOR — Educational            ║
║     Understand Linux permissions, SUID/SGID & risks         ║
╚══════════════════════════════════════════════════════════════╝
"""

def format_permissions(mode):
    """
    Convert a numeric mode to an ls-style rwxrwxrwx string, including the
    special bits: s/S for SUID and SGID, t/T for the sticky bit (uppercase
    when the matching execute bit is not set).
    """
    triplets = [
        (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR, stat.S_ISUID, "s"),
        (stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP, stat.S_ISGID, "s"),
        (stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH, stat.S_ISVTX, "t"),
    ]
    perms = ""
    for read, write, execute, special, letter in triplets:
        perms += "r" if mode & read else "-"
        perms += "w" if mode & write else "-"
        if mode & special:
            perms += letter if mode & execute else letter.upper()
        else:
            perms += "x" if mode & execute else "-"
    return perms

def get_owner(st):
    """Return owner:group string from stat result."""
    try:
        import grp
        import pwd
        owner = pwd.getpwuid(st.st_uid).pw_name
        group = grp.getgrgid(st.st_gid).gr_name
    except (ImportError, KeyError):
        owner = str(st.st_uid)
        group = str(st.st_gid)
    return f"{owner}:{group}"

def scan_directory(path):
    """Recursively yield (filepath, stat_result) for all files."""
    for root, dirs, files in os.walk(path):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            fpath = os.path.join(root, name)
            try:
                st = os.lstat(fpath)
                yield fpath, st
            except (PermissionError, FileNotFoundError):
                continue

def world_writable_files(path):
    """
    Return [(filepath, stat_result)] for regular files any user can modify.

    Symlinks are skipped: on Linux they always show as rwxrwxrwx, but that
    mode is never used for access checks, so listing them is a false positive.
    """
    return [(fpath, st) for fpath, st in scan_directory(path)
            if stat.S_ISREG(st.st_mode) and st.st_mode & stat.S_IWOTH]


def suid_sgid_files(path):
    """Return two lists of (filepath, stat_result): SUID files and SGID files."""
    suid, sgid = [], []
    for fpath, st in scan_directory(path):
        if not stat.S_ISREG(st.st_mode):
            continue
        if st.st_mode & stat.S_ISUID:
            suid.append((fpath, st))
        if st.st_mode & stat.S_ISGID:
            sgid.append((fpath, st))
    return suid, sgid


def audit_directory():
    """Full permission audit of a directory — show all files with permissions."""
    path = input("\n[?] Enter directory path to audit [default: current dir]: ").strip()
    if not path:
        path = "."
    if not os.path.isdir(path):
        print(f"[!] Not a valid directory: {path}")
        return

    print(f"\n[*] Auditing: {os.path.abspath(path)}\n")
    print(f"  {'Permissions':<12} {'Type':<5} {'Owner':<20} {'File'}")
    print(f"  {'─'*11} {'─'*4} {'─'*19} {'─'*40}")

    count = 0
    for fpath, st in scan_directory(path):
        mode = st.st_mode
        perms = format_permissions(mode)
        ftype = "dir " if stat.S_ISDIR(mode) else "link" if stat.S_ISLNK(mode) else "file"
        owner = get_owner(st)
        rel = os.path.relpath(fpath, path)
        print(f"  {perms:<12} {ftype:<5} {owner:<20} {rel}")
        count += 1

    print(f"\n[+] {count} file(s) scanned.")

def find_world_writable():
    """Find world-writable files — anyone can modify them."""
    path = input("\n[?] Enter directory to scan [default: current dir]: ").strip() or "."
    if not os.path.isdir(path):
        print(f"[!] Not a valid directory: {path}")
        return

    print(f"\n[*] Scanning for world-writable files in: {os.path.abspath(path)}\n")
    print("  [!] World-writable files can be modified by ANY user — potential security risk.\n")

    found = [(fpath, format_permissions(st.st_mode), get_owner(st))
             for fpath, st in world_writable_files(path)]

    if found:
        print(f"  {'Permissions':<12} {'Owner':<20} {'File'}")
        print(f"  {'─'*11} {'─'*19} {'─'*40}")
        for fpath, perms, owner in found:
            print(f"  {perms:<12} {owner:<20} {fpath}")
        print(f"\n[!] {len(found)} world-writable file(s) found — review these carefully.")
    else:
        print("[+] No world-writable files found.")

def find_suid_sgid():
    """Find SUID/SGID files — run with elevated privileges."""
    path = input("\n[?] Enter directory to scan [default: /usr]: ").strip() or "/usr"
    if not os.path.isdir(path):
        print(f"[!] Not a valid directory: {path}")
        return

    print(f"\n[*] Scanning for SUID/SGID files in: {path}\n")
    print("  [!] SUID files run with the file owner's privileges (often root).")
    print("  [!] These are common privilege escalation targets.\n")

    suid, sgid = suid_sgid_files(path)
    suid_files = [(fpath, format_permissions(st.st_mode), get_owner(st)) for fpath, st in suid]
    sgid_files = [(fpath, format_permissions(st.st_mode), get_owner(st)) for fpath, st in sgid]

    if suid_files:
        print("  SUID Files (run as file owner):")
        print(f"  {'Permissions':<12} {'Owner':<20} {'File'}")
        print(f"  {'─'*11} {'─'*19} {'─'*40}")
        for fpath, perms, owner in suid_files:
            print(f"  {perms:<12} {owner:<20} {fpath}")

    if sgid_files:
        print("\n  SGID Files (run as file group):")
        print(f"  {'Permissions':<12} {'Owner':<20} {'File'}")
        print(f"  {'─'*11} {'─'*19} {'─'*40}")
        for fpath, perms, owner in sgid_files:
            print(f"  {perms:<12} {owner:<20} {fpath}")

    total = len(suid_files) + len(sgid_files)
    if total == 0:
        print("[+] No SUID/SGID files found in this directory.")
    else:
        print(f"\n[!] {len(suid_files)} SUID and {len(sgid_files)} SGID file(s) found.")

def explain_permissions():
    """Teach permission notation interactively."""
    print("""
  ┌─────────────────────────────────────────────────────┐
  │          Linux Permission Notation Guide            │
  └─────────────────────────────────────────────────────┘

  Format:  [type][owner][group][others]
  Example:  -rwxr-xr--

  File Types:
    -   regular file
    d   directory
    l   symbolic link
    s   socket
    p   named pipe

  Permission Characters:
    r   read    (4)
    w   write   (2)
    x   execute (1)
    -   no permission (0)

  Special Bits:
    s   SUID (on owner execute) — file runs as owner
    s   SGID (on group execute) — file runs as group
    t   Sticky bit (on others execute) — only owner can delete

  Octal Examples:
    777  →  rwxrwxrwx  (full access for all)   ← DANGEROUS
    755  →  rwxr-xr-x  (owner full, others read/exec)
    644  →  rw-r--r--  (owner rw, others read only)
    600  →  rw-------  (owner only)             ← private keys
    4755 →  rwsr-xr-x  (SUID set)               ← runs as owner
""")

    demo = input("  [?] Enter an octal permission number to decode (e.g. 755): ").strip()
    try:
        mode = int(demo, 8)
        if not 0 <= mode <= 0o7777:
            raise ValueError
        print(f"\n  {demo:>4} octal  →  {format_permissions(mode)}")
        print(f"         Owner : {'r' if mode&0o400 else '-'}{'w' if mode&0o200 else '-'}{'x' if mode&0o100 else '-'}")
        print(f"         Group : {'r' if mode&0o040 else '-'}{'w' if mode&0o020 else '-'}{'x' if mode&0o010 else '-'}")
        print(f"         Other : {'r' if mode&0o004 else '-'}{'w' if mode&0o002 else '-'}{'x' if mode&0o001 else '-'}")
        if mode & 0o4000:
            print("         [!] SUID bit is SET")
        if mode & 0o2000:
            print("         [!] SGID bit is SET")
        if mode & 0o1000:
            print("         [*] Sticky bit is SET")
    except ValueError:
        print("  [!] Invalid octal number.")

def main():
    print(BANNER)
    while True:
        print("  Options:")
        print("  1. Audit directory (list all files with permissions)")
        print("  2. Find world-writable files")
        print("  3. Find SUID / SGID files")
        print("  4. Learn permission notation")
        print("  0. Exit\n")
        choice = input("[?] Select option: ").strip()
        print()
        if   choice == "1": audit_directory()
        elif choice == "2": find_world_writable()
        elif choice == "3": find_suid_sgid()
        elif choice == "4": explain_permissions()
        elif choice == "0": print("[+] Goodbye.\n"); sys.exit(0)
        else: print("[!] Invalid option.")
        print()

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted.\n")
        sys.exit(0)
