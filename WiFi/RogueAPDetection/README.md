# Rogue Access Point Detection

This script detects unauthorized (rogue) access points by comparing broadcasted SSIDs in a PCAP file against a predefined whitelist.

---

## Requirements

- Python 3.x  
- TShark  
- Python standard library: `binascii`

---

## Input

- A PCAP file named `wifi_anomalies.pcap` must be present in the same directory or referenced correctly in the script.
- Modify the `whitelist_ssids` variable in the script to include your trusted SSID names.

---

## Usage

```bash
python RogueAPDetection.py
```

**Output Example:**

```
PCAP contains Wi-Fi traffic. Checking for Rogue APs...

Rogue Access Points Detected:
 - SSID: EvilNetwork, BSSID: 66:77:88:99:AA:BB (Not in trusted SSID list!)
```

---

## How It Works

- Extracts beacon frames using TShark
- Decodes SSID and BSSID pairs
- Flags SSIDs not in the predefined trusted list

---

## Notes

This tool is ideal for environments where SSID names are tightly controlled. It can help identify unauthorized devices attempting to mimic or bypass network policy.
