# ABDNS: Automatic Best DNS Selector

ABDNS benchmarks public DNS servers using **real UDP DNS queries** (not just pings) and applies the fastest one to your system. Works on Linux, macOS, and Windows.

## Features

- **Real DNS benchmarking** — sends actual A-record queries over UDP port 53 and measures round-trip time; no external dependencies required.
- **Packet loss reporting** — tracks timeouts per server and shows loss percentage alongside latency.
- **9 DNS providers** — Google, Cloudflare, Quad9, OpenDNS, AdGuard, NextDNS, CleanBrowsing, Comodo, Level3.
- **Primary + secondary DNS** — applies both addresses when configuring your system.
- **Cross-platform apply** — Linux (systemd-resolved via `resolvectl`, fallback to `/etc/resolv.conf`), macOS (`networksetup`), Windows (`netsh`).
- **CLI flags** — verbose output, custom test domains, direct apply by name, and server listing.

## Usage

```bash
python3 abdns.py [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-v`, `--verbose` | Show per-domain query times during benchmarking |
| `-d DOMAIN [...]` | Override the default test domains |
| `--apply NAME` | Apply a specific server by name without the interactive prompt |
| `--list` | List all available DNS servers and exit |

### Examples

```bash
# Interactive benchmark and apply
python3 abdns.py

# Verbose benchmark (shows every query result)
python3 abdns.py -v

# Benchmark against custom domains
python3 abdns.py -d example.com wikipedia.org

# Apply Cloudflare directly (no prompt)
python3 abdns.py --apply Cloudflare

# List available servers
python3 abdns.py --list
```

## Notes

- **Privileges required** to apply DNS settings: use `sudo` on Linux/macOS, run as Administrator on Windows.
- On Linux with systemd-resolved, settings are applied via `resolvectl` and take effect immediately. Without it, `/etc/resolv.conf` is written directly.
- On macOS, DNS is applied to every active network service returned by `networksetup`.
