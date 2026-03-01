#!/bin/bash
# Syscript — Ubuntu System Administration Toolkit
# Version: 2.0  by @lexlucas

# ---------------------------------------------------------------------------
# Colors (literal escape chars via $'...' — no echo -e needed)
# ---------------------------------------------------------------------------
GREEN=$'\033[0;32m'
BGREEN=$'\033[1;32m'
RED=$'\033[0;31m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
DIM=$'\033[2m'
NC=$'\033[0m'

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

confirm() {
    # confirm "message" → returns 0 if user types y/Y, 1 otherwise
    local msg="${1:-Are you sure?}"
    read -rp "${YELLOW}${msg} (y/N): ${NC}" ans
    [[ "${ans,,}" == "y" ]]
}

section() {
    printf "\n%s=== %s ===%s\n\n" "$CYAN" "$1" "$NC"
}

pause() {
    printf "\n%sPress Enter to continue...%s" "$DIM" "$NC"
    read -r
}

pkg_check() {
    # pkg_check name → prints warning and returns 1 if not installed
    if ! command -v "$1" >/dev/null 2>&1; then
        printf "%s'%s' is not installed.%s\n" "$YELLOW" "$1" "$NC"
        return 1
    fi
}

bar() {
    # bar value max width → prints ASCII progress bar
    local val=$1 max=$2 width=${3:-30}
    (( max == 0 )) && max=1
    local filled=$(( val * width / max ))
    local empty=$(( width - filled ))
    local b=""
    for ((i = 0; i < filled; i++)); do b+="█"; done
    for ((i = 0; i < empty;  i++)); do b+="░"; done
    local pct=$(( val * 100 / max ))
    local color=$GREEN
    (( pct > 70 )) && color=$YELLOW
    (( pct > 90 )) && color=$RED
    printf "%s[%s]%s %d%%" "$color" "$b" "$NC" "$pct"
}

# ---------------------------------------------------------------------------
# Package Management
# ---------------------------------------------------------------------------

pkg_update() {
    section "Update & Full-Upgrade"
    sudo apt update && sudo apt full-upgrade -y \
        && printf "\n%sSystem is up to date.%s\n" "$GREEN" "$NC" \
        || printf "%sUpdate failed.%s\n" "$RED" "$NC"
}

pkg_autoremove() {
    section "Autoremove"
    sudo apt autoremove -y \
        && printf "%sAutoremove complete.%s\n" "$GREEN" "$NC" \
        || printf "%sAutoremove failed.%s\n" "$RED" "$NC"
}

pkg_clean() {
    section "Clean Cache"
    sudo apt clean && sudo apt autoclean
    printf "%sCache cleaned.%s\n" "$GREEN" "$NC"
}

pkg_upgradable() {
    section "Upgradable Packages"
    apt list --upgradable 2>/dev/null | grep -v "^Listing"
}

pkg_installed() {
    section "Installed Packages"
    dpkg --get-selections | grep -v deinstall | less
}

pkg_search() {
    section "Search Repository"
    read -rp "${CYAN}Package name to search: ${NC}" pkg
    [[ -z "$pkg" ]] && printf "%sNo name entered.%s\n" "$RED" "$NC" && return
    apt-cache search "$pkg" | sort | less
}

pkg_install() {
    section "Install Package"
    read -rp "${CYAN}Package name to install: ${NC}" pkg
    [[ -z "$pkg" ]] && printf "%sNo name entered.%s\n" "$RED" "$NC" && return
    printf "Installing '%s'...\n" "$pkg"
    sudo apt install "$pkg" -y \
        && printf "%sInstalled: %s%s\n" "$GREEN" "$pkg" "$NC" \
        || printf "%sInstall failed.%s\n" "$RED" "$NC"
}

pkg_remove() {
    section "Remove Package"
    read -rp "${CYAN}Package name to remove: ${NC}" pkg
    [[ -z "$pkg" ]] && printf "%sNo name entered.%s\n" "$RED" "$NC" && return
    confirm "Remove '$pkg'?" || { printf "Cancelled.\n"; return; }
    sudo apt remove "$pkg" -y \
        && printf "%sRemoved: %s%s\n" "$GREEN" "$pkg" "$NC" \
        || printf "%sRemoval failed.%s\n" "$RED" "$NC"
}

pkg_purge() {
    section "Purge Package"
    read -rp "${CYAN}Package name to purge (removes config too): ${NC}" pkg
    [[ -z "$pkg" ]] && printf "%sNo name entered.%s\n" "$RED" "$NC" && return
    confirm "Purge '$pkg' including all config files?" || { printf "Cancelled.\n"; return; }
    sudo apt purge "$pkg" -y \
        && printf "%sPurged: %s%s\n" "$GREEN" "$pkg" "$NC" \
        || printf "%sPurge failed.%s\n" "$RED" "$NC"
}

# ---------------------------------------------------------------------------
# System Information
# ---------------------------------------------------------------------------

sys_disk() {
    section "Disk Usage"
    df -h --output=source,size,used,avail,pcent,target \
        | grep -E '^(Filesystem|/dev/)' \
        | column -t
}

sys_memory() {
    section "Memory & Swap"
    free -h
    printf "\n%s--- /proc/meminfo summary ---%s\n" "$DIM" "$NC"
    awk '/^(MemTotal|MemAvailable|MemFree|SwapTotal|SwapFree|Buffers|Cached)/{
        printf "  %-20s %s\n", $1, $2" "$3
    }' /proc/meminfo
}

sys_cpu() {
    section "CPU Info & Load Average"
    printf "%sCPU model:%s\n" "$BOLD" "$NC"
    grep "model name" /proc/cpuinfo | head -1 | awk -F': ' '{print "  "$2}'
    printf "%sCores:%s %s\n" "$BOLD" "$NC" "$(nproc)"
    printf "%sCache:%s\n" "$BOLD" "$NC"
    grep "cache size" /proc/cpuinfo | head -1 | awk -F': ' '{print "  "$2}'
    printf "\n%sLoad average (1m / 5m / 15m):%s\n" "$BOLD" "$NC"
    read load1 load5 load15 _ < /proc/loadavg
    printf "  %s / %s / %s\n" "$load1" "$load5" "$load15"
    printf "\n%sUptime:%s %s\n" "$BOLD" "$NC" "$(uptime -p 2>/dev/null || uptime)"
}

sys_info() {
    section "System Information"
    printf "%sKernel:%s\n  %s\n\n" "$BOLD" "$NC" "$(uname -a)"
    if command -v lsb_release >/dev/null 2>&1; then
        printf "%sDistribution:%s\n" "$BOLD" "$NC"
        lsb_release -a 2>/dev/null | grep -v "^No LSB" | sed 's/^/  /'
    elif [[ -f /etc/os-release ]]; then
        printf "%sDistribution:%s\n" "$BOLD" "$NC"
        grep -E '^(NAME|VERSION)=' /etc/os-release | sed 's/^/  /'
    fi
}

sys_processes() {
    section "Running Processes"
    printf "%sTop 20 by CPU usage:%s\n" "$BOLD" "$NC"
    ps aux --sort=-%cpu | head -21 | \
        awk 'NR==1{printf "  %-10s %-6s %-5s %-5s %s\n",$1,$2,$3,$4,$11}
             NR>1{printf "  %-10s %-6s %-5s %-5s %s\n",$1,$2,$3,$4,$11}'
    printf "\n%sTop 10 by memory usage:%s\n" "$BOLD" "$NC"
    ps aux --sort=-%mem | head -11 | \
        awk 'NR==1{printf "  %-10s %-6s %-5s %-5s %s\n",$1,$2,$3,$4,$11}
             NR>1{printf "  %-10s %-6s %-5s %-5s %s\n",$1,$2,$3,$4,$11}'
}

sys_hardware() {
    section "Hardware Summary"
    if pkg_check "lshw"; then
        sudo lshw -short 2>/dev/null | less
    else
        printf "%sCPU:%s\n" "$BOLD" "$NC"
        grep "model name" /proc/cpuinfo | head -1 | awk -F': ' '{print "  "$2}'
        printf "\n%sBlock devices:%s\n" "$BOLD" "$NC"
        lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | sed 's/^/  /'
        printf "\n%sPCI devices:%s\n" "$BOLD" "$NC"
        command -v lspci >/dev/null 2>&1 && lspci | head -20 | sed 's/^/  /' \
            || echo "  lspci not available"
    fi
}

# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------

net_interfaces() {
    section "Network Interfaces"
    ip -brief addr show
    printf "\n%sDetailed:%s\n" "$BOLD" "$NC"
    ip addr show | grep -E '^[0-9]+:|inet' | sed 's/^/  /'
}

net_ports() {
    section "Open Ports & Listeners"
    ss -tuln | column -t
}

net_connections() {
    section "Active Connections"
    printf "%sEstablished TCP/UDP connections:%s\n" "$BOLD" "$NC"
    ss -tupn state established 2>/dev/null | column -t | head -40 \
        || netstat -tupn 2>/dev/null | head -30
}

# ---------------------------------------------------------------------------
# System Management
# ---------------------------------------------------------------------------

mgmt_logs() {
    section "System Logs (last 50 entries)"
    # No sudo needed for user-visible logs; no pager trap
    journalctl -n 50 --no-pager 2>/dev/null \
        || sudo journalctl -n 50 --no-pager 2>/dev/null \
        || tail -50 /var/log/syslog 2>/dev/null \
        || printf "%sNo accessible log source found.%s\n" "$YELLOW" "$NC"
}

mgmt_failed_services() {
    section "Failed Services"
    local failed
    failed=$(systemctl --failed --no-legend 2>/dev/null)
    if [[ -z "$failed" ]]; then
        printf "%sNo failed services.%s\n" "$GREEN" "$NC"
    else
        printf "%sFailed:%s\n" "$RED" "$NC"
        echo "$failed" | sed 's/^/  /'
    fi
}

mgmt_service_control() {
    section "Service Control"
    read -rp "${CYAN}Service name: ${NC}" svc
    [[ -z "$svc" ]] && printf "%sNo service entered.%s\n" "$RED" "$NC" && return

    printf "\n  1) Status   2) Start   3) Stop\n"
    printf "  4) Restart  5) Enable  6) Disable\n\n"
    read -rp "${CYAN}Action: ${NC}" action

    case "$action" in
        1) systemctl status "$svc" --no-pager ;;
        2) sudo systemctl start   "$svc" && printf "%sStarted.%s\n"  "$GREEN" "$NC" ;;
        3) sudo systemctl stop    "$svc" && printf "%sStopped.%s\n"  "$GREEN" "$NC" ;;
        4) sudo systemctl restart "$svc" && printf "%sRestarted.%s\n" "$GREEN" "$NC" ;;
        5) sudo systemctl enable  "$svc" && printf "%sEnabled.%s\n"  "$GREEN" "$NC" ;;
        6) sudo systemctl disable "$svc" && printf "%sDisabled.%s\n" "$GREEN" "$NC" ;;
        *) printf "%sInvalid action.%s\n" "$RED" "$NC" ;;
    esac
}

mgmt_firewall() {
    section "UFW Firewall Status"
    if pkg_check "ufw"; then return; fi
    sudo ufw status verbose
}

mgmt_clear_logs() {
    section "Clear Old Journal Logs"
    printf "Current journal size: "
    journalctl --disk-usage 2>/dev/null | grep "Archived and active"
    printf "\n"
    read -rp "${CYAN}Keep logs for how many days? (default 7): ${NC}" days
    days=${days:-7}
    if [[ ! "$days" =~ ^[0-9]+$ ]]; then
        printf "%sInvalid number.%s\n" "$RED" "$NC"; return
    fi
    confirm "Delete journal logs older than ${days} days?" || { printf "Cancelled.\n"; return; }
    sudo journalctl --vacuum-time="${days}d" \
        && printf "%sLogs older than %s days removed.%s\n" "$GREEN" "$days" "$NC"
}

# ---------------------------------------------------------------------------
# User & Environment
# ---------------------------------------------------------------------------

user_info() {
    section "User Information"
    printf "%sCurrent user:%s  %s\n" "$BOLD" "$NC" "$(whoami)"
    printf "%sUID/GID/Groups:%s\n  %s\n" "$BOLD" "$NC" "$(id)"
    printf "\n%sSupplementary groups:%s\n" "$BOLD" "$NC"
    groups | tr ' ' '\n' | sed 's/^/  /'
    printf "\n%sHome directory:%s  %s\n" "$BOLD" "$NC" "$HOME"
    printf "%sLogin shell:%s    %s\n"    "$BOLD" "$NC" "$(getent passwd "$(whoami)" | cut -d: -f7)"
    printf "\n%sRecent logins:%s\n" "$BOLD" "$NC"
    last "$(whoami)" | head -6 | sed 's/^/  /'
}

user_cron() {
    section "Scheduled Tasks"
    printf "%sCrontab (current user):%s\n" "$BOLD" "$NC"
    crontab -l 2>/dev/null | grep -v '^#' | grep -v '^$' | sed 's/^/  /' \
        || printf "  %s(no crontab)%s\n" "$DIM" "$NC"
    printf "\n%sSystemd timers:%s\n" "$BOLD" "$NC"
    systemctl list-timers --no-pager 2>/dev/null | head -20 | sed 's/^/  /' \
        || printf "  %s(systemd not available)%s\n" "$DIM" "$NC"
}

user_env() {
    section "Environment Variables"
    printenv | sort | less
}

user_history() {
    section "Bash History (last 50 commands)"
    local histfile="${HISTFILE:-$HOME/.bash_history}"
    if [[ -f "$histfile" ]]; then
        tail -50 "$histfile"
    else
        printf "%sNo history file found at %s%s\n" "$YELLOW" "$histfile" "$NC"
    fi
}

# ---------------------------------------------------------------------------
# System Health Overview (dashboard)
# ---------------------------------------------------------------------------

sys_health() {
    section "System Health Overview"

    # Uptime & Load
    read load1 load5 load15 _ < /proc/loadavg
    printf "%sUptime:%s   %s\n" "$BOLD" "$NC" "$(uptime -p 2>/dev/null || uptime)"
    printf "%sLoad:%s     %s (1m)  %s (5m)  %s (15m)\n\n" \
        "$BOLD" "$NC" "$load1" "$load5" "$load15"

    # Memory
    local mem_total mem_avail mem_used
    mem_total=$(awk '/MemTotal/{print $2}'    /proc/meminfo)
    mem_avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    mem_used=$(( mem_total - mem_avail ))
    printf "%sMemory:%s  " "$BOLD" "$NC"
    bar "$mem_used" "$mem_total"
    printf "  (%d MB used / %d MB total)\n\n" \
        "$(( mem_used / 1024 ))" "$(( mem_total / 1024 ))"

    # Disk (each real device)
    printf "%sDisk:%s\n" "$BOLD" "$NC"
    df -h --output=source,used,size,pcent,target \
        | grep '^/dev/' \
        | while read -r dev used size pct mnt; do
            local pct_num="${pct/\%/}"
            printf "  %-15s %-8s / %-8s " "$dev" "$used" "$size"
            bar "$pct_num" 100 20
            printf "  %s\n" "$mnt"
        done

    # Failed services
    printf "\n%sFailed services:%s  " "$BOLD" "$NC"
    local failed_count
    failed_count=$(systemctl --failed --no-legend 2>/dev/null | wc -l)
    if (( failed_count > 0 )); then
        printf "%s%d failed%s\n" "$RED" "$failed_count" "$NC"
        systemctl --failed --no-legend 2>/dev/null | awk '{print "    "$1}'
    else
        printf "%snone%s\n" "$GREEN" "$NC"
    fi

    # Pending updates
    printf "\n%sPending updates:%s  " "$BOLD" "$NC"
    local updates
    updates=$(apt list --upgradable 2>/dev/null | grep -c "upgradable" || echo 0)
    if (( updates > 0 )); then
        printf "%s%d package(s)%s\n" "$YELLOW" "$updates" "$NC"
    else
        printf "%sup to date%s\n" "$GREEN" "$NC"
    fi
}

# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

show_menu() {
    clear
    local host uptime_str load1 load5 load15
    host=$(hostname)
    uptime_str=$(uptime -p 2>/dev/null | sed 's/up //')
    read load1 load5 load15 _ < /proc/loadavg

    printf "%s" "$BGREEN"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║         SYSCRIPT  //  Ubuntu Admin Toolkit       ║"
    echo "╚══════════════════════════════════════════════════╝"
    printf "%s\n" "$NC"
    printf "  %s%-10s%s %-22s  %sLoad:%s %s %s %s\n\n" \
        "$BOLD" "$host" "$NC" "$uptime_str" \
        "$DIM" "$NC" "$load1" "$load5" "$load15"

    printf "  %s[Package Management]%s\n" "$CYAN" "$NC"
    printf "   1)  Update & full-upgrade      2)  Autoremove\n"
    printf "   3)  Clean cache                4)  List upgradable\n"
    printf "   5)  List installed             6)  Search repository\n"
    printf "   7)  Install package            8)  Remove package\n"
    printf "   9)  Purge package\n\n"

    printf "  %s[System Information]%s\n" "$CYAN" "$NC"
    printf "  10)  Disk usage               11)  Memory & swap\n"
    printf "  12)  CPU info & load          13)  System info\n"
    printf "  14)  Running processes        15)  Hardware summary\n\n"

    printf "  %s[Network]%s\n" "$CYAN" "$NC"
    printf "  16)  Network interfaces       17)  Open ports\n"
    printf "  18)  Active connections\n\n"

    printf "  %s[System Management]%s\n" "$CYAN" "$NC"
    printf "  19)  System logs              20)  Failed services\n"
    printf "  21)  Service control          22)  UFW firewall status\n"
    printf "  23)  Clear old journal logs\n\n"

    printf "  %s[User & Environment]%s\n" "$CYAN" "$NC"
    printf "  24)  User info                25)  Scheduled tasks\n"
    printf "  26)  Environment variables    27)  Bash history\n\n"

    printf "  %s[Extra]%s\n" "$CYAN" "$NC"
    printf "  28)  System health overview\n\n"

    printf "   %sq)  Quit%s\n\n" "$RED" "$NC"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    while true; do
        show_menu
        read -rp "${CYAN}Enter choice: ${NC}" choice
        printf "\n"

        case "$choice" in
            1)  pkg_update          ;;
            2)  pkg_autoremove      ;;
            3)  pkg_clean           ;;
            4)  pkg_upgradable      ;;
            5)  pkg_installed       ;;
            6)  pkg_search          ;;
            7)  pkg_install         ;;
            8)  pkg_remove          ;;
            9)  pkg_purge           ;;
            10) sys_disk            ;;
            11) sys_memory          ;;
            12) sys_cpu             ;;
            13) sys_info            ;;
            14) sys_processes       ;;
            15) sys_hardware        ;;
            16) net_interfaces      ;;
            17) net_ports           ;;
            18) net_connections     ;;
            19) mgmt_logs           ;;
            20) mgmt_failed_services ;;
            21) mgmt_service_control ;;
            22) mgmt_firewall       ;;
            23) mgmt_clear_logs     ;;
            24) user_info           ;;
            25) user_cron           ;;
            26) user_env            ;;
            27) user_history        ;;
            28) sys_health          ;;
            q|Q)
                printf "%sExiting Syscript. Goodbye.%s\n" "$GREEN" "$NC"
                exit 0
                ;;
            "")
                # ignore empty Enter press
                continue
                ;;
            *)
                printf "%sInvalid option: '%s'%s\n" "$RED" "$choice" "$NC"
                ;;
        esac

        pause
    done
}

main "$@"
