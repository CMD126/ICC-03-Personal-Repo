#!/bin/bash

while true; do

    clear
    cat<<EOF
    ==============================
    Syscript for Ubuntu
    ------------------------------
    Please enter your choice

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
    ------------------------------
EOF
    read -s
    case "$REPLY" in

# Update and full upgrade
    
    "1")
        echo "Your system will update after you put the password"
        sudo apt update && sudo apt full-upgrade -y
        echo "=== System up to date ===" ;;


# Autoremove unused packages

    "2")
        echo "Removing unused packages..."
        if sudo apt autoremove -y; then
            echo "=== Autoremove complete ==="
        else
            echo "Erro ao remover pacotes."
        fi ;;

 # Clean up

    "3")
        echo "Cleaning up..."
        sudo apt clean
        echo "=== Clean complete ===" ;;

# List upgradable packages
    "4")
        echo "Listing upgradable packages..."
        apt list --upgradable
        echo "=== List complete ===" ;;

# List installed packages
    "5")
        echo "Listing installed packages..."
        dpkg --get-selections
        echo "=== List complete ===" ;;

# Search for a package
    "6")
        read -p "Enter package name to search: " pkg
        echo "Searching for package '$pkg'..."
        apt search "$pkg"
        echo "=== Search complete ===" ;;

# Install a package
    "7")
        read -p "Enter package name to install: " pkg
        echo "Installing package '$pkg'..."
        sudo apt install "$pkg" -y
        echo "=== Install complete ===" ;;

# Remove a package
    "8")
        read -p "Enter package name to remove: " pkg
        echo "Removing package '$pkg'..."
        sudo apt remove "$pkg" -y
        echo "=== Remove complete ===" ;;

# Show disk usage
    "9")
        echo "Showing disk usage..."
        df -h
        echo "=== Disk usage complete ===" ;;

# Show memory usage
    "10")
        echo "Showing memory usage..."
        free -h
        echo "=== Memory usage complete ===" ;;

# Show system information
    "11")
        echo "Showing system information..."
        uname -a
        echo "=== System information complete ===" ;;

# Show running processes
    "12")
        echo "Showing running processes..."
        ps aux
        echo "=== Running processes complete ===" ;;

# Show network information
    "13")
        echo "Showing network information..."
        ip a
        echo "=== Network information complete ===" ;;

# Show open ports
    "14")
        echo "Showing open ports..."
        ss -tuln
        echo "=== Open ports complete ===" ;;

# Show system logs
    "15")
        echo "Showing system logs..."
        sudo journalctl -xe
        echo "=== System logs complete ===" ;;

# Show user information
    "16")
        echo "Showing user information..."
        whoami
        echo "=== User information complete ===" ;;

# Show scheduled tasks
    "17")
        echo "Showing scheduled tasks..."
        crontab -l  
        echo "=== Scheduled tasks complete ===" ;;

# Show hardware information
    "18")
        echo "Showing hardware information..."
        lshw -short
        echo "=== Hardware information complete ===" ;;

# Show kernel information
    "19")
        echo "Showing kernel information..."
        uname -r
        echo "=== Kernel information complete ===" ;;

# Show environment variables
    "20")
        echo "Showing environment variables..."
        printenv
        echo "=== Environment variables complete ===" ;;

# Show bash history
    "21")
        echo "Showing bash history..."
        history
        echo "=== Bash history complete ===" ;;   

    
# Quit
    
    "Q"|"q")
        echo "Exiting..."
        exit 0 ;;
# Invalid option

     * )
       echo "invalid option" ;;

    esac
        read -p "Pressione Enter para continuar..."
done
