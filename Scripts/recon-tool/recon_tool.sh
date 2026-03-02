#!/usr/bin/env bash
# ==============================================================================
#  Recon Tool — v1.0
#  Automated OSINT & reconnaissance for a target domain or IP.
#  Only scan targets you own or have explicit permission to test.
# ==============================================================================

# ── Colours ────────────────────────────────────────────────────────────────────
R='\033[0;31m'; G='\033[0;32m'; Y='\033[0;33m'
B='\033[0;34m'; C='\033[0;36m'; W='\033[1;37m'; N='\033[0m'

# ── Config ─────────────────────────────────────────────────────────────────────
LOG_DIR="${HOME}/.local/share/recon"
TIMEOUT=10
WORDLIST_SIZE=50        # number of common subdomains to try

# ── Common subdomains wordlist ─────────────────────────────────────────────────
SUBDOMAINS=(
  www mail ftp ssh vpn admin portal api dev staging test beta
  app cdn static assets media img images upload download backup
  blog forum shop store support helpdesk docs wiki git gitlab
  jenkins ci smtp pop imap webmail mx ns1 ns2 ldap monitor
  db database redis elastic kibana grafana prometheus vault
)

# ── Helpers ────────────────────────────────────────────────────────────────────
sep()   { echo -e "${B}$(printf '─%.0s' {1..65})${N}"; }
title() { sep; echo -e "${W}  $1${N}"; sep; }
info()  { echo -e "  ${G}[+]${N} $1"; }
warn()  { echo -e "  ${Y}[!]${N} $1"; }
err()   { echo -e "  ${R}[-]${N} $1"; }
need()  { command -v "$1" &>/dev/null; }

log_write() {
    mkdir -p "$LOG_DIR"
    local file="${LOG_DIR}/recon_${TARGET}_$(date +%Y%m%d_%H%M%S).txt"
    echo "$1" | tee -a "$file" >/dev/null
}

check_target() {
    if [[ -z "$TARGET" ]]; then
        echo -e "\n${C}Enter target (domain or IP): ${N}"
        read -r TARGET
        TARGET="${TARGET,,}"          # lowercase
        TARGET="${TARGET#http*://}"   # strip scheme
        TARGET="${TARGET%%/*}"        # strip path
    fi
    if [[ -z "$TARGET" ]]; then
        err "No target specified."; return 1
    fi
}

# ── 1. WHOIS ───────────────────────────────────────────────────────────────────
run_whois() {
    title "WHOIS LOOKUP  →  ${TARGET}"
    if need whois; then
        local out
        out=$(timeout "$TIMEOUT" whois "$TARGET" 2>/dev/null)
        if [[ -z "$out" ]]; then
            warn "No WHOIS data returned."
        else
            # Print key fields only
            echo "$out" | grep -iE \
              "registrar:|registrant|creation date|expiry|updated|name server|status|country|organisation|admin|tech" \
              | head -40 | sed 's/^/  /'
        fi
    else
        warn "whois not installed.  Install: sudo apt install whois"
    fi
}

# ── 2. DNS Records ─────────────────────────────────────────────────────────────
run_dns() {
    title "DNS RECORDS  →  ${TARGET}"
    local resolver
    if need dig; then
        resolver="dig +short"
    elif need nslookup; then
        resolver=""   # handled differently below
    else
        warn "Neither dig nor nslookup found."; return
    fi

    for type in A AAAA MX NS TXT SOA CNAME; do
        local result
        if need dig; then
            result=$(timeout "$TIMEOUT" dig +short "$TARGET" "$type" 2>/dev/null)
        else
            result=$(timeout "$TIMEOUT" nslookup -type="$type" "$TARGET" 2>/dev/null \
                     | grep -v "^Server\|^Address\|^Non-auth" | grep -v "^$")
        fi
        if [[ -n "$result" ]]; then
            echo -e "\n  ${Y}${type}${N}"
            echo "$result" | sed 's/^/    /'
        fi
    done

    # DNSSEC check
    echo -e "\n  ${Y}DNSSEC${N}"
    if need dig; then
        local dnssec
        dnssec=$(timeout "$TIMEOUT" dig "$TARGET" +dnssec +short 2>/dev/null | grep -i "rrsig\|dnskey")
        if [[ -n "$dnssec" ]]; then
            echo -e "    ${G}Enabled${N}"
        else
            echo -e "    ${R}Not detected${N}"
        fi
    else
        warn "dig required for DNSSEC detection"
    fi
}

