# Pwn2Own Techniques & Tools Reference

## Overview
Compiled from: Reversec Labs blog, Wikipedia, pwn2ooown.tech CTF writeup, 0vercl0k's Pwn2Own 2023 Miami repo, and Android kernel exploitation workshop (cloudfuzz).

---

## 1. History & Contest Structure (Wikipedia + Reversec Labs)

- **Started:** 2007 by Dragos Ruiu (CanSecWest). Goal: prove Mac OS X was exploitable.
- **Organizer:** Zero Day Initiative (ZDI) / Trend Micro.
- **Categories (evolved over time):** Browsers (Chrome, Safari, Firefox, Edge, IE), Mobile (Android, iOS), ICS/SCADA, Vehicles (Tesla), Smart TVs, Printers, Routers, NAS, Smart Speakers, SOHO devices.
- **Prize:** Hacked device + cash (up to $400K+ in one contest for VUPEN in 2014).
- **2024 (AIS3 EOF):** Raspberry Pi-based Pwn2Own challenge with evolving firmware versions.

---

## 2. Vulnerability Categories & Techniques from All Sources

### A. Memory Corruption Exploits

| Technique | Source | Details |
|-----------|--------|---------|
| **Use-After-Free (UAF)** | Pwn2Own Miami 2023 (CVE-2023-32174), Android Kernel (CVE-2019-2215) | Race condition between AddServer/RemoveServer in OPC UA Gateway; binder_thread UAF in Android kernel |
| **Heap Underflow** | Pwn2Own 2018 Safari | Exploited in Safari browser rendering engine |
| **Null Pointer Dereference** | Pwn2Own Miami 2023 (CVE-2023-32171) | Broken XML parsing in TagFile.ImportCsv |
| **Stack Buffer Overflow** | AIS3 EOF Pwn2Own 2024 (v14) | strcpy in auth binary, ROP to system() |
| **Race Condition → UAF** | Pwn2Own Miami 2023 (CVE-2023-32174) | Two threads racing AddServer/RemoveServer, no proper locking → UAF of virtual method dispatch |
| **Uninitialized Memory** | Pwn2Own 2018 Safari T2 talk | Used for sandbox breakout |
| **Integer Overflow → Infinite Loop** | CVE-2023-32170 | ASN1 certificate parsing integer overflow → size=0 → no forward progress → infinite loop DoS |

### B. Logic/Design Vulnerabilities

| Technique | Source | Details |
|-----------|--------|---------|
| **Logic Bug Chains** | Huawei Mate 9 Pro (2017), Chainspotting (2018) | 11 logic bugs across 6 Android apps chained for silent APK installation |
| **Command Injection** | AIS3 EOF Pwn2Own v1 | Direct command injection in /cgi-bin/login.cgi password field |
| **Path Traversal** | AIS3 EOF Pwn2Own v3 | ../../html/contest via image_id param → overwrite contest.html |
| **Python Code Injection** | AIS3 EOF Pwn2Own v4 | HTTP_COOKIE passed to python3 -c |
| **JWT Forging** | AIS3 EOF Pwn2Own v11 | Hardcoded secret "A1s3-E0f_2O24" discovered via firmware diff |
| **Webshell Upload** | AIS3 EOF Pwn2Own v11 | Unrestricted .php upload after JWT bypass |
| **XML Injection → Permanent DoS** | CVE-2023-32173 | Invalid XML chars persisted to config → server never starts again |
| **WebView JavaScript Interface Abuse** | Samsung S20 Galaxy Store (2020) | Exposed JS interface via WebView → silent app installation via NFC/WiFi MITM |
| **Logic Bugs Over Memory Corruption** | "The Mate Escape" (2018) | Scaled logic vulnerability hunting on Android handsets |

### C. Android-Specific Exploitation

| Technique | Source | Details |
|-----------|--------|---------|
| **Binder UAF Exploitation** | Android Kernel Workshop (CVE-2019-2215) | CVE-2019-2215: Android Binder Use-After-Free, discovered by syzkaller, exploited in the wild |
| **epoll + binder race** | Android Kernel Workshop | epoll_ctl links binder_thread wait queue → BINDER_THREAD_EXIT frees → process exit triggers use on dangling chunk |
| **iovec Corruption Technique** | Android Kernel Workshop (via Project Zero) | Reallocate freed binder_thread as iovec array → unlink corrupts iov_base/iov_len → scoped read/write |
| **addr_limit Clobbering** | Android Kernel Workshop | Clobber task_struct->thread.addr_limit to 0xFFFFFFFFFFFFFFFE → arbitrary kernel R/W |
| **cred Structure Patching** | Android Kernel Workshop | kWrite uid/gid/euid/egid/fsuid/fsgid to 0, set capabilities to CAP_FULL_SET |
| **SELinux Disable via nsproxy** | Android Kernel Workshop | Leak nsproxy from task_struct → compute kernel base → write 0 to selinux_enforcing |
| **Pipe Blocking for Race Windows** | Android Kernel Workshop | F_SETPIPE_SZ to PAGE_SIZE, fork(), child sleeps 2s then triggers unlink while parent blocks in writev |
| **Socketpair + recvmsg for Scoped Write** | Android Kernel Workshop | AF_UNIX SOCK_STREAM with MSG_WAITALL → block after first iovec → child writes to socket → corrupted iovecs processed |
| **4GB Aligned Page for Spinlock Bypass** | Android Kernel Workshop | mmap at 0x100000000 → lower 32 bits = 0 → overlapped spinlock appears unlocked |
| **CPU Affinity Binding** | Android Kernel Workshop | sched_setaffinity to CPU 0 → prevent SLUB state corruption across cores |

