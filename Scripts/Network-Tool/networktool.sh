#!/bin/bash
# Enhanced Network Diagnostic Tool
# Version: 2.0

# Configuration
LOG_FILE="$(pwd)/network_diagnostic.log"
TEMP_DIR="/tmp/netdiag_$$"
DEFAULT_PING_COUNT=4
DEFAULT_NMAP_PORTS="1-1000"
TIMEOUT_SECONDS=10

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Setup and cleanup
setup_environment() {
    mkdir -p "$TEMP_DIR"
    trap cleanup EXIT INT TERM
}

cleanup() {
    rm -rf "$TEMP_DIR"
    echo -e "\n${GREEN}Cleaning up temporary files...${NC}"
}

# Logging function
log_action() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" >> "$LOG_FILE"
    echo -e "${BLUE}[LOG]${NC} $1"
}

# Error handling
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    log_action "ERROR: $1"
    read -p "Press Enter to continue..."
    return 1
}

# Check for required tools
check_dependencies() {
    local missing_tools=()
    
    for tool in "$@"; do
        if ! command -v "$tool" >/dev/null 2>&1; then
            missing_tools+=("$tool")
        fi
    done
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        error_exit "Missing tools: ${missing_tools[*]}"
        return 1
    fi
    return 0
}

# Menu functions
show_interfaces() {
    echo -e "\n${GREEN}=== Network Interfaces ===${NC}\n"
    
    echo -e "${YELLOW}Active Interfaces:${NC}"
    ip -color addr show | grep -E '^[0-9]+:' | while read -r line; do
        iface=$(echo "$line" | awk '{print $2}' | tr -d ':')
        state=$(echo "$line" | grep -oE '(UP|DOWN)')
        mac=$(ip link show "$iface" 2>/dev/null | grep -oE 'link/ether [0-9a-f:]+' | cut -d' ' -f2)
        echo -e "Interface: $iface | State: $state | MAC: ${mac:-N/A}"
    done
    
    echo -e "\n${YELLOW}IP Addresses:${NC}"
    ip -color addr show | grep -E 'inet[6]?' | while read -r line; do
        iface=$(echo "$line" | awk '{print $NF}')
        ip_info=$(echo "$line" | awk '{print $2}')
        ip_type=$(echo "$line" | awk '{print $1}')
        echo -e "$ip_type: $ip_info on $iface"
    done
    
    echo -e "\n${YELLOW}Interface Statistics:${NC}"
    ip -s link show | grep -A1 -E '^[0-9]+:' | grep -E '^(RX|TX|[0-9]+:)'
}

ping_host() {
    read -p "Enter host to ping (default: 8.8.8.8): " host
    host=${host:-8.8.8.8}
    
    read -p "Number of packets (default: $DEFAULT_PING_COUNT): " count
    count=${count:-$DEFAULT_PING_COUNT}
    
    if ! check_dependencies "ping"; then
        return
    fi
    
    log_action "Pinging $host with $count packets"
    
    if timeout $TIMEOUT_SECONDS ping -c "$count" -i 0.2 -W 1 "$host" 2>/dev/null; then
        echo -e "\n${GREEN}Ping successful${NC}"
    else
        error_exit "Ping failed or timed out"
    fi
}

port_scan() {
    read -p "Enter host to scan (default: localhost): " host
    host=${host:-localhost}
    
    read -p "Port range (default: $DEFAULT_NMAP_PORTS): " ports
    ports=${ports:-$DEFAULT_NMAP_PORTS}
    
    if ! check_dependencies "nmap"; then
        echo "Install nmap with: sudo apt install nmap"
        return
    fi
    
    log_action "Scanning $host ports $ports"
    
    echo -e "\n${YELLOW}Scanning $host...${NC}"
    
    # Check if we need sudo for SYN scan
    if [[ $EUID -eq 0 ]]; then
        SCAN_TYPE="-sS"
    else
        SCAN_TYPE="-sT"
        echo -e "${YELLOW}Running TCP connect scan (non-root)${NC}"
    fi
    
    if nmap $SCAN_TYPE -p "$ports" --open --max-retries 1 --host-timeout 30s "$host" 2>/dev/null; then
        echo -e "\n${GREEN}Scan completed${NC}"
    else
        error_exit "Scan failed"
    fi
}

show_routing() {
    echo -e "\n${GREEN}=== Routing Table ===${NC}\n"
    
    echo -e "${YELLOW}Default Gateway:${NC}"
    ip route show default 2>/dev/null | head -1
    
    echo -e "\n${YELLOW}All Routes:${NC}"
    ip -color route show | while read -r route; do
        echo "$route"
    done
    
    echo -e "\n${YELLOW}ARP Table:${NC}"
    ip neigh show | head -20
}

