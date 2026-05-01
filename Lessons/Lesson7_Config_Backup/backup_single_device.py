# WHAT THIS SCRIPT DOES
# CONNECT TO ONE DEVICE AND SAVE ITS RUNNING CONFIGURATION TO A FILE
from multiprocessing.forkserver import connect_to_new_process

from netmiko import ConnectHandler
from datetime import datetime
import os


device = {
    'device_type': 'cisco_ios',
    'host': '192.168.253.5',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
}

today   = datetime.now().strftime('%Y-%m-%d')
timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

backup_folder = f"D:/Automaion Project/configs/backups/{today}"
os.mkdir(backup_folder)

try:
    print(f"Connecting to {device['host']}....")

    with ConnectHandler(**device) as connection:
        connection.enable()
        print(f"Connected : {connection.base_prompt}")

        #Send command retuns entire running config as string,
        #read_timeout=60 beacuse large configs takes time
        config = connection.send_command('show running-config',read_timeout=60)

        # Save config to a file
        filename = f"{backup_folder}/{device['host']}_{timestamp}.txt"

        # Open file and write output
        with open(filename,'w') as f:
            f.write(f"Backup of Device : {device['host']}\n")
            f.write(f"Date & Time      : {timestamp}\n")
            f.write("__"*60)
            f.write(config)
        print(f"Backup saved to : {filename}")
except Exception as e:
    print(f"Error : {e}")