import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import MeanSquaredError

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

def autoencoder_anomaly(df, seq_len=10):
    data = np.array([df['delta'].iloc[i:i+seq_len].values for i in range(len(df)-seq_len)])
    X = data
    model = Sequential([
        Dense(8, activation='relu', input_shape=(seq_len,)),
        Dense(4, activation='relu'),
        Dense(8, activation='relu'),
        Dense(seq_len)
    ])
    model.compile(optimizer=Adam(), loss=MeanSquaredError())
    model.fit(X, X, epochs=50, batch_size=32, verbose=0)
    
    preds = model.predict(X)
    mse = np.mean((X - preds) ** 2, axis=1)
    threshold = np.mean(mse) + 3 * np.std(mse)
    anomalies = mse > threshold
    
    plt.figure(figsize=(10, 4))
    plt.plot(mse, label="Reconstruction Error")
    plt.axhline(threshold, color='red', linestyle='--', label="Threshold")
    plt.scatter(np.where(anomalies)[0], mse[anomalies], color='red', label="Anomalies")
    plt.title("Autoencoder Anomaly Detection")
    plt.xlabel("Sequence Index")
    plt.ylabel("Reconstruction Error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    # Replace with your actual PCAP file path
    pcap_file = "your_pcap.pcap"
    df = read_pcap_timestamps(pcap_file)
    autoencoder_anomaly(df)