# Changelog

All notable changes to this repository are documented here.

---

## [Unreleased]

- Exercises for GRC, Cloud Security, and Threat Hunting — in progress

---

## [3.0.0] — 2026

### Changed
- Restructured entire repository: merged separate `/Notes` and `/Exercises` directories into unified topic-based module folders at the root level
- Each module now contains `notes/` and `exercises/` subdirectories
- Removed `Module X - ` prefix from all folder names — folders are now named by topic only (e.g., `Data Security/`, `Penetration Testing/`)
- Updated `README.md`, `CONTRIBUTING.md` to reflect new structure

---

## [2.3.0] — 2026

### Added
- New script: `hash-toolkit` — menu-driven Python tool for hash identification (20+ types), generation (MD5–SHA3–BLAKE2b), file integrity checking, and constant-time hash comparison
- New script: `recon-tool` — Bash OSINT and reconnaissance tool with 8 modules: WHOIS, DNS records, subdomain enumeration, port scanning, HTTP security headers, SSL/TLS analysis, IP geolocation, and full recon with report saving

### Removed
- `Scripts/basic-shell-commands/` — removed (too basic, not cybersecurity-relevant)
- `Exercises/Module 0 - Foundations/` — hello-world and file-handler exercises removed
- `Exercises/Module 1 - Networking and Systems Administration/` — network-tool bash exercise removed

### Changed
- Network Diagnostic Tool upgraded to **v4.0**: added Listening Services, Host Discovery, HTTP Response Checker, Firewall Status; enhanced DNS (TXT + DNSSEC) and SSL (weak protocol detection); menu reorganized into 4 categories
- Updated main `README.md` to reflect all script changes

---

## [2.1.0] — 2025

### Changed
- Renamed all script files to combine brand identity with function description:
  - `syscript.sh` → `syscript_sysadmin.sh`
  - `nmatrix.sh` → `nmatrix_nmap_scanner.sh`
  - `network_tool.sh` (Scripts) → `net_diagnostic_tool.sh`
  - `abdns.py` → `abdns_dns_benchmark.py`
  - `shell_commands.py` → `shell_exec_demo.py`
  - `lexcrypt.py` → `lexcrypt_file_encryptor.py`
  - `messages.py` → `message_encryptor.py`
  - `network_tool.sh` (Exercises) → `net_recon_tool.sh`
- Updated all README usage examples to reflect new filenames

---

## [2.0.0] — 2025

### Added
- Full module-based folder structure for `/Notes` (Module 0–8) with cheat sheets
- Full module-based folder structure for `/Exercises` (Module 0–8)
- New exercises: `password-auditor`, `log-analyzer`, `port-scanner`, `web-headers-checker`
- New cheat sheets: GRC, Data Security, Security Operations, Cloud Security, Threat Hunting, Application Security
- `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
- GitHub issue templates (bug report, feature request)
- `requirements.txt` for Python exercises with external dependencies
- `README.md` added to previously undocumented exercises (`hello-world`, `file-handler`)

### Changed
- Reorganized all `/Exercises` into module subdirectories matching `/Notes` structure
- Renamed `/Scripts` folders to consistent lowercase-hyphen convention:
  - `NMATRIX` → `nmatrix`
  - `ABDNS` → `abdns`
  - `Network-Tool` → `network-tool`
  - `Basic_py_script` → `basic-shell-commands`
- Renamed script files to snake_case:
  - `act.sh` → `syscript.sh`
  - `networktool.sh` → `network_tool.sh`
  - `script.py` → `shell_commands.py`
  - `hscript.py` → `file_handler.py`
  - `ransom_win_be.py` → `ransomware_simulator.py`
  - `my_network_tool.sh` → `network_tool.sh`
- Renamed `Lexcript/` → `file-encryptor/`
- Renamed `ransomware_py/` → `ransomware-simulator/`
- Renamed `ss/` screenshots folder → `screenshots/`
- Updated all README.md files to reflect new paths and filenames
- Fixed unescaped `<group>` in Linux cheat sheet
- Fixed switches/repeaters placement in OSI Model cheat sheet
- Reformatted Nmap README from single mega-table to sectioned layout
- Reformatted Ubuntu shortcuts README — split combined shortcut rows

---

## [1.0.0] — 2025-03

### Added
- Initial repository structure with `/Scripts`, `/Exercises`, `/Notes`
- Scripts: `syscript`, `NMATRIX`, `Network-Tool`, `ABDNS`, `Basic_py_script`
- Exercises: `hello_world`, `bash_scripting`, `hscript`, `Lexcript`, `ransomware_py`
- Notes: Linux, Ubuntu, OSI Model, Wireshark, Nmap
- `README.md`, `LICENSE.md`, `CODE_OF_CONDUCT.md`
- `.github/` configuration (CODEOWNERS, PR template, settings)
