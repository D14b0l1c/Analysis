# Temporal Clustering of Probe Requests

This module clusters MAC addresses based on the timing and sequence behavior of their probe requests. Even when MAC addresses are randomized, devices often reveal consistency in how frequently they send probes and how sequence numbers change. These patterns can be used to infer repeated device behavior.

---

## Purpose

To identify groups of randomized MAC addresses that share similar timing intervals and 802.11 sequence behavior, potentially indicating a single physical device rotating its identity.

---

## Requirements

- Python 3.x  
- Scapy  
- pandas  
- numpy  
- scikit-learn

Install dependencies:

```bash
pip install scapy pandas numpy scikit-learn
```

---

## Input

- PCAP file containing 802.11 probe requests  
  **Expected path:**  
  `WiFiProbeRequestsPCAP/probe_requests.pcap`

Update the path if needed:

```python
PCAP_FILE = "WiFiProbeRequestsPCAP/probe_requests.pcap"
```

---

## How It Works

1. Parses probe request frames using Scapy.
2. For each MAC address:
   - Records timestamps and 802.11 sequence numbers
   - Calculates:
     - Mean and standard deviation of time deltas (Δt)
     - Mean and standard deviation of sequence number deltas
3. Builds a feature set with these metrics.
4. Applies DBSCAN clustering on the feature vectors.
5. Outputs clusters of MACs with similar temporal behavior.

---

## Output

- `temporal_clusters.csv`  
  Contains:
  - MAC address
  - Mean and standard deviation of Δt
  - Mean and standard deviation of sequence deltas
  - Assigned cluster label

Console output example:

```
Temporal clustering done using Scapy. Fields used: timestamp deltas and sequence deltas
Cluster 0: ['aa:bb:cc:dd:ee:ff', '11:22:33:44:55:66']
```

---

## Notes

- This method is most effective when multiple probe requests from each MAC are present in the capture.
- Useful for identifying session reuse patterns and potential MAC rotation intervals.
- Best used in conjunction with SSID and tag-based clustering for multi-dimensional correlation.
