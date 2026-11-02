# Product Backlog: Scrum (1 item / day)

Sprint = 1 week (5 days). One story per day. Daily agent takes the first `[ ]` item,
does it, marks it `[x]`, adds date, pushes.

**Definition of Done**
- Code runs (`python3 -m py_compile`, `bash -n`).
- `ruff check .` and `pytest -q` pass, and CI is green.
- README of touched tool updated.
- `CHANGELOG.md` → `[Unreleased]` updated.
- Item ticked here with date.

---

## Sprint 1: Repo hygiene & quality gates

- [x] **S1-1** Merge duplicate `Scripts/` folders (`ABDNS`/`abdns`, `NMATRIX`/`nmatrix`, `Network-Tool`/`network-tool`) and fix broken `.gitignore` (stray `cat << 'EOF'` lines, over-broad `settings.py`, `*.crt`, `migrations/`, `*.editorconfig`). Done 2026-11-02
- [x] **S1-2** Add `pyproject.toml` with ruff config; fix the ~23 auto-fixable ruff findings (unused imports, etc.). Done 2026-11-02 in PR #10
- [x] **S1-3** Add GitHub Actions CI: ruff + `py_compile` for Python, `shellcheck` + `bash -n` for shell scripts. Done 2026-11-02 in PR #10 (ruff, pytest, ShellCheck, link check)
- [x] **S1-4** Add `tests/` with pytest for pure functions: `subnet_calculator`, `risk_assessment_tool.get_severity`, `hash_toolkit` hash identify. Done 2026-11-02 in PR #10 (24 tests, also log analyzer, IOC scanner, IAM analyzer, header grading)
- [x] **S1-5** Fix remaining ruff warnings (bare `except: pass`, implicit Optional, unused vars, `sys.exit`). Done 2026-11-02 in PR #10 (bare excepts and unused vars fixed; implicit Optional and `sys.exit` are outside the chosen ruff rules)

## Sprint 2: Security & robustness

- [ ] **S2-1** `ransomware_simulator.py`: guard `ctypes.windll` import (crash on Linux/macOS), require `--i-understand-vm-only` flag, keep target dir limited to lab folder.
- [ ] **S2-2** `message_encryptor.py`: store `key.key` next to script (not cwd), `chmod 600`, warn before overwrite.
- [ ] **S2-3** `lexcrypt_file_encryptor.py`: store salt per file (header) instead of one shared `salt.bin`.
- [ ] **S2-4** `password_auditor.py`: add PBKDF2 / `hashlib.scrypt` demo next to MD5/SHA to show slow hash.
- [ ] **S2-5** `web_headers_checker.py`: add timeout, follow redirects, check `Permissions-Policy` + cookie flags.

## Sprint 3: Usability (CLI)

- [ ] **S3-1** Add `argparse` non-interactive mode to `port_scanner.py` (`-t host -p 1-1024`).
- [ ] **S3-2** Add `argparse` to `log_analyzer.py` (`--file`, `--json` output) + sample `auth.log`.
- [ ] **S3-3** Add `argparse` to `ioc_scanner.py` and `iam_policy_analyzer.py` (`--json` output).
- [ ] **S3-4** Add `--help` / `-h` flag to all Bash tools (`syscript`, `nmatrix`, `network-tool`, `recon-tool`).
- [ ] **S3-5** Root `requirements.txt` + "Getting Started" section with venv steps.

## Sprint 4: Content

- [ ] **S4-1** Threat Hunting notes: MITRE ATT&CK mapping cheat sheet.
- [ ] **S4-2** Cloud Security exercise: S3 bucket policy checker (public access detection).
- [ ] **S4-3** Networking exercise: simple pcap summary with `scapy` (optional dep).
- [ ] **S4-4** AppSec exercise: SQLi / XSS input-validation demo (local Flask, safe vs unsafe).
- [ ] **S4-5** Sprint retro: update README tables, bump CHANGELOG version.

---

## Retro notes

_Daily agent adds one line per day: what done, what blocked._

- 2026-11-02: S1-1 done. No block.
- 2026-11-02: S1-2 to S1-5 done in PR #10, together with the folder rename to `00-foundations` … `08-penetration-testing` and `tools/`.
