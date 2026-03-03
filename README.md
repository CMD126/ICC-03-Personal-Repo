# ICC-03 Cybersecurity Learning Repository

## Table of Contents

- [About](#about)
- [Repository Structure](#repository-structure)
- [Scripts](#scripts)
- [Modules](#modules)
- [Getting Started](#getting-started)
- [License](#license)

---

## About

Welcome to the ICC-03 Cybersecurity Learning Repository! This collection of personal notes, exercises, and custom-built scripts was developed during the ICC-03 cybersecurity program. It is designed to be a practical and evolving resource for anyone interested in cybersecurity, from beginners to experienced practitioners.

Here you will find tools and resources to support learning across network security, system administration, threat operations, cloud security, and more.

---

## Repository Structure

```
ICC-03-Personal-Repo/
├── Scripts/                              # Custom-built cybersecurity tools
├── Foundations/
│   ├── notes/                            # Linux, Ubuntu cheat sheets
│   └── exercises/
├── Networking and Systems Administration/
│   ├── notes/                            # OSI Model, Wireshark cheat sheets
│   └── exercises/
├── Governance, Risk, and Compliance (GRC)/
│   ├── notes/
│   └── exercises/
├── Data Security/
│   ├── notes/
│   └── exercises/                        # file-encryptor, password-auditor, ransomware-simulator
├── Security Operations/
│   ├── notes/
│   └── exercises/                        # log-analyzer
├── Cloud Security/
│   ├── notes/
│   └── exercises/
├── Threat Hunting/
│   ├── notes/
│   └── exercises/
├── Application Security and Vulnerability Analysis/
│   ├── notes/
│   └── exercises/                        # web-headers-checker
└── Penetration Testing/
    ├── notes/                            # Nmap cheat sheet
    └── exercises/                        # port-scanner
```

---

## Scripts

Production-quality tools, each in its own directory under `/Scripts` with a `README.md`.

| Tool | Description |
|------|-------------|
| [syscript](./Scripts/syscript/) | **v2.0** — Menu-driven Bash toolkit for Ubuntu/Debian administration. Covers package management, system info, networking, service control, firewall status, and a live system health dashboard. |
| [nmatrix](./Scripts/nmatrix/) | **v2.0** — Matrix-style, menu-driven Nmap frontend with 8 scan types (Quick/Full TCP, Service+Script, OS Detection, UDP, Ping Sweep, Vulnerability, Custom), scan logging, and save-to-file support. |
| [network-tool](./Scripts/network-tool/) | **v4.0** — Comprehensive Bash network diagnostic utility with 16 options across 4 categories: Diagnostics, Scanning & Discovery (host discovery, listening services), Security & Analysis (HTTP response checker, firewall status, SSL/TLS, DNS), and Information & Monitoring. |
| [abdns](./Scripts/abdns/) | Python tool that benchmarks 9 public DNS providers using real UDP queries, reports packet loss, and applies the fastest primary + secondary DNS on Linux, macOS, or Windows. |
| [hash-toolkit](./Scripts/hash-toolkit/) | **v1.0** — Menu-driven Python utility to identify hash types (MD5 → bcrypt → Argon2), generate hashes with optional salt, verify file integrity, and compare digests using constant-time comparison. |
| [recon-tool](./Scripts/recon-tool/) | **v1.0** — Automated OSINT and reconnaissance tool. Covers WHOIS, DNS enumeration, subdomain brute-forcing, port scanning, HTTP security headers, SSL/TLS analysis, and IP geolocation — all from one menu. |

---

## Modules

Each module contains a `notes/` folder with cheat sheets and an `exercises/` folder with hands-on Python or Bash projects.

**Note:** Educational simulations (e.g., ransomware) are in Data Security — run only in a controlled VM environment.

### Foundations

| Type | Content |
|------|---------|
| [Notes](./Foundations/notes/) | [Linux](./Foundations/notes/Linux/README.md), [Ubuntu](./Foundations/notes/Ubuntu/README.md) |
| [file-permissions-auditor](./Foundations/exercises/file-permissions-auditor/) | Audits Linux file permissions — finds world-writable files, SUID/SGID binaries, and decodes permission notation interactively. |

### Networking and Systems Administration

| Type | Content |
|------|---------|
| [Notes](./Networking%20and%20Systems%20Administration/notes/) | [OSI Model](./Networking%20and%20Systems%20Administration/notes/OSI%20Model/README.md), [Wireshark](./Networking%20and%20Systems%20Administration/notes/Wireshark/README.md) |
| [subnet-calculator](./Networking%20and%20Systems%20Administration/exercises/subnet-calculator/) | Calculates subnet information (network/broadcast/host range), identifies IP classes, expands CIDR ranges, and divides networks into equal subnets. |

### Governance, Risk, and Compliance (GRC)

| Type | Content |
|------|---------|
| [Notes](./Governance%2C%20Risk%2C%20and%20Compliance%20(GRC)/notes/) | [GRC Cheat Sheet](./Governance%2C%20Risk%2C%20and%20Compliance%20(GRC)/notes/README.md) |
| [risk-assessment-tool](./Governance%2C%20Risk%2C%20and%20Compliance%20(GRC)/exercises/risk-assessment-tool/) | Builds a risk register using Likelihood × Impact scoring, assigns severity levels (Low→Critical), recommends response strategies, and saves entries to JSON. |

### Data Security

| Type | Content |
|------|---------|
| [Notes](./Data%20Security/notes/) | [Data Security Cheat Sheet](./Data%20Security/notes/README.md) |
| [file-encryptor](./Data%20Security/exercises/file-encryptor/) | Python GUI app (Tkinter) for file and message encryption/decryption. Uses PBKDF2-SHA256 key derivation, Fernet (AES-128-CBC), and chunked I/O for large files. |
| [password-auditor](./Data%20Security/exercises/password-auditor/) | Demonstrates hashing algorithms (MD5 → SHA-512), salting, dictionary attack simulation, and why bcrypt/PBKDF2 are required for secure password storage. |
| [ransomware-simulator](./Data%20Security/exercises/ransomware-simulator/) | **Educational only** — Python ransomware simulation with encryption/decryption, wallpaper generation, and fullscreen popup. Run in a VM only. |

### Security Operations

| Type | Content |
|------|---------|
| [Notes](./Security%20Operations/notes/) | [SecOps Cheat Sheet](./Security%20Operations/notes/README.md) |
| [log-analyzer](./Security%20Operations/exercises/log-analyzer/) | Parses SSH `auth.log` files to detect brute force attempts, successful logins, and invalid username enumeration. Generates a SOC-style security report. |

### Cloud Security

| Type | Content |
|------|---------|
| [Notes](./Cloud%20Security/notes/) | [Cloud Security Cheat Sheet](./Cloud%20Security/notes/README.md) |
| [iam-policy-analyzer](./Cloud%20Security/exercises/iam-policy-analyzer/) | Parses AWS-style IAM policy JSON files, flags dangerous permissions (wildcards, admin access, public principals), and explains the least privilege principle. |

### Threat Hunting

| Type | Content |
|------|---------|
| [Notes](./Threat%20Hunting/notes/) | [Threat Hunting Cheat Sheet](./Threat%20Hunting/notes/README.md) |
| [ioc-scanner](./Threat%20Hunting/exercises/ioc-scanner/) | Scans log files and directories for Indicators of Compromise (IPs, domains, file hashes) against a threat intelligence feed. Covers the Pyramid of Pain and hunt reporting. |

### Application Security and Vulnerability Analysis

| Type | Content |
|------|---------|
| [Notes](./Application%20Security%20and%20Vulnerability%20Analysis/notes/) | [AppSec Cheat Sheet](./Application%20Security%20and%20Vulnerability%20Analysis/notes/README.md) |
| [web-headers-checker](./Application%20Security%20and%20Vulnerability%20Analysis/exercises/web-headers-checker/) | Fetches HTTP response headers from any URL and audits for missing security headers, information disclosure, and scores the target's security posture (A–F). |

### Penetration Testing

| Type | Content |
|------|---------|
| [Notes](./Penetration%20Testing/notes/) | [Nmap](./Penetration%20Testing/notes/Nmap/README.md) |
| [port-scanner](./Penetration%20Testing/exercises/port-scanner/) | TCP connect scanner built with raw Python sockets and multithreading. Scans common ports or custom ranges, maps services, and optionally grabs banners. |

---

## Getting Started

Clone the repository locally:

```bash
git clone https://github.com/CMD126/ICC-03-Personal-Repo.git
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE.md) file for details.
