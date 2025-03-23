# Evil Twin Detection

This script detects Evil Twin attacks by identifying multiple BSSIDs (MAC addresses) broadcasting the same SSID from a PCAP file.

---

## Requirements

- Python 3.x  
- TShark  
- Python standard library: `binascii`

---

## Input

- A PCAP file named `wifi_anomalies.pcap` must be present in the same directory or referenced correctly in the script.

---

## Usage

```bash
python EvilTwinDetection.py
```

**Output Example:**

```
PCAP contains Wi-Fi traffic. Checking for Evil Twin Attacks...

Possible Evil Twin Attack Detected: SSID 'PublicWiFi' is being broadcasted by multiple BSSIDs:
 - BSSID: 00:11:22:33:44:55
 - BSSID: 66:77:88:99:AA:BB
```

---

## How It Works

- Extracts beacon frames using TShark
- Parses SSID and BSSID from each beacon
- Flags SSIDs that are advertised by more than one BSSID

---

## Notes

Evil Twin attacks trick users into connecting to rogue access points with matching SSIDs. This script helps identify overlapping SSID broadcasts that may indicate such a threat.
