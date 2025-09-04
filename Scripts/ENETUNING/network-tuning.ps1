# network-tuning.ps1
# © 2025 CMD126
# Licensed under the MIT License

# --- Administrative Privileges Check ---
Write-Host "Checking for Administrator privileges..."
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Administrator privileges are required. Please re-run this script as an Administrator."
    # A small pause to ensure the user sees the message.
    Start-Sleep -Seconds 5
    exit 1
}
Write-Host "Successfully verified Administrator privileges." -ForegroundColor Green


# Requires -RunAsAdministrator

# --- Auto-detect Network Adapter ---
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
Write-Host "Applying TCP/IP optimizations..."

Write-Host " - Enabling TCP Receive Window Auto-Tuning..."
netsh int tcp set global autotuninglevel=normal

Write-Host " - Enabling TCP Chimney Offload..."
netsh int tcp set global chimney=enabled

Write-Host " - Enabling Receive Side Scaling (RSS)..."
netsh int tcp set global rss=enabled

Write-Host " - Enabling NetDMA..."
netsh int tcp set global netdma=enabled

Write-Host " - Enabling ECN Capability..."
netsh int tcp set global ecncapability=enabled

Write-Host " - Disabling TCP Heuristics..."
netsh int tcp set heuristics disabled

Write-Host " - Setting MTU to 1500 for adapter '$adapterName'..."
netsh interface ipv4 set subinterface "$adapterName" mtu=1500 store=persistent

# --- Finalizing ---
Write-Host "Clearing DNS resolver cache..."
ipconfig /flushdns

Write-Host "Displaying new global TCP settings:" -ForegroundColor Green
netsh int tcp show global

Write-Host "Network tuning script finished." -ForegroundColor Green
