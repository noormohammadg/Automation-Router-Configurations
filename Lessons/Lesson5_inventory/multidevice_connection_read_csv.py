import csv

try:
    # Read csv file
    with open('./Inventory/host.csv', "r") as f:
        reader = csv.DictReader(f)
        devices = list(reader)

    print(f"Total number of devices : {len(devices)}\n")
    for device in devices:
        print(f"host {device['host']}\n")
except Exception as e:
    print(e)
