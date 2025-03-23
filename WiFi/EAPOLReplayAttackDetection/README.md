# EAPOL Replay Attack Detection

This script detects potential EAPOL (Extensible Authentication Protocol over LAN) replay attacks by analyzing repeated authentication exchanges from the same MAC address in Wi-Fi traffic.

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
python EAPOLReplayAttackDetection.py
```

**Output Example:**

```
PCAP contains Wi-Fi traffic. Checking for EAPOL Replay Attacks...
Possible EAPOL Replay Attack detected: 6 EAPOL messages from 00:11:22:33:44:55
```

---

## How It Works

- Filters for EAPOL packets in the PCAP (`eapol`)
- Tracks the number of repeated authentication messages by source MAC
- Flags a potential replay attack if the count exceeds a predefined threshold

---

## Notes

Replay attacks typically involve resending previously captured EAPOL frames to disrupt or hijack authentication processes. This detector highlights excessive EAPOL activity that could be malicious.
