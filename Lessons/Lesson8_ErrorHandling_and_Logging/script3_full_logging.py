# What this script will do
# It is full script it combines:
# Read devices from csv file
# Loop through all devices
# Full logging on every step
import logging
import os
from netmiko import ConnectHandler
from datetime import datetime
import csv

# Function 1 : setup_logger()
def setup_logger():

    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("logs",exist_ok=True)
    log_file = f"logs/full_logging_{today}.log"

    logger = logging.getLogger("DeviceAutomation")
    logger.setLevel(logging.DEBUG)


    formatter = logging.Formatter(
        fmt = "%(asctime)s %(levelname)s %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(log_file,mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger, log_file

# Function 2 : load_device_from_csv()
def load_device_from_csv(filepath,logger):

    logger.info(f"Loading device from {filepath}")

    # Check if file exist or not
    if not os.path.exists(filepath):
        logger.critical(f"CSV file not found : {filepath}")
        logger.critical("Can not continue because no device found")
        return [],[]

    # Empty list to store readed csv devices
    netmiko_device = []
    try:
        with open(filepath,"r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                netmiko_device.append({
                    'device_type':row['device_type'],
                    'host':row['host'],
                    'username':row['username'],
                    'password':row['password'],
                    'secret':row['secret']
                })

                logger.debug(f"Loaded Device : {row['host']}")

        logger.info(f"Total device loaded : {len(netmiko_device)}")
    except Exception as e:
        logger.error(f"Error in reading csv file {e}")

    return netmiko_device

# Function 3 : process_device() ---> we connect device, run commands
def process_device(device, commands, logger):

    logger.info(f"Processing device : {device}")
    try:
        logger.info(f"Opening SSH connection to {device['host']}")
        # Connecting to device
        with ConnectHandler(**device) as connection:
            logger.info(f"SSH conncted successfully : {device['host']}")
            connection.enable()
            connection.set_base_prompt()
            prompt = connection.find_prompt()
            logger.debug(f"Prompt : {prompt}")

            # Run commands
            for cmd in commands:
                logger.debug(f"Sending command : '{cmd}'")
                connection.send_command(cmd)
                logger.info(f"command ' {cmd} ' : executed successfully")
            logger.info("All commands successfully")
        return True

    except Exception as e:
        logger.error(f"Some Error found : {e}")
        return False

# Main script

# Calling Function1: setup_logger()
logger, log_file = setup_logger()

# Commands
command = ['show version','show ip interface brief','show ip route']

# CSV path
CSV_path = "D:/Automaion Project/Inventory/host.csv"

# log scrip starts
logger.info("============Script started==============")
logger.info(f"logfile   : {log_file}")
logger.info(f"CSV file  : {CSV_path}")
logger.info(f"Commands : {len(command)}")

# Calling Function2: load_device_from_csv()
devices = load_device_from_csv(CSV_path, logger)

success = []
failed = []
for device in devices:
    # Calling Function3: process_device()--> returns True or False
    result = process_device(device,command,logger)
    if result == True:
        success.append(device['host'])
    else:
        failed.append(device['host'])

logger.info("Automation finished")
logger.info(f"Total processed devices : {len(devices)}")
logger.info(f"Successfull Devices : {len(success)}")

for host in success:
    logger.info(f"successfully connected to : {host}")

for host in failed:
    logger.info(f"Failed to connected to : {host}")

logger.info(f"logger file saved to : {log_file}")