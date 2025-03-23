# Time Delta Statistical Threshold Detection

This module uses a statistical thresholding approach to detect timing anomalies in Ethernet traffic. It analyzes inter-packet delays (`Δt`) and flags values that fall outside a normal range defined by the mean and standard deviation.

---

## Requirements

- Python 3.x  
- TShark (Wireshark CLI)  
- Python packages:
  ```
  pandas, numpy, matplotlib
  ```

---

## Input

- A `.pcap` file (e.g., `your_pcap.pcap`)
- The script uses TShark to extract `frame.time_epoch` timestamps and calculate Δt between consecutive packets.

---

## How It Works

1. Computes Δt values from the timestamp sequence.
2. Calculates:
   - Mean of all Δt values
   - Standard deviation of Δt values
3. Defines anomaly thresholds:
   - Upper = mean + 3 × std
   - Lower = mean − 3 × std
4. Flags Δt values that fall outside these bounds.

---

## Usage

Edit the script with the name of your PCAP file:

```python
pcap_file = "your_capture.pcap"
```

Then run:

```bash
python time_delta_statistical.py
```

---

## Output

The script produces a plot of all Δt values, with threshold lines and anomalies clearly marked.

---

## Notes

- This is a fast, simple method to detect obvious outliers.
- Best used as a first-pass filter before applying machine learning-based techniques.
- Assumes Δt values are normally distributed — not ideal for complex or evolving traffic patterns.
