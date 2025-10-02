#!/bin/bash
# Shebang to specify this is a Bash script
#!/bin/bash
# Shebang to specify Bash script

# Function for enhanced Matrix-style animation
matrix_effect() {
    clear
    echo -e "\033[32m"  # Set green text
    chars=("0" "1" "a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" "n")
    lines=$(tput lines)   # Get terminal height
    cols=$(tput cols)     # Get terminal width
    declare -A grid       # Array to track character positions
    for ((i=0; i<cols; i++)); do
        grid[$i]=$((RANDOM % lines))  # Random starting position for each column
    done
    for ((frame=0; frame<30; frame++)); do
        clear
        for ((row=0; row<lines; row++)); do
            for ((col=0; col<cols; col++)); do
                pos=${grid[$col]}
                if ((row == pos)); then
                    printf "${chars[$((RANDOM % 16))]}"  # Print random character
                    grid[$col]=$(( (pos + 1) % lines ))  # Move down
                elif ((row > pos && row < pos + (RANDOM % 5 + 3))); then
                    printf "${chars[$((RANDOM % 16))]}"  # Trail effect
                else
                    printf " "  # Empty space
                fi
            done
            echo
        done
        sleep 0.1  # Slower for smoother animation
    done
    echo -e "\033[0m"  # Reset color
    sleep 0.5
    clear
}

# Check if nmap is installed
if ! command -v nmap >/dev/null; then
    echo "Error: nmap not installed. Install with 'sudo apt install nmap'"
    exit 1
fi

while true; do
    matrix_effect  # Display enhanced Matrix effect
    # Display menu with Matrix-style header
    echo -e "\033[32m=== Matrix Nmap Scanner ===\033[0m"
    echo "1) Quick TCP Scan"
    echo "2) Detailed TCP Scan"
    echo "3) UDP Scan"
    echo "4) Ping Scan"
    echo "5) Exit"
    echo -e "\n"
    read -p "Select an option (1-5): " choice

    case $choice in
        1)
            # Quick TCP scan (-sS, top 100 ports)
            read -p "Enter host to scan (e.g., 192.168.1.1): " host
            if [[ -z "$host" ]]; then
                echo "Error: Host cannot be empty"; sleep 2; continue
            fi
            echo -e "\nScanning $host (Quick TCP)..."
            if nmap_result=$(sudo nmap -sS --top-ports 100 "$host" 2>/dev/null); then
                open_ports=$(echo "$nmap_result" | grep -oP '^\d+/tcp.*open' | awk '{print $1}')
                if [[ -n "$open_ports" ]]; then
                    echo "Open TCP Ports:"
                    echo "$open_ports"
                else
                    echo "No open TCP ports found"
                fi
            else
                echo "Error: Scan failed. Check host or permissions"; sleep 2
            fi
            ;;
        2)
            # Detailed TCP scan (-sS, all ports, version detection)
            read -p "Enter host to scan (e.g., 192.168.1.1): " host
            if [[ -z "$host" ]]; then
                echo "Error: Host cannot be empty"; sleep 2; continue
            fi
            echo -e "\nScanning $host (Detailed TCP)..."
            if nmap_result=$(sudo nmap -sS -p- -sV "$host" 2>/dev/null); then
                open_ports=$(echo "$nmap_result" | grep -oP '^\d+/tcp.*open' | awk '{print $1, $3}')
                if [[ -n "$open_ports" ]]; then
                    echo "Open TCP Ports (with services):"
                    echo "$open_ports"
                else
                    echo "No open TCP ports found"
                fi
            else
                echo "Error: Scan failed. Check host or permissions"; sleep 2
            fi
            ;;
        3)
            # UDP scan (-sU, top 100 ports)
            read -p "Enter host to scan (e.g., 192.168.1.1): " host
            if [[ -z "$host" ]]; then
                echo "Error: Host cannot be empty"; sleep 2; continue
            fi
            echo -e "\nScanning $host (UDP)..."
            if nmap_result=$(sudo nmap -sU --top-ports 100 "$host" 2>/dev/null); then
                open_ports=$(echo "$nmap_result" | grep -oP '^\d+/udp.*open' | awk '{print $1}')
                if [[ -n "$open_ports" ]]; then
                    echo "Open UDP Ports:"
                    echo "$open_ports"
                else
                    echo "No open UDP ports found"
                fi
            else
                echo "Error: Scan failed. Check host or permissions"; sleep 2
            fi
            ;;
        4)
            # Ping scan (-sn, no port scan)
            read -p "Enter network to scan (e.g., 192.168.1.0/24): " network
            if [[ -z "$network" ]]; then
                echo "Error: Network cannot be empty"; sleep 2; continue
            fi
            echo -e "\nScanning $network (Ping Scan)..."
            if nmap_result=$(nmap -sn "$network" 2>/dev/null); then
                hosts=$(echo "$nmap_result" | grep -oP 'Nmap scan report for \K.*' | awk '{print $1}')
                if [[ -n "$hosts" ]]; then
                    echo "Live Hosts:"
                    echo "$hosts"
                else
                    echo "No live hosts found"
                fi
            else
                echo "Error: Scan failed. Check network or permissions"; sleep 2
            fi
            ;;
        5)
            # Exit script
            echo -e "\033[32mExiting Matrix Scanner...\033[0m"
            exit 0
            ;;
        *)
            # Handle invalid input
            echo "Invalid option. Please select 1-5."; sleep 2
            ;;
    esac
    read -p "Press Enter to continue..."
done