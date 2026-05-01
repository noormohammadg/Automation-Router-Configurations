# WHAT THIS SCRIPT DOES
# READ ALL DEVICES FROM CSV FILE, CONNECT TO EACH DEVICE AND SAVE CONFIG TO SEPRATE FILE

import csv
from netmiko import ConnectHandler
import os
from datetime import datetime

# Function : load devices from CSV
# Returns two list - device credentials and device info

def load_device_from_csv(filepath):
    device_info = []
    meta_info = []

    with open(filepath,"r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            device = {
                "device_type": row["device_type"],
                "host": row["host"],
                "username": row["username"],
                "password": row["password"],
                "secret":row["secret"]
            }
            info = {
                "host": device["host"],
            }
            device_info.append(device)
            meta_info.append(info)
    return device_info, meta_info

today = datetime.now().strftime('%Y-%m-%d')
timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

backup_folder = f"D:/Automaion Project/configs/backups/{today}"
#os.mkdir(backup_folder)

# Track which device worked & which device failed
success_device = []
failed_device = []

# CSV File path
Csv_path = "D:/Automaion Project/Inventory/host.csv"

# Check csv file is exist or not
if not os.path.exists(Csv_path):
    print("CSV file not exist")
    exit()

# Calling function
devices, meta = load_device_from_csv(Csv_path)

print("=="*60)
print("Backup")
print(f"Devices  : {len(devices)}")
print(f"Time     : {timestamp}")
print("=="*60)

# Main Loop - backup every device one by one
# zip(devices, meta) - loop both lists at the same time
for devices, meta in zip(devices, meta):
    hostip = meta["host"]
    print("__"*60)
    print(f"Backing up  : {hostip}")
    print("__"*60)

    try:
        with ConnectHandler(**devices)as connection:
            connection.enable()
            print(f"Connected to {hostip} : {connection.find_prompt()}")
            print("Fetching full configuration.....")
            config_output = connection.send_command('show running-config',read_timeout=60)

            # Save to file
            filename = f"{backup_folder}/{hostip}.txt"

            # Open & write output to a file
            with open(filename, "w") as f:
                f.write(f"Device    :  {hostip}\n")
                f.write(f"Time      :  {timestamp}\n")
                f.write("=="*60 + "\n\n")
                f.write(config_output)
            print(f"File saved to : {filename}")
            success_device.append(hostip)

    except Exception as e:
        print(f"Error is : {e}")
        failed_device.append(hostip)

# Final summary
print("=="*60)
print("Backup job complete")
print("=="*60)
print(f"Successful devices : {len(success_device)}")
num = 1
for device in success_device:
    print(f"Device {num} : {device}")
    num = num + 1

print("--"*60)

count = 1
print(f"Failed devices : {len(failed_device)}")
for device in failed_device:
    print(f"Device {count} : {device}")
    count = count +1




