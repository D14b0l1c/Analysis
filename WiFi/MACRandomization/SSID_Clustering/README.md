# SSID-Based Clustering of Probe Requests (TShark Version)

This module groups probe requests by analyzing the SSIDs each device is scanning for.  
Devices using randomized MAC addresses often scan for the same SSIDs repeatedly.  
By clustering MAC addresses that probe for similar SSID sets, we can infer repeated device behavior.

---

## Project Structure

| File | Purpose |
|:-----|:--------|
| `tshark_SSID_List_Clustering.py` | Main script: TShark-based SSID clustering. |
| `SSID_List_Clustering.py` | (Legacy) Original Scapy-based version (optional). |
| `ssid_clusters.csv` | Output file containing clustered devices. |
| `README.md` | Documentation (this file). |

---

## Purpose

Identify and group randomized MAC addresses based on the overlap of their probed SSIDs.  
This method infers shared device identity by analyzing common scan patterns.

---

## Requirements

- Python 3.x
- TShark installed and in system PATH
- Python libraries:
  - pandas
  - scikit-learn

Install dependencies:

```bash
pip install pandas scikit-learn
```

Ensure TShark is installed:

```bash
# Ubuntu/Debian
sudo apt-get install tshark

# MacOS (Homebrew)
brew install wireshark
```

---

## How to Run

```bash
python tshark_SSID_List_Clustering.py <input_file.pcap>
```

Example:

```bash
python tshark_SSID_List_Clustering.py capture_probe_requests.pcap
```

This will:
- Extract Probe Request frames (MAC and SSIDs).
- Build sets of SSIDs per MAC address.
- Calculate Jaccard similarity between SSID sets.
- Cluster MAC addresses into logical groups.
- Output results to `ssid_clusters.csv`.

---

## Output

The resulting CSV (`ssid_clusters.csv`) contains:

| Field | Description |
|:------|:------------|
| mac | Device MAC address |
| ssid_set | List of probed SSIDs |
| cluster | Cluster ID assigned by Jaccard-based DBSCAN |

Sample:

| mac | ssid_set | cluster |
|:---|:---------|:--------|
| aa:bb:cc:dd:ee:ff | {\"HomeNetwork\", \"CoffeeShopWiFi\"} | 0 |
| 11:22:33:44:55:66 | {\"WorkNetwork\", \"CoffeeShopWiFi\"} | 1 |

---

## Extracted Fields

- `wlan.sa` — Source MAC Address
- `wlan_mgt.ssid` — SSID probed for
- `frame.time_epoch` — (Optional) Timestamp for probe request frame

(Only frames with `wlan.fc.type_subtype == 4` — Probe Request frames — are extracted.)

---

## Notes

- SSID overlap is a **strong indicator** of shared device identity under MAC randomization.
- Very useful for IoT investigations, enterprise Wi-Fi analysis, and rogue device detection.
- Can be combined with Fingerprint and Temporal clustering for even stronger attribution.
