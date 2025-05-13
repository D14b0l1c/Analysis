import pandas as pd
from virtualitics import api

def load_and_plot(auth_token: str, csv_path: str) -> None:
    """
    Load Bluetooth devices broadcasting rich services and create a 2D Map Plot in Virtualitics Explore.

    Args:
        auth_token (str): pyVIP authentication token.
        csv_path (str): Full path to the rich_services.csv file.
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to load CSV: {e}")
        return

    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Bluetooth - Rich Services")

    vip.maps2d(
        x="avg_lon",
        y="avg_lat",
        color="bt_type"
    )

    print("2D Map Plot for Bluetooth - Rich Services created.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    path = input("Enter full path to rich_services.csv: ").strip()
    load_and_plot(auth_token=token, csv_path=path)