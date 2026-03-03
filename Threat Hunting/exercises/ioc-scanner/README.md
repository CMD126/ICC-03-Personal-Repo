# IOC Scanner

Hands-on exercise for understanding Indicators of Compromise (IOCs), threat intelligence feeds, and the threat hunting process by scanning logs and files for known-bad IPs, domains, and file hashes.

---

## What You Will Learn

- What IOCs are and the different types (IP, domain, hash, URL)
- The Pyramid of Pain — why TTPs are more valuable than hash IOCs
- How threat intelligence feeds work
- How to scan log files for signs of compromise
- The threat hunting methodology: Hypothesis → Collect → Investigate → Discover → Report

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | Scan Log File | Parses a log file line by line, extracts IPs/domains/hashes, flags IOC matches with source line |
| 2 | Scan Directory | Recursively scans `.log`, `.txt`, `.csv`, `.json` files in a folder |
| 3 | Scan Manual Text | Paste any text and scan it for IOC matches |
| 4 | Hash File Check | Hashes a file (MD5/SHA-1/SHA-256) and checks it against the IOC list |
| 5 | Learn IOCs | Guide to IOC types, Pyramid of Pain, threat hunting process, and IOC sources |

---

## Usage

```bash
python3 ioc_scanner.py
```

The tool loads `sample_iocs.txt` automatically on startup. You can also provide your own IOC file in the same format.

---

## IOC File Format (`sample_iocs.txt`)

```
# type:value:severity:description
ip:185.220.101.45:HIGH:Tor exit node — C2 traffic observed
domain:evil-malware.ru:CRITICAL:Active malware distribution
hash:44d88612fea8a8f36de82e1278abb02f:HIGH:Emotet dropper
```

---

## Requirements

Pure Python 3 stdlib — no external packages needed.

| Module | Used for |
|--------|----------|
| `re` | Regex extraction of IPs, domains, hashes |
| `hashlib` | MD5/SHA-1/SHA-256 file hashing |
| `os` | File and directory traversal |
