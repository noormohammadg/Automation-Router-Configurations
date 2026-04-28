from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.253.5",
    "username": "admin",
    "password": "admin",
    "secret": "admin"
}

with ConnectHandler(**device) as connection:
    connection.enable()
    output = connection.send_command('show ip int brief', use_textfsm=True)

    up_interface = []
    down_interface = []

    # Now loop through each interface in a list
    for interface in output:
        interface_name = interface['interface']
        interface_ip = interface['ip_address']
        interface_status = interface['status']

        print(f"Interface : {interface_name}, Ip : {interface_ip}, Status: {interface_status}")

        if(interface_status == "up"):
            up_interface.append(interface_name)
        else:
            down_interface.append(interface_name)

    print(f"UP interface : {up_interface}")
    if down_interface == []:
        print(f"DOWN interface : 0")




