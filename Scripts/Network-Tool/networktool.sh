#!/bin/bash
# Network Diagnostic Tool — Version 3.0
# Author: @lexlucas

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
LOG_FILE="${HOME}/.local/share/netdiag/network_diagnostic.log"
TEMP_DIR="/tmp/netdiag_$$"
DEFAULT_PING_COUNT=4
DEFAULT_NMAP_PORTS="1-1000"
TIMEOUT_SECONDS=10

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# Core utilities
# ---------------------------------------------------------------------------

setup_environment() {
    mkdir -p "$TEMP_DIR"
    mkdir -p "$(dirname "$LOG_FILE")"
    # Only clean up temp files on exit — no noisy message
    trap 'rm -rf "$TEMP_DIR"' EXIT
}

log_action() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" >> "$LOG_FILE"
    echo -e "${BLUE}[LOG]${NC} $1"
}

# Print error and return 1 — does NOT pause or exit the program
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    log_action "ERROR: $1"
    return 1
}

check_dependencies() {
    local missing=()
    for tool in "$@"; do
        command -v "$tool" >/dev/null 2>&1 || missing+=("$tool")
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}Missing tools: ${missing[*]}${NC}" >&2
        return 1
    fi
}

# ---------------------------------------------------------------------------
# 1. Network Interfaces
# ---------------------------------------------------------------------------

show_interfaces() {
    echo -e "\n${GREEN}=== Network Interfaces ===${NC}\n"

    echo -e "${YELLOW}Interfaces & MAC addresses:${NC}"
    # Use 'ip addr show' without -color to avoid ANSI codes breaking awk
    ip addr show | awk '
        /^[0-9]+:/ {
            iface = $2; gsub(/:/, "", iface)
            state = ($0 ~ /UP/) ? "UP" : "DOWN"
        }
        /link\/ether/ {
            printf "  %-14s state=%-5s mac=%s\n", iface, state, $2
        }'

    echo -e "\n${YELLOW}IP Addresses:${NC}"
    ip addr show | awk '/inet/{
        printf "  %-6s %-22s %s\n", $1, $2, $NF
    }'

    echo -e "\n${YELLOW}Interface Statistics (from /proc/net/dev):${NC}"
    if [[ -f /proc/net/dev ]]; then
        awk 'NR>2 {
            gsub(/:/, "", $1)
            printf "  %-14s RX: %-16s TX: %s bytes\n", $1, $2, $10
        }' /proc/net/dev
    else
        ip -s link show | grep -E '(^[0-9]+:|RX:|TX:)' | sed 's/^/  /'
    fi
}

# ---------------------------------------------------------------------------
# 2. Ping Host
# ---------------------------------------------------------------------------

ping_host() {
    read -rp "Enter host to ping (default: 8.8.8.8): " host
    host=${host:-8.8.8.8}

    read -rp "Number of packets (default: $DEFAULT_PING_COUNT): " count
    count=${count:-$DEFAULT_PING_COUNT}

    log_action "Pinging $host with $count packets"

    if timeout "$TIMEOUT_SECONDS" ping -c "$count" -i 0.2 -W 2 "$host" 2>/dev/null; then
        echo -e "\n${GREEN}Ping successful${NC}"
    else
        error_exit "Ping to $host failed or timed out"
    fi
}

# ---------------------------------------------------------------------------
# 3. Latency Graph (NEW)
# ---------------------------------------------------------------------------

