# Wi-Fi Fingerprint Clustering (Full TShark Extraction)

This module clusters devices based on full Wi-Fi frame fingerprinting, using **TShark** to extract Management, Control, and Data frame information, including Radiotap, Vendor, Prism, and AVS headers.

---

## Project Structure

| File | Purpose |
|:-----|:--------|
| `tshark_Fingerprint_Clustering.py` | Main script: TShark-based fingerprint clustering. |
| `Fingerprint_Clustering.py` | (Legacy) Older basic fingerprint version (optional). |
| `fingerprint_clusters.csv` | Output file containing clustered devices. |
| `README.md` | Documentation (this file). |

---

## Purpose

This script allows robust clustering and identification of wireless devices —  
even when MAC address randomization is enabled — by using detailed hardware, capability, and radio fingerprinting features.

- MAC Addresses (Source, Destination, BSSID, Transmitter, Receiver)
- Supported Rates, Extended Rates
- HT (802.11n), VHT (802.11ac), HE (802.11ax) Capabilities
- RSN and WPA Security Configurations
- Vendor-Specific Information
- Radio Measurements (RCPI, RSNI, Measurement Types)
- Physical Layer Information (MCS, NSS, Antenna Signal/Noise)
- Prism and AVS header fields (for specialized captures)

---

## Requirements

- Python 3.8+
- TShark installed (`tshark` in system PATH)
- Python libraries:
  - pandas
  - scikit-learn

Install dependencies:

```bash
pip install pandas scikit-learn
```

Install TShark:

```bash
# Ubuntu/Debian
sudo apt-get install tshark

# MacOS (Homebrew)
brew install wireshark
```

---

## How to Run

```bash
python tshark_Fingerprint_Clustering.py <input_file.pcap>
```

Example:

```bash
python tshark_Fingerprint_Clustering.py example_capture.pcap
```

This will:
- Extract all critical Wi-Fi fields
- Build fingerprints
- Cluster devices
- Output to `fingerprint_clusters.csv`

---

## Output

The resulting CSV (`fingerprint_clusters.csv`) contains:

| Field | Description |
|:------|:------------|
| mac | Device MAC address (if available) |
| fingerprint | MD5 hash of all extracted capabilities |
| cluster | Cluster label assigned by DBSCAN |

Example:

| mac | fingerprint | cluster |
|:---|:------------|:--------|
| aa:bb:cc:dd:ee:ff | d41d8cd98f00b204e9800998ecf8427e | 0 |
| 11:22:33:44:55:66 | 0cc175b9c0f1b6a831c399e269772661 | 1 |

---

## Features Extracted

- Full 802.11 Management/Control/Data header fields
- Extended Vendor Tags and Custom IEs
- RSN (WPA2/WPA3) Security Parameters
- HT/VHT/HE Capabilities
- Radiotap Signal Strengths, Antennas, Channel Info
- Prism and AVS Header Data (if present)

---

## Notes

- No frame-type filter applied: captures **all** Wi-Fi frames.
- Designed for high-fidelity clustering in dense wireless environments.
- Works across Wi-Fi 4/5/6 clients and IoT devices.
- Resilient to MAC address randomization techniques.
