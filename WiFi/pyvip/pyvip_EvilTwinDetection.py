import subprocess
import pandas as pd
from virtualitics import api

def detect_evil_twin(pcap_file: str, csv_output: str) -> pd.DataFrame:
    """
    Detect Evil Twin attacks based on multiple BSSIDs per SSID.

    Args:
        pcap_file (str): Path to the PCAP file.
        csv_output (str): Path to save the results CSV.
    Returns:
        pd.DataFrame: Summarized detection results.
    """
    print("[*] Running tshark to extract beacon/probe frames...")
    tshark_command = [
        "tshark", "-r", pcap_file,
        "-Y", "(wlan.fc.type_subtype == 8 or wlan.fc.type_subtype == 5)",  # beacon or probe response
        "-T", "fields", "-E", "separator=,", "-E", "quote=d", "-E", "header=y",
        "-e", "wlan.ssid", "-e", "wlan.bssid"
    ]
    result = subprocess.run(tshark_command, capture_output=True, text=True)

    data = [line.strip().split(",") for line in result.stdout.strip().split("\n") if line]
    df = pd.DataFrame(data, columns=["wlan.ssid", "wlan.bssid"])

    # Drop empty SSIDs (hidden)
    df = df[df["wlan.ssid"] != ""]

    # Count BSSIDs per SSID
    unique_bssids = df.drop_duplicates().groupby("wlan.ssid").count().reset_index()
    unique_bssids.rename(columns={"wlan.bssid": "bssid_count"}, inplace=True)
    unique_bssids["attack_type"] = "evil_twin"

    unique_bssids.to_csv(csv_output, index=False)
    print(f"[+] Evil Twin summary saved to {csv_output}")
    return unique_bssids

def visualize_evil_twin(auth_token: str, csv_path: str):
    """
    Load Evil Twin detection CSV into Virtualitics and create a bar chart.
    """
    df = pd.read_csv(csv_path)
    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Wi-Fi Attack: Evil Twin")
    vip.bar(x="wlan.ssid", y="bssid_count")
    print("Bar chart created for Evil Twin attack visualization.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    pcap_path = input("Enter path to .pcap file: ").strip()
    output_csv = "output/evil_twin_results.csv"
    df = detect_evil_twin(pcap_path, output_csv)
    visualize_evil_twin(token, output_csv)
