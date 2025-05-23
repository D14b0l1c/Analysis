import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

def time_delta_statistical(df):
    mean = df['delta'].mean()
    std = df['delta'].std()
    upper = mean + 3 * std
    lower = mean - 3 * std
    anomalies = (df['delta'] > upper) | (df['delta'] < lower)

    plt.figure(figsize=(10, 4))
    plt.plot(df['delta'], label="Δt")
    plt.axhline(upper, color='red', linestyle='--', label="Upper Threshold")
    plt.axhline(lower, color='red', linestyle='--', label="Lower Threshold")
    plt.scatter(df[anomalies].index, df[anomalies]['delta'], color='red', label="Anomalies")
    plt.title("Statistical Threshold Anomaly Detection")
    plt.xlabel("Packet Index")
    plt.ylabel("Δt (seconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pcap_file = "your_pcap.pcap"
    df = read_pcap_timestamps(pcap_file)
    time_delta_statistical(df)