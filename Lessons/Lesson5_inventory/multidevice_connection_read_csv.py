import netmiko


device = {
    'device_type': 'cisco_ios',
    'ip': '172.16.31.10',
    'username': 'admin',
    'password': 'admin',
    'secret':'admin'
}


with netmiko.Netmiko(**device) as ssh:
