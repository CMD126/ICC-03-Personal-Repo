# NMATRIX - Matrix Nmap Scanner

NMATRIX is a shell script that provides a user-friendly, menu-driven interface for the powerful `nmap` network scanner. It enhances the experience with a "digital rain" animation inspired by The Matrix, making network scanning a bit more fun.

## Features

*   **Interactive Menu:** An easy-to-use menu to select from various scan types.
*   **Matrix Animation:** A cool "digital rain" animation that runs before the menu is displayed.
*   **Multiple Scan Options:**
    *   Quick TCP Scan (Top 100 ports)
    *   Detailed TCP Scan (All ports with service version detection)
    *   UDP Scan (Top 100 ports)
    *   Ping Scan (to discover live hosts on a network)
*   **Input Validation:** Basic checks to ensure a host or network is provided.
*   **Prerequisite Check:** Verifies if `nmap` is installed before running.

## Prerequisites

Before running NMATRIX, you need to have `nmap` installed on your system. You can install it on Debian-based systems (like Ubuntu) using the following command:

```bash
sudo apt-get update
sudo apt-get install nmap
```

## Usage

1.  **Navigate to the script directory:**
    ```bash
    cd Scripts/NMATRIX
    ```

2.  **Make the script executable:**
    ```bash
    chmod +x nmatrix.sh
    ```

3.  **Run the script:**
    ```bash
    ./nmatrix.sh
    ```
    *Note: The script uses `sudo` for some `nmap` commands, so you may be prompted for your password.*

## Scan Options

The script provides the following scan options:

1.  **Quick TCP Scan:** Performs a fast SYN scan (`-sS`) on the top 100 most common TCP ports.
2.  **Detailed TCP Scan:** A more thorough SYN scan (`-sS`) that checks all 65,535 TCP ports and attempts to identify the version of the services running (`-sV`).
3.  **UDP Scan:** Scans the top 100 most common UDP ports (`-sU`). This type of scan is generally slower than TCP scans.
4.  **Ping Scan:** Discovers which hosts are active on a given network (`-sn`) without performing any port scans.
5.  **Exit:** Exits the NMATRIX script.