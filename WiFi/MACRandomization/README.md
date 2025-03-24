# MAC Randomization Analysis

This directory contains tools for analyzing 802.11 probe request behavior under MAC address randomization. It focuses on detecting randomized MAC usage, clustering behavior across sessions, and inferring patterns that may reveal consistent device activity.

---

## Contents

| Folder               | Description                                                              |
|----------------------|--------------------------------------------------------------------------|
| `Fingerprint_Clustering` | Clusters probe requests by tag content to infer device fingerprints     |
| `SSID_Clustering`        | Groups probe requests by common SSIDs scanned across MACs              |
| `Temporal_Clustering`    | Detects repeated timing behavior and MAC rotation intervals             |
|`Exploration of User Privacy in 802.11 Probe Requests with MAC Address Randomization Using Temporal Pattern Analysis.pdf` | Research documentation supporting methodology and goals |

---

## Key Concepts

- **MAC Randomization:** Mobile devices frequently use randomized MACs to protect user privacy during active scans.
- **Probe Requests:** Devices broadcast SSIDs they are looking for. These can include vendor-specific tags, timestamps, or consistent scanning patterns.
- **Clustering Techniques:** The modules in this directory attempt to re-identify likely device sessions using:

  - Tag fingerprint similarity
  - SSID overlap
  - Time proximity and sequence behavior

---

## Requirements

- Python 3.x  
- Scapy  
- Additional libraries used across modules:
  ```
  pandas, numpy, matplotlib, scikit-learn
  ```

Install dependencies:

```bash
pip install scapy pandas numpy matplotlib scikit-learn
```

---

## How to Use

1. Choose a clustering method based on your goal:
   - **SSID-based correlation:** `SSID_Clustering`
   - **Timing behavior:** `Temporal_Clustering`
   - **Tag sequence/IE similarity:** `Fingerprint_Clustering`

2. Update the script to point to your probe request `.pcap` file, typically:

```python
pcap_file = "../../WiFiProbeRequestsPCAP/probe_requests.pcap"
```

3. Run the module's script:

```bash
python <clustering_script>.py
```

Each script generates a plot or summary report highlighting clusters or suspected device groupings.

---

## Documentation

Refer to the included PDF for detailed background:

```
Exploration of User Privacy in 802.11 Probe Requests with MAC Address Randomization Under Clustering Attacks.pdf
```

This paper outlines the threat model, assumptions, clustering heuristics, and limitations.

---

## Notes

- Each clustering method is independent and can be used separately or in combination.
- These tools are designed for research and analysis in controlled or authorized environments.
