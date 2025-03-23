import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler  # ✅ This was missing!

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

def clustering_methods(df):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[['delta']])

    # DBSCAN
    db = DBSCAN(eps=0.5, min_samples=5)
    db_labels = db.fit_predict(scaled)
    plt.figure(figsize=(10, 4))
    plt.scatter(df.index, df['delta'], c=db_labels, cmap='tab10')
    plt.title("DBSCAN Clustering")
    plt.xlabel("Packet Index")
    plt.ylabel("Δt (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # KMeans
    km = KMeans(n_clusters=2, random_state=42)
    kmeans_labels = km.fit_predict(scaled)
    plt.figure(figsize=(10, 4))
    plt.scatter(df.index, df['delta'], c=kmeans_labels, cmap='Set2')
    plt.title("KMeans Clustering")
    plt.xlabel("Packet Index")
    plt.ylabel("Δt (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pcap_file = "your_pcap.pcap"
    df = read_pcap_timestamps(pcap_file)
    clustering_methods(df)