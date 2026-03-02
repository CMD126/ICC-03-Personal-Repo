#!/bin/bash
# NMATRIX — Matrix-style Nmap Scanner
# Version: 2.0  by @lexlucas

# ---------------------------------------------------------------------------
# Colors (using $'...' so escape codes are literal — no echo -e needed)
# ---------------------------------------------------------------------------
BG=$'\033[1;32m'   # bright green
G=$'\033[0;32m'    # green
DG=$'\033[2;32m'   # dim green
R=$'\033[0;31m'    # red
Y=$'\033[1;33m'    # yellow
C=$'\033[0;36m'    # cyan
N=$'\033[0m'       # reset

LOG_DIR="${HOME}/.local/share/nmatrix"
LOG_FILE="${LOG_DIR}/scans.log"

# ---------------------------------------------------------------------------
# Core utilities
# ---------------------------------------------------------------------------

setup() {
    mkdir -p "$LOG_DIR"
    if ! command -v nmap >/dev/null 2>&1; then
        printf "%sError: nmap not installed. Run: sudo apt install nmap%s\n" "$R" "$N"
        exit 1
    fi
    # Always restore cursor on any exit
    trap 'printf "\033[?25h"' EXIT
}

log() {
    printf "[%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG_FILE"
}

# Run nmap with sudo only when not already root
nmap_run() {
    if [[ $EUID -eq 0 ]]; then
        nmap "$@"
    else
        sudo nmap "$@"
    fi
}

# ---------------------------------------------------------------------------
# Matrix animation — fixed: heads advance ONCE per frame, variable speeds,
#                   larger character set, brighter head vs trail
# ---------------------------------------------------------------------------

matrix_effect() {
    local lines cols
    lines=$(tput lines)
    cols=$(tput cols)

    # Cap to avoid extreme slowness on very wide terminals
    (( cols  > 180 )) && cols=180
    (( lines > 40  )) && lines=40

    local CHARS='!#$%&*+/<=>?@[\]^{}|~0123456789ABCDEFabcdef'
    local clen=${#CHARS}

    # Per-column state
    local -a head trail speed
    for ((c = 0; c < cols; c++)); do
        head[$c]=$(( RANDOM % lines ))
        trail[$c]=$(( RANDOM % 8 + 4 ))
        speed[$c]=$(( RANDOM % 3 + 1 ))   # 1=fast, 2=medium, 3=slow
    done

    printf "\033[?25l\033[2J"   # hide cursor, clear screen

    local frame h t ch buf row col
    for ((frame = 0; frame < 28; frame++)); do
        printf "\033[H"   # cursor home (no flicker vs clear)
        buf=""

        for ((row = 0; row < lines; row++)); do
            for ((col = 0; col < cols; col++)); do
                h=${head[$col]}
                t=${trail[$col]}
                ch="${CHARS:$(( RANDOM % clen )):1}"

                if   (( row == h           )); then buf+="${BG}${ch}${N}"
                elif (( row >= h-t && row < h )); then buf+="${G}${ch}${N}"
                elif (( row == h-t-1       )); then buf+="${DG}${ch}${N}"
                else                                  buf+=" "
                fi
            done
            (( row < lines - 1 )) && buf+=$'\n'
        done
        printf "%s" "$buf"

        # Advance each column head ONCE per frame (skip based on speed)
        for ((c = 0; c < cols; c++)); do
            if (( frame % speed[$c] == 0 )); then
                head[$c]=$(( (head[$c] + 1) % lines ))
                # Randomise trail + speed when column wraps around
                if (( head[$c] == 0 )); then
                    trail[$c]=$(( RANDOM % 8 + 4 ))
                    speed[$c]=$(( RANDOM % 3 + 1 ))
                fi
            fi
        done

        sleep 0.06
    done

    printf "\033[?25h\033[2J\033[H"   # show cursor, clear
}

# ---------------------------------------------------------------------------
# Input helpers — store result in TARGET_HOST / TARGET_NET globals
# ---------------------------------------------------------------------------

get_host() {
    read -rp "${C}Target host/IP:${N} " TARGET_HOST
    if [[ -z "$TARGET_HOST" ]]; then
        printf "%sError: host cannot be empty.%s\n" "$R" "$N"
        return 1
    fi
}

get_network() {
    read -rp "${C}Target network (e.g. 192.168.1.0/24):${N} " TARGET_NET
    if [[ -z "$TARGET_NET" ]]; then
        printf "%sError: network cannot be empty.%s\n" "$R" "$N"
        return 1
    fi
}

# ---------------------------------------------------------------------------
# Format nmap output as an aligned table (portable grep — no -P flag)
# ---------------------------------------------------------------------------

print_results() {
    local raw="$1"
    local open
    open=$(printf "%s" "$raw" | grep -E '^[0-9]+/(tcp|udp).*open')

    if [[ -z "$open" ]]; then
        printf "  %sNo open ports found.%s\n" "$Y" "$N"
        return
    fi

    printf "\n  %s%-20s %-8s %-16s %s%s\n" "$BG" "PORT" "STATE" "SERVICE" "VERSION" "$N"
    printf "  %-20s %-8s %-16s %s\n"        "----" "-----" "-------" "-------"

    while IFS= read -r line; do
        local port state service version
        port=$(awk '{print $1}' <<< "$line")
        state=$(awk '{print $2}' <<< "$line")
        service=$(awk '{print $3}' <<< "$line")
        version=$(awk '{for(i=4;i<=NF;i++) printf $i" "; print ""}' <<< "$line")
        printf "  %s%-20s%s %-8s %s%-16s%s %s\n" \
            "$G" "$port" "$N" "$state" "$C" "$service" "$N" "$version"
    done <<< "$open"
}

# ---------------------------------------------------------------------------
# Offer to save raw nmap output to a timestamped file
# ---------------------------------------------------------------------------

save_results() {
    local raw="$1" target="$2" type="$3"
    printf "\n"
    read -rp "Save full results to file? (y/N): " ans
    if [[ "${ans,,}" == "y" ]]; then
        local fname
        fname="nmap_${type}_${target//\//_}_$(date +%Y%m%d_%H%M%S).txt"
        printf "%s" "$raw" > "$fname"
        printf "%sSaved:%s %s\n" "$G" "$N" "$fname"
    fi
}

# ---------------------------------------------------------------------------
# Scan functions
# ---------------------------------------------------------------------------

scan_quick() {
    get_host || return
    printf "\n%sQuick TCP scan — %s (top 100 ports, -T4)%s\n\n" "$Y" "$TARGET_HOST" "$N"
    log "Quick TCP scan: $TARGET_HOST"
    local result
    result=$(nmap_run -sS -T4 --top-ports 100 "$TARGET_HOST" 2>/dev/null)
    print_results "$result"
    save_results "$result" "$TARGET_HOST" "quick"
}

scan_full_tcp() {
    get_host || return
    printf "\n%sFull TCP scan — %s (all 65535 ports + version)%s\n\n" "$Y" "$TARGET_HOST" "$N"
    log "Full TCP scan: $TARGET_HOST"
    local result
    result=$(nmap_run -sS -p- -sV -T4 "$TARGET_HOST" 2>/dev/null)
    print_results "$result"
    save_results "$result" "$TARGET_HOST" "full_tcp"
}

scan_service_script() {
    get_host || return
    printf "\n%sService & Script scan — %s (-sC -sV)%s\n\n" "$Y" "$TARGET_HOST" "$N"
    log "Service+Script scan: $TARGET_HOST"
    local result
    result=$(nmap_run -sC -sV -T4 "$TARGET_HOST" 2>/dev/null)
    print_results "$result"
    printf "\n%s--- NSE Script Output ---%s\n" "$C" "$N"
    grep -E '^\|' <<< "$result" | head -50 | sed 's/^/  /'
    save_results "$result" "$TARGET_HOST" "scripts"
}

scan_os() {
    get_host || return
    printf "\n%sOS Detection — %s (-O)%s\n\n" "$Y" "$TARGET_HOST" "$N"
    log "OS Detection: $TARGET_HOST"
    local result
    result=$(nmap_run -O -T4 "$TARGET_HOST" 2>/dev/null)
    print_results "$result"
    printf "\n%s--- OS Guess ---%s\n" "$C" "$N"
    grep -E '(OS:|Running:|OS CPE:|Aggressive OS)' <<< "$result" | sed 's/^/  /'
    save_results "$result" "$TARGET_HOST" "os_detect"
}

scan_udp() {
    get_host || return
    printf "\n%sUDP scan — %s (top 100 ports)%s\n\n" "$Y" "$TARGET_HOST" "$N"
    log "UDP scan: $TARGET_HOST"
    local result
    result=$(nmap_run -sU --top-ports 100 -T4 "$TARGET_HOST" 2>/dev/null)
    print_results "$result"
    save_results "$result" "$TARGET_HOST" "udp"
}

scan_ping_sweep() {
    get_network || return
    printf "\n%sPing sweep — %s%s\n\n" "$Y" "$TARGET_NET" "$N"
    log "Ping sweep: $TARGET_NET"
    local result
    result=$(nmap -sn "$TARGET_NET" 2>/dev/null)
    local hosts
    hosts=$(grep "Nmap scan report for" <<< "$result" | sed 's/Nmap scan report for //')
    if [[ -n "$hosts" ]]; then
        printf "  %sLive hosts:%s\n" "$BG" "$N"
        sed 's/^/  /' <<< "$hosts"
    else
        printf "  %sNo live hosts found.%s\n" "$Y" "$N"
    fi
    save_results "$result" "$TARGET_NET" "ping_sweep"
}

scan_vuln() {
    get_host || return
    printf "\n%sVulnerability scan — %s (--script vuln)%s\n" "$R" "$TARGET_HOST" "$N"
    printf "%sOnly scan targets you own or have explicit permission to test.%s\n\n" "$Y" "$N"
    log "Vuln scan: $TARGET_HOST"
    local result
    result=$(nmap_run --script vuln -T4 "$TARGET_HOST" 2>/dev/null)
    print_results "$result"
    printf "\n%s--- Vulnerability Output ---%s\n" "$C" "$N"
    grep -E '(\||\+--)' <<< "$result" | head -60 | sed 's/^/  /'
    save_results "$result" "$TARGET_HOST" "vuln"
}

scan_custom() {
    get_host || return
    read -rp "${C}Custom nmap flags (e.g. -p 80,443 -sV --script http-title):${N} " flags
    if [[ -z "$flags" ]]; then
        printf "%sNo flags entered.%s\n" "$R" "$N"; return
    fi
    printf "\n%sCustom scan — %s : nmap %s%s\n\n" "$Y" "$TARGET_HOST" "$flags" "$N"
    log "Custom scan: $TARGET_HOST flags=$flags"
    local result
    # shellcheck disable=SC2086  (intentional word splitting for flags)
    result=$(nmap_run $flags "$TARGET_HOST" 2>/dev/null)
    print_results "$result"
    save_results "$result" "$TARGET_HOST" "custom"
}

# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

show_menu() {
    clear
    printf "%s" "$BG"
    echo "╔═════════════════════════════════════════════════╗"
    echo "║          NMATRIX  //  Nmap Scanner              ║"
    echo "║                  Version 2.0                   ║"
    echo "╚═════════════════════════════════════════════════╝"
    printf "%s\n" "$N"
    printf "  %sScans:%s\n" "$G" "$N"
    echo "   1)  Quick TCP Scan         (top 100 ports)"
    echo "   2)  Full TCP Scan          (all 65535 ports + version)"
    echo "   3)  Service & Script Scan  (-sC -sV + NSE output)"
    echo "   4)  OS Detection           (requires root)"
    echo "   5)  UDP Scan               (top 100 ports)"
    echo "   6)  Ping Sweep             (host discovery)"
    echo "   7)  Vulnerability Scan     (--script vuln)"
    echo "   8)  Custom Scan            (manual nmap flags)"
    echo ""
    printf "  %sOther:%s\n" "$G" "$N"
    echo "   9)  View Scan Log"
    echo "  10)  Exit"
    echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    setup
    log "NMATRIX v2.0 started"
    matrix_effect   # animation runs once at startup only

    while true; do
        show_menu
        read -rp "Select option (1-10): " choice
        printf "\n"

        case $choice in
            1)  scan_quick          ;;
            2)  scan_full_tcp       ;;
            3)  scan_service_script ;;
            4)  scan_os             ;;
            5)  scan_udp            ;;
            6)  scan_ping_sweep     ;;
            7)  scan_vuln           ;;
            8)  scan_custom         ;;
            9)
                printf "%sLast 30 scan log entries:%s\n\n" "$Y" "$N"
                tail -30 "$LOG_FILE" 2>/dev/null || printf "No log yet at %s\n" "$LOG_FILE"
                ;;
            10)
                printf "\n%sExiting NMATRIX...%s\n" "$BG" "$N"
                log "NMATRIX exited"
                exit 0
                ;;
            *)
                printf "%sInvalid option: '%s'%s\n" "$R" "$choice" "$N"
                ;;
        esac

        printf "\n%s────────────────────────────────────────────────%s\n" "$G" "$N"
        read -rp "Press Enter to return to menu..."
    done
}

main "$@"
