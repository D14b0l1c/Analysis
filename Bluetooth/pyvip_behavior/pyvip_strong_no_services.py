import pandas as pd
from virtualitics import api

def load_and_plot(auth_token: str, csv_path: str) -> None:
    """
    Load strong signal, no-service Bluetooth device data and create a 2D Map Plot.

    Args:
        auth_token (str): pyVIP authentication token.
        csv_path (str): Full path to the strong_no_services.csv file.
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Bluetooth - Strong No Services")

    vip.maps2d(
        x="avg_lon",
        y="avg_lat",
        color="bt_type"
    )

    print("2D Map Plot for Bluetooth - Strong No Services created.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    path = input("Enter full path to strong_no_services.csv: ").strip()
    load_and_plot(auth_token=token, csv_path=path)