# ABDNS: DNS Performance and Configuration Tool

ABDNS is a Python script that helps you find the fastest DNS server from a curated list of popular public DNS providers and automatically apply the settings to your system. It is designed to work on Linux, macOS, and Windows.

## Features

- **DNS Benchmark**: Pings a list of public DNS servers to measure their response times.
- **Automated Configuration**: Applies the selected DNS server to your system's network settings.
- **Cross-Platform**: Supports Linux, macOS, and Windows.

## Usage

To use ABDNS, run the script from your terminal:

```bash
python3 abdns.py
```

The script will first analyze the DNS servers and then prompt you to choose one to apply.

**Note**: You may need to run the script with administrative privileges (e.g., using `sudo`) to apply the DNS settings.