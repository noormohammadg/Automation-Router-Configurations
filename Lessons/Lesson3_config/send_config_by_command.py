from netmiko import ConnectHandler

# SENDING CONFIGURATION METHOD 1 USING LIST OF COMMAND

device = {
    'device_type':'cisco_ios',
    'host':'192.168.253.5',
    'username':'admin',
    'password':'admin',
    'secret':'admin'
}
config_commands = ['interface fa1/0','description LAN','ip address 192.168.1.1 255.255.255.0','no shutdown']
try:
    with ConnectHandler(**device) as connection:
        connection.enable()
        before_result = connection.send_command('show ip interface brief')
        print(f"\n ====== Before configuration ======\n {before_result}")
        print("="*70)
        #Applying configuration
        connection.send_config_set(config_commands)
        connection.save_config()
        after_result = connection.send_command('show ip interface brief', read_timeout=30)
        print(f"\n ====== After configuration ======\n\n\n {after_result}")
        print("=" * 70)

        if "192.168.1.1" in after_result:
            print("Configuration Successful")
        else:
            print("Configuration Failed")
except Exception as e:
    print(e)