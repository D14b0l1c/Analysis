import subprocess
import pandas as pd
from virtualitics import api

def detect_deauth(pcap_file: str, csv_output: str) -> pd.DataFrame:
    """
    Detect Deauthentication attacks using tshark and export summary to CSV.

    Args:
        pcap_file (str): Path to the PCAP file.
        csv_output (str): Path to save the results CSV.
    Returns:
        pd.DataFrame: Summarized detection results.
    """
    print("[*] Running tshark to detect deauth frames...")
    tshark_command = [
        "tshark", "-r", pcap_file, "-Y", "wlan.fc.type_subtype == 12",
        "-T", "fields", "-E", "separator=,", "-E", "quote=d", "-E", "header=y",
        "-e", "wlan.sa", "-e", "wlan.da", "-e", "wlan.bssid"
    ]
    result = subprocess.run(tshark_command, capture_output=True, text=True)

    data = [line.strip().split(",") for line in result.stdout.strip().split("\n") if line]
    df = pd.DataFrame(data, columns=["wlan.sa", "wlan.da", "wlan.bssid"])
    df["count"] = 1
    summary = df.groupby(["wlan.sa", "wlan.bssid"]).count().reset_index()
    summary["attack_type"] = "deauth"

    summary.to_csv(csv_output, index=False)
    print(f"[+] Deauth attack summary saved to {csv_output}")
    return summary

def visualize_deauth(auth_token: str, csv_path: str):
    """
    Load the deauth detection CSV into Virtualitics and generate a bar chart.
    """
    df = pd.read_csv(csv_path)
    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Wi-Fi Attack: Deauth")
    vip.bar(x="wlan.sa", y="count")
    print("Bar chart created for Deauth attack visualization.")

if __name__ == "__main__":
    import sys
    token = input("Paste your pyVIP auth token: ").strip()
    pcap_path = input("Enter path to .pcap file: ").strip()
    output_csv = "output/deauth_results.csv"
    df = detect_deauth(pcap_path, output_csv)
    visualize_deauth(token, output_csv)
