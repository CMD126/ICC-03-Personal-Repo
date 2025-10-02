# Network Diagnostic Tool

This script is a comprehensive, menu-driven Bash utility designed to simplify common network diagnostics. It provides a single, easy-to-use interface for various command-line networking tools, making it ideal for quick network troubleshooting.

## Features

*   **Interactive Menu:** A clear and simple menu to access different diagnostic functions.
*   **Comprehensive Diagnostics:** Includes a variety of essential network tools:
    *   Network Interface Information (`ip addr`)
    *   Host Pinging (`ping`)
    *   Port Scanning (`nmap`)
    *   Routing Table Display (`ip route`)
    *   Traceroute (`traceroute`)
    *   DNS Resolution (`nslookup`)
*   **Prerequisite Checks:** The script automatically checks if necessary tools like `nmap` and `traceroute` are installed before attempting to use them.
*   **User-Friendly Output:** Parses the output of command-line tools to present the most relevant information in a clean and readable format.

## Prerequisites

This script relies on several standard networking utilities. Most are pre-installed on modern Linux systems. However, you may need to install `nmap` and `traceroute`.

You can install them on Debian-based systems (like Ubuntu) using the following command:

```bash
sudo apt-get update
sudo apt-get install nmap traceroute
```

## Usage

1.  **Navigate to the script directory:**
    ```bash
    cd "Scripts/Network tool"
    ```

2.  **Make the script executable:**
    ```bash
    chmod +x networktool.sh
    ```

3.  **Run the script:**
    ```bash
    ./networktool.sh
    ```
    *Note: The Nmap port scan option requires `sudo` privileges, so you may be prompted for your password when selecting it.*

## Menu Options

1.  **Check Network Interface Information:** Displays information about your network interfaces, including their status (UP/DOWN) and assigned IP addresses.
2.  **Ping a Host:** Sends ICMP packets to a specified host (domain name or IP address) to check for connectivity and measures packet loss and average round-trip time (RTT).
3.  **Port Scan with Nmap:** Performs a TCP SYN scan (`-sS`) on a given host to identify open TCP ports.
4.  **Display Routing Table:** Shows the system's routing table, including the default gateway and other routes.
5.  **Traceroute to Host:** Traces the network path to a specified host, showing the sequence of routers the packets pass through.
6.  **Check DNS Resolution:** Resolves a domain name to its corresponding IP address using `nslookup`.
7.  **Exit:** Terminates the script.