import argparse
import platform
import random
import socket
import struct
import subprocess
import time

# ---------------------------------------------------------------------------
# DNS server registry — (primary, secondary)
# ---------------------------------------------------------------------------
DNS_SERVERS = {
    "Google":        ("8.8.8.8",         "8.8.4.4"),
    "Cloudflare":    ("1.1.1.1",         "1.0.0.1"),
    "Quad9":         ("9.9.9.9",         "149.112.112.112"),
    "OpenDNS":       ("208.67.222.222",  "208.67.220.220"),
    "AdGuard":       ("94.140.14.14",    "94.140.15.15"),
    "NextDNS":       ("45.90.28.0",      "45.90.30.0"),
    "CleanBrowsing": ("185.228.168.9",   "185.228.169.9"),
    "Comodo":        ("8.26.56.26",      "8.20.247.20"),
    "Level3":        ("209.244.0.3",     "209.244.0.4"),
}

# Domains used for resolution benchmarking
DEFAULT_DOMAINS = [
    "google.com",
    "cloudflare.com",
    "github.com",
    "microsoft.com",
    "amazon.com",
]

# ---------------------------------------------------------------------------
# Real DNS query over UDP (no external dependencies)
# ---------------------------------------------------------------------------

def _build_query(domain: str) -> bytes:
    """Build a minimal DNS A-record query packet."""
    txid = random.randint(0, 65535)
    flags = 0x0100          # QR=0 (query), RD=1 (recursion desired)
    header = struct.pack(">HHHHHH", txid, flags, 1, 0, 0, 0)

    qname = b""
    for label in domain.rstrip(".").split("."):
        encoded = label.encode()
        qname += bytes([len(encoded)]) + encoded
    qname += b"\x00"

    question = qname + struct.pack(">HH", 1, 1)  # QTYPE=A, QCLASS=IN
    return header + question


def query_dns(server_ip: str, domain: str, timeout: float = 2.0) -> float:
    """
    Send a real DNS query to *server_ip* and return the round-trip time in ms.
    Returns float('inf') on timeout or error.
    """
    packet = _build_query(domain)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        start = time.perf_counter()
        sock.sendto(packet, (server_ip, 53))
        data, _ = sock.recvfrom(512)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Sanity-check: response code must be NOERROR (0) or NXDOMAIN (3)
        rcode = struct.unpack(">H", data[2:4])[0] & 0x000F
        if rcode not in (0, 3):
            return float("inf")
        return elapsed_ms
    except Exception:
        return float("inf")
    finally:
        sock.close()


def benchmark_server(
    server_ip: str,
    domains: list[str],
    count: int = 3,
    verbose: bool = False,
) -> tuple[float, float]:
    """
    Benchmark *server_ip* by querying each domain *count* times.
    Returns (average_ms, packet_loss_percent).
    """
    times: list[float] = []
    for domain in domains:
        for _ in range(count):
            t = query_dns(server_ip, domain)
            times.append(t)
            if verbose:
                result = f"{t:.1f} ms" if t != float("inf") else "TIMEOUT"
                print(f"      {domain}: {result}")

    valid = [t for t in times if t != float("inf")]
    if not valid:
        return float("inf"), 100.0
    avg = sum(valid) / len(valid)
    loss = (len(times) - len(valid)) / len(times) * 100.0
    return avg, loss


# ---------------------------------------------------------------------------
# Benchmark all servers
# ---------------------------------------------------------------------------

def analyse_dns(
    domains: list[str] = DEFAULT_DOMAINS,
    verbose: bool = False,
) -> list[tuple]:
    """
    Benchmark all DNS servers, print results, and return a list sorted by
    average response time: [(name, primary, secondary, avg_ms, loss_pct), ...]
    """
    print(f"Benchmarking {len(DNS_SERVERS)} DNS servers "
          f"({len(domains)} domains × 3 queries each)...\n")

    results = []
    for name, (primary, secondary) in DNS_SERVERS.items():
        if verbose:
            print(f"  {name} ({primary})")
        avg, loss = benchmark_server(primary, domains, verbose=verbose)
        results.append((name, primary, secondary, avg, loss))
        status = f"{avg:.1f} ms" if avg != float("inf") else "UNREACHABLE"
        loss_str = f"  loss={loss:.0f}%" if loss > 0 else ""
        print(f"  {name:<15} {primary:<18} {status}{loss_str}")

    sorted_results = sorted(results, key=lambda x: x[3])
    print("\nRanked by average response time:")
    for i, (name, primary, secondary, avg, loss) in enumerate(sorted_results, 1):
        status = f"{avg:.1f} ms" if avg != float("inf") else "UNREACHABLE"
        loss_str = f"  (loss {loss:.0f}%)" if loss > 0 else ""
        print(f"  {i}. {name:<15} primary={primary}  {status}{loss_str}")

    return sorted_results


# ---------------------------------------------------------------------------
# DNS application — per-platform
# ---------------------------------------------------------------------------

