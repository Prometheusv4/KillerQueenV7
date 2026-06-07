# Embedded, IoT, ICS, UEFI, and Firmware Security — Tools & Techniques

> **Generated:** 2026-06-06
> **Sources:** 8 cloned repos + 2 web-extracted articles
> **Note:** infosecinstitute.com blocked by Cloudflare; those URLs excluded.

---

## TABLE OF CONTENTS

1. [Embedded & IoT Security — Tools](#1-embedded--iot-security--tools)
2. [Embedded & IoT Security — Techniques & Resources](#2-embedded--iot-security--techniques--resources)
3. [ICS/SCADA Security — Tools](#3-icsscada-security--tools)
4. [ICS/SCADA Security — Resources & Literature](#4-icsscada-security--resources--literature)
5. [Firmware Security (Platform/UEFI) — Tools](#5-firmware-security-platformuefi--tools)
6. [Firmware Security — Techniques & Threats](#6-firmware-security--techniques--threats)
7. [UEFI Security — Tools](#7-uefi-security--tools)
8. [UEFI Security — Bootkits & Exploits](#8-uefi-security--bootkits--exploits)
9. [Red Teaming — Embedded/Peripheral Device Hacking](#9-red-teaming--embeddedperipheral-device-hacking)
10. [Articles & Blog Extracts](#10-articles--blog-extracts)

---

## 1. Embedded & IoT Security — Tools

### Analysis Frameworks
- **EXPLIoT** — Pentest framework like Metasploit specialized for IoT. https://gitlab.com/expliot_framework/expliot
- **FACT (Firmware Analysis and Comparison Tool)** — Full-featured static analysis framework. https://fkie-cad.github.io/FACT_core/
- **FwAnalyzer** — Analyze firmware security based on customized rules. https://github.com/cruise-automation/fwanalyzer
- **HAL – The Hardware Analyzer** — Reverse engineering & manipulation of gate-level netlists. https://github.com/emsec/hal
- **HomePWN** — Swiss Army Knife for IoT pentesting. https://github.com/ElevenPaths/HomePWN
- **IoTSecFuzz** — IoT layers security analysis: hardware, software, communication. https://gitlab.com/invuls/iot-projects/iotsecfuzz
- **KillerBee** — ZigBee & IEEE 802.15.4 network testing/auditing framework. https://github.com/riverloopsec/killerbee
- **PRET** — Printer Exploitation Toolkit. https://github.com/RUB-NDS/PRET
- **Routersploit** — Exploitation framework for embedded devices. https://github.com/threat9/routersploit

### Binary/Firmware Analysis
- **Binwalk** — Analyze, reverse engineer, extract firmware images. https://github.com/ReFirmLabs/binwalk
- **unblob** — Fast/accurate firmware extraction (100+ formats). https://github.com/onekey-sec/unblob / https://unblob.org/
- **OFRAK** — Binary analysis + modification platform (unpack, analyze, modify, repack). https://github.com/redballoonsecurity/ofrak
- **LIEF** — Parse/modify/abstract ELF, PE, Mach-O, DEX, OAT. https://github.com/lief-project/LIEF
- **cwe_checker** — Finds vulnerable patterns in ELF binaries. https://github.com/fkie-cad/cwe_checker
- **firmwalker** — Searches extracted firmware for interesting files/creds. https://github.com/craigz28/firmwalker
- **SCOUT** — Deterministic firmware-to-exploit evidence engine (42-stage pipeline). https://github.com/R00T-Kim/SCOUT
- **FLARE-FLOSS** — Obfuscated string solver for binaries. https://github.com/mandiant/flare-floss
- **argXtract** — Static argument extraction from stripped ARM Cortex-M firmware. https://github.com/projectbtle/argXtract
- **checksec** — Check binary security hardening flags. https://github.com/slimm609/checksec.sh
- **cpu_rec** — Identify CPU architecture from binary blob. https://github.com/airbus-seclab/cpu_rec
- **binbloom** — Find loading address, endianness from raw firmware. https://github.com/quarkslab/binbloom
- **Kaitai Struct** — Declarative language for binary data structures. https://kaitai.io/

### Firmware Emulation
- **FirmAE** — Automated IoT firmware emulation (79% success rate). https://github.com/pr0v3rbs/FirmAE
- **Firmadyne** — Automated emulation & dynamic analysis of Linux-based firmware. https://github.com/firmadyne/firmadyne
- **QEMU** — Generic machine emulator/virtualizer. https://github.com/qemu/qemu / https://www.qemu.org/
- **Qiling** — Cross-platform binary emulation (Windows, Linux, Android, BSD, UEFI). https://github.com/qilingframework/qiling
- **Unicorn Engine** — Lightweight multi-architecture CPU emulator. https://github.com/unicorn-engine/unicorn
- **PANDA** — Platform for Architecture-Neutral Dynamic Analysis. https://github.com/panda-re/panda
- **Renode** — Open-source hardware simulation framework. https://renode.io/
- **Avatar2** — Dynamic analysis orchestration across emulators + real hardware. https://github.com/avatartwo/avatar2
- **HALucinator** — MCU firmware emulation via HAL function replacement. https://github.com/embedded-sec/halucinator
- **FirmSolo** — Load proprietary kernel modules for dynamic analysis. https://github.com/BUseclab/FirmSolo
- **EMUX** — Embedded device emulation framework. https://github.com/therealsaumil/emux

### Disassemblers / Decompilers
- **Ghidra** — NSA's SRE suite, free decompiler. https://github.com/NationalSecurityAgency/ghidra / https://ghidra-sre.org/
- **IDA Pro** — Commercial disassembler & decompiler. https://hex-rays.com/IDA-pro/
- **Binary Ninja** — Interactive disassembler/decompiler. https://binary.ninja/
- **Cutter** — Free RE platform (Rizin-based). https://cutter.re/
- **Rizin** — Free RE framework. https://rizin.re/
- **radare2** — Free/libre RE toolchain. https://github.com/radare/radare2 / https://www.radare.org/n/
- **Angr** — Platform-agnostic binary analysis framework. https://github.com/angr/angr
- **Angr Management** — GUI for Angr. https://github.com/angr/angr-management
- **Capstone** — Lightweight multi-arch disassembly framework. https://github.com/capstone-engine/capstone
- **Keystone** — Lightweight multi-arch assembler framework. https://github.com/keystone-engine/keystone
- **BARF** — Binary analysis & RE framework with ROP gadget search. https://github.com/programa-stic/barf-project
- **RetDec** — Retargetable decompiler (ARM, MIPS, x86). https://github.com/avast/retdec
- **Vivisect** — Combined disassembler/static analysis/symbolic execution/debugger. https://github.com/vivisect/vivisect

### Fuzzing Tools
- **AFL++** — Coverage-guided fuzzer with enhanced mutations. https://github.com/AFLplusplus/AFLplusplus
- **afl-unicorn** — AFL with Unicorn for binary fuzzing. https://github.com/Battelle/afl-unicorn
- **honggfuzz** — Feedback-driven fuzzer with HW coverage. https://github.com/google/honggfuzz
- **boofuzz** — Network protocol fuzzer (Sulley successor). https://github.com/jtpereyda/boofuzz
- **Fuzzowski** — Network protocol fuzzer (Sulley/BooFuzz based). https://github.com/nccgroup/fuzzowski
- **Peach** — Smart fuzzer (generation + mutation). https://gitlab.com/peachtech/peach-fuzzer-community
- **libFuzzer** — In-process coverage-guided fuzzing engine (LLVM). https://llvm.org/docs/LibFuzzer.html
- **GDBFuzz** — GDB hardware breakpoint coverage for uninstrumented targets. https://github.com/boschresearch/gdbfuzz
- **Fuzzware** — MMIO-aware MCU firmware fuzzer. https://github.com/fuzzware-fuzzer/fuzzware
- **μEmu** — Peripheral-aware MCU firmware fuzzing. https://github.com/MCUSec/uEmu
- **SAFIREFUZZ** — Dynamic binary rewriting for ARM Cortex-M fuzzing. https://github.com/pr0me/SAFIREFUZZ
- **Icicle** — Rust-based grey-box fuzzer (MSP430, RISC-V). https://github.com/icicle-emu/icicle-emu
- **μAFL** — Hardware-in-the-loop fuzzer using ARM ETM trace. https://github.com/MCUSec/microAFL
- **DICE** — DMA channel emulation for MCU fuzzing. https://github.com/RiS3-Lab/DICE-DMA-Emulation

### Taint Analysis Tools
- **KARONTE** — Multi-binary taint propagation for embedded firmware. https://github.com/ucsb-seclab/karonte
- **SaTC** — String-anchored taint analysis for web+backend binaries. https://github.com/NSSL-SJTU/SaTC
- **EmTaint** — Symbolic expression-based taint analysis. https://github.com/kuc001/EmTaint

### Firmware Malware / Security Analysis
- **EMBA** — Efficient malware analysis for embedded firmware. https://github.com/e-m-b-a/emba
- **EMBArk** — Enterprise web UI for EMBA. https://github.com/e-m-b-a/embark
- **Firmware Analysis Toolkit** — Automated firmware emulation & vuln discovery. https://github.com/attify/firmware-analysis-toolkit
- **Firmware Slap** — Concolic analysis & function clustering for firmware. https://github.com/ChrisTheCoolHut/Firmware_Slap
- **Trommel** — Searches firmware images for interesting content. https://github.com/CERTCC/trommel
- **Firmware.re** — Free firmware unpack/scan service. http://firmware.re/
- **bugprove** — Automatic firmware analysis platform. https://bugprove.com/

### Extraction & Support Tools
- **FACT Extractor** — Auto-detects container format & extracts. https://github.com/fkie-cad/fact_extractor
- **Firmware Mod Kit** — Deconstruct/reconstruct firmware images. https://github.com/rampageX/firmware-mod-kit/wiki
- **SRecord** — Manipulate EPROM/binary files. http://srecord.sourceforge.net/
- **dumpflash** — Low-level NAND Flash dump/parse. https://github.com/ohjeongwook/dumpflash
- **flashrom** — Identify/read/write/verify/erase flash chips. https://github.com/flashrom/flashrom / https://flashrom.org/
- **Samsung Firmware Magic** — Decrypt Samsung SSD firmware. https://github.com/chrivers/samsung-firmware-magic
- **TritonDSE** — Emulation & symbolic execution library. https://github.com/quarkslab/tritondse
- **SVD-Loader for Ghidra** — Load SVD files for peripheral awareness. https://github.com/leveldown-security/SVD-Loader-Ghidra
- **Buildroot** — Cross-compiler toolchain. https://buildroot.org/

### Secure Boot & Firmware Trust
- **MCUboot** — Secure bootloader for 32-bit MCUs. https://github.com/mcu-tools/mcuboot
- **AVB (Android Verified Boot)** — Chained trust for embedded Android. https://android.googlesource.com/platform/external/avb/+/master/README.md
- **U-Boot Verified Boot** — FIT-signature based verified boot. https://docs.u-boot.org/en/latest/usage/fit/verified-boot.html
- **wolfBoot** — Portable secure bootloader for 32-bit MCUs. https://github.com/wolfSSL/wolfBoot

### Supply Chain & SBOM
- **in-toto** — Framework for supply chain integrity. https://in-toto.io/
- **Sigstore Cosign** — Keyless signing/verification of artifacts. https://github.com/sigstore/cosign
- **Syft** — SBOM generator for filesystems/artifacts. https://github.com/anchore/syft
- **Grype** — Vulnerability scanner consuming SBOMs. https://github.com/anchore/grype

### RTOS Security
- **FreeRTOS Security** — MQTT/TLS, PKCS#11, PSA Certified. https://www.freertos.org/Security/01-Security-overview
- **Zephyr Project Security** — TF-M, verified boot, security testing. https://docs.zephyrproject.org/latest/security/index.html
- **RT-Thread Security** — IoT OS security. https://github.com/RT-Thread/rt-thread/security
- **seL4** — Formally verified microkernel. https://sel4.systems/
- **Tock OS** — Rust-based embedded OS with HW isolation. https://www.tockos.org/

### TEE / Trusted Execution Environments
- **OP-TEE** — Open-source TEE for ARM TrustZone. https://optee.readthedocs.io/
- **Trusty TEE** — Android TEE for secure services. https://source.android.com/docs/security/features/trusty
- **Intel SGX SDK** — SDK for Intel SGX enclaves. https://github.com/intel/linux-sgx
- **AMD SEV** — Secure Encrypted Virtualization. https://developer.amd.com/sev/
- **Samsung TrustZone Research Toolkit** — RE toolkit for Kinibi TrustZone. https://github.com/quarkslab/samsung-trustzone-research

### Root of Trust & TPM
- **TPM 2.0 Reference Implementation** — TCG specs & reference. https://trustedcomputinggroup.org/resource-library/
- **IBM Software TPM** — Software TPM 2.0 emulator. https://sourceforge.net/projects/ibmswtpm2/
- **tpm2-tss** — TCG Software Stack for TPM 2.0. https://github.com/tpm2-software/tpm2-tss
- **Keylime** — TPM-based remote attestation. https://keylime.dev/
- **tpm2-algtest** — TPM chip testing (RNG, timing, algorithms). https://github.com/crocs-muni/tpm2-algtest

### OTA Update Security
- **SUIT** — IETF manifest-based firmware update architecture. https://datatracker.ietf.org/wg/suit/about/
- **RAUC** — Safe firmware update framework with A/B partitioning. https://rauc.io/
- **Mender** — OTA software updater for Linux IoT. https://mender.io/
- **SWUpdate** — Linux firmware update agent. https://sbabic.github.io/swupdate/

### IoT Protocol Security
- **wolfMQTT** — MQTT client library with TLS. https://www.wolfssl.com/products/wolfmqtt/
- **libcoap** — CoAP with DTLS support. https://libcoap.net/
- **Cotopaxi** — Multi-protocol IoT security testing toolkit (14 protocols). https://github.com/Samsung/cotopaxi
- **MQTT-PWN** — IoT Broker penetration testing. https://mqtt-pwn.readthedocs.io/en/latest/
- **Eclipse Mosquitto** — Open source MQTT broker. https://mosquitto.org/

### Zigbee / Z-Wave Security
- **KillerBee** — IEEE 802.15.4/ZigBee security framework. https://github.com/riverloopsec/killerbee
- **ZigDiggity** — ZigBee Hacking Toolkit. https://github.com/BishopFox/zigdiggity
- **Z-Fuzzer** — Coverage-guided Zigbee protocol fuzzer. https://github.com/zigbeeprotocol/Z-Fuzzer
- **VFuzz** — Dedicated open-source Z-Wave security fuzzer. https://github.com/CNK2100/VFuzz-public

### Bluetooth / BLE Security
- **nRF Sniffer for Bluetooth LE** — BLE packet sniffer (Nordic). https://www.nordicsemi.com/Products/Development-tools/nRF-Sniffer-for-Bluetooth-LE
- **GATTacker** — BLE MITM tool. https://github.com/securing/gattacker
- **BtleJuice** — BLE MITM proxy framework. https://github.com/DigitalSecurity/btlejuice
- **Btlejack** — Sniff/jam/hijack BLE devices. https://github.com/virtualabs/btlejack
- **Bettercap BLE** — BLE scanning/enumeration module. https://www.bettercap.org/modules/ble/
- **InternalBlue** — Bluetooth firmware experimentation framework. https://github.com/seemoo-lab/internalblue
- **BrakTooth** — Exploit suite for BT Classic LMP vulnerabilities. https://github.com/Matheus-Garbelini/braktooth_esp32_bluetooth_classic_attacks
- **SweynTooth** — PoC exploits for 18 BLE link-layer vulnerabilities. https://github.com/Matheus-Garbelini/sweyntooth_bluetooth_low_energy_attacks
- **WHAD Framework** — Multi-protocol wireless security framework (BLE, Zigbee, ESB, ANT). https://github.com/whad-team/whad-client
- **Sniffle** — Bluetooth 5/4.x LE sniffer (TI CC1352/CC26x2). https://github.com/nccgroup/Sniffle

### Baseband Security
- **FirmWire** — Full-system baseband firmware emulation + fuzzing. https://github.com/FirmWire/FirmWire

### Language-Specific Decompilers
- **ILSpy** — .NET Decompiler. https://github.com/icsharpcode/ILSpy
- **dnSpy** — .NET debugger & assembly editor. https://github.com/dnSpyEx/dnSpy
- **de4dot** — .NET deobfuscator. https://github.com/de4dot/de4dot
- **JD-GUI** — Java decompiler. https://github.com/java-decompiler/jd-gui
- **JADX** — Dex to Java decompiler. https://github.com/skylot/jadx

### Debugging Tools
- **OpenOCD** — On-chip programming & debugging (JTAG). https://github.com/openocd-org/openocd/ / http://openocd.org/
- **GDB** — GNU Project debugger. https://www.sourceware.org/gdb/
- **GEF** — GDB Enhanced Features (ARM, MIPS, PPC, SPARC). https://hugsy.github.io/gef/
- **Black Magic Probe** — Open-source JTAG/SWD debugger. https://codeberg.org/blackmagic-debug/blackmagic
- **pyOCD** — Python library for Arm Cortex-M debugging. https://pyocd.io
- **probe-rs** — Rust-based embedded debug toolkit. https://probe.rs/
- **Frida** — Dynamic instrumentation toolkit. https://frida.re/

### Hardware Reverse Engineering / Multitools
- **Tigard** — FT2232H-based multi-protocol hardware tool. https://github.com/tigard-tools/tigard
- **Bus Pirate** — Open source hacker multi-tool. https://github.com/ElderlyPirate/Bus_Pirate
- **Glasgow Interface Explorer** — FPGA-based hardware debugging. https://glasgow-embedded.org/ / https://github.com/GlasgowEmbedded/Glasgow
- **GreatFET** — USB hardware security research platform. https://greatscottgadgets.com/greatfet/ / https://github.com/greatscottgadgets/greatfet
- **Hydrabus** — Multi-protocol hardware hacking tool. https://hydrabus.com/
- **FTDI FT2232H** — USB 2.0 Hi-Speed to UART/FIFO IC. https://www.ftdichip.com/old2020/Products/ICs/FT2232H.html

### Hardware Debug Interfaces
- **JTAGenum** — Enumerate JTAG pinouts via brute-force. https://github.com/cyphunk/JTAGenum
- **JTAGulator** — Auto-discover JTAG/SWD/UART debug interfaces. https://github.com/grandideastudio/jtagulator
- **UrJTAG** — Open-source JTAG toolkit. https://urjtag.sourceforge.io/
- **LUNA** — FPGA-based USB analysis platform. https://github.com/greatscottgadgets/luna
- **SEGGER J-Link** — USB powered JTAG debug probes. https://www.segger.com/products/debug-probes/j-link/

### Chip-Off / Memory Forensics
- **Flashrom** — Identify/read/write SPI flash chips. https://flashrom.org/ / https://github.com/flashrom/flashrom
- **CHIPSEC** — Platform security assessment framework. https://github.com/chipsec/chipsec
- **The Sleuth Kit** — File system forensic toolkit. https://www.sleuthkit.org/sleuthkit/
- **SNANDer** — CLI NAND flash programmer (CH341A). https://github.com/McMCCRU/SNANDer
- **NANDO** — Open hardware NAND flash programmer. https://github.com/bbogush/nand_programmer

### Side-Channel Analysis
- **ChipWhisperer** — Open-source SCA + fault injection toolchain. https://github.com/newaetech/chipwhisperer
- **SCALE** — Side-Channel Attack Lab Exercises. https://github.com/danpage/scale
- **lascar** — Fast Python SCA library (CPA, DPA, MIA, ML). https://github.com/Ledger-Donjon/lascar
- **scared** — Industrial-grade SCA framework. https://github.com/eshard/scared

### Fault Injection
- **PicoGlitcher** — RP2040/RP2350 voltage glitching (sub-10ns). https://github.com/MKesenheimer/fault-injection-library
- **PicoEMP** — Entry-level EMFI tool (Raspberry Pi Pico). https://github.com/newaetech/chipshouter-picoemp
- **EM-Fault-It-Yourself** — Motorized XYZ-stage EMFI platform. https://github.com/fgsect/EM-Fault-It-Yourself
- **ChipSHOUTER** — Full EMFI platform. https://rtfm.newae.com/ChipSHOUTER/ChipSHOUTER/
- **ICEStick ICE40 FPGA Glitcher** — Simple voltage glitcher. https://github.com/SySS-Research/icestick-glitcher
- **RP2040 Pico Glitcher** — Low-cost voltage glitcher. https://github.com/ZeusWPI/pico-glitcher

### Logic Analyzer
- **Saleae** — Commercial logic analyzer HW + SW. https://www.saleae.com/
- **Sigrok** — FLOSS signal analysis suite. https://sigrok.org/
- **Pico Oscilloscope** — PC oscilloscopes. https://www.picotech.com/products/oscilloscope

### RF / NFC / RFID Tools
- **Flipper Zero** — Portable multi-tool (RF, access control, HW). https://docs.flipper.net/
- **Awesome Flipper Zero** — Collection of Flipper resources. https://github.com/RogueMaster/awesome-flipperzero-withModules
- **Proxmark3** — RFID swiss army knife. https://github.com/RfidResearchGroup/proxmark3
- **ChameleonUltra** — Pocket LF/HF RFID emulator. https://github.com/RfidResearchGroup/ChameleonUltra
- **Bruce** — ESP32 firmware for offensive security. https://bruce.computer/
- **HydraNFC** — 13.56MHz NFC platform. https://hydrabus.com/hydranfc-1-0-specifications/

### SDR (Software Defined Radio)
- **HackRF One** — 1 MHz to 6 GHz SDR. https://greatscottgadgets.com/hackrf/
- **RTL-SDR** — ~$30 USB radio scanner. https://www.rtl-sdr.com/
- **ADALM-PLUTO (PlutoSDR)** — Analog Devices SDR. https://wiki.analog.com/university/tools/pluto
- **BladeRF 2.0** — 47 MHz to 6 GHz SDR (full-duplex). https://www.nuand.com/bladerf-2-0-micro/
- **LimeSDR** — 100 KHz to 3.8 GHz SDR (full-duplex). https://www.crowdsupply.com/lime-micro/limesdr
- **USRP B Series** — 70 MHz to 6 GHz SDR. https://www.ettus.com/product-categories/usrp-bus-series/
- **Yard Stick One** — Sub-1 GHz half-duplex transceiver. https://greatscottgadgets.com/yardstickone/
- **GNURadio** — Free SDR development toolkit. https://github.com/gnuradio/gnuradio
- **Future SDR** — Stream-based SDR. https://www.futuresdr.org/
- **Maia SDR** — FPGA-based SDR (ADALM Pluto). https://maia-sdr.org/

### WiFi Tools
- **Pwnagotchi** — A2C-based WiFi cracking AI. https://pwnagotchi.ai/
- **ESP32Maurauder** — WiFi/Bluetooth offensive tools for ESP32. https://github.com/justcallmekoko/ESP32Marauder

### ZigBee Hardware
- **ApiMote** — ZigBee security research hardware. http://apimote.com
- **RaspBee** — Raspberry Pi Zigbee gateway. https://phoscon.de/en/raspbee/
- **nRF52840 Dongle** — Bluetooth 5.4, Thread, Zigbee, 802.15.4. https://www.nordicsemi.com/Products/Development-hardware/nRF52840-Dongle

### Bluetooth Hardware
- **UberTooth One** — 2.4 GHz BT experimentation. https://greatscottgadgets.com/ubertoothone/
- **Bluefruit LE Sniffer** — Easy BLE sniffer. https://www.adafruit.com/product/2269
- **nRF51 DK** — BLE development kit. https://www.nordicsemi.com/Products/Development-hardware/nRF51-DK
- **ESP32** — Wi-Fi + Bluetooth MCU. https://www.espressif.com/en/products/socs/esp32

---

## 2. Embedded & IoT Security — Techniques & Resources

### Labs / CTF / Practice Targets
- **DVRF (Damn Vulnerable Router Firmware)** — MIPS/ARM binary exploitation challenges. https://github.com/praetorian-inc/DVRF
- **IoTGoat** — OWASP deliberately insecure OpenWrt firmware. https://github.com/OWASP/IoTGoat
- **DVAR (Damn Vulnerable ARM Router)** — Vulnhub ARM router. https://www.vulnhub.com/entry/damn-vulnerable-arm-router-dvar-tinysploitarm,224/
- **DVID (Damn Vulnerable IoT Device)** — ATmega328p board for UART/firmware/BLE practice. https://github.com/Vulcainreo/DVID
- **Microcorruption** — Browser-based MSP430 embedded CTF. https://microcorruption.com/
- **MITRE eCTF** — Annual "build-then-break" ARM MCU competition. https://ectf.mitre.org/
- **RHme-2015/2016/2017** — Riscure hardware CTF challenges. https://github.com/Riscure/RHme-2015 / https://github.com/Riscure/Rhme-2016 / https://github.com/Riscure/Rhme-2017
- **Exploit Security CTF** — IoT-focused challenges. https://exploitthis.ctfd.io/challenges
- **CSAW Embedded Security Challenge 2019** — https://github.com/TrustworthyComputing/csaw_esc_2019

### Books
- Practical IoT Hacking — https://nostarch.com/practical-iot-hacking
- The Hardware Hacking Handbook — https://nostarch.com/hardwarehacking
- Blue Fox: Arm Assembly Internals and Reverse Engineering — https://www.wiley.com/en-us/Blue+Fox%3A+Arm+Assembly+Internals+and+Reverse+Engineering-p-9781119745303
- Fuzzing Against the Machine — https://www.packtpub.com/product/fuzzing-against-the-machine/9781804614976
- Car Hacker's Handbook — https://nostarch.com/carhacking
- Microcontroller Exploits — https://nostarch.com/microcontroller-exploits
- Attacking and Securing U-Boot — https://www.amazon.com/Attacking-Securing-U-Boot-Gabriel-Gonzalez-ebook/dp/B0DHYTSWZC/
- Pentest Hardware — https://github.com/unprovable/PentestHardware
- The IoT Hacker's Handbook — https://www.apress.com/us/book/9781484242995
- IoT Penetration Testing Cookbook — https://www.packtpub.com/networking-and-servers/iot-penetration-testing-cookbook
- Practical Hardware Pentesting, 2nd Ed — https://www.packtpub.com/product/practical-hardware-pentesting-second-edition-second-edition/9781803249322
- Hardware Security: A Hands-on Learning Approach — https://www.elsevier.com/books/hardware-security/bhunia/978-0-12-812477-2
- The Hardware Hacker — https://nostarch.com/hardwarehackerpaperback
- The Art of PCB Reverse Engineering — https://visio-for-engineers.blogspot.com/p/order.html
- Hacking the Xbox — https://nostarch.com/xboxfree

### Standards & Regulations
- ETSI EN 303 645 (Consumer IoT Security) — https://www.etsi.org/deliver/etsi_en/303600_303699/303645/02.01.00_30/en_303645v020100v.pdf
- EU Cyber Resilience Act — https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act
- Radio Equipment Directive (RED) 2022/30/EU — https://eur-lex.europa.eu/eli/reg_del/2022/30/oj
- USA IoT Cybersecurity Improvement Act of 2020 — https://www.congress.gov/bill/116th-congress/house-bill/1668
- UK Product Security Regime — https://www.gov.uk/government/publications/the-uk-product-security-and-telecommunications-infrastructure-product-security-regime
- NISTIR 8259 (IoT Device Manufacturers) — https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program/nistir-8259-series
- ARM PSA Certified — https://www.psacertified.org/
- Common Criteria — https://www.commoncriteriaportal.org/index.cfm
- IASME IoT Cyber — https://iasme.co.uk/iasme-iot-cyber/
- GlobalPlatform SESIP — https://globalplatform.org/sesip/

### Key Research Papers (Embedded/IoT)
- SAFER: IoT Device Risk Assessment Framework — https://dl.acm.org/doi/abs/10.1145/3414173
- BenchIoT: Security Benchmark for IoT — https://nebelwelt.net/publications/files/19DSN.pdf
- SoK: Security Evaluation of Home-Based IoT Deployments — https://alrawi.github.io/static/papers/alrawi_sok_sp19.pdf
- Firmadyne: Automated Dynamic Analysis for Linux-based Embedded Firmware — https://www.dcddcc.com/docs/2016_paper_firmadyne.pdf
- Firmalice: Automatic Detection of Authentication Bypass in Binary Firmware — https://www.ndss-symposium.org/wp-content/uploads/2017/09/11_1_2.pdf
- Avatar: Dynamic Security Analysis of Embedded Firmwares — http://www.eurecom.fr/en/publication/4158/download/rs-publi-4158.pdf
- FIE on Firmware: Finding Vulns in Embedded Systems via Symbolic Execution — https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_davidson.pdf
- KARONTE (IEEE S&P 2020) — https://github.com/ucsb-seclab/karonte
- SaTC (USENIX Security 2021) — https://github.com/NSSL-SJTU/SaTC
- EmTaint (ISSTA 2023) — https://github.com/kuc001/EmTaint

### Blogs (Embedded/IoT)
- **/dev/ttyS0** — http://www.devttys0.com/blog/
- **wrong baud** — https://wrongbaud.github.io/
- **Quarkslab** — https://blog.quarkslab.com/
- **Payatu** — https://payatu.com/tag/iot/
- **Attify** — https://blog.attify.com/
- **STAR Labs** — https://starlabs.sg/blog/
- **PenTestPartners** — https://www.pentestpartners.com/internet-of-things/
- **jcjc-dev** — https://jcjc-dev.com/
- **Exploiteers** — https://www.exploitee.rs/
- **Firmware Security** — https://firmwaresecurity.com/
- **VoidStar Security** — https://voidstarsec.com/blog/
- **GracefulSecurity (Hardware tag)** — https://gracefulsecurity.com/category/hardware/
- **Black Hills (Hardware Hacking tag)** — https://www.blackhillsinfosec.com/tag/hardware-hacking/
- **0x434b** — https://0x434b.dev/
- **LimitedResults** — https://limitedresults.com/posts/
- **Synacktiv** — https://www.synacktiv.com/en/publications
- **eshard** — https://eshard.com/posts
- **claroty/Team82** — https://claroty.com/team82/research
- **NCC Group** — https://research.nccgroup.com/
- **Mandiant** — https://www.mandiant.com/resources/blog
- **IOActive** — https://labs.ioactive.com/
- **Riscure** — https://www.riscure.com/blog/
- **interruptlabs** — https://www.interruptlabs.co.uk/articles
- **hacefresko** — https://www.hacefresko.com/
- **debugmen** — https://debugmen.dev/
- **rossmarks** — https://rossmarks.uk/blog
- **blog.ret2.io** — https://blog.ret2.io/
- **VulnCheck** — https://vulncheck.com/blog
- **0xbigshaq** — https://0xbigshaq.github.io/
- **Coalfire** — https://www.coalfire.com/the-coalfire-blog

### YouTube Channels
- **stacksmashing** — https://www.youtube.com/@stacksmashing
- **Flashback Team** — https://www.youtube.com/@FlashbackTeam
- **Matt Brown** — https://www.youtube.com/@mattbrwn/videos
- **LiveOverflow** — https://www.youtube.com/@LiveOverflow
- **Colin O'Flynn** — https://www.youtube.com/@ColinOFlynn
- **Joe Grand** — https://www.youtube.com/@JoeGrand
- **RECESSIM** — https://www.youtube.com/@RECESSIM
- **Billy Ellis** — https://www.youtube.com/@BillyEllis/videos
- **GuidedHacking** — https://www.youtube.com/@GuidedHacking
- **IoTVillage** — https://www.youtube.com/@IoTVillage
- **RealPars** — https://www.youtube.com/channel/UCUKKQwBQZczpYzETkZNxi-w

### Training
- **OpenSecurityTraining2** — https://ost2.fyi/
- **Cyberpath: Practical IoT Hacking** — https://cyberpath.training/
- **Hextree.io** — https://www.hextree.io/
- **Attify Offensive IoT Exploitation** — https://www.attify-store.com/collections/training
- **Hardware Security Training** — https://learn.securinghardware.com/
- **GrandIdeaStudio** — https://grandideastudio.com/training/
- **Introduction to Reverse Engineering with Ghidra** — https://hackaday.io/course/172292-introduction-to-reverse-engineering-with-ghidra

### Other Awesome Lists
- **Awesome Embedded & IoT Security (FKIE)** — https://github.com/fkie-cad/awesome-embedded-and-iot-security
- **Awesome Embedded Security (hexsecs)** — https://github.com/hexsecs/awesome-embedded-security
- **Awesome Embedded Systems Vuln Research** — https://github.com/IamAlch3mist/Awesome-Embedded-Systems-Vulnerability-Research
- **Awesome IoT & Hardware Security** — https://github.com/kayranfatih/awesome-iot-and-hardware-security
- **Awesome Connected Things Security** — https://github.com/V33RU/awesome-connected-things-sec
- **Awesome Bluetooth Security** — https://github.com/engn33r/awesome-bluetooth-security
- **TEE Reversing** — https://github.com/enovella/TEE-reversing
- **Awesome Automotive Security** — https://github.com/hexsecs/awesome-automotive-security
- **Awesome CANbus** — https://github.com/iDoka/awesome-canbus
- **Awesome IoT Hacks** — https://github.com/nebgnahz/awesome-iot-hacks
- **HardwareAllTheThings** — https://github.com/swisskyrepo/HardwareAllTheThings

---

## 3. ICS/SCADA Security — Tools

From https://github.com/hslatman/awesome-industrial-control-system-security

### Analysis & Enumeration
- **AttkFinder** — Static program analysis of PLC programs (IEC 61131-3), produces data-oriented attack vectors. https://gitlab.com/jhcastel/attkfinder
- **CSET** — Cyber Security Evaluation Tool (DHS/CISA). https://github.com/cisagov/cset
- **Digital Bond's 3S CoDeSys Tools** — Command shell, file transfer, Nmap for CoDeSys PLCs. https://www.digitalbond.com/tools/basecamp/3s-codesys/
- **Digital Bond Redpoint** — ICS enumeration via Nmap extensions. https://github.com/digitalbond/Redpoint
- **GRASSMARLIN** — Passive ICS/SCADA network situational awareness. https://github.com/iadgov/GRASSMARLIN
- **ꓘamerka GUI** — Ultimate IoT/ICS reconnaissance tool. https://github.com/woj-ciech/Kamerka-GUI
- **plcscan** — PLC scanner (s7comm/modbus). https://github.com/yanlinlin82/plcscan
- **s7scan** — Siemens PLC enumeration (firmware, HW version, network config). https://github.com/klsecservices/s7scan
- **ModScan** — SCADA MODBUS TCP network mapper. https://github.com/moki-ics/modscan

### Exploitation Frameworks
- **ISF (Industrial Exploitation Framework)** — Python exploitation framework (QNX, Siemens, Schneider). https://github.com/dark-lbp/isf
- **ISEF (Industrial Security Exploitation Framework)** — Based on Equation Group Fuzzbunch. https://github.com/w3h/isf
- **MODBUS Penetration Testing Framework (smod)** — Full modbus pentest framework. https://github.com/0x0mar/smod

### PLC Analysis & Fuzzing
- **ICSREF** — Reverse engineering CODESYS v2 binaries. https://github.com/momalab/ICSREF
- **ICSFuzz** — PLC-side fuzzing for CODESYS/Wago PLCs. https://github.com/momalab/ICSFuzz
- **PLCinject** — Code injection into PLCs. https://github.com/SCADACS/PLCinject
- **SCADAShutdownTool** — ICS automation/testing: enumerate, read/write registers. https://github.com/0xICF/SCADAShutdownTool

### Protocol Tools
- **mbtget** — Modbus transactions from CLI (Perl). https://github.com/sourceperl/mbtget
- **ModbusPal** — MODBUS slave simulator. http://modbuspal.sourceforge.net/
- **NetToPLCSim** — TCP/IP extension for Siemens PLCSim. https://sourceforge.net/projects/nettoplcsim/
- **OpenDNP3** — IEEE-1815 (DNP3) reference implementation. https://dnp3.github.io/
- **Snap7** — Ethernet communication suite for Siemens S7 PLCs. http://snap7.sourceforge.net/
- **S7Comm-Analyzer** — Bro/Zeek plugin for S7comm. https://github.com/dw2102/S7Comm-Analyzer
- **Wireshark** — Protocol analyzer with ICS protocol support. https://www.wireshark.org/

### Defense & Monitoring
- **Quickdraw IDS** — Snort rules + preprocessors for SCADA. https://www.digitalbond.com/tools/quickdraw/download/
- **PCS7-Hardening-Tool** — PowerShell script for Siemens PCS 7 DCS security. https://github.com/otoriocyber/PCS7-Hardening-Tool
- **splonebox** — Network assessment tool with ICS protocol plugins. https://splone.com/splonebox/
- **S7 Password Bruteforcer** — Offline S7 password cracking from PCAP. (list at repo)

### Memory Analysis
- **ics_mem_collect** — Memory collector for GE D20MX. https://github.com/fireeye/ics_mem_collect
- **sixnet-tools** — Exploit Sixnet RTUs for root access. https://github.com/mssabr01/sixnet-tools

### Simulation / Testbeds
- **MiniCPS** — Cyber-Physical Systems security research toolkit. https://github.com/scy-phy/minicps

### Distributions
- **Moki Linux** — Kali-based ICS/SCADA pentesting distribution. https://github.com/moki-ics/moki
- **ControlThings Platform** — ICS security assessment Linux distro. https://www.controlthings.io/

### Honeypots
- **Conpot** — Low-interactive ICS honeypot. https://github.com/mushorg/conpot
- **GasPot** — Veeder Root Guardian AST honeypot. https://github.com/sjhilt/GasPot
- **T-Pot** — Multi-honeypot platform (includes Conpot). https://dtag-dev-sec.github.io/mediator/feature/2016/03/11/t-pot-16.03.html

### PCAP / Data Sources
- **4SICS ICS Lab PCAPS** — http://www.netresec.com/?page=PCAP4SICS
- **DEF CON 23 ICS Village PCAPS** — https://media.defcon.org/DEF%20CON%2023/DEF%20CON%2023%20villages/DEF%20CON%2023%20ics%20village/
- **ICS PCAP Collection** — https://github.com/automayt/ICS-pcap
- **S7 PCAP samples** — https://sourceforge.net/projects/s7commwireshark/files/Sample-captures/
- **SCADAPASS** — Default/hardcoded ICS passwords. https://github.com/scadastrangelove/SCADAPASS
- **TRISIS/TRITON/HATMAN malware repo** — https://github.com/ICSrepo/TRISIS-TRITON-HATMAN
- **HVAC Traces** — HVAC system PCAPs for NIDS evaluation. https://github.com/gkabasele/HVAC_Traces

### Frameworks
- **I-ISMS** — Industrial Information Security Management System templates. https://github.com/nathanpocock/I-ISMS
- **CIS Controls Implementation Guide for ICS** — https://www.newnettechnologies.com/downloads/Implementation-Guide-for-ICS-using-the-CIS-Controls.pdf

---

## 4. ICS/SCADA Security — Resources & Literature

### Key Resources
- **ATT&CK for ICS (MITRE)** — https://collaborate.mitre.org/attackics/index.php/Main_Page
- **SCADAhacker Library** — https://scadahacker.com/library/index.html
- **Robert M. Lee's Getting Started Guide** — https://www.robertmlee.org/a-collection-of-resources-for-getting-started-in-icsscada-cybersecurity/
- **NIST SP 800-82r2** — Guide to ICS Security. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r2.pdf
- **ICS Cyber Kill Chain (SANS)** — https://www.sans.org/reading-room/whitepapers/ICS/industrial-control-system-cyber-kill-chain-36297
- **Abbreviated History of ICS Cybersecurity (SANS)** — https://ics.sans.org/media/An-Abbreviated-History-of-Automation-and-ICS-Cybersecurity.pdf
- **Hacker Machine Interface (TrendMicro)** — https://documents.trendmicro.com/assets/wp/wp-hacker-machine-interface.pdf
- **SCADA Cybersecurity Framework (ISACA)** — http://www.isaca.org/Journal/archives/2014/Volume-1/Documents/SCADA-Cybersecurity-Framework_joa_Eng_0114.pdf
- **OT-CSIO Ontology (FireEye/Mandiant)** — https://www.fireeye.com/blog/threat-research/2019/09/ontology-understand-assess-operational-technology-cyber-incidents.html

### Books
- Applied Cyber Security and the Smart Grid — https://www.amazon.com/Applied-Cyber-Security-Smart-Grid/dp/1597499986/
- Handbook of SCADA/Control Systems Security — https://www.amazon.com/Handbook-Control-Systems-Security-Second/dp/1498717071/
- Industrial Network Security, Second Edition — https://www.amazon.com/Industrial-Network-Security-Second-Edition/dp/0124201148/
- Power System SCADA and Smart Grids — https://www.amazon.com/Power-System-SCADA-Smart-Grids/dp/148222674X

### ICS Feeds & Alerts
- ICS-CERT Alerts — https://ics-cert.us-cert.gov/alerts
- ICS-CERT RSS — https://ics-cert.us-cert.gov/xml/rss.xml
- Siemens Industrial Security Alerts — https://new.siemens.com/global/en/products/services/cert.html
- NERC Alerts — http://www.nerc.com/pa/rrm/bpsa/Pages/Alerts.aspx
- ABB Cybersecurity Alerts — http://new.abb.com/about/technology/cyber-security/alerts-and-notifications
- Schneider Electric Alerts — http://software.schneider-electric.com/support/cyber-security-updates/

### ICS Conferences
- CS3STHLM — https://cs3sthlm.se/
- CS4CA — https://cs3sthlm.se/
- SANS ICS Summit Archives — https://www.sans.org/cyber-security-summit/archives
- SANS ICS Cybersecurity Conference (WeissCon) — http://www.icscybersecurityconference.com/
- Kaspersky Industrial Cybersecurity (KICS con) — https://ics.kaspersky.com/conference/
- ICCPS (ACM/IEEE Cyber-Physical Systems) — https://iccps.acm.org/
- ICSS Workshop — https://www.acsac.org/2024/workshops/icss/
- CyberICPS — https://conferences.ds.unipi.gr/cybericps2025/
- CPSIoTSec — https://cpsiotsec.github.io/
- CPSS (ACM Cyber-Physical System Security) — http://jianying.space/cpss/CPSS2025/
- IEEE ICPS — https://icps2025.ieee-ies.org/
- CPS-Sec Workshop — https://cns2024.ieee-cns.org/workshop/cps-sec-workshop

### ICS Education / Testbeds
- GRFICSv2 — Graphical Realism Framework for ICS simulations. https://github.com/Fortiphyd/GRFICSv2
- LICSTER — Low-cost ICS Security Testbed. https://github.com/hsainnos/LICSTER
- ICS Cyber Security Institute — https://icscsi.org/

### ICS Training (YouTube)
- PLC Training Org — http://plc-training.org/plc-network-to-hmi-scada.html
- Control System Basics — https://www.youtube.com/watch?v=VQLRVjEFRGI
- SCADA Utility 101 — https://www.youtube.com/watch?v=vv2CoTiaWPI
- Control System Lectures — https://www.youtube.com/user/ControlLectures
- The PLC Professor — https://www.youtube.com/user/plcprofessor
- Serial Communications RS232/RS485 — https://www.youtube.com/watch?v=2DQdEHvnqvI
- MODBUS-RTU — https://www.youtube.com/watch?v=OvRD2UvrHjE
- MODBUS Data Structures — https://www.youtube.com/watch?v=8FYFai21JPA
- MODBUS-TCP — https://www.youtube.com/watch?v=E1nsgukeKKA
- Ethernet TCP/IP for Industrial Protocols — https://www.youtube.com/watch?v=DL_zIjhCEpU

---

## 5. Firmware Security (Platform/UEFI) — Tools

From https://github.com/PreOS-Security/awesome-firmware-security and https://github.com/river-li/awesome-uefi-security

### Open-Source Firmware Tools
- **CHIPSEC** — Intel-created platform security assessment framework for BIOS/UEFI. https://github.com/chipsec/chipsec
- **UEFITool** — GUI program to parse, extract, and modify UEFI firmware images (also includes UEFIDump, UEFIExtract, UEFIFind). https://github.com/LongSoft/UEFITool
- **UEFI Firmware Parser** — Library for parsing UEFI firmware images. https://github.com/theopolis/uefi-firmware-parser
- **Flashrom** — Identify/read/write/verify/erase flash chips (BIOS/EFI/coreboot). https://flashrom.org/ / https://github.com/flashrom/flashrom
- **ACPICA tools** — ACPI reference implementation & tools (acpidump, etc.). https://acpica.org/downloads
- **BITS (BIOS Implementation Test Suite)** — Intel bootable pre-OS BIOS testing. https://biosbits.org/
- **FWTS (Firmware Test Suite)** — Canonical's collection of firmware tests. https://launchpad.net/fwts
- **LUV (Linux UEFI Validation)** — Intel distro bundling CHIPSEC + FWTS. https://01.org/linux-uefi-validation
- **LVFS/fwupd** — Linux Vendor Firmware Services for firmware updates. https://fwupd.org/
- **Pawn** — Google's Linux-centric online firmware dumper. https://github.com/google/pawn
- **Sandsifter** — x86 fuzzer. https://github.com/xoreaxeaxeax/sandsifter
- **TXT Suite** — Intel TXT validation suite. https://github.com/9elements/txt-suite
- **Firmadyne** — Automated Linux-based embedded firmware emulation. https://github.com/firmadyne/firmadyne
- **Firmware.re** — Free firmware unpack/scan service. http://firmware.re/
- **DarwinDumper** — macOS system overview/dump tool. https://bitbucket.org/blackosx/darwindumper
- **EFIgy** — Duo Security's macOS EFI firmware checker. https://efigy.io
- **zenfish IPMI tools** — IPMI security testing tools by Dan Farmer. https://github.com/zenfish/ipmi

### UEFI-Specific Tools
- **efiXplorer** — IDA Pro plugin for UEFI binary analysis (best-in-class). https://github.com/binarly-io/efiXplorer
- **brick** — IDA Pro static vulnerability scanner for UEFI. https://github.com/Sentinel-One/brick
- **fwhunt-scan** — Binarly firmware vulnerability scanner. https://github.com/binarly-io/fwhunt-scan
- **FwHunt** — Firmware threat detection at scale. https://github.com/binarly-io/fwhunt
- **qiling (EFI mode)** — Partially emulate UEFI binaries. https://github.com/qilingframework/qiling
- **efiSeek** — Ghidra plugin for UEFI binary analysis. https://github.com/DSecurity/efiSeek
- **efi_fuzz** — Coverage-guided emulator-based NVRAM fuzzer for UEFI (Qiling-based). https://github.com/Sentinel-One/efi_fuzz
- **efi_dxe_emulator** — Simple UEFI DXE file emulator. https://github.com/assafcarlsbad/efi_dxe_emulator
- **uefi_retool** — UEFI RE tool. https://github.com/yeggor/uefi_retool
- **BIOSUtilities** — Scripts to parse/extract UEFI firmware from EXE files. https://github.com/platomav/BIOSUtilities
- **innoextract** — Unpack Inno Setup installers (firmware updates). https://github.com/dscharrer/innoextract
- **EfiGuard** — UEFI bootkit/security tool. https://github.com/Mattiwatti/EfiGuard
- **ghidra-firmware-utils** — Ghidra firmware helpers. https://github.com/al3xtjames/ghidra-firmware-utils
- **dropWPBT** — Remove Windows Platform Binary Table. https://github.com/Jamesits/dropWPBT
- **fwexpl** — Firmware exploit tool. https://github.com/Cr4sh/fwexpl
- **fiano** — LinuxBoot's firmware image manipulation. https://github.com/linuxboot/fiano
- **UefiVarMonitor** — Monitor UEFI variable access. https://github.com/tandasat/UefiVarMonitor
- **VBiosFinder** — Find/extract VBIOS from firmware. https://github.com/coderobe/VBiosFinder
- **kraft_dinner** — Tanda's SMM/ACPI tool. https://github.com/tandasat/kraft_dinner
- **Voyager** — UEFI hypervisor/monitor. https://git.back.engineering/_xeroxz/voyager
- **efi-memory** — UEFI memory manipulation. https://github.com/SamuelTulach/efi-memory
- **smram_parse** — SMRAM parser. https://github.com/Cr4sh/smram_parse
- **ebvm** — EBC (EFI Byte Code) virtual machine. https://github.com/yabits/ebcvm
- **UEFI-SecureBoot-SignTool** — Sign UEFI binaries for SecureBoot. https://github.com/aneesh-neelam/UEFI-SecureBoot-SignTool
- **PciLeech** — DMA attacks against UEFI. https://github.com/ufrisk/pcileech
- **bob_efi_fuzzer** — UEFI fuzzer. https://github.com/HO-9/bob_efi_fuzzer
- **uefi-rs** — Rust wrapper for UEFI development/PoC. https://github.com/rust-osdev/uefi-rs
- **tsffs** — Intel SIMICS-based snapshot fuzzer (UEFI, Kernel, BIOS). https://github.com/intel/tsffs
- **efi-inspector** — Binary Ninja plugin for UEFI firmware parsing. https://github.com/zznop/efi-inspector
- **efi-resolver** — Official Binary Ninja UEFI plugin (type propagation). https://github.com/Vector35/efi-resolver
- **python-uefivars** — Python tool to inspect UEFI variables. https://github.com/awslabs/python-uefivars

### UEFI Developer Tools
- **EDK II** — Tianocore's UEFI development kit. https://github.com/edk2/edk2
- **edk2-pytool-library** — https://github.com/tianocore/edk2-pytool-library
- **edk2-libc** — https://github.com/tianocore/edk2-libc
- **UEFI-Lessons** — https://github.com/Kostr/UEFI-Lessons
- **Visual UEFI** — Visual Studio plugin for UEFI EDK2. https://github.com/ionescu007/VisualUefi
- **Eclipse UEFI EDK2 Wizards** — https://github.com/ffmmjj/uefi_edk2_wizards_plugin

### Bootloaders
- **GRUB** — Multiboot boot loader (BIOS/UEFI). https://www.gnu.org/software/grub/
- **Linux Shim** — UEFI boot loader for Secure Boot chain. https://github.com/rhboot/shim
- **rEFInd** — UEFI boot manager. http://www.rodsbooks.com/refind/
- **Linux Stub** — Linux kernel as BIOS/EFI boot loader. https://www.kernel.org/doc/Documentation/efi-stub.txt

### Other Tools
- **RU.EFI** — Third-party UEFI Shell multi-purpose utility. https://github.com/JamesAmiTw/ru-uefi/
- **RWEverything** — Windows hardware access tool. http://rweverything.com/
- **PhoenixTool** — Manipulate (U)EFI and legacy BIOS firmware. https://forums.mydigitallife.net/threads/13194/
- **UEFI Utilities** — Collection of UEFI Shell diagnostic tools. https://github.com/fpmurphy/UEFI-Utilities-2018

---

## 6. Firmware Security — Techniques & Threats

### Technologies & Terminology
- **UEFI** — Platform firmware technology, EFI successor. https://uefi.org
- **coreboot** — Open-source platform firmware. https://coreboot.org
- **U-Boot** — Embedded bootloader. https://www.denx.de/wiki/U-Boot/
- **SeaBIOS** — Open-source BIOS implementation. https://seabios.org
- **Heads** — Minimal Linux as coreboot/LinuxBoot payload. https://github.com/osresearch/heads
- **LinuxBoot** — Linux kernel replacing UEFI DXE phase. https://www.linuxboot.org/
- **Tianocore** — UEFI Forum's open-source implementation. https://tianocore.org/
- **Intel Boot Guard** — Pre-UEFI boot security. https://en.wikipedia.org/wiki/Intel_vPro#Intel_Boot_Guard
- **Secure Boot** — UEFI security feature for boot process. https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface#Secure_boot
- **Verified Boot** — Google's boot security (Android/ChromeOS). https://source.android.com/security/verifiedboot/
- **Measured Boot** — Intel TPM-based boot security. https://firmware.intel.com/blog/security-technologies-and-minnowboard-max
- **SMM** — Systems Management Mode (Ring -2). https://en.wikipedia.org/wiki/System_Management_Mode
- **TrustZone** — ARM security extension (Management Mode). https://www.arm.com/products/security-on-arm/trustzone
- **TPM** — Trusted Platform Module. http://www.trustedcomputinggroup.org/
- **Intel ME** — Management Engine (MINIX-based). https://en.wikipedia.org/wiki/Intel_Management_Engine
- **AMD PSP** — Platform Security Processor. https://en.wikipedia.org/wiki/AMD_Platform_Security_Processor
- **BMC** — Baseboard Management Controller. https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface#Baseboard_management_controller
- **OpenBMC** — Open-source BMC Linux distribution. https://github.com/openbmc/openbmc
- **Redfish** — Modern IPMI replacement. http://dmtf.org/standards/redfish/
- **Intel AMT** — Active Management Technology. https://software.intel.com/en-us/articles/developing-for-intel-active-management-technology-amt
- **ACPI** — Advanced Configuration and Power Interface. http://uefi.org/acpi/
- **ACPICA** — ACPI Component Architecture. https://acpica.org

### Known Threats
- **BadBIOS** — Alleged firmware malware. https://en.wikipedia.org/wiki/BadBIOS
- **Evil Maid Attack** — Physical access firmware attack. https://theinvisiblethings.blogspot.com/2011/09/anti-evil-maid.html
- **Hacking Team UEFI Malware** — Government-sold UEFI attack. https://attack.mitre.org/wiki/Software/S0047
- **ThinkPwn** — UEFI malware PoC (ThinkPad). https://github.com/Cr4sh/ThinkPwn
- **PCILeech** — PCI-based DMA attack. https://github.com/ufrisk/pcileech/
- **Rowhammer** — DRAM-based attack. https://en.wikipedia.org/wiki/Row_hammer
- **USB Rubber Ducky** — Rogue USB HID device. https://hakshop.com/products/usb-rubber-ducky-deluxe
- **Fish2 IPMI Security** — IPMI insecurities. http://www.fish2.com/ipmi/

### UEFI Bootkits (Chronological)
| Date | Name | URL |
|------|------|-----|
| Nov 2024 | Bootkitty | https://www.welivesecurity.com/en/eset-research/bootkitty-analyzing-first-uefi-bootkit-linux/ |
| Oct 2022 | BlackLotus | https://www.welivesecurity.com/2023/03/01/blacklotus-uefi-bootkit-myth-confirmed/ |
| Jul 2022 | CosmicStrand | https://securelist.com/cosmicstrand-uefi-firmware-rootkit/106973/ |
| Jan 2022 | MoonBounce | https://securelist.com/moonbounce-the-dark-side-of-uefi-firmware/105468/ |
| Oct 2021 | Especter | https://www.welivesecurity.com/2021/10/05/uefi-threats-moving-esp-introducing-especter-bootkit/ |
| Sep 2021 | FinSpy | https://securelist.com/finspy-unseen-findings/104322/ |
| Dec 2020 | Trickbot/TrickBoot | https://eclypsium.com/wp-content/uploads/2020/12/TrickBot-Now-Offers-TrickBoot-Persist-Brick-Profit.pdf |
| Oct 2020 | MosaicRegressor | https://securelist.com/mosaicregressor/98849/ |
| 2018 | LoJax | https://www.welivesecurity.com/2018/09/27/lojax-first-uefi-rootkit-found-wild-courtesy-sednit-group/ |

### Bootkit Repositories
- **LoJax** — https://github.com/loneicewolf/LOJAX
- **umap** — https://github.com/btbd/umap
- **UEFI-Bootkit** — https://github.com/ajkhoury/UEFI-Bootkit
- **SmmBackdoor** — https://github.com/Cr4sh/SmmBackdoor
- **PeiBackdoor** — https://github.com/Cr4sh/PeiBackdoor
- **bootlicker** — https://github.com/realoriginal/bootlicker

### UEFI Vulnerabilities & Exploits
- **PixieFail** — 9 vulns in EDK II IPv6 stack. https://blog.quarkslab.com/pixiefail-nine-vulnerabilities-in-tianocores-edk-ii-ipv6-network-stack.html
- **Vulnerability-REsearch (Binarly)** — https://github.com/binarly-io/Vulnerability-REsearch
- **vulnerability-disclosures (ESET)** — https://github.com/eset/vulnerability-disclosures
- **vulnerabilities (10TG)** — https://github.com/10TG/vulnerabilities
- **CVE-2022-3430/3431/3432** — Lenovo NVRAM vulns disable Secure Boot.
- **CVE-2022-4020** — Acer NVRAM vuln.
- **ThinkPwn** — https://github.com/Cr4sh/ThinkPwn
- **Aptiocalypsis** — https://github.com/Cr4sh/Aptiocalypsis
- **UsbRt_ROP** — https://github.com/binarly-io/Research_Publications/tree/main/OffensiveCon_2022/UsbRt_ROP_PoC
- **CVE-2022-21894** — https://github.com/Wack0/CVE-2022-21894
- **CVE-2014-8274** — https://www.kb.cert.org/vuls/id/976132
- **Super-UEFIinSecureBoot-Disk** — https://github.com/ValdikSS/Super-UEFIinSecureBoot-Disk
- **SmmExploit** — https://github.com/tandasat/SmmExploit
- **CERT/CC UEFI Analysis Resources** — https://github.com/CERTCC/UEFI-Analysis-Resources

### UEFI CTF Challenges
- **UIUCTF-2022 SMM Cow Say 1** — https://github.com/sigpwny/UIUCTF-2022-Public/tree/main/systems/smm_cowsay_1
- **UIUCTF-2022 SMM Cow Say 2** — https://github.com/sigpwny/UIUCTF-2022-Public/tree/main/systems/smm_cowsay_2
- **UIUCTF-2022 SMM Cow Say 3** — https://github.com/sigpwny/UIUCTF-2022-Public/tree/main/systems/smm_cowsay_3
- **D^3CTF-2022 d3guard** — https://github.com/yikesoftware/d3ctf-2022-pwn-d3guard
- **corCTF 2023 smm-diary** — https://2023.cor.team/challs
- **Dubhe CTF 2024 ToySMM** — https://dubhectf2024.xctf.org.cn/
- **DVUEFI (Damn Vulnerable UEFI)** — https://github.com/hacking-support/DVUEFI

### UEFI Security Papers
- **RSFUZZER: Discovering SMI Handler Vulns (S&P 2023)** — https://www.computer.org/csdl/proceedings-article/sp/2023/933600b765/1Js0Ek1SE6c
- **SoK: Security Below the OS (arXiv 2023)** — http://arxiv.org/abs/2311.03809
- **Finding SMM Privilege-Escalation Vulns (S&P 2022)** — https://dblp.uni-trier.de/conf/sp/YinLWSZHX22
- **UEFI Firmware Fuzzing with Simics (DAC 2020)** — https://dblp.uni-trier.de/conf/dac/YangVYYZ20
- **FUZZUER: Fuzzing UEFI Interfaces on EDK-2 (NDSS 2025)** — https://machiry.github.io/files/fuzzuerr.pdf
- **STASE: Symbolic Execution for UEFI (ASE 2024)** — https://dl.acm.org/doi/10.1145/3691620.3695543
- **UEFI Memory Forensics (arXiv 2025)** — https://arxiv.org/pdf/2501.16962
- **Bootkits: Past, Present & Future (Virus Bulletin 2014)** — https://www.virusbulletin.com/uploads/pdf/conference/vb2014/VB2014-RodionovMatrosov.pdf
- **Thunderstrike: EFI bootkits for MacBooks (SYSTOR 2015)** — https://dl.acm.org/doi/pdf/10.1145/2757667.2757673
- **Symbolic Execution for BIOS Security (WOOT 2015)** — https://www.usenix.org/system/files/conference/woot15/woot15-paper-bazhaniuk.pdf

### UEFI Blogs
- **Binarly** — https://www.binarly.io
- **Cr4sh** — http://blog.cr4.sh/
- **Eclypsium** — https://eclypsium.com
- **ESET Research** — https://www.welivesecurity.com
- **Sentinel Labs** — https://sentinelone.com/
- **Synacktiv** — https://www.synacktiv.com
- **NCC Group** — https://research.nccgroup.com

### UEFI Training
- Advanced x86: Intro to BIOS & SMM — https://opensecuritytraining.info/IntroBIOS.html
- UEFI Official Learning Center — https://uefi.org/learning_center
- EDK II Secure Code Review Guide — https://edk2-docs.gitbook.io/edk-ii-secure-code-review-guide/
- Tianocore Training — https://github.com/tianocore-training/Tianocore_Training_Contents/wiki
- Intel Firmware Security Training — https://github.com/advanced-threat-research/firmware-security-training
- Open Security Training: Intro to BIOS & SMM — http://opensecuritytraining.info/IntroBIOS.html

### UEFI Documentation
- UEFI Forum — https://uefi.org/
- UEFI Specification v2.10 — https://uefi.org/sites/default/files/resources/UEFI_Spec_2_10_Aug29.pdf
- UEFI PI Specification v1.7a — https://uefi.org/sites/default/files/resources/PI_Spec_1_7_A_final_May1.pdf
- UEFI Shell Specification v2.2 — http://www.uefi.org/sites/default/files/resources/UEFI_Shell_2_2.pdf
- ACPI Specification v6.5 — https://uefi.org/sites/default/files/resources/ACPI_Spec_6_5_Aug29.pdf
- UEFI DBX Revocation List — https://www.uefi.org/revocationlistfile

### NIST Firmware Guidance
- **SP 800-193** (Platform Firmware Resiliency) — https://csrc.nist.gov/CSRC/media/Publications/sp/800-193/draft/documents/sp800-193-draft.pdf
- **SP 800-147** (BIOS Protection) — https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-147.pdf
- **SP 800-147b** (BIOS Protection for Servers) — https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-147B.pdf
- **SP 800-155** (BIOS Integrity Measurement) — https://csrc.nist.gov/csrc/media/publications/sp/800-155/draft/documents/draft-sp800-155_dec2011.pdf

### Books
- Beyond BIOS (3rd Ed) — https://www.degruyter.com/view/product/484468
- Harnessing the UEFI Shell (2nd Ed) — https://www.degruyter.com/view/product/484477
- Rootkits and Bootkits — https://nostarch.com/rootkits
- Linux on UEFI (online book) — http://www.rodsbooks.com/linux-uefi/

---

## 7. UEFI Security — Tools (Consolidated from multiple sources)

- **efiXplorer (IDA Pro)** — https://github.com/binarly-io/efiXplorer
- **brick (IDA Pro)** — https://github.com/Sentinel-One/brick
- **efiSeek (Ghidra)** — https://github.com/DSecurity/efiSeek
- **efi-inspector (Binary Ninja)** — https://github.com/zznop/efi-inspector
- **efi-resolver (Binary Ninja official)** — https://github.com/Vector35/efi-resolver
- **UEFITool / UEFIExtract / UEFIFind / UEFIDump** — https://github.com/LongSoft/UEFITool
- **UEFI Firmware Parser** — https://github.com/theopolis/uefi-firmware-parser
- **BIOSUtilities** — https://github.com/platomav/BIOSUtilities
- **fiano** — https://github.com/linuxboot/fiano
- **ghidra-firmware-utils** — https://github.com/al3xtjames/ghidra-firmware-utils
- **CHIPSEC** — https://github.com/chipsec/chipsec
- **FWTS** — https://launchpad.net/fwts
- **LUV** — https://01.org/linux-uefi-validation
- **LVFS / fwupd** — https://fwupd.org/
- **TXT Suite** — https://github.com/9elements/txt-suite
- **Pawn** — https://github.com/google/pawn
- **EFIgy** — https://efigy.io
- **Python UEFIvars** — https://github.com/awslabs/python-uefivars
- **qiling (EFI mode)** — https://github.com/qilingframework/qiling
- **efi_fuzz** — https://github.com/Sentinel-One/efi_fuzz
- **bob_efi_fuzzer** — https://github.com/HO-9/bob_efi_fuzzer
- **tsffs (Intel SIMICS fuzzer)** — https://github.com/intel/tsffs
- **efi_dxe_emulator** — https://github.com/assafcarlsbad/efi_dxe_emulator
- **uefi_retool** — https://github.com/yeggor/uefi_retool
- **PciLeech (DMA attacks)** — https://github.com/ufrisk/pcileech
- **uefi-rs (Rust)** — https://github.com/rust-osdev/uefi-rs
- **EfiGuard** — https://github.com/Mattiwatti/EfiGuard
- **UefiVarMonitor** — https://github.com/tandasat/UefiVarMonitor
- **SmmExploit** — https://github.com/tandasat/SmmExploit
- **kraft_dinner** — https://github.com/tandasat/kraft_dinner
- **smram_parse** — https://github.com/Cr4sh/smram_parse
- **fwexpl** — https://github.com/Cr4sh/fwexpl
- **Voyager** — https://git.back.engineering/_xeroxz/voyager
- **RU.EFI** — https://github.com/JamesAmiTw/ru-uefi/
- **RWEverything** — http://rweverything.com/
- **Sandsifter** — https://github.com/xoreaxeaxeax/sandsifter
- **ACPICA tools** — https://acpica.org/downloads
- **BITS** — https://biosbits.org/
- **innoextract** — https://github.com/dscharrer/innoextract
- **dropWPBT** — https://github.com/Jamesits/dropWPBT
- **ebvm** — https://github.com/yabits/ebcvm
- **UEFI-SecureBoot-SignTool** — https://github.com/aneesh-neelam/UEFI-SecureBoot-SignTool
- **VBiosFinder** — https://github.com/coderobe/VBiosFinder
- **efi-memory** — https://github.com/SamuelTulach/efi-memory
- **arch-secure-boot** — https://github.com/maximbaz/arch-secure-boot

---

## 8. UEFI Security — Bootkits & Exploits (Consolidated)

### Bootkit Timeline
| Nov 2024 | Bootkitty (first Linux UEFI bootkit) | https://www.welivesecurity.com/en/eset-research/bootkitty-analyzing-first-uefi-bootkit-linux/ |
| Oct 2022 | BlackLotus | https://www.welivesecurity.com/2023/03/01/blacklotus-uefi-bootkit-myth-confirmed/ |
| Jul 2022 | CosmicStrand | https://securelist.com/cosmicstrand-uefi-firmware-rootkit/106973/ |
| Jan 2022 | MoonBounce | https://securelist.com/moonbounce-the-dark-side-of-uefi-firmware/105468/ |
| Oct 2021 | Especter | https://www.welivesecurity.com/2021/10/05/uefi-threats-moving-esp-introducing-especter-bootkit/ |
| Sep 2021 | FinSpy | https://securelist.com/finspy-unseen-findings/104322/ |
| Dec 2020 | Trickboot | https://eclypsium.com/wp-content/uploads/2020/12/TrickBot-Now-Offers-TrickBoot-Persist-Brick-Profit.pdf |
| Oct 2020 | MosaicRegressor | https://securelist.com/mosaicregressor/98849/ |
| 2018 | LoJax (first UEFI rootkit in wild) | https://www.welivesecurity.com/2018/09/27/lojax-first-uefi-rootkit-found-wild-courtesy-sednit-group/ |

---

## 9. Red Teaming — Embedded/Peripheral Device Hacking

From https://github.com/r3p3r/yeyintminthuhtut-Awesome-Red-Teaming

### Physical / RFID / NFC
- Proxmark3 & ProxBrute — https://www.trustwave.com/Resources/SpiderLabs-Blog/Getting-in-with-the-Proxmark-3-and-ProxBrute/
- RFID Badge Copying Guide — https://blog.nviso.be/2017/01/11/a-practical-guide-to-rfid-badge-copying/
- Physical Pentester Backpack — https://www.tunnelsup.com/contents-of-a-physical-pen-testers-backpack/
- MagSpoof (credit card/magstripe spoofer) — https://github.com/samyk/magspoof
- Wireless Keyboard Sniffer (KeySweeper) — https://samy.pl/keysweeper/
- RFID Hacking with Proxmark 3 — https://blog.kchung.co/rfid-hacking-with-the-proxmark-3/
- Proxmark: Swiss Army Knife for RFID — https://www.cs.bham.ac.uk/~garciaf/publications/Tutorial_Proxmark_the_Swiss_Army_Knife_for_RFID_Security_Research-RFIDSec12.pdf
- Exploring NFC Attack Surface — https://media.blackhat.com/bh-us-12/Briefings/C_Miller/BH_US_12_Miller_NFC_attack_surface_WP.pdf
- Outsmarting Smartcards (PhD thesis) — http://gerhard.dekoninggans.nl/documents/publications/dekoninggans.phd.thesis.pdf
- Reverse engineering HID iClass Master keys — https://blog.kchung.co/reverse-engineering-hid-iclass-master-keys/
- Android Open Pwn Project (AOPP) — https://www.pwnieexpress.com/aopp

### Hardware Implant / USB
- Bash Bunny — https://hakshop.com/products/bash-bunny
- USB Rubber Ducky — https://hakshop.com/products/usb-rubber-ducky-deluxe
- USB Drop Attacks — https://www.redteamsecure.com/usb-drop-attacks-the-danger-of-lost-and-found-thumb-drives/
- PlugBot: Hardware Botnet — https://www.redteamsecure.com/the-plugbot-hardware-botnet-research-project/

---

## 10. Articles & Blog Extracts

### Robert M. Lee — Getting Started in ICS/SCADA Cybersecurity
**Source:** https://www.robertmlee.org/a-collection-of-resources-for-getting-started-in-icsscada-cybersecurity/
**Last Updated:** January 2023

Key insights:
- IT vs. OT/ICS: The biggest difference is the MISSION function. IT focuses on system and data; ICS is about adversaries manipulating multiple systems to cause physical manifestation.
- Physics and safety are paramount: protect people, environment, and operations.
- Structured approach: Prerequisites → Intro to Control Systems → Network Security → ICS Cybersecurity → Books → Training → Conferences.
- Recommended training: SANS ICS courses. "If your employer doesn't have a training policy, find a new employer."
- Conferences: "The Big 5" ICS cybersecurity conferences.
- Advice: Start with the mission, self-teach aggressively, be skeptical of sources, build hands-on skills, engage with the community.

### Firmware Security Blog — Tag: awesome
**Source:** https://firmwaresecurity.com/tag/awesome/

Key announcements/links:
- **PreOS Security awesome-firmware-security** — https://github.com/PreOS-Security/awesome-firmware-security
- Awesome lists collection includes:
  - awesome-threat-detection — https://github.com/0x4D31/awesome-threat-detection
  - awesome-fuzzing — https://github.com/secfigo/Awesome-Fuzzing
  - awesome-malware-analysis — https://github.com/rshipp/awesome-malware-analysis
  - awesome-symbolic-execution — https://github.com/ksluckow/awesome-symbolic-execution
  - awesome-yara — https://github.com/InQuest/awesome-yara
  - awesome-osint — https://github.com/jivoi/awesome-osint
  - awesome-exploit-development — https://github.com/FabioBaroni/awesome-exploit-development
  - awesome-vehicle-security — https://github.com/jaredmichaelsmith/awesome-vehicle-security
  - awesome-safety-critical — https://github.com/stanislaw/awesome-safety-critical
  - awesome-cve-poc — https://github.com/qazbnm456/awesome-cve-poc
  - awesome-incident-response — https://github.com/meirwah/awesome-incident-response
  - awesome-forensics — https://github.com/cugu/awesome-forensics
  - awesome-threat-intelligence — https://github.com/hslatman/awesome-threat-intelligence
  - awesome-hacking — https://github.com/carpedm20/awesome-hacking
  - awesome-reversing — https://github.com/fdivrp/awesome-reversing

### Infosec Institute Article
**URL:** https://www.infosecinstitute.com/resources/scada-ics-security/ics-scada-security-technologies-and-tools/
**Status:** BLOCKED by Cloudflare — content could not be retrieved via curl, web_extract, or browser.

---

## Notes

- All GitHub/GitLab/project URLs have been preserved in full as requested.
- The infosecinstitute.com article (ICS/SCADA Security Technologies and Tools) was blocked by Cloudflare's bot protection on all retrieval methods.
- This document consolidates tools and techniques from 8 repos and 2 web articles.
- Red Teaming repo (r3p3r) focuses mostly on IT/AD red teaming; only the embedded/peripheral devices section (Section 5 of that repo) was extracted.
