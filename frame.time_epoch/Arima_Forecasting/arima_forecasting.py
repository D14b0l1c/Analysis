import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

def read_pcap_timestamps(pcap_path):
    # Use TShark to extract frame.time_epoch
    command = [
        "tshark", "-r", pcap_path,
        "-T", "fields", "-e", "frame.time_epoch"
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"TShark failed: {result.stderr}")
    lines = result.stdout.strip().split("\n")
    timestamps = pd.to_numeric(pd.Series(lines), errors='coerce').dropna()
    df = pd.DataFrame({
        "frame.time_epoch": timestamps,
        "delta": timestamps.diff().fillna(0)
    })
    return df

def arima_forecasting(df):
    model = ARIMA(df['delta'], order=(2, 0, 1))
    model_fit = model.fit()
    forecast = model_fit.predict(start=0, end=len(df)-1)
    residuals = df['delta'] - forecast
    threshold = 3 * residuals.std()
    anomalies = np.abs(residuals) > threshold
    
    plt.figure(figsize=(10, 4))
    plt.plot(df['delta'], label="Δt")
    plt.plot(forecast, label="ARIMA Forecast")
    plt.scatter(df.index[anomalies], df['delta'][anomalies], color='red', label="Anomaly")
    plt.title("ARIMA Forecasting Anomaly Detection")
    plt.xlabel("Packet Index")
    plt.ylabel("Δt (seconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    # Replace with your actual PCAP file path
    pcap_file = "your_pcap.pcap"
    df = read_pcap_timestamps(pcap_file)
    arima_forecasting(df)