latency_graph() {
    read -rp "Enter host (default: 8.8.8.8): " host
    host=${host:-8.8.8.8}

    read -rp "Number of samples (default: 20): " samples
    samples=${samples:-20}

    echo -e "\n${YELLOW}Collecting $samples ping samples to $host...${NC}"
    log_action "Latency graph: $host ($samples samples)"

    local -a rtts
    local min_ms=999999 max_ms=0

    for ((i = 1; i <= samples; i++)); do
        rtt=$(ping -c 1 -W 2 "$host" 2>/dev/null \
              | grep -oE 'time=[0-9]+\.?[0-9]*' | cut -d= -f2)
        if [[ -z "$rtt" ]]; then
            rtts+=("T")
            echo -ne "${RED}x${NC}"
        else
            rtts+=("$rtt")
            rtt_int=${rtt%.*}
            (( rtt_int < min_ms )) && min_ms=$rtt_int
            (( rtt_int > max_ms )) && max_ms=$rtt_int
            echo -ne "."
        fi
    done
    echo -e "\n"

    local bar_width=40
    echo -e "${CYAN}=== Latency Graph (ms) ===${NC}"
    echo -e "  Scale: min=${min_ms}ms  max=${max_ms}ms\n"

    for i in "${!rtts[@]}"; do
        rtt="${rtts[$i]}"
        printf "  %3d │ " "$((i + 1))"
        if [[ "$rtt" == "T" ]]; then
            echo -e "${RED}TIMEOUT${NC}"
        else
            rtt_int=${rtt%.*}
            local range=$(( max_ms - min_ms + 1 ))
            (( range <= 0 )) && range=1
            local bar_len=$(( (rtt_int - min_ms + 1) * bar_width / range ))
            (( bar_len < 1 )) && bar_len=1
            local color=$GREEN
            (( rtt_int > 100 )) && color=$YELLOW
            (( rtt_int > 200 )) && color=$RED
            local bar
            bar=$(printf '%*s' "$bar_len" '' | tr ' ' '█')
            echo -e "${color}${bar}${NC} ${rtt} ms"
        fi
    done

    # Summary
    local valid=() sum=0 lost=0
    for rtt in "${rtts[@]}"; do
        if [[ "$rtt" == "T" ]]; then
            (( lost++ ))
        else
            valid+=("$rtt")
            sum=$(awk "BEGIN{print $sum + $rtt}")
        fi
    done

    echo -e "\n${YELLOW}Summary:${NC}"
    if [[ ${#valid[@]} -gt 0 ]]; then
        local avg
        avg=$(awk "BEGIN{printf \"%.2f\", $sum / ${#valid[@]}}")
        echo -e "  Min: ${min_ms} ms  Avg: ${avg} ms  Max: ${max_ms} ms"
    fi
    local loss_pct
    loss_pct=$(awk "BEGIN{printf \"%.1f\", $lost * 100 / $samples}")
    echo -e "  Sent: $samples  Lost: $lost  Loss: ${loss_pct}%"
}

# ---------------------------------------------------------------------------
# 4. Port Scan
# ---------------------------------------------------------------------------

port_scan() {
    read -rp "Enter host to scan (default: localhost): " host
    host=${host:-localhost}

    read -rp "Port range (default: $DEFAULT_NMAP_PORTS): " ports
    ports=${ports:-$DEFAULT_NMAP_PORTS}

    if ! check_dependencies "nmap"; then
        echo "Install with: sudo apt install nmap"
        return
    fi

    log_action "Port scan: $host ports $ports"
    echo -e "\n${YELLOW}Scanning $host (ports $ports)...${NC}"

    local scan_type="-sT"
    if [[ $EUID -eq 0 ]]; then
        scan_type="-sS"
    else
        echo -e "${YELLOW}Non-root: using TCP connect scan (-sT)${NC}"
    fi

    nmap $scan_type -p "$ports" --open --max-retries 1 \
        --host-timeout 30s -oG "$TEMP_DIR/scan.txt" "$host" 2>/dev/null

    echo -e "\n${GREEN}Open ports:${NC}"
    if grep -q "Ports:" "$TEMP_DIR/scan.txt" 2>/dev/null; then
        grep "Ports:" "$TEMP_DIR/scan.txt" \
        | grep -oE '[0-9]+/open/[a-z]+/[^,/]*' \
        | awk -F/ '{printf "  %-8s %-6s %s\n", $1, $2, $4}'
    else
        echo "  No open ports found."
    fi
    echo -e "\n${GREEN}Scan completed${NC}"
}

# ---------------------------------------------------------------------------
# 5. Routing Table
# ---------------------------------------------------------------------------

show_routing() {
    echo -e "\n${GREEN}=== Routing Table ===${NC}\n"

    echo -e "${YELLOW}Default Gateway:${NC}"
    ip route show default 2>/dev/null | sed 's/^/  /'

    echo -e "\n${YELLOW}All Routes:${NC}"
    ip route show | sed 's/^/  /'

    echo -e "\n${YELLOW}ARP / Neighbor Table:${NC}"
    ip neigh show | head -20 | sed 's/^/  /'
}

# ---------------------------------------------------------------------------
# 6. Traceroute
# ---------------------------------------------------------------------------

trace_route() {
    read -rp "Enter host for traceroute (default: 8.8.8.8): " host
    host=${host:-8.8.8.8}

    log_action "Traceroute to $host"
    echo -e "\n${YELLOW}Traceroute to $host (max 30 hops):${NC}"

    if command -v traceroute >/dev/null 2>&1; then
        traceroute -m 30 -w 2 -q 1 "$host" 2>/dev/null \
            || error_exit "traceroute to $host failed"
    elif command -v tracepath >/dev/null 2>&1; then
        tracepath "$host" 2>/dev/null \
            || error_exit "tracepath to $host failed"
    else
        error_exit "No traceroute tool. Install: sudo apt install traceroute"
    fi
}

# ---------------------------------------------------------------------------
# 7. DNS Resolution  (fixed dig syntax)
# ---------------------------------------------------------------------------

check_dns() {
    read -rp "Enter domain to resolve (default: google.com): " domain
    domain=${domain:-google.com}

    echo -e "\n${YELLOW}DNS Resolution for $domain:${NC}"
    log_action "DNS lookup: $domain"

    if command -v dig >/dev/null 2>&1; then
        echo -e "\n${BLUE}A records (IPv4):${NC}"
        dig +short A "$domain" 2>/dev/null | sed 's/^/  /' || echo "  None"

        echo -e "\n${BLUE}AAAA records (IPv6):${NC}"
        dig +short AAAA "$domain" 2>/dev/null | sed 's/^/  /' || echo "  None"

        echo -e "\n${BLUE}MX records (mail):${NC}"
        dig +short MX "$domain" 2>/dev/null | sort -n | sed 's/^/  /' || echo "  None"

        echo -e "\n${BLUE}Nameservers:${NC}"
        dig +short NS "$domain" 2>/dev/null | sed 's/^/  /' || echo "  None"

        echo -e "\n${BLUE}Query time:${NC}"
        dig A "$domain" 2>/dev/null | grep "Query time" | sed 's/^/  /'
    elif command -v nslookup >/dev/null 2>&1; then
        nslookup "$domain" 2>/dev/null
    elif command -v host >/dev/null 2>&1; then
        host "$domain" 2>/dev/null
    else
        error_exit "No DNS lookup tool found. Install: sudo apt install dnsutils"
        return
    fi

    echo -e "\n${BLUE}Active DNS servers:${NC}"
    grep -E '^nameserver' /etc/resolv.conf 2>/dev/null \
        | awk '{print "  "$2}' \
        || echo "  Could not read /etc/resolv.conf"
}

# ---------------------------------------------------------------------------
# 8. Speed Test  (fixed URLs + shows Mbps)
# ---------------------------------------------------------------------------

speed_test() {
    echo -e "\n${YELLOW}Running speed test...${NC}"
    log_action "Speed test"

    check_dependencies "curl" || return

    # Prefer dedicated CLI tools if available
    if command -v speedtest-cli >/dev/null 2>&1; then
        echo -e "${BLUE}Using speedtest-cli:${NC}"
        speedtest-cli --simple 2>/dev/null
        return
    fi
    if command -v speedtest >/dev/null 2>&1; then
        echo -e "${BLUE}Using speedtest:${NC}"
        speedtest 2>/dev/null
        return
    fi

    echo -e "${BLUE}Download test (10 MB):${NC}\n"
    local endpoints=(
        "https://speed.cloudflare.com/__down?bytes=10000000"
        "https://speedtest.tele2.net/10MB.zip"
        "https://proof.ovh.net/files/10Mb.dat"
    )

    local success=0
    for url in "${endpoints[@]}"; do
        local host
        host=$(echo "$url" | awk -F/ '{print $3}')
        echo -e "  Endpoint: ${CYAN}${host}${NC}"
        local result
        result=$(curl -o /dev/null \
            -w "%{speed_download} %{time_total}" \
            -s --max-time 20 --connect-timeout 5 "$url" 2>/dev/null)

        local bps time_s
        read -r bps time_s <<< "$result"

        if [[ -n "$bps" ]] && awk "BEGIN{exit !($bps > 0)}"; then
            local mbps
            mbps=$(awk "BEGIN{printf \"%.2f\", $bps * 8 / 1000000}")
            echo -e "  Speed:    ${GREEN}${mbps} Mbps${NC}  (${time_s}s)"
            success=1
            break
        else
            echo -e "  ${YELLOW}Skipping (no response)${NC}"
        fi
    done

    [[ $success -eq 0 ]] && error_exit "All speed test endpoints unreachable"
}

# ---------------------------------------------------------------------------
# 9. SSL Certificate Check (NEW)
# ---------------------------------------------------------------------------

ssl_check() {
    read -rp "Enter domain to inspect (default: google.com): " domain
    domain=${domain:-google.com}

    read -rp "Port (default: 443): " port
    port=${port:-443}

    check_dependencies "openssl" || return

    echo -e "\n${YELLOW}SSL/TLS certificate for ${domain}:${port}${NC}\n"
    log_action "SSL check: $domain:$port"

    local cert_info
    cert_info=$(echo | timeout 5 openssl s_client \
        -connect "${domain}:${port}" -servername "$domain" 2>/dev/null \
        | openssl x509 -noout -subject -issuer -dates -fingerprint 2>/dev/null)

    if [[ -z "$cert_info" ]]; then
        error_exit "Could not retrieve certificate from ${domain}:${port}"
        return
    fi

    while IFS= read -r line; do
        local key val
        key=$(echo "$line" | cut -d= -f1 | xargs)
        val=$(echo "$line" | cut -d= -f2- | xargs)
        case "$key" in
            subject)
                echo -e "  ${BLUE}Subject    :${NC} $val" ;;
            issuer)
                echo -e "  ${BLUE}Issuer     :${NC} $val" ;;
            notBefore)
                echo -e "  ${BLUE}Valid from :${NC} $val" ;;
            notAfter)
                # Calculate days remaining
                local exp_epoch now_epoch days_left color
                exp_epoch=$(date -d "$val" +%s 2>/dev/null \
                    || date -j -f "%b %d %H:%M:%S %Y %Z" "$val" +%s 2>/dev/null)
                now_epoch=$(date +%s)
                days_left=$(( (exp_epoch - now_epoch) / 86400 ))
                color=$GREEN
                (( days_left < 30 )) && color=$YELLOW
                (( days_left < 7  )) && color=$RED
                echo -e "  ${BLUE}Expires    :${NC} $val ${color}(${days_left} days left)${NC}"
                ;;
            "SHA1 Fingerprint")
                echo -e "  ${BLUE}SHA1       :${NC} $val" ;;
        esac
    done <<< "$cert_info"

    echo -e "\n  ${BLUE}TLS protocol & cipher:${NC}"
    echo | timeout 5 openssl s_client \
        -connect "${domain}:${port}" -servername "$domain" 2>/dev/null \
        | grep -E '^\s*(Protocol|Cipher)' | sed 's/^/    /'
}

