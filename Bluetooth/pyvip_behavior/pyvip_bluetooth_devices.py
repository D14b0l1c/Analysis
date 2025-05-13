import pandas as pd
from virtualitics import api

def load_bluetooth_csv_to_virtualitics(auth_token: str, csv_path: str):
    """
    Load the bluetooth_devices.csv file into Virtualitics Explore using pyVIP.

    Args:
        auth_token (str): Your pyVIP authentication token.
        csv_path (str): Full path to the bluetooth_devices.csv file.
    """
    df = pd.read_csv(csv_path)

    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Bluetooth Devices Export")
    print("Data loaded into Virtualitics Explore.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    path = input("Enter full path to bluetooth_devices.csv: ").strip()
    load_bluetooth_csv_to_virtualitics(auth_token=token, csv_path=path)