def _apply_linux(primary: str, secondary: str | None) -> bool:
    # Prefer systemd-resolved via resolvectl
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "systemd-resolved"],
            capture_output=True, text=True,
        )
        if result.stdout.strip() == "active":
            # Detect the default-route interface
            route_out = subprocess.check_output(
                ["ip", "route", "show", "default"], text=True
            )
            tokens = route_out.split()
            if "dev" in tokens:
                iface = tokens[tokens.index("dev") + 1]
                dns_args = [primary] + ([secondary] if secondary else [])
                subprocess.run(
                    ["resolvectl", "dns", iface] + dns_args, check=True
                )
                print(f"DNS applied via systemd-resolved on interface '{iface}'.")
                return True
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        pass

    # Fallback: write /etc/resolv.conf directly
    try:
        lines = [f"nameserver {primary}\n"]
        if secondary:
            lines.append(f"nameserver {secondary}\n")
        with open("/etc/resolv.conf", "w") as f:
            f.writelines(lines)
        print("DNS applied to /etc/resolv.conf.")
        return True
    except PermissionError:
        print("Permission denied. Run with sudo.")
        return False


def _apply_macos(primary: str, secondary: str | None) -> bool:
    try:
        services_raw = subprocess.check_output(
            ["networksetup", "-listallnetworkservices"], text=True
        ).splitlines()
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"networksetup error: {e}")
        return False

    applied = False
    for service in services_raw:
        if not service or service.startswith("*") or service.lower().startswith("an asterisk"):
            continue
        dns_args = [primary] + ([secondary] if secondary else [])
        try:
            subprocess.run(
                ["networksetup", "-setdnsservers", service] + dns_args,
                check=True, capture_output=True,
            )
            print(f"DNS applied to service '{service}'.")
            applied = True
        except subprocess.CalledProcessError:
            pass

    if not applied:
        print("No writable network services found.")
    return applied


def _get_windows_interface() -> str | None:
    """Return the name of the first connected network interface on Windows."""
    try:
        out = subprocess.check_output(
            "netsh interface show interface",
            shell=True, text=True, stderr=subprocess.DEVNULL,
        )
        for line in out.splitlines():
            if "Connected" in line:
                parts = line.split()
                if len(parts) >= 4:
                    return " ".join(parts[3:])
    except subprocess.CalledProcessError:
        pass
    return None


def _apply_windows(primary: str, secondary: str | None) -> bool:
    iface = _get_windows_interface()
    if not iface:
        print("No connected network interface found.")
        return False
    try:
        subprocess.run(
            f'netsh interface ip set dns name="{iface}" static {primary}',
            shell=True, check=True,
        )
        if secondary:
            subprocess.run(
                f'netsh interface ip add dns name="{iface}" {secondary} index=2',
                shell=True, check=True,
            )
        print(f"DNS applied to interface '{iface}'.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"netsh error: {e}")
        return False


def apply_dns(primary: str, secondary: str | None = None) -> bool:
    """Apply DNS settings for the current operating system."""
    system = platform.system()
    suffix = f", secondary={secondary}" if secondary else ""
    print(f"\nApplying DNS — primary={primary}{suffix}")
    try:
        if system == "Linux":
            return _apply_linux(primary, secondary)
        elif system == "Darwin":
            return _apply_macos(primary, secondary)
        elif system == "Windows":
            return _apply_windows(primary, secondary)
        else:
            print(f"Unsupported OS: {system}")
            return False
    except PermissionError:
        print("Permission denied. Run with administrator privileges.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="abdns",
        description="ABDNS — Automatic Best DNS Selector\n"
                    "Benchmarks public DNS servers using real UDP queries and applies the best one.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show per-domain query times during benchmarking",
    )
    parser.add_argument(
        "-d", "--domains",
        nargs="+",
        metavar="DOMAIN",
        default=DEFAULT_DOMAINS,
        help="Override the list of domains used for benchmarking",
    )
    parser.add_argument(
        "--apply",
        metavar="NAME",
        help="Apply a specific DNS server by name without interactive prompt (e.g. Cloudflare)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available DNS servers and exit",
    )
    args = parser.parse_args()

    if args.list:
        print("Available DNS servers:")
        for name, (primary, secondary) in DNS_SERVERS.items():
            print(f"  {name:<15} primary={primary}, secondary={secondary}")
        return

    sorted_results = analyse_dns(domains=args.domains, verbose=args.verbose)

    if args.apply:
        match = next(
            ((n, p, s) for n, p, s, *_ in sorted_results
             if n.lower() == args.apply.lower()),
            None,
        )
        if match:
            apply_dns(match[1], match[2])
        else:
            names = ", ".join(n for n, *_ in sorted_results)
            print(f"Unknown server '{args.apply}'. Available: {names}")
        return

    print()
    choice = input("Enter number to apply, or 'q' to quit: ").strip()
    if choice.lower() == "q":
        print("Exiting.")
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(sorted_results):
            name, primary, secondary, *_ = sorted_results[idx]
            apply_dns(primary, secondary)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")


if __name__ == "__main__":
    main()
