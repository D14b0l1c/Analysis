# Wi-Fi Anomaly Detection Suite

This directory contains multiple tools to detect various Wi-Fi attacks using PCAP files and TShark.

---

## Submodules

Each subfolder contains a standalone detection script and instructions:

| Module                    | Description                                     |
|---------------------------|-------------------------------------------------|
| `De-AuthAttackDetection`  | Detects 802.11 deauthentication attack frames   |
| `EAPOLReplayAttackDetection` | Identifies repeated EAPOL messages (replay attacks) |
| `EvilTwinDetection`       | Flags multiple BSSIDs using the same SSID       |
| `RogueAPDetection`        | Detects SSIDs not in a trusted whitelist        |

---

## Sample PCAP

A sample packet capture is provided in [`WiFiAnomaliesPCAP/wifi_anomalies.pcap`](../WiFi/WiFiAnomaliesPCAP/wifi_anomalies.pcap).  
Each detection module references this by default.

---

## Requirements

- Python 3.x  
- [TShark](https://www.wireshark.org/docs/man-pages/tshark.html) (part of Wireshark suite)

Install TShark:
```bash
sudo apt install tshark
