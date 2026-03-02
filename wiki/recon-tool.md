# recon-tool — v1.0

Automated Bash OSINT and reconnaissance tool for domains and IP addresses. All modules run from a single menu and degrade gracefully if optional tools are missing.

---

## Features

| # | Module | Description |
|---|--------|-------------|
| 1 | WHOIS Lookup | Registrar, creation/expiry dates, name servers, contacts |
| 2 | DNS Records | A, AAAA, MX, NS, TXT, SOA, CNAME + DNSSEC detection |
| 3 | Subdomain Enumeration | Brute-forces 50 common subdomains; optional `nmap dns-brute` |
| 4 | Port Scan | SYN scan (root) or TCP connect (non-root) via Nmap; raw socket fallback |
| 5 | HTTP Headers | Status code, full headers, OWASP security audit, info disclosure check |
| 6 | SSL/TLS Certificate | Subject, SANs, expiry, fingerprint, cipher, weak TLS 1.0/1.1 detection |
| 7 | IP Geolocation | Country, region, city, ISP, ASN, timezone, coordinates |
| 8 | Full Recon | Runs all modules; saves timestamped report to `~/.local/share/recon/` |

---

## Usage

```bash
chmod +x recon_tool.sh
./recon_tool.sh

# Pass a target directly:
./recon_tool.sh example.com

# SYN scan requires root:
sudo ./recon_tool.sh
```

---

## Requirements

**Essential:** `bash 4+`, `curl`

**Optional:**

| Tool | Used for |
|------|----------|
| `whois` | WHOIS lookup |
| `dig` / `nslookup` | DNS records, DNSSEC, subdomains |
| `nmap` | Port scanning, DNS brute-force |
| `openssl` | SSL/TLS analysis |

Install on Debian/Ubuntu:
```bash
sudo apt install whois dnsutils nmap openssl curl
```

---

> **Disclaimer:** Only scan targets you own or have explicit permission to test.

---

→ [View source](../Scripts/recon-tool/) | [← Home](Home)
