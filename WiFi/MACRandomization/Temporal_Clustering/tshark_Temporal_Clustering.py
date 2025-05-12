# Temporal_Clustering_TShark.py

import subprocess
import pandas as pd
import os
from sklearn.cluster import DBSCAN
import numpy as np


def extract_timing_fields(pcap_file, output_csv="temporal_data.csv"):
    """
    Extracts MAC addresses and frame timestamps using TShark.

    Args:
        pcap_file (str): Path to the PCAP file.
        output_csv (str): Path to save extracted CSV.

    Returns:
        str: Path to the generated CSV.
    """
    fields = [
        "wlan.sa",    # Source MAC Address
        "frame.time_epoch"  # Packet Timestamp
    ]

    tshark_command = [
        "tshark",
        "-r", pcap_file,
        "-T", "fields"
    ]

    for field in fields:
        tshark_command += ["-e", field]

    tshark_command += ["-E", "separator=,"]

    with open(output_csv, "w") as f:
        subprocess.run(tshark_command, stdout=f, check=True)

    return output_csv


def build_temporal_profiles(csv_file):
    """
    Loads extracted CSV and builds temporal profiles per MAC address.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame with MAC addresses and timing features.
    """
    df = pd.read_csv(csv_file, header=None, names=["mac", "time"])
    df.dropna(subset=["mac", "time"], inplace=True)

    profiles = []

    for mac, group in df.groupby("mac"):
        times = group["time"].astype(float).sort_values().values
        if len(times) > 1:
            inter_arrival = np.diff(times)
            mean_gap = np.mean(inter_arrival)
            std_gap = np.std(inter_arrival)
            total_time = times[-1] - times[0]
        else:
            mean_gap = 0
            std_gap = 0
            total_time = 0

        profiles.append({
            "mac": mac.lower(),
            "mean_gap": mean_gap,
            "std_gap": std_gap,
            "total_time": total_time,
            "frame_count": len(times)
        })

    profile_df = pd.DataFrame(profiles)
    return profile_df


def cluster_by_temporal_patterns(df):
    """
    Clusters devices based on temporal behavior patterns.

    Args:
        df (pd.DataFrame): DataFrame with timing features.

    Returns:
        pd.DataFrame: DataFrame with cluster labels.
    """
    features = df[["mean_gap", "std_gap", "total_time", "frame_count"]].values
    clustering = DBSCAN(eps=5, min_samples=1).fit(features)
    df["cluster"] = clustering.labels_

    return df


def main(pcap_path):
    """
    Main function to execute Temporal Clustering pipeline.

    Args:
        pcap_path (str): Path to input PCAP file.
    """
    print("[+] Extracting timing fields with TShark...")
    csv_path = extract_timing_fields(pcap_path)

    print("[+] Building temporal profiles...")
    df = build_temporal_profiles(csv_path)

    print("[+] Clustering devices based on temporal patterns...")
    df_clustered = cluster_by_temporal_patterns(df)

    output_path = "temporal_clusters.csv"
    df_clustered.to_csv(output_path, index=False)
    print(f"[+] Done! Clustered data saved to {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python Temporal_Clustering_TShark.py <input.pcap>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    if not os.path.exists(pcap_file):
        print("[-] Input PCAP file does not exist.")
        sys.exit(1)

    main(pcap_file)