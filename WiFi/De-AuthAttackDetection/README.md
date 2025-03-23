# Deauthentication Attack Detection

This script detects deauthentication attacks in PCAP files by analyzing 802.11 Wi-Fi traffic for deauth frames.

---

## Requirements

- Python 3.x  
- TShark (part of the Wireshark suite)

---

## Input

- A PCAP file named `wifi_anomalies.pcap` must be present in the same directory or referenced correctly in the script.

---

## Usage

```bash
python De-AuthAttackDetection.py
```

**Output Example:**

```
PCAP contains Wi-Fi traffic. Checking for Deauthentication Attacks...
Deauthentication Attack Detected! Possible MAC addresses involved:
00:11:22:33:44:55 -> ff:ff:ff:ff:ff:ff
```

---

## How It Works

- Uses TShark to check for 802.11 deauthentication frames (`wlan.fc.type_subtype == 0x0C`)
- Extracts MAC addresses from source and destination fields
- Flags a potential deauthentication attack when these frames are found

---

## Notes

This is a lightweight, fast way to detect basic deauthentication attacks. It works best as a first-pass scan on 802.11 traffic.
