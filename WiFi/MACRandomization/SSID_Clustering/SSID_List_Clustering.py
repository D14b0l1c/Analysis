from scapy.all import rdpcap, Dot11, Dot11Elt, Dot11ProbeReq
import pandas as pd
from collections import defaultdict

# Load the PCAP file
PCAP_FILE = "probe_requests.pcap"
packets = rdpcap(PCAP_FILE)

# Extract SSIDs from directed probe requests
ssid_map = defaultdict(set)

for pkt in packets:
    if pkt.haslayer(Dot11ProbeReq):
        mac = pkt.addr2
        elt = pkt.getlayer(Dot11Elt)
        while elt is not None:
            if elt.ID == 0 and elt.info != b"":  # SSID tag and non-broadcast
                ssid_map[mac].add(elt.info.decode(errors="ignore"))
                break
            elt = elt.payload.getlayer(Dot11Elt)

# Convert to DataFrame
macs = list(ssid_map.keys())
ssids = list(ssid_map.values())
df = pd.DataFrame({"mac": macs, "ssids": ssids})

# Compute Jaccard similarity matrix
matrix = []
for i in range(len(ssids)):
    row = []
    for j in range(len(ssids)):
        a, b = ssids[i], ssids[j]
        sim = len(a & b) / len(a | b) if a | b else 0
        row.append(sim)
    matrix.append(row)

# Cluster using DBSCAN on (1 - similarity)
from sklearn.cluster import DBSCAN
import numpy as np
X = 1 - np.array(matrix)
clustering = DBSCAN(eps=0.5, min_samples=2, metric="precomputed").fit(X)
df["cluster"] = clustering.labels_
df.to_csv("ssid_clusters.csv", index=False)

print("SSID clustering done using Scapy. Fields used: Dot11Elt SSID (non-broadcast)")
for _, group in df.groupby("cluster"):
    print(f"Cluster {group['cluster'].iloc[0]}: {group['mac'].tolist()}")