# File Permissions Auditor

Hands-on exercise for understanding Linux file permissions, ownership, and privilege escalation risks through SUID/SGID and world-writable files.

---

## What You Will Learn

- How Linux permission notation works (`rwxrwxrwx`, octal)
- The difference between owner, group, and other permissions
- What SUID and SGID bits do and why they are security risks
- How to identify world-writable files and why they matter
- How attackers use misconfigured permissions for privilege escalation

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | Audit Directory | Lists every file with its permissions, type, and owner |
| 2 | World-Writable Files | Finds files any user can modify — common misconfiguration |
| 3 | SUID / SGID Files | Finds binaries that run with elevated privileges |
| 4 | Learn Permission Notation | Interactive guide to octal/symbolic notation decoder |

---

## Usage

```bash
python3 file_permissions_auditor.py
```

No root required (some SUID/SGID scans may show more results with root).

---

## Requirements

Pure Python 3 stdlib — no external packages needed.

| Module | Used for |
|--------|----------|
| `os` | Directory traversal |
| `stat` | Permission bit masks |
| `pwd` / `grp` | Username and group name resolution (Linux/macOS) |
