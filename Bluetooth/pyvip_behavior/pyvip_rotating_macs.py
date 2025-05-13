import pandas as pd
from virtualitics import api

def load_and_plot(auth_token: str, csv_path: str) -> None:
    """
    Load MAC rotation data and create a bar chart in Virtualitics Explore.

    Args:
        auth_token (str): pyVIP authentication token.
        csv_path (str): Full path to the rotating_macs.csv file.
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to load CSV: {e}")
        return

    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Bluetooth - Rotating MACs")

    vip.bar(
        x="vendor_prefix",
        y="unique_macs"
    )

    print("Bar chart for Bluetooth - Rotating MACs created.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    path = input("Enter full path to rotating_macs.csv: ").strip()
    load_and_plot(auth_token=token, csv_path=path)