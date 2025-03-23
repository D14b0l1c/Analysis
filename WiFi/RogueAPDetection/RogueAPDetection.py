import subprocess
from collections import defaultdict
import binascii

pcap_file = "wifi_anomalies.pcap"

# Step 1: Check if the PCAP contains Wi-Fi traffic (frame.encap_type == 23)
pcap_type_cmd = ["tshark", "-r", pcap_file, "-T", "fields", "-e", "frame.encap_type"]
pcap_type_result = subprocess.run(pcap_type_cmd, capture_output=True, text=True)
pcap_type = set(pcap_type_result.stdout.strip().split("\n"))

if "23" in pcap_type:  # 23 = Wi-Fi
    print("\n PCAP contains Wi-Fi traffic. Checking for Rogue APs...")

    # Step 2: Define a list of known trusted SSIDs (Modify this for your environment)
    whitelist_ssids = {"HomeWiFi", "OfficeAP", "SecureNetwork", "PublicWiFi"}

    # Step 3: Extract SSIDs and BSSIDs from Beacon frames
    cmd = [
        "tshark", "-r", pcap_file,
        "-Y", "wlan.fc.type_subtype == 0x08",  # Only check Beacon frames (SSID advertisements)
        "-T", "fields",
        "-e", "wlan.ssid",   # Extract SSID
        "-e", "wlan.bssid"   # Extract BSSID
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Step 4: Process the output (Decode Hex SSIDs)
    rogue_aps = []
    
    for line in result.stdout.strip().split("\n"):
        if line and "\t" in line:
            ssid_hex, bssid = line.split("\t")
            try:
                ssid = binascii.unhexlify(ssid_hex).decode("utf-8", "ignore")  # Convert hex to text
            except binascii.Error:
                ssid = ssid_hex  # If conversion fails, use the raw value

            if ssid not in whitelist_ssids:  # If the SSID is not in the trusted list, flag it
                rogue_aps.append((ssid, bssid))

    # Step 5: Report Rogue APs
    if rogue_aps:
        print("\n Rogue Access Points Detected:")
        for ssid, bssid in rogue_aps:
            print(f"   - SSID: {ssid}, BSSID: {bssid} (Not in trusted SSID list!)")
    else:
        print("\n No Rogue APs Detected.")
else:
    print("\n This PCAP does not contain Wi-Fi traffic. Rogue AP detection skipped.")