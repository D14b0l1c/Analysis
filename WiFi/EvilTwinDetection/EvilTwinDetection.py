import subprocess
from collections import defaultdict
import binascii

pcap_file = "wifi_anomalies.pcap"

# Step 1: Check if the PCAP contains Wi-Fi traffic (frame.encap_type == 23)
pcap_type_cmd = ["tshark", "-r", pcap_file, "-T", "fields", "-e", "frame.encap_type"]
pcap_type_result = subprocess.run(pcap_type_cmd, capture_output=True, text=True)
pcap_type = set(pcap_type_result.stdout.strip().split("\n"))

if "23" in pcap_type:  # 23 = Wi-Fi
    print("\n PCAP contains Wi-Fi traffic. Checking for Evil Twin Attacks...")

    # Step 2: Extract SSIDs and BSSIDs
    cmd = [
        "tshark", "-r", pcap_file,
        "-Y", "wlan.fc.type_subtype == 0x08",  # Only check Beacon frames (SSID advertisements)
        "-T", "fields",
        "-e", "wlan.ssid",   # Extract SSID
        "-e", "wlan.bssid"   # Extract BSSID
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Step 3: Process the output (Decode Hex SSIDs)
    bssid_counts = defaultdict(set)

    for line in result.stdout.strip().split("\n"):
        if line and "\t" in line:
            ssid_hex, bssid = line.split("\t")
            try:
                ssid = binascii.unhexlify(ssid_hex).decode("utf-8", "ignore")  # Convert hex to text
            except binascii.Error:
                ssid = ssid_hex  # If conversion fails, use the raw value
            bssid_counts[ssid].add(bssid)

    # Step 4: Detect Evil Twin (More than 1 BSSID per SSID)
    found = False
    for ssid, bssids in bssid_counts.items():
        if len(bssids) > 1:  # More than one unique BSSID broadcasting the same SSID
            found = True
            print(f"\n Possible Evil Twin Attack Detected: SSID '{ssid}' is being broadcasted by multiple BSSIDs:")
            for bssid in bssids:
                print(f"   - BSSID: {bssid}")

    if not found:
        print("\n No Evil Twin Attack Found.")
else:
    print("\n This PCAP does not contain Wi-Fi traffic. Evil Twin detection skipped.")