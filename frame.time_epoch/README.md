# Timing-Based Anomaly Detection (frame.time_epoch)

This directory contains a collection of detection modules for identifying timing anomalies in Ethernet traffic. All methods are based on analyzing `frame.time_epoch` from PCAP files, which captures the timestamp of each packet. By calculating the time delta (Δt) between packets, the modules apply a variety of techniques—statistical and machine learning—to detect bursts, silences, outliers, or unusual traffic patterns.

---

## Detection Modules

| Folder              | Method Summary                                                      |
|---------------------|----------------------------------------------------------------------|
| Arima_Forecasting   | Uses ARIMA forecasting to model normal timing behavior and flag deviations |
| Autoencoder         | Trains a neural network to reconstruct normal Δt patterns and flags large reconstruction errors |
| Burst_Silence       | Detects high-density traffic bursts and idle silences based on thresholding |
| Clustering          | Applies DBSCAN and KMeans to detect timing-based outliers via clustering |
| Sliding_Window      | Extracts window-based features (mean, std) and uses One-Class SVM to identify anomalies |
| Time_Delta          | Flags Δt values outside mean ± 3×std as statistical outliers         |

---

## Shared Approach

All modules follow a similar process:

1. Use TShark to extract `frame.time_epoch` from a `.pcap` file.
2. Compute Δt as the time difference between consecutive packets.
3. Analyze the Δt series using a specific detection technique.
4. Output detected anomalies through plotted or printed results.

---

## Dependencies

Each script is standalone and may have unique requirements, but collectively the tools rely on:

- Python 3.x
- TShark (Wireshark CLI)
- Common Python libraries:
  ```
  pandas, numpy, matplotlib, scikit-learn, statsmodels, keras, tensorflow
  ```

You can install the required packages with:

```bash
pip install -r requirements.txt
```

TShark must also be installed and accessible in your system's PATH:

```bash
sudo apt install tshark
```

---

## Usage

Each subfolder contains its own script and README file. To use any detection module:

1. Navigate into the module's directory.
2. Update the script to point to your PCAP file.
3. Run the script using Python.

Example:

```bash
cd Arima_Forecasting
python arima_forecasting.py
```

---

## Choosing a Detection Strategy

- Use `Time_Delta` or `Burst_Silence` for fast, interpretable results.
- Use `Autoencoder` or `Sliding_Window` for ML-based adaptive detection.
- Use `Clustering` to explore unsupervised structure in timing behavior.
- Use `Arima_Forecasting` for time series analysis of periodic anomalies.

---

## File Organization

Each module contains:

- A Python detection script
- A `README.md` for usage
- A `.txt` file explaining the theory and implementation details

---

## Notes

These tools are modular and designed to support rapid experimentation with time-based anomaly detection. They can be extended to handle non-Ethernet traffic, alternate timestamp formats, or real-time processing.
