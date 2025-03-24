# Fingerprint-Based Clustering of Probe Requests

This script clusters probe requests by hashing their 802.11 Information Elements (IEs). Devices using randomized MAC addresses often still include consistent tag sets in their probe requests, making it possible to fingerprint and group them.

---

## Purpose

To identify likely device sessions in the presence of MAC randomization by comparing the tag-level content of probe requests.

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

- PCAP file containing probe requests  
  **Expected path:**  
  `WiFiProbeRequestsPCAP/probe_requests.pcap`

Update this path in the script if needed:

```python
PCAP_FILE = "WiFiProbeRequestsPCAP/probe_requests.pcap"
```

---

## How It Works

1. Loads probe request frames using Scapy.
2. Extracts and hashes all `Dot11Elt` (tag) contents to generate a fingerprint.
3. Groups MAC addresses that share the same tag fingerprint.
4. Exports results to a CSV file.

---

## Output

- `fingerprint_clusters.csv`:  
  Each row contains:
  - Fingerprint hash
  - List of source MACs using it

Console output summarizes:

```
Fingerprint clustering complete.
Fingerprint ab12cd34... → MACs: [aa:bb:cc:dd:ee:ff, 11:22:33:44:55:66]
```

---

## Notes

- This method ignores SSID content and timing — it clusters purely by tag similarity.
- Tag sets are vendor-influenced and can be stable even when MACs rotate.
- Ideal for probe-level privacy analysis and identifying persistent scanning behavior.
