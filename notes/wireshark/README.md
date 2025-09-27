# Wireshark Cheat Sheet

Wireshark is a powerful packet analyzer used for troubleshooting, analysis, and network security.  
Here are some useful filters and shortcuts.

---

## Display Filters

| Filter | Description |
|--------|-------------|
| `ip.addr == 192.168.1.1` | Show all traffic to/from the specified IP. |
| `ip.src == 192.168.1.1` | Show only packets **sent by** this IP. |
| `ip.dst == 192.168.1.1` | Show only packets **destined for** this IP. |
| `tcp.port == 80` | Show TCP traffic on port 80. |
| `udp.port == 53` | Show DNS traffic (UDP/53). |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Show SYN packets (TCP connection initiation). |
| `tcp.flags.fin == 1` | Show FIN packets (TCP connection termination). |
| `http` | Show only HTTP traffic. |
| `dns` | Show only DNS traffic. |
| `arp` | Show only ARP traffic. |
| `icmp` | Show only ICMP packets (ping, traceroute). |
| `tls` or `ssl` | Show TLS/SSL (HTTPS) traffic. |
| `tcp contains "login"` | Show TCP packets containing the string “login”. |
| `frame contains "password"` | Show packets containing the string “password”. |

---

## Capture Filters

*(defined before starting the capture — more efficient than display filters)*

| Filter | Description |
|--------|-------------|
| `host 192.168.1.1` | Capture all traffic to/from a specific host. |
| `net 192.168.1.0/24` | Capture traffic from an entire subnet. |
| `port 22` | Capture only traffic on port 22 (SSH). |
| `tcp` | Capture only TCP traffic. |
| `udp` | Capture only UDP traffic. |
| `icmp` | Capture only ICMP packets. |
| `src host 10.0.0.5` | Capture only traffic from a specific source. |
| `dst host 8.8.8.8` | Capture only traffic destined for a specific host. |
| `tcp portrange 1-1024` | Capture TCP traffic on ports 1–1024. |
| `not arp` | Capture everything except ARP packets. |

---

## Useful Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+E` | Start/stop capture. |
| `Ctrl+K` | Apply display filter. |
| `Ctrl+F` | Find within captured packets. |
| `Ctrl+H` | Show/hide packet details pane. |
| `Ctrl+Shift+P` | Open Wireshark preferences. |
| `Ctrl+=` / `Ctrl+-` | Zoom in / Zoom out. |
| `Ctrl+M` | Mark/unmark a packet. |
| `Ctrl+Shift+M` | Jump to the next marked packet. |
| `Ctrl+Alt+Shift+T` | Show time statistics. |

---

## Tips

- Use **display filters** for analysis after capture; use **capture filters** to limit what gets captured.  
- Combine filters, e.g. `ip.addr==192.168.1.1 && tcp.port==443`.  
- Export only relevant packets: *File → Export Specified Packets*.  
- For encrypted traffic (TLS/SSL), Wireshark can decrypt if you import the right keys.  

---