# ---------------------------------------------------------------------------
# 10. Connection Info + Geolocation (enhanced)
# ---------------------------------------------------------------------------

connection_info() {
    echo -e "\n${GREEN}=== Connection Information ===${NC}\n"

    echo -e "${YELLOW}Public IP & Geolocation:${NC}"
    local geo
    geo=$(curl -s --max-time 5 "http://ip-api.com/json" 2>/dev/null)
    if [[ -n "$geo" ]]; then
        # Parse with python3 if available, else grep fallback
        if command -v python3 >/dev/null 2>&1; then
            python3 - <<'EOF' <<< "$geo"
import sys, json
d = json.load(sys.stdin)
fields = [("IP", "query"), ("ISP", "isp"), ("Org", "org"),
          ("Country", "country"), ("Region", "regionName"),
          ("City", "city"), ("Timezone", "timezone")]
for label, key in fields:
    print(f"  {label:<10}: {d.get(key, 'N/A')}")
EOF
        else
            echo "$geo" | grep -oE '"(query|country|city|isp)":[^,}]+' \
                | sed 's/"//g; s/:/ : /; s/^/  /'
        fi
    else
        echo "  Could not retrieve geolocation (no internet or rate-limited)"
    fi

    echo -e "\n${YELLOW}Socket statistics:${NC}"
    ss -s 2>/dev/null | head -10 | sed 's/^/  /' \
        || netstat -s 2>/dev/null | head -10 | sed 's/^/  /'

    echo -e "\n${YELLOW}Top established connections:${NC}"
    ss -tupn state established 2>/dev/null | head -20 | sed 's/^/  /' \
        || netstat -tupn 2>/dev/null | head -15 | sed 's/^/  /'
}

