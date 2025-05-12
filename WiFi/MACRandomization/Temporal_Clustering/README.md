# Temporal Clustering of Wi-Fi Devices (TShark Version)

This module clusters devices based on the timing behavior of their Wi-Fi frames, using timestamps and appearance patterns extracted directly via **TShark**.  
Even under MAC randomization, timing consistency can reveal persistent devices.

---

## Project Structure

| File | Purpose |
|:-----|:--------|
| `tshark_Temporal_Clustering.py` | Main script: TShark-based temporal clustering. |
| `Temporal_Clustering.py` | (Legacy) Scapy-based temporal clustering version (optional). |
| `temporal_clusters.csv` | Output file containing clustered devices. |
| `README.md` | Documentation (this file). |

---

## Purpose

Identify devices that behave similarly over time, based on:
- Inter-arrival timing of frames
- Total session duration
- Frame transmission frequency

Temporal fingerprints are resilient against MAC randomization and are critical for wireless surveillance, IoT tracking, and behavioral analysis.

---

## Requirements

- Python 3.x
- TShark installed (must be in system PATH)
- Python libraries:
  - pandas
  - numpy
  - scikit-learn

Install Python dependencies:

```bash
pip install pandas numpy scikit-learn
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
python tshark_Temporal_Clustering.py <input_file.pcap>
```

Example:

```bash
python tshark_Temporal_Clustering.py capture.pcap
```

This will:
- Extract timestamps and MAC addresses from all frames.
- Build timing profiles per device.
- Cluster devices based on their temporal characteristics.
- Output to `temporal_clusters.csv`.

---

## Output

The resulting CSV (`temporal_clusters.csv`) contains:

| Field | Description |
|:------|:------------|
| mac | Device MAC address |
| mean_gap | Mean inter-arrival time (seconds) |
| std_gap | Standard deviation of inter-arrival times |
| total_time | Total observed session time (seconds) |
| frame_count | Total number of frames seen |
| cluster | Cluster ID assigned by DBSCAN |

Example:

| mac | mean_gap | std_gap | total_time | frame_count | cluster |
|:---|:---------|:--------|:-----------|:------------|:--------|
| aa:bb:cc:dd:ee:ff | 0.2 | 0.05 | 20.4 | 100 | 0 |
| 11:22:33:44:55:66 | 0.25 | 0.07 | 18.9 | 85 | 1 |

---

## Extracted Fields

- `wlan.sa` — Source MAC Address
- `frame.time_epoch` — Packet timestamp

(Optionally expandable with `radiotap.dbm_antsignal`, `radiotap.antenna` for signal-based enrichment.)

---

## Notes

- Works across all Wi-Fi frame types (Management, Control, Data).
- Extremely effective in environments with MAC address randomization.
- Best results when used alongside Fingerprint and SSID Clustering modules.
- Useful for forensic reconstructions, persistence analysis, and mobility studies.
