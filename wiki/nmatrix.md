# nmatrix — v2.0

Matrix-style, menu-driven Nmap frontend with scan logging and file export.

---

## Features

| # | Scan Type | Description |
|---|-----------|-------------|
| 1 | Quick Scan | Fast scan of top 100 ports (`-T4 -F`) |
| 2 | Full TCP Scan | All 65535 ports (`-p-`) |
| 3 | Service + Script | Version detection and default NSE scripts (`-sV -sC`) |
| 4 | OS Detection | Operating system fingerprinting (`-O`) — requires root |
| 5 | UDP Scan | Top UDP ports (`-sU`) — requires root |
| 6 | Ping Sweep | Host discovery on a subnet (`-sn`) |
| 7 | Vulnerability Scan | Known CVE checks (`--script vuln`) |
| 8 | Custom Scan | Enter any custom Nmap flags |

---

## Usage

```bash
chmod +x nmatrix_nmap_scanner.sh
./nmatrix_nmap_scanner.sh

# OS detection and UDP scans require root:
sudo ./nmatrix_nmap_scanner.sh
```

---

## Requirements

| Tool | Used for |
|------|----------|
| `bash 4+` | Required |
| `nmap` | Required — all scans |

---

→ [View source](../Scripts/nmatrix/) | [← Home](Home)
