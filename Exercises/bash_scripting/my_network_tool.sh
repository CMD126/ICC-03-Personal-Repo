#!/bin/bash

# QUICK INTRO
#     __    __             __                                        __       
#    |  \  |  \           |  \                                      |  \      
#    | $$\ | $$  ______  _| $$_    __   __   __   ______    ______  | $$   __ 
#    | $$$\| $$ /      \|   $$ \  |  \ |  \ |  \ /      \  /      \ | $$  /  \
#    | $$$$\ $$|  $$$$$$\\$$$$$$  | $$ | $$ | $$|  $$$$$$\|  $$$$$$\| $$_/  $$
#    | $$\$$ $$| $$    $$ | $$ __ | $$ | $$ | $$| $$  | $$| $$   \$$| $$   $$ 
#    | $$ \$$$$| $$$$$$$$ | $$|  \| $$_/ $$_/ $$| $$__/ $$| $$      | $$$$$$\ 
#    | $$  \$$$ \$$     \  \$$  $$ \$$   $$   $$ \$$    $$| $$      | $$  \$$\
#     \$$   \$$  \$$$$$$$   \$$$$   \$$$$$\$$$$   \$$$$$$  \$$       \$$   \$$
#                                                                             
#                                                                             
#                                                                             
#           __           ________                    __                       
#          |  \         |        \                  |  \                      
#           \$$\         \$$$$$$$$______    ______  | $$                      
#            \$$\          | $$  /      \  /      \ | $$                      
#             >$$\         | $$ |  $$$$$$\|  $$$$$$\| $$                      
#            /  $$         | $$ | $$  | $$| $$  | $$| $$                      
#           /  $$          | $$ | $$__/ $$| $$__/ $$| $$                      
#          |  $$           | $$  \$$    $$ \$$    $$| $$                      
#           \$$             \$$   \$$$$$$   \$$$$$$  \$$                      
#                                                                             
#                                                                             
#########################################################################################
#In this project I use a script made for a task in my ICC.This project has an objective .
#Be fast and furious. Im goin call him TORETOOLFAMALYFIRST.

# While loop && Simple menu

while true; do

        	echo -e "\n"		
	echo "1) Check Network Interface Information"
        	echo -e "\n"		
    	echo "2) Ping a Host"
        	echo -e "\n"		
    	echo "3) Port Scan with Nmap"
        	echo -e "\n"		
    	echo "4) Display Routing Table"
        	echo -e "\n"		
    	echo "5) Traceroute to Host"
        	echo -e "\n"		
    	echo "6) Exit"
        	echo -e "\n"		
	read -p "Please select your option: " choice

# Condicions 	
#1 Network Interfaces	
	if [ "$choice" == "1" ]; then
        	echo -e "\n"		
        	echo "=== Network Interfaces ==="
		ifconfig
        	echo -e "\n"		
		echo -e "\n Choose another one"
#2 Ping Host
	elif [ "$choice" == "2" ]; then
        	echo -e "\n"		
		read -p "=== Enter host to ping: " host
        	echo -e  "\n=== Pinging $host ==="
        	ping -c 1 $host  &> /dev/null && echo success || echo fail
		echo -e "\n"	
		echo -e "\n Choose another one"
#3 Nmap Port Scan with grep open and awk
	elif [ "$choice" == "3" ]; then
        	echo -e "\n"		
		read -p "=== Enter your target to port scan: " host
		echo -e "\n=== NMAP portscan $host ==="
		nmap -p- $host | grep 'open' | awk '{print $1, $2}'
        	echo -e "\n"		
		echo -e "\n Choose another one"
#4 Routing Table
	elif [ "$choice" == "4" ]; then
        	echo -e "\n"		
		echo "=== Routing Table==="
        	echo -e "\n"		
		netstat -rn
        	echo -e "\n"		
		echo -e "\n Choose another one"
#5 Trace Route
	elif [ "$choice" == "5" ]; then
        	echo -e "\n"		
		read -p "=== Enter what you want to traceroute: " host
        	echo -e "\n"		
		echo "=== Discover route ==="
		echo -e "\n"		
		traceroute $host	
		echo -e "\n"		
		total_hops=`traceroute $host | tail -n 1 | cut -d " " -f 1 `
		echo -e "\n The host $host is $total_hops hops away"		
		echo -e "\n"		
		echo -e "\n Choose another one"
#6 EXIT
	elif [ "$choice" == "6" ]; then
        	echo -e "\n"		
		echo "=== Good Bye ==="; break
        	echo -e "\n"		
# Else
	else
        	echo -e "\n"		
		echo "ERROR: Invalid option!!!"
		echo -e "\n Choose a number between 1 and 6 :)"
	fi
#ICC-03 / BASH SCRIPT FUNDAMENTALS / Miguel Sousa / 08/09/2025 
done
