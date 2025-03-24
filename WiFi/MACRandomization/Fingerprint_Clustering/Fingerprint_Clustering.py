from scapy.all import rdpcap, Dot11, Dot11Elt, Dot11ProbeReq
import hashlib
import pandas as pd
from collections import defaultdict

# Load the PCAP file
PCAP_FILE = "probe_requests.pcap"
packets = rdpcap(PCAP_FILE)

# Extract and hash Dot11Elt content per MAC
fingerprints = defaultdict(list)

for pkt in packets:
    if pkt.haslayer(Dot11ProbeReq):
        mac = pkt.addr2
        ies = []
        elt = pkt.getlayer(Dot11Elt)
        while elt is not None:
            ies.append(bytes(elt))
            elt = elt.payload.getlayer(Dot11Elt)
        if ies:
            fingerprint = hashlib.md5(b''.join(ies)).hexdigest()
            fingerprints[fingerprint].append(mac)

# Build DataFrame from fingerprints
df_fp = pd.DataFrame([{"fingerprint": fp, "macs": macs} for fp, macs in fingerprints.items()])
df_fp.to_csv("fingerprint_clusters.csv", index=False)

print("Fingerprint clustering done using Scapy. Fields used: Dot11Elt content hashed per MAC")
for _, row in df_fp.iterrows():
    print(f"Fingerprint {row['fingerprint'][:8]}... → MACs: {row['macs']}")