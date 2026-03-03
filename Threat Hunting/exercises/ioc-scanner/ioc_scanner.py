#!/usr/bin/env python3
"""
IOC Scanner — Educational Exercise
Demonstrates threat hunting concepts: Indicators of Compromise (IOCs),
threat intelligence feeds, log scanning, and hunt reporting.
"""

import hashlib
import os
import re
import sys
from collections import defaultdict

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║              IOC SCANNER — Educational                      ║
║   Indicators of Compromise · Threat Intel · Hunt Reports   ║
╚══════════════════════════════════════════════════════════════╝
"""

DEFAULT_IOC_FILE = os.path.join(os.path.dirname(__file__), "sample_iocs.txt")

# Regex patterns for auto-detection
RE_IPV4   = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
RE_DOMAIN = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|ru|tk|xyz|io|co|info|biz|cc|pw|top)\b')
RE_MD5    = re.compile(r'\b[a-fA-F0-9]{32}\b')
RE_SHA1   = re.compile(r'\b[a-fA-F0-9]{40}\b')
RE_SHA256 = re.compile(r'\b[a-fA-F0-9]{64}\b')

def load_iocs(path=None):
    """Load IOCs from a file. Returns dict of type→{value: (severity, desc)}."""
    iocs = {"ip": {}, "domain": {}, "hash": {}}
    fpath = path or DEFAULT_IOC_FILE
    if not os.path.exists(fpath):
        print(f"[!] IOC file not found: {fpath}")
        return iocs
    with open(fpath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(":", 3)
            if len(parts) == 4:
                itype, value, severity, desc = parts
                itype = itype.lower().strip()
                if itype in iocs:
                    iocs[itype][value.strip().lower()] = (severity.strip(), desc.strip())
    total = sum(len(v) for v in iocs.values())
    print(f"[+] Loaded {total} IOCs ({len(iocs['ip'])} IPs, {len(iocs['domain'])} domains, {len(iocs['hash'])} hashes)")
    return iocs

def scan_text(text, iocs, source="input"):
    """Scan text for IOC matches. Returns list of hit dicts."""
    hits = []
    text_lower = text.lower()

    for ip in RE_IPV4.findall(text):
        if ip.lower() in iocs["ip"]:
            sev, desc = iocs["ip"][ip.lower()]
            hits.append({"type": "IP", "value": ip, "severity": sev, "desc": desc, "source": source})

    for domain in RE_DOMAIN.findall(text):
        if domain.lower() in iocs["domain"]:
            sev, desc = iocs["domain"][domain.lower()]
            hits.append({"type": "Domain", "value": domain, "severity": sev, "desc": desc, "source": source})

    for h in RE_MD5.findall(text) + RE_SHA1.findall(text) + RE_SHA256.findall(text):
        if h.lower() in iocs["hash"]:
            sev, desc = iocs["hash"][h.lower()]
            hits.append({"type": "Hash", "value": h, "severity": sev, "desc": desc, "source": source})

    return hits

def scan_log_file(iocs):
    """Scan a log file for IOC matches line by line."""
    path = input("\n[?] Path to log file: ").strip().strip('"')
    if not os.path.isfile(path):
        print(f"[!] File not found: {path}")
        return

    print(f"\n[*] Scanning: {path}\n")
    all_hits = []
    lines_scanned = 0

    with open(path, errors="ignore") as f:
        for lineno, line in enumerate(f, 1):
            hits = scan_text(line, iocs, source=f"line {lineno}")
            for hit in hits:
                hit["line"] = line.strip()
                hit["lineno"] = lineno
            all_hits.extend(hits)
            lines_scanned += 1

    print_hits(all_hits, lines_scanned)

def scan_directory(iocs):
    """Scan all text files in a directory for IOC matches."""
    path = input("\n[?] Directory to scan: ").strip().strip('"')
    if not os.path.isdir(path):
        print(f"[!] Not a valid directory: {path}")
        return

    print(f"\n[*] Scanning directory: {path}\n")
    all_hits = []
    files_scanned = 0

    for root, _, files in os.walk(path):
        for fname in files:
            if not fname.endswith((".log", ".txt", ".csv", ".json")):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, errors="ignore") as f:
                    for lineno, line in enumerate(f, 1):
                        hits = scan_text(line, iocs, source=fpath)
                        for hit in hits:
                            hit["line"] = line.strip()
                            hit["lineno"] = lineno
                        all_hits.extend(hits)
                files_scanned += 1
            except (PermissionError, OSError):
                continue

    print(f"[+] Scanned {files_scanned} file(s)")
    print_hits(all_hits, files_scanned)

def scan_manual(iocs):
    """Scan manually entered text for IOCs."""
    print("\n[*] Paste text to scan (empty line to finish):\n")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    text = "\n".join(lines)
    hits = scan_text(text, iocs, source="manual input")
    print()
    print_hits(hits, len(lines))

def hash_file_check(iocs):
    """Hash a file and check against known IOC hashes."""
    path = input("\n[?] File to hash and check: ").strip().strip('"')
    if not os.path.isfile(path):
        print(f"[!] File not found: {path}")
        return

    print(f"\n[*] Hashing: {path}")
    for algo_name, algo in [("MD5", hashlib.md5), ("SHA-1", hashlib.sha1), ("SHA-256", hashlib.sha256)]:
        h = algo()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        digest = h.hexdigest()
        match = iocs["hash"].get(digest.lower())
        status = f"[!!] MATCH: {match[1]}" if match else "[OK] Not in IOC list"
        print(f"  {algo_name:<8}: {digest}  {status}")

def print_hits(hits, lines_scanned):
    """Print IOC scan results."""
    if not hits:
        print("[+] No IOC matches found.")
        return

    by_severity = defaultdict(list)
    for h in hits:
        by_severity[h["severity"]].append(h)

    print(f"  [!] {len(hits)} IOC match(es) found!\n")
    print(f"  {'Severity':<10} {'Type':<8} {'Value':<35} {'Description'}")
    print(f"  {'─'*9} {'─'*7} {'─'*34} {'─'*30}")

    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        for h in by_severity.get(sev, []):
            marker = "[!!]" if sev == "CRITICAL" else "[! ]" if sev == "HIGH" else "[ *]"
            val = h["value"][:33] + "…" if len(h["value"]) > 33 else h["value"]
            print(f"  {sev:<10} {h['type']:<8} {val:<35} {h['desc'][:30]}")
            if "line" in h:
                snippet = h["line"][:70] + "…" if len(h["line"]) > 70 else h["line"]
                print(f"  {'':10} {'':8} Source: {h['source']} → {snippet}")

    print(f"\n  Summary: CRITICAL={len(by_severity['CRITICAL'])} HIGH={len(by_severity['HIGH'])} MEDIUM={len(by_severity['MEDIUM'])} LOW={len(by_severity['LOW'])}")

def explain_iocs():
    """Explain IOC types and threat hunting methodology."""
    print("""
  ┌─────────────────────────────────────────────────────┐
  │  IOC Types & Threat Hunting Guide                   │
  └─────────────────────────────────────────────────────┘

  IOC = Indicator of Compromise
  Evidence that a system has been attacked or compromised.

  IOC Types:
    IP Address   — Known malicious C2 servers, scanners, botnets
    Domain       — Malware distribution, C2, phishing sites
    File Hash    — Known malware files (MD5, SHA-1, SHA-256)
    Email        — Phishing sender addresses
    URL          — Malicious links in emails or logs
    Registry Key — Windows persistence mechanisms

  Pyramid of Pain (David Bianco):
    Hardest to change ↑
      TTPs (tactics, techniques, procedures)    ← most valuable
      Tools (malware, exploit frameworks)
      Network artifacts (User-agents, URIs)
      Host artifacts (registry keys, filenames)
      Domain names
      IP addresses
      Hash values                               ← easiest to change
    Easiest to change ↓

  Threat Hunting Process:
    1. Hypothesis  — "Attacker may be using C2 over DNS"
    2. Collect     — Pull DNS logs, proxy logs, netflow
    3. Investigate — Scan for known bad domains/IPs
    4. Discover    — Confirm or rule out hypothesis
    5. Report      — Document findings, escalate if confirmed

  IOC Sources:
    - MISP (Malware Information Sharing Platform)
    - VirusTotal, AlienVault OTX
    - CISA advisories, FBI flash alerts
    - Vendor threat intelligence feeds
    - Internal incident data
""")

def main():
    print(BANNER)
    iocs = load_iocs()
    print()
    while True:
        print("  Options:")
        print("  1. Scan a log file for IOCs")
        print("  2. Scan a directory for IOCs")
        print("  3. Scan manually entered text")
        print("  4. Hash a file and check against IOC list")
        print("  5. Learn about IOCs and threat hunting")
        print("  0. Exit\n")
        choice = input("[?] Select option: ").strip()
        print()
        if   choice == "1": scan_log_file(iocs)
        elif choice == "2": scan_directory(iocs)
        elif choice == "3": scan_manual(iocs)
        elif choice == "4": hash_file_check(iocs)
        elif choice == "5": explain_iocs()
        elif choice == "0": print("[+] Goodbye.\n"); sys.exit(0)
        else: print("[!] Invalid option.")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted.\n")
        sys.exit(0)
