# Clustering-Based Anomaly Detection

This module applies unsupervised clustering algorithms—DBSCAN and KMeans—to detect anomalies in packet timing based on inter-packet delays (`Δt`). It groups similar Δt values and flags outliers or structural patterns in timing behavior.

---

## Requirements

- Python 3.x  
- TShark (Wireshark CLI)  
- Python packages:
  ```
  pandas, numpy, matplotlib, scikit-learn
  ```

---

## Input

- A `.pcap` file (e.g., `your_pcap.pcap`)
- The script uses TShark to extract `frame.time_epoch` timestamps and compute Δt values.

---

## How It Works

1. Computes Δt values from packet timestamps.
2. Standardizes the values using `StandardScaler`.
3. Applies:
   - **DBSCAN:** Detects dense clusters and labels noise as outliers.
   - **KMeans:** Clusters all values into a fixed number of groups (default: 2).
4. Visualizes the clusters for interpretation.

---

## Usage

Edit the script to specify your PCAP file:

```python
pcap_file = "your_capture.pcap"
```

Then run:

```bash
python clustering_analysis.py
```

To use the downsampled version (for large PCAPs):

```bash
python clustering_analysis_downsampled.py
```

---

## Output

Each clustering method generates a plot showing the distribution of Δt values, colored by cluster assignment. DBSCAN outliers are labeled as noise (`-1`).

---

## Notes

- DBSCAN is well-suited for outlier detection but sensitive to `eps` and `min_samples` parameters.
- KMeans provides clearer structure but requires predefining `k`.
- Downsampling (`df.iloc[::10]`) improves performance on large captures while preserving trends.
