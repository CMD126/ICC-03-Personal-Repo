# Recon Tool — v1.0

A menu-driven Bash OSINT and reconnaissance tool for domains and IP addresses. Runs all major passive and active recon modules from a single interface. Degrades gracefully if optional tools are not installed.

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | **WHOIS Lookup** | Registrar, registrant, creation/expiry dates, name servers, and status fields |
| 2 | **DNS Records** | Full A/AAAA/MX/NS/TXT/SOA/CNAME enumeration with DNSSEC detection |
| 3 | **Subdomain Enumeration** | Brute-forces 50 common subdomains via DNS resolution; optionally uses `nmap --script dns-brute` |
| 4 | **Port Scan** | SYN scan (root) or TCP connect scan (non-root) of top 1000 ports via Nmap; raw socket fallback on common ports |
| 5 | **HTTP Headers & Security Audit** | Status code, full response headers, OWASP security header audit (7 headers), information disclosure check |
| 6 | **SSL/TLS Certificate Analysis** | Subject, issuer, SANs, expiry with color-coded days remaining, SHA-1 fingerprint, cipher, weak protocol detection (TLS 1.0/1.1) |
| 7 | **IP Geolocation** | Country, region, city, ISP, org, ASN, timezone, coordinates from ip-api.com |
| 8 | **Full Recon** | Runs all modules sequentially; saves a timestamped report to `~/.local/share/recon/` |

---

## Usage

```bash
chmod +x recon_tool.sh
./recon_tool.sh

# Optionally pass a target directly:
./recon_tool.sh example.com

# Some features (SYN port scan) benefit from root:
sudo ./recon_tool.sh
```

---

## Requirements

**Essential:**
```
bash 4+    curl
```

**Optional** — tool degrades gracefully if missing:

| Tool | Used for |
|------|----------|
| `whois` | WHOIS lookup |
| `dig` / `nslookup` | DNS records, DNSSEC, subdomain enumeration |
| `nmap` | Port scanning, DNS brute-force |
| `openssl` | SSL/TLS certificate analysis |

Install all on Debian/Ubuntu:
```bash
sudo apt install whois dnsutils nmap openssl curl
```

---

## Output

- Results are displayed with color-coded output in the terminal.
- Full recon reports are saved to `~/.local/share/recon/recon_<target>_<timestamp>.txt`.

---

## Workflow Examples

**Domain recon before a pentest:**
```
t → Set target (example.com)
1 → WHOIS         # registrar, expiry, contacts
2 → DNS Records   # infrastructure mapping
3 → Subdomains    # attack surface discovery
6 → SSL/TLS       # certificate issues, weak protocols
```

**Web application audit:**
```
5 → HTTP Headers  # missing security headers, server disclosure
6 → SSL/TLS       # cert validity, weak TLS versions
4 → Port Scan     # open services beyond 80/443
```

**Quick IP investigation:**
```
7 → Geolocation   # ISP, country, ASN
4 → Port Scan     # what's running on the IP
```

---

**Disclaimer:** Use only on targets you own or have explicit written permission to test. Unauthorized scanning may be illegal in your jurisdiction.
