# Show version gives lots of information in raw form
# TextFSM parse it into clean fields

from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'host': '192.168.253.5',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
}

with ConnectHandler(**device) as connection:
    connection.enable()
    version_data = connection.send_command('show version',use_textfsm=True)

    info = version_data[0]

    print("=="*60)
    print("Device Information")
    print("=="*60)
    print(f"Hostname    : {info['hostname']}")
    print(f"Ios version : {info['version']}")
    print(f"Serial number : {info['serial']}")
    print(f"Up time      : {info['uptime']}")
    print("=="*60)