# ---------------------------------------------------------------------------
# 11. WiFi Diagnostics (NEW)
# ---------------------------------------------------------------------------

wifi_info() {
    echo -e "\n${GREEN}=== WiFi Diagnostics ===${NC}\n"
    log_action "WiFi diagnostics"

    # Detect wireless interface (starts with wl on Linux)
    local wlan
    wlan=$(ip link show | awk -F': ' '/^ *[0-9]+: wl/{print $2; exit}' | awk '{print $1}')

    if [[ -z "$wlan" ]]; then
        echo -e "${YELLOW}No wireless interface detected.${NC}"
        return
    fi

    echo -e "${YELLOW}Interface: ${CYAN}${wlan}${NC}\n"

    # iw (preferred, modern)
    if command -v iw >/dev/null 2>&1; then
        echo -e "${BLUE}Connection details:${NC}"
        iw dev "$wlan" link 2>/dev/null \
            | grep -E '(SSID|freq|signal|tx bitrate|Connected)' \
            | sed 's/^\s*/  /'

        echo -e "\n${BLUE}Station stats:${NC}"
        iw dev "$wlan" station dump 2>/dev/null \
            | grep -E '(signal|tx bitrate|rx bitrate|connected time)' \
            | sed 's/^\s*/  /'
    fi

    # nmcli — nearby networks
    if command -v nmcli >/dev/null 2>&1; then
        echo -e "\n${BLUE}Active connection:${NC}"
        nmcli -t -f NAME,TYPE,DEVICE,STATE connection show --active 2>/dev/null \
            | grep -i wifi | sed 's/^/  /'

        echo -e "\n${BLUE}Nearby networks:${NC}"
        nmcli -f SSID,SIGNAL,SECURITY,CHAN dev wifi list 2>/dev/null \
            | head -15 | sed 's/^/  /'
    fi

    # iwconfig fallback if iw not available
    if ! command -v iw >/dev/null 2>&1 && command -v iwconfig >/dev/null 2>&1; then
        echo -e "${BLUE}Connection details (iwconfig):${NC}"
        iwconfig "$wlan" 2>/dev/null | sed 's/^/  /'
    fi
}

