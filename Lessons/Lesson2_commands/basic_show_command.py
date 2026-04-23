from netmiko import ConnectHandler
from datetime import datetime
import os

device = {
    'device_type':'cisco_ios',
    'host':'192.168.253.5',
    'username':'admin',
    'password':'admin',
    'secret':'admin'
}
#Commands to send =====================================================================
commands = ["show version","show ip interface brief","show ip route"]

#Generate File name with time stamp ===================================================
os.makedirs("configs/backups", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"configs/backups/show_output_{device['host']}_{timestamp}.txt"
#Main code ==============================================================================
try:
    print("="*60)
    print(f"Connecting to {device['host']}")
    print("="*60)
    with ConnectHandler(**device) as connection:
        connection.enable()
        print(f"Connected prompt {connection.find_prompt()}\n")
        result = {}
        for cmd in commands:
            print(f"Running:  {cmd}")
            result[cmd]=connection.send_command(cmd)
        print(f"All {len(commands)} commands collected!\n")
    #Save to File
    with open(filename,"w") as f:
        f.write(f"Device : {device['host']}\n")
        f.write(f"Time : {timestamp}\n")
        f.write("="*60 + "\n\n")

        for cmd, output in result.items():
            f.write(output + "\n\n")
    print(f"Output save to {filename}")
except Exception as e:
    print(e)

