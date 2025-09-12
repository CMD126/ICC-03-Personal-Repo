# network-tuning.ps1
# © 2025 CMD126
# Licensed under the MIT License
#
# This script applies various network optimizations to a Windows host
# to improve throughput, reduce latency, and enhance connection stability.

# --- Administrative Privileges Check ---
# This section ensures the script is run with elevated (Administrator) privileges,
# as modifying network settings requires them.
Write-Host "Checking for Administrator privileges..."
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Administrator privileges are required. Please re-run this script as an Administrator."
    # A small pause to ensure the user sees the message before the window closes.
    Start-Sleep -Seconds 5
    exit 1
}
Write-Host "Successfully verified Administrator privileges." -ForegroundColor Green

# --- Auto-detect Active Network Adapter ---
# This section identifies the primary physical network adapter that is currently active ('Up').
# This avoids applying settings to disconnected or virtual adapters.
Write-Host "Detecting active network adapter..."
$adapter = Get-NetAdapter -Physical | Where-Object { $_.Status -eq 'Up' } | Select-Object -First 1
if ($null -eq $adapter) {
    Write-Warning "No active physical network adapter found with 'Up' status. Exiting."
    Start-Sleep -Seconds 5
    exit 1
}
$adapterName = $adapter.Name
Write-Host "Found active adapter: '$adapterName'" -ForegroundColor Green

# --- Applying TCP/IP Optimizations ---
# The following commands use `netsh` (Network Shell) to modify system-wide TCP settings.
Write-Host "Applying TCP/IP optimizations..."

# Enables TCP Receive Window Auto-Tuning to 'normal'.
# This allows the OS to adjust the receive buffer size dynamically, which is crucial for high-speed networks.
Write-Host " - Enabling TCP Receive Window Auto-Tuning..."
netsh int tcp set global autotuninglevel=normal

# Enables TCP Chimney Offload.
# This offloads TCP/IP processing from the CPU to the network adapter, freeing up CPU resources.
Write-Host " - Enabling TCP Chimney Offload..."
netsh int tcp set global chimney=enabled

# Enables Receive Side Scaling (RSS).
# RSS distributes the processing of network traffic across multiple CPU cores, preventing bottlenecks.
Write-Host " - Enabling Receive Side Scaling (RSS)..."
netsh int tcp set global rss=enabled

# Enables NetDMA (Direct Memory Access).
# This allows the network adapter to transfer data directly to memory without CPU involvement.
Write-Host " - Enabling NetDMA..."
netsh int tcp set global netdma=enabled

# Enables ECN (Explicit Congestion Notification).
# ECN helps manage network congestion more efficiently without dropping packets, improving throughput.
Write-Host " - Enabling ECN Capability..."
netsh int tcp set global ecncapability=enabled

# Disables TCP Heuristics.
# This prevents Windows from automatically modifying TCP settings in response to certain network conditions,
# which can sometimes lead to performance degradation.
Write-Host " - Disabling TCP Heuristics..."
netsh int tcp set heuristics disabled

# Sets the MTU (Maximum Transmission Unit) to 1500 for the detected adapter.
# 1500 is the standard MTU for Ethernet and ensures compatibility and optimal packet size.
Write-Host " - Setting MTU to 1500 for adapter '$adapterName'..."
netsh interface ipv4 set subinterface "$adapterName" mtu=1500 store=persistent

# --- Finalizing ---
# These final steps help apply the changes and provide feedback to the user.

# Clears the local DNS resolver cache.
# This removes outdated or incorrect DNS entries.
Write-Host "Clearing DNS resolver cache..."
ipconfig /flushdns

# Displays the newly configured global TCP settings for verification.
Write-Host "Displaying new global TCP settings:" -ForegroundColor Green
netsh int tcp show global

Write-Host "Network tuning script finished successfully." -ForegroundColor Green