# ---------------------------------------------------------------------------
# 12. Bandwidth Monitor — live (NEW)
# ---------------------------------------------------------------------------

bandwidth_monitor() {
    if [[ ! -f /proc/net/dev ]]; then
        error_exit "/proc/net/dev not available on this system"
        return
    fi

    # Detect default interface
    local default_iface
    default_iface=$(ip route show default 2>/dev/null \
        | grep -oE 'dev [^ ]+' | awk '{print $2}' | head -1)
    default_iface=${default_iface:-eth0}

    read -rp "Interface to monitor (default: $default_iface): " iface
    iface=${iface:-$default_iface}

    if ! awk -v dev="${iface}:" '$1==dev{found=1} END{exit !found}' /proc/net/dev 2>/dev/null; then
        error_exit "Interface '$iface' not found"
        return
    fi

    echo -e "\n${YELLOW}Live bandwidth on ${CYAN}${iface}${YELLOW} — Ctrl+C to stop${NC}\n"
    printf "  ${CYAN}%-10s  %-20s  %-20s  %-10s  %-10s${NC}\n" \
        "Time" "Download" "Upload" "RX pkts/s" "TX pkts/s"
    printf "  %-10s  %-20s  %-20s  %-10s  %-10s\n" \
        "----------" "--------------------" "--------------------" "----------" "----------"

    log_action "Bandwidth monitor started on $iface"

    # Override INT trap so Ctrl+C stops the monitor but not the whole script
    local _running=1
    local _old_int
    _old_int=$(trap -p INT)
    trap '_running=0' INT

    local prev_rx=0 prev_tx=0 prev_rxp=0 prev_txp=0

    while [[ $_running -eq 1 ]]; do
        local stats
        stats=$(awk -v dev="${iface}:" '$1==dev{print $2,$3,$10,$11}' /proc/net/dev)
        local rx rxp tx txp
        read -r rx rxp tx txp <<< "$stats"

        if [[ $prev_rx -ne 0 ]]; then
            local drx=$(( rx  - prev_rx  ))
            local dtx=$(( tx  - prev_tx  ))
            local drxp=$(( rxp - prev_rxp ))
            local dtxp=$(( txp - prev_txp ))

            _fmt_rate() {
                local b=$1
                if   (( b >= 1048576 )); then awk "BEGIN{printf \"%.2f MB/s\", $b/1048576}"
                elif (( b >= 1024    )); then awk "BEGIN{printf \"%.1f KB/s\", $b/1024}"
                else                          echo "${b} B/s"
                fi
            }

            local rx_str tx_str ts
            rx_str=$(_fmt_rate "$drx")
            tx_str=$(_fmt_rate "$dtx")
            ts=$(date '+%H:%M:%S')

            printf "  %-10s  ${GREEN}↓ %-18s${NC}  ${YELLOW}↑ %-18s${NC}  %-10s  %-10s\n" \
                "$ts" "$rx_str" "$tx_str" "$drxp" "$dtxp"
        fi

        prev_rx=$rx prev_tx=$tx prev_rxp=$rxp prev_txp=$txp
        sleep 1
    done

    # Restore original INT trap
    eval "${_old_int:-trap - INT}"
    echo -e "\n${YELLOW}Monitor stopped.${NC}"
    log_action "Bandwidth monitor stopped on $iface"
}

# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

show_menu() {
    clear
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║        NETWORK TOOL BY @lexlucas             ║"
    echo "║                Version 3.0                   ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo -e "  ${CYAN}Diagnostics${NC}"
    echo "   1)  Network Interfaces"
    echo "   2)  Ping Host"
    echo "   3)  Latency Graph"
    echo "   4)  Port Scan"
    echo "   5)  Routing Table"
    echo "   6)  Traceroute"
    echo ""
    echo -e "  ${CYAN}Information${NC}"
    echo "   7)  DNS Resolution"
    echo "   8)  Speed Test"
    echo "   9)  SSL Certificate Check"
    echo "  10)  Connection Info & Geolocation"
    echo "  11)  WiFi Diagnostics"
    echo ""
    echo -e "  ${CYAN}Monitor${NC}"
    echo "  12)  Bandwidth Monitor (live)"
    echo ""
    echo -e "  ${CYAN}Other${NC}"
    echo "  13)  View Log"
    echo "  14)  Exit"
    echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    setup_environment
    log_action "Network Tool v3.0 started"

    while true; do
        show_menu
        read -rp "Enter choice (1-14): " choice
        echo ""

        case $choice in
            1)  show_interfaces ;;
            2)  ping_host ;;
            3)  latency_graph ;;
            4)  port_scan ;;
            5)  show_routing ;;
            6)  trace_route ;;
            7)  check_dns ;;
            8)  speed_test ;;
            9)  ssl_check ;;
            10) connection_info ;;
            11) wifi_info ;;
            12) bandwidth_monitor ;;
            13)
                echo -e "${YELLOW}Last 30 log entries:${NC}\n"
                tail -30 "$LOG_FILE" 2>/dev/null || echo "No log file at $LOG_FILE"
                ;;
            14)
                echo -e "${GREEN}Goodbye.${NC}"
                log_action "Tool exited"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option: '$choice'${NC}"
                ;;
        esac

        echo -e "\n${BLUE}────────────────────────────────────────────────${NC}"
        read -rp "Press Enter to return to menu..."
    done
}

main "$@"
