

import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)


# Create log file with today's date
today = datetime.now().strftime("%Y-%m-%d")
log_file = f"logs/automation_{today}.log"


# Creat a logger object
logger = logging.getLogger("Networklogger")

# Set logger to Debug so that we get all messages
logger.setLevel(logging.INFO)


# Define the format of log lines
formatter = logging.Formatter(
    fmt = "%(asctime)s - %(levelname)s - %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)

# Create FileHandler to save log in file
file_handler = logging.FileHandler(log_file,mode="a")
# Set log level for file
file_handler.setLevel(logging.DEBUG)
# Set datetime format for file
file_handler.setFormatter(formatter)


# Create StreamHandler to print output on console
stream_handler = logging.StreamHandler()
# Set log level for console till info only on cosole will print
stream_handler.setLevel(logging.INFO)
# Set datetime format for console
stream_handler.setFormatter(formatter)


# Connect both handler to logger, without this logger do not know where send the message
logger.addHandler(file_handler)
logger.addHandler(stream_handler)



logger.info("iam info logger")
logger.info(f"log file save to location : {log_file}")

# This dbug will not print on console because on streamHandler we set log level to info
logger.debug("iam debug message")

