import pandas as pd
from virtualitics import api

def load_and_plot(auth_token: str, csv_path: str):
    """
    Load persistent device data and create a 2D Map Plot in Virtualitics Explore.

    Args:
        auth_token (str): pyVIP authentication token.
        csv_path (str): Full path to the persistent.csv file.
    """
    # Load CSV data
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Connect to Virtualitics
    vip = api.VIP(auth_token=auth_token)

    # Load data into Explore
    vip.load_data(data=df, dataset_name="Bluetooth - Persistent Devices")

    # Create a 2D Map Plot
    vip.maps2d(
        x="avg_lon",
        y="avg_lat",
        color="bt_type"
    )

    print("2D Map Plot for Bluetooth - Persistent Devices created.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    path = input("Enter full path to persistent.csv: ").strip()
    load_and_plot(auth_token=token, csv_path=path)