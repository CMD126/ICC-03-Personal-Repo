# Subnet Calculator

Hands-on exercise for understanding IP addressing, CIDR notation, subnetting, and network ranges — core knowledge for network administration and security.

---

## What You Will Learn

- IPv4 address structure and classes (A, B, C, D, E)
- What CIDR notation means (`/24`, `/16`, etc.)
- How to calculate network address, broadcast address, and usable hosts
- The difference between private and public IP ranges
- How to divide a network into equal subnets

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | Subnet Information | Full breakdown: network/broadcast addresses, mask, wildcard, host range, total hosts |
| 2 | IP Class Identifier | Identifies class (A/B/C/D/E), default mask, type (private/public/loopback/multicast), binary representation |
| 3 | List IPs in CIDR Range | Enumerates all addresses in a range (limited to /24 or smaller) |
| 4 | Divide Network into Subnets | Splits a network into N equal subnets showing each range and host count |

---

## Usage

```bash
python3 subnet_calculator.py
```

No root required. No external packages needed.

---

## Requirements

| Module | Used for |
|--------|----------|
| `ipaddress` | IP network and address calculations (Python stdlib) |

---

## Example

```
[?] Network: 192.168.10.0/26

  Network Address   : 192.168.10.0
  Broadcast Address : 192.168.10.63
  Subnet Mask       : 255.255.255.192
  Wildcard Mask     : 0.0.0.63
  CIDR Notation     : 192.168.10.0/26
  Usable Hosts      : 62
  First Host        : 192.168.10.1
  Last Host         : 192.168.10.62
```
