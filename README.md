# ICC-03 Cybersecurity Portfolio

[![CI](https://github.com/CMD126/ICC-03-Personal-Repo/actions/workflows/ci.yml/badge.svg)](https://github.com/CMD126/ICC-03-Personal-Repo/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Bash](https://img.shields.io/badge/shell-bash-green)

I built this repository while going through the ICC-03 cybersecurity program. It started as a place to keep my notes, and over time it turned into a set of working tools I wrote myself to understand how things actually work: how a port scanner talks to a socket, how you spot a brute force attack in `auth.log`, why an IAM policy with `"Resource": "*"` should make you nervous.

Everything here runs. The Python code is linted and tested on every push, and the Bash scripts go through ShellCheck. If you work in security, you should be able to pick any tool, read the README next to it, and use it in a lab within a couple of minutes.

**Contents**

- [What I can do (and where to see it)](#what-i-can-do-and-where-to-see-it)
- [Quick start](#quick-start)
- [Tools](#tools)
- [Modules](#modules)
- [Framework mapping](#framework-mapping)
- [How the repo is kept healthy](#how-the-repo-is-kept-healthy)
- [Responsible use](#responsible-use)

---

## What I can do (and where to see it)

Instead of listing buzzwords, here is each skill next to the code that shows it.

| Area | What I did | Proof |
|------|------------|-------|
| Network reconnaissance | Wrote a multithreaded TCP connect scanner from raw sockets, then a menu-driven Nmap front end and an OSINT recon script (WHOIS, DNS, subdomains, TLS) | [port-scanner](./08-penetration-testing/exercises/port-scanner/), [nmatrix](./tools/nmatrix/), [recon-tool](./tools/recon-tool/) |
| Log analysis and detection | Parsed SSH `auth.log` to flag brute force sources, successful logins and username enumeration, with a SOC style report | [log-analyzer](./04-security-operations/exercises/log-analyzer/) |
| Threat hunting | Built an IOC scanner that matches IPs, domains and file hashes in logs and folders against a threat intel feed | [ioc-scanner](./06-threat-hunting/exercises/ioc-scanner/) |
| Cloud security | Wrote an analyzer for AWS IAM policies that flags public principals, wildcard resources and privilege escalation actions like `iam:PassRole` | [iam-policy-analyzer](./05-cloud-security/exercises/iam-policy-analyzer/) |
| Web application security | Audited HTTP security headers (CSP, HSTS, X-Frame-Options and others), caught version leaks, graded sites A to F | [web-headers-checker](./07-appsec/exercises/web-headers-checker/) |
| Cryptography | Used PBKDF2 key derivation with Fernet for file encryption, identified and compared hashes in constant time, showed why fast hashes are bad for passwords | [file-encryptor](./03-data-security/exercises/file-encryptor/), [hash-toolkit](./tools/hash-toolkit/), [password-auditor](./03-data-security/exercises/password-auditor/) |
| Adversary emulation | Simulated ransomware behaviour (encryption, ransom note, wallpaper change) in an isolated VM to understand what defenders need to detect | [ransomware-simulator](./03-data-security/exercises/ransomware-simulator/) |
| Linux hardening | Audited file permissions, found world-writable files and SUID/SGID binaries | [file-permissions-auditor](./00-foundations/exercises/file-permissions-auditor/) |
| Risk management | Built a risk register using Likelihood × Impact scoring with response strategies, stored as JSON | [risk-assessment-tool](./02-grc/exercises/risk-assessment-tool/) |
| Networking and sysadmin | Subnetting, Bash admin toolkits, network diagnostics and a DNS benchmark that measures real UDP queries | [subnet-calculator](./01-networking-and-sysadmin/exercises/subnet-calculator/), [syscript](./tools/syscript/), [network-tool](./tools/network-tool/), [abdns](./tools/abdns/) |

---

## Quick start

```bash
git clone https://github.com/CMD126/ICC-03-Personal-Repo.git
cd ICC-03-Personal-Repo

# Most Python tools only need the standard library
python3 04-security-operations/exercises/log-analyzer/log_analyzer.py

# Bash tools
bash tools/recon-tool/recon_tool.sh
```

A few tools need extra packages (`cryptography`, `Pillow`). Those folders have their own `requirements.txt`, so install them only when you need them:

```bash
pip install -r 03-data-security/exercises/file-encryptor/requirements.txt
```

---

## Tools

Bigger utilities I keep improving and actually use. Each one has its own README with options and examples.

| Tool | Language | What it does |
|------|----------|--------------|
| [recon-tool](./tools/recon-tool/) | Bash | OSINT and recon in one menu: WHOIS, DNS records, subdomain brute forcing, port scan, HTTP security headers, SSL/TLS and IP geolocation, with a saved report. |
| [nmatrix](./tools/nmatrix/) | Bash | Nmap front end with 8 scan profiles (quick and full TCP, service and scripts, OS detection, UDP, ping sweep, vuln scripts, custom), scan logging and export. |
| [network-tool](./tools/network-tool/) | Bash | Network diagnostics with 16 options: host discovery, listening services, HTTP checks, firewall status, TLS and DNS (including DNSSEC). |
| [hash-toolkit](./tools/hash-toolkit/) | Python | Identifies hash formats from MD5 to bcrypt and Argon2, generates salted hashes, checks file integrity and compares digests in constant time. |
| [abdns](./tools/abdns/) | Python | Benchmarks 9 public DNS resolvers with real UDP queries, reports packet loss and applies the fastest pair on Linux, macOS or Windows. |
| [syscript](./tools/syscript/) | Bash | Admin toolkit for Ubuntu and Debian: packages, services, firewall, networking and a live health dashboard. |

---

## Modules

The modules follow the order of the course. Each one has a `notes/` folder with my cheat sheets and an `exercises/` folder with a hands-on project.

| # | Module | Notes | Exercise |
|---|--------|-------|----------|
| 00 | [Foundations](./00-foundations/) | [Linux](./00-foundations/notes/linux/README.md), [Ubuntu](./00-foundations/notes/ubuntu/README.md) | [file-permissions-auditor](./00-foundations/exercises/file-permissions-auditor/) |
| 01 | [Networking and Sysadmin](./01-networking-and-sysadmin/) | [OSI model](./01-networking-and-sysadmin/notes/osi-model/README.md), [Wireshark](./01-networking-and-sysadmin/notes/wireshark/README.md) | [subnet-calculator](./01-networking-and-sysadmin/exercises/subnet-calculator/) |
| 02 | [Governance, Risk and Compliance](./02-grc/) | [GRC](./02-grc/notes/README.md) | [risk-assessment-tool](./02-grc/exercises/risk-assessment-tool/) |
| 03 | [Data Security](./03-data-security/) | [Data security](./03-data-security/notes/README.md) | [file-encryptor](./03-data-security/exercises/file-encryptor/), [password-auditor](./03-data-security/exercises/password-auditor/), [ransomware-simulator](./03-data-security/exercises/ransomware-simulator/) |
| 04 | [Security Operations](./04-security-operations/) | [SecOps](./04-security-operations/notes/README.md) | [log-analyzer](./04-security-operations/exercises/log-analyzer/) |
| 05 | [Cloud Security](./05-cloud-security/) | [Cloud security](./05-cloud-security/notes/README.md) | [iam-policy-analyzer](./05-cloud-security/exercises/iam-policy-analyzer/) |
| 06 | [Threat Hunting](./06-threat-hunting/) | [Threat hunting](./06-threat-hunting/notes/README.md) | [ioc-scanner](./06-threat-hunting/exercises/ioc-scanner/) |
| 07 | [Application Security](./07-appsec/) | [AppSec](./07-appsec/notes/README.md) | [web-headers-checker](./07-appsec/exercises/web-headers-checker/) |
| 08 | [Penetration Testing](./08-penetration-testing/) | [Nmap](./08-penetration-testing/notes/nmap/README.md) | [port-scanner](./08-penetration-testing/exercises/port-scanner/) |

---

## Framework mapping

If you think in terms of MITRE ATT&CK or the NIST Cybersecurity Framework 2.0, this is where each project fits. Offensive tools map to the technique they perform. Defensive tools map to the technique they help detect and the CSF function they support.

| Project | MITRE ATT&CK | NIST CSF 2.0 |
|---------|--------------|--------------|
| port-scanner, nmatrix | [T1046](https://attack.mitre.org/techniques/T1046/) Network Service Discovery | ID.AM (asset inventory) |
| recon-tool | [T1595](https://attack.mitre.org/techniques/T1595/) Active Scanning, [T1590](https://attack.mitre.org/techniques/T1590/) Gather Victim Network Information | ID.RA (risk assessment) |
| log-analyzer | Detects [T1110](https://attack.mitre.org/techniques/T1110/) Brute Force | DE.CM, DE.AE (monitoring, adverse event analysis) |
| ioc-scanner | Detects indicators tied to known campaigns | DE.CM, DE.AE |
| iam-policy-analyzer | Finds paths to [T1078.004](https://attack.mitre.org/techniques/T1078/004/) Cloud Accounts and [T1098](https://attack.mitre.org/techniques/T1098/) Account Manipulation | PR.AA (identity and access control) |
| web-headers-checker | OWASP Top 10 A05 Security Misconfiguration | ID.RA, PR.PS |
| password-auditor, hash-toolkit | [T1110.002](https://attack.mitre.org/techniques/T1110/002/) Password Cracking | PR.DS (data security) |
| ransomware-simulator | [T1486](https://attack.mitre.org/techniques/T1486/) Data Encrypted for Impact, [T1491.001](https://attack.mitre.org/techniques/T1491/001/) Internal Defacement | RS, RC (respond, recover) |
| file-encryptor | | PR.DS |
| file-permissions-auditor | Finds candidates for [T1548.001](https://attack.mitre.org/techniques/T1548/001/) Setuid and Setgid | PR.PS (platform security) |
| risk-assessment-tool | | GV.RM, ID.RA (risk management) |

---

## How the repo is kept healthy

- **CI on every push and pull request** ([workflow](./.github/workflows/ci.yml)): `ruff` lints the Python, `pytest` runs the tests in [`tests/`](./tests/), ShellCheck checks the Bash scripts and a link checker makes sure no README points to a file that moved.
- **Tests for the logic that matters**: log parsing, IOC matching, IAM findings, risk scoring, header grading and hash identification. They run offline in under a second.
- **Changes are tracked** in the [CHANGELOG](./CHANGELOG.md).

To run the same checks locally:

```bash
pip install ruff pytest
ruff check .
pytest -q
```

---

## Responsible use

These tools are for learning and for systems you own or have written permission to test. Scanning or attacking anything else is illegal in most countries. The ransomware simulator in particular should only ever run inside an isolated, snapshotted VM. More detail is in [SECURITY.md](./SECURITY.md).

---

## Contact and contributing

Found a bug or have an idea? Open an issue, or read [CONTRIBUTING.md](./CONTRIBUTING.md) if you want to send a pull request. For anything security related please reach me privately on [LinkedIn](https://www.linkedin.com/in/cmdmiguelsousa/).

Released under the [MIT License](./LICENSE.md).