# ── 3. Subdomain Enumeration ───────────────────────────────────────────────────
run_subdomains() {
    title "SUBDOMAIN ENUMERATION  →  ${TARGET}"
    warn "Testing ${#SUBDOMAINS[@]} common subdomains..."
    echo ""

    local found=0
    for sub in "${SUBDOMAINS[@]}"; do
        local fqdn="${sub}.${TARGET}"
        local result
        if need dig; then
            result=$(timeout 3 dig +short "$fqdn" A 2>/dev/null | head -1)
        elif need host; then
            result=$(timeout 3 host "$fqdn" 2>/dev/null | grep "has address" | awk '{print $NF}' | head -1)
        else
            result=$(timeout 3 getent hosts "$fqdn" 2>/dev/null | awk '{print $1}' | head -1)
        fi
        if [[ -n "$result" ]]; then
            printf "  ${G}[FOUND]${N}  %-35s  ${C}%s${N}\n" "$fqdn" "$result"
            ((found++))
        fi
    done

    echo ""
    if [[ $found -eq 0 ]]; then
        warn "No subdomains resolved."
    else
        info "$found subdomain(s) found."
    fi

    # nmap subdomain check if available
    if need nmap; then
        echo -e "\n  ${Y}Running nmap DNS brute-force (--script dns-brute)...${N}"
        timeout 30 nmap --script dns-brute -p 80 "$TARGET" 2>/dev/null \
            | grep -E "DNS_BRUTE|[0-9]+\.[0-9]" | sed 's/^/  /'
    fi
}

# ── 4. Port Scan ───────────────────────────────────────────────────────────────
run_portscan() {
    title "PORT SCAN  →  ${TARGET}"
    if need nmap; then
        warn "Scanning top 1000 ports (TCP)..."
        echo ""
        local flags="-T4 --open"
        [[ $EUID -eq 0 ]] && flags="-sS $flags" || flags="-sT $flags"
        timeout 60 nmap $flags "$TARGET" 2>/dev/null \
            | grep -E "^[0-9]+|Nmap scan report|Host is" | sed 's/^/  /'
    else
        warn "nmap not installed.  Running basic TCP check on common ports..."
        local ports=(21 22 23 25 53 80 110 143 443 445 3306 3389 5432 6379 8080 8443 27017)
        for p in "${ports[@]}"; do
            (echo >/dev/tcp/"$TARGET"/"$p") 2>/dev/null \
                && echo -e "  ${G}[OPEN]${N}  $p/tcp" \
                || true
        done
    fi
}

# ── 5. HTTP Headers & Security Audit ──────────────────────────────────────────
run_http() {
    title "HTTP HEADERS  →  ${TARGET}"
    if ! need curl; then
        warn "curl not installed."; return
    fi

    local url="https://${TARGET}"
    local headers
    headers=$(timeout "$TIMEOUT" curl -skI -L --max-redirs 5 \
              -A "Mozilla/5.0" "$url" 2>/dev/null)

    if [[ -z "$headers" ]]; then
        url="http://${TARGET}"
        headers=$(timeout "$TIMEOUT" curl -skI -L --max-redirs 5 \
                  -A "Mozilla/5.0" "$url" 2>/dev/null)
    fi

    if [[ -z "$headers" ]]; then
        err "No HTTP response from $TARGET"; return
    fi

    # Status line
    local status
    status=$(echo "$headers" | grep -i "^HTTP/" | tail -1)
    echo -e "\n  ${W}Status:${N}  $status"

    # All headers
    echo -e "\n  ${Y}Response Headers:${N}"
    echo "$headers" | grep -v "^HTTP/" | grep -v "^$" | sed 's/^/    /'

    # Security header audit
    echo -e "\n  ${Y}Security Header Audit:${N}"
    local sec_headers=(
        "Strict-Transport-Security:HSTS"
        "Content-Security-Policy:CSP"
        "X-Frame-Options:X-Frame-Options"
        "X-Content-Type-Options:X-Content-Type-Options"
        "Referrer-Policy:Referrer-Policy"
        "Permissions-Policy:Permissions-Policy"
        "X-XSS-Protection:X-XSS-Protection"
    )
    local score=0; local total=0
    for entry in "${sec_headers[@]}"; do
        local hname="${entry%%:*}"; local label="${entry##*:}"
        ((total++))
        if echo "$headers" | grep -qi "^${hname}:"; then
            echo -e "    ${G}[PRESENT]${N}  $label"
            ((score++))
        else
            echo -e "    ${R}[MISSING]${N}  $label"
        fi
    done

    # Information disclosure
    echo -e "\n  ${Y}Information Disclosure:${N}"
    for h in "Server:" "X-Powered-By:" "X-AspNet-Version:" "X-Generator:"; do
        local val
        val=$(echo "$headers" | grep -i "^${h}" | head -1)
        [[ -n "$val" ]] && echo -e "    ${R}[EXPOSED]${N}  $val" || true
    done

    # Score
    echo -e "\n  ${W}Security Score: ${score}/${total}${N}"
}