### D. ICS/SCADA Exploitation (Pwn2Own Miami 2023)

| Technique | Source | Details |
|-----------|--------|---------|
| **OPC UA Protocol Fuzzing** | Pwn2Own Miami 2023 (0vercl0k) | Fuzzing with wtf (custom fuzzer) against UaGateway OPC UA server |
| **Post-Auth Anonymous Exploit** | CVE-2023-32171 | TagFile.ImportCsv accessible to anonymous users → NULL deref |
| **Pre-Auth DoS** | CVE-2023-32170 | Integer overflow in ASN1 certificate parsing, no auth needed |
| **OPC UA Protocol Sequence** | CVE-2023-32174 PoC | Hello → Acknowledge → OpenSecureChannel → GetEndpoints → CreateSession → ActivateSession → Call(AddServer/RemoveServer) |

### E. Browser Exploitation (Historical)

| Technique | Source | Details |
|-----------|--------|---------|
| **QuickTime/Safari Flaw** | Pwn2Own 2007 (first ever win) | Dino Dai Zovi wrote exploit overnight |
| **Safari PCRE Exploit** | Pwn2Own 2008 (Charlie Miller) | Regex engine vulnerability in Safari |
| **Chrome Sandbox Escape** | Pwn2Own 2012 (VUPEN) | First successful Chrome sandbox escape on Windows 7 SP1 |
| **Trifecta** | Pwn2Own 2009 (Nils) | Safari, IE8, Firefox all hacked; bypassed DEP & ASLR on Windows 7 Beta |
| **Full Desktop Compromise** | Pwn2Own 2018 Safari (CVE-2018-4199, CVE-2018-4196) | Two CVEs chained for full macOS compromise through Safari 11.0.3 |

### F. Hardware/Firmware Analysis

| Technique | Source | Details |
|-----------|--------|---------|
| **eMMC Dumping** | Samsung Q60 Smart TV (2019) | Board-level analysis, eMMC flash extraction |
| **VDFS Filesystem Analysis** | Samsung Q60 Smart TV (2019) | Proprietary filesystem reverse engineering |
| **Debug Port Exploration** | Samsung Q60 Smart TV (2019) | Hardware debug interface probing |
| **Firmware Diffing** | AIS3 EOF Pwn2Own v11 | binwalk extraction, firmware comparison to discover hardcoded secrets |
| **Binary Exploitation on ARM** | AIS3 EOF Pwn2Own v14 | ROP on ARM (pop {r0, r4, pc} gadget), system() call |

---

## 3. Tools & Methodologies

### Vulnerability Discovery

| Tool | Source | Purpose |
|------|--------|---------|
| **wtf** (by 0vercl0k) | Pwn2Own Miami 2023 | Custom fuzzer for OPC UA server; discovered CVE-2023-32171 |
| **Jandroid** | Reversec Labs (2019) | Template-based APK scanner for Android logic bugs |
| **syzkaller** | Android Kernel Workshop | Kernel fuzzer that originally discovered CVE-2019-2215 |
| **Custom Fuzzing Tools** | Pwn2Own 2018 Safari T2 | Specialized browser fuzzing for Safari |
| **KASan (Kernel Address Sanitizer)** | Android Kernel Workshop | Kernel build with CONFIG_KASAN for UAF detection |
| **kasan_symbolize.py** | Android Kernel Workshop | Symbolize KASan crash reports |
| **binwalk** | AIS3 EOF Pwn2Own | Firmware extraction and analysis |
| **Firmware Diffing** | AIS3 EOF Pwn2Own | Extract + compare firmware versions to find patches/secrets |

### Exploitation Tooling

