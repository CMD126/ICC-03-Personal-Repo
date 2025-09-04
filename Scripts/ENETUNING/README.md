# ENETUNING

This directory contains scripts focused on network tuning and optimization for Windows systems.

## Purpose

The main goal is to enhance and stabilize internet performance on Windows hosts, particularly when operating multiple virtual machines or performing bandwidth-intensive tasks (e.g., ethical hacking labs, traffic analysis, automated updates).

## Script: `network-tuning.ps1`

### Description

The PowerShell script `network-tuning.ps1` applies low-level TCP/IP and network interface optimizations on Windows. These changes aim to:

- Improve download/upload speed
- Increase connection stability
- Reduce latency and bottlenecks
- Ensure consistent throughput for virtual environments (VMs)

### Key Features

The script:

- **Auto-detects** the primary active network adapter.
- Checks for **Administrator privileges** before running.
- Provides **real-time feedback** as it applies each optimization.
- Enables TCP Receive Window Auto-Tuning (`autotuninglevel=normal`).
- Enables TCP Chimney Offload.
- Enables Receive Side Scaling (RSS).
- Enables NetDMA (Direct Memory Access).
- Enables ECN (Explicit Congestion Notification).
- Disables TCP Heuristics.
- Sets the MTU to `1500` on the detected network adapter.
- Clears the DNS resolver cache.
- Displays the final global TCP settings.

### Requirements

- Windows 10/11 or Windows Server
- PowerShell 5.0 or higher
- Administrator privileges

### Usage

Run in an elevated PowerShell terminal:

.\network-tuning.ps1

> The script will automatically detect your primary active network adapter.

### Reverting Changes

To manually revert the applied tuning settings:

netsh int tcp set global autotuninglevel=restricted
netsh int tcp set global chimney=default
netsh int tcp set global rss=default
netsh int tcp set global netdma=default
netsh int tcp set global ecncapability=default
netsh int tcp set heuristics enabled


## License

This project is licensed under the MIT License — © 2025 CMD126



