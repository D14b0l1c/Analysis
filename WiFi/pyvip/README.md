### Wi-Fi Attack Detection and pyVIP Visualization

This toolkit provides detection and visualization scripts for common Wi-Fi attacks using `.pcap` files and integrates with **Virtualitics Explore** via the **pyVIP API** (Virtualitics' Python interface for Predict apps).

---

## Requirements

- [TShark](https://www.wireshark.org/docs/man-pages/tshark.html) (installed and on PATH)
- Python 3.8+
- [`pyVIP`](https://api.virtualitics.com/) (Virtualitics' Python API)
- `pandas`

---

## Included Scripts

| Script                             | Attack Type     | Description                                        |
|-----------------------------------|-----------------|----------------------------------------------------|
| `pyvip_DeAuthAttackDetection.py`  | Deauthentication| Identifies MACs sending deauth packets             |
| `pyvip_EAPOLReplayAttackDetection.py` | EAPOL Replay  | Counts replayed EAPOL handshakes                   |
| `pyvip_EvilTwinDetection.py`      | Evil Twin       | Detects SSIDs advertised by multiple BSSIDs        |
| `pyvip_RogueAPDetection.py`       | Rogue AP        | Flags SSIDs not present in a known whitelist       |

---

## Usage

Each script follows a standard interactive flow:

1. **Provide your pyVIP API token** – used for authentication with the Virtualitics platform
2. **Enter the path to your `.pcap` file**
3. **Optionally provide extra input (e.g., whitelist SSIDs)**
4. **Script will export CSVs and push visualizations to Virtualitics Explore**

> 🔗 Learn more about `pyVIP` methods, authentication, and app-building via the [Virtualitics API Reference](https://api.virtualitics.com/).

---

## Examples

### 1. Deauthentication Detection

```bash
python pyvip_DeAuthAttackDetection.py
```

- Prompts for `.pcap`
- Summarizes deauth frame senders (`wlan.sa`)
- Visualizes with bar chart

---

### 2. EAPOL Replay Detection

```bash
python pyvip_EAPOLReplayAttackDetection.py
```

- Extracts EAPOL handshake packets
- Aggregates counts per source MAC
- Useful for detecting key replays

---

### 3. Evil Twin Detection

```bash
python pyvip_EvilTwinDetection.py
```

- Extracts SSID+BSSID combos
- Flags when one SSID is broadcast by multiple BSSIDs
- Visualized by number of BSSIDs per SSID

---

### 4. Rogue AP Detection

```bash
python pyvip_RogueAPDetection.py
```

When prompted:

```
Enter known SSIDs (comma-separated): MyHomeWiFi,CorpSSID,IoT_Zone
```

- Flags access points with unknown SSIDs
- Adds whitelist column to output
- Visualizes `wlan.ssid` vs `wlan.bssid` in bar chart

---

## Output

Each script will save results to the `output/` directory (e.g., `deauth_results.csv`) and push the dataset to Virtualitics Explore.
