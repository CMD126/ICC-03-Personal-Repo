# Log Analyzer

**Module 4 — Security Operations**

A Python-based SSH auth.log parser that detects brute force attempts, successful logins, and invalid username enumeration. Simulates a core SOC analyst task — reviewing logs for suspicious activity and generating an actionable report.

---

## Features

| Feature | Description |
|---------|-------------|
| Brute force detection | Flags IPs exceeding a configurable failed-login threshold (default: 5) |
| Successful login tracking | Lists all accepted SSH sessions with timestamp and source IP |
| Username enumeration detection | Identifies invalid usernames attackers probed |
| Summary report | Outputs a structured, human-readable security report |
| Sample log included | `sample_auth.log` contains a realistic simulated scenario |

---

## Usage

```bash
python3 log_analyzer.py
```

No external dependencies — uses only Python's built-in `re` and `collections` modules.

---

## Sample Output

```
  [!] BRUTE FORCE ALERTS  (threshold: >= 5 failures)

    IP Address           Attempts   Targeted Accounts
    ──────────────────────────────────────────────────
    192.168.1.105        11         admin, root
    185.220.101.5        6          admin, ftp, pi, postgres, support, user
    172.16.0.88          6          root
```

---

## Concepts Demonstrated

| Concept | Explanation |
|---------|-------------|
| **Log parsing** | Using regex to extract structured data from unstructured log lines |
| **Brute force detection** | Counting failed attempts per IP and triggering alerts above a threshold |
| **Username enumeration** | Attackers probe common usernames (root, admin, pi, guest) before attacking |
| **Triage & reporting** | Presenting findings in a prioritized, readable format — a core SOC skill |

---

## Log Format Supported

Standard Linux SSH `auth.log` / syslog format:

```
Jan 15 08:23:01 server sshd[1234]: Failed password for root from 192.168.1.105 port 51200 ssh2
Jan 15 08:23:15 server sshd[1209]: Accepted password for admin from 10.0.0.5 port 55000 ssh2
Jan 15 08:25:00 server sshd[1210]: Invalid user ftpuser from 203.0.113.42 port 60000 ssh2
```

---

## Requirements

- Python 3.6+
- No external packages needed
