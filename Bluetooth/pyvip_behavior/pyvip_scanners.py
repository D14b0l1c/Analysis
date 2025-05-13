import pandas as pd
from virtualitics import api

def load_and_plot(auth_token: str, csv_path: str) -> None:
    """
    Load scanner device data and create a 2D Map Plot in Virtualitics Explore.

    Parameters:
    - auth_token: pyVIP authentication token.
    - csv_path: Path to the scanners.csv file (output from bluetooth.py).
    """
    # Load data from CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    # Connect to Virtualitics
    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Bluetooth - Scanners")

    # Create 2D Map Plot
    vip.maps2d(
        x="avg_lon",
        y="avg_lat",
        color="bt_type"
    )

    print("2D Map Plot for Bluetooth - Scanners created.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    path = input("Enter full path to scanners.csv: ").strip()
    load_and_plot(auth_token=token, csv_path=path)