| Tool | Source | Purpose |
|------|--------|---------|
| **ROP Gadgets** | AIS3 EOF v14 | `pop {r0, r4, pc}` + call to system() on ARM |
| **Python asyncua/opcua-asyncio** | Pwn2Own Miami 2023 | OPC UA client libraries for exploit PoCs |
| **WinDbg** | Pwn2Own Miami 2023 | Debugging UaGateway.exe, PageHeap for heap analysis |
| **GDB** | Android Kernel Workshop | Dynamic kernel analysis, GDB macros for KGDB |
| **Android NDK** | Android Kernel Workshop | Cross-compilation of kernel exploits |
| **Android Emulator (AVD)** | Android Kernel Workshop | Custom kernel booting with -show-kernel flag |
| **PageHeap (gflags)** | Pwn2Own Miami 2023 | Enable per-process heap verification |

### Static/Dynamic Analysis

| Tool | Source | Purpose |
|------|--------|---------|
| **Visual Studio Code** | Android Kernel Workshop | Kernel source navigation with intellisense (vscode-linux-kernel) |
| **Kernel Tracing** | Android Kernel Workshop | ftrace for dynamic analysis of kernel code paths |
| **Static Analysis of syscall chains** | Android Kernel Workshop | Trace open → epoll_create → epoll_ctl → ioctl → exit_group |

---

## 4. Key Exploit Primitives & Patterns

### Android Kernel EoP via CVE-2019-2215 (FULL CHAIN):

```
Step 1: bindToCPU() - sched_setaffinity to core 0
Step 2: leakTaskStruct()
    - open /dev/binder, epoll_create, pipe with PAGE_SIZE capacity
    - link epoll wait queue to binder_thread via epoll_ctl(EPOLL_CTL_ADD)
    - fork() → child sleeps 2s, parent frees binder_thread (BINDER_THREAD_EXIT)
    - Parent reallocates via writev with crafted iovec stack (25 iovecs = 400 bytes)
    - Child triggers unlink (epoll_ctl EPOLL_CTL_DEL) → corrupts iovecStack[10].iov_len and iovecStack[11].iov_base
    - Parent reads leaked kernel data → extracts task_struct pointer
Step 3: clobberAddrLimit()
    - socketpair(AF_UNIX, SOCK_STREAM), recvmsg with MSG_WAITALL
    - Same UAF + iovec realloc → overwrite iovec pointers
    - Write 0xFFFFFFFFFFFFFFFE to task_struct->thread.addr_limit
Step 4: Arbitrary R/W via pipe
    - write(kernel_addr) to pipe → read from pipe → arbitrary read
    - write to pipe → read(kernel_addr) from pipe → arbitrary write
Step 5: patchCred() - overwrite cred->uid/gid/euid/etc to 0, set capabilities
Step 6: disableSELinuxEnforcing() - leak nsproxy → compute kernel base → write 0 to selinux_enforcing
Step 7: spawnRootShell() - system("/bin/sh")
```

### Key Offsets & Structures:

- `binder_thread` = 408 bytes → kmalloc-512 cache
- `iovec` = 16 bytes → 25 iovecs = 400 bytes (fits in freed binder_thread, leaving task_struct pointer intact)
- `binder_thread->wait` at offset 0xA0 → aligns to iovecStack[10]
- `wait.lock` overlaps iovecStack[10].iov_base
- `wait.head.next` overlaps iovecStack[10].iov_len
- `wait.head.prev` overlaps iovecStack[11].iov_base

---

## 5. Pwn2Own 2024 AIS3 EOF - Evolving Firmware Challenge

A Raspberry Pi target with continuously patched firmware. Key lessons:

| Version | Vulnerability | Technique |
|---------|--------------|-----------|
| v1 | Command injection in login | `DISPLAY=:0` + chromium to attacker .mp4 |
| v3 | Path traversal + overwrite | Upload redirect HTML as contest.html via ../../ |
| v4 | Python code injection | Cookie passed to `python3 -c` |
| v11 | Webshell + forged JWT | Hardcoded secret + unrestricted .php upload |
| v14 | Stack buffer overflow | ROP chain to system() on ARM |

**Key takeaway:** After each demo, vendors patched the exploited bug. Attackers had to find new vulnerabilities in each version.

---

## 6. Notable Researchers & Teams

- **0vercl0k (Axel Souchet):** Pwn2Own Miami 2023 OPC UA exploits, author of wtf fuzzer
- **VUPEN:** Chrome sandbox escape (2012), $400K in 2014 with 11 zero-days
- **Pinkie Pie:** Chrome on Android exploit (2013 Mobile Pwn2Own)
- **Maddie Stone / Jann Horn (Project Zero):** Original CVE-2019-2215 analysis and exploit
- **CloudFuzz / HackSysTeam (Ashfaq Ansari):** Android kernel exploitation workshop
- **Claroty Research (Team82):** Won Pwn2Own Miami 2023
- **Dino Dai Zovi:** First Pwn2Own winner (2007)
- **Charlie Miller:** First Safari hack (2008)
- **Georgi Geshev, Robert Miller:** Chainspotting - 11 logic bugs chained
- **Ken Gannon:** Samsung S20 RCE (2020)
- **Fabian Beterke:** Safari Pwn2Own 2018 whitepaper
