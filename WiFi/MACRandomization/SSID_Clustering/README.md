# SSID-Based Clustering of Probe Requests

This module groups probe requests by analyzing the SSIDs each device is scanning for. Devices using randomized MAC addresses often scan for the same SSIDs repeatedly. By clustering MACs that probe for similar SSID sets, we can infer repeated device behavior.

---

## Purpose

To identify and group randomized MAC addresses based on the overlap of their probed SSIDs, which may indicate they belong to the same physical device.

---

## Requirements

- Python 3.x  
- Scapy  
- pandas

Install dependencies:

```bash
pip install scapy pandas
```

---

## Input

- PCAP file containing 802.11 probe requests  
  **Expected path:**  
  `WiFiProbeRequestsPCAP/probe_requests.pcap`

Update the script path if necessary:

```python
PCAP_FILE = "WiFiProbeRequestsPCAP/probe_requests.pcap"
```

---

## How It Works

1. Extracts probe request frames from the PCAP using Scapy.
2. For each MAC address, collects a list of SSIDs it has probed.
3. Compares SSID sets across all MACs using a similarity metric (e.g. Jaccard).
4. Groups MACs that share common SSIDs above a defined threshold.
5. Outputs SSID-based clusters to a CSV.

---

## Output

- A printed list of clusters showing which MACs probed for similar SSIDs.
- Optional: `ssid_clusters.csv` (if included in your implementation) containing:
  - Cluster ID
  - Associated MAC addresses
  - SSIDs probed

---

## Notes

- SSID overlap is a strong indicator of shared device identity when MACs are randomized.
- This method is especially effective in environments with hidden SSIDs or enterprise Wi-Fi.
- For more robust results, combine with fingerprint or temporal clustering.
