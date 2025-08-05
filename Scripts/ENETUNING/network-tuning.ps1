# network-tuning.ps1
# © 2025 CMD126
# Licensed under the MIT License

# Requires -RunAsAdministrator

# Set the network adapter name (edit as needed)
$adapter = "Ethernet"  # e.g., "Wi-Fi", "Ethernet"

# Enable TCP Receive Window Auto-Tuning
netsh int tcp set global autotuninglevel=normal

# Enable TCP Chimney Offload
netsh int tcp set global chimney=enabled

# Enable Receive Side Scaling (RSS)
netsh int tcp set global rss=enabled

# Enable NetDMA
netsh int tcp set global netdma=enabled

# Enable ECN
netsh int tcp set global ecncapability=enabled

# Disable TCP Heuristics
netsh int tcp set heuristics disabled

# Set MTU to 1500 on the specified adapter
netsh interface ipv4 set subinterface $adapter mtu=1500 store=persistent

# Clear DNS resolver cache
ipconfig /flushdns

# Display current global TCP settings
netsh int tcp show global
