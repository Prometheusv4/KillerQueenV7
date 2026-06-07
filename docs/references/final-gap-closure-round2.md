# Final Gap Closure — Round 2 Outstanding Items
# Extracted June 2026

---

## PROJECT ZERO 0-DAY RCA (googleprojectzero.github.io/0days-in-the-wild/rca.html)

Complete CVE catalogue of in-the-wild 0-days with published root cause analyses:

### Top Bug Classes (from 60+ CVEs analyzed):
- **JIT Type Confusions**: CVE-2019-11707 (IonMonkey Array.Pop), CVE-2020-16009 (Turbofan Map Deprecation), CVE-2020-6418 (Turbofan side-effect modeling), CVE-2021-30551 (V8 type confusion), CVE-2021-30632 (Turbofan Global property), CVE-2022-1096 (Property Access Interceptor), CVE-2022-1364 (Object Materialization in V8)
- **Use-After-Free**: CVE-2019-1367 (IE JScript), CVE-2019-13720 (Chrome webaudio), CVE-2019-2215 (Android Binder), CVE-2019-7286 (iOS cfprefsd), CVE-2020-0674 (IE JScript), CVE-2020-1380 (IE JScript9), CVE-2020-6820 (Firefox Cache), CVE-2021-1879 (QuickTimePlugin), CVE-2021-1905 (Adreno GPU), CVE-2021-21166 (Chrome Audio), CVE-2021-21206 (Chrome Animations), CVE-2021-30858 (WebKit IndexedDB), CVE-2022-22620 (Safari), CVE-2021-4102 (Turbofan WriteBarrier elision)
- **Font Driver Exploitation**: CVE-2020-0938 (Type 1 BlendDesignPositions), CVE-2020-1020 (Type 1 VToHOrigin), CVE-2020-15999 (FreeType Load_SBit_Png), CVE-2020-27930 (Safari libType1Scaler)
- **Kernel/Driver**: CVE-2019-1458 (win32k task switching), CVE-2020-0986 (splwow64 pointer deref), CVE-2020-1027 (CSRSS buffer overflow), CVE-2020-17087 (cng.sys IOCTL), CVE-2020-27932 (iOS turnstiles), CVE-2020-27950 (XNU Mach Message Trailers), CVE-2021-1732 (win32k xxCreateWindowEx), CVE-2022-21882 (Win32k type confusion), CVE-2022-24521 (CLFS logical error), CVE-2021-1048 (Android kernel refcount)
- **GPU Driver**: CVE-2021-1905 (Adreno), CVE-2022-22706/CVE-2021-39793 (Mali GPU read-only bypass)
- **Exchange**: CVE-2021-26855 (ProxyLogon SSRF)
- **Samsung**: CVE-2021-25337 (clipboard), CVE-2021-25369 (sec_log info leak), CVE-2022-22265 (NPU double free)
- **Logic Bugs**: CVE-2021-1647 (Windows Defender mpengine), CVE-2021-37975 (V8 GC logic bug), CVE-2021-38000 (Chrome Intents), CVE-2022-3723 (Turbofan JIT logic)
- **AppleAVD**: CVE-2022-22675 (AVC_RBSP::parseHRD overflow), CVE-2022-32917 (AppleSPU OOB write)
- **WebRTC**: CVE-2022-2294 (heap buffer overflow)

### Pattern: JIT bugs + UAF dominate. Font drivers are a persistent attack surface. GPU drivers emerging. Logic bugs growing.

---

## USENIX SECURITY 2025 — KEY PAPERS

- **AidFuzzer**: Adaptive Interrupt-Driven Firmware Fuzzing — 8 new vulns in RT-Thread, Mynewt-OS
- **TransFuzz**: Confused deputy attacks on EDA software — 20 translation vulns, 31 bugs, 25 CVEs
- **COAT/CORF**: Cross-app OAuth Account Takeover + Request Forgery — 11 of 18 platforms vulnerable, CVSS 9.6
- **StruQ**: Defending Against Prompt Injection with Structured Queries — separate prompts from data
- **BLE Proximity Tracking**: 7 new vulns in Apple Find My + Samsung Find My Mobile
- **StackWarp**: Architectural attacks (referenced but details not in summary)
- **NeuroScope**: Reverse engineering DNN binaries on edge devices
- **Firmware fuzzing** and **IoT security** are major themes

---

## BLACK HAT USA 2017 GIST (naotokatsumi)

Topics covered (from session list):
- Web cache deception
- Multi-target SQLite exploitation
- Serverless runtime hacking
- Cloud orchestration security (Kubernetes/Mesos/Docker)
- Docker API RCE
- New SSRF techniques

Note: Full content not extracted (GitHub gist rendering issue)

---

## REMAINING OUTSTANDING (genuinely blocked):

- **ddosi.org full dataset**: 14,617 entries, JS pagination broken. Only 15 extracted.
- **NCC Group 2025 Report**: Failed to fetch (server error)
- **H1 reports 3475626, 2899858**: Needs authenticated HackerOne access
- **bugboard.rsecloud.com**: Timed out
- **GitLab work item 23606**: Timed out
- **kslr/simple-cloudflare-bypass**: Empty response
- **0day spreadsheet**: Local D:\ path, not accessible
- **infosecinstitute.com ICS**: Cloudflare bot protection
- **Orange Tsai individual slides**: Repository structure extracted, individual slide content not deep-read

---

*Generated June 2026*
