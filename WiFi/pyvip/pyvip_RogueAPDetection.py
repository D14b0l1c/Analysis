import subprocess
import pandas as pd
from virtualitics import api

def detect_rogue_ap(pcap_file: str, csv_output: str, known_ssids_input: str) -> pd.DataFrame:
    """
    Detect Rogue Access Points by comparing observed SSIDs against a list of known SSIDs.

    Args:
        pcap_file (str): Path to the PCAP file.
        csv_output (str): Output path for results CSV.
        known_ssids_input (str): Comma-separated list of known SSIDs.
    Returns:
        pd.DataFrame: Access points labeled as known or rogue.
    """
    print("[*] Running tshark to extract beacon frames...")
    tshark_command = [
        "tshark", "-r", pcap_file, "-Y", "wlan.fc.type_subtype == 8",
        "-T", "fields", "-E", "separator=,", "-E", "quote=d", "-E", "header=y",
        "-e", "wlan.ssid", "-e", "wlan.bssid"
    ]
    result = subprocess.run(tshark_command, capture_output=True, text=True)

    data = [line.strip().split(",") for line in result.stdout.strip().split("\n") if line]
    df = pd.DataFrame(data, columns=["wlan.ssid", "wlan.bssid"]).dropna().drop_duplicates()

    known_ssids = [ssid.strip() for ssid in known_ssids_input.split(",") if ssid.strip()]
    df["whitelist"] = df["wlan.ssid"].isin(known_ssids)
    df["attack_type"] = df["whitelist"].apply(lambda x: "known_ap" if x else "rogue_ap")
    df["count"] = 1

    df.to_csv(csv_output, index=False)
    print(f"[+] Access Point listing saved to {csv_output}")
    return df

def visualize_rogue_ap(auth_token: str, csv_path: str):
    """
    Load Rogue AP detection CSV into Virtualitics and create a bar chart.
    """
    df = pd.read_csv(csv_path)
    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Wi-Fi Attack: Rogue AP")
    vip.bar(x="wlan.ssid", y="wlan.bssid")
    print("Bar chart created for Rogue AP attack visualization.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    pcap_path = input("Enter path to .pcap file: ").strip()
    known_ssids = input("Enter known SSIDs (comma-separated): ").strip()
    output_csv = "output/rogue_ap_results.csv"
    df = detect_rogue_ap(pcap_path, output_csv, known_ssids)
    visualize_rogue_ap(token, output_csv)
