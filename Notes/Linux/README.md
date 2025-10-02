# Linux Command Cheat Sheet

A quick reference of commonly used Linux commands for file management, navigation, system monitoring, and more.

---

## File and Directory Management

| Command | Description |
|---------|-------------|
| **ls** | List all files and directories in the current directory. |
| **cd** | Change the current working directory. |
| **pwd** | Show the full path of the current directory. |
| **mkdir \<dir\>** | Create a new directory. |
| **touch \<file\>** | Create a new empty file or update the timestamp of an existing file. |
| **cp \<src\> \<dst\>** | Copy files or directories. |
| **mv \<src\> \<dst\>** | Move or rename files and directories. |
| **rm \<file\>** | Remove files. Use `rm -r` for directories. |
| **rmdir \<dir\>** | Remove an empty directory. |
| **tree** | Show directories and files in a tree-like structure. |

---

## File Viewing and Editing

| Command | Description |
|---------|-------------|
| **cat \<file\>** | Display the contents of a file. |
| **less \<file\>** | View a file one page at a time (scrollable). |
| **head \<file\>** | Show the first 10 lines of a file. |
| **tail \<file\>** | Show the last 10 lines of a file. |
| **nano \<file\>** | Open a simple terminal text editor. |
| **vim \<file\>** | Open a powerful text editor. |
| **wc \<file\>** | Count lines, words, and characters in a file. |

---

## Searching and Finding

| Command | Description |
|---------|-------------|
| **find \<dir\> -name \<file\>** | Search for a file or directory. |
| **grep "text" \<file\>** | Search for text inside a file. |
| **grep -r "text" \<dir\>** | Search text recursively in a directory. |
| **locate \<file\>** | Quickly find files by name (uses an index). |

---

## Permissions and Ownership

| Command | Description |
|---------|-------------|
| **chmod \<mode\> \<file\>** | Change file permissions. |
| **chown \<user\>:<group> \<file\>** | Change file owner and group. |
| **ls -l** | List files with detailed permissions and metadata. |

---

## System Information & Monitoring

| Command | Description |
|---------|-------------|
| **uname -a** | Show system information (kernel, architecture). |
| **whoami** | Show the current logged-in user. |
| **top** | Show running processes (dynamic view). |
| **htop** | Interactive process viewer (if installed). |
| **ps aux** | Show all running processes. |
| **df -h** | Show disk usage of mounted filesystems. |
| **du -sh \<dir\>** | Show disk usage of a directory. |
| **free -h** | Show memory (RAM) usage. |
| **uptime** | Show how long the system has been running. |

---

## Networking

| Command | Description |
|---------|-------------|
| **ping \<host\>** | Test connectivity to a host. |
| **curl \<url\>** | Fetch data from a URL. |
| **wget \<url\>** | Download files from the web. |
| **ifconfig** | Show network interfaces (deprecated, use `ip`). |
| **ip addr** | Show IP addresses and network info. |
| **netstat -tulnp** | Show active connections and listening ports. |
| **ss -tulnp** | Modern replacement for `netstat`. |

---

## Package Management (Debian/Ubuntu)

| Command | Description |
|---------|-------------|
| **apt update** | Update package list. |
| **apt upgrade** | Upgrade installed packages. |
| **apt install \<pkg\>** | Install a package. |
| **apt remove \<pkg\>** | Remove a package. |
| **dpkg -i \<pkg.deb\>** | Install a `.deb` package file. |

---

## Other Useful Commands

| Command | Description |
|---------|-------------|
| **echo "text"** | Output text to the terminal or a file (`echo "hi" > file.txt`). |
| **history** | Show command history. |
| **alias** | Create a shortcut for a command. |
| **clear** | Clear the terminal screen. |
| **shutdown -h now** | Shut down immediately. |
| **reboot** | Restart the system. |

---
