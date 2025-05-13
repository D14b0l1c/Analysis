# Bluetooth Device Behavior Analysis & Visualization

This repository supports the extraction, analysis, and visualization of Bluetooth device activity from Kismet `.kismet` databases. It includes:

- A standalone processor script (`bluetooth.py`)
- pyVIP visualization modules for classified Bluetooth behaviors
- Output for CSV, charts, and KML geospatial visualization

---

## 🔧 Features

- Convert `.kismet` SQLite to JSON and extract Bluetooth metadata
- Classify devices by behavior (advertisers, persistent, scanners, etc.)
- Infer GPS if missing using snapshot matching
- Export results to CSVs and charts
- Visualize results with pyVIP (Virtualitics Python API)
- Generate KML files for mapping in Google Earth or similar

---

## 📁 Folder Structure

```

Bluetooth/
├── bluetooth.py                  # Main processor script
├── kismet\_output/               # Output folder for CSV/KML/images
├── pyvip\_behavior/              # pyVIP scripts for each behavior class
│   ├── pyvip\_advertisers.py
│   ├── pyvip\_persistent.py
│   ├── pyvip\_scanners.py
│   ├── pyvip\_rich\_services.py
│   ├── pyvip\_strong\_no\_services.py
│   ├── pyvip\_rotating\_macs.py
│   ├── pyvip\_repetitive\_advertisers.py
│   └── pyvip\_bluetooth\_devices.py
└── README.md                    # This file

````

---

## 🚀 Quick Start

### 1. Process a Kismet DB

```bash
python bluetooth.py
````

You will be prompted for:

* The `.kismet` file path
* The output directory

### Outputs include:

* `bluetooth_devices.csv`
* Behavior-classified CSVs (e.g. `advertisers.csv`, `persistent.csv`)
* KML map file (`bluetooth_devices.kml`)
* Vendor distribution chart and timeline plots

---

## 📊 pyVIP Visualizations

Each script in `pyvip_behavior/` loads a behavior CSV and renders it in Virtualitics Explore.

Run from terminal:

```bash
python pyvip_<behavior>.py
```

Behavior options include:

* `advertisers`
* `persistent`
* `scanners`
* `rich_services`
* `strong_no_services`
* `rotating_macs`
* `repetitive_advertisers`

You will be prompted for:

* Your pyVIP auth token
* The path to the corresponding behavior CSV

---

## 📦 Dependencies

* Python 3.7+
* `pandas`
* `matplotlib`
* `virtualitics` (for pyVIP scripts)
* Optional: Google Earth or any KML viewer

Install requirements:

```bash
pip install pandas matplotlib
```

For pyVIP usage:

```bash
pip install virtualitics
```

---

## 🛰️ GPS Inference

If your Kismet capture lacks device-level GPS, `bluetooth.py` will:

* Use `snapshots` table
* Match by `first_time` to infer approximate `avg_lat` and `avg_lon`
* Mark inferred entries with `gps_inferred = True`

---

## 📚 Notes

* Behavioral classification is rule-based using device duration, services, and signal strength
* MAC rotation detection uses `vendor_prefix` clustering
* Strong signal but no service devices are flagged as potential scanners

---

## 🔗 Integration

All CSV outputs are compatible with other analytics pipelines. Each pyVIP script can also be imported as a module:

```python
from pyvip_behavior.pyvip_advertisers import load_and_plot_advertisers
load_and_plot_advertisers(auth_token="...", csv_path="advertisers.csv")
```

---

## 🧠 Authoring & Usage

This package was designed to support Bluetooth situational awareness in edge, mobile, or forensics scenarios. It can be run offline and exported for geospatial or time-series review.

---

## ✅ Example Output

```
- advertisers.csv
- persistent.csv
- rich_services.csv
- scanners.csv
- rotating_macs.csv
- repetitive_advertisers.csv
- strong_no_services.csv
- bluetooth_devices.kml
- vendor_distribution.png
- device_timeline.png
```