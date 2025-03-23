# Sliding Window One-Class SVM Detection

This module detects timing anomalies in PCAP traffic using a sliding window approach combined with a One-Class SVM. It extracts statistical features from sequences of Δt values and flags windows that deviate from learned normal behavior.

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

1. Computes Δt values from timestamps.
2. Splits the Δt series into fixed-size sliding windows (default: 50 packets).
3. For each window, extracts features:
   - Mean Δt
   - Standard deviation (jitter)
   - Packet count
4. Standardizes the features using `StandardScaler`.
5. Fits a One-Class SVM to the feature space.
6. Flags windows classified as outliers (`-1`) as anomalies.

---

## Usage

Edit the script with your PCAP file path:

```python
pcap_file = "your_capture.pcap"
```

Then run:

```bash
python sliding_window_ocsvm.py
```

---

## Output

The script produces a plot showing anomaly scores by window index. Each window is labeled as normal (`1`) or anomalous (`-1`).

---

## Notes

- You can tune detection sensitivity by adjusting the `window_size` and SVM `nu` parameter.
- Best suited for detecting short-lived changes in behavior over local segments of time.
- Complements global techniques like ARIMA or clustering.