trace_route() {
    read -p "Enter host for traceroute (default: 8.8.8.8): " host
    host=${host:-8.8.8.8}
    
    if ! check_dependencies "traceroute"; then
        echo "Install traceroute with: sudo apt install traceroute"
        return
    fi
    
    log_action "Traceroute to $host"
    
    echo -e "\n${YELLOW}Traceroute to $host (max 30 hops):${NC}"
    
    # Use different options based on available commands
    if command -v traceroute >/dev/null 2>&1; then
        traceroute -m 30 -w 1 -q 1 "$host" 2>/dev/null || error_exit "Traceroute failed"
    elif command -v tracepath >/dev/null 2>&1; then
        tracepath "$host" 2>/dev/null || error_exit "Tracepath failed"
    else
        error_exit "No traceroute tool found"
    fi
}

check_dns() {
    read -p "Enter domain to resolve (default: google.com): " domain
    domain=${domain:-google.com}
    
    echo -e "\n${YELLOW}DNS Resolution for $domain:${NC}"
    
    # Try dig first, then nslookup, then host
    if command -v dig >/dev/null 2>&1; then
        echo -e "\n${BLUE}Using dig:${NC}"
        dig +short "$domain" A "$domain" AAAA | while read -r result; do
            echo "  $result"
        done
        
        # Get nameservers
        echo -e "\n${BLUE}Nameservers:${NC}"
        dig +short NS "$domain" 2>/dev/null || echo "  Could not retrieve nameservers"
    elif command -v nslookup >/dev/null 2>&1; then
        echo -e "\n${BLUE}Using nslookup:${NC}"
        nslookup "$domain" 2>/dev/null | grep -A5 "Answer:" || nslookup "$domain" 2>/dev/null
    elif command -v host >/dev/null 2>&1; then
        echo -e "\n${BLUE}Using host:${NC}"
        host "$domain" 2>/dev/null
    else
        error_exit "No DNS lookup tool found"
        return
    fi
    
    # Check DNS server
    echo -e "\n${BLUE}Current DNS Servers:${NC}"
    cat /etc/resolv.conf | grep -E '^nameserver' | cut -d' ' -f2
}

speed_test() {
    echo -e "\n${YELLOW}Running speed test...${NC}"
    log_action "Running speed test"
    
    if ! check_dependencies "curl"; then
        return
    fi
    
    # Simple speed test using curl
    echo -e "${BLUE}Download test (10MB file):${NC}"
    
    # Try different speed test endpoints
    endpoints=(
        "http://speedtest.ftp.otenet.gr/files/test10Mb.db"
        "http://ipv4.download.thinkbroadband.com/10MB.zip"
    )
    
    for url in "${endpoints[@]}"; do
        echo -e "\nTesting with $url"
        if curl -o /dev/null -w "Speed: %{speed_download} bytes/sec\n" -s "$url"; then
            break
        fi
    done
}

connection_info() {
    echo -e "\n${GREEN}=== Connection Information ===${NC}\n"
    
    # Public IP
    echo -e "${YELLOW}Public IP Address:${NC}"
    curl -s --max-time 3 https://api.ipify.org || echo "Could not determine public IP"
    
    # Network statistics
    echo -e "\n${YELLOW}Network Statistics:${NC}"
    ss -s | head -10
    
    # Active connections
    echo -e "\n${YELLOW}Top Active Connections:${NC}"
    ss -tupn state established | head -20
}

# Main menu
show_menu() {
    clear
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════╗"
    echo "║     NETWORK TOOL BY @lexlucas         ║"
    echo "║           Version 2.0                 ║"
    echo "╚═══════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "\nSelect an option:\n"
    echo "1)  Check Network Interfaces"
    echo "2)  Ping Host"
    echo "3)  Port Scan"
    echo "4)  Display Routing Table"
    echo "5)  Traceroute"
    echo "6)  Check DNS Resolution"
    echo "7)  Speed Test"
    echo "8)  Connection Information"
    echo "9)  View Log File"
    echo "10) Exit"
    echo -e "\n"
}

# Main execution
main() {
    setup_environment
    
    while true; do
        show_menu
        read -p "Enter choice (1-10): " choice
        
        case $choice in
            1) show_interfaces ;;
            2) ping_host ;;
            3) port_scan ;;
            4) show_routing ;;
            5) trace_route ;;
            6) check_dns ;;
            7) speed_test ;;
            8) connection_info ;;
            9)
                echo -e "\n${YELLOW}Last 20 log entries:${NC}"
                tail -20 "$LOG_FILE" 2>/dev/null || echo "No log file found"
                ;;
            10)
                echo -e "\n${GREEN}Exiting...${NC}"
                log_action "Tool exited"
                exit 0
                ;;
            *)
                error_exit "Invalid option"
                continue
                ;;
        esac
        
        echo -e "\n${BLUE}----------------------------------------${NC}"
        read -p "Press Enter to continue..."
    done
}


main