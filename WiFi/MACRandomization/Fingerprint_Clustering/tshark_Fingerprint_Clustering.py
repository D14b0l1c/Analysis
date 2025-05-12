import subprocess
import hashlib
from collections import defaultdict
import pandas as pd
import sys

fields = [
    "wlan.sa",  # Source MAC (must be first for grouping)
    # Stable fingerprint fields only
    "wlan.ssid",
    "wlan.supported_rates",
    "wlan.extended_supported_rates",
    "wlan.rsn.version",
    "wlan.rsn.akms",
    "wlan.rsn.capabilities",
    "wlan.ht.capabilities",
    "wlan.vht.capabilities",
    "wlan.tag.vendor.data"
]

def extract_tshark_fields(pcap_file):
    """
    Extracts MAC and stable fingerprint fields using TShark.
    """
    cmd = ["tshark", "-r", pcap_file, "-Y", "wlan.fc.type_subtype == 4", "-T", "fields"]
    for field in fields:
        cmd.extend(["-e", field])

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Error running TShark:\n", result.stderr)
        sys.exit(1)

    records = []
    for line in result.stdout.strip().split('\n'):
        parts = line.split('\t')
        if not parts or len(parts) < 2:
            continue
        mac = parts[0]
        blob = ''.join(parts[1:])
        records.append((mac, blob))

    return records

def cluster_by_fingerprint(records):
    """
    Groups MACs based on fingerprint hash of stable TShark field blob and writes to CSV.
    """
    fingerprints = defaultdict(list)
    for mac, blob in records:
        fingerprint = hashlib.md5(blob.encode()).hexdigest()
        if mac not in fingerprints[fingerprint]:
            fingerprints[fingerprint].append(mac)

    cluster_data = []
    cluster_id = 1
    for macs in fingerprints.values():
        if len(macs) > 1:
            print(f"Cluster {cluster_id}:\n  MACs: {macs}\n")
            cluster_data.append({"cluster": cluster_id, "macs": macs})
            cluster_id += 1

    if cluster_data:
        df = pd.DataFrame(cluster_data)
        df.to_csv("tshark_fingerprint_clusters.csv", index=False)
        print("Fingerprint clusters saved to 'tshark_fingerprint_clusters.csv'")
    else:
        print("No multi-MAC clusters found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tshark_fingerprint_clustering.py <path_to_pcap>")
        sys.exit(1)
    pcap_path = sys.argv[1]
    records = extract_tshark_fields(pcap_path)
    cluster_by_fingerprint(records)
