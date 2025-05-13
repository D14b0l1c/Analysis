"""
kismetdb_with_kml.py

This script processes Kismet .kismet SQLite databases to extract and analyze Bluetooth device activity.
It converts the database to JSON, extracts Bluetooth-related devices into CSV, performs behavioral analysis,
and optionally exports device locations as a KML file for geospatial visualization.

Key Features:
- Converts SQLite to JSON
- Extracts Bluetooth device metadata
- Detects behavioral patterns (advertisers, persistent, scanners, etc.)
- Identifies rotating MAC addresses and repetitive signals
- Exports charts and CSVs
- Generates KML for GPS-aware devices (with fallback if GPS missing)
"""

import sqlite3
import json
import csv
import os
import pandas as pd
from datetime import datetime, timezone
import matplotlib.pyplot as plt



def export_kismet_to_json(db_path, json_path):
    """
    Extracts all tables from a Kismet SQLite database and saves the contents to a JSON file.

    Args:
        db_path (str): Path to the .kismet database.
        json_path (str): Output path for the JSON file.
    """
    def clean_row(row_dict):
        for key, value in row_dict.items():
            if isinstance(value, bytes):
                try:
                    row_dict[key] = value.decode('utf-8', errors='replace')
                except:
                    row_dict[key] = str(value)
        return row_dict

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    db_data = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        table = table_name[0]
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        cleaned = [clean_row(dict(zip(columns, row))) for row in rows]
        db_data[table] = cleaned

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(db_data, f, indent=2)
    conn.close()
    print(f" Exported Kismet DB to JSON: {json_path}")

def infer_device_gps_from_snapshots(devices_df, db_path):
    """
    Infers approximate GPS location for Bluetooth devices by matching their first seen timestamp
    to the closest timestamp in the snapshots table.

    Args:
        devices_df (pd.DataFrame): DataFrame of Bluetooth devices.
        db_path (str): Path to the .kismet database.

    Returns:
        pd.DataFrame: DataFrame with avg_lat, avg_lon, and gps_inferred columns.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            snapshots = pd.read_sql_query(
                "SELECT ts_sec, ts_usec, lat, lon FROM snapshots ORDER BY ts_sec, ts_usec",
                conn
            )
        snapshots['timestamp'] = snapshots['ts_sec'] + snapshots['ts_usec'] / 1_000_000

        def find_closest_gps(ts):
            closest = snapshots.iloc[(snapshots['timestamp'] - ts).abs().argsort()[:1]]
            return closest[['lat', 'lon']].values[0]

        devices_df[['avg_lat', 'avg_lon']] = devices_df['first_time'].apply(find_closest_gps).apply(pd.Series)
        devices_df['gps_inferred'] = True
    except Exception as e:
        print(" GPS inference failed or snapshots table missing.", e)
        devices_df['avg_lat'] = 0.0
        devices_df['avg_lon'] = 0.0
        devices_df['gps_inferred'] = False
    return devices_df

def extract_bluetooth_to_csv(json_path, output_csv_path):
    """
    Parses the JSON export of the Kismet DB and extracts Bluetooth devices.
    Adds metadata like Bluetooth type (BLE/Classic), vendor prefix, and service list.

    Args:
        json_path (str): Path to the Kismet JSON export.
        output_csv_path (str): Path to write the Bluetooth device CSV.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    devices = data.get('devices', [])
    bluetooth_devices = [d for d in devices if d.get('phyname', '').lower() == 'bluetooth']

    for dev in bluetooth_devices:
        d = dev.get('device')
        if isinstance(d, str):
            try:
                dj = json.loads(d)
                bt_meta = dj.get("bluetooth.device", {})
                services = bt_meta.get("bluetooth.device.services", [])
                bt_type_code = bt_meta.get("bluetooth.device.type")

                # Determine BLE or Classic
                if bt_type_code == 1:
                    dev['bt_type'] = 'BLE'
                elif bt_type_code == 0:
                    dev['bt_type'] = 'Classic'
                else:
                    dev['bt_type'] = 'BLE' if any(s.startswith('0000') for s in services) else 'Unknown'

                dev['services'] = ', '.join(services) if services else "None"
            except:
                dev['services'] = "Invalid JSON"
                dev['bt_type'] = "Unknown"
        else:
            dev['services'] = "None"
            dev['bt_type'] = "Unknown"

        dev['vendor_prefix'] = dev.get('devmac', '')[:8]
        dev['first_seen'] = datetime.fromtimestamp(dev.get('first_time', 0), timezone.utc).isoformat()
        dev['last_seen'] = datetime.fromtimestamp(dev.get('last_time', 0), timezone.utc).isoformat()

    fieldnames = ['devmac', 'phyname', 'type', 'strongest_signal', 'bytes_data', 'vendor_prefix',
                  'first_seen', 'last_seen', 'services', 'bt_type', 'avg_lat', 'avg_lon']
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dev in bluetooth_devices:
            row = {key: dev.get(key, '') for key in fieldnames}
            writer.writerow(row)

    print(f" Extracted {len(bluetooth_devices)} Bluetooth devices to CSV: {output_csv_path}")

