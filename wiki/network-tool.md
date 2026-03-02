# network-tool — v4.0

Comprehensive Bash network diagnostic, security analysis, and monitoring tool with 16 options across 4 categories.

---

## Features

### Diagnostics
| # | Option | Description |
|---|--------|-------------|
| 1 | Network Interfaces | Lists interfaces, MAC addresses, IPs, and live RX/TX counters |
| 2 | Ping Host | ICMP connectivity test with configurable packet count |
| 3 | Latency Graph | Sends N pings and plots a color-coded ASCII bar chart |
| 4 | Traceroute | Path tracing with `traceroute` or `tracepath` fallback |
| 5 | Routing Table | Default gateway, full route table, and ARP cache |

### Scanning & Discovery
| # | Option | Description |
|---|--------|-------------|
| 6 | Port Scan | Nmap SYN or TCP connect scan; results parsed to open-port list |
| 7 | Listening Services | All locally listening TCP/UDP ports and established connections |
| 8 | Host Discovery | Pings all hosts on local subnet; `nmap -sn` / `arp-scan` / ICMP fallback |

### Security & Analysis
| # | Option | Description |
|---|--------|-------------|
| 9 | DNS Resolution | A/AAAA/MX/NS/TXT lookups + DNSSEC detection |
| 10 | SSL Certificate | Cert subject/issuer/expiry, fingerprint, cipher, weak TLS detection |
| 11 | HTTP Response | Status code, redirect chain, timing, OWASP header audit |
| 12 | Firewall Status | UFW, firewalld, iptables, nftables — whichever is installed |

### Information & Monitoring
| # | Option | Description |
|---|--------|-------------|
| 13 | Speed Test | Download speed; `speedtest-cli` or Cloudflare/OVH fallback |
| 14 | Connection Info | Public IP, ISP, geolocation, active connections |
| 15 | WiFi Diagnostics | SSID, signal, channel, Tx bitrate; nearby network scan |
| 16 | Bandwidth Monitor | Real-time per-second RX/TX rates and packet counts |

---

## Usage

```bash
chmod +x net_diagnostic_tool.sh
./net_diagnostic_tool.sh

# Some features benefit from root:
sudo ./net_diagnostic_tool.sh
```

---

## Requirements

**Essential:** `bash 4+`, `ip`, `ping`, `curl`, `awk`

**Optional:** `nmap`, `traceroute`, `dig`, `openssl`, `iw`, `nmcli`, `speedtest-cli`, `ss`, `ufw`, `arp-scan`

---

→ [View source](../Scripts/network-tool/) | [← Home](Home)
