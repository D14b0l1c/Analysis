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

def burst_silence_detection(df, burst_thresh=0.001, silence_thresh=1):
    is_burst = df['delta'] < burst_thresh
    is_silence = df['delta'] > silence_thresh

    plt.figure(figsize=(10, 4))
    plt.plot(df['delta'], label="Δt")
    plt.scatter(df[is_burst].index, df[is_burst]['delta'], color='orange', label="Burst")
    plt.scatter(df[is_silence].index, df[is_silence]['delta'], color='purple', label="Silence")
    plt.title("Burst and Silence Detection")
    plt.xlabel("Packet Index")
    plt.ylabel("Δt (seconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pcap_file = "your_pcap.pcap"
    df = read_pcap_timestamps(pcap_file)
    burst_silence_detection(df)