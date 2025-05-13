# Analysis

This repository contains modular tools for analyzing network anomalies from packet capture (PCAP) files. It covers three primary domains:

- **Wi-Fi** anomaly detection (802.11)
- **Ethernet** timing analysis using `frame.time_epoch`
- **Vulnerability** detection and analysis
- **Bluetooth** passive device classification and behavioral fingerprinting

Each technique is implemented in Python, with modular scripts and reproducible outputs.

---

## Repository Structure

| Directory             | Description                                                                |
|-----------------------|----------------------------------------------------------------------------|
| `WiFi/`               | Tools for analyzing 802.11 wireless traffic for attacks and behavioral leaks|
| `frame.time_epoch/`   | Timing-based anomaly detection in Ethernet PCAPs using statistical and ML techniques|
| `Vulnerability/`      | Tools for identifying and analyzing network vulnerabilities using scan data and exploit databases|
| `Bluetooth/`          | Scripts for classifying and visualizing Bluetooth device behaviors using Kismet logs and pyVIP|

---

## Wi-Fi Analysis Modules

Located in: [`WiFi/`](./WiFi)

| Module                       | Description                                                             |
|------------------------------|-------------------------------------------------------------------------|
| `De-AuthAttackDetection`     | Detects 802.11 deauthentication frames                                  |
| `EAPOLReplayAttackDetection` | Flags repeated EAPOL messages for replay attack detection               |
| `EvilTwinDetection`          | Identifies multiple BSSIDs broadcasting the same SSID                   |
| `RogueAPDetection`           | Detects unauthorized access points not in a known whitelist             |
| `MACRandomization`           | Analyzes MAC randomization behavior through submodules                  |
| `pyvip`                      | pyVIP-compatible scripts to visualize detection outputs in Explore      |

Sample PCAPs for these modules can be found in:

- `WiFiAnomaliesPCAP/`
- `WiFiProbeRequestsPCAP/`

---

## Bluetooth Analysis Modules

Located in: [`Bluetooth/`](./Bluetooth)

This module analyzes Bluetooth Classic and BLE data from `.kismet` logs to extract passive device insights and behavioral patterns. Outputs include CSVs, KML maps, and pyVIP-compatible visualizations.

| Component                    | Description                                                              |
|------------------------------|--------------------------------------------------------------------------|
| `bluetooth.py`               | Main extraction and classification engine for Kismet `.kismet` files     |
| `pyvip_behavior/`            | pyVIP scripts for each behavior class (advertisers, scanners, etc.)      |
| `kismet_output/`             | Folder for CSV exports, plots, and KML maps                              |

### Classifications:
- Advertisers
- Persistent devices
- Repetitive advertisers
- Rich vs. no-service profiles
- Rotating MACs
- Signal strength anomalies
- Scanners

Behavioral classifications are based on signal patterns, observed services, presence duration, and vendor prefix clustering.

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

## Vulnerability Analysis

Located in: [`Vulnerability/`](./Vulnerability)

This module integrates network vulnerability detection and analysis, combining scan data (e.g., from Nmap) with known vulnerability databases like ExploitDB and NVD.

| Subdirectory       | Description                                                         |
|--------------------|---------------------------------------------------------------------|
| `core/`            | Core processing scripts (e.g., matching, extracting, merging)       |
| `data/`            | Contains `input/` and `output/` folders for parsed vulnerability data|
| `docs/`            | Documentation and user setup guides                                 |
| `exploit_db/`      | Exploit and CVE datasets including custom and indexed files         |
| `tools/`           | pyVIP-based and auxiliary scripts for interactive exploration       |

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
- Bluetooth presence mapping, MAC analysis, vendor distribution
- Vulnerability detection, prioritization, and exploitability assessment
- pyVIP visualizations of risk surfaces and exploit distributions