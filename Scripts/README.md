
# Syscript

Syscript is a collection of shell scripts for automating common system administration tasks on Ubuntu. The main script, `act.sh`, provides an interactive menu for performing updates, cleaning, package management, system info, and more.

## Features

- Update and upgrade your system
- Remove unused packages and clean up
- List upgradable and installed packages
- Search, install, and remove packages
- Show disk and memory usage
- Display system, hardware, kernel, and user information
- View running processes, network info, open ports, and system logs
- Show scheduled tasks, environment variables, and bash history

## Menu Options (act.sh)

```
1) Update && full-upgrade
2) Autoremove
3) Clean
4) List upgradable packages
5) List installed packages
6) Search package
7) Install package
8) Remove package
9) Show disk usage
10) Show memory usage
11) Show system information
12) Show running processes
13) Show network information
14) Show open ports
15) Show system logs
16) Show user information
17) Show scheduled tasks
18) Show hardware information
19) Show kernel information
20) Show environment variables
21) Show bash history
q) Quit
```

## Usage

Make the script executable and run it:

```bash
chmod +x act.sh
./act.sh
```

You may be prompted for your password for certain administrative actions.

## Requirements

- Ubuntu or compatible Linux distribution
- Bash shell
- Some options require `sudo` privileges

