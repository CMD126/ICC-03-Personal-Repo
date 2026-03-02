# Port Scanner

**Module 8 — Penetration Testing**

> **Disclaimer:** Only use on systems you own or have explicit written authorization to test. Unauthorized port scanning may be illegal in your jurisdiction.

A Python TCP port scanner built from scratch using raw sockets and multithreading. Performs TCP connect scans, maps open ports to known services, and optionally grabs service banners — the same fundamentals behind tools like Nmap.

---

## Features

| Feature | Description |
|---------|-------------|
| TCP connect scan | Attempts a full TCP handshake to determine if a port is open |
| Service mapping | Identifies 20 common services by port number |
| Banner grabbing | Reads the first response from open ports to identify service versions |
| Multithreaded | Uses a thread pool for fast parallel scanning |
| Flexible targets | Accepts hostnames or IP addresses; resolves DNS automatically |
| Three scan modes | Common ports, full 1–1024 sweep, or custom range |

---

## Usage

```bash
python3 port_scanner.py
```

No external dependencies — uses only Python's built-in `socket`, `concurrent.futures`, and `time` modules.

---

## Example Output

```
  PORT     SERVICE          BANNER
  ───────────────────────────────────────────────────────
  22       SSH              SSH-2.0-OpenSSH_8.9p1 Ubuntu
  80       HTTP             HTTP/1.1 200 OK
  443      HTTPS
  3306     MySQL
```

---

## Scan Modes

| Mode | Ports scanned |
|------|--------------|
| Common ports | 20 well-known ports (SSH, HTTP, RDP, SMB, MySQL, etc.) |
| Full scan | All ports 1–1024 |
| Custom range | User-defined start and end port |

---

## Concepts Demonstrated

| Concept | Explanation |
|---------|-------------|
| **TCP Connect Scan** | Completes the full 3-way handshake — detectable but reliable |
| **Socket programming** | Direct use of Python `socket` for low-level network communication |
| **Service fingerprinting** | Matching port numbers to known services; reading banners for version info |
| **Multithreading** | `ThreadPoolExecutor` allows hundreds of ports to be probed concurrently |
| **Recon methodology** | Port scanning is the first active step in any penetration test (reconnaissance → enumeration) |

---

## Requirements

- Python 3.10+
- No external packages needed
