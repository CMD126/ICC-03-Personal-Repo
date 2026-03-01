# Syscript — Ubuntu Admin Toolkit v2.0

A menu-driven bash script for common Ubuntu/Debian system administration tasks. Grouped into categories with colour output and a live header showing hostname, uptime, and load averages.

## Menu Reference

### Package Management
| # | Option | Command(s) |
|---|--------|-----------|
| 1 | Update & full-upgrade | `apt update && apt full-upgrade -y` |
| 2 | Autoremove | `apt autoremove -y` |
| 3 | Clean cache | `apt clean && apt autoclean` |
| 4 | List upgradable | `apt list --upgradable` |
| 5 | List installed | `dpkg --get-selections` (piped to `less`) |
| 6 | Search repository | `apt-cache search` |
| 7 | Install package | `apt install` |
| 8 | Remove package | `apt remove` — asks confirmation |
| 9 | **Purge package** *(new)* | `apt purge` — removes config too, asks confirmation |

### System Information
| # | Option | What it shows |
|---|--------|--------------|
| 10 | Disk usage | `df -h` filtered to real devices |
| 11 | Memory & swap | `free -h` + `/proc/meminfo` summary |
| 12 | **CPU info & load** *(new)* | Model, core count, cache, load average (1/5/15m), uptime |
| 13 | System info | `uname -a` + `lsb_release -a` / `/etc/os-release` |
| 14 | Running processes | Top 20 by CPU + top 10 by memory (`ps aux --sort`) |
| 15 | Hardware summary | `lshw -short` with fallback to `/proc/cpuinfo`, `lsblk`, `lspci` |

### Network
| # | Option | What it shows |
|---|--------|--------------|
| 16 | Network interfaces | `ip -brief addr` + detailed `ip addr` |
| 17 | Open ports & listeners | `ss -tuln` |
| 18 | **Active connections** *(new)* | `ss -tupn state established` |

### System Management
| # | Option | Notes |
|---|--------|-------|
| 19 | System logs | Last 50 entries, `--no-pager` — no pager trap |
| 20 | **Failed services** *(new)* | `systemctl --failed` with pass/fail colour |
| 21 | **Service control** *(new)* | Status / Start / Stop / Restart / Enable / Disable for any service |
| 22 | **UFW firewall status** *(new)* | `ufw status verbose` |
| 23 | **Clear old journals** *(new)* | `journalctl --vacuum-time=Nd` — asks how many days to keep |

### User & Environment
| # | Option | What it shows |
|---|--------|--------------|
| 24 | User info | `whoami` + `id` + groups + shell + home + last logins |
| 25 | Scheduled tasks | `crontab -l` (skips comments) + `systemctl list-timers` |
| 26 | Environment variables | `printenv \| sort` piped to `less` |
| 27 | Bash history | **Reads `~/.bash_history` directly** — works correctly in a script |

### Extra
| # | Option | Notes |
|---|--------|-------|
| 28 | **System health overview** *(new)* | Dashboard: uptime, load, memory bar, disk bars per device, failed services, pending updates |

## What changed in v2.0

- **`read -s` removed** — was silent with no prompt; replaced with `read -rp "Enter choice: "` so input is visible
- **Portuguese strings removed** — `"Erro ao remover pacotes."` and `"Pressione Enter para continuar..."` replaced with English
- **`history` fixed** — bash builtin returns nothing in a subshell; now reads `~/.bash_history` (or `$HISTFILE`)
- **`journalctl -xe` replaced** — was opening an endless pager; now uses `journalctl -n 50 --no-pager`
- **`ps aux` replaced** — was dumping hundreds of lines; now shows top 20 by CPU and top 10 by memory
- **Option 16 expanded** — was just `whoami`; now shows `id`, groups, shell, home directory, and last logins
- **`lshw` guarded** — checks if installed before calling; falls back to `/proc/cpuinfo`, `lsblk`, `lspci`
- **Confirmation prompts** — Remove and Purge ask before executing destructive operations
- **Color-coded UI** — section headers, prompts, success/warning/error messages all colour-coded
- **Functions** — each option is its own function; no more deeply nested case statements
- **Empty input ignored** — pressing Enter at the menu without a choice no longer shows "Invalid option"
- **7 new menu options** added (9, 12, 18, 20, 21, 22, 23, 28)

## Requirements

- Ubuntu / Debian-based Linux
- `bash` 4+, `sudo` privileges for admin operations

**Optional tools** (gracefully skipped if missing):
- `lshw` — hardware summary (falls back to `/proc/cpuinfo`, `lsblk`)
- `lspci` — PCI device list
- `ufw` — firewall status
- `lsb_release` — distro info (falls back to `/etc/os-release`)

## Usage

```bash
chmod +x act.sh
./act.sh
```

---

Created by @lexlucas
