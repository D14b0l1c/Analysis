# ARIMA Forecasting Anomaly Detection

This module applies ARIMA (AutoRegressive Integrated Moving Average) modeling to detect timing anomalies in network traffic. It uses packet timestamp data extracted from PCAP files to compute inter-packet time deltas (Δt) and forecasts expected values. Anomalies are flagged when actual Δt values deviate significantly from the forecast.

---

## Requirements

- Python 3.x  
- TShark (Wireshark CLI)  
- Python packages:
  ```
  pandas, numpy, matplotlib, statsmodels
  ```

---

## Input

- A `.pcap` file (e.g., `your_pcap.pcap`)
- The script uses TShark to extract `frame.time_epoch` timestamps and calculate Δt values.

---

## How It Works

1. Extract packet timestamps using TShark.
2. Compute the Δt (time difference) between consecutive packets.
3. Fit an ARIMA(2, 0, 1) model on the Δt series.
4. Forecast future Δt values and calculate the residual error.
5. Flag any points where the residual exceeds 3 standard deviations from the mean as anomalies.

---

## Usage

Edit the script to specify your PCAP file:

```python
pcap_file = "your_capture.pcap"
```

Then run:

```bash
python arima_forecasting.py
```

---

## Output

The script generates a line plot showing:

- Actual Δt values
- ARIMA forecast
- Detected anomalies highlighted

The anomalies are identified based on deviations from the expected forecast range.

---

## Notes

- This method assumes the Δt series is sufficiently stationary for ARIMA to be meaningful.
- It works well for detecting periodic or cyclical deviations in traffic timing.
- It is best used as part of a broader detection toolkit alongside thresholding and machine learning-based methods.
