import subprocess
import socket
import time
import platform

# List of popular public DNS servers
DNS_SERVERS = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "Quad9": "9.9.9.9",
    "OpenDNS": "208.67.222.222",
    "CleanBrowsing": "185.228.168.9"
}

def ping_dns(dns_ip, count=3, timeout=1):
    # Tests connection latency to the DNS server using TCP on port 53
    times = []
    for _ in range(count):
        start = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((dns_ip, 53))
            elapsed = (time.time() - start) * 1000  # Time in ms
            times.append(elapsed)
            sock.close()
        except Exception:
            times.append(float('inf'))  # If it fails, record infinity
    avg_time = sum(times) / count
    return avg_time

def analyse_dns():
    # Analyzes all DNS servers and shows the average response time
    results = {}
    print("Analysing DNS servers...")
    for name, ip in DNS_SERVERS.items():
        avg_ping = ping_dns(ip)
        results[name] = (ip, avg_ping)
        print(f"{name} ({ip}): {avg_ping:.2f} ms")
    # Sort servers by response time
    sorted_dns = sorted(results.items(), key=lambda x: x[1][1])
    print("\nBest DNS servers by response time:")
    for i, (name, (ip, ping)) in enumerate(sorted_dns, 1):
        print(f"{i}. {name} ({ip}) - {ping:.2f} ms")
    return sorted_dns

def apply_dns(dns_ip):
    # Applies the chosen DNS for Windows, macOS, and Linux
    system = platform.system()
    print(f"Applying DNS: {dns_ip}")
    try:
        if system == "Linux":
            # Linux: edit /etc/resolv.conf
            resolv_conf = "/etc/resolv.conf"
            try:
                with open(resolv_conf, 'w') as f:
                    f.write(f"nameserver {dns_ip}\n")
                print("DNS applied successfully. You may need to reconnect your network.")
            except PermissionError:
                print("Permission denied. Please run this script with sudo/root privileges.")
        elif system == "Darwin":
            # macOS: use networksetup
            services = subprocess.check_output(
                ["networksetup", "-listallnetworkservices"],
                text=True
            ).splitlines()
            # Skip header lines and find first valid service
            for service in services:
                if service and not service.startswith("*"):
                    try:
                        subprocess.run(
                            ["networksetup", "-setdnsservers", service, dns_ip],
                            check=True
                        )
                        print(f"DNS applied successfully to {service}.")
                    except subprocess.CalledProcessError:
                        print(f"Failed to apply DNS to {service}.")
            print("You may need to reconnect your network.")
        elif system == "Windows":
            # Windows: use netsh
            interfaces = subprocess.check_output(
                'netsh interface show interface', shell=True, text=True
            ).splitlines()
            iface = None
            for line in interfaces:
                if "Connected" in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        iface = " ".join(parts[3:])
                        break
            if not iface:
                print("No connected network interface found.")
                return
            subprocess.run(
                f'netsh interface ip set dns name="{iface}" static {dns_ip}',
                shell=True, check=True
            )
            print("DNS applied successfully. You may need to reconnect your network.")
        else:
            print("Unsupported OS.")
    except PermissionError:
        print("Permission denied. Please run this script with administrator privileges to apply DNS.")
    except Exception as e:
        print(f"Failed to apply DNS: {e}")

def main():
    # Main function: analyzes, shows options, and applies the chosen DNS
    sorted_dns = analyse_dns()
    choice = input("\nEnter the number of the DNS server to apply (or 'q' to quit): ")
    if choice.lower() == 'q':
        print("Exiting.")
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(sorted_dns):
            dns_ip = sorted_dns[idx][1][0]
            apply_dns(dns_ip)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()