# WHAT THIS SCRIPT DOES:
# Compares Today's backup with yesterday's backup & show exactly what changes happend

# This is very useful to kow:
# - Did someone make changes to device?
# - what exactly changed?

# difflib - It is a python library, it compares two texts and show the difference

import difflib

from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.253.5",
    "username": "admin",
    "password": "admin",
    "secret": "admin",
}

connection = ConnectHandler(**device)
connection.enable()

running_config = connection.send_command("show running-config")

NewFileConfi = f"D:/Automaion Project/Lessons/Lesson4_multidevice/config/backup/{device['host']}_new.txt"
with open(NewFileConfi, "w") as f:
    f.write(f"Device  : {device['host']}\n")
    f.write(running_config)


filename1 = "D:/Automaion Project/Lessons/Lesson4_multidevice/config/backup/192.168.253.5_2026-04-22_21-26-26.txt"
filename2 = NewFileConfi
with open(filename1, "r") as f:
    oldfile = f.readlines()

with open(filename2, "r") as f:
    newfile = f.readlines()


diff = difflib.unified_diff(oldfile,newfile,fromfile="oldFile",tofile = "newFile")
for lines in diff:
    if lines.startswith("-"):
        print(f"Old file configuration : {lines}")

    elif lines.startswith("+"):
        print(f"New file configuration : {lines}")










