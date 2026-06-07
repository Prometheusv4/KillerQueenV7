# Embedded, IoT, ICS, UEFI Security & Cloud Reference

## 1. Embedded Vulnerability Research (awesome-embedded-vuln.md)

### Essential Tools
| Tool | Purpose |
|------|---------|
| unblob | Firmware extraction engine, 100+ formats, fewer false positives than Binwalk |
| Binwalk | Firmware analysis, reverse engineering, extraction |
| Ghidra | Free NSA decompiler for most architectures (ARM, MIPS, x86, etc.) |
| IDA Pro | Commercial disassembler/decompiler (costs for decompilers) |
| Qiling Framework | Cross-platform binary emulation & instrumentation |
| Unicorn Engine | Lightweight multi-architecture CPU emulator (ARM, MIPS, x86, RISC-V) |
| QEMU | Full system emulator for firmware emulation |
| Buildroot | Cross-compiler toolchain builder |
| bugprove | Automatic firmware analysis platform |
| TritonDSE | Emulation & symbolic execution library (Quarkslab) |
| gdb-multiarch / gdbserver | Cross-architecture debugging |
| picocom/minicom/putty/screen | Serial interfacing for UART/console access |
| AFL++ | Coverage-guided fuzzer with QEMU/Unicorn modes |
| SVD-Loader for Ghidra | Hardware register definitions for firmware RE |
| cpu_rec | Identify CPU architecture from binary blob (Airbus) |
| binbloom | Analyze raw firmware to find load address, endianness (Quarkslab) |
| afl-unicorn | AFL fuzzing harness for Unicorn |
| SCOUT | Deterministic firmware-to-exploit evidence engine, 42-stage pipeline, SARIF + CycloneDX SBOM output |

### Hardware Debug Tools
| Tool | Interface |
|------|-----------|
| JTAGulator | Auto-discovery of JTAG, SWD, UART debug interfaces on PCBs |
| JTAGenum | Arduino-based JTAG pin enumeration via brute-force |
| OpenOCD | On-chip programming and debugging with JTAG/SWD support |
| pyOCD | Python library for Arm Cortex-M debugging |
| probe-rs | Rust-based SWD/JTAG debug toolkit with GDB server |
| Black Magic Probe | Open-source JTAG/SWD debugger with embedded GDB server |
| Bus Pirate | Multi-protocol (SPI, I2C, UART, 1-Wire, JTAG) |
| Tigard | FT2232H-based multi-protocol hardware hacking tool |
| Glasgow Interface Explorer | FPGA-based digital interface multitool |
| GreatFET | USB host-side hardware security platform |
| Hydrabus | Multi-protocol tool (SPI, I2C, UART, CAN, 1-Wire, JTAG) |
| Flipper Zero | Portable multi-tool for radio, access control, hardware |

### Firmware Extraction Methods
- SPI flash dumping (Bus Pirate, flashrom, Tigard)
- eMMC chip-off / in-system extraction (SNANDer, NANDO)
- UART console access to interrupt bootloader
- JTAG/SWD debugger memory dumping
- Firmware update interception (network capture)
- Encrypted firmware decryption (static analysis + key extraction)
- U-Boot shell access (interrupt autoboot)
- ChipWhisperer for glitching readout protection

### Attack Techniques
| Technique | Description |
|-----------|-------------|
| **Voltage Fault Injection (Glitching)** | Momentary voltage drop to bypass security checks, readout protection |
| **Electromagnetic Fault Injection (EMFI)** | EM pulse to induce faults, bypass secure boot |
| **Side-Channel Analysis (SCA)** | Power analysis (CPA/DPA), timing attacks against crypto |
| **UART Exploitation** | Finding serial console pads, accessing root shells, bypassing login |
| **JTAG/SWD Debugging** | Halt CPU, dump memory, flash modification, bypass code protection |
| **SPI Flash Dumping** | Direct flash chip reading via SOIC clips or desoldering |
| **I2C Sniffing/Injection** | Intercepting sensor/EEPROM communication |
| **Firmware Reverse Engineering** | Static analysis (Ghidra/IDA), emulation (QEMU/Qiling), fuzzing |
| **Bootloader Attacks** | U-Boot shell, modifying bootargs, loading unsigned kernels |
| **Secure Boot Bypass** | NVRAM variable manipulation, leaked signing keys, TOCTOU in verification |
| **ROP/JOP Exploitation** | ARM/MIPS return-oriented programming on embedded Linux |
| **CAN Bus Attacks** | CAN injection for car hacking, arbitration ID spoofing |

### Key MCU Fuzzing Tools
| Tool | Description |
|------|-------------|
| Fuzzware | MMIO peripheral modeling via symbolic execution for Cortex-M fuzzing |
| uEmu | Peripheral behavior inference for bare-metal fuzzing |
| SAFIREFUZZ | Dynamic binary rewriting for ARM firmware fuzzing (600x speedup) |
| HALucinator | HAL function replacement for firmware emulation |
| uAFL | Hardware-in-the-loop fuzzer using ARM ETM trace |
| DICE | DMA input channel emulation for fuzzing |
| Icicle | Rust-based grey-box fuzzer (MSP430, RISC-V support) |
| GDBFuzz | GDB hardware breakpoints as coverage for uninstrumented targets |

### Fault Injection Platforms
| Tool | Type |
|------|------|
| ChipWhisperer | Power analysis + voltage/clock glitching |
| PicoGlitcher | RP2040-based voltage glitching, 66A crowbar, sub-10ns resolution |
| PicoEMP | Entry-level EMFI tool (Raspberry Pi Pico + flash transformer) |
| ChipSHOUTER | Full-featured EMFI platform |
| EM-Fault-It-Yourself | Motorized XYZ-stage EMFI, attacked AMD Secure Processor |

---

## 2. ICS/SCADA Security (awesome-ics-scada.md)

### ICS-Specific Protocols
| Protocol | Description | Security Notes |
|----------|-------------|----------------|
| **Modbus (RTU/TCP)** | Legacy serial/TCP industrial protocol, function codes for read/write coils/registers | No authentication, no encryption, trivial MITM |
| **DNP3** | IEEE-1815, used in electric/water utilities | OpenDNP3 reference implementation, Secure Authentication v5 adds challenge-response |
| **OPC-UA** | Modern industrial interoperability standard | Supports encryption and authentication, but complex implementation leads to vulnerabilities |
| **S7comm** | Siemens proprietary protocol for S7 PLCs | Snap7/S7comm-Analyzer for enumeration and exploitation |
| **EtherNet/IP** | Common Industrial Protocol over Ethernet | Often exposed without authentication |
| **IEC 61850** | Substation automation (GOOSE, MMS, SV) | Time-critical, difficult to add security retroactively |
| **BACnet** | Building automation and HVAC control | Commonly internet-exposed, weak/default credentials |
| **PROFINET** | Siemens industrial Ethernet | Real-time requirements limit security options |
| **HART** | Highway Addressable Remote Transducer | Hybrid analog/digital, wireless HART adds attack surface |
| **CODESYS** | IEC 61131-3 runtime for PLCs | PLC runtime with known vulnerabilities, ICSREF for RE |

### ICS-Specific Tools
| Tool | Purpose |
|------|---------|
| ISF (Industrial Exploitation Framework) | Metasploit-like exploitation for PLCs (QNX, Siemens, Schneider) |
| ISEF (Industrial Security Exploitation Framework) | Based on Equation Group Fuzzbunch toolkit |
| GRASSMARLIN | Passive ICS/SCADA network mapping and visualization |
| CSET (Cyber Security Evaluation Tool) | Systematic security posture assessment |
| AttkFinder | Static PLC program analysis, data-oriented attack vectors |
| ICSREF | CODESYS binary reverse engineering automation |
| ICSFuzz | PLC-side fuzzing for CODESYS/Wago platforms |
| MiniCPS | Cyber-Physical Systems security research toolkit (SUTD) |
| smod | Full Modbus penetration testing framework (Python/Scapy) |
| plcscan | PLC scanning over s7comm and modbus |
| Redpoint | Nmap extensions for ICS device enumeration |
| Digital Bond 3S CoDeSys Tools | Command shell, file transfer, NMap script for CoDeSys PLCs |
| mbtget | Modbus transactions from CLI (Perl) |
| Quickdraw IDS | Snort rules + preprocessors for SCADA protocols |
| SCADAShutdownTool | SCADA enumeration and register read/write testing |
| sixnet-tools | Exploit Sixnet RTUs with undocumented function codes |
| S7 Password Bruteforcer | Offline S7 password cracking from PCAP |
| Conpot | Low-interactive ICS honeypot (Modbus, S7, BACnet, etc.) |
| GasPot | Gas station tank gauge honeypot |
| Kamerka GUI | IoT/ICS reconnaissance tool |
| splonebox | Modular network assessment with ICS protocol plugins |

### ICS Attack Vectors
- PLC logic manipulation (data-oriented attacks)
- Protocol-level MITM (Modbus, DNP3 without auth)
- Firmware backdooring/replacement
- Engineering workstation compromise
- HMI exploitation (web-based HMIs with XSS/CSRF)
- Safety Instrumented System (SIS) attacks (TRISIS/TRITON malware)
- Supply chain attacks on ICS vendors
- IT-OT pivot (from corporate network to control network)

### Key Malware
- **TRISIS/TRITON/HATMAN**: Targeted Triconex SIS controllers, designed to cause physical damage
- **Stuxnet**: First known ICS-specific weapon, targeted Siemens S7-300 PLCs
- **BlackEnergy/Industroyer**: Ukrainian power grid attacks
- **Havex**: OPC scanning and data exfiltration

### ICS-Specific Frameworks
- **ATT&CK for ICS** (MITRE): Adversary tactics and techniques for ICS environments
- **ICS Cyber Kill Chain**: Two-phase attack model (Stage 1: IT intrusion, Stage 2: OT attack)
- **NIST SP 800-82 r2**: Guide to Industrial Control Systems Security
- **IEC 62443**: Series of standards for IACS security

### ICS Honeypots
- **Conpot**: Low-interactive, supports Modbus, S7, BACnet, HTTP, SNMP, IPMI
- **GasPot**: Simulates Veeder Root Guardian AST tank gauges
- **T-Pot**: Multi-honeypot platform including Conpot

### ICS Distributions
- **Moki Linux**: Kali modification with ICS/SCADA tools
- **ControlThings Platform** (formerly SamuraiSTFU): ICS security assessment Linux distro

### ICS Education / Labs
- **GRFICSv2**: Unity 3D ICS simulation with attack scenarios (command injection, MITM, buffer overflow)
- **LICSTER**: Low-cost ICS Security Testbed for Education and Research

### ICS-Specific Conferences
- CS3STHLM (Stockholm ICS Security Summit)
- SANS ICS Summit series
- Kaspersky Industrial Cybersecurity Conference (KICS con)
- ICCPS (ACM/IEEE Cyber-Physical Systems)
- CyberICPS, CPSIoTSec, CPSS workshops

---

## 3. Embedded Security (awesome-embedded-security.md)

### Binary Analysis Tools
| Tool | Function |
|------|----------|
| Kaitai Struct | Declarative binary format description language |
| OFRAK | Unpack, analyze, modify, repack binaries |
| LIEF | Parse/modify ELF, PE, Mach-O, DEX, OAT |
| checksec | Check binary hardening (NX, PIE, RELRO, stack canary, ASLR) |
| firmwalker | Searches extracted firmware for credentials, configs, vulns |
| SCOUT | 42-stage deterministic firmware analysis pipeline |
| cwe_checker | Cross-architecture CWE violation detection |
| FLARE-FLOSS | Obfuscated string extraction from binaries |
| argXtract | Static SVC/HAL argument extraction from ARM Cortex-M BLE |

### Disassemblers/Decompilers
- Ghidra, IDA Pro, Binary Ninja, Cutter/Rizin, radare2, Angr, Capstone, Keystone, BARF, RetDec, Vivisect

### Debugging Tools
- OpenOCD, GDB/GEF, Black Magic Probe, pyOCD, probe-rs, Frida (dynamic instrumentation)

### Secure Boot & Trust
- MCUboot: Signed images, rollback protection, measured boot for 32-bit MCUs
- Android Verified Boot (AVB): Chained trust and verified partitions
- U-Boot Verified Boot: FIT-signature verified boot
- wolfBoot: Portable secure bootloader with Ed25519/ECC/RSA/PQ, voltage-glitch countermeasures

### Firmware Supply Chain / SBOM
- in-toto: Signed provenance for supply chain integrity
- Sigstore Cosign: Keyless signing and verification
- Syft: SBOM generator for firmware
- Grype: Vulnerability scanner consuming SBOMs

### Fuzzing Tools
- AFL++, honggfuzz, Fuzzowski, Peach, libFuzzer, boofuzz, GDBFuzz

### Firmware Taint Analysis
- KARONTE: Cross-binary taint propagation using angr (IEEE S&P 2020)
- SaTC: String-anchored taint analysis, found 33 bugs (USENIX Security 2021)
- EmTaint: Structured symbolic taint analysis, found 151 0-days (ISSTA 2023)

### RTOS Security
- FreeRTOS: MQTT over TLS, PKCS#11, PSA Certified
- Zephyr: TF-M integration, verified boot
- RT-Thread: Security resources for IoT OS
- seL4: Formally verified microkernel (functional correctness, integrity, confidentiality proofs)
- Tock OS: Rust-based, hardware-enforced memory isolation, Cortex-M/RISC-V

### TEE / Trusted Execution Environments
- OP-TEE: Open-source TEE for ARM TrustZone
- Trusty TEE: Android secure services and keystore
- Intel SGX SDK: Hardware-based memory enclaves
- AMD SEV: Encrypted VM memory
- Samsung TrustZone Research Toolkit: Ghidra loader + Unicorn emulator for Kinibi TA exploitation

### Root of Trust / TPM
- TPM 2.0 Reference Implementation, IBM Software TPM, tpm2-tss, Keylime (remote attestation)
- tpm2-algtest: Tests real TPM chips for RNG quality, key gen, algorithm support

### OTA Update Security
- SUIT (IETF working group), RAUC (A/B partitioning), Mender (atomic updates), SWUpdate

### IoT Protocol Security
- TLS for MQTT, wolfMQTT, CoAP with DTLS, libcoap, KillerBee (802.15.4/ZigBee)
- Cotopaxi: Multi-protocol IoT security testing (MQTT, CoAP, AMQP, DTLS, KNX, QUIC, RTSP, SSDP, HTTP/2, gRPC)

### Bluetooth/BLE Security
- nRF Sniffer, GATTacker (BLE MITM), BtleJuice (BLE proxy), Bettercap BLE
- InternalBlue: Broadcom/Cypress firmware patching via LMP injection
- BrakTooth: Bluetooth Classic LMP layer exploits (1,400+ affected products)
- SweynTooth: 18 BLE link-layer exploits across 6 SDK vendors
- WHAD Framework: Hardware-agnostic multi-protocol wireless (BLE, Zigbee, ESB, ANT)

### Zigbee/Z-Wave Security
- Z-Fuzzer: Coverage-guided Zigbee fuzzer (6 CVEs in TI Z-Stack)
- VFuzz: Dedicated Z-Wave fuzzer

### Baseband Security
- FirmWire: Full-system Samsung/MediaTek baseband emulation with AFL++ fuzzing (7 pre-auth memory corruptions, NDSS 2022)

### Hardware Tools
- **Logic Analyzers**: Saleae (commercial), Sigrok (open-source)
- **Side-Channel**: ChipWhisperer, SCALE (educational), lascar (Ledger, fast Python), scared (eShard, industrial-grade)
- **Fault Injection**: PicoGlitcher, PicoEMP, EM-Fault-It-Yourself
- **RF Tools**: Flipper Zero, Yard Stick One, Proxmark3, ChameleonUltra
- **SDR**: HackRF One, PlutoSDR, RTL-SDR
- **WiFi**: Pwnagotchi, ESP32Marauder

---

## 4. CloudGoat Scenarios (cloudgoat-readme.md)

CloudGoat is Rhino Security Labs' "Vulnerable by Design" AWS/Azure deployment tool. Each scenario is a standalone CTF-style learning environment.

### EASY Scenarios

| Scenario | Starting Point | Attack Path | Goal |
|----------|---------------|-------------|------|
| **iam_enum_basics** | Low-level IAM user "Bob" access keys | IAM enumeration: managed policies, inline policies, group memberships, assumable roles | Find 5 distinct flags |
| **data_secrets** | IAM user with limited permissions | Misconfigured EC2 User Data leaks creds -> SSH access -> IMDS role theft -> Lambda env vars -> Secrets Manager secret | Retrieve secret from Secrets Manager |
| **beanstalk_secrets** | Low-privileged AWS credentials with Elastic Beanstalk access | Enumerate EB environment -> misconfigured env vars containing secondary creds -> IAM enumeration -> create admin access key | Retrieve flag from Secrets Manager |
| **sns_secrets** | Basic AWS account access | Enumerate privileges -> discover subscribable SNS topic -> leaked API key -> API Gateway access | Final flag via API Gateway |
| **iam_privesc_by_key_rotation** | Role that manages other users' credentials | Insecure IAM permissions on key rotation -> access admin role | Flag from Secrets Manager |
| **iam_privesc_by_rollback** | Highly-limited IAM user | Review previous IAM policy versions -> restore version with full admin privileges | Privilege escalation to admin |
| **lambda_privesc** | IAM user "Chris" | Assume role with full Lambda access + pass role -> privilege escalation via Lambda | Full admin privileges |
| **sqs_flag_shop** | SHOP web page | Source code exposure -> analyze code for vulnerabilities -> exploit to purchase FLAG | Purchase FLAG |

### MEDIUM Scenarios

| Scenario | Starting Point | Attack Path | Goal |
|----------|---------------|-------------|------|
| **static** | External attacker visiting corporate portal | Public S3 bucket hosting JS libraries -> overwrite library (supply chain attack) -> admin bot logs in | Capture bot credentials, exfiltrate to bucket |
| **vulnerable_cognito** | Signup/login page with AWS Cognito | Bypass restrictions, exploit Cognito misconfigurations | Elevated privileges, Cognito Identity Pool credentials |
| **vulnerable_lambda** | IAM user "bilbo" | Assume higher-privilege role -> discover Lambda that applies policies -> exploit Lambda to escalate bilbo | Search for secrets |
| **cloud_breach_s3** | Anonymous outsider, no access | Misconfigured reverse-proxy -> query EC2 metadata service -> instance profile keys -> S3 bucket access and exfiltration | Exfiltrate sensitive S3 data |
| **iam_privesc_by_attachment** | Very limited permissions | Leverage instance-profile-attachment -> create EC2 with greater privileges -> full admin | Delete cg-super-critical-security-server |
| **ec2_ssrf** | IAM user "Solus" | ReadOnly Lambda permissions -> hardcoded secrets -> EC2 with SSRF-vulnerable web app -> metadata service keys -> private S3 bucket -> invoke Lambda | Complete scenario |
| **ecs_takeover** | External website access | RCE vulnerability -> container access -> ECS misconfigurations -> force ECS reschedule to compromised instance | IAM permission escalation |
| **rds_snapshot** | User "David" | Leverage privileges to steal credentials -> RDS vulnerability -> DB access | Retrieve flags from DB |
| **glue_privesc** | Web page uploads CSV, data visualization via Glue | SQL injection to steal web credentials -> upload reverse shell -> create Glue Job | Obtain secret string |
| **agentcore_identity_confusion** | AWS credentials managing Bedrock agentcore code interpreters | Leverage code interpreter access -> gain access to other agentcore runtime agents' data | Flag from Bedrock knowledgebase |
| **bedrock_agent_hijacking** | AWS credentials to invoke Bedrock Agent and update Lambda functions | Analyze agent -> understand real-time info access -> intercept flow | Extract flag from S3 |

### HARD Scenarios

| Scenario | Starting Point | Attack Path | Goal |
|----------|---------------|-------------|------|
| **rce_web_app** | IAM user "Lara" (OR user "McDuck") | Path A: Load Balancer + S3 clues -> RCE on vulnerable web app -> RDS database; Path B: S3 enumeration -> SSH keys -> EC2 -> database | Access highly-secured RDS database |
| **codebuild_secrets** | IAM user "Solo" | Enumerate CodeBuild projects -> find unsecured IAM keys for "Calrissian" -> RDS database -> RDS snapshot functionality (Alternative: SSM parameters -> SSH keys -> EC2 -> metadata service -> database) | Extract pair of secret strings from RDS |
| **detection_evasion** | Explicitly outlined goals | Read two secrets from Secrets Manager without triggering CloudTrail/GuardDuty alarms. Requires multiple playthroughs. | Read both secrets (cg-secret-XXXXXX-XXXXXX) without detection |
| **ecs_efs_attack** | Access to "ruse" EC2 | Instance profile abuse -> backdoor ECS container -> container metadata API credentials -> session on tagged EC2 -> tag manipulation on Admin EC2 -> port scan for EFS -> mount EFS | Flag from Elastic File System |
| **ecs_privesc_evade_protection** | Web service to EC2 container | Exploit web service vulnerability -> metadata API credentials -> initiate new container with specific role -> privilege escalation | Read FLAG from S3 |
| **secrets_in_the_cloud** | IAM user with limited privileges | Examine AWS resources for clues/hidden info -> acquire role with access | Retrieve final secret from Secrets Manager |

### Key CloudGoat Attack Patterns
1. **IMDSv1 exploitation**: SSRF to query 169.254.169.254 for instance profile credentials
2. **IAM privilege escalation**: PassRole, CreateAccessKey, UpdateAssumeRolePolicy, AttachUserPolicy, instance profile attachment
3. **S3 misconfigurations**: Public buckets, overly permissive bucket policies, static website hosting
4. **Lambda exploitation**: Hardcoded secrets in environment variables, vulnerable function code, Lambda layer manipulation
5. **Credential leakage**: EC2 User Data, environment variables, SSM parameters, CodeBuild buildspec
6. **Cross-service pivoting**: Lambda -> EC2 -> RDS -> S3 chains
7. **Elastic Beanstalk**: Environment variable secrets, misconfigured S3 buckets for source bundles
8. **Container escapes**: ECS task definition manipulation, container instance backdooring

---

## 5. UEFI Security (awesome-uefi-security.md)

### UEFI Architecture & Phases
| Phase | Description |
|-------|-------------|
| **SEC (Security)** | First code executed, initializes cache-as-RAM, verifies PEI |
| **PEI (Pre-EFI Initialization)** | Minimal initialization, memory discovery, loads DXE |
| **DXE (Driver Execution Environment)** | Main UEFI phase, loads drivers, produces boot services |
| **BDS (Boot Device Selection)** | UEFI boot manager, selects boot device |
| **TSL (Transient System Load)** | OS boot loader runs, ExitBootServices() called |
| **RT (Runtime)** | UEFI Runtime Services active alongside OS |

### Key UEFI Attack Vectors
| Attack Vector | Description |
|---------------|-------------|
| **SMM Exploitation** | System Management Mode is ring -2, invisible to OS; vulnerabilities in SMI handlers allow full compromise |
| **UEFI Bootkit** | Malware in DXE/PEI phase, persists across OS reinstall |
| **Secure Boot Bypass** | Exploiting signed-but-vulnerable bootloaders, leaked keys, NVRAM variable manipulation |
| **LogoFAIL** | Image parsing vulnerabilities during boot logo display (Black Hat EU 2023) |
| **PixieFail** | 9 vulnerabilities in Tianocore EDK II IPv6 network stack |
| **DMA Attacks** | Thunderbolt/PCIe DMA to read/write system memory, bypass OS protections |
| **SPI Flash Manipulation** | Directly modifying firmware in SPI flash chip if write-protection can be bypassed |
| **NVRAM Attacks** | Setting UEFI variables to disable Secure Boot, enable test signing (CVE-2022-3430 series) |
| **Option ROM Exploitation** | Malicious PCIe device firmware executing during boot |
| **S3 Boot Script** | Sleep/wake transitions execute boot script table, vulnerable to modification |
| **Pre-EFI (Boot Guard Bypass)** | Leaked Intel Boot Guard keys allow custom firmware flashing |
| **Sinkclose (AMD)** | Ring -2 privilege escalation via AMD System Management Mode (DEF CON 32) |
| **TPM Genie** | Hardware attack on TPM communication bus for <$50 |

### Notable UEFI Bootkits / Rootkits
| Bootkit | Year | Description |
|---------|------|-------------|
| **Bootkitty** | 2024 | First UEFI bootkit targeting Linux |
| **BlackLotus** | 2022 | UEFI bootkit bypassing Secure Boot on Windows 11 |
| **CosmicStrand** | 2022 | UEFI firmware rootkit persisting in DXE driver |
| **MoonBounce** | 2022 | Hidden in SPI flash, no changes on filesystem |
| **ESPecter** | 2021 | Bootkit on EFI System Partition |
| **FinSpy** | 2021 | Commercial UEFI bootkit in surveillance software |
| **TrickBoot** | 2020 | Trickbot firmware-level persistence module |
| **MosaicRegressor** | 2020 | Multi-component framework including UEFI implant |
| **LoJax** | 2018 | First UEFI rootkit found in wild (Sednit/APT28) |

### UEFI Security Tools
| Tool | Function |
|------|----------|
| **efiXplorer** | IDA Pro plugin, best UEFI binary analysis |
| **UEFITool** | Parse and extract UEFI firmware images (GUI + CLI) |
| **brick** | IDA Pro static vulnerability scanner for UEFI |
| **fwhunt-scan / FwHunt** | Firmware threat detection at scale (Binarly) |
| **Qiling EFI mode** | Partially emulate UEFI binaries |
| **efiSeek** | Ghidra plugin for UEFI analysis |
| **efi_fuzz** | Coverage-guided NVRAM fuzzer for UEFI (Qiling-based) |
| **CHIPSEC** | Intel platform security assessment, firmware extraction, vulnerability exploitation |
| **Chipsec** | The most commonly used tool for UEFI security testing |
| **tsffs** | Intel's snapshotting coverage-guided fuzzer for UEFI/BIOS on SIMICS |
| **efi-inspector** | Binary Ninja UEFI plugin |
| **efi-resolver** | Official Binary Ninja UEFI plugin with type propagation & PEI support |
| **PciLeech** | DMA attacks against UEFI, can hook Runtime Services |
| **bob_efi_fuzzer** | UEFI fuzzer |
| **uefi-rs** | Rust wrapper for UEFI app/PoC development |
| **EfiGuard** | Disable PatchGuard and DSE at boot |
| **DVUEFI** | Damn Vulnerable UEFI - exploitation learning platform |

### Key UEFI Research Groups
- **Binarly**: Leading UEFI firmware security research (efiXplorer, FwHunt, massive vulnerability disclosures)
- **ESET Research**: LoJax, BlackLotus, ESPecter discovery, NVRAM vulnerabilities
- **Cr4sh**: Exploiting AMI Aptio firmware, SMM backdoors, Lenovo firmware exploitation
- **Eclypsium**: Bootloader vulnerabilities, firmware attack timelines, iLOBleed implant
- **Sentinel Labs**: SMM bug hunting, HP firmware vulnerabilities, UEFI fuzzing pipeline
- **SYNACKTIV**: SMM vulnerability research, Lenovo UEFI password reversing
- **NCCGroup**: Insyde SMM stepping, Intel SMM race conditions, BIOS HID driver bugs
- **Quarkslab**: PixieFail (EDK II IPv6), Samsung TrustZone, UEFI exploitation

### UEFI Security Papers (Key)
| Year | Venue | Paper |
|------|-------|-------|
| 2025 | NDSS | FUZZUER: Enabling Fuzzing of UEFI Interfaces on EDK-2 |
| 2024 | ASE | STASE: Static Analysis Guided Symbolic Execution for UEFI |
| 2023 | S&P | RSFUZZER: Discovering Deep SMI Handler Vulnerabilities with Hybrid Fuzzing |
| 2022 | S&P | Finding SMM Privilege-Escalation Vulnerabilities with Protocol-Centric Static Analysis |
| 2020 | DAC | UEFI Firmware Fuzzing with Simics Virtual Platform |
| 2015 | WOOT | Symbolic Execution for BIOS Security |

### UEFI CTF Challenges
- UIUCTF 2022: SMM Cow Say 1/2/3
- D^3CTF 2022: d3guard
- corCTF 2023: smm-diary
- Dubhe CTF 2024: ToySMM
- DVUEFI: Damn Vulnerable UEFI exploitation platform

---

## 6. IoT Hardware Hacking (awesome-iot-hardware-v2.md)

### Hardware Debug Interfaces
| Interface | Purpose | Tools |
|-----------|---------|-------|
| **UART** | Serial console, bootloader access, debug output | Bus Pirate, Tigard, FTDI adapters |
| **JTAG** | On-chip debugging, flash programming, boundary scan | J-Link, JTAGulator, OpenOCD |
| **SWD** | ARM serial wire debug (2-pin alternative to JTAG) | Black Magic Probe, pyOCD, probe-rs |
| **SPI** | Flash memory access, peripheral communication | Bus Pirate, Tigard, logic analyzers |
| **I2C** | Sensor/EEPROM communication | Bus Pirate, logic analyzers |

### Logic Analyzers & Oscilloscopes
- **Saleae**: Commercial, effortless protocol decode (SPI, I2C, Serial, etc.)
- **PicoScope**: PC oscilloscopes

### SDR Tools
- HackRF One (1 MHz - 6 GHz, TX/RX, half-duplex)
- RTL-SDR (~$30, 500 kHz - 1.75 GHz, RX only)
- BladeRF 2.0 (47 MHz - 6 GHz, full-duplex)
- USRP B Series (70 MHz - 6 GHz, full-duplex)
- LimeSDR (100 kHz - 3.8 GHz, full-duplex)
- GNURadio: Signal processing development toolkit

### RFID/NFC Tools
- Proxmark3 RDV4: LF + HF RFID swiss-army tool
- ChameleonUltra: LF/HF emulation and manipulation
- HydraNFC: 13.56MHz NFC shield for sniff/read/write/emulate

### Bluetooth/BLE Tools
- Ubertooth One: 2.4 GHz Bluetooth experimentation
- nRF51 DK / nRF52840 Dongle: BLE development and sniffing
- Sniffle: Bluetooth 5 and 4.x LE sniffer (TI CC1352/CC26x2)
- ESP32: WiFi+BLE MCU for development/attacks

### Zigbee Tools
- RaspBee: Raspberry Pi Zigbee gateway
- nRF52840 Dongle: Supports Thread, Zigbee, 802.15.4
- ZigDiggity: ZigBee hacking toolkit
- KillerBee: Framework for sniffing/injecting/auditing Zigbee

### MQTT Tools
- Eclipse Mosquitto: Open-source MQTT broker
- MQTT-PWN: IoT broker penetration testing framework
- Nmap MQTT Library

### Firmware Tools
- EMBA: Central firmware analysis (extraction, static, dynamic via emulation, reporting)
- Firmware Mod Kit: Deconstruction/reconstruction of router firmware (TRX/uImage, SquashFS/CramFS)
- FirmAE: Scalable firmware emulation (79% success rate)
- FIRMADYNE: Automated Linux-based firmware emulation
- FACT: Web UI firmware analysis (Router, IoT, UEFI, Webcams, Drones)
- HAL: Netlist reverse engineering for hardware

### Key Pentest Case Studies
- Philips Hue Bridge root (Colin O'Flynn)
- Hardware crypto wallet $2M recovery (Joe Grand)
- Apple AirTag hacking (Thomas Roth)
- SpaceX Starlink user terminal glitching (Lennert Wouters)
- ESP32-C3/C6 fault injection + flash encryption bypass (Kevin Courdesses)
- SECGlitcher: STM32 voltage glitching (SEC Consult)

### IoT Security Standards & Regulations
- ETSI EN 303 645: Consumer IoT baseline requirements
- EU Cyber Resilience Act
- UK Product Security regime (effective April 2024)
- USA IoT Cybersecurity Improvement Act 2020
- NISTIR 8259: IoT device manufacturer recommendations
- ARM PSA Certified: IoT security framework and certification
- Common Criteria, SESIP methodology
- Cybersecurity Labelling Scheme (Singapore)

---

## 7. Firmware Security (awesome-firmware-security.md)

### Platform Firmware Technologies
| Technology | Description |
|------------|-------------|
| **BIOS** | Legacy 8086 Real Mode, being phased out (Intel EOL by 2020) |
| **UEFI** | Modern replacement for BIOS, supports Secure Boot, 64-bit |
| **coreboot** | Open-source firmware, loads payloads (SeaBIOS, UEFI, LinuxBoot) |
| **LinuxBoot** | Replaces UEFI DXE phase with Linux kernel |
| **Heads** | Minimal Linux as coreboot/LinuxBoot payload for secure boot |
| **U-Boot** | Embedded bootloader, supports verified boot (FIT signatures) |

### Platform Security Technologies
| Technology | Function |
|------------|----------|
| **Intel Boot Guard** | Hardware-enforced boot integrity before UEFI (cannot be disabled once enabled) |
| **Intel ME** | Management & security processor, runs MINIX, fTPM, AMT |
| **AMD PSP** | Platform Security Processor, fTPM, secure boot |
| **SMM** | System Management Mode (ring -2), invisible to OS, full system control |
| **Intel TXT** | Trusted Execution Technology for measured launch |
| **TPM** | Hardware root-of-trust for measured boot and attestation |
| **Secure Boot** | UEFI feature that only allows signed bootloaders/OS |
| **Measured Boot** | Records boot chain measurements in TPM PCRs |
| **Verified Boot** | Google's technology for ChromeOS/Android, checks hash chain |
| **UEFI DBX** | Secure Boot blacklist/revocation database |

### Management Systems (Out-of-Band)
| System | Description |
|--------|-------------|
| **Intel AMT** | Remote KVM, power control, OS restore via ME |
| **BMC (Baseboard Management Controller)** | Server remote management, OpenBMC is main open source implementation |
| **IPMI** | Legacy server management, being replaced by Redfish |
| **Redfish** | DMTF standard, RESTful replacement for IPMI |
| **iLOBleed** | Rootkit targeting HP iLO (Lights Out Management) |

### Key Firmware Threats
- **BadBIOS**: Alleged firmware malware
- **Evil Maid**: Physical access while unattended, install firmware malware
- **Hacking Team UEFI Malware**: Commercial UEFI attack tool
- **ThinkPwn**: UEFI malware PoC targeting ThinkPads
- **Thunderbolt DMA**: Rogue PCIe hardware via Thunderbolt
- **Rowhammer**: Memory bit-flip attacks (defense: ECC memory)
- **USB Rubber Ducky**: Rogue USB HID injection

### Platform Security Tools
| Tool | Purpose |
|------|---------|
| CHIPSEC | Platform security assessment, firmware extraction, vulnerability checking |
| FlashROM | Read/write/erase flash chips (SPI programming) |
| UEFITool | Parse and extract UEFI firmware images |
| Intel LUV (Linux UEFI Validation) | Live-boot distro bundling CHIPSEC, FWTS |
| FWTS (Firmware Test Suite) | Ubuntu's firmware testing, recommended by UEFI Forum |
| GRUB/Shim/Linux Stub | UEFI boot loaders |
| EFIgy | Check Apple Mac EFI firmware currency |
| DarwinDumper | OS X system and firmware information gathering |
| BIOS BITS | Intel BIOS Implementation Test Suite |
| Sandsifter | x86 instruction fuzzer |
| TXT Suite | Intel TXT validation, TPM boot chain verification |
| LVFS/fwupd | Linux Vendor Firmware Service, standardized firmware updates |
| Pawn | Google tool to dump platform firmware image |

### IBVs (Independent BIOS/Firmware Vendors)
- AMI (American Megatrends), Insyde, Phoenix

---

## 8. Pacu - AWS Exploitation Framework (pacu-readme.md)

Pacu is Rhino Security Labs' open-source AWS exploitation framework for offensive cloud security testing.

### Architecture
- Modular plugin system for enumeration, privilege escalation, data exfiltration, service exploitation, log manipulation
- Local SQLite database stores enumerated data, minimizing API calls and associated CloudTrail logs
- Session-based: each session holds AWS key pairs and data from modules
- Command logging and exporting for reporting and audit trail

### Module Categories
- **Enumeration**: Discover AWS resources (IAM, EC2, S3, Lambda, RDS, etc.)
- **Privilege Escalation**: Exploit IAM misconfigurations for higher access
- **Data Exfiltration**: Extract data from discovered resources
- **Service Exploitation**: Attack vulnerable AWS services
- **Log Manipulation**: Cover tracks by modifying CloudTrail or other logs
- **Persistence**: Backdoor IAM users/roles for sustained access

### Key Commands
- `set_keys`: Configure AWS access key, secret key, session token
- `list`: List available modules for current session regions
- `run <module>`: Execute module with default parameters
- `help <module>`: Module-specific help
- Session management: Start, resume, switch between sessions

### CLI Usage
- `pacu --session <name> --exec --module-name <module>`: Run module non-interactively
- `pacu --set-regions <regions>`: Configure target regions
- `pacu --data <service>`: Query local database for enumerated info
- `pacu --whoami`: Current IAM user/role information

---

## 9. AI Red Teaming (awesome-ai-red-teaming-readme.md)

### Prompt Engineering
- Learning Prompting (learnprompting.org)
- DeepLearning.AI - ChatGPT Prompt Engineering for Developers

### Attacks
- **Indirect Prompt Injection**: Attacker-controlled text in documents/web pages that LLMs process

### Red Teaming Approaches
- **Anthropic**: Red teaming language models to reduce harms - methods, scaling behaviors, lessons learned
- **DeepMind**: Red teaming language models with language models (automated red teaming)

### Events
- HackAPrompt: Prompt hacking competition
- AI Village at DEFCON: Generative AI Red Team
- Twitter Algorithmic Bias Bounty Challenge
- PromptTrace: Free prompt injection labs with real LLMs, 10 labs + 15-level CTF

---

## 10. HackerOne Writeup Patterns Analysis

### Top 100 Overall Patterns
The most upvoted H1 reports cluster around these vulnerability categories:

| Pattern | Prevalence | Top Examples |
|---------|------------|--------------|
| **Account Takeover** | Very High | Shopify SSO bypass, leaked session cookie, password reset flaws |
| **Stored XSS** | High | PayPal signin cache poisoning, GitLab Wiki, Imgur profile |
| **RCE** | High | Steam buffer overflow, npm misconfig (PayPal), ExifTool metadata (GitLab) |
| **SQLi** | High | Starbucks enterprise DB, Razer, Mail.ru |
| **SSRF** | High | Shopify Exchange ROOT access, Lyft expense report, Snapchat metadata |
| **Token/Key Leaks** | High | GitHub access token (Shopify, $50K), Snapchat Kubernetes API |
| **Request Smuggling** | High | Slack mass account takeover (864 upvotes) |
| **OAuth Misconfig** | Medium | Shopify Stocky App, GitLab email bypass, IDN homograph |
| **IDOR** | Medium | PayPal business manage users |
| **Privilege Escalation** | Medium | Ubiquiti user-to-SYSTEM via unauthenticated command exec |

### Race Condition Patterns (TOPRACECONDITION.md)
| Pattern | Examples |
|---------|----------|
| **Gift card / coupon multi-redeem** | Most common: race multiple redemptions for free money/credits |
| **Invite limit bypass** | Register multiple users from one invite, exceed team member limits |
| **Email verification bypass** | Activate account without verifying email |
| **Duplicate payment/payout** | Get paid multiple times for same action |
| **2FA bypass** | Race condition in 2FA validation flow |
| **Count/limit bypass** | Exceed workspace/folder/domain/subscriber limits |
| **Voting/likes manipulation** | Multiple votes or likes from single user |
| **OAuth race conditions** | Create multiple valid sessions from single authorization |
| **Timeout-based** | CURL connection reuse, TOCTOU in file operations |

### OAuth Patterns (TOPOAUTH.md)
| Pattern | Examples |
|---------|----------|
| **redirect_uri manipulation** | IDN homograph attacks, open redirect in OAuth flow, incomplete validation |
| **OAuth token theft** | Referer leakage, image injection, clickjacking authorization page |
| **CSRF on OAuth endpoint** | Missing state parameter, Cross-Site Flashing |
| **Account takeover via OAuth** | Bypass email verification, misconfigured OAuth provider trust |
| **OAuth + XSS chaining** | Stored XSS in redirect URI, XSS on authorize endpoint |
| **OAuth app permission abuse** | Overly broad scopes, token impersonation |
| **Race condition in OAuth** | Multiple valid sessions from single authorization code |
| **Code leakage** | Authorization code exposed via screenshot viewer, referer header |

### Request Smuggling Patterns (TOPREQUESTSMUGGLING.md)
| Pattern | Examples |
|---------|----------|
| **CL.TE / TE.CL smuggling** | Most common: front-end uses Content-Length, back-end uses Transfer-Encoding |
| **HTTP/2 downgrade smuggling** | HTTP/2 -> HTTP/1.1 conversion flaws (Basecamp, $7500) |
| **Malformed Transfer-Encoding** | CR-to-Hyphen conversion, ignoring chunk extensions |
| **Header field parsing** | Improper delimiter handling, space before colon |
| **Transform rule smuggling** | Hex escapes in concat(), newlines in host_header (Cloudflare) |
| **Tomcat CVE-2023-45648 / CVE-2024-21733** | Client-side desync in Apache Tomcat |
| **Node.js smuggling** | Multiple CVEs: CVE-2022-32213/32214/32215 series |
| **curl smuggling/SSRF** | CRLF injection in custom headers |

### XXE Patterns (TOPXXE.md)
| Pattern | Examples |
|---------|----------|
| **Out-of-band (OOB) XXE** | Most common approach: exfiltrate data via external DTD/entity |
| **XXE via file upload** | SVG image upload, XMP metadata in JPEG, PowerPoint files |
| **SOAP endpoint XXE** | SOAP web services with XML parsing, WAF bypass |
| **Blind XXE** | No direct output, use SSRF/error-based or out-of-band channels |
| **Office document XXE** | XXE in PowerPoint, XLSX parsing (Open-Xchange, $2000) |
| **SAML XXE** | XXE in SAML authentication response processing |
| **XXE to SSRF/RCE** | Chaining XXE with SSRF, file read, deserialization |
| **Spellcheck endpoint XXE** | Spellcheck service parsing XML without validation |

---

## 11. AI Red Teaming Summary (awesome-ai-red-teaming-readme.md)

### Attack Surface
- **Prompt Injection**: Manipulating LLM behavior through crafted input
- **Indirect Prompt Injection**: Embedding instructions in data the LLM processes (web pages, documents, emails)
- **Jailbreaking**: Bypassing safety/alignment guardrails

### Red Teaming Methods
- Manual adversarial probing by domain experts
- Automated red teaming using LLMs to generate attacks (DeepMind approach)
- Crowd-sourced red teaming events (DEFCON AI Village, HackAPrompt)
- Scale-dependent harm discovery (Anthropic scaling studies)

### Key Resources
- learnprompting.org: Prompt engineering and injection techniques
- PromptTrace: Hands-on labs with real LLMs, prompt stack visibility

---

## Overall Key Attack Patterns Cross-Reference

| Attack Type | Embedded/IoT | ICS/SCADA | Cloud (AWS) | UEFI |
|-------------|-------------|-----------|-------------|------|
| **Firmware extraction** | SPI dump, eMMC, UART | JTAG, firmware update intercept | N/A | SPI dump, CHIPSEC |
| **Debug interface** | UART, JTAG, SWD | JTAG, serial | N/A | DCI (USB debug) |
| **Side-channel** | Power analysis, EM glitch | Timing attacks on crypto | N/A | Boot Guard key extraction |
| **Privilege escalation** | ROP on ARM/MIPS, shell escape | PLC logic manipulation | IAM role chaining, PassRole | SMM ring -2 exploitation |
| **Network attacks** | MQTT/CoAP/Zigbee MITM | Modbus/DNP3/S7 MITM | SSRF, IMDS exploitation | PXE boot attacks |
| **Supply chain** | Firmware modification | ICS vendor compromise | S3 bucket hijacking | Leaked Boot Guard keys |
| **Persistence** | Bootloader backdoor | PLC firmware implant | IAM backdoor users | UEFI bootkit |
