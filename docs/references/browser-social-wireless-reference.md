# BROWSER EXPLOITATION + SOCIAL ENGINEERING + WIRELESS/RF + PHYSICAL SECURITY
## Killer Queen Knowledge Base — Combined Reference

*Consolidated from: browser-exploitation-reference.md, awesome-redteam.md, red-team-tradecraft-reference.md, and web research.*

---

## BROWSER EXPLOITATION

### 1. Browser Engine Architectures

#### 1.1 Chromium / Blink + V8
- **Renderer Engine**: Blink (DOM, layout, rendering)
- **JavaScript Engine**: V8 (Google)
- **Process Model**: Multi-process — 1 Browser Process (unsandboxed) + N Renderer Processes (sandboxed) + GPU, Utility, Extensions
- **Site Isolation**: Each origin gets its own renderer process since Chrome 67

**V8 Pipeline** (evolution):
```
Parser -> Ignition (interpreter) -> Sparkplug (baseline JIT) -> Maglev (mid-tier JIT) -> TurboFan (optimizing JIT)
```
- **Ignition**: Generates bytecode; collects type feedback in Feedback Vectors
- **Sparkplug**: Fast non-optimizing compiler, added 2021
- **Maglev**: Mid-tier SSA compiler between Sparkplug and TurboFan, added Chrome 114 (2023)
- **TurboFan**: Optimizing compiler, Sea of Nodes IR, speculative optimization, type lowering, bounds check elimination

**Key Source Locations**:
- `v8/src/compiler/pipeline.cc` — TurboFan optimization phases
- `v8/src/compiler/opcodes.h` — All IR opcodes
- `v8/src/compiler/typer.cc` — Type inference
- `v8/src/compiler/simplified-lowering.cc` — Bounds check elimination
- `v8/src/interpreter/` — Ignition bytecode
- `v8/src/maglev/` — Maglev compiler

#### 1.2 WebKit / JavaScriptCore (Safari)
- **Renderer Engine**: WebKit
- **JavaScript Engine**: JavaScriptCore (JSC)
- **4-Layer JIT System**: LLInt -> Baseline JIT -> DFG JIT -> FTL JIT (B3 backend)

**Key Source Locations**:
- `Source/JavaScriptCore/llint/` — Low Level Interpreter
- `Source/JavaScriptCore/jit/` — Baseline JIT
- `Source/JavaScriptCore/dfg/` — Data Flow Graph JIT
- `Source/JavaScriptCore/ftl/` — Faster Than Light JIT (uses B3 compiler)
- `Source/JavaScriptCore/runtime/` — JS object model, JSCell, Structures

