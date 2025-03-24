# Analysis

This repository contains modular tools for analyzing network anomalies from packet capture (PCAP) files. It is divided into two primary domains:

- **Wi-Fi** anomaly detection (802.11)
- **Ethernet** timing analysis using `frame.time_epoch`

Each technique is implemented in Python, with modular scripts and reproducible output.

---

## Repository Structure

| Directory           | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `WiFi/`             | Tools for analyzing 802.11 wireless traffic for attacks and behavioral leaks |
| `frame.time_epoch/` | Timing-based anomaly detection in Ethernet PCAPs using statistical and ML techniques |

---

## Wi-Fi Analysis Modules

Located in: [`WiFi/`](./WiFi)

| Module                   | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `De-AuthAttackDetection` | Detects 802.11 deauthentication frames                                       |
| `EAPOLReplayAttackDetection` | Flags repeated EAPOL messages for replay attack detection             |
| `EvilTwinDetection`      | Identifies multiple BSSIDs broadcasting the same SSID                      |
| `RogueAPDetection`       | Detects unauthorized access points not in a known whitelist                |
| `MACRandomization`       | Clusters randomized MACs via SSID, timing, and tag fingerprinting          |

Sample PCAPs for these modules can be found in:

- `WiFiAnomaliesPCAP/`
- `WiFiProbeRequestsPCAP/`

---

## Ethernet Timing Analysis

Located in: [`frame.time_epoch/`](./frame.time_epoch)

Each module analyzes inter-packet delay (`Δt`) to detect abnormal patterns in Ethernet traffic.

| Module              | Method                             |
|---------------------|------------------------------------|
| `Arima_Forecasting` | Forecast-based anomaly detection   |
| `Autoencoder`       | Neural reconstruction errors       |
| `Burst_Silence`     | Threshold-based activity spikes    |
| `Clustering`        | DBSCAN / KMeans for Δt grouping    |
| `Sliding_Window`    | One-Class SVM on rolling windows   |
| `Time_Delta`        | Outlier detection with statistical thresholds |

---

## Requirements

- Python 3.x  
- TShark (Wireshark CLI) for timestamp extraction  
- Python libraries (varies per module):
  ```
  scapy, pandas, numpy, matplotlib, scikit-learn, statsmodels, tensorflow, keras
  ```

---

## Use Cases

- Wireless privacy audits (MAC randomization)
- Attack detection in 802.11 networks
- Behavioral fingerprinting of probe activity
- Time-based Ethernet traffic anomaly analysis
- Clustering and modeling device behavior across sessions

---

## License

This repository is intended for research, academic, and authorized security auditing use. Please use responsibly.

---

## Author

Maintained by [D14b01c](https://github.com/D14b01c)
```

Let me know if you'd like badges (e.g. license, Python version) or a `setup.py` to make this pip-installable.
