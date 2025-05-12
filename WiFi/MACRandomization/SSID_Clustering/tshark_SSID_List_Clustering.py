# SSID_List_Clustering_TShark.py

import subprocess
import pandas as pd
import os
import hashlib
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances


def extract_probe_requests(pcap_file, output_csv="probe_requests.csv"):
    """
    Extracts MAC addresses and SSIDs from Probe Request frames using TShark.

    Args:
        pcap_file (str): Path to the PCAP file.
        output_csv (str): Path to save extracted CSV.

    Returns:
        str: Path to the generated CSV.
    """
    fields = [
        "wlan.sa",    # Source MAC Address
        "wlan.ssid",  # SSID being probed
        "frame.time_epoch"
    ]

    tshark_command = [
        "tshark",
        "-r", pcap_file,
        "-Y", "wlan.fc.type_subtype == 4",
        "-T", "fields"
    ]

    for field in fields:
        tshark_command += ["-e", field]

    tshark_command += ["-E", "separator=,"]

    with open(output_csv, "w") as f:
        subprocess.run(tshark_command, stdout=f, check=True)

    return output_csv


def build_ssid_sets(csv_file):
    """
    Loads extracted CSV and groups SSIDs by MAC address.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame with MAC and set of SSIDs.
    """
    df = pd.read_csv(csv_file, header=None, names=["mac", "ssid", "time"])
    df.dropna(subset=["mac"], inplace=True)

    ssid_dict = {}

    for _, row in df.iterrows():
        mac = row["mac"].lower()
        ssid = row["ssid"]
        if mac not in ssid_dict:
            ssid_dict[mac] = set()
        if pd.notna(ssid) and ssid != "":
            ssid_dict[mac].add(ssid)

    mac_list = list(ssid_dict.keys())
    ssid_sets = list(ssid_dict.values())

    result_df = pd.DataFrame({"mac": mac_list, "ssid_set": ssid_sets})
    return result_df


def cluster_by_ssid(df):
    """
    Clusters devices based on Jaccard similarity of SSID sets.

    Args:
        df (pd.DataFrame): DataFrame with MACs and SSID sets.

    Returns:
        pd.DataFrame: DataFrame with cluster labels.
    """
    sets = df["ssid_set"].tolist()
    n = len(sets)
    distance_matrix = [[1 - jaccard_index(sets[i], sets[j]) for j in range(n)] for i in range(n)]

    clustering = DBSCAN(eps=0.5, min_samples=1, metric="precomputed").fit(distance_matrix)
    df["cluster"] = clustering.labels_

    return df


def jaccard_index(set1, set2):
    """
    Computes Jaccard similarity index between two sets.

    Args:
        set1 (set): First set.
        set2 (set): Second set.

    Returns:
        float: Jaccard similarity index.
    """
    if not set1 and not set2:
        return 1.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0


def main(pcap_path):
    """
    Main function to execute SSID clustering pipeline.

    Args:
        pcap_path (str): Path to input PCAP file.
    """
    print("[+] Extracting probe requests with TShark...")
    csv_path = extract_probe_requests(pcap_path)

    print("[+] Building SSID sets...")
    df = build_ssid_sets(csv_path)

    print("[+] Clustering devices based on SSID sets...")
    df_clustered = cluster_by_ssid(df)

    output_path = "ssid_list_clusters.csv"
    df_clustered.to_csv(output_path, index=False)
    print(f"[+] Done! Clustered data saved to {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python SSID_List_Clustering_TShark.py <input.pcap>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    if not os.path.exists(pcap_file):
        print("[-] Input PCAP file does not exist.")
        sys.exit(1)

    main(pcap_file)
