# 🌐 Home Network Scanner

A command-line cybersecurity tool to scan your home network, discover live hosts, and identify open ports and risky services — built with pure Python, no external libraries needed.

> ⚠️ **Ethical Use Only** — Only scan networks you own or have permission to scan.

## 🛡️ Features

- ✅ Auto-detects your local IP and network range
- ✅ Ping sweep to discover all live devices on your network
- ✅ Port scanning across 17 common ports (FTP, SSH, HTTP, RDP, etc.)
- ✅ Flags risky open ports (Telnet, RDP, SMB, VNC, FTP)
- ✅ Resolves hostnames of discovered devices
- ✅ Saves a full scan report to a `.txt` file
- ✅ Three scan modes: Quick, Full, and Single IP

## 📸 Example Output

```
  ╔══════════════════════════════════════════════╗
  ║         HOME NETWORK SCANNER                 ║
  ║         by Kartik | Cybersecurity Tool       ║
  ╚══════════════════════════════════════════════╝

  Your IP Address : 192.168.1.5
  Network Range   : 192.168.1.0/24

  ┌─ HOST: 192.168.1.1 (router.home)
  │   ◄ GATEWAY
  │  PORT     SERVICE        STATUS
  │  -----------------------------------
  │  80       HTTP             OK   
  │  443      HTTPS            OK   
  │  23       Telnet         ⚠ RISKY
  └────────────────────────────────────────
```

## 🚀 How to Run

**Requirements:** Python 3.x (no extra installs needed)

```bash
# Clone the repo
git clone https://github.com/yourusername/network-scanner.git
cd network-scanner

# Run the tool
python network_scanner.py
```

## 🗂️ Scan Modes

| Mode | What it does |
|---|---|
| Quick Scan | Ping sweep — finds all live devices on your network |
| Full Scan | Ping sweep + port scan on every live host |
| Single IP | Port scan a specific IP address |

## 🔴 Risky Ports Flagged

| Port | Service | Why it's risky |
|---|---|---|
| 21 | FTP | Transfers files in plaintext |
| 23 | Telnet | Sends all data unencrypted |
| 135 | MS-RPC | Common Windows attack target |
| 139 | NetBIOS | Old Windows sharing, exploitable |
| 445 | SMB | EternalBlue / WannaCry attack vector |
| 3389 | RDP | Remote Desktop — brute-force target |
| 5900 | VNC | Remote access, often unsecured |

## 🧰 Tech Stack

- **Language:** Python 3
- **Libraries:** `socket`, `subprocess`, `ipaddress`, `platform` (all built-in)

## 👤 Author

**Kartik** — QA Analyst | Cybersecurity Enthusiast  
📧 palkartik2005@gmail.com

## 📄 License

MIT License — free to use and modify.