def analyze_behavior(csv_path, output_dir):
    """
    Analyzes Bluetooth device behavior by categorizing them as advertisers, persistent,
    scanners, etc., based on signal strength, duration, and services. Saves CSVs and visualizations.

    Args:
        csv_path (str): Path to the enriched Bluetooth CSV.
        output_dir (str): Directory to write output CSVs and charts.
    """
    df = pd.read_csv(csv_path)
    df['first_seen'] = pd.to_datetime(df['first_seen'])
    df['last_seen'] = pd.to_datetime(df['last_seen'])
    df['duration_sec'] = (df['last_seen'] - df['first_seen']).dt.total_seconds()
    df['num_services'] = df['services'].fillna('None').astype(str).apply(
        lambda x: 0 if x.strip().lower() == 'none' else len(x.split(','))
    )

    df['behavior'] = 'unknown'
    df.loc[(df['num_services'] == 0) & (df['duration_sec'] <= 30), 'behavior'] = 'advertiser'
    df.loc[df['duration_sec'] > 300, 'behavior'] = 'persistent'
    df.loc[df['num_services'] > 3, 'behavior'] = 'rich_services'
    df.loc[(df['duration_sec'] <= 60) & (df['strongest_signal'] >= -50), 'behavior'] = 'scanner'

    df.to_csv(csv_path, index=False)

    df[df['behavior'] == 'advertiser'].to_csv(os.path.join(output_dir, 'advertisers.csv'), index=False)
    df[df['behavior'] == 'persistent'].to_csv(os.path.join(output_dir, 'persistent.csv'), index=False)
    df[df['behavior'] == 'rich_services'].to_csv(os.path.join(output_dir, 'rich_services.csv'), index=False)
    df[df['behavior'] == 'scanner'].to_csv(os.path.join(output_dir, 'scanners.csv'), index=False)

    rotating_macs = df.groupby('vendor_prefix')['devmac'].nunique().reset_index()
    rotating_macs = rotating_macs[rotating_macs['devmac'] > 1]
    rotating_macs.columns = ['vendor_prefix', 'unique_macs']
    rotating_macs.to_csv(os.path.join(output_dir, 'rotating_macs.csv'), index=False)

    short_lived = df[df['duration_sec'] <= 60]
    repeat_counts = short_lived['devmac'].value_counts()
    repeats = repeat_counts[repeat_counts > 1].reset_index()
    repeats.columns = ['devmac', 'count']
    repeats.to_csv(os.path.join(output_dir, 'repetitive_advertisers.csv'), index=False)

    strong_no_services = df[(df['strongest_signal'] >= -40) & (df['num_services'] == 0)]
    strong_no_services.to_csv(os.path.join(output_dir, 'strong_no_services.csv'), index=False)

    try:
        plt.figure()
        vendor_counts = df['vendor_prefix'].value_counts().reset_index()
        vendor_counts.columns = ['Vendor Prefix', 'Count']
        vendor_counts.head(10).plot(kind='bar', x='Vendor Prefix', y='Count', legend=False)
        plt.title('Top 10 Bluetooth Vendor Prefixes')
        plt.ylabel('Device Count')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'vendor_distribution.png'))

        df['hour'] = df['first_seen'].dt.floor("h")
        timeline = df.groupby('hour').size().reset_index(name='device_count')
        plt.figure()
        plt.plot(timeline['hour'], timeline['device_count'], marker='o')
        plt.title('Bluetooth Devices Seen Over Time')
        plt.xlabel('Time (Hour)')
        plt.ylabel('Devices Seen')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'device_timeline.png'))
    except Exception as e:
        print(f" Plotting failed: {e}")

