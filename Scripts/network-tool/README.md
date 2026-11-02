# Net Diagnostic Tool — v4.0

A comprehensive Bash-based network diagnostic, security analysis, and monitoring tool with an interactive categorized menu. Runs on any Linux system with standard iproute2 tools.

---

## Features

### Diagnostics

| # | Option | Description |
|---|--------|-------------|
| 1 | **Network Interfaces** | Lists interfaces, MAC addresses, IP assignments, and live RX/TX byte counters from `/proc/net/dev` |
| 2 | **Ping Host** | ICMP connectivity test with configurable packet count and timeout |
| 3 | **Latency Graph** | Sends N pings and plots a color-coded ASCII bar chart (green/yellow/red); shows min/avg/max/loss summary |
| 4 | **Traceroute** | Path tracing with `traceroute` or `tracepath` fallback |
| 5 | **Routing Table** | Default gateway, full route table, and ARP/neighbour cache |

### Scanning & Discovery

| # | Option | Description |
|---|--------|-------------|
| 6 | **Port Scan (Nmap)** | SYN scan (root) or TCP connect scan (non-root); results parsed to a clean open-port list |
| 7 | **Listening Services** *(new v4.0)* | Lists all locally listening TCP/UDP ports and established connections — useful for auditing exposed services |
| 8 | **Host Discovery** *(new v4.0)* | Pings all hosts on the local subnet; uses `nmap -sn` if available, otherwise `arp-scan` or ICMP sweep |

### Security & Analysis

| # | Option | Description |
|---|--------|-------------|
| 9 | **DNS Resolution** | A, AAAA, MX, NS, and TXT lookups with query timing and DNSSEC detection |
| 10 | **SSL Certificate Check** | Cert subject/issuer/expiry (color-coded days remaining), SHA1 fingerprint, negotiated cipher, and weak protocol detection (TLS 1.0/1.1 flagged) |
| 11 | **HTTP Response Checker** *(new v4.0)* | Checks status code, redirect chain, connect/total time, response size, and audits all OWASP security headers and information disclosure |
| 12 | **Firewall Status** *(new v4.0)* | Reports active rules from UFW, firewalld, iptables, and nftables — whichever is installed |

### Information & Monitoring

| # | Option | Description |
|---|--------|-------------|
| 13 | **Speed Test** | Download speed in Mbps; uses `speedtest-cli` if installed, otherwise hits Cloudflare/OVH endpoints |
| 14 | **Connection Info & Geolocation** | Public IP with ISP, org, country, city, timezone from ip-api.com; active connections via `ss` |
| 15 | **WiFi Diagnostics** | SSID, signal, channel, Tx bitrate via `iw`; nearby network scan via `nmcli`; `iwconfig` fallback |
| 16 | **Bandwidth Monitor** | Real-time per-second download/upload rates and packet counts; Ctrl+C stops the monitor without exiting the tool |

---

## Usage

```bash
chmod +x net_diagnostic_tool.sh
./net_diagnostic_tool.sh

# Some features (port scan, firewall, host discovery) benefit from root:
sudo ./net_diagnostic_tool.sh
```

---

## Requirements

**Essential** (standard on all Linux distros):
```
bash 4+    ip (iproute2)    ping    curl    awk
```

**Optional** — the tool degrades gracefully if any are missing:

| Tool | Used for |
|------|----------|
| `nmap` | Port scanning, host discovery |
| `traceroute` / `tracepath` | Traceroute |
| `dig` / `nslookup` / `host` | DNS resolution |
| `openssl` | SSL certificate check |
| `iw` / `nmcli` / `iwconfig` | WiFi diagnostics |
| `speedtest-cli` / `speedtest` | Accurate speed test |
| `python3` | JSON parsing for geolocation |
| `ss` / `netstat` | Connection stats, listening ports |
| `ufw` / `iptables` / `nft` | Firewall status |
| `arp-scan` | ARP-based host discovery |

Install all optional tools on Debian/Ubuntu:
```bash
sudo apt install nmap traceroute dnsutils iproute2 curl openssl \
                 wireless-tools iw network-manager arp-scan
```

---

## Configuration

Edit these variables at the top of the script:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_FILE` | `~/.local/share/netdiag/network_diagnostic.log` | Persistent log path |
| `DEFAULT_PING_COUNT` | `4` | Default ping packet count |
| `DEFAULT_NMAP_PORTS` | `1-1000` | Default nmap port range |
| `TIMEOUT_SECONDS` | `10` | Command timeout |

---

## Workflow Examples

**Diagnose slow internet:**
```
3 → Latency Graph      # spot jitter and packet loss
13 → Speed Test        # confirm throughput
4 → Traceroute         # find the slow hop
```

**Inspect a domain or web service:**
```
9  → DNS Resolution         # A/AAAA/MX/NS/TXT + DNSSEC
10 → SSL Certificate Check  # cert validity, weak TLS versions
11 → HTTP Response Checker  # status, headers, security audit
```

**Audit local machine security:**
```
7  → Listening Services     # what's exposed locally
12 → Firewall Status        # are the right rules in place
8  → Host Discovery         # what else is on the network
```

**Monitor a machine:**
```
16 → Bandwidth Monitor      # live RX/TX on chosen interface
14 → Connection Info        # established connections + geolocation
```

---

## Changelog

| Version | Changes |
|---------|---------|
| **v4.0** | Added: Listening Services, Host Discovery, HTTP Response Checker, Firewall Status. DNS: added TXT records and DNSSEC detection. SSL: added weak protocol detection (TLS 1.0/1.1). Latency Graph: added color legend. Menu reorganized into 4 categories. |
| **v3.0** | Added: Latency Graph, SSL Certificate Check, WiFi Diagnostics, Bandwidth Monitor, Geolocation. |
| **v2.0** | Menu-driven interface, logging, color output. |
| **v1.0** | Initial network diagnostic script. |

---

## Notes

- Log file is written to `~/.local/share/netdiag/` — not the working directory.
- Ctrl+C inside **Bandwidth Monitor** stops only the monitor — the menu remains open.
- Only scan hosts and networks you own or have explicit permission to test.

---

**Disclaimer:** Use responsibly and only on networks you own or have permission to test. Unauthorised scanning may be illegal in your jurisdiction.
