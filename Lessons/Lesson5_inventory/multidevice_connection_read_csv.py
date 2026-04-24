# WHAT THIS SCRIPT WILL DO
# 1. Reads device list from a CSV file
# 2. Connects to each device one by one
# 3. Run show commands on each device
# 4. Saves output to a separate file for each device
# 5. Show summary at end

import csv
import os
from datetime import datetime
from netmiko import ConnectHandler

# 1. Read devices from CSV file
def load_device_from_csv(filepath):
    netmiko_devices = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            device = {
               # 'name': row['name'],
                'host': row['host'],
                'device_type': row['device_type'],
                'username': row['username'],
                'password': row['password'],
                'secret': row['secret'],
                #'read_timeout': 30
            }
            netmiko_devices.append(device)
    return netmiko_devices



# 2.
os.makedirs(r"D:\Automaion Project\configs\backups", exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

success = []
failed = []
commands = ["show ip interface brief","show ip route"]

# Load devices from CSV
devices = load_device_from_csv(r"D:\Automaion Project\Inventory\host.csv")

print("=="*50)
print(f"Total devices loaded : ")
print(f"Timestamp : {timestamp}")
print("=="*50)

for device in devices:
    print("=="*50 + "\n")
    print(f"Device : {device['host']}")
    print("==" * 50 + "\n")

    try:

        with ConnectHandler(**device) as connection:
            connection.enable()
            print(f"Connectd prompt : {connection.find_prompt()}")

            # File to save output
            filename = rf"D:\Automaion Project\configs\backups\{device['host']}_{timestamp}.txt"
            with open(filename, "w") as f:
                f.write(f"Device  :{device['host']} \n")
                f.write(f"Time    : {timestamp}\n")
                f.write("=="*50 +"\n")

                for cmd in commands:
                    print(f"Running command : {cmd}")
                    output = connection.send_command(cmd)
                    f.write(f"Command : {cmd} \n")
                    f.write("=="*50 + "\n")
                    f.write(output +"\n\n")
            print(f"Output save to file : {filename}")
            success.append(device['host'])

    except Exception as e:
        error = e
        print(f"Error : {e}")
        failed.append(device['host'])

# Final summary
print("=="*50+"\n")
print("FINAL SUMMARY")
print("=="*50+"\n")



print(f"Total devices : {len(devices)}")
print(f"Success       : {len(success)}")
print("Success Device are :")
for device in success:
    print(f"{device}")


print("_"*60)
print(f"Failed        : {len(failed)}")
for device in failed:
    print(f"Failed to connect  : {device} , with Error {error}")
print("_"*60)
print("Script Completed!!!!!!")