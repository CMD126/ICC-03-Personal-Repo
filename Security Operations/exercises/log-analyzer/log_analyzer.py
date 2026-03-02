#!/usr/bin/env python3
"""
Log Analyzer - Brute Force & Anomaly Detector
ICC-03 Cybersecurity Program | Module 4: Security Operations

Demonstrates:
- Parsing Linux SSH auth.log format
- Detecting brute force login attempts by IP
- Identifying successful logins
- Flagging invalid username enumeration
- Generating a structured security report
"""

import re
from collections import defaultdict

BANNER = """
╔═══════════════════════════════════════╗
║         LOG ANALYZER v1.0             ║
║   Brute Force & Anomaly Detection     ║
╚═══════════════════════════════════════╝
"""

# Number of failed attempts from a single IP to trigger a brute force alert
BRUTE_FORCE_THRESHOLD = 5

# Regex patterns matching standard Linux auth.log / syslog SSH entries
FAILED_RE  = re.compile(r"(\w+\s+\d+\s+[\d:]+).*Failed password for (?:invalid user )?(\S+) from ([\d.]+)")
ACCEPTED_RE = re.compile(r"(\w+\s+\d+\s+[\d:]+).*Accepted password for (\S+) from ([\d.]+)")
INVALID_RE  = re.compile(r"(\w+\s+\d+\s+[\d:]+).*Invalid user (\S+) from ([\d.]+)")


def parse_log(filepath: str):
    """
    Parse an auth.log file and extract:
    - failed login attempts  (by source IP)
    - successful logins
    - invalid username attempts
    """
    failed        = defaultdict(list)   # ip -> [(timestamp, username), ...]
    accepted      = []                   # [(timestamp, username, ip), ...]
    invalid_users = defaultdict(int)     # username -> count

    try:
        with open(filepath, "r") as f:
            for line in f:
                m = FAILED_RE.search(line)
                if m:
                    ts, user, ip = m.group(1), m.group(2), m.group(3)
                    failed[ip].append((ts, user))
                    continue

                m = ACCEPTED_RE.search(line)
                if m:
                    ts, user, ip = m.group(1), m.group(2), m.group(3)
                    accepted.append((ts, user, ip))
                    continue

                m = INVALID_RE.search(line)
                if m:
                    user = m.group(2)
                    invalid_users[user] += 1

    except FileNotFoundError:
        print(f"\n  [!] File not found: {filepath}")
        return None, None, None

    return failed, accepted, invalid_users


def detect_brute_force(failed: dict) -> dict:
    """Return only IPs that exceeded the brute force threshold."""
    return {ip: entries for ip, entries in failed.items()
            if len(entries) >= BRUTE_FORCE_THRESHOLD}


def print_report(filepath: str, failed: dict, accepted: list, invalid_users: dict):
    brute_force   = detect_brute_force(failed)
    total_failed  = sum(len(v) for v in failed.values())

    print(f"\n  {'=' * 58}")
    print(f"  SECURITY LOG ANALYSIS REPORT")
    print(f"  File   : {filepath}")
    print(f"  {'=' * 58}")

    # Summary
    print(f"\n  [SUMMARY]")
    print(f"    Total failed login attempts  : {total_failed}")
    print(f"    Unique source IPs (failed)   : {len(failed)}")
    print(f"    Successful logins            : {len(accepted)}")
    print(f"    Unique invalid usernames     : {len(invalid_users)}")
    print(f"    Brute force alerts           : {len(brute_force)}")

    # Brute force alerts
    print(f"\n  {'─' * 58}")
    if brute_force:
        print(f"  [!] BRUTE FORCE ALERTS  (threshold: >= {BRUTE_FORCE_THRESHOLD} failures)")
        print(f"\n    {'IP Address':<20} {'Attempts':<10} Targeted Accounts")
        print(f"    {'─' * 50}")
        for ip, entries in sorted(brute_force.items(), key=lambda x: -len(x[1])):
            users = ", ".join(sorted(set(u for _, u in entries)))
            print(f"    {ip:<20} {len(entries):<10} {users}")
    else:
        print(f"  [+] No brute force activity detected.")

    # Successful logins
    print(f"\n  {'─' * 58}")
    if accepted:
        print(f"  [+] SUCCESSFUL LOGINS ({len(accepted)})")
        print(f"\n    {'Timestamp':<24} {'User':<15} Source IP")
        print(f"    {'─' * 50}")
        for ts, user, ip in accepted:
            print(f"    {ts:<24} {user:<15} {ip}")
    else:
        print(f"  [-] No successful logins found.")

    # Invalid usernames (enumeration)
    print(f"\n  {'─' * 58}")
    if invalid_users:
        print(f"  [?] INVALID USERNAME ENUMERATION — top targets")
        print(f"\n    {'Username':<20} Attempts")
        print(f"    {'─' * 30}")
        for user, count in sorted(invalid_users.items(), key=lambda x: -x[1])[:10]:
            print(f"    {user:<20} {count}")
    else:
        print(f"  [+] No invalid username attempts detected.")

    print(f"\n  {'=' * 58}\n")


def main():
    print(BANNER)
    print("  1) Analyze sample_auth.log (included)")
    print("  2) Specify a custom log file path")
    print("  3) Exit")

    choice = input("\n  Select option: ").strip()

    if choice == "1":
        filepath = "sample_auth.log"
    elif choice == "2":
        filepath = input("  Enter log file path: ").strip()
    elif choice == "3":
        return
    else:
        print("  [!] Invalid option.")
        return

    print(f"\n  [*] Parsing: {filepath} ...")
    failed, accepted, invalid_users = parse_log(filepath)

    if failed is None:
        return

    print_report(filepath, failed, accepted, invalid_users)


if __name__ == "__main__":
    main()
