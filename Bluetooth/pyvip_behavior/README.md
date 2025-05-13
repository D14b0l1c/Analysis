# pyVIP Bluetooth Behavior Visualization Scripts

This directory contains standalone Python scripts to visualize Bluetooth device behaviors using the Virtualitics Python API (`pyVIP`). Each script corresponds to a specific behavior classification or analysis result from Bluetooth scan data processed via `bluetooth.py`.

## Requirements

- Python 3.7+
- `pandas`
- `virtualitics` (pyVIP API)
- A valid Virtualitics Explore environment and access token

## Usage

Each script is self-contained and can be run directly from the terminal or imported as a module in another Python workflow.

**To run a script:**

```bash
python pyvip_<behavior>.py
```

Each script will prompt you for:
- Your pyVIP auth token
- The path to the corresponding CSV file

## Scripts Overview

| Script Name                            | Plot Type   | Description |
|----------------------------------------|-------------|-------------|
| `pyvip_advertisers.py`                | Map Plot    | Visualizes brief, service-less advertising devices |
| `pyvip_persistent.py`                 | Map Plot    | Shows devices present longer than 5 minutes |
| `pyvip_scanners.py`                   | Map Plot    | Highlights short-lived, high-signal devices (potential scanners) |
| `pyvip_rich_services.py`              | Map Plot    | Visualizes devices offering 4+ Bluetooth services |
| `pyvip_strong_no_services.py`         | Map Plot    | Displays strong-signal devices not advertising any services |
| `pyvip_rotating_macs.py`              | Bar Chart   | Plots vendor_prefix vs number of unique MACs (MAC rotation) |
| `pyvip_repetitive_advertisers.py`     | Bar Chart   | Plots devmacs seen repeatedly over short time intervals |
| `pyvip_bluetooth_devices.py` | None | Loads bluetooth_devices.csv into Virtualitics Explore without plotting |

## Integration

These scripts can also be imported into other Python projects:

```python
from pyvip_advertisers import load_and_plot_advertisers

load_and_plot_advertisers(auth_token="YOUR_TOKEN", csv_path="path/to/advertisers.csv")
```

## Notes

- GPS fields are used in Map Plots: `avg_lat`, `avg_lon`
- Data is passed unmodified from CSVs; filtering is handled inside pyVIP or externally
- Suitable for integration with a full Bluetooth behavior analytics pipeline
