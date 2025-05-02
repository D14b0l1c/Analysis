import subprocess
import pandas as pd
from virtualitics import api

def detect_eapol_replay(pcap_file: str, csv_output: str) -> pd.DataFrame:
    """
    Detect EAPOL replay attacks and export summary to CSV.

    Args:
        pcap_file (str): Path to the PCAP file.
        csv_output (str): Path to save the results CSV.
    Returns:
        pd.DataFrame: Summarized detection results.
    """
    print("[*] Running tshark to extract EAPOL frames...")
    tshark_command = [
        "tshark", "-r", pcap_file, "-Y", "eapol", "-T", "fields",
        "-E", "separator=,", "-E", "quote=d", "-E", "header=y",
        "-e", "wlan.sa", "-e", "frame.time_relative"
    ]
    result = subprocess.run(tshark_command, capture_output=True, text=True)

    data = [line.strip().split(",") for line in result.stdout.strip().split("\n") if line]
    df = pd.DataFrame(data, columns=["wlan.sa", "frame.time_relative"])
    df["frame.time_relative"] = pd.to_numeric(df["frame.time_relative"], errors="coerce")

    # Count number of EAPOL frames per MAC as a simple indicator
    df["count"] = 1
    summary = df.groupby("wlan.sa")["count"].sum().reset_index()
    summary["attack_type"] = "eapol_replay"

    summary.to_csv(csv_output, index=False)
    print(f"[+] EAPOL replay summary saved to {csv_output}")
    return summary

def visualize_eapol(auth_token: str, csv_path: str):
    """
    Load the EAPOL replay CSV into Virtualitics and generate a bar chart.
    """
    df = pd.read_csv(csv_path)
    vip = api.VIP(auth_token=auth_token)
    vip.load_data(data=df, dataset_name="Wi-Fi Attack: EAPOL Replay")
    vip.bar(x="wlan.sa", y="count")
    print("Bar chart created for EAPOL replay attack visualization.")

if __name__ == "__main__":
    token = input("Paste your pyVIP auth token: ").strip()
    pcap_path = input("Enter path to .pcap file: ").strip()
    output_csv = "output/eapol_replay_results.csv"
    df = detect_eapol_replay(pcap_path, output_csv)
    visualize_eapol(token, output_csv)
