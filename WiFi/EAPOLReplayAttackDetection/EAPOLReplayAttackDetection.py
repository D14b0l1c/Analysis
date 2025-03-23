import subprocess
from collections import defaultdict

pcap_file = "wifi_anomalies.pcap"

# Step 1: Check if the PCAP contains Wi-Fi traffic (frame.encap_type == 23)
pcap_type_cmd = ["tshark", "-r", pcap_file, "-T", "fields", "-e", "frame.encap_type"]
pcap_type_result = subprocess.run(pcap_type_cmd, capture_output=True, text=True)
pcap_type = set(pcap_type_result.stdout.strip().split("\n"))

if "23" in pcap_type:  # 23 = Wi-Fi
    print("\n PCAP contains Wi-Fi traffic. Checking for EAPOL Replay Attacks...")

    # Step 2: Extract EAPOL packets and check for repeated sources
    cmd = [
        "tshark", "-r", pcap_file,
        "-Y", "eapol",
        "-T", "fields",
        "-e", "wlan.sa",   # Source MAC address
        "-e", "eapol.type" # EAPOL message type
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Step 3: Process the output
    eapol_counts = defaultdict(int)
    for line in result.stdout.strip().split("\n"):
        if line and "\t" in line:
            mac_address, eapol_type = line.split("\t")
            eapol_counts[mac_address] += 1

    # Step 4: Detect repeated EAPOL packets (indicating replay attacks)
    found = False
    for mac, count in eapol_counts.items():
        if count > 3:  # Threshold: More than 3 repeated EAPOL messages
            found = True
            print(f" Possible EAPOL Replay Attack detected: {count} EAPOL messages from {mac}")

    if not found:
        print(" No EAPOL Replay Attack Found.")
else:
    print("\n This PCAP does not contain Wi-Fi traffic. EAPOL Replay detection skipped.")