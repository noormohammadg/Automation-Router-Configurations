# This show diffrence between
# 1. Raw output
# 2. Parsed output

from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    'host':'192.168.253.5',
    'username': 'admin',
    'password': 'admin',
    'secret':'admin'
}

with ConnectHandler(**device) as connection:
    connection.enable()

    # Type 1: RAW Output6
    raw_output = connection.send_command('show ip interface brief')
    print(f"Type of output : {type(raw_output)}")
    print("_"*70)
    print(raw_output)
    print("_"*70)

    # Type 2: Parsed Output
    parsed_output = connection.send_command('show ip interface brief', use_textfsm=True)
    print(f"Type of output : {type(parsed_output)}")
    print("_" * 70)
    print(parsed_output)
    print("_" * 70)
