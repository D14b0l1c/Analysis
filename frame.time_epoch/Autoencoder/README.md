# Autoencoder-Based Anomaly Detection

This module uses a neural network autoencoder to detect anomalies in Ethernet traffic by analyzing inter-packet timing (`Δt`) extracted from PCAP files. It learns normal timing patterns and flags sequences that cannot be reconstructed accurately as anomalies.

---

## Requirements

- Python 3.x  
- TShark (Wireshark CLI)  
- Python packages:
  ```
  pandas, numpy, matplotlib, keras, tensorflow
  ```

---

## Input

- A `.pcap` file (e.g., `your_pcap.pcap`)
- The script uses TShark to extract `frame.time_epoch` timestamps and calculate Δt values.

---

## How It Works

1. Extracts packet timestamps and computes Δt values.
2. Forms sliding sequences of Δt values (default window size: 10).
3. Trains a simple feedforward autoencoder on these sequences.
4. Measures reconstruction error for each sequence.
5. Flags anomalies where error exceeds `mean + 3 × std deviation`.

---

## Usage

Edit the script with your PCAP file name:

```python
pcap_file = "your_capture.pcap"
```

Then run:

```bash
python autoencoder_anomaly.py
```

---

## Output

The script produces a line plot showing:

- Reconstruction error for each Δt sequence
- Threshold line for anomaly detection
- Anomalous sequences highlighted

---

## Notes

- Effective at capturing non-linear patterns in timing data.
- Requires tuning sequence length, architecture, and training parameters for best results.
- Complements other time-series methods like ARIMA or clustering.
