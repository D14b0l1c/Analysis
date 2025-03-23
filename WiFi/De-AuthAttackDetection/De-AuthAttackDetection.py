import subprocess

pcap_file = "wifi_anomalies.pcap"

# Check PCAP type
pcap_type_cmd = ["tshark", "-r", pcap_file, "-T", "fields", "-e", "frame.encap_type"]
pcap_type_result = subprocess.run(pcap_type_cmd, capture_output=True, text=True)
pcap_type = set(pcap_type_result.stdout.strip().split("\n"))

if "23" in pcap_type:
    print("\n PCAP contains Wi-Fi traffic. Checking for Deauthentication Attacks...")
    
    cmd = [
        "tshark", "-r", pcap_file,
        "-Y", "wlan.fc.type_subtype == 0x0C",
        "-T", "fields",
        "-e", "wlan.sa",
        "-e", "wlan.da"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout.strip():
        print(" Deauthentication Attack Detected! Possible MAC addresses involved:")
        print(result.stdout)
    else:
        print(" No Deauthentication Attack Found.")
else:
    print("\n This PCAP does not contain Wi-Fi traffic. Deauth detection skipped.")