#!/usr/bin/env python3
"""
Port Scanner - TCP Connect Scanner
ICC-03 Cybersecurity Program | Module 8: Penetration Testing

DISCLAIMER: Only use on systems you own or have explicit written
authorization to test. Unauthorized port scanning may be illegal
in your jurisdiction.

Demonstrates:
- TCP connect scanning using Python sockets
- Common port identification and service mapping
- Banner grabbing from open services
- Multithreading for scan performance
"""

import concurrent.futures
import socket
import time

BANNER = """
╔═══════════════════════════════════════════╗
║           PORT SCANNER v1.0               ║
║          TCP Connect Scanner              ║
║   [!] Authorized Systems Only             ║
╚═══════════════════════════════════════════╝
"""

TIMEOUT = 1.0

# Map of well-known ports to service names
COMMON_PORTS = {
    21:    "FTP",
    22:    "SSH",
    23:    "Telnet",
    25:    "SMTP",
    53:    "DNS",
    80:    "HTTP",
    110:   "POP3",
    135:   "MS-RPC",
    139:   "NetBIOS",
    143:   "IMAP",
    443:   "HTTPS",
    445:   "SMB",
    3306:  "MySQL",
    3389:  "RDP",
    5432:  "PostgreSQL",
    5900:  "VNC",
    6379:  "Redis",
    8080:  "HTTP-Alt",
    8443:  "HTTPS-Alt",
    27017: "MongoDB",
}


def resolve_host(target: str) -> str | None:
    """Resolve a hostname to an IP address."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"\n  [!] Could not resolve host: {target}")
        return None


def grab_banner(host: str, port: int) -> str:
    """
    Read a service banner from an open port.

    Many services (SSH, FTP, SMTP, MySQL...) greet the client first, so the
    scanner listens before sending anything. Only if the service stays quiet
    does it send a minimal HTTP request, which most web servers answer.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((host, port))
            s.settimeout(TIMEOUT / 2)  # short wait for a greeting
            try:
                data = s.recv(256)
            except TimeoutError:
                data = b""
            s.settimeout(TIMEOUT)
            if not data:
                s.sendall(f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
                data = s.recv(256)
    except OSError:
        return ""
    banner = data.decode(errors="ignore").strip()
    return banner.splitlines()[0][:70] if banner else ""


def parse_port_range(start: str, end: str) -> list:
    """Turn user input into a list of ports. Raises ValueError if invalid."""
    start_port, end_port = int(start), int(end)
    if not 1 <= start_port <= end_port <= 65535:
        raise ValueError("ports must satisfy 1 <= start <= end <= 65535")
    return list(range(start_port, end_port + 1))


def scan_port(host: str, port: int) -> dict | None:
    """
    Attempt a TCP connection to a single port.
    Returns a result dict if the port is open, None if closed/filtered.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            result = s.connect_ex((host, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                return {"port": port, "service": service}
    except OSError:
        pass
    return None


def scan_host(host: str, ports: list, max_threads: int = 100) -> list:
    """Scan a list of ports concurrently using a thread pool."""
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, host, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return sorted(open_ports, key=lambda x: x["port"])


def print_results(target: str, ip: str, open_ports: list, elapsed: float, grab_banners: bool):
    print(f"\n  {'=' * 58}")
    print("  Scan Results")
    print(f"  Target    : {target}  ({ip})")
    print(f"  Scan time : {elapsed:.2f}s")
    print(f"  {'=' * 58}")

    if not open_ports:
        print("\n  No open ports found.\n")
        return

    print(f"\n  {'PORT':<8} {'SERVICE':<16} {'BANNER' if grab_banners else ''}")
    print(f"  {'─' * 55}")

    for p in open_ports:
        banner = ""
        if grab_banners:
            banner = grab_banner(ip, p["port"])
        print(f"  {p['port']:<8} {p['service']:<16} {banner}")

    print(f"\n  {len(open_ports)} open port(s) found.")
    print(f"  {'=' * 58}\n")


def main():
    print(BANNER)
    print("  [!] Only scan systems you own or have explicit authorization to test.\n")

    target = input("  Enter target (IP or hostname): ").strip()
    if not target:
        print("  [!] No target specified.")
        return

    ip = resolve_host(target)
    if not ip:
        return

    if ip != target:
        print(f"  [*] Resolved: {target} -> {ip}")

    print()
    print("  Scan type:")
    print("  1) Common ports (top 20 well-known ports)")
    print("  2) Full scan    (ports 1–1024)")
    print("  3) Custom range")
    scan_choice = input("\n  Select: ").strip()

    if scan_choice == "1":
        ports = list(COMMON_PORTS.keys())
    elif scan_choice == "2":
        ports = list(range(1, 1025))
    elif scan_choice == "3":
        try:
            ports = parse_port_range(input("  Start port: ").strip(), input("  End port  : ").strip())
        except ValueError:
            print("  [!] Invalid port range (integers, 1-65535, start <= end).")
            return
    else:
        print("  [!] Invalid option.")
        return

    grab = input("\n  Attempt banner grabbing on open ports? (y/n): ").strip().lower() == "y"

    print(f"\n  [*] Scanning {ip} — {len(ports)} port(s) ...\n")
    start_time = time.time()
    open_ports = scan_host(ip, ports)
    elapsed    = time.time() - start_time

    print_results(target, ip, open_ports, elapsed, grab)


if __name__ == "__main__":
    main()
