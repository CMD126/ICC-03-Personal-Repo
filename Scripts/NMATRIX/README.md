# NMATRIX — Matrix-style Nmap Scanner v2.0

A bash menu-driven frontend for `nmap` with a Matrix digital-rain intro animation.

## Features

| # | Scan | nmap flags | Notes |
|---|------|-----------|-------|
| 1 | **Quick TCP** | `-sS -T4 --top-ports 100` | Top 100 ports, fast |
| 2 | **Full TCP** | `-sS -p- -sV -T4` | All 65535 ports + version detection |
| 3 | **Service & Script** | `-sC -sV -T4` | Default NSE scripts + version; full script output shown |
| 4 | **OS Detection** | `-O -T4` | Guesses operating system; requires root |
| 5 | **UDP Scan** | `-sU --top-ports 100 -T4` | Top 100 UDP ports; slower by nature |
| 6 | **Ping Sweep** | `-sn` | Discovers live hosts on a subnet; no port scan |
| 7 | **Vulnerability Scan** | `--script vuln -T4` | Runs NSE vuln scripts; only use on authorised targets |
| 8 | **Custom Scan** | user-defined | Enter any nmap flags manually |
| 9 | **View Log** | — | Last 30 entries from `~/.local/share/nmatrix/scans.log` |

## What changed in v2.0

- **Animation fixed** — heads now advance *once per frame* (not inside the row loop), giving correct cascading rain. Variable column speeds (1–3 frame intervals) and a larger character set (`!#$%&*+/<=>?@[\]^{}|~0123456789ABCDEFabcdef`). Bright-green head, normal-green trail, dim-green fade at tail end.
- **Animation runs once at startup** — no longer repeats before every menu.
- **`sudo` only when not root** — if you run as root, `sudo` is skipped.
- **Portable grep** — removed `-P` (Perl regex) flag; uses `-E` (extended) which works on GNU/BSD/macOS.
- **Proper output table** — port, state, service, and full version string displayed in aligned columns with colour.
- **Save results** — after every scan you can save the raw nmap output to a timestamped `.txt` file.
- **Logging** — every scan is timestamped and appended to `~/.local/share/nmatrix/scans.log`.
- **4 new scan types** — Service+Script, OS Detection, Vulnerability Scan, Custom Scan.
- **Cursor always restored** — `trap` on EXIT ensures the terminal cursor is shown even if the script crashes.

## Requirements

- `bash` 4+
- `nmap` — `sudo apt install nmap`

## Usage

```bash
chmod +x nmatrix.sh
./nmatrix.sh

# Some scans (SYN, OS detection) need root:
sudo ./nmatrix.sh
```

## Notes

- **Legal**: Only scan hosts and networks you own or have explicit written permission to test.
- Scan results are saved in the current working directory as `nmap_<type>_<target>_<timestamp>.txt`.
- The log file is at `~/.local/share/nmatrix/scans.log`.

---

Created by @lexlucas
**Disclaimer**: Use responsibly. Unauthorised port scanning may be illegal in your jurisdiction.
