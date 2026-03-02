# syscript — v2.0

Menu-driven Bash toolkit for Ubuntu/Debian system administration.

---

## Features

| # | Option | Description |
|---|--------|-------------|
| 1 | Package Management | Install, remove, update, list packages via `apt` |
| 2 | System Information | Hostname, OS, kernel, uptime, CPU, RAM, disk |
| 3 | Network Information | IP addresses, active connections, open ports |
| 4 | Service Control | Start, stop, restart, check status of systemd services |
| 5 | Firewall Status | UFW rules, active/inactive state |
| 6 | System Health Dashboard | Live CPU, memory, disk, and top processes |

---

## Usage

```bash
chmod +x syscript_sysadmin.sh
./syscript_sysadmin.sh

# Some features require root:
sudo ./syscript_sysadmin.sh
```

---

## Requirements

| Tool | Used for |
|------|----------|
| `bash 4+` | Required |
| `apt` | Package management |
| `systemctl` | Service control |
| `ufw` | Firewall status |
| `ss` / `netstat` | Network connections |

---

→ [View source](../Scripts/syscript/) | [← Home](Home)
