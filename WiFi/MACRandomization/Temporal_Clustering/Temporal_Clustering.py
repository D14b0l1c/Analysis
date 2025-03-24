from scapy.all import rdpcap, Dot11, Dot11ProbeReq
import pandas as pd
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN

# Load the PCAP file
PCAP_FILE = "probe_requests.pcap"
packets = rdpcap(PCAP_FILE)

# Collect per-MAC timestamps and sequence numbers
data = defaultdict(list)

for pkt in packets:
    if pkt.haslayer(Dot11ProbeReq):
        mac = pkt.addr2
        ts = float(pkt.time)
        seq = pkt.SC >> 4 if hasattr(pkt, "SC") else None
        if seq is not None:
            data[mac].append((ts, seq))

# Extract per-MAC timing and sequence stats
records = []
for mac, points in data.items():
    if len(points) < 2:
        continue
    points.sort()
    timestamps, sequences = zip(*points)
    dt = np.diff(timestamps)
    ds = np.diff(sequences)
    records.append({
        "mac": mac,
        "mean_dt": np.mean(dt),
        "std_dt": np.std(dt),
        "mean_seq": np.mean(ds),
        "std_seq": np.std(ds)
    })

# Build feature dataframe
df = pd.DataFrame(records).fillna(0)

# Apply clustering on temporal features
X = df[["mean_dt", "std_dt", "mean_seq", "std_seq"]].values
clustering = DBSCAN(eps=0.5, min_samples=2).fit(X)
df["cluster"] = clustering.labels_
df.to_csv("temporal_clusters.csv", index=False)

print("Temporal clustering done using Scapy. Fields used: timestamp deltas and sequence deltas")
for _, group in df.groupby("cluster"):
    print(f"Cluster {group['cluster'].iloc[0]}: {group['mac'].tolist()}")