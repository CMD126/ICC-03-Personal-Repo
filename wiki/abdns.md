# abdns

Python tool that benchmarks public DNS providers and optionally applies the fastest one as your system DNS.

---

## Features

- Benchmarks 9 popular DNS providers using real UDP queries
- Reports response time, packet loss, and jitter per provider
- Ranks providers by speed
- Applies the fastest primary + secondary DNS on Linux, macOS, or Windows
- No external dependencies — pure Python stdlib

### DNS Providers Tested

| Provider | Primary | Secondary |
|----------|---------|-----------|
| Cloudflare | 1.1.1.1 | 1.0.0.1 |
| Google | 8.8.8.8 | 8.8.4.4 |
| Quad9 | 9.9.9.9 | 149.112.112.112 |
| OpenDNS | 208.67.222.222 | 208.67.220.220 |
| AdGuard | 94.140.14.14 | 94.140.15.15 |
| Comodo | 8.26.56.26 | 8.20.247.20 |
| NextDNS | 45.90.28.0 | 45.90.30.0 |
| Level3 | 4.2.2.1 | 4.2.2.2 |
| Verisign | 64.6.64.6 | 64.6.65.6 |

---

## Usage

```bash
python3 abdns_dns_benchmark.py [options]

# Benchmark only (no changes):
python3 abdns_dns_benchmark.py --benchmark

# Benchmark and apply fastest DNS (requires root/admin):
sudo python3 abdns_dns_benchmark.py --apply
```

---

## Requirements

| Tool | Used for |
|------|----------|
| `python3` | Required |
| Root/admin | Required only to apply DNS changes |

---

→ [View source](../Scripts/abdns/) | [← Home](Home)
