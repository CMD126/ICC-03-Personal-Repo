#!/usr/bin/env python3
"""
Subnet Calculator — Educational Exercise
Demonstrates IP addressing concepts: subnetting, CIDR notation,
network/broadcast addresses, usable host ranges, and IP classes.
"""

import ipaddress
import sys

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║            SUBNET CALCULATOR — Educational                  ║
║   IP Addressing · CIDR · Subnetting · Network Ranges        ║
╚══════════════════════════════════════════════════════════════╝
"""

def subnet_info():
    """Full breakdown of a network given IP/CIDR or IP + subnet mask."""
    print("\n  Enter network in CIDR notation (e.g. 192.168.1.0/24)")
    print("  or IP with subnet mask (e.g. 192.168.1.0 255.255.255.0)\n")
    raw = input("[?] Network: ").strip()

    try:
        # Support 'IP MASK' format
        if " " in raw:
            parts = raw.split()
            ip, mask = parts[0], parts[1]
            net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
        else:
            net = ipaddress.IPv4Network(raw, strict=False)
    except ValueError as e:
        print(f"[!] Invalid input: {e}")
        return

    hosts = list(net.hosts())
    print(f"""
  ┌─────────────────────────────────────────────────────┐
  │  Network Information                                │
  └─────────────────────────────────────────────────────┘
  Network Address   : {net.network_address}
  Broadcast Address : {net.broadcast_address}
  Subnet Mask       : {net.netmask}
  Wildcard Mask     : {net.hostmask}
  CIDR Notation     : {net}
  Prefix Length     : /{net.prefixlen}
  Total Addresses   : {net.num_addresses}
  Usable Hosts      : {len(hosts)}
  First Host        : {hosts[0] if hosts else 'N/A'}
  Last Host         : {hosts[-1] if hosts else 'N/A'}
  IP Version        : IPv{net.version}
  Private Range     : {'Yes' if net.is_private else 'No'}""")

def ip_class_identifier():
    """Identify the class and type of an IPv4 address."""
    raw = input("\n[?] Enter an IPv4 address: ").strip()
    try:
        ip = ipaddress.IPv4Address(raw)
    except ValueError:
        print("[!] Invalid IPv4 address.")
        return

    first_octet = int(str(ip).split(".")[0])

    if first_octet < 128:
        cls, default_mask, hosts = "A", "255.0.0.0 (/8)", "16,777,214"
    elif first_octet < 192:
        cls, default_mask, hosts = "B", "255.255.0.0 (/16)", "65,534"
    elif first_octet < 224:
        cls, default_mask, hosts = "C", "255.255.255.0 (/24)", "254"
    elif first_octet < 240:
        cls, default_mask, hosts = "D (Multicast)", "N/A", "N/A"
    else:
        cls, default_mask, hosts = "E (Reserved)", "N/A", "N/A"

    addr_type = []
    if ip.is_private:     addr_type.append("Private")
    if ip.is_loopback:    addr_type.append("Loopback")
    if ip.is_multicast:   addr_type.append("Multicast")
    if ip.is_link_local:  addr_type.append("Link-local")
    if ip.is_global:      addr_type.append("Public/Global")
    if not addr_type:     addr_type.append("Unknown")

    print(f"""
  IP Address      : {ip}
  Class           : {cls}
  Default Mask    : {default_mask}
  Max Hosts       : {hosts}
  Type            : {', '.join(addr_type)}
  Binary          : {'.'.join(f'{int(o):08b}' for o in str(ip).split('.'))}""")

def cidr_range():
    """List all IP addresses in a CIDR range (limited to /24 or smaller)."""
    raw = input("\n[?] Enter CIDR (e.g. 10.0.0.0/28): ").strip()
    try:
        net = ipaddress.IPv4Network(raw, strict=False)
    except ValueError as e:
        print(f"[!] Invalid CIDR: {e}")
        return

    if net.prefixlen < 24:
        print(f"[!] Range too large (/{net.prefixlen}). Only /24 or smaller shown here.")
        print(f"  Network  : {net.network_address}")
        print(f"  Broadcast: {net.broadcast_address}")
        print(f"  Hosts    : {net.num_addresses - 2}")
        return

    print(f"\n  Addresses in {net}:\n")
    hosts = list(net.hosts())
    print(f"  Network   : {net.network_address}  (not assignable)")
    for i, host in enumerate(hosts):
        label = " ← first host" if i == 0 else " ← last host" if i == len(hosts)-1 else ""
        print(f"  Host      : {host}{label}")
    print(f"  Broadcast : {net.broadcast_address}  (not assignable)")
    print(f"\n  [+] {len(hosts)} usable host(s)")

def subnet_divider():
    """Divide a network into equal subnets."""
    raw = input("\n[?] Enter network to divide (e.g. 192.168.1.0/24): ").strip()
    try:
        net = ipaddress.IPv4Network(raw, strict=False)
    except ValueError as e:
        print(f"[!] Invalid network: {e}")
        return

    try:
        n = int(input("[?] How many equal subnets? (e.g. 4): ").strip())
        if n < 2:
            raise ValueError
    except ValueError:
        print("[!] Enter a number >= 2.")
        return

    try:
        subnets = list(net.subnets(new_prefix=None))
        # Find prefix needed
        import math
        bits_needed = math.ceil(math.log2(n))
        new_prefix = net.prefixlen + bits_needed
        if new_prefix > 30:
            print("[!] Not enough address space to divide further.")
            return
        subnets = list(net.subnets(new_prefix=new_prefix))[:n]
    except Exception as e:
        print(f"[!] Cannot divide: {e}")
        return

    print(f"\n  Dividing {net} into {len(subnets)} subnets (/{new_prefix}):\n")
    print(f"  {'#':<4} {'Network':<20} {'First Host':<16} {'Last Host':<16} {'Broadcast':<16} {'Hosts'}")
    print(f"  {'─'*3} {'─'*19} {'─'*15} {'─'*15} {'─'*15} {'─'*5}")
    for i, sub in enumerate(subnets, 1):
        hosts = list(sub.hosts())
        first = str(hosts[0]) if hosts else "N/A"
        last  = str(hosts[-1]) if hosts else "N/A"
        print(f"  {i:<4} {str(sub):<20} {first:<16} {last:<16} {str(sub.broadcast_address):<16} {len(hosts)}")

def main():
    print(BANNER)
    while True:
        print("  Options:")
        print("  1. Subnet information (network, broadcast, host range)")
        print("  2. IP address class identifier")
        print("  3. List all IPs in a CIDR range")
        print("  4. Divide a network into equal subnets")
        print("  0. Exit\n")
        choice = input("[?] Select option: ").strip()
        print()
        if   choice == "1": subnet_info()
        elif choice == "2": ip_class_identifier()
        elif choice == "3": cidr_range()
        elif choice == "4": subnet_divider()
        elif choice == "0": print("[+] Goodbye.\n"); sys.exit(0)
        else: print("[!] Invalid option.")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted.\n")
        sys.exit(0)
