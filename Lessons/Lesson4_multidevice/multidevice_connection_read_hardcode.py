import os

from netmiko import ConnectHandler
from datetime import datetime

from Lessons.Lesson3_config.send_config_from_file import timestamp

devices = [
{
    'device_type': 'cisco_ios',
    'host': '192.168.253.5',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin'
},
{
    'device_type':'cisco_ios',
    'host':'192.168.253.6',
    'username':'noor',
    'secret':'noor123',
    'password':'noor124'
},
{
     'device_type': 'cisco_ios',
    'host': '192.168.253.7',
    'username': 'noor1',
    'password': 'noor@123',
    'secret':'noor@123'
}
]

# Commands & Config
show_commands = ["show ip interface brief","show version"]
config_commands = ["logging buffered 10000","ntp server 8.8.8.8"]

# File setup
os.makedirs("config/backup", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Adding successfull and failed devices in list
success_devices = []
failed_devices =[]

print("=="*50)
print("Multi-Device Automation")
print(f"Device : {len(devices)}")
print(f"Time   : {timestamp}")
print("=="*50)

# Main code
# Looping through each and every device in devices list
for device in devices:
    host = device['host']
    print("_"*60)
    print(f"Processing : {host}")
    print("_" * 60)

    try:
        with ConnectHandler(**device) as connection:
            connection.enable()
            print(f"Connected to {host}, {connection.find_prompt()}")

            filename = f"config/backup/{host}_{timestamp}.txt"
            with open(filename,"w") as f:
                print(f"Device is  :{host}")
                print(f"Timestamp  : {timestamp}")
                print("=="*50)

                # Running show command
                print("Running show commands")
                for cmd in show_commands:
                    show_output = connection.send_command(cmd, read_timeout=30)
                    f.write(f"Command : {cmd}\n")
                    f.write("_"*50 + "\n")
                    f.write(show_output + "\n\n")

                # Pushing Config commands
                config_output = connection.send_config_set(config_commands, read_timeout=30)
                f.write("config Pushed" + "\n")
                f.write("_"*50 + "\n")
                f.write(config_output + "\n\n")

            # Save Config
            print(f"Config save to file :  {filename}")

            # Add device to success list
            success_devices.append(host)

    except Exception as e:
        print(f"error : {e}")
        failed_devices.append(host)

# Final summary
print("=="*50)
print("AUTOMATION COMPLETE - SUMMARY ")
print("=="*50)
print(f"Success : {len(success_devices)}")
for success in success_devices:
    print(f"--> {success}")
print(f"Failed : {len(failed_devices)}/{len(devices)} devices")




