# Network Tool — v3.0

A bash-based network diagnostic and monitoring tool with an interactive menu. Runs on any Linux system with standard iproute2 tools.

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | **Network Interfaces** | Lists interfaces, MAC addresses, IP assignments, and live RX/TX byte counters from `/proc/net/dev` |
| 2 | **Ping Host** | ICMP connectivity test with configurable count and timeout |
| 3 | **Latency Graph** *(new)* | Sends N pings and plots an ASCII bar chart of round-trip times; shows min/avg/max/loss summary |
| 4 | **Port Scan** | nmap SYN scan (root) or TCP connect scan (non-root); results parsed to a clean port list |
| 5 | **Routing Table** | Default gateway, full route table, and ARP/neighbour cache |
| 6 | **Traceroute** | Path tracing with `traceroute` or `tracepath` fallback |
| 7 | **DNS Resolution** | Separate A, AAAA, MX, and NS lookups with query timing; falls back to `nslookup`/`host` |
| 8 | **Speed Test** | Download speed in Mbps; uses `speedtest-cli` if installed, otherwise hits Cloudflare/OVH endpoints |
| 9 | **SSL Certificate Check** *(new)* | Inspects TLS cert subject, issuer, validity dates, days-to-expiry (colour-coded), SHA1 fingerprint, and negotiated protocol/cipher |
| 10 | **Connection Info & Geolocation** *(enhanced)* | Public IP with ISP, country, city, timezone from ip-api.com; active connections via `ss` |
| 11 | **WiFi Diagnostics** *(new)* | SSID, signal, channel, Tx bitrate via `iw`; nearby network scan via `nmcli`; `iwconfig` fallback |
| 12 | **Bandwidth Monitor** *(new)* | Real-time per-second download/upload rates and packet counts from `/proc/net/dev`; Ctrl+C stops monitor without exiting the tool |
| 13 | **View Log** | Last 30 entries from the session log |
| 14 | **Exit** | Clean exit |

## Requirements

**Essential** (standard on all Linux distros):
- `bash` 4+, `ip` (iproute2), `ping`, `curl`, `awk`

**Optional** (gracefully degraded if missing):
| Tool | Used for |
|------|----------|
| `nmap` | Port scanning |
| `traceroute` / `tracepath` | Traceroute |
| `dig` / `nslookup` / `host` | DNS resolution |
| `openssl` | SSL certificate check |
| `iw` / `nmcli` / `iwconfig` | WiFi diagnostics |
| `speedtest-cli` / `speedtest` | Accurate speed test |
| `python3` | JSON parsing for geolocation (grep fallback used otherwise) |
| `ss` / `netstat` | Connection statistics |

Install common tools on Debian/Ubuntu:
```bash
sudo apt install nmap traceroute dnsutils iproute2 curl openssl wireless-tools iw network-manager
```

## Usage

```bash
chmod +x networktool.sh
./networktool.sh

# With elevated privileges (enables SYN scanning, resolv.conf write)
sudo ./networktool.sh
```

## Configuration

Edit these variables at the top of the script:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_FILE` | `~/.local/share/netdiag/network_diagnostic.log` | Persistent log location |
| `DEFAULT_PING_COUNT` | `4` | Default ping packet count |
| `DEFAULT_NMAP_PORTS` | `1-1000` | Default nmap port range |
| `TIMEOUT_SECONDS` | `10` | Command timeout |

## Workflow examples

**Diagnose slow internet:**
```
3 → Latency Graph (8.8.8.8)   # spot jitter / packet loss
8 → Speed Test                 # confirm throughput
6 → Traceroute                 # find the slow hop
```

**Inspect a domain:**
```
7  → DNS Resolution            # A/AAAA/MX/NS records
9  → SSL Certificate Check     # cert validity and expiry
```

**Monitor a machine:**
```
12 → Bandwidth Monitor         # live RX/TX on chosen interface
10 → Connection Info           # see established connections
```

## Notes

- Log file is written to `~/.local/share/netdiag/` — not the working directory.
- Ctrl+C inside **Bandwidth Monitor** stops only the monitor; the menu remains open.
- Only scan hosts/networks you own or have explicit permission to test.

## Author

Created by @lexlucas

---

**Disclaimer**: Use responsibly and only on networks you own or have permission to test. Unauthorised scanning may be illegal in your jurisdiction.
