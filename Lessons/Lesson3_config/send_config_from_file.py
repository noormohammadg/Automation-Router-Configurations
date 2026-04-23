from datetime import datetime
import os
from netmiko import ConnectHandler

# SENDING CONFIGURATION METHOD 2 USING FILE

device = {
    'device_type':'cisco_ios',
    'host':'192.168.253.5',
    'username':'admin',
    'password':'admin',
    'secret':'admin'
}

# COMMANDS FILE PATH
config_file = "D:/Automaion Project/Lessons/Lesson3_config/commands.txt"

# OUTPUT FOLDER TO SAVE BEFORE AND AFTER CONFIGURATION FILES
os.makedirs("configs/backups", exist_ok=True)
timestamp = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
log_file = f"configs/backups/config_push_{device['host']}_{timestamp}.txt"

try:
    with ConnectHandler(**device) as connection:
        connection.enable()

        print("=="*50)
        print(f"Config Push --> {device['host']}")
        print(f"Time : {timestamp}")
        print("=="*50)

        print("Connected prompt : ", connection.find_prompt())

        # TAKING CURRENT RUNNING CONFIGURATION
        print("Backing up current running configuration......")
        before_config = connection.send_command("show running-config")
        before_config_backup = f"configs/backups/Before_{device['host']}_{timestamp}.txt"

        # PUSH BEFORE CONFIGURATION OUTPUT TO THE FILE
        with open(before_config_backup, "w") as f:
            f.write(before_config)
        print(f"Backup saved to : {before_config_backup}")

        # PUSHING CONFIGURATION FROM FILE
        print("Pushing configuration commands....")
        print(f"Loading config from file : {config_file}")
        config_output = connection.send_config_from_file(config_file)

        # SAVING CONFIGURATION
        print("Saving configuration to NVRAM.....")
        connection.save_config()

        # VERIFYING CHANGES
        print("\nVerifying Changes")
        verify = connection.send_command("show running-config | include description|ip route|", read_timeout=30)
        #print(verify)

        # SAVING LOG OF WHAT WAS PUSHED
        with open(log_file, "w") as f:
            f.write(f"Device : {device['host']}")
            f.write(f"Time   : {timestamp}")
            f.write("=="* 50 + "\n")
            f.write("COMMANDS PUSHED:\n")
            for cmd in config_file:
                f.write(f"{cmd}")
            f.write("\n"+"=="*50 + "\n")
            f.write("OUTPUT : \n")
            f.write(config_output)
        print("\n"+"=="*50+"\n")
        print("Config successfully pushed \n")
        print(f"Log saved : {log_file}")
        print(f"Backup : {before_config_backup}")

except Exception as e:
    print(e)