**Butterfly Memory Layout** (JSC's unique design):
- Properties AND elements stored in the same contiguous memory region called the "butterfly"
- Butterfly header contains length field; elements follow
- This dual-use design is central to many JSC exploitation techniques

#### 1.3 Firefox / SpiderMonkey + Gecko
- **Renderer Engine**: Gecko
- **JavaScript Engine**: SpiderMonkey
- **JIT Compiler**: IonMonkey (optimizing), Baseline (non-optimizing), WarpBuilder
- **Build**: Uses `mozilla-central` via hg or git mirror (`gecko-dev`)

**Key Source Locations**:
- `js/src/jit/` — IonMonkey compiler
- `js/src/builtin/` — Built-in functions
- `js/src/vm/` — JS object model

#### 1.4 Edge (Legacy EdgeHTML + ChakraCore)
- **Modern Edge**: Now Chromium-based (uses V8)
- **Legacy Edge**: EdgeHTML engine + ChakraCore JS engine
- **Source**: `lib/Runtime/Types/`, `lib/Runtime/Language/`

---

### 2. JavaScript Engine Internals (Exploitation Relevant)

#### 2.1 JIT Compilation and Type Feedback
All modern JS engines use speculative JIT compilation:
1. Interpreter collects **type feedback** (which shapes/classes/types a call site sees)
2. When a function is "hot" (runs frequently), the JIT compiles it based on observed types
3. If assumptions break (wrong type arrives), **deoptimization** occurs

**This is the #1 source of exploitable bugs**: JIT optimizations that make incorrect assumptions about types.

#### 2.2 Object Representation

**V8**:
- Objects use **Map** (hidden class) to describe property layout
- Property access uses inline caches (ICs)
- SMI (Small Integer): tagged pointer with LSB = 0
- HeapObject: pointer with LSB = 1
- **Pointer Compression**: In 64-bit V8, heap pointers are 32-bit compressed addresses + 4GB heap base register

**JavaScriptCore**:
- **JSCell**: 8-byte header containing StructureID, flags, and type info
- **Structure**: describes object shape (like V8's Map)
- **Butterfly**: combined property + element storage
- **StructureID**: critical for faking objects; must be guessed/sprayed

**SpiderMonkey**:
- Objects use **Shapes** (like V8 Maps)
- Property storage uses **slots**
- Elements stored separately from named properties

#### 2.3 Garbage Collection
- V8: Orinoco (concurrent, parallel, generational GC)
- JSC: Uses bmalloc for heap management; generational collector
- SpiderMonkey: Generational GC
- **Exploitation relevance**: GC can be triggered to rearrange heap layout (heap feng shui), trigger UAF through race conditions

#### 2.4 Sea of Nodes IR (TurboFan)
TurboFan uses a Sea of Nodes graph with 3 edge types:
- **Control edges**: CFG (branches, loops)
- **Value edges**: Data flow (dependencies)
- **Effect edges**: Order stateful operations

Key optimization phases:
- **TyperPhase**: Computes type information (ranges for integers)
- **TypedLoweringPhase**: Replaces JS ops with lower-level ops
- **SimplifiedLoweringPhase**: Bounds check elimination, truncation

---

### 3. Common Browser Bug Classes

#### 3.1 Type Confusion
**The workhorse of modern browser exploitation.**

V8 Examples:
- CVE-2023-3420: Type confusion from incorrect side effect modeling in JIT
- CVE-2023-4069: Maglev type confusion via `Reflect.construct` with mismatched `new.target`
- CVE-2024-2887: WASM type confusion from improper type count limit enforcement

JSC Examples:
- CVE-2018-4192: Race condition in `Array.reverse()` — free butterfly then reclaim it
- CVE-2017-2446: `JSGlobalObject::havingABadTime` type confusion

#### 3.2 JIT Compiler Bugs (The Crown Jewels)
- **Bounds Check Elimination (BCE) Errors**: TurboFan's `SimplifiedLowering` phase removes bounds checks based on `OperationTyper` ranges
- **Incorrect Side Effects**: JIT assumes operation has no side effects -> eliminates/reorders it
- **Speculative Optimization Bugs**: CVE-2019-5786 (Mojo binding type confusion), CVE-2019-9810 (IonMonkey)

#### 3.3 Use-After-Free (UAF)
- DOM objects freed while JS references remain
- Issue 1062091 (Theori sandbox escape): UAF in `RenderFrameHost` through raw pointer in `SelfOwnedReceiver`
- GC race conditions (CVE-2018-4192 Safari)
- Array buffer detachment, WeakMap/WeakSet edge cases

#### 3.4 Array OOB Access
- CVE-2023-4069 (Maglev): Array created with uninitialized `length` -> OOB
- V8 CTF challenges: `v9`, `Krautflare`, `oob-v8`
- OOB on typed arrays enables direct arbitrary read/write

#### 3.5 WASM-Related Bugs
- CVE-2024-2887: WASM GC type confusion (recursive types)
- WASM bypasses many dynamic checks present in JS JIT pipeline
- Raw pointers in `WasmIndirectFunctionTable` can provide V8 sandbox bypass

---

### 4. Renderer Exploit Primitives

#### 4.1 The Primitive Ladder
```
Vulnerability -> OOB Read/Write -> addrof + fakeobj -> Arbitrary R/W -> Code Execution
```

#### 4.2 addrof (Address Of)
Convert a JS object to its memory address:
```javascript
prims.addrof = function(obj) {
    oob_target[0] = obj;
    return Int64.fromDouble(oob_array[oob_target_index]);
};
```

#### 4.3 fakeobj (Fake Object)
Convert a memory address into a fake JS object reference:
```javascript
prims.fakeobj = function(addr) {
    oob_array[oob_target_index] = addr.asDouble();
    return oob_target[0];
};
```

#### 4.4 Arbitrary Read/Write via Fake TypedArray
1. Use `addrof`/`fakeobj` to create a fake `Float64Array` TypedArray
2. Overwrite the backing store pointer -> typed array reads/writes arbitrary memory
3. Requires guessing StructureID (spray structures to increase predictability)

#### 4.5 JIT Code Overwrite -> Shellcode Execution
- **RWX JIT pages**: Overwrite JIT code with shellcode, call function
- **W^X JIT** (modern V8, JSC): Must use ROP/JOP or function pointer overwrite
- **JIT spraying**: Use JIT compiler to emit attacker-controlled constants that decode to shellcode

#### 4.6 GigaUnCager (JSC-specific)
Project Zero technique to escape the Gigacage:
- DFG/FTL JIT code uncages and unPACs backing store pointers into registers
- Hold more typed arrays than available registers -> force register spilling to stack
- Corrupt the spilled (raw) pointer on the stack -> arbitrary R/W

---

### 5. Sandbox Escape Patterns

#### 5.1 Mojo IPC Bugs (Chrome)
- **Mojo Architecture**: Modern IPC system. IDL -> C++/Java/JS bindings. Key concepts: `MessagePipe`, `Remote`, `PendingReceiver`, `SelfOwnedReceiver`
- **Escape Pattern #1** (Issue 1062091): Raw pointer UAF in browser process via `SelfOwnedReceiver`
- **Escape Pattern #2** (RIDL/MDS): Leak Mojo port names from CPU buffers, inject messages to privileged interfaces
- **Escape Pattern #3** (CVE-2025-2783): Logic bug in `FileSystemAccess` Mojo interface

#### 5.2 Win32k Syscall Filtering Bypass (Chrome Windows)
- Chrome on Win8+ blocks `win32k.sys` syscalls from renderer
- Win7 did NOT receive this backport -> vulnerable to Win32k-based escapes
- CVE-2019-0808: NULL pointer deref in `win32k.sys` via fake menu window

#### 5.3 Filesystem/Named Pipe Escapes (Chrome Windows)
- Named Pipe prefix canonicalization bypass
- SQLite Cookie DB trick: write .bat files to AutoRun folder

#### 5.4 macOS/iOS Sandbox Escapes (Safari)
- **Seatbelt/TinyScheme**: Whitelist-based; deny default, allow explicit resources
- **Mach Lookup**: `com.apple.windowserver.active`, `com.apple.audio.*`
- **IOKit user clients**: `IOHIDParamUserClient`, GPU drivers
- **XPC services**: `com.apple.coremedia.videodecoder`
- **WindowServer**: ~600 remote procedures, root-equivalent
- **DiskArbitrationd Escape** (phoenhex 2017): Mount crafted filesystem -> trigger kernel bug

---

### 6. Browser-Specific Exploit Mitigations

- **Site Isolation** (Chrome): Each origin in separate sandboxed process
- **V8 Heap Sandbox** (Chrome 103+): All V8 heap objects in 4GB virtual address space. Bypass vectors: WASM raw pointers, JSPI stack switching
- **Pointer Compression** (V8): 64-bit pointers compressed to 32-bit
- **W^X JIT Pages**: JIT code pages never simultaneously Writable + Executable
- **Gigacage** (JSC): Primitive heap quarantine for ArrayBuffer backing stores
- **Pointer Authentication Codes (PAC)** (ARM64e): Pointers cryptographically signed
- **APRR** (Apple): Restricts memory permission transitions
- **StructureID Randomization** (JSC): Bypass via Structure ID spraying
- **MiraclePtr** (Chrome): Raw pointer protection in Blink
- **Win32k Lockdown** (Chrome Win8+): Blocks win32k.sys syscalls
- **Seccomp-BPF** (Chrome Linux): Renders only allowed ~100 syscalls

---

### 7. Real Browser Exploit Chains

| Chain | Vulnerability | Sandbox Escape | Target |
|-------|--------------|----------------|--------|
| Pwn2Own 2018 (RET2) | CVE-2018-4192 JSC UAF | WindowServer RCE | Safari + macOS |
| Pwn2Own 2017 (phoenhex) | JSC bug | DiskArbitrationd | Safari + macOS |
| CVE-2019-5786 + 0808 | Mojo binding bug | Win32k NULL deref | Chrome Win7 |
| Issue 1062091 (Theori) | Mojo UAF | Browser process escape | Chrome |
| RIDL Escape (Project Zero) | V8 bug + MDS hardware leak | Mojo port name spoofing | Chrome |
| CVE-2024-2887 (P2O 2024) | WASM type confusion | JSPI stack switching | Chrome |
| Chrome 2025 Kill Chain | CVE-2025-13223 V8 TC | ANGLE GPU + Mojo logic | Chrome |

---

### 8. Fuzzing Targets and Approaches

**JavaScript Engine Fuzzers**:
- **Fuzzilli** (Google Project Zero): Guided fuzzing with FuzzIL intermediate language
  - https://github.com/googleprojectzero/fuzzilli
- **Nautilus**: Grammar-based fuzzing using ANTLR grammars
- **Superion**: Extends AFL with grammar-awareness via ANTLR
- **libfuzzer-js**: Coverage-guided in-process fuzzing

**DOM Fuzzers**:
- **Domato** (Google Project Zero): Grammar-based DOM fuzzer
  - https://github.com/googleprojectzero/domato
- **Morph**: Browser fuzzing framework with crash management
- **Grinder**: Browser fuzzing and crash management framework

**IPC/Wire Protocol Fuzzers**:
- **DIE** (SSLab): Differential fuzzing for JS engines
- Custom Frida instrumentation of Mach/IPC dispatch

---

### 9. Build Environments and Debugging

**V8 / Chromium**:
```bash
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH=$PATH:$(pwd)/depot_tools
fetch v8 && cd v8 && gclient sync
./build/install-build-deps.sh
tools/dev/gm.py x64.release  # or x64.debug
```

**Key d8 flags**: `--allow-natives-syntax`, `--print-opt-code`, `--print-bytecode`, `--trace-turbo`, `--trace-opt`, `--trace-deopt`, `--maglev`, `--expose-gc`

**Turbolizer**:
```bash
cd v8/tools/turbolizer
npm i && npm run-script build
python -m http.server 8000
```

**WebKit / JSC**:
```bash
git clone git://git.webkit.org/WebKit.git && cd WebKit
Tools/gtk/install-dependencies
Tools/Scripts/build-webkit --jsc-only --debug
```

**SpiderMonkey**:
```bash
git clone https://github.com/mozilla/gecko-dev.git && cd gecko-dev
cd js/src && autoconf2.13
mkdir build_DBG.OBJ && cd build_DBG.OBJ
../configure --enable-debug --disable-optimize
make -j$(nproc)
```

**Essential Debugging Tools**:
- **GEF / pwndbg**: GDB plugins for exploit development
- **rr**: Record-and-replay debugging (Mozilla), invaluable for race conditions
- **Frida**: Dynamic instrumentation (JS injection into any process) — https://github.com/frida/frida
- **Turbolizer**: V8 Sea of Nodes visualization
- **IonGraph**: SpiderMonkey JIT visualization
- **Compiler Explorer** (godbolt.org): Quick JIT code inspection
- **shadow**: jemalloc heap exploitation framework (used by Firefox)

**Exploit Development Libraries**:
- **pwnjs** (theori-io): JS library for browser exploitation (Int64, utility functions)
- **int64.js** (saelo): 64-bit integer operations in JS
- **WasmModuleBuilder**: Programmatic WASM module construction in d8

---

### 10. Browser Exploitation Tools & Frameworks

#### BeEF — Browser Exploitation Framework
- **Repo**: https://github.com/beefproject/beef
- **Website**: https://beefproject.com
- Hooks one or more web browsers and uses them as beachheads for launching directed command modules
- Extensive library of browser-based command modules
- Client-side attack vectors from within browser context
- Kali package: `beef-xss`

#### XSS Frameworks & Tools
- **OWASP Xenotix XSS Exploit Framework**: https://github.com/ajinabraham/OWASP-Xenotix-XSS-Exploit-Framework
- **BruteXSS**: Automated XSS vulnerability finder
- **XSStrike**: Advanced XSS detection suite — https://github.com/s0md3v/XSStrike
- **xsser**: Automated XSS exploitation — https://github.com/epsylon/xsser
- **XSS-Payloads**: Cross-site scripting payloads — https://github.com/payloadbox/xss-payload-list

#### Browser Automation for Exploitation
- **Frida**: https://github.com/frida/frida — Dynamic instrumentation toolkit
- **Objection**: https://github.com/sensepost/objection — Runtime mobile exploration powered by Frida
- **Playwright / Puppeteer**: Browser automation for exploit development
- **Selenium**: WebDriver-based browser automation

#### Browser Exploitation References & Repos
- **browser-pwn**: https://github.com/m1ghtym0/browser-pwn — Architecture/build guides per engine, CTF writeups
- **awesome-browser-exploit**: https://github.com/Escapingbug/awesome-browser-exploit — Curated tutorials per engine
- **browser-exploitation**: https://github.com/drtychai/browser-exploitation — N-day exploits, CVEs, fuzzing tools
- **js-vuln-db**: https://github.com/tunz/js-vuln-db — JavaScript engine CVEs with PoCs
- **chrome-sbx-db**: https://github.com/allpaca/chrome-sbx-db — Chrome sandbox escape database

#### Foundational Papers and Articles
- Phrack: "Attacking JavaScript Engines" (saelo) — http://www.phrack.org/papers/attacking_javascript_engines.html
- Phrack: "Exploiting Logic Bugs in JavaScript JIT Engines" (saelo)
- RET2 Pwn2Own 2018 series: https://blog.ret2.io/2018/06/05/pwn2own-2018-exploit-development/
- "Introduction to TurboFan" (doar-e): https://doar-e.github.io/blog/2019/01/28/introduction-to-turbofan/
- "JITSploitation I/II/III" (Project Zero): JSC exploitation techniques
- "An Introduction to Chrome Exploitation - Maglev Edition" (matteomalvica)
- "Cleanly Escaping the Chrome Sandbox" (Theori): Mojo UAF escape
- "Escaping the Chrome Sandbox with RIDL" (Project Zero): Hardware side-channel escape
- "Windows Within Windows" (Exodus): Win32k sandbox escape
- "Fooling the Sandbox: A Chrome-atic Escape" (STAR Labs)

---

## SOCIAL ENGINEERING

### 1. Phishing Frameworks

#### GoPhish
- **Repo**: https://github.com/gophish/gophish
- Open-source phishing toolkit for businesses and penetration testers
- Self-hosted phishing campaigns with tracking, email templates, landing pages
- Import/export capability for campaigns and users
- REST API for automation

#### EvilGinx
- **Repo**: https://github.com/kgretzky/evilginx2
- Standalone man-in-the-middle attack framework for phishing
- Bypasses 2-factor authentication by capturing session cookies
- Phishlets for major services (Office 365, Google, etc.)
- Reverse proxy architecture

#### Modlishka
- **Repo**: https://github.com/drk1wi/Modlishka
- Reverse proxy phishing tool, precursor to EvilGinx
- Automatic SSL certificate generation
- Credential harvesting with transparent reverse proxy

#### SocialFish
- **Repo**: https://github.com/UndeadSec/SocialFish
- Phishing tool and information collector
- v3.0: Cloning modern login pages, capturing cookies, intercepting 2FA codes
- Live operator panel for real-time monitoring
- Mobile remote control available: https://github.com/UndeadSec/SocialFishMobile

#### SET (Social Engineering Toolkit)
- **Repo**: https://github.com/trustedsec/social-engineer-toolkit
- By TrustedSec / Dave Kennedy
- Open-source Python-driven tool for social engineering penetration tests
- Attack vectors: spear-phishing, website attack vectors, infectious media generator, mass mailer
- Over 2 million downloads, standard for SE testing

#### King Phisher
- **Repo**: https://github.com/securestate/king-phisher (archived), https://github.com/CrimsonForge-io/king-phisher
- Phishing campaign toolkit for testing and promoting user awareness
- Flexible architecture with client/server model
- Templates: https://github.com/securestate/king-phisher-templates

#### SpoofWeb
- **Repo**: https://github.com/5icorgi/SpoofWeb
- Deploy phishing websites easily

---

### 2. Spearphishing & Email Attack Vectors

#### Email Spoofing
- **SPF/DKIM/DMARC bypass techniques**: Misconfigured SPF records, subdomain spoofing
- **swaks**: Swiss Army Knife for SMTP — test email delivery, spoofing
- **SendEmail**: Command-line SMTP client for sending spoofed emails

#### Phishing Templates & Content
- **Phishing templates for GoPhish**: https://github.com/topics/gophish
- **HTML smuggling**: Embed base64 payload in HTML that auto-downloads and runs
- **Macro-based delivery**: Office docs with VBA dropping payloads
- **DDE attacks**: `{ DDEAUTO c:\\windows\\system32\\cmd.exe "/k calc.exe" }` in Word fields

#### Spearphishing Infrastructure
- **Evilginx-Phishing-Infra-Setup**: https://github.com/An0nUD4Y/Evilginx-Phishing-Infra-Setup
  - Guide for securing Evilginx and Gophish infrastructure
  - Domain purchase and categorization techniques
  - Email deliverability optimization

---

### 3. Credential Harvesting & MFA Bypass

#### Adversary-in-The-Middle (AiTM)
- **EvilGinx** and **Modlishka**: Transparent reverse proxy captures session cookies
- Bypasses 2FA/MFA by stealing authenticated session tokens
- **muraena**: Reverse proxy for phishing and MFA bypass
- **Necrobrowser**: Stolen cookie replay and session hijacking

#### Credential Harvesting Pages
- Cloned login portals for Office 365, Google Workspace, VPN portals, Citrix, etc.
- Real-time credential validation via API integration
- Credential capture with browser hooks (BeEF)

#### Password/Token Capture Tools
- **LaZagne**: https://github.com/AlessandroZ/LaZagne — Multi-application password recovery
- **HackBrowserData**: Browser credential extraction (Chrome, Firefox, Edge)
- **mimikatz**: Windows credential dumping
- **Responder**: LLMNR/NBT-NS/mDNS poisoning for NetNTLMv2 capture

---

### 4. OSINT Tools for Target Profiling

#### Email Discovery
- **theHarvester**: https://github.com/laramies/theHarvester — Email, subdomain, and name harvesting
- **Hunter.io**: https://hunter.io — Find email addresses by domain
- **Snov.io**: https://app.snov.io — Email finder and verifier
- **Phonebook.cz**: https://phonebook.cz — Subdomain and URL discovery
- **Skymem**: https://www.skymem.info — Email address search
- **email-format.com**: https://www.email-format.com — Corporate email format discovery
- **emailrep.io**: https://emailrep.io — Email reputation and account discovery

#### Leaked Credentials
- **Have I Been Pwned**: https://haveibeenpwned.com — Breach database search
- **BreachDirectory**: https://breachdirectory.org — Password breach search
- **DeHashed**: Breach data search engine
- **LeakCheck**: Credential leak databases

#### Social Media Profiling
- **LinkedIn**: Map org chart, find sysadmins, developers, cloud engineers
- **Job postings**: Tech stack, versions, internal tool names
- **GitHub Dorking**: Search for `target.com` secrets, API keys, tokens
  - https://github.com/obheda12/GitDorker
  - https://github.com/damit5/gitdorks_go
- **Wayback Machine**: https://web.archive.org — Historical snapshots, forgotten endpoints
- **Google Dorking**: https://www.exploit-db.com/google-hacking-database

#### Domain & Infrastructure Recon
- **WHOIS**: `whois target.com` — registrant, email, nameservers
- **crt.sh**: Certificate transparency logs
- **dnsdumpster.com**: DNS recon
- **Shodan/Fofa/ZoomEye/Censys**: Internet-wide asset discovery

#### OSINT Frameworks & Resources
- **OSINT Framework**: https://osintframework.com/
- **OSINT Resource List**: https://start.me/p/rx6Qj8/nixintel-s-osint-resource-list
- **OSINT Handbook**: https://i-intelligence.eu/uploads/public-documents/OSINT_Handbook_2020.pdf

---

### 5. SMS & Voice Phishing (Vishing)

#### SMS Online Services
- https://sms-activate.io — 180+ countries
- https://www.supercloudsms.com/en/
- https://getfreesmsnumber.com/
- https://receive-sms.cc/

#### Temporary Email Services
- http://24mail.chacuo.net/
- https://www.guerrillamail.com/
- https://rootsh.com/

---

## WIRELESS / RF

### 1. Wi-Fi (802.11)

#### Aircrack-ng Suite
- **Repo**: https://github.com/aircrack-ng/aircrack-ng
- Complete suite of tools to assess WiFi network security
- Tools: aircrack-ng, airmon-ng, airodump-ng, aireplay-ng, airdecap-ng
- WEP/WPA/WPA2 cracking, packet injection, monitor mode

#### Bettercap
- **Repo**: https://github.com/bettercap/bettercap
- Swiss army knife for WiFi, BLE, Ethernet, and HID attacks
- Real-time network monitoring, MITM, credential harvesting
- HTTP/HTTPS proxy, DNS spoofing, transparent proxying
- Built-in modules for WiFi deauth, PMKID capture, client-less WPA handshake capture

#### Kismet
- **Repo**: https://github.com/kismetwireless/kismet
- Wireless network detector, sniffer, and IDS
- Supports WiFi, Bluetooth, SDR, and other wireless protocols
- Web UI for remote monitoring

#### Reaver / WPS Attacks
- **Reaver**: WPS brute force attack tool — https://github.com/t6x/reaver-wps-fork-t6x
- **Bully**: WPS brute force attack tool (newer) — https://github.com/aanarchyy/bully
- **Pixiewps**: Offline WPS PIN recovery — https://github.com/wiire-a/pixiewps

#### Wifite
- **Repo**: https://github.com/derv82/wifite2
- Automated wireless auditor
- Targets WEP, WPA, WPS encrypted networks
- Automates aircrack-ng, reaver, pixiewps

#### Additional Wi-Fi Tools
- **airgeddon**: https://github.com/v1s1t0r1sh3r3/airgeddon — Multi-use bash script for wireless auditing
- **WiFi-Pumpkin**: https://github.com/P0cL4bs/wifipumpkin3 — Rogue AP framework
- **Hostapd-mana**: Modified hostapd for rogue AP/EAP attacks
- **EAPHammer**: Targeted evil twin attacks against WPA2-Enterprise networks
- **hcxtools**: https://github.com/ZerBea/hcxtools — WPA hash conversion tools
- **hcxdumptool**: https://github.com/ZerBea/hcxdumptool — Small tool for packet capture
- **WiFi Pineapple** (Hak5): Commercial penetration testing platform — https://github.com/hak5
- **wifi-arsenal**: https://github.com/0x90/wifi-arsenal — Curated WiFi tool collection

---

### 2. Bluetooth (BR/EDR + BLE)

#### Core Bluetooth Tools
- **BlueZ**: https://github.com/bluez/bluez — Official Linux Bluetooth protocol stack
  - Tools: `hcitool`, `gatttool`, `bluetoothctl`, `hciconfig`
- **Bettercap BLE**: https://github.com/bettercap/bettercap — BLE scanning, enumeration, GATT service discovery
- **btlejack**: https://github.com/virtualabs/btlejack — BLE Swiss-army knife; sniff, jam, hijack BLE
  - Uses BBC Micro:Bit devices for hardware BLE capture
- **GATTacker**: https://github.com/securing/gattacker — BLE MITM and security assessment toolkit
  - Node.js package for BLE security assessment
  - Central/Peripheral impersonation
- **BTLEJuice**: BLE MITM framework

#### Bluetooth Security Resources
- **Awesome Bluetooth Security**: https://github.com/engn33r/awesome-bluetooth-security
- **BlueToolkit**: Bluetooth Classic vulnerability testing framework
- **InternalBlue**: Bluetooth experimentation framework for Broadcom/Cypress chips

#### Additional Bluetooth Tools
- **btproxy**: MITM proxy for Bluetooth
- **Bluesniff**: Bluetooth device discovery
- **carwhisperer**: Bluetooth headset injection
- **btscanner**: Bluetooth device scanner
- **crackle**: BLE pairing cracking
- **Ubertooth One**: Open-source Bluetooth sniffer hardware — https://github.com/greatscottgadgets/ubertooth

---

### 3. Software Defined Radio (SDR)

#### SDR Hardware
- **HackRF One**: https://github.com/greatscottgadgets/hackrf — 1 MHz to 6 GHz, half-duplex
- **RTL-SDR**: https://github.com/osmocom/rtl-sdr — DVB-T dongle based on RTL2832U, very cheap
- **LimeSDR**: Full-duplex SDR platform
- **USRP** (Ettus): Professional-grade SDR platform
- **BladeRF**: 2x2 MIMO SDR

#### SDR Software
- **GNU Radio**: https://github.com/gnuradio/gnuradio — Framework for SDR and signal processing
- **Universal Radio Hacker (URH)**: https://github.com/jopohl/urh — Wireless protocol investigation suite
  - Native support for HackRF, RTL-SDR, LimeSDR
  - Automatic modulation detection, demodulation, protocol analysis
  - Next-gen fork: https://github.com/PentHertz/urh-ng
- **GQRX**: https://github.com/gqrx-sdr/gqrx — SDR receiver powered by GNU Radio
- **SDR++**: https://github.com/AlexandreRouma/SDRPlusPlus — Cross-platform SDR software
- **CubicSDR**: Cross-platform SDR application
- **inspectrum**: Offline signal analyzer — https://github.com/miek/inspectrum

#### SDR Security Tools
- **RFSec-ToolKit**: https://github.com/cn0xroot/RFSec-ToolKit — Collection of RF security tools
- **gr-gsm**: GNU Radio GSM receiver
- **IMSI-catcher**: https://github.com/Oros42/IMSI-catcher — IMSI catcher for SDR
- **YateBTS**: GSM base station software
- **OpenBTS**: Open-source GSM base station
- **SigDigger**: Signal analysis and digital demodulation — https://github.com/BatchDrake/SigDigger

---

### 4. RFID / NFC

#### Hardware Tools
- **Proxmark3**: https://github.com/RfidResearchGroup/proxmark3 — The definitive RFID/NFC research tool
  - LF (125 kHz) and HF (13.56 MHz) support
  - Firmware: https://github.com/RfidResearchGroup/proxmark3
  - Community: https://github.com/RfidResearchGroup
- **Chameleon Ultra**: https://github.com/RfidResearchGroup/ChameleonUltra — Versatile contactless smartcard emulator
- **Chameleon Mini**: https://github.com/iceman1001/ChameleonMini-rebooted — NFC card emulator
- **Flipper Zero**: https://github.com/flipperdevices/flipperzero-firmware — Multi-tool for pentesters
  - RFID/NFC, Sub-GHz, iButton, GPIO, IR, BadUSB
  - Firmware forks: Momentum (https://github.com/Next-Flip/Momentum-Firmware), RogueMaster (https://github.com/RogueMaster/flipperzero-firmware-wPlugins)
  - Awesome list: https://github.com/djsime1/awesome-flipperzero
- **ACR122U**: USB NFC reader/writer (libnfc compatible)
- **PN532**: NFC/RFID breakout board

#### Software Tools
- **libnfc**: https://github.com/nfc-tools/libnfc — Low-level NFC SDK
- **mfoc**: https://github.com/nfc-tools/mfoc — MIFARE Classic offline cracker
- **mfcuk**: MIFARE Classic Universal toolKit
- **MIFARE Classic Tool** (Android): NFC card reading/writing/analysis
- **RFIDtools**: https://github.com/RfidResearchGroup/RFIDtools — Android app for Proxmark3 RDV4 + blueshark
- **RFIDler**: Open-source LF RFID reader/writer/emulator

---

### 5. Zigbee (802.15.4)

#### Tools & Frameworks
- **KillerBee**: https://github.com/riverloopsec/killerbee — IEEE 802.15.4/ZigBee Security Research Toolkit
  - Sniffing, injection, replay, network discovery
  - Supports RZUSBStick, MoteIV Tmote, TelosB
- **Z-Fuzzer**: https://github.com/zigbeeprotocol/Z-Fuzzer — Device-agnostic Zigbee protocol fuzzing
- **Zigbee2MQTT**: https://github.com/Koenkk/zigbee2mqtt — Zigbee to MQTT bridge
  - Control Zigbee devices without vendor bridge
  - Extensive device compatibility
- **Z3sec**: Zigbee security penetration testing framework
- **scapy-com**: Zigbee layer for Scapy
- **Api-Mote**: https://github.com/riverloopsec/apimote — Hardware for 802.15.4 security research

#### Hardware
- **RZUSBStick**: Atmel AVR RZUSBstick for 802.15.4
- **CC2531**: Texas Instruments Zigbee USB dongle
- **nRF52840**: Multi-protocol BLE/Zigbee/Thread dongle
- **XBee**: Digi XBee modules with API mode

---

### 6. Additional Wireless/RF Tools

- **FreqShow**: RTL-SDR frequency spectrum visualizer
- **rtl_433**: https://github.com/merbanan/rtl_433 — Decode 433 MHz devices (weather stations, sensors)
- **dump1090**: https://github.com/antirez/dump1090 — ADS-B/Mode S decoder for RTL-SDR
- **Wireshark**: Protocol analysis with wireless dissectors
- **Scapy**: Packet manipulation with wireless layers

---

## PHYSICAL SECURITY

### 1. Lock Picking & Physical Entry

#### Learning & Reference
- **awesome-lockpicking**: https://github.com/fabacab/awesome-lockpicking — Guides, tools, resources
- **awesome-physec**: https://github.com/LiveGray/awesome-physec — Physical security resources
- **Lock Picking Lawyer** (YouTube): Technique demonstrations
- **Deviant Ollam**: "I'll Let Myself In" — Physical penetration testing talks

#### Techniques
- **Lock picking**: Raking, single pin picking (SPP), bumping
- **Bump keys**: Universally cut keys for pin tumbler locks
- **Shimming**: Padlock bypass with thin metal strips
- **Under-door tools**: Reach under door to actuate lever handles
- **Latch slipping**: Card/bypass tool for spring latches
- **Impressioning**: Create working key from blank

---

### 2. HID Injection / BadUSB

#### Hak5 Tools
- **USB Rubber Ducky**: Keystroke injection tool disguised as USB flash drive
  - Payloads: https://github.com/hak5/usbrubberducky-payloads
  - DuckyScript language for automated keystroke attacks
- **Bash Bunny**: USB attack platform (Linux-based)
  - Payloads: https://github.com/hak5/bashbunny-payloads
  - Keyboard emulation, USB mass storage, Ethernet emulation, BLE
  - Multiple attack modes (HID, storage, serial, ethernet)
- **OMG Cable**: Malicious USB cable with embedded WiFi and keystroke injection
  - Payloads: https://github.com/hak5/omg-payloads
- **Shark Jack**: Portable network attack tool
  - Payloads: https://github.com/hak5/sharkjack-payloads
- **Key Croc**: USB keylogger with remote access
  - Payloads: https://github.com/hak5/keycroc-payloads

#### Open-Source BadUSB Alternatives
- **Flipper Zero BadUSB**: https://github.com/flipperdevices/flipperzero-firmware
  - DuckyScript-compatible payload execution
  - Community payloads: https://github.com/I-Am-Jakoby/Flipper-Zero-BadUSB
- **P4wnP1 / P4wnP1 A.L.O.A.**: Raspberry Pi Zero W USB attack platform
  - https://github.com/RoganDawes/P4wnP1_aloa
  - HID, mass storage, ethernet, serial over USB
- **PiKVM**: Raspberry Pi based KVM over IP for physical access
- **WHID Injector**: Open-source WiFi HID injector (ESP8266-based)
- **USB-Rubber-Ducky** (pico): Raspberry Pi Pico as Rubber Ducky
  - https://github.com/dbisu/pico-ducky

#### Custom Firmware Keyboards
- **QMK Firmware**: https://github.com/qmk/qmk_firmware — Custom keyboard firmware with macro injection
- **TMK Keyboard Firmware**: Custom keyboard firmware with programmable macros

---

### 3. Network Implants & Physical Access

#### Hak5 Network Tools
- **LAN Turtle**: Covert network implant (USB Ethernet adapter form factor)
  - Modules: https://github.com/hak5/lanturtle-modules
  - Remote access, MITM, packet capture, DNS spoofing
  - Appears as standard USB Ethernet adapter
- **Packet Squirrel**: Ethernet MITM attack platform
  - Payloads: https://github.com/hak5/packetsquirrel-payloads
  - Mark II: DuckyScript support, 2x Gigabit Ethernet
  - Packet capture, VPN tunnel, DNS spoofing, network pivot
- **WiFi Pineapple**: Rogue access point and WiFi penetration testing platform
  - Modules: https://github.com/hak5/pineapple-modules
  - MITM, captive portals, credential harvesting, client tracking
- **Plunder Bug**: LAN tap for passive packet capture
- **Signal Owl**: Portable wireless signal manipulation tool

#### USB Armory
- **USB Armory** (Inverse Path / WithSecure): USB form factor Linux computer
  - https://github.com/usbarmory
  - Full Debian Linux on a USB stick
  - Secure boot, hardware AES, HID emulation

---

### 4. Keylogging Hardware

- **Key Croc** (Hak5): USB keylogger with keystroke injection, remote access
  - Payloads: https://github.com/hak5/keycroc-payloads
- **USB Keylogger** (Keelog): Hardware USB/PS2 keyloggers
- **AirKey**: Bluetooth keylogger
- **KeyGrabber**: WiFi-enabled hardware keylogger

---

### 5. USB Killer & Destructive Devices

- **USB Killer**: Commercial device; discharges high voltage through USB data lines
  - *Not open-source*; destroys hardware by overloading USB bus capacitors
- **USBKill** (software): https://github.com/hephaest0s/usbkill — Anti-forensic kill switch
  - Wipes RAM / shuts down when USB changes detected
- **BusKill**: https://github.com/BusKill/buskill-app — Magnetic breakaway USB cable kill cord
- **Thunderbolt DMA Attacks**: Physical memory access via Thunderbolt
  - **Thunderclap**: https://github.com/thunderclap-io/thunderclap — Research platform for Thunderbolt DMA
  - **PCILeech**: https://github.com/ufrisk/pcileech — DMA attack tool for PCIe hardware

---

### 6. BIOS / UEFI Physical Attacks

- **Cold boot attack**: Freeze RAM chips, transfer to attacker machine, dump memory
- **JTAG / UART debug**: Physical debugging interfaces on motherboard
- **SPI flash dumping**: Direct read/write of BIOS/UEFI firmware chips
- **Evil Maid attack**: Boot from external media, modify OS to inject backdoor
- **BootGuard bypass**: Intel BootGuard key leaks, manufacturing mode bypass
- **TPM sniffing**: I2C/SPI bus sniffing between CPU and TPM chip
- **PCILeech**: https://github.com/ufrisk/pcileech — Direct Memory Access (DMA) attacks via PCIe
- **Chipsec**: https://github.com/chipsec/chipsec — Platform security assessment framework

---

### 7. Physical Security Assessment Tools

- **ZAP / High Gain Antennas**: Long-range RFID/NFC reading
- **IR blasters / learners**: Clone IR remote controls
- **RF cloners**: Clone fixed-code RF remote controls (garage doors, gates)
- **Magnetic stripe reader/writer**: MSR605/606 for magstripe cards
- **Lock decoder**: Determine pin depths from keyway
- **Lishi tools**: Decoder and pick in one tool
- **Borescope / Endoscope**: Inspect internal mechanisms
- **UV light / Alternate light source**: Reveal hidden markings, cleaned surfaces
- **Seal picks / tamper-evident bypass**: Bypass tamper-evident seals and packaging

---

### 8. Surveillance & Counter-Surveillance

- **Hidden camera detection**: RF detectors, IR scanners
- **Bug sweepers**: Non-linear junction detectors (NLJD)
- **Thermal imaging**: FLIR cameras for heat signature detection
- **Audio surveillance**: Laser microphones, contact microphones, parabolic mics
- **GPS trackers**: Vehicle/personnel tracking devices
- **TSCM (Technical Surveillance Counter-Measures)**: Professional bug sweeping

---

## QUICK REFERENCE: ALL GITHUB REPOS

### Browser Exploitation
| Tool/Resource | Repo |
|--------------|------|
| BeEF | https://github.com/beefproject/beef |
| Frida | https://github.com/frida/frida |
| Objection | https://github.com/sensepost/objection |
| Fuzzilli | https://github.com/googleprojectzero/fuzzilli |
| Domato | https://github.com/googleprojectzero/domato |
| browser-pwn | https://github.com/m1ghtym0/browser-pwn |
| awesome-browser-exploit | https://github.com/Escapingbug/awesome-browser-exploit |
| browser-exploitation | https://github.com/drtychai/browser-exploitation |
| js-vuln-db | https://github.com/tunz/js-vuln-db |
| chrome-sbx-db | https://github.com/allpaca/chrome-sbx-db |

### Social Engineering
| Tool/Resource | Repo |
|--------------|------|
| GoPhish | https://github.com/gophish/gophish |
| EvilGinx2 | https://github.com/kgretzky/evilginx2 |
| Modlishka | https://github.com/drk1wi/Modlishka |
| SocialFish | https://github.com/UndeadSec/SocialFish |
| SET | https://github.com/trustedsec/social-engineer-toolkit |
| King Phisher | https://github.com/securestate/king-phisher |
| SpoofWeb | https://github.com/5icorgi/SpoofWeb |
| theHarvester | https://github.com/laramies/theHarvester |
| GitDorker | https://github.com/obheda12/GitDorker |
| Evilginx Infra Setup | https://github.com/An0nUD4Y/Evilginx-Phishing-Infra-Setup |

### Wi-Fi
| Tool | Repo |
|-----|------|
| Aircrack-ng | https://github.com/aircrack-ng/aircrack-ng |
| Bettercap | https://github.com/bettercap/bettercap |
| Kismet | https://github.com/kismetwireless/kismet |
| Wifite2 | https://github.com/derv82/wifite2 |
| Reaver (fork) | https://github.com/t6x/reaver-wps-fork-t6x |
| Pixiewps | https://github.com/wiire-a/pixiewps |
| airgeddon | https://github.com/v1s1t0r1sh3r3/airgeddon |
| WiFi-Pumpkin | https://github.com/P0cL4bs/wifipumpkin3 |
| hcxtools | https://github.com/ZerBea/hcxtools |
| hcxdumptool | https://github.com/ZerBea/hcxdumptool |
| wifi-arsenal | https://github.com/0x90/wifi-arsenal |

### Bluetooth
| Tool | Repo |
|-----|------|
| BlueZ | https://github.com/bluez/bluez |
| btlejack | https://github.com/virtualabs/btlejack |
| GATTacker | https://github.com/securing/gattacker |
| Ubertooth | https://github.com/greatscottgadgets/ubertooth |
| Awesome Bluetooth Sec | https://github.com/engn33r/awesome-bluetooth-security |

### SDR
| Tool | Repo |
|-----|------|
| HackRF | https://github.com/greatscottgadgets/hackrf |
| RTL-SDR | https://github.com/osmocom/rtl-sdr |
| GNU Radio | https://github.com/gnuradio/gnuradio |
| Universal Radio Hacker | https://github.com/jopohl/urh |
| URH Next Gen | https://github.com/PentHertz/urh-ng |
| GQRX | https://github.com/gqrx-sdr/gqrx |
| SDR++ | https://github.com/AlexandreRouma/SDRPlusPlus |
| inspectrum | https://github.com/miek/inspectrum |
| SigDigger | https://github.com/BatchDrake/SigDigger |
| RFSec-ToolKit | https://github.com/cn0xroot/RFSec-ToolKit |
| rtl_433 | https://github.com/merbanan/rtl_433 |
| dump1090 | https://github.com/antirez/dump1090 |

### RFID / NFC
| Tool | Repo |
|-----|------|
| Proxmark3 | https://github.com/RfidResearchGroup/proxmark3 |
| Chameleon Ultra | https://github.com/RfidResearchGroup/ChameleonUltra |
| Chameleon Mini | https://github.com/iceman1001/ChameleonMini-rebooted |
| Flipper Zero | https://github.com/flipperdevices/flipperzero-firmware |
| Awesome FlipperZero | https://github.com/djsime1/awesome-flipperzero |
| libnfc | https://github.com/nfc-tools/libnfc |
| mfoc | https://github.com/nfc-tools/mfoc |
| RFIDtools | https://github.com/RfidResearchGroup/RFIDtools |

### Zigbee
| Tool | Repo |
|-----|------|
| KillerBee | https://github.com/riverloopsec/killerbee |
| Z-Fuzzer | https://github.com/zigbeeprotocol/Z-Fuzzer |
| Zigbee2MQTT | https://github.com/Koenkk/zigbee2mqtt |

### Physical Security
| Tool | Repo |
|-----|------|
| USB Rubber Ducky Payloads | https://github.com/hak5/usbrubberducky-payloads |
| Bash Bunny Payloads | https://github.com/hak5/bashbunny-payloads |
| LAN Turtle Modules | https://github.com/hak5/lanturtle-modules |
| Packet Squirrel Payloads | https://github.com/hak5/packetsquirrel-payloads |
| Shark Jack Payloads | https://github.com/hak5/sharkjack-payloads |
| Key Croc Payloads | https://github.com/hak5/keycroc-payloads |
| OMG Payloads | https://github.com/hak5/omg-payloads |
| Flipper Zero BadUSB | https://github.com/I-Am-Jakoby/Flipper-Zero-BadUSB |
| P4wnP1 A.L.O.A. | https://github.com/RoganDawes/P4wnP1_aloa |
| pico-ducky | https://github.com/dbisu/pico-ducky |
| QMK Firmware | https://github.com/qmk/qmk_firmware |
| USBKill | https://github.com/hephaest0s/usbkill |
| BusKill | https://github.com/BusKill/buskill-app |
| Thunderclap | https://github.com/thunderclap-io/thunderclap |
| PCILeech | https://github.com/ufrisk/pcileech |
| Chipsec | https://github.com/chipsec/chipsec |
| awesome-lockpicking | https://github.com/fabacab/awesome-lockpicking |
| awesome-physec | https://github.com/LiveGray/awesome-physec |

---

### 9. OSINT Resources

| Resource | URL |
|---------|-----|
| OSINT Framework | https://osintframework.com/ |
| OSINT Resource List | https://start.me/p/rx6Qj8/nixintel-s-osint-resource-list |
| OSINT Handbook | https://i-intelligence.eu/uploads/public-documents/OSINT_Handbook_2020.pdf |
| Have I Been Pwned | https://haveibeenpwned.com/ |
| BreachDirectory | https://breachdirectory.org/ |
| theHarvester | https://github.com/laramies/theHarvester |
| Hunter.io | https://hunter.io |
| Phonebook.cz | https://phonebook.cz |
| Snov.io | https://app.snov.io |
| Hunter | https://hunter.io |
| Google Hacking DB | https://www.exploit-db.com/google-hacking-database |
| GitDorker | https://github.com/obheda12/GitDorker |
| Shodan | https://www.shodan.io/ |
| Fofa | https://fofa.info/ |
| ZoomEye | https://www.zoomeye.org/ |
| Censys | https://search.censys.io/ |
| Hunter (Qianxin) | https://hunter.qianxin.com/ |
| crt.sh | https://crt.sh |
| dnsdumpster | https://dnsdumpster.com |
| Wayback Machine | https://web.archive.org/ |
| WHOIS (domain tools) | https://who.is/ |

---

*"The browser is the ultimate prize. It runs untrusted code from anywhere on the internet. If you can control what happens after that code runs, you control the user."*
*"Social engineering bypasses all technical controls. The human is always the weakest link."*
*"If you can't break in through the network, walk in through the front door."*
