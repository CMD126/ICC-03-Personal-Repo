#!/bin/bash
#!/bin/bash
# Shebang to specify this is a Bash script

while true; do
    clear  # Clear terminal for a clean interface
    echo -e "\n=== Network Diagnostic Tool ===\n"  # Display tool title
    # Print menu options
    echo "1) Check Network Interface Information"
    echo "2) Ping a Host"
    echo "3) Port Scan with Nmap"
    echo "4) Display Routing Table"
    echo "5) Traceroute to Host"
    echo "6) Check DNS Resolution"
    echo "7) Exit"
    echo -e "\n"
    read -p "Select an option (1-7): " choice  # Prompt user for input

    case $choice in
        1)
            # Display network interface information
            echo -e "\nActive Network Interfaces:"
            # Parse 'ip addr' to show interface names and status (UP/DOWN)
            ip -color addr | grep -E '^[0-9]+:.*(UP|DOWN)' | awk '{print $2, $9}' | sed 's/://'
            # Extract and display IP addresses
            ip -color addr | grep inet | awk '{print $2}' | while read ip; do echo "IP: $ip"; done
            ;;
        2)
            # Ping a specified host
            read -p "Enter host to ping (e.g., google.com): " host  # Prompt for host
            if [[ -z "$host" ]]; then
                echo "Error: Host cannot be empty"; sleep 2; continue  # Check for empty input
            fi
            echo -e "\nPinging $host..."
            ping_result=$(ping -c 4 "$host" 2>/dev/null)  # Ping host 4 times, suppress errors
            if [[ $? -eq 0 ]]; then
                # Parse packet loss and average RTT from ping output
                packet_loss=$(echo "$ping_result" | grep -oP '\d+% packet loss' | awk '{print $1}')
                avg_rtt=$(echo "$ping_result" | grep -oP 'rtt min/avg/max/mdev = [\d\.]+/[\d\.]+' | awk -F'/' '{print $2}')
                echo "Packet Loss: $packet_loss"
                echo "Average RTT: ${avg_rtt}ms"
            else
                echo "Error: Ping failed"; sleep 2  # Handle ping failure
            fi
            ;;
        3)
            # Perform port scan with nmap
            read -p "Enter host to scan (e.g., 192.168.1.1): " host  # Prompt for host
            if [[ -z "$host" ]]; then
                echo "Error: Host cannot be empty"; sleep 2; continue  # Check for empty input
            fi
            if ! command -v nmap >/dev/null; then
                # Check if nmap is installed
                echo "Error: nmap not installed. Install with 'sudo apt install nmap'"; sleep 2; continue
            fi
            echo -e "\nScanning $host with nmap..."
            nmap_result=$(sudo nmap -sS "$host" 2>/dev/null)  # Run SYN scan, requires sudo
            if [[ $? -eq 0 ]]; then
                # Parse open TCP ports from nmap output
                open_ports=$(echo "$nmap_result" | grep -oP '^\d+/tcp.*open' | awk '{print $1}')
                if [[ -n "$open_ports" ]]; then
                    echo "Open TCP Ports:"
                    echo "$open_ports"
                else
                    echo "No open TCP ports found"
                fi
            else
                echo "Error: Nmap scan failed"; sleep 2  # Handle nmap failure
            fi
            ;;
        4)
            # Display routing table
            echo -e "\nDefault Gateway and Routes:"
            # Show default gateway
            ip -color route | grep default | awk '{print "Gateway: "$3}'
            # Show other routes
            ip -color route | grep -v default | awk '{print "Route: "$1" via "$3}'
            ;;
        5)
            # Perform traceroute to a host
            read -p "Enter host for traceroute (e.g., google.com): " host  # Prompt for host
            if [[ -z "$host" ]]; then
                echo "Error: Host cannot be empty"; sleep 2; continue  # Check for empty input
            fi
            if ! command -v traceroute >/dev/null; then
                # Check if traceroute is installed
                echo "Error: traceroute not installed. Install with 'sudo apt install traceroute'"; sleep 2; continue
            fi
            if ! ping -c 1 "$host" >/dev/null 2>&1; then
                # Verify host is reachable
                echo "Error: Host $host is unreachable"; sleep 2; continue
            fi
            echo -e "\nTraceroute to $host..."
            traceroute_result=$(traceroute -m 10 "$host" 2>/dev/null)  # Run traceroute, max 10 hops
            if [[ $? -eq 0 ]]; then
                # Parse hop count and last hop
                hops=$(echo "$traceroute_result" | grep -E '^[ ]*[0-9]+' | wc -l)
                last_hop=$(echo "$traceroute_result" | grep -E '^[ ]*[0-9]+' | tail -1 | awk '{print $2}')
                echo "Hops: $hops"
                echo "Last Hop: $last_hop"
            else
                echo "Error: Traceroute failed. Check host or network"; sleep 2  # Handle traceroute failure
            fi
            ;;
        6)
            # Check DNS resolution
            read -p "Enter domain to resolve (e.g., google.com): " domain  # Prompt for domain
            if [[ -z "$domain" ]]; then
                echo "Error: Domain cannot be empty"; sleep 2; continue  # Check for empty input
            fi
            echo -e "\nDNS Resolution for $domain:"
            nslookup_result=$(nslookup "$domain" 2>/dev/null)  # Run nslookup
            if [[ $? -eq 0 ]]; then
                # Parse first resolved IP
                ip=$(echo "$nslookup_result" | grep -oP 'Address: \K[\d\.]+' | head -1)
                echo "Resolved IP: $ip"
            else
                echo "Error: DNS lookup failed"; sleep 2  # Handle nslookup failure
            fi
            ;;
        7)
            # Exit the script
            echo "Exiting..."
            exit 0
            ;;
        *)
            # Handle invalid menu options
            echo "Invalid option. Please select 1-7."; sleep 2
            ;;
    esac
    read -p "Press Enter to continue..."  # Pause to review output
done