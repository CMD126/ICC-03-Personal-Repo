#!/usr/bin/python3

#Import Lib
import os

os.system("ls > list.txt")
os.system("whoami > user.txt")

# for loop in python$

for file in ["list.txt", "user.txt"] :
    with open(file, 'r') as f:
        output = f.read()
        print(f"\n Command output of {file} is : \n {output}")