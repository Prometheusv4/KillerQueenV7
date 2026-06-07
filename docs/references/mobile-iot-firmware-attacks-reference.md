# Mobile, IoT, Firmware & Embedded Attacks — Killer Queen's Reference

> "If it runs code, I can own it. If it has memory, I can corrupt it. If it boots, I can persist in it."
> — Killer Queen

## PART A: MOBILE EXPLOITATION

## 1. iOS Exploitation

### 1.1 The iOS Security Model
```
App Sandbox → [App]
     ↓
XNU Kernel (with PAC, KASLR, KTRR/KPP)
     ↓
Secure Enclave (SEP) → Touch ID, Face ID, crypto keys
     ↓
Boot Chain: Boot ROM → iBoot → Kernel → Userland
```

### 1.2 iOS Attack Surface

**Remote Attack Vectors (no user interaction):**
- iMessage (most valuable — zero-click target)
- MMS (ImageIO, CoreGraphics parsers)
- Wi-Fi/Bluetooth baseband
- Airdrop, FaceTime, Mail

**Local Attack Vectors:**
- WebKit (Safari, all browsers on iOS)
- App Store apps (bypassing review)
- USB/Lightning (checkm8 era)
- Kernel drivers (IOKit)

### 1.3 Key iOS Exploit Primitives

**PAC (Pointer Authentication) Bypasses:**
- PAC signing gadget reuse (use existing signed pointers)
- PAC forgery via brute force (limited tries on A12+)
- PACless targets (older devices)
- JOP/ROP to avoid authentication

**KASLR Bypass:**
- Heap spray with predictable layout
- Side-channel information leaks
- Zone allocator determinism

**Sandbox Escape:**
- IOKit driver bugs (most common LPE vector)
- XPC service bugs
- Mach message trailer info leaks (CVE-2020-27950)
- cfprefsd (CVE-2019-7286)

### 1.4 Notable iOS 0-Day Chains
- **Project Zero iOS chain**: cfprefsd UAF → IOKit buffer overflow (2019)
- **Pwn2Own 2018**: Safari WASM bug → WebKit RCE → sandbox escape → kernel
- **Samsung Galaxy Store RCE (2020)**: WebView JavaScript interface → silent app installation

## 2. Android Exploitation

### 2.1 Android Security Model
```
App Sandbox (SELinux context per app)
     ↓
Android Framework (Binder IPC)
     ↓
Linux Kernel (+ Android patches, SELinux)
     ↓
TrustZone (TEE) → Keymaster, Fingerprint
     ↓
Boot Chain: Boot ROM → Bootloader → Kernel → Init
```

### 2.2 Android Attack Surface

**Remote:**
- Chrome/V8 bugs (most common remote vector)
- SMS/MMS (Stagefright era — media framework)
- WebView in apps (exposed JS interfaces)
- NFC (limited range but interesting)
- Wi-Fi/Bluetooth drivers

**Local:**
- Binder IPC (UAF in CVE-2019-2215 — direct kernel)
- GPU drivers (Qualcomm Adreno, Mali — massive attack surface)
- Vendor-specific drivers (Samsung NPU, Huawei)
- Filesystem race conditions

### 2.3 Android Kernel Exploitation Workshop Insights
- **Binder**: IPC mechanism between processes. Target for UAF, race conditions
- **ION/ION memory allocator**: GPU memory sharing → UAF targets
- **SELinux bypass**: Look for contexts that are too permissive
- **Vendor drivers**: Samsung, Qualcomm, MediaTek — each adds 100K+ lines of kernel code
- **Fuzzing targets**: syscalls, IOCTLs, netlink sockets, filesystem operations

### 2.4 Android LPE Methodology (from DUASYNT training)
```
1. Find a kernel vulnerability (fuzzing IOCTLs, reviewing patch diffs)
2. Determine exploit primitive (arbitrary read, arbitrary write, UAF)
3. Bypass mitigations:
   - KASLR → info leak (often from /proc or sysfs)
   - PXN/PAN → kernel RW only, no execute
   - CFI/SCS → target data structures, not control flow
4. Overwrite cred structure → set uid=0, gid=0, selinux context
5. Disable SELinux enforcement for full root
```

## PART B: FIRMWARE & UEFI EXPLOITATION

## 3. UEFI/BIOS Security

### 3.1 The UEFI Attack Surface
```
Pre-Boot:
  SPI Flash (firmware storage) → physical access = permanent persistence
  SMM (System Management Mode) → Ring -2, invisible to OS
  PEI/DXE phases → early boot code, no OS protections
  Secure Boot → bypass = boot arbitrary code
  ACPI tables → OS-trusted data from firmware
```

### 3.2 UEFI Bootkit Arsenal (Real-World Malware)
| Bootkit | Year | Technique |
|---------|------|-----------|
| **LoJax** | 2018 | First UEFI rootkit in wild. Flashed malicious DXE driver to SPI flash |
| **MosaicRegressor** | 2020 | Multi-component framework, UEFI persistence module |
| **TrickBoot** | 2020 | TrickBot UEFI module — brick-or-persist capability |
| **FinSpy** | 2021 | UEFI bootkit in commercial spyware |
| **Especter** | 2021 | Bootkit targeting ESP (EFI System Partition) |
| **MoonBounce** | 2022 | Hides in SPI flash, no ESP artifacts, advanced anti-detection |
| **CosmicStrand** | 2022 | UEFI firmware rootkit — persists across OS reinstall |
| **BlackLotus** | 2022 | First UEFI bootkit bypassing Secure Boot on Windows 11 |
| **Bootkitty** | 2024 | First Linux UEFI bootkit — targets Ubuntu |

### 3.3 UEFI Exploitation Techniques

**SMM (Ring -2) Exploitation:**
- SMM code runs with highest privilege, invisible to OS
- SMM handlers can be exploited if they reference attacker-controlled memory (SMM callout)
- Once in SMM: disable Secure Boot, write to SPI flash, install permanent implant

**Secure Boot Bypasses:**
- BlackLotus (2022): exploited CVE-2022-21894 (Baton Drop) — signed but revoked bootloader still accepted
- Shim vulnerabilities: many Linux shim versions had bypass bugs
- PK/KEK manipulation: if you can write to firmware variables, you control the trust chain

**SPI Flash Persistence:**
- Write directly to SPI flash (requires physical access or kernel privileges)
- Replace legitimate DXE driver with malicious one
- SMM backdoor (Cr4sh's SmmBackdoor)
- PEI backdoor (Cr4sh's PeiBackdoor)

### 3.4 UEFI Attack Tools
- **CHIPSEC**: Firmware security assessment framework
- **RWEverything**: Hardware register access from Windows
- **UEFITool**: Parse/extract/modify UEFI firmware images
- **umap**: Map UEFI modules to physical memory
- **UEFI-Bootkit**: Reference implementation for learning
- **DVUEFI**: Deliberately vulnerable UEFI for practice

## 4. IoT / Embedded Systems Exploitation

### 4.1 Attack Surface
```
Hardware:  UART, JTAG, SWD, SPI flash, I2C, GPIO
Firmware:  Bootloader (U-Boot), kernel, rootfs, application
Network:   HTTP, MQTT, CoAP, custom protocols
Radio:     Wi-Fi, BLE, Zigbee, LoRa, NFC, SDR
Cloud:     Backend API, MQTT broker, firmware update server
```

### 4.2 Hardware Hacking Toolkit
- **UART**: Universal Asynchronous Receiver/Transmitter — find the serial console
  - Look for 4-6 pin headers, test with multimeter (GND, VCC, TX, RX)
  - Common baud rates: 115200, 57600, 9600
  - Often gives root shell without authentication
  
- **JTAG/SWD**: On-chip debugging interfaces
  - Can halt CPU, read/write memory, extract firmware
  - JTAGulator: identify JTAG pinouts
  - OpenOCD + GDB: debug target chip

- **SPI Flash Dumping**:
  - Desolder or clip onto flash chip
  - Dump with flashrom or dedicated programmer
  - Extract filesystem, find hardcoded keys, reverse engineer

### 4.3 Firmware Extraction & Analysis
1. **Get the firmware**: Download from vendor, dump from flash, capture OTA update
2. **Unpack**: binwalk, FMK (Firmware Mod Kit), FACT extractor
3. **Analyze**: strings, grep for keys/secrets, check /etc/shadow, check hardcoded URLs
4. **Emulate**: QEMU user-mode or full-system emulation (Firmadyne, FIRMADYNE)
5. **Modify**: Change root password, add backdoor, repack, flash back

### 4.4 Common IoT Vulnerabilities
- **Hardcoded credentials**: root:root, admin:admin, vendor-specific backdoors
- **UART root shell**: Serial console with no authentication
- **Unencrypted firmware updates**: MITM the update, flash malicious firmware
- **Command injection**: CGI scripts passing user input to system()
- **Buffer overflows**: Custom network services written in C without protections
- **MQTT without auth**: Publish/subscribe to device topics → control devices
- **Default Wi-Fi/AP passwords**: Derived from SSID/MAC, algorithms published

## 5. ICS/SCADA Attacks

### 5.1 The ICS/SCADA Kill Chain
```
Recon → Initial Access → Network Enumeration → Process Manipulation → Impact
  ↓           ↓               ↓                     ↓                  ↓
Shodan     Phishing       ARP scan            Modify PLC logic    Physical damage
Censys     VPN vuln       Protocol scan       Spoof HMI values    Production halt
Google     IT→OT pivot    Device discovery     Disable safeties    Safety bypass
```

### 5.2 ICS Protocol Landscape
| Protocol | Port | Purpose | Attack Vectors |
|----------|------|---------|----------------|
| Modbus/TCP | 502 | PLC communication | Read/write coils (no auth), function code fuzzing |
| DNP3 | 20000 | SCADA comms | Replay attacks, unsolicited responses |
| PROFINET | 34964 | Siemens PLCs | Device discovery, program upload/download |
| EtherNet/IP | 44818 | Rockwell/CIP | Implicit messaging, tag manipulation |
| OPC UA | 4840 | Industrial interoperability | UAF in servers (Pwn2Own 2023), auth bypass |
| BACnet | 47808 | Building automation | Device discovery, property write |
| S7comm | 102 | Siemens S7 | Start/stop CPU, read/write program blocks |
| IEC 61850 | 102 | Power substations | GOOSE spoofing, MMS manipulation |

### 5.3 ICS Exploitation Tools
- **ISF (Industrial Exploitation Framework)** : Metasploit-style for ICS
  - Exploits for Siemens, Schneider, QNX, others
  - Protocol scanners and fuzzers
  
- **Redpoint (Digital Bond)** : Nmap scripts for ICS enumeration
  - Protocol-aware device discovery
  - Legitimate commands for enumeration (no crashes)
  
- **GRASSMARLIN**: Passive network mapping for ICS/SCADA
  - Visual topology mapping
  - Device fingerprinting by network behavior

- **AttkFinder**: Static analysis of PLC programs
  - Data-flow graph for IEC 61131-3 programs
  - Finds data-oriented attack vectors in PLC logic

### 5.4 Notable ICS Attacks
| Attack | Year | Technique | Impact |
|--------|------|-----------|--------|
| **Stuxnet** | 2010 | PLC code modification via Windows 0-days | Centrifuge destruction |
| **Havex** | 2013 | OPC scanning, trojanized ICS software installers | Reconnaissance |
| **BlackEnergy 2** | 2014 | HMI exploitation (GE Cimplicity) | Espionage |
| **BlackEnergy 3** | 2015 | SCADA → power grid disruption | Ukrainian blackout |
| **CRASHOVERRIDE** | 2016 | Modular ICS attack framework | Ukrainian blackout (automated) |
| **TRITON/TRISIS** | 2017 | Safety instrumented system (SIS) attack | Safety system compromise |
| **EKANS** | 2020 | Ransomware targeting ICS processes | Production halt |

### 5.5 ICS Attack Patterns
- **PLC logic modification**: Change ladder logic to operate dangerously
- **HMI spoofing**: Show operators normal values while process is in danger state
- **Safety system bypass**: TRITON targeted SIS directly — disable safety before dangerous operation
- **Firmware replacement**: Replace device firmware with malicious version
- **Protocol-level MITM**: Intercept and modify process values between PLC and HMI

## 6. RAT/Trojan Builders

The `rat-builder` topic on GitHub reveals the commodity malware ecosystem:

### Common RAT Builder Features:
- **Builder GUI**: Configure C2 address, port, persistence method, installation path
- **Persistence**: Registry Run, Scheduled Tasks, Startup folder, WMI event subscription
- **Evasion**: Process injection, obfuscation, anti-VM, anti-debug, AMSI bypass
- **C2**: HTTP/HTTPS, DNS tunneling, Telegram bot API, Discord webhooks
- **Payloads**: Keylogger, screen capture, file browser, reverse shell, webcam, password stealer

### Infection Vectors:
- Spearphishing attachment (ISO, VHD, VBS, HTA, LNK, Office macro)
- Drive-by download (browser exploit → download + execute)
- Malvertising (ad network → redirect to exploit kit)
- Fake software installers/cracks
- USB drop (autorun, LNK file)

## 7. Killer Queen's Hardware Domain Checklist

```
EMBEDDED/IoT:
[ ] Find UART console (check for root shell)
[ ] Dump SPI flash (extract firmware, find secrets)
[ ] Check for default credentials
[ ] Intercept firmware update (MITM or capture OTA)
[ ] Analyze firmware (binwalk + strings + grep)
[ ] Exploit web interface (command injection, etc.)
[ ] Attack MQTT broker (subscribe to topics, publish commands)

MOBILE:
[ ] Check for exposed JS interfaces in WebView apps
[ ] Test for deeplink/URL scheme hijacking
[ ] Look for exported Activities/Services in AndroidManifest
[ ] Fuzz IPC endpoints (Binder, XPC)
[ ] Target IOKit/GPU drivers for kernel LPE

UEFI/FIRMWARE:
[ ] Check Secure Boot status (if off: boot arbitrary OS)
[ ] Look for writable EFI variables
[ ] Check for SMM callout vulnerabilities
[ ] Extract firmware with CHIPSEC, look for secrets
[ ] If kernel access: write to SPI flash for persistence

ICS/SCADA:
[ ] Scan for Modbus (502), DNP3 (20000), S7 (102), EtherNet/IP (44818)
[ ] Test Modbus function codes (read coils, read holding registers)
[ ] Test for default/blank authentication on engineering software
[ ] Look for web-based HMI interfaces (often poorly secured)
[ ] Check for firmware download capability without auth
```