def export_kml(csv_path, output_dir):
    """
    Converts Bluetooth device data into a KML format for map-based visualization.
    Includes info like behavior, signal strength, services, and GPS source.

    Args:
        csv_path (str): Path to the Bluetooth CSV with coordinates.
        output_dir (str): Directory to save the KML output.
    """
    df = pd.read_csv(csv_path)
    df = df.fillna(0)
    kml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '<Document>',
        '<name>Bluetooth Devices</name>'
    ]

    for _, row in df.iterrows():
        lat, lon = row.get('avg_lat', 0), row.get('avg_lon', 0)
        if lat == 0 and lon == 0:
            continue
        devmac = row.get('devmac', 'Unknown')
        vendor = row.get('vendor_prefix', 'N/A')
        signal = row.get('strongest_signal', 'N/A')
        behavior = row.get('behavior', 'Unknown')
        bt_type = row.get('bt_type', 'Unknown')
        inferred = row.get('gps_inferred', False)
        kml_lines += [
            '<Placemark>',
            f'<name>{devmac}</name>',
            '<description><![CDATA[',
            f'Vendor: {vendor}<br>',
            f'Type: {bt_type}<br>',
            f'Behavior: {behavior}<br>',
            f'Signal: {signal}<br>',
            f'Services: {row.get("services", "")}<br>',
            f'GPS Inferred: {inferred}',
            ']]></description>',
            '<Point>',
            f'<coordinates>{lon},{lat},0</coordinates>',
            '</Point>',
            '</Placemark>'
        ]

    kml_lines += ['</Document>', '</kml>']
    kml_path = os.path.join(output_dir, 'bluetooth_devices.kml')
    with open(kml_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(kml_lines))
    print(f" KML file created at: {kml_path}")



def run_analyze_bluetooth(kismet_db_path, output_dir, bluetooth_csv_path, json_output_path):
    os.makedirs(output_dir, exist_ok=True)

    # === RUN ALL STEPS ===
    export_kismet_to_json(kismet_db_path, json_output_path)
    extract_bluetooth_to_csv(json_output_path, bluetooth_csv_path)

    df = pd.read_csv(bluetooth_csv_path)
    if 'avg_lat' not in df.columns or df['avg_lat'].fillna(0).eq(0).all():
        print(" No GPS in Bluetooth device entries — inferring from snapshots...")
        df['first_time'] = pd.to_numeric(df['first_seen'].apply(lambda x: pd.Timestamp(x).timestamp()), errors='coerce')
        df = infer_device_gps_from_snapshots(df, kismet_db_path)
        df.to_csv(bluetooth_csv_path, index=False)

    analyze_behavior(bluetooth_csv_path, output_dir)
    export_kml(bluetooth_csv_path, output_dir)


if __name__ == "__main__":
    # === CONFIGURE PATHS ===
    # kismet_db_path = r'C:\Users\anthony.b\Desktop\pcap\real_pcap\wifi\Kismet-20250305-18-02-38-1.kismet'
    kismet_db_path = input('Input the kismet db full file path: ')
    # output_dir = r'C:\Users\anthony.b\Desktop\pcap\real_pcap\wifi\kismet_output'
    output_dir = input('Input your target output directory: ')
    json_output_path = os.path.join(output_dir, 'kismet_data.json')
    bluetooth_csv_path = os.path.join(output_dir, 'bluetooth_devices.csv')
    
    run_analyze_bluetooth(kismet_db_path, output_dir, bluetooth_csv_path, json_output_path)
