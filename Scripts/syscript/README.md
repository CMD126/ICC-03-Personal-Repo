# Syscript: Ubuntu System Administration Toolkit

**Syscript** is a powerful, menu-driven shell script designed to simplify common system administration tasks on Ubuntu and other Debian-based distributions. It provides a comprehensive set of tools for system maintenance, package management, and information retrieval, all accessible through an easy-to-use interactive menu.Syscript is a collection of shell scripts for automating common system administration tasks on Ubuntu. The main script, `act.sh`, provides an interactive menu for performing updates, cleaning, package management, system info, and more.

## Overview

The core of Syscript is `act.sh`, a Bash script that automates a wide range of administrative functions. Whether you need to update your system, manage packages, monitor resource usage, or retrieve detailed system information, Syscript streamlines the process and makes it more efficient.

## Features

- **System Maintenance**: Keep your system up-to-date, clean, and optimized with options for updating, upgrading, and removing unnecessary packages.
- **Package Management**: Easily list, search, install, and remove packages without needing to remember complex `apt` commands.
- **Resource Monitoring**: Get a quick overview of disk and memory usage in a human-readable format.
- **In-Depth System Information**: Access detailed information about your system, hardware, kernel, network, and running processes.
- **User-Friendly Interface**: An interactive menu guides you through the available options, making it accessible for both new and experienced users.

## Getting Started

Follow these simple steps to get Syscript up and running on your system.

### Prerequisites

- An Ubuntu or Debian-based Linux distribution.
- The Bash (Bourne-Again SHell).
- `sudo` privileges for administrative actions.

### Installation and Usage

1.  **Navigate to the script directory**:
    ```bash
    cd Scripts/syscript
    ```

2.  **Make the script executable**:
    ```bash
    chmod +x act.sh
    ```

3.  **Run the script**:
    ```bash
    ./act.sh
    ```

You may be prompted for your password for actions that require `sudo` privileges.

## Menu Options Explained

Here is a detailed breakdown of each option available in the `act.sh` menu:

| Option | Description                                                                                                                              |
| :----- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| `1`    | **Update && full-upgrade**: Updates the package list and upgrades all installed packages to their latest versions.                     |
| `2`    | **Autoremove**: Removes packages that were automatically installed to satisfy dependencies for other packages and are no longer needed.  |
| `3`    | **Clean**: Clears out the local repository of retrieved package files.                                                                   |
| `4`    | **List upgradable packages**: Shows a list of all packages that have new versions available.                                            |
| `5`    | **List installed packages**: Displays all packages currently installed on the system.                                                   |
| `6`    | **Search package**: Searches for a package in the repositories. You will be prompted to enter the package name.                         |
| `7`    | **Install package**: Installs a new package. You will be prompted to enter the package name.                                            |
| `8`    | **Remove package**: Uninstalls a package from the system. You will be prompted to enter the package name.                               |
| `9`    | **Show disk usage**: Displays file system disk space usage in a human-readable format (`df -h`).                                       |
| `10`   | **Show memory usage**: Shows the amount of free and used memory in the system (`free -h`).                                                |
| `11`   | **Show system information**: Displays system information, including kernel name, version, and more (`uname -a`). |
| `12`   | **Show running processes**: Lists all currently running processes (`ps aux`).                                                           |
| `13`   | **Show network information**: Shows information about network interfaces (`ip a`).                                                      |
| `14`   | **Show open ports**: Lists all listening TCP and UDP ports (`ss -tuln`).                                                                |
| `15`   | **Show system logs**: Displays the latest entries from the system journal (`journalctl -xe`).                                             |
| `16`   | **Show user information**: Shows the current user's username (`whoami`).                                                                  |
| `17`   | **Show scheduled tasks**: Displays the current user's cron jobs (`crontab -l`).                                                         |
| `18`   | **Show hardware information**: Provides a summary of the system's hardware (`lshw -short`).                                             |
| `19`   | **Show kernel information**: Displays the kernel release version (`uname -r`).                                                          |
| `20`   | **Show environment variables**: Prints the current environment variables (`printenv`).                                                    |
| `21`   | **Show bash history**: Shows the command history for the current session (`history`).                                                   |
| `q`    | **Quit**: Exits the script.                                                                                                             |

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.

