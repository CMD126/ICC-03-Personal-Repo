# Full Nmap Command Cheat Sheet

A comprehensive Nmap reference grouped by purpose. Use responsibly.

---

| Command | Description |
|---------|-------------|
| **Basic Scans** | |
| `nmap 192.168.1.1` | Simple scan of a single host. |
| `nmap 192.168.1.0/24` | Scan an entire subnet (CIDR). |
| `nmap -v target.com` | Verbose output during scan. |
| `nmap -vv target.com` | Very verbose (extra debugging/info). |
| **Host Discovery / Ping Options** | |
| `nmap -sn 192.168.1.0/24` | Ping scan (no port scan) — find live hosts. |
| `nmap -PS80,443 target.com` | TCP SYN ping to port(s) (host discovery). |
| `nmap -PA21,23,80 target.com` | TCP ACK/Connect-style host discovery. |
| `nmap -PE target.com` | ICMP echo request discovery. |
| `nmap -PP target.com` | ICMP timestamp request discovery. |
| **Scan Types (TCP/UDP/Other)** | |
| `nmap -sS target.com` | SYN (half-open) scan — stealthy, requires privileges. |
| `nmap -sT target.com` | TCP connect() scan — no raw sockets needed. |
| `nmap -sU target.com` | UDP scan (slow, useful for non-TCP services). |
| `nmap -sY target.com` | SCTP COOKIE-ECHO scan (for SCTP services). |
| `nmap -sN target.com` | TCP Null scan (no flags). |
| `nmap -sF target.com` | TCP FIN scan. |
| `nmap -sX target.com` | TCP Xmas scan (FIN/PSH/URG). |
| `nmap -sA target.com` | ACK scan — useful for firewall rule-mapping. |
| **Port Selection & Specifiers** | |
| `-p 22,80,443` | Specific ports. |
| `-p 1-1024` | Port range. |
| `-p-` | All ports (1-65535). |
| `--top-ports 100` | Scan the top N most common ports. |
| `--exclude 192.168.1.5` | Exclude specific host(s). |
| `--excludefile exclude.txt` | Exclude hosts listed in a file. |
| **Service & Version Detection** | |
| `nmap -sV target.com` | Service/version detection. |
| `nmap -sV --version-light target.com` | Faster/light version detection. |
| `nmap -sV --version-all target.com` | More thorough, slower version probing. |
| **OS Detection & Traceroute** | |
| `nmap -O target.com` | Try to detect OS (requires privileges). |
| `nmap --osscan-guess target.com` | Guess OS when detection is uncertain. |
| `nmap --traceroute target.com` | Run traceroute after scan. |
| **Nmap Scripting Engine (NSE)** | |
| `nmap --script=default target.com` | Run default scripts. |
| `nmap --script=vuln target.com` | Run vulnerability scripts. |
| `nmap --script "http-*" target.com` | Run script category or pattern. |
| `nmap --script-help http-title` | Show info about an NSE script. |
| `nmap --script-updatedb` | Update script database index. |
| `nmap --script-args 'user=admin,pass=123'` | Pass arguments to scripts. |
| **Output Options & Formats** | |
| `nmap -oN out.txt target.com` | Normal (human) output to file. |
| `nmap -oX out.xml target.com` | XML output. |
| `nmap -oG out.gnmap target.com` | Grepable output. |
| `nmap -oA basename target.com` | Save all three output formats (`basename.*`). |
| `nmap -v -oN verbose.txt target.com` | Verbose scanning with saved output. |
| **Timing & Performance** | |
| `-T0` … `-T5` | Timing templates (0 = slowest/stealthiest, 5 = fastest/noisiest). |
| `nmap -T4 -p- target.com` | Faster full-port scan (no extreme stealth). |
| `--max-retries 2` | Reduce retransmissions to speed up scan. |
| `--host-timeout 30m` | Set timeout for hosts. |
| **Firewall / Evasion Techniques** | |
| `nmap -f target.com` | Fragment packets to try to evade simple filters. |
| `nmap -D decoy1,decoy2,ME target.com` | Use decoys to obscure source. |
| `nmap --data-length 24 target.com` | Add random data to packets (change fingerprint). |
| `nmap --source-port 53 target.com` | Use a specific source port (bypass simple filters). |
| `nmap --ttl 64 target.com` | Set IP TTL for probes (fingerprint evasion). |
| `nmap -S 1.2.3.4 target.com` | Spoof source IP (requires special network setup). |
| **Advanced / Raw Packet Options** | |
| `--send-eth` | Send packets at Ethernet layer (requires raw access). |
| `--badsum` | Send packets with incorrect checksums (for research). |
| **Host/Target Selection & Randomization** | |
| `--randomize-hosts` | Randomize the order of targets. |
| `--min-parallelism N` | Minimum parallel probes. |
| `--max-hostgroup 256` | Set hostgroup size for parallelism. |
| **Scan Filters & Output Control** | |
| `--open` | Show only open (or possibly open) ports. |
| `--reason` | Show why Nmap thinks a port/state is in that state. |
| `--packet-trace` | Show sent and received packets (debugging). |
| `--iflist` | Show available interfaces and routing. |
| **UDP-specific Options** | |
| `nmap -sU -pU:53,161 target.com` | UDP scan for specific UDP ports. |
| `--top-ports 50 --open -sU target.com` | Fast top-ports UDP scan (careful, UDP is slow). |
| **Useful Combined Examples** | |
| `sudo nmap -sS -sV -O -p- -T4 -oA fullscan target.com` | SYN full-port + version + OS, save outputs. |
| `nmap -sU -sV --top-ports 200 -oA udp_top target.com` | UDP top ports + version detection. |
| `nmap -A -T3 --script vuln -oN vuln_report.txt target.com` | Aggressive discovery + vuln scripts (intrusive). |
| `nmap -Pn -p22,80 -sV --script=http-title -oN quick.txt target.com` | Skip discovery, version + http title on ports 22 & 80. |
| `nmap -sC -sV -oA scan_with_default_scripts target.com` | Run default scripts + service detection. |
| **Safety, Legal & Practical Notes** | |
| `NOTE` | Only scan systems you own or have explicit authorization to test. Many options are intrusive and can disrupt services. Some scans require `sudo`/root. NSE scripts vary from informational to intrusive — check script docs before use. IDS/IPS and firewalls will detect many evasive techniques; logs and legal consequences can follow. |
