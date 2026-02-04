# Network tool Diagnostic

A comprehensive bash-based network diagnostic and troubleshooting tool with an interactive menu interface.

## Features

- **Network Interface Analysis**: View active interfaces, IP addresses, and statistics
- **Connectivity Testing**: Ping hosts with customizable packet counts
- **Port Scanning**: Basic port scanning using nmap (SYN scan as root, TCP connect as user)
- **Routing Information**: Display routing table, default gateway, and ARP cache
- **Path Tracing**: Traceroute to identify network path and latency
- **DNS Diagnostics**: DNS resolution and nameserver configuration
- **Speed Testing**: Simple download speed measurement
- **Connection Monitoring**: Active connections and network statistics
- **Logging**: Comprehensive logging of all operations

## Requirements

### Essential Tools

The script requires standard networking utilities typically found on Linux systems:

- `ip` (iproute2 package)
- `ping`
- `curl`

### Optional Tools (for full functionality)

- `nmap` - for port scanning (install with `sudo apt install nmap`)
- `traceroute` or `tracepath` - for path tracing
- `dig`, `nslookup`, or `host` - for DNS diagnostics
- `ss` - for socket statistics

## Installation

1. **Download the script:**

   ```bash
   curl -O https://raw.githubusercontent.com/yourusername/network-tool/main/network_diagnostic.sh
   ```

2. **Make it executable:**

   ```bash
   chmod +x network_diagnostic.sh
   ```

3. **Optional: Install missing dependencies:**

   ```bash
   # On Debian/Ubuntu
   sudo apt install nmap traceroute dnsutils iproute2 curl
   
   # On RHEL/CentOS
   sudo yum install nmap traceroute bind-utils iproute curl
   ```

## Usage

### Basic Usage

```bash
./network_diagnostic.sh
```

### Running with Elevated Privileges

Some features work better with root privileges:

```bash
sudo ./network_diagnostic.sh
```

**Note:** Running as root enables SYN scanning (-sS) in nmap for faster and more stealthy port scans.

## Menu Options

| Option | Function | Description | Defaults |
|--------|----------|-------------|----------|
| **1** | Check Network Interfaces | Displays all network interfaces, their states, MAC addresses, IP addresses, and traffic statistics | N/A |
| **2** | Ping Host | Test connectivity to a host with customizable packet count | Host: 8.8.8.8<br>Packets: 4 |
| **3** | Port Scan | Scan ports on a target host (SYN scan as root, TCP connect as user) | Host: localhost<br>Ports: 1-1000 |
| **4** | Display Routing Table | Shows routing table, default gateway, and ARP cache entries | N/A |
| **5** | Traceroute | Trace the network path to a destination | Host: 8.8.8.8<br>Max hops: 30 |
| **6** | Check DNS Resolution | Resolve domain names and display DNS server configuration | Domain: google.com |
| **7** | Speed Test | Perform a simple download speed test using public test files | Test file: 10MB |
| **8** | Connection Information | Show public IP address, network statistics, and active connections | N/A |
| **9** | View Log File | Display the last 20 entries from the log file | N/A |
| **10** | Exit | Exit the application | N/A |

## Logging

All operations are logged to `network_diagnostic.log` in the current directory with timestamps. The log includes:

- Tool startup and shutdown
- Each diagnostic operation performed
- Error messages and warnings
- Scan results and findings

## Temporary Files

The script creates a temporary directory in `/tmp/netdiag_$$` (where `$$` is the process ID) for any temporary files. This directory is automatically cleaned up on exit.

## Configuration

You can modify these variables at the top of the script:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_FILE` | `$(pwd)/network_diagnostic.log` | Log file location |
| `DEFAULT_PING_COUNT` | 4 | Default number of ping packets |
| `DEFAULT_NMAP_PORTS` | "1-1000" | Default port range for scanning |
| `TIMEOUT_SECONDS` | 10 | Timeout for various operations |

## Examples

### Quick Connectivity Check

```
1. Select option 1 to check interfaces
2. Select option 2 to ping Google DNS (8.8.8.8)
3. Select option 6 to verify DNS resolution
```

### Troubleshooting Network Issues

```
1. Check interfaces (option 1) - Verify IP configuration
2. Ping gateway (option 2) - Test local connectivity
3. Traceroute to external host (option 5) - Identify where connection fails
4. Check DNS (option 6) - Verify name resolution
```

### Security Audit

```
1. Scan localhost ports (option 3) - Check for open services
2. View active connections (option 8) - Monitor established connections
```

## Notes and Warnings

1. **Legal Considerations**: Only scan networks you own or have permission to test
2. **Port Scanning**: Some network administrators may consider port scanning hostile
3. **Resource Usage**: Intensive scans may impact network performance
4. **Root Access**: Running as root provides more accurate results but increases security risk
5. **Log Files**: Logs may contain sensitive network information - handle appropriately

## Troubleshooting

### Common Issues

1. **"Missing tools" error**: Install the required packages as shown in Requirements section
2. **Slow port scans**: Regular users use slower TCP connect scans; run as root for SYN scans
3. **Permission denied**: Some operations require root privileges
4. **Timeout errors**: Network may be blocking certain tests; try different hosts

### Error Messages

- **Ping failed or timed out**: Host unreachable or blocking ICMP
- **Scan failed**: Target may be filtering or firewalled
- **No DNS tool found**: Install dnsutils or bind-utils package

## Version History

- **Version 2.0**: Enhanced features, improved logging, better error handling
- **Version 1.0**: Initial release with basic functionality

## Author

Created by @lexlucas

## License

This tool is provided for educational and legitimate diagnostic purposes. Users are responsible for complying with all applicable laws and regulations.

---

**Disclaimer**: Use this tool responsibly and only on networks you own or have explicit permission to test. Unauthorized scanning or testing of networks may be illegal in your jurisdiction.
