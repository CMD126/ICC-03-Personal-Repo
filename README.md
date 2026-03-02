# ICC-03 Cybersecurity Learning Repository

## Table of Contents

- [About](#about)
- [Repository Structure](#repository-structure)
- [Tools](#tools)
- [Notes](#notes)
- [Getting Started](#getting-started)
- [License](#license)

---

## About

Welcome to the ICC-03 Cybersecurity Learning Repository! This collection of personal notes, exercises, and custom-built scripts was developed during the ICC-03 cybersecurity program. It is designed to be a practical and evolving resource for anyone interested in cybersecurity, from beginners to experienced practitioners.

Here you will find tools and resources to support learning across network security, system administration, threat operations, cloud security, and more.

---

## Repository Structure

| Directory | Description |
|-----------|-------------|
| `/Scripts` | Custom-built scripts to automate and simplify common cybersecurity tasks. |
| `/Exercises` | Hands-on exercises and simulations, including encryption and defensive labs. |
| `/Notes` | Personal study notes organized by course module (Module 0–8). |

---

## Tools

Each tool lives in its own directory under `/Scripts` with a `README.md` containing detailed usage instructions.

**Note:** Educational simulations (e.g., ransomware) are located under `/Exercises` for safety and learning focus.

| Tool | Description |
|------|-------------|
| [Syscript](./Scripts/syscript/) | **v2.0** — A menu-driven bash toolkit for Ubuntu/Debian administration. Covers package management, system info, networking, service control, firewall status, and a live system health dashboard. |
| [NMATRIX](./Scripts/NMATRIX/) | **v2.0** — A Matrix-style, menu-driven frontend for `nmap` with 8 scan types (Quick/Full TCP, Service+Script, OS Detection, UDP, Ping Sweep, Vulnerability, Custom), scan logging, and save-to-file support. |
| [Network-Tool](./Scripts/Network-Tool/) | **v3.0** — A comprehensive bash network diagnostic utility with 14 options including a latency ASCII graph, SSL certificate checker, WiFi diagnostics, real-time bandwidth monitor, and geolocation lookup. |
| [ABDNS](./Scripts/ABDNS/) | A Python script that benchmarks 9 public DNS providers using real UDP queries, reports packet loss, and applies the fastest primary + secondary DNS on Linux, macOS, or Windows. |
| [Basic Py Script](./Scripts/Basic_py_script/) | A simple Python script that demonstrates how to execute shell commands (`ls`, `whoami`) and print their output to the console. |
| [LEXCRYPT](./Exercises/Lexcript/) | A Python GUI app (Tkinter) for file and message encryption/decryption. Uses PBKDF2-SHA256 key derivation, Fernet (AES-128-CBC) encryption, and chunked I/O for large files. |
| [Ransomware Simulator](./Exercises/ransomware_py/) | **Educational only** — A Python-based simulation demonstrating ransomware encryption/decryption using password-derived keys and Fernet (AES). Includes full recovery. |

---

## Notes

Study notes are organized by course module under `/Notes`. Each module contains cheat sheets and references for its topic area.

| Module | Topic | Notes |
|--------|-------|-------|
| [Module 0](./Notes/Module%200%20-%20Foundations/) | Foundations | [Linux](./Notes/Module%200%20-%20Foundations/Linux/README.md), [Ubuntu](./Notes/Module%200%20-%20Foundations/Ubuntu/README.md) |
| [Module 1](./Notes/Module%201%20-%20Networking%20and%20Systems%20Administration/) | Networking and Systems Administration | [OSI Model](./Notes/Module%201%20-%20Networking%20and%20Systems%20Administration/OSI%20Model/README.md), [Wireshark](./Notes/Module%201%20-%20Networking%20and%20Systems%20Administration/Wireshark/README.md) |
| [Module 2](./Notes/Module%202%20-%20Governance%2C%20Risk%2C%20and%20Compliance%20(GRC)/) | Governance, Risk, and Compliance (GRC) | [GRC Cheat Sheet](./Notes/Module%202%20-%20Governance%2C%20Risk%2C%20and%20Compliance%20(GRC)/README.md) |
| [Module 3](./Notes/Module%203%20-%20Data%20Security/) | Data Security | [Data Security Cheat Sheet](./Notes/Module%203%20-%20Data%20Security/README.md) |
| [Module 4](./Notes/Module%204%20-%20Security%20Operations/) | Security Operations | [SecOps Cheat Sheet](./Notes/Module%204%20-%20Security%20Operations/README.md) |
| [Module 5](./Notes/Module%205%20-%20Cloud%20Security/) | Cloud Security | [Cloud Security Cheat Sheet](./Notes/Module%205%20-%20Cloud%20Security/README.md) |
| [Module 6](./Notes/Module%206%20-%20Threat%20Hunting/) | Threat Hunting | [Threat Hunting Cheat Sheet](./Notes/Module%206%20-%20Threat%20Hunting/README.md) |
| [Module 7](./Notes/Module%207%20-%20Application%20Security%20and%20Vulnerability%20Analysis/) | Application Security and Vulnerability Analysis | [AppSec Cheat Sheet](./Notes/Module%207%20-%20Application%20Security%20and%20Vulnerability%20Analysis/README.md) |
| [Module 8](./Notes/Module%208%20-%20Penetration%20Testing/) | Penetration Testing | [Nmap](./Notes/Module%208%20-%20Penetration%20Testing/Nmap/README.md) |

---

## Getting Started

Clone the repository locally:

```bash
git clone https://github.com/CMD126/ICC-03-Personal-Repo.git
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.
