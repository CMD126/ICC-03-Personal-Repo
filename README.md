# ICC-03 Cybersecurity Learning Repository
## About This Repository
Welcome to the ICC-03 Cybersecurity Learning Repository! This collection of personal notes, exercises, and custom-built scripts was developed during the ICC-03 cybersecurity program. It is designed to be a practical and evolving resource for anyone interested in cybersecurity, from beginners to experienced practitioners.
Here, you will find tools and resources to support your learning in network security, system administration, and automation.
## Key Features
- **Practical Scripts**: A suite of custom scripts for tasks like network optimization, system administration, and data conversion.
- **Hands-On Learning**: A collection of exercises and study notes covering various cybersecurity topics.
- **Open Source**: Licensed under the MIT License, so you can freely use, modify, and distribute the contents.
## Tools
This repository includes a variety of custom-built scripts to automate and simplify common cybersecurity tasks. Each tool is located in its own directory within the `/Scripts` folder, which contains the script itself and a `README.md` file with detailed instructions.

**Note**: Some educational simulations (e.g., ransomware) are located under `/Exercises` for safety and learning focus.

| Tool | Description |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| [Syscript](./Scripts/syscript/) | **v2.0** — A menu-driven bash toolkit for Ubuntu/Debian administration. Covers package management, system info, networking, service control, firewall status, and a live system health dashboard. |
| [NMATRIX](./Scripts/NMATRIX/) | **v2.0** — A Matrix-style, menu-driven frontend for `nmap` with 8 scan types (Quick/Full TCP, Service+Script, OS Detection, UDP, Ping Sweep, Vulnerability, Custom), scan logging, and save-to-file support. |
| [Network-Tool](./Scripts/Network-Tool/) | **v3.0** — A comprehensive bash network diagnostic utility with 14 options including a latency ASCII graph, SSL certificate checker, WiFi diagnostics, real-time bandwidth monitor, and geolocation lookup. |
| [ABDNS](./Scripts/ABDNS/) | A Python script that benchmarks 9 public DNS providers using real UDP queries, reports packet loss, and applies the fastest primary + secondary DNS on Linux, macOS, or Windows. |
| [Basic Py Script](./Scripts/Basic_py_script/) | A simple Python script that demonstrates how to execute shell commands (`ls`, `whoami`) and print their output to the console. |
| [LEXCRYPT](./Exercises/Lexcript/) | A Python GUI app (Tkinter) for file and message encryption/decryption. Uses PBKDF2-SHA256 key derivation, Fernet (AES-128-CBC) encryption, and chunked I/O for large files. |
| [Ransomware Simulator](./Exercises/ransomware_py/) | **Educational only** – A Python-based simulation demonstrating ransomware encryption/decryption using password-derived keys and Fernet (AES). Includes full recovery. |

## Repository Structure
| Directory | Description |
| ------------ | ---------------------------------------------------------------------------------------------------- |
| `/Exercises` | Contains hands-on exercises and tasks related to the course material, including encryption simulations and defensive labs. |
| `/Notes` | A collection of personal study notes on various cybersecurity topics, including tools like Wireshark. |
| `/Scripts` | A collection of custom scripts for various purposes. See the [Tools](#tools) section for details. |

## Getting Started
To get a local copy of this repository, clone it using the following command:
```bash
git clone https://github.com/CMD126/ICC-03-Personal-Repo.git
```

## License
This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.
