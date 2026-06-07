# RAT Builder Sources & Techniques Reference

## Overview
Compiled from GitHub Topics: `rat-builder` (28 repositories), plus cloned and analyzed repos: Vortex RAT, EgnakeRAT, Millenium RAT. Covers builder patterns, C2 architectures, evasion techniques, and payload capabilities.

---

## 1. RAT Builder Categories

### A. Windows Desktop RATs

| Repository | Author | Key Features |
|------------|--------|--------------|
| **Vortex-Advance-RAT (v2.0)** | Ansh-Vortex | Telegram bot control, 60+ commands, PyInstaller builder GUI, 4 persistence methods |
| **Res0luti0n** | Data3rr | Malware builder undetected by Windows Defender; anti-VM; triple-layer randomized obfuscation; malware partitioning; recompilation system (Python + C#) |
| **Millenium-RAT** | Shinyenigma-official | RAT builder with panel (focused on builder + C2 panel integration) |
| **Pulsar-RAT** | callertos | Undetected, modular, feature-rich C2 framework |
| **XWorm V7.2/V7.4** | sixruth, p0llsy, seanlitbeer | Widely distributed RAT builder variants |
| **Blx-Virus-Builder** | BenzoXdev | CustomTkinter GUI; Discord webhook; .py/.exe output; modular RAT/Backdoor/Ransomware configs |
| **Nebula-Trojan-Maker** | WaltuhJuhiow | Silent FUD system loader builder; credential harvesting; encrypted Python payloads; Windows privilege escalation |
| **ApocalypseRat** | A-CodeCreater | Windows remote administration via Telegram bot |
| **Pure-Rat** | Elementdibarrier | Full working Pure RAT, patched for local work; builder + panel |
| **RAT-Collection** | Pyran1 | 260+ RAT builders collected in one repo |

### B. Android RATs

| Repository | Author | Key Features |
|------------|--------|--------------|
| **EgnakeRAT** | egnake | Advanced Android C2; AES-256-CBC encryption; DOM keylogging; E2EE notification interception; Flask+Socket.IO dashboard |
| **Curse_Rat** | thorthehacker111 | Android RAT with Node.js C2, Java client, Smali-surgery APK builder |
| **EchoRat** | pub-master | Modular Android remote access framework for cybersecurity research and red teaming |

### C. Non-Windows/Cross-Platform

| Repository | Author | Key Features |
|------------|--------|--------------|
| **iOS-kernel-UAF** | programmens | PoC demonstrating UAF in XNU kernel on iOS (tagged under rat-builder) |
| **FRPUI** | abboodan | Windows Forms GUI for FRP tunnel configuration (.NET/C#) |

---

## 2. Vortex RAT - Deep Dive

### Architecture:
- **Control channel:** Telegram Bot API (polling-based)
- **Builder:** Python Tkinter GUI (builder.py) → PyInstaller compilation
- **Client:** Python script compiled to .exe via PyInstaller
- **Persistence:** 4 methods via `/startup` command

### Builder Techniques:
- Template-based: builder.py reads client.py template, injects BOT_TOKEN + ADMIN_ID
- PyInstaller compilation: `--onefile --noconsole --clean` flags
- Icon customization: .ico file embedding
- Output: `/output/` directory with compiled .exe
- Standalone builder packaging: builder itself can be compiled via PyInstaller with `--add-data "client.py;."`

### Command Categories (60+ commands):
| Category | Commands |
|----------|----------|
| System | shell, admincheck, sysinfo, whoami, shutdown, restart, logoff, lock, sleep, listprocess, prockill, idletime, installed, services |
| File Management | cd, dir, currentdir, download, upload, uploadlink, delete, copy, move, rename, mkdir, openfile, drives, search, encrypt/decrypt (XOR) |
| Interaction | message, fakeerror, voice (TTS), write (keyboard), wallpaper, website, audio, popup, volumeup/down, mute, monitors_off |
| Surveillance | screenshot, clipboard, setclipboard, getcams, selectcam, webcampic, geolocate, record (mic), keylog, stopkeylog, passwords |
| Network | wifilist, wifipasswords, ipconfig, netstat, env |
| System Control | blocksite, unblocksite, disabletaskmgr, enabletaskmgr, disabledefender, enabledefender, disablefirewall, enablefirewall, hidetaskbar, showtaskbar, hidedesktop, showdesktop, swap_mouse, bluescreen, critproc |

### Persistence Methods:
1. **HKCU Registry Run key** (Current User, no admin required)
2. **Startup Folder** (VBS/BAT script, Current User, no admin required)
3. **Scheduled Task** (on logon trigger, Current User)
4. **HKLM Registry Run key** (All Users, requires admin)

### Multi-Device Support:
- Device ID: hash of hostname + username + MAC
- Device tags: `[HOSTNAME | username]` prefix
- Auto-reconnect: retry logic for network delays after reboot
- Dual notification: `🟢 Client Started` for fresh launch, `🔄 Machine Back Online` for reconnection

### Dependencies:
```
pyTelegramBotAPI, Pillow, pyttsx3, pyautogui, opencv-python,
pyperclip, requests, pystray, pyinstaller, psutil, pycaw,
comtypes, pyaudio, keyboard, pycryptodome
```

---

## 3. EgnakeRAT - Deep Dive (Android)

### Architecture:
```
┌──────────────┬──────────────────┬───────────────────────┐
│ C2 TCP Server│  Web Dashboard   │  Android Client       │
│ (asyncio)    │  (Flask+SIO)     │  (Java/Kotlin)        │
└──────────────┴──────────────────┴───────────────────────┘
```

### C2 Server (server/c2_server.py):
- **asyncio.start_server** — fully async, coroutine-per-connection
- StreamReader/StreamWriter for TCP communication
- Handles handshake → heartbeat → command dispatch
- Ngrok tunnel support via pyngrok

### Cryptographic Layer (server/crypto.py):
- **AES-256-CBC** encryption
- **SHA-256 key derivation** from passphrase
- **Random IV** prepended to ciphertext (16 bytes)
- **Base64 encoding** after encryption
- Key hash verification: `MD5(SHA256(passphrase))` sent during handshake
- Default passphrase: `"EgnakeRAT_v2_SecureKey_2026"`

### Wire Protocol (server/protocol.py):
```
┌────────────┬──────────────────────────────────┐
│ 4 bytes    │ N bytes                          │
│ Length (BE)│ AES-256-CBC(JSON payload)        │
└────────────┴──────────────────────────────────┘
```
- Length-prefixed framing (4-byte big-endian header)
- Max message size: 50MB
- JSON payload types: handshake, heartbeat, command, response, stream, shell_io, disconnect, keylog, screen_frame, notification_data

### Handshake Flow:
1. Client connects TCP
2. Client sends `handshake` message: `{device_id, model, android_version, key_hash}`
3. Server verifies `key_hash == MD5(SHA256(passphrase))`
4. Server responds `handshake_ack`
5. Client enters heartbeat loop

### Web Dashboard:
- **Flask + Socket.IO** for real-time events
- Dark glassmorphism UI with Lucide icons
- Modules: Tactical commands, Remote shell, Keylogger, Screen stream, Notification intercept, File exfiltration, Audit log
- **Payload generator** — configure and patch APK from browser
- **Leaflet.js** global map for device geolocation

### Android Client Capabilities:
| Category | Commands |
|----------|----------|
| Recon | deviceInfo, getBatteryStatus, getWifiInfo, getIP, getMACAddress, getSimDetails, getInstalledApps, getClipData |
| Surveillance | getLocation, getSMS, getCallLogs, getContacts, getNotifications |
| Media | camList, takepic, screenshot, startAudio/stopAudio, startVideo/stopVideo |
| Live Interaction | startScreenStream/stopScreenStream, makeCall, sendSMS, openUrl, showToast, vibrate, lockScreen |
| Shell & Files | shell, shellCmd, fileList, fileDownload, fileUpload, fileDelete |
| Accessibility | startKeylogger/stopKeylogger, readScreen, performAction, checkAccessibility, enableAccessibility |

### Builder:
- CLI-based: `python EgnakeRAT.py build -i <IP> -p <PORT> -k <KEY>`
- Patches `config.java` with C2 IP/port/passphrase
- APK built via Android Studio or `./gradlew assembleRelease`
- Ngrok tunnel auto-resolution for external C2

---

## 4. Res0luti0n - Evasion Techniques

- **Triple-layer randomized obfuscation system** — nested code transformations
- **Malware partitioning system** — splits payload across multiple stages
- **Recompilation system** — recompiles code at build time with varying structure
- **Anti-VM detection** — detects virtualized environments
- **Python + C# hybrid** — cross-language evasion
- **Undetected by Windows Defender** (claim)

---

## 5. Other Notable RAT Builders

### Curse_Rat (Android):
- Node.js C2 server
- Java-based Android client
- **Smali-surgery APK builder** — modifies Smali bytecode directly rather than recompiling from source
- Smali patching allows injecting payload into existing APKs

### Nebula-Trojan-Maker:
- FUD (Fully Undetectable) system loaders
- Encrypted Python payloads
- Native Windows privilege escalation
- Credential harvesting focus

### Blx-Virus-Builder:
- CustomTkinter GUI (modern Python UI)
- Discord webhook for exfiltration
- Output formats: .py or .exe
- Customizable icon
- Modular configs: RAT, Backdoor, Ransomware modes
- Built-in decipher and bot operator

---

## 6. Common RAT Builder Patterns

### Builder Architecture Pattern:
```
┌──────────────┐     ┌───────────────┐     ┌──────────────────┐
│ Builder GUI  │ --> │ Config Inject │ --> │ Compiler/Packer  │
│ (Tkinter/CLI)│     │ (template +   │     │ (PyInstaller/    │
│              │     │  IP/PORT/KEY) │     │  Gradle/VS)      │
└──────────────┘     └───────────────┘     └──────────────────┘
                                                    │
                                                    ▼
                                           ┌──────────────────┐
                                           │ Output Payload   │
                                           │ (.exe / .apk)    │
                                           └──────────────────┘
```

### C2 Communication Patterns:
| Pattern | Example | Pros | Cons |
|---------|---------|------|------|
| Telegram Bot API | Vortex RAT | No infrastructure needed; encrypted; hard to block | Rate limits; poll-based latency |
| Raw TCP | EgnakeRAT | Low latency; full control | Detectable; needs open port |
| HTTP/HTTPS | XWorm, Pulsar | Blends with web traffic | Higher overhead |
| Discord Webhook | Blx-Virus-Builder | Free; simple | Rate limited; logs exposed |
| Ngrok Tunnel | EgnakeRAT | Dynamic public endpoint | Third-party dependency |

### Payload Compilation Techniques:
- **PyInstaller:** `--onefile --noconsole --clean --icon`
- **Gradle/Android Studio:** `assembleRelease` for APK
- **Smali Surgery:** Direct bytecode injection into existing APKs
- **MSBuild/Visual Studio:** .NET/C# payloads
- **Template-based:** Read client template → string replace IP/PORT/KEY → output final payload

### Persistence Mechanisms (Windows):
1. Registry: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
2. Registry: `HKLM\Software\Microsoft\Windows\CurrentVersion\Run` (admin)
3. Startup Folder: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`
4. Scheduled Tasks: `schtasks /create /sc onlogon`
5. Service Installation: `sc create` (admin)

### Persistence Mechanisms (Android):
1. Foreground Service with persistent notification
2. Accessibility Service (survives app kills)
3. Boot Receiver (BOOT_COMPLETED broadcast)
4. Device Admin (harder to uninstall)

---

## 7. Defense & Detection Indicators

### Network Indicators:
- Persistent TCP connections to non-standard ports
- Encrypted non-TLS traffic patterns
- Periodic heartbeat/beacon packets
- Telegram/Discord API calls from non-browser processes
- DNS queries for ngrok/portmap/serveo domains

### Host Indicators (Windows):
- Suspicious PyInstaller-compiled executables (high entropy sections)
- New registry Run keys
- Unscheduled task creation
- Unusual Python/script process trees
- Keyboard/mouse hook DLLs

### Host Indicators (Android):
- Apps requesting `BIND_ACCESSIBILITY_SERVICE`
- Background services consuming battery
- Apps with `RECEIVE_BOOT_COMPLETED` + `INTERNET` permissions
- Screen recording/casting permissions
- Notification listener services

---

## 8. Complete RAT Collection Reference

From Pyran1/RAT-Collection: 260+ RAT builders catalogued. The most commonly represented families:
- **XWorm** (multiple versions: 7.2, 7.4)
- **Pure RAT**
- **Pulsar RAT**
- **Vortex RAT**
- **AsyncRAT**
- **QuasarRAT**
- **NjRAT**
- **DarkComet**
- **BlackShades**
- **Poison Ivy**
