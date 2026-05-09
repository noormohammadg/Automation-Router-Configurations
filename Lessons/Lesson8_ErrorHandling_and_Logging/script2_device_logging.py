# In this script we'll take device and connect it.
# Every single step of connection process is logged

import logging
from datetime import datetime
from netmiko import ConnectHandler
import os



#  Setup log file with today's date
today = datetime.now().strftime("%Y-%m-%d")
os.makedirs("logs", exist_ok=True)
log_file = f"logs/device_logging_{today}.log"

# Creat logger object
logger = logging.getLogger("DeviceLogger")
logger.setLevel(logging.DEBUG)

# Create date time formatter
formatter = logging.Formatter(
    fmt = "%(asctime)s %(levelname)s %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)

# Create File Handler
file_handler = logging.FileHandler(log_file,mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create Stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Connect both handler to logger, without this logger do not know where send the message
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Device Dictionary
device = {
    'device_type':'cisco_ios',
    'host':'192.168.253.5',
    'username':'admin',
    'password':'admin',
    'secret':'admin'
}

# Command list
commands = ["show version","show ip interface brief","show ip route"]


logger.info("=="*45)
logger.info("Scrip started")

logger.info(f"Device  : {device['host']}")
logger.info(f"Command count : {len(commands)}")
logger.info("=="*45)


# Main logic
try:
    logger.info(f'Connecting to {device['host']}....')

    with ConnectHandler(**device) as connection:
        logger.info(f"Connected to {device['host']}")
        connection.enable()
        connection.set_base_prompt()
        prompt = connection.find_prompt()
        logger.info(f"Device prompt is : {prompt}")

        # send commands to device
        for cmd in commands:
            logger.info(f"sending command {cmd}")
            output = connection.send_command(cmd, read_timeout=30)
            logger.info(f"successfully sended : {cmd} : command")

        logger.info("All commands completed")

    logger.info(f"Disconnected from device : {device['host']}")

except Exception as e:
    logger.error(f"Unexpected error : {e}")
finally:
    logger.info("Scrip completed")
    logger.info(f"log file save {log_file}")


