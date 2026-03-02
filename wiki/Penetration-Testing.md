# Penetration Testing

Offensive security techniques, Nmap scanning, and hands-on exploitation exercises.

---

## Notes

### Nmap Scan Types

| Scan | Command | Notes |
|------|---------|-------|
| Quick scan | `nmap -T4 -F <target>` | Top 100 ports |
| Full TCP | `nmap -p- <target>` | All 65535 ports |
| Service/version | `nmap -sV <target>` | Detect service versions |
| OS detection | `nmap -O <target>` | Requires root |
| Script scan | `nmap -sC <target>` | Default NSE scripts |
| Vulnerability | `nmap --script vuln <target>` | Known CVEs |
| UDP | `nmap -sU <target>` | Slow — top UDP ports |
| Ping sweep | `nmap -sn <subnet>` | Host discovery only |
| SYN scan | `nmap -sS <target>` | Stealth — requires root |

### Nmap Output Formats

| Flag | Output |
|------|--------|
| `-oN` | Normal text |
| `-oX` | XML |
| `-oG` | Grepable |
| `-oA` | All three formats |

### Pentest Phases

| Phase | Description |
|-------|-------------|
| Reconnaissance | Passive/active info gathering |
| Scanning | Port/service enumeration |
| Exploitation | Gaining access |
| Post-Exploitation | Privilege escalation, lateral movement |
| Reporting | Document findings and remediations |

→ [View full Nmap cheat sheet](../Penetration%20Testing/notes/Nmap/README.md)

---

## Exercises

### port-scanner
TCP connect scanner built with raw Python sockets.
- Multithreaded with `ThreadPoolExecutor`
- Scans common ports or custom range
- Service name mapping
- Optional banner grabbing

```bash
python3 port_scanner.py
```

→ [View exercise](../Penetration%20Testing/exercises/port-scanner/)

---

> **Disclaimer:** Only scan systems you own or have explicit written permission to test.

---

[← Home](Home)
