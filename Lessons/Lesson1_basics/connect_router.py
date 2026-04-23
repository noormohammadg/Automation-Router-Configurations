from itertools import count

from netmiko import ConnectHandler

#Defining device
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.253.5',
    'username':'admin',
    'secret':'admin',
    'password':'admin'
}

# connection and verification
try:
    print("="*60)
    print(f"connecting to {device['host']}")
    print("="*60)


    with ConnectHandler(**device) as connection:
        print("connected successfully")
        print(f"host     : {device['host']}")
        print(f"type     : {device['device_type']}")
        print(f"prompt   : {connection.find_prompt()}")
        print("="*60)

        output = connection.send_command("show ip interface brief")
        result = output.splitlines()
        for res in result:
            print(res)
            print("-"*60)

    print("Disconnected successfully")
except Exception as e:
    pass


