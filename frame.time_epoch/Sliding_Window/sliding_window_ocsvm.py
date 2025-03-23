import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler

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

def sliding_window_ocsvm(df, window_size=50):
    features = []
    for i in range(0, len(df) - window_size, window_size):
        window = df['delta'].iloc[i:i+window_size]
        avg = window.mean()
        std = window.std()
        count = len(window)
        features.append([avg, std, count])
    features = np.array(features)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    oc_svm = OneClassSVM(nu=0.1)
    preds = oc_svm.fit_predict(features_scaled)
    
    plt.figure(figsize=(10, 4))
    plt.plot(preds, label="One-Class SVM Window Score")
    plt.title("Sliding Window One-Class SVM Detection")
    plt.xlabel("Window Index")
    plt.ylabel("Anomaly Score")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Replace with your actual PCAP file path
    pcap_file = "your_pcap.pcap"
    df = read_pcap_timestamps(pcap_file)
    sliding_window_ocsvm(df)