# ── 6. SSL Certificate ─────────────────────────────────────────────────────────
run_ssl() {
    title "SSL/TLS CERTIFICATE  →  ${TARGET}"
    if ! need openssl; then
        warn "openssl not installed."; return
    fi

    local raw
    raw=$(echo | timeout "$TIMEOUT" openssl s_client -connect "${TARGET}:443" \
          -servername "$TARGET" 2>/dev/null)

    if [[ -z "$raw" ]]; then
        err "Could not connect to ${TARGET}:443"; return
    fi

    local cert
    cert=$(echo "$raw" | openssl x509 -noout -text 2>/dev/null)

    # Subject / Issuer
    echo ""
    echo "$raw" | openssl x509 -noout -subject -issuer 2>/dev/null | sed 's/^/  /'

    # Validity
    local not_before not_after
    not_before=$(echo "$raw" | openssl x509 -noout -startdate 2>/dev/null | cut -d= -f2)
    not_after=$(echo "$raw"  | openssl x509 -noout -enddate  2>/dev/null | cut -d= -f2)
    echo -e "  Valid From : $not_before"
    echo -e "  Expires    : $not_after"

    # Days remaining
    local expiry_epoch now_epoch days_left
    expiry_epoch=$(date -d "$not_after" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$not_after" +%s 2>/dev/null)
    now_epoch=$(date +%s)
    if [[ -n "$expiry_epoch" ]]; then
        days_left=$(( (expiry_epoch - now_epoch) / 86400 ))
        if   [[ $days_left -gt 30 ]]; then echo -e "  ${G}Days Left  : $days_left${N}"
        elif [[ $days_left -gt 7  ]]; then echo -e "  ${Y}Days Left  : $days_left (expiring soon)${N}"
        else                               echo -e "  ${R}Days Left  : $days_left (CRITICAL)${N}"; fi
    fi

    # SANs
    echo -e "\n  ${Y}Subject Alternative Names:${N}"
    echo "$cert" | grep -A1 "Subject Alternative Name" | grep DNS | \
        tr ',' '\n' | sed 's/DNS://g;s/^ //;s/^/    /'

    # Fingerprint + cipher
    echo -e "\n  ${Y}SHA-1 Fingerprint:${N}"
    echo "$raw" | openssl x509 -noout -fingerprint -sha1 2>/dev/null | sed 's/^/    /'

    echo -e "\n  ${Y}Negotiated Cipher:${N}"
    echo "$raw" | grep "Cipher" | head -1 | sed 's/^/    /'

    # Weak protocol check
    echo -e "\n  ${Y}Weak Protocol Check:${N}"
    for proto in tls1 tls1_1; do
        local label
        [[ "$proto" == "tls1" ]] && label="TLS 1.0" || label="TLS 1.1"
        if echo | timeout 5 openssl s_client -connect "${TARGET}:443" \
                  -"${proto}" -servername "$TARGET" 2>/dev/null | grep -q "Cipher"; then
            echo -e "    ${R}[WEAK]${N}  $label accepted"
        else
            echo -e "    ${G}[OK]${N}    $label not accepted"
        fi
    done
}

# ── 7. IP Geolocation ──────────────────────────────────────────────────────────
run_geo() {
    title "IP GEOLOCATION  →  ${TARGET}"
    if ! need curl; then
        warn "curl not installed."; return
    fi

    local json
    json=$(timeout "$TIMEOUT" curl -s "http://ip-api.com/json/${TARGET}?fields=status,message,query,country,regionName,city,zip,isp,org,as,timezone,lat,lon" 2>/dev/null)

    if [[ -z "$json" ]]; then
        err "No response from ip-api.com"; return
    fi

    local status
    status=$(echo "$json" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    if [[ "$status" == "fail" ]]; then
        warn "Geolocation failed (private/reserved IP or rate-limited)."; return
    fi

    echo ""
    for field in query country regionName city zip isp org as timezone lat lon; do
        local val
        val=$(echo "$json" | grep -o "\"${field}\":\"[^\"]*\"" | cut -d'"' -f4)
        [[ -z "$val" ]] && val=$(echo "$json" | grep -o "\"${field}\":[0-9.]*" | cut -d: -f2)
        [[ -n "$val" ]] && printf "  ${G}%-14s${N}  %s\n" "$field" "$val"
    done
}

# ── 8. Full Recon ──────────────────────────────────────────────────────────────
run_full() {
    title "FULL RECON  →  ${TARGET}"
    warn "Running all modules. This may take a few minutes..."
    echo ""
    run_whois
    run_dns
    run_subdomains
    run_portscan
    run_http
    run_ssl
    run_geo

    # Save to log
    local logfile="${LOG_DIR}/recon_${TARGET}_$(date +%Y%m%d_%H%M%S).txt"
    mkdir -p "$LOG_DIR"
    {
        echo "Recon Report — ${TARGET} — $(date)"
        sep_plain() { printf '─%.0s' {1..65}; echo; }
        sep_plain
        run_whois 2>/dev/null
        run_dns   2>/dev/null
    } > "$logfile" 2>/dev/null
    echo -e "\n  ${G}Full report saved:${N}  $logfile"
}

# ── Main Menu ──────────────────────────────────────────────────────────────────
banner() {
    clear
    echo -e "${C}"
    echo "  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗"
    echo "  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║"
    echo "  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║"
    echo "  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║"
    echo "  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║"
    echo "  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝"
    echo -e "${N}${W}  Recon Tool v1.0  —  OSINT & Reconnaissance${N}"
    echo -e "${R}  Only scan targets you own or have permission to test.${N}"
}

main_menu() {
    while true; do
        banner
        sep
        echo -e "  ${G}Target:${N}  ${W}${TARGET:-<not set>}${N}"
        sep
        echo -e "  ${Y}t${N}.  Set / Change Target"
        echo ""
        echo -e "  ${Y}1${N}.  WHOIS Lookup"
        echo -e "  ${Y}2${N}.  DNS Records (A/AAAA/MX/NS/TXT/SOA + DNSSEC)"
        echo -e "  ${Y}3${N}.  Subdomain Enumeration"
        echo -e "  ${Y}4${N}.  Port Scan"
        echo -e "  ${Y}5${N}.  HTTP Headers & Security Audit"
        echo -e "  ${Y}6${N}.  SSL/TLS Certificate Analysis"
        echo -e "  ${Y}7${N}.  IP Geolocation"
        echo -e "  ${Y}8${N}.  Full Recon (all modules)"
        sep
        echo -e "  ${Y}0${N}.  Exit"
        sep
        echo -ne "\n${C}Select option: ${N}"
        read -r choice

        case "$choice" in
            t|T)
                echo -ne "\n${C}Enter target (domain or IP): ${N}"
                read -r TARGET
                TARGET="${TARGET,,}"
                TARGET="${TARGET#http*://}"
                TARGET="${TARGET%%/*}" ;;
            1) check_target && run_whois;      echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            2) check_target && run_dns;        echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            3) check_target && run_subdomains; echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            4) check_target && run_portscan;   echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            5) check_target && run_http;       echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            6) check_target && run_ssl;        echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            7) check_target && run_geo;        echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            8) check_target && run_full;       echo -e "\n${Y}Press Enter to continue...${N}"; read -r ;;
            0) echo -e "\n${G}Goodbye.${N}\n"; exit 0 ;;
            *) echo -e "${R}Invalid option.${N}"; sleep 1 ;;
        esac
    done
}

# ── Entry ───────────────────────────────────────────────────────────────────────
TARGET="${1:-}"
trap 'echo -e "\n\n${Y}Interrupted.${N}\n"; exit 0' INT
main_menu
