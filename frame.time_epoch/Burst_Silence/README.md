# Burst and Silence Detection

This module detects "bursts" and "silences" in network traffic by analyzing the time delta (`Δt`) between consecutive packets extracted from a PCAP file. It flags extremely short and long inter-packet delays, which may indicate anomalies such as DoS attacks, beaconing, or idle periods.

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
- The script uses TShark to extract `frame.time_epoch` timestamps and calculate Δt values.

---

## How It Works

1. Extracts timestamps from the PCAP and computes Δt values.
2. Flags:
   - **Bursts:** Δt < 0.001 seconds (configurable)
   - **Silences:** Δt > 1 second (configurable)
3. Visualizes the timing profile with bursts and silences highlighted.

---

## Usage

Edit the script to specify your PCAP file:

```python
pcap_file = "your_capture.pcap"
```

Then run:

```bash
python burst_silence_detection.py
```

---

## Output

The script generates a plot of Δt values over time, with bursts and silences marked.

---

## Notes

- Thresholds for burst and silence detection can be tuned via `burst_thresh` and `silence_thresh` in the script.
- This method is fast and effective for initial exploratory analysis of traffic timing.
- Works well as a companion tool to more advanced anomaly detection models.
