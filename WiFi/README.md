# Wi-Fi Anomaly Detection Suite

This directory contains multiple tools to detect various Wi-Fi anomalies by analyzing PCAP files using TShark and Python. Each module targets a specific type of suspicious behavior in 802.11 wireless traffic.

---

## Modules

| Folder                      | Description                                                               |
|-----------------------------|---------------------------------------------------------------------------|
| `De-AuthAttackDetection`    | Detects 802.11 deauthentication attack frames                            |
| `EAPOLReplayAttackDetection`| Identifies repeated EAPOL messages that may indicate replay attacks      |
| `EvilTwinDetection`         | Flags multiple BSSIDs broadcasting the same SSID (potential Evil Twins)  |
| `RogueAPDetection`          | Detects access points not in a predefined whitelist                      |
| `MACRandomization`          | Analyzes probe requests for randomized MAC address behavior              |

---

## Sample PCAP Files

| Location                    | File Name           | Use Case                                      |
|-----------------------------|---------------------|-----------------------------------------------|
| `WiFiAnomaliesPCAP/`        | `wifi_anomalies.pcap` | Used by most detection modules above         |
| `WiFiProbeRequestsPCAP/`    | `probe_requests.pcap` | Used specifically for MAC randomization analysis |

---

## Requirements

- Python 3.x  
- TShark (CLI tool from Wireshark suite)  
- Python libraries (module-dependent):
  ```
  pandas, numpy, matplotlib, scikit-learn, binascii, scapy
  ```

Install TShark (Ubuntu example):

```bash
sudo apt install tshark
```

---

## Usage

Each module contains a self-contained Python script and its own `README.md`. To use a module:

1. Navigate into the module’s folder  
2. Modify the script to reference the appropriate PCAP file  
3. Run the script:

```bash
python <script_name>.py
```

Example:

```bash
cd De-AuthAttackDetection
python De-AuthAttackDetection.py
```

---

## Notes

- All modules use `frame.time_epoch` and other 802.11 fields via TShark.
- Output is typically visualized with `matplotlib` or printed to console.
- You can extend this suite with additional modules by reusing the same PCAP access pattern.

---

## Coming Soon

- SSID Fingerprinting
- Channel Hopping Analysis
- Beacon Flood Detection
