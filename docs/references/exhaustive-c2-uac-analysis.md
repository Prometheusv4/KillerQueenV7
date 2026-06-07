# Exhaustive C2, UAC Bypass & Post-Exploitation Technique Analysis

## REPOSITORY 1: SLIVER (BishopFox C2 Framework)

**Total source files examined: ~565 Go files** (implant/sliver: 237, server: 274, util: 54)

### 1. C2 PROTOCOLS

| Protocol | File(s) | Key Details |
|----------|---------|-------------|
| **mTLS** | `implant/sliver/transports/mtls/mtls.go` (291 lines) | Mutual TLS with custom CA verification. Uses Ed25519 envelope signing. Length-prefixed framing with raw signature prefix. `RootOnlyVerifyCertificate()` skips hostname validation, only verifies CA chain. |
| **WireGuard** | `implant/sliver/transports/wireguard/wireguard.go` (406 lines) | Userspace WireGuard via `golang.zx2c4.com/wireguard`. In-band netstack TUN. Key exchange: initial implant keypair -> connect to key exchange listener -> receive session-specific dynamic keypair. Ed25519 envelope signing. Supports `CONNECT`, `BIND`, `KEY_EXCHANGE` flows. |
| **HTTP/HTTPS** | `implant/sliver/transports/httpclient/httpclient.go` (698 lines) | Poll-based HTTP(S) with session init via Age-encrypted key exchange. Supports nonce query args, OTP query args, custom headers, custom path segments (C2 profiles). Driver abstraction (Go default http, WinInet on Windows). |
| **DNS** | `implant/sliver/transports/dnsclient/dnsclient.go` (1051 lines) | DNS-over-TXT/AAAA with Base32 encoding. Subdomain encoding: [data].[ns].[parent]. Max ~60 bytes payload per query. Multiple resolvers with per-resolver worker pools. Session init via random session ID + Age key exchange. Parallel send/recv workers. |
| **Pivots** | `implant/sliver/pivots/` | TCP pivot (`tcp.go`), Named Pipe pivot (`named-pipe.go`, `named-pipe_windows.go`). Duplex pivot connections through implant chains. |
| **Connection Strategy** | `implant/sliver/transports/transports.go` | `random`, `randomDomain`, `sequential` URL selection strategies. Dynamic C2 URI reconfiguration support. Reconnect interval with jitter. |

### 2. IMPLANT GENERATION

| Feature | File(s) | Key Details |
|---------|---------|-------------|
| **Template-based code generation** | `server/generate/implants.go`, `binaries.go`, `profiles.go` | Go template system. Implant config (C2 URLs, protocols, evasion, debug) baked at compile time via `{{.Config.X}}` placeholders. |
| **Output Formats** | `server/generate/binaries.go` | `EXECUTABLE`, `SHARED_LIB`, `SHELLCODE`, `SERVICE` formats. Cross-compilation via Go toolchain. |
| **Garble Obfuscation** | `util/assets/garble.go` | Optional garble-based Go obfuscation during build (identifier renaming, string obfuscation). |
| **Donut Integration** | `server/generate/donut.go` (159 lines) | PE-to-shellcode conversion via `wasm-donut`. Supports entropy levels, compression, AMSI bypass modes, exit options, thread creation. `addStackCheck()` prepends stack alignment fix for x64. |
| **SRDI (Shellcode Reflective DLL Injection)** | `server/generate/srdi.go`, `srdi-shellcode.go` | Port of Leo Loobeek's SRDI. Converts DLLs into position-independent shellcode with reflective loader. |
| **Shellcode Encoders** | `server/encoders/shellcode/` | XOR encoders for amd64 and arm64 with dynamic key generation. Shikata Ga Nai (SGN) encoder via `sgn/` package. |
| **Canaries** | `server/generate/canaries.go` | Token canary system for detecting implant compromise/analysis. |
| **Implant Profiles** | `server/generate/profiles.go` | Named configurations for repeatable builds. |

### 3. PROCESS INJECTION TECHNIQUES

| Technique | File(s) | Key Details |
|-----------|---------|-------------|
| **Classic Remote Thread Injection** | `implant/sliver/taskrunner/task_windows.go` (534 lines) | `VirtualAllocEx` + `WriteProcessMemory` + `CreateRemoteThread`. Supports RWX and RW->RX page transitions. |
| **NtCreateThreadEx** | `implant/sliver/syscalls/syscalls_windows.go` | Direct syscall via `NtCreateThreadEx` to bypass userland hooks. |
| **CreateThread (local)** | `implant/sliver/taskrunner/task_windows.go` | Local shellcode execution via `VirtualAlloc` + `CreateThread`. |
| **Threadless Injection via APC** | `implant/sliver/syscalls/syscalls_windows.go` | `QueueUserAPC` syscall exposed for APC injection. |
| **Process Hollowing / SpawnDll** | `implant/sliver/taskrunner/task_windows.go` | `SpawnDll()`: starts suspended process, injects DLL via reflective loader, resumes. |
| **Sideloading** | `implant/sliver/taskrunner/task_windows.go` | `Sideload()` wraps `SpawnDll()` with offset=0 for binary sideloading as shellcode. |
| **In-Process .NET Assembly Execution** | `implant/sliver/taskrunner/task_windows.go` | `ExecuteAssembly()` with `InProcExecuteAssembly()` for .NET assemblies. Optional AMSI + ETW patching. |
| **DLL Hijack for Automation** | `server/rpc/rpc-hijack.go` (401 lines) | Automated DLL hijacking: downloads reference DLL from target, builds proxy DLL via implant profile, clones export table with forwarded exports, uploads back. |
| **MiniDumpWriteDump** | `implant/sliver/syscalls/syscalls_windows.go` | Syscall for process memory dumping. |
| **PssCaptureSnapshot** | `implant/sliver/syscalls/syscalls_windows.go` | Process snapshot for live memory forensics. |

### 4. PRIVILEGE ESCALATION

| Technique | File(s) | Key Details |
|-----------|---------|-------------|
| **GetSystem via Remote Thread** | `implant/sliver/priv/priv_windows.go` (719 lines) | `GetSystem()`: enables SeDebugPrivilege, finds SYSTEM process by name, injects via `RemoteTask()` into SYSTEM process. |
| **Token Impersonation** | `implant/sliver/priv/priv_windows.go` | `impersonateProcess()`: opens target process, `OpenProcessToken`, `ImpersonateLoggedOnUser`, `DuplicateTokenEx`. |
| **MakeToken (LogonUser)** | `implant/sliver/priv/priv_windows.go` | `MakeToken()`: `LogonUserW` with `LOGON32_LOGON_NEW_CREDENTIALS` for network-only token creation. |
| **RunAs (CreateProcessWithLogonW)** | `implant/sliver/priv/priv_windows.go` | `RunAs()`: spawns process as different user with `CreateProcessWithLogonW`, supports `LOGON_NETCREDENTIALS_ONLY`. |
| **Token Manipulation** | `implant/sliver/priv/priv_windows.go` | `SePrivEnable()`, `RevertToSelf()`, `impersonateUser()`, `RunProcessAsUser()`. |
| **Integrity Level Detection** | `implant/sliver/priv/priv_windows.go` | `getProcessIntegrityLevel()` returns Untrusted/Low/Medium/High. |
| **Privilege Enumeration** | `implant/sliver/priv/priv_windows.go` | `GetPrivs()` enumerates all token privileges with names, descriptions, and enabled state. |

### 5. EVASION TECHNIQUES

| Technique | File(s) | Key Details |
|-----------|---------|-------------|
| **DLL Unhooking (RefreshPE)** | `implant/sliver/evasion/evasion_windows.go` | `RefreshPE()`: reloads .text section from disk into loaded DLL to erase EDR hooks. Uses `VirtualProtect` to make memory RWX, overwrites, restores permissions. |
| **AMSI Patching** | `implant/sliver/taskrunner/task_windows.go` | `patchAmsi()`: patches `AmsiScanBuffer`, `AmsiInitialize`, `AmsiScanString` with `RET (0xC3)` instruction. |
| **ETW Patching** | `implant/sliver/taskrunner/task_windows.go` | `patchEtw()`: patches `EtwEventWrite` in ntdll with `RET (0xC3)`. |
| **Parent PID Spoofing** | `implant/sliver/spoof/spoof_windows.go` | `SpoofParent()`: sets `ParentProcess` in `SysProcAttr` via `PROCESS_CREATE_PROCESS` access. |
| **Process Masquerading** | `implant/sliver/taskrunner/task_windows.go` | `startProcess()` optionally spoofs parent and sets token for child process. |
| **Hide Window** | `implant/sliver/taskrunner/task_windows.go` | `HideWindow: true` in `SysProcAttr`. `CREATE_SUSPENDED` flag support. |
| **Traffic Encoders** | `implant/sliver/encoders/` | Encoder chain: Base32, Base58, Base64, BaseX, Hex, English, Gzip, PNG images. Random encoder selection per message. |
| **Nonce-based URL randomization** | `implant/sliver/transports/httpclient/httpclient.go` | Nonce chars, length, mode configurable. Nonce embedded in URL path or query param. |
| **C2 Profile Headers/Params** | `implant/sliver/transports/httpclient/httpclient.go` | Custom HTTP headers with probability-based inclusion. Extra URL parameters with method-specific filtering. Random path segment generation with configurable min/max length and file extensions. |
| **WinInet HTTP Driver** | `implant/sliver/transports/httpclient/drivers/win/wininet/` | Windows-only: uses WinInet API instead of Go's net/http for stealth (uses IE proxy settings, less unusual).
| **Minisign Envelope Signing** | `implant/sliver/cryptography/` | All C2 messages signed with Ed25519 derived from peer key pair. Prevents message forgery/tampering. |
| **Timeout Delta Sync** | `implant/sliver/transports/httpclient/httpclient.go` | `TimeDelta` captures server-client time skew from Date header for timing normalization. |

### 6. BOF/COFF LOADING

| Feature | File(s) | Key Details |
|---------|---------|-------------|
| **BOF Package System** | `server/rpc/aitools/package_bof.go` | AI-driven BOF packaging. Packages TrustedSec COFF objects for execution. |
| **Package Tools** | `server/rpc/aitools/package_tools.go` | Build automation for COFF/BOF packages with dependency resolution. |
| **AI-Powered Execution** | `server/rpc/aitools/executor.go` | AI-driven tool selection and execution including BOFs. |

### 7. CRYPTO IMPLEMENTATIONS

| Primitive | File(s) | Key Details |
|-----------|---------|-------------|
| **Age Encryption** | `implant/sliver/cryptography/crypto.go` | X25519 key exchange + ChaCha20Poly1305 for session init. |
| **ChaCha20Poly1305** | `implant/sliver/cryptography/crypto.go` | Symmetric session encryption after key exchange. Gzip compression before encryption. Replay attack detection via SHA256 digest tracking. |
| **Minisign** | `implant/sliver/cryptography/minisign.go`, `util/minisign/` | Ed25519-based message signing for all C2 envelopes. 74-byte raw signature format. |
| **Ed25519** | `implant/sliver/cryptography/minisign.go` | Used for per-envelope signatures derived from peer key pair. |
| **mTLS Certificates** | `implant/sliver/transports/mtls/mtls.go` | Baked-in PEM certificates. Custom CA verification without hostname check. |
| **WireGuard Crypto** | native WireGuard | Curve25519 + ChaCha20Poly1305 (native WireGuard stack). |

### 8. ADDITIONAL SLIVER CAPABILITIES

- **Extensions** (`extension/`): WASM-based extension system, in-memory filesystem (`memfs.go`)
- **Netstack** (`netstack/`): Userspace TCP/IP stack for WireGuard TUN interface
- **Port Forwarding** (`rportfwd/`, `forwarder/`): Reverse port forwarding and SOCKS5 proxy
- **Service Installation** (`service/`): Windows service creation for persistence
- **Screenshot** (`screen/`): Cross-platform screenshot via GDI (Windows), X11 (Linux), CoreGraphics (macOS)
- **Process Dump** (`procdump/`): Cross-platform process memory dumping
- **Registry Operations** (`registry/`): Windows registry read/write/delete
- **Netstat** (`netstat/`): Cross-platform network connection enumeration
- **PS** (`ps/`): Cross-platform process listing
- **Mount** (`mount/`): Linux mount namespace operations
- **Shell** (`shell/`): Interactive PTY shell with resize support
- **SSH** (`shell/ssh/`): SSH client for pivoting
- **TCP Proxy** (`tcpproxy/`): TCP-level forwarding for pivots
- **Watchtower** (`server/watchtower/`): Implant health monitoring

---

## REPOSITORY 2: PUPY (Python C2 Framework)

**Total source files examined: 507 .py files**

### 1. C2 TRANSPORT PROTOCOLS (16 total)

| Transport | Directory | Encryption | Key Exchange |
|-----------|-----------|------------|--------------|
| **ssl** | `transports/ssl/` | AES-256-CTR over TLS | RSA-4096 + AES-256 |
| **ssl_rsa** | `transports/ssl_rsa/` | AES-256-CTR over TLS | RSA-4096 |
| **rsa** | `transports/rsa/` | AES-256-CTR | RSA-4096 |
| **ec4** | `transports/ec4/` | AES-256-CTR | ECDH (Curve25519) + RC4 |
| **ecm** | `transports/ecm/` | AES-256-CTR | ECDH (brainpoolP384r1) |
| **obfs3** | `transports/obfs3/` | AES-CTR after obfs3 handshake | ECDH via obfs3 DH + HMAC-SHA256 |
| **kc4** | `transports/kc4/` | AES-256-CTR | Custom KX + RC4 |
| **http** | `transports/http/` | AES-256-CTR wrapped in HTTP | RSA-4096 + AES-256 |
| **ws** | `transports/ws/` | AES-256-CTR over WebSocket | RSA-4096 + AES-256 |
| **dfws** | `transports/dfws/` | AES-256-CTR over WebSocket | RSA-4096 + AES-256 (direct flow) |
| **tcp_cleartext** | `transports/tcp_cleartext/` | None | None |
| **udp_cleartext** | `transports/udp_cleartext/` | None | None |
| **udp_secure** | `transports/udp_secure/` | AES-256-CTR over UDP | RSA-4096 + AES-256 |

### 2. TRANSPORT CRYPTO PRIMITIVES

| Primitive | Implementation File | Details |
|-----------|---------------------|---------|
| **ECPV (EC Point Verification)** | `network/lib/transports/cryptoutils/ecpv.py` (412 lines) | Custom ECDH with pubkey caching. Supports multiple curves (brainpoolP384r1). Uses SHA3-256/SHA3-512 hashing. CTR/CFB AES modes. |
| **AES** | `network/lib/transports/cryptoutils/aes.py` | AES-256-CTR and AES-256-CFB implementations. |
| **RC4** | `network/lib/transports/cryptoutils/rc4.py` | RC4 stream cipher for legacy transports. |
| **XOR** | `network/lib/transports/cryptoutils/xor.py` | Simple XOR cipher. |
| **SHA** | `network/lib/transports/cryptoutils/sha.py` | SHA1, SHA3-256, SHA3-512 wrappers. |
| **PBKDF2** | `network/lib/transports/cryptoutils/pbkdf2.py` | Password-based key derivation. |
| **RSA+AES** | `network/lib/transports/rsa_aes.py` | RSA-4096 key exchange + AES-256-CTR session. |
| **obfs3 DH** | `network/lib/transports/obfs3/obfs3_dh.py` | obfs3-specific ECDH with uniform group element representation. |
| **Dummy** | `network/lib/transports/dummy.py` | No-op transport for testing. |

### 3. TRANSPORT WRAPPERS

| Wrapper | File | Details |
|---------|------|---------|
| **HTTP Wrapper** | `network/lib/transports/httpwrap.py` | Wraps any transport in HTTP POST/GET with configurable headers, user-agent, host. |
| **WebSocket** | `network/lib/transports/websocket.py` | WebSocket framing for ws/dfws transports. |

### 4. LAUNCHERS

| Launcher | File | Function |
|----------|------|----------|
| **connect** | `network/lib/launchers/connect.py` | Outbound TCP connection with chosen transport. Multiple host fallback. |
| **bind** | `network/lib/launchers/bind.py` | Inbound TCP listener. |
| **auto_proxy** | `network/lib/launchers/auto_proxy.py` | Automatic proxy detection and connection. |
| **dnscnc** | `network/lib/launchers/dnscnc.py` | DNS command-and-control with DoH support, port quiz, online detection. |

### 5. DNS COMMAND & CONTROL (PicoCmd)

| Component | File | Details |
|-----------|------|---------|
| **Core protocol** | `network/lib/picocmd/picocmd.py` (1828 lines) | Binary protocol over DNS TXT/A/AAAA records. Commands: Poll, Ack, Idle, Sleep, CheckConnect, Reexec, Exit, Disconnect, Policy, Kex, SystemInfo, SetProxy, Connect, DownloadExec, OnlineStatus, ConnectablePort. |
| **DNS Encoder** | `network/lib/picocmd/dns_encoder.py` | Encodes binary data into DNS-safe character set. |
| **Base Conversion** | `network/lib/picocmd/baseconv.py` | Arbitrary base encoding for DNS transport. |
| **ASCII85** | `network/lib/picocmd/ascii85.py` | ASCII85 encoding for compact DNS payloads. |

### 6. PERSISTENCE METHODS

| Platform | Method | File | Details |
|----------|--------|------|---------|
| **Windows** | Registry Run Key | `scriptlets/persistence.py` | `add_registry_startup()` - copies executable, adds HKLM/HKCU Run key. |
| **Linux** | systemd Service | `packages/linux/all/persistence.py` (418 lines) | Creates systemd service units with `.service` + `.d/` override files. Supports LD_PRELOAD injection for shared libraries. |
| **Linux** | XDG Autostart | `packages/linux/all/persistence.py` | Creates `~/.config/autostart/*.desktop` or `/etc/xdg/autostart/*.desktop` entries. |
| **Linux** | RC Scripts | `packages/linux/all/persistence.py` | Appends to writable RC scripts (`/etc/rc.local`, `/etc/init.d/rc.local`, `/etc/rc`, `/etc/init.d/dbus`). |
| **Linux** | Binary Drop | `packages/linux/all/persistence.py` | Drops payload to masqueraded paths (e.g., `~/.dropbox-dist/dropboxc`, `/usr/bin/atd`, `/usr/bin/dcrond`). Timestomps to `/bin/sh` time. |
| **Linux** | Library Drop | `packages/linux/all/persistence.py` | Drops .so to paths like `~/.local/lib/*.so.1`, `/lib/lib*.so.1`, `/usr/lib/lib*.so.1`. LD_PRELOAD via systemd/Xdg/Rc. |
| **Linux** | Daemonize | `scriptlets/daemonize.py` | Forks, detaches from terminal, becomes a daemon process. |

### 7. PROCESS INJECTION TECHNIQUES

| Technique | File | Platform | Details |
|-----------|------|----------|---------|
| **Reflective DLL Injection** | `packages/windows/all/pupwinutils/memexec.py` (236 lines) | Windows | `run_pe_from_memory()` via `pupymemexec` extension. Allocates memory, maps PE, resolves imports, calls entry point. |
| **PowerLoader (PowerShell Pipe)** | `packages/windows/all/powerloader.py` (121 lines) | Windows | Creates named pipe, generates Base64-encoded PowerShell one-liner that reads assembly from pipe, loads via `Reflection.Assembly.Load`. |
| **memfd_create** | `agent/_linux_memfd.py` (97 lines) | Linux | Creates anonymous in-memory file via `memfd_create` syscall (x86_64:319, i686:356, arm:385). Used for in-memory binary execution. |
| **Migration** | `modules/lib/windows/migrate.py` | Windows | Process migration via reflective DLL injection into target process. |
| **Linux ELF Execution** | `modules/lib/linux/exec_elf.py` | Linux | In-memory ELF execution. |
| **Linux Migration** | `modules/lib/linux/migrate.py` | Linux | Linux process migration. |

### 8. CREDENTIAL DUMPING

| Module | File | Details |
|--------|------|---------|
| **Creddump7** | `external/creddump7/` | Full creddump7 integration. Dumps: SAM hashes (`pwdump.py` via framework), LSA secrets (`lsadump.py`), cached domain credentials (`cachedump.py`), domain cached credentials (`domcachedump.py`). Registry hive parsing (`rawreg.py`, `hashdump.py`, `lsasecrets.py`). |
| **WDigest** | `packages/windows/all/pupwinutils/wdigest.py` | Enables/disables WDigest `UseLogonCredential` registry key to force plaintext credential storage. |
| **Mimikatz** | `modules/mimikatz.py` | Mimikatz integration via reflective loading. |
| **Mimipy** | `modules/mimipy.py` | Python-based credential dumping (Mimikatz alternative). |
| **Lazagne** | `modules/lazagne.py` | LaZagne password recovery integration. |
| **NetCreds** | `packages/all/pupyutils/netcreds.py` | Network credential sniffing. |
| **Credential Store** | `network/lib/netcreds.py` | `add_cred()`, `find_first_cred()` for managing captured credentials. |

### 9. LATERAL MOVEMENT

| Technique | File | Details |
|-----------|------|---------|
| **PsExec** | `packages/all/pupyutils/psexec.py` (1413 lines) | SMB-based lateral movement using Impacket. Creates Windows service via SCM RPC over SMB. Supports SMB1/2/3. Uploads service binary via ADMIN$ share. Named pipe stager. PowerShell stdout capture. |
| **WMI** | `modules/wmic.py`, `modules/rwmic.py` | WMI-based remote execution via DCOM. |
| **SMB Spider** | `packages/all/pupyutils/smbspider.py` | SMB share enumeration and file spidering. |
| **Share Enum** | `packages/all/pupyutils/share_enum.py` | Network share enumeration. |
| **AD Operations** | `modules/ad.py` | Active Directory enumeration and operations. |
| **RDP** | `modules/rdesktop.py` | Remote desktop enable/check. |
| **RDP Check** | `packages/all/pupyutils/rdp_check.py` | RDP availability check. |

### 10. UAC BYPASS

| Method | File | Details |
|--------|------|---------|
| **Token Manipulation** | `packages/windows/all/pupwinutils/bypassuac_token_imp.py` (433 lines) | Token stealing from auto-elevated process (wusa.exe). Duplicate elevated token, lower IL from High to Medium, create restricted LUA token, impersonate, run target. Based on James Forshaw/UACME method. |
| **Registry Hijacking - Fodhelper** | `packages/windows/all/pupwinutils/bypassuac_registry.py` | `HKCU\Software\Classes\ms-settings\Shell\Open\command` hijack + fodhelper.exe trigger. |
| **Registry Hijacking - EventVwr** | `packages/windows/all/pupwinutils/bypassuac_registry.py` | `HKCU\Software\Classes\mscfile\shell\open\command` hijack + eventvwr.exe trigger. |

### 11. ADDITIONAL PUPY CAPABILITIES

| Category | Key Modules |
|----------|------------|
| **Android** | GPS tracking, camera capture, contacts, calls, SMS, vibrator, text-to-speech, app listing |
| **Keylogging** | Windows keylogger (`keylogger.py`), mouse logger (`mouselogger.py`), Linux keylogger |
| **Screen Capture** | Screenshot (`screenshot.py`), webcam snap (`webcamsnap.py`) |
| **File System** | Full FS operations, junctions (`junctions.py`), NTFS streams (`ntfs_streams.py`) |
| **Shell** | Interactive shell, PowerShell (`powershell.py`), Python shell (`pyexec.py`), SSH (`ssh.py`) |
| **Network** | Port forward, SOCKS5 proxy, TCP dump, NBNS spoofing, port scan, netmon |
| **VM Detection** | `checkvm.py` for detecting virtualized environments |
| **Stealth** | `hide_process.py` (Linux), `linux_stealth.py`, `hide_argv.py` |
| **Outlook** | Outlook email extraction (`outlook.py`) |
| **RDP** | RDP session manipulation (`rdp.py`, `rdesktop.py`) |
| **ODBC** | Database credential extraction (`odbc.py`) |
| **Cloud** | Cloud metadata extraction (`cloudinfo.py`) |

### 12. PUPY ARCHITECTURE NOTES

- **RPyC-based RPC**: Custom RPyC protocol for command dispatch (`network/lib/rpc/`)
- **Memory Importer**: `agent/memimporter/` for loading Python packages from memory (Windows PE, Linux ELF, POSIX)
- **Offloading**: `pupylib/PupyOffload.py` for offloading heavy tasks
- **Trigger System**: `pupylib/PupyTriggers.py`, `triggers/` for event-based actions
- **Payload Generation**: `payloads/` for generating diverses payloads (PS1, Python oneliner, Rubber Ducky, dotnet)

---

## REPOSITORY 3: UACME (UAC Bypass Toolkit)

**Total source files examined: 65 .c files (no .cpp)**

### COMPLETE UAC BYPASS METHOD CATALOG

All methods from `Source/Akagi/methods/methods.c` dispatch table:

| # | Method Name | Function | Min OS Build | Max OS Build | Technique Category |
|---|-------------|----------|-------------|-------------|-------------------|
| 1 | **UacMethodTest** | `MethodTest` | Win7 RTM | MAX | Debug test method |
| 2 | **UacMethodDISM** | `MethodDism` | Win7 RTM | MAX | DLL hijacking - DISM |
| 3 | **UacMethodUiAccess** | `MethodUiAccess` | Win7 RTM | MAX | UI Accessibility token manipulation |
| 4 | **UacMethodMsSettings** | `MethodMsSettings` | Win10 TH1 | MAX | Registry hijack - ms-settings protocol |
| 5 | **UacMethodDiskSilentCleanup** | `MethodTyranid` | Win8 Blue | MAX | Environment variable hijack - DiskCleanup |
| 6 | **UacMethodHakril** | `MethodHakril` | Win7 RTM | MAX | AppInfo command line parser abuse + custom MMC snap-in |
| 7 | **UacMethodCorProfiler** | `MethodCorProfiler` | Win7 RTM | MAX | .NET CLR Profiler DLL hijacking |
| 8 | **UacMethodCMLuaUtil** | `MethodCMLuaUtil` | Win7 RTM | MAX | COM elevation - ICMLuaUtil interface (CMSTPLUA CLSID) |
| 9 | **UacMethodDccwCOM** | `MethodDccwCOM` | Win7 RTM | MAX | COM elevation - DCCW (Display Color Calibration) |
| 10 | **UacMethodShellSdclt** | `MethodShellSdctl` | Win10 RS1 | MAX | Shell registry hijack - sdclt.exe |
| 11 | **UacMethodDebugObject** | `MethodDebugObject` | Win7 RTM | MAX | Debug object privilege abuse |
| 12 | **UacMethodShellChangePk** | `MethodShellChangePk` | Win10 RS1 | MAX | Shell registry hijack via ChangePK |
| 13 | **UacMethodMsSettings2** | `MethodMsSettings` | Win10 RS4 | MAX | Registry protocol hijack (variant) |
| 14 | **UacMethodNICPoison** | `MethodNICPoison` | Win7 RTM | MAX | Network interface configuration abuse |
| 15 | **UacMethodIeAddOnInstall** | `MethodIeAddOnInstall` | Win7 RTM | MAX | IE add-on installer hijacking |
| 16 | **UacMethodMsSettingsProtocol** | `MethodProtocolHijack` | Win10 TH1 | MAX | Protocol handler hijacking |
| 17 | **UacMethodMsStoreProtocol** | `MethodProtocolHijack` | Win10 RS5 | MAX | Microsoft Store protocol hijacking |
| 18 | **UacMethodCurVer** | `MethodCurVer` | Win10 TH1 | MAX | CurVer COM hijacking |
| 19 | **UacMethodNICPoison2** | `MethodNICPoison` | Win7 RTM | MAX | NIC Poison variant |
| 20 | **UacMethodMsdt** | `MethodMsdt` | Win10 TH1 | MAX | MSDT diagnostic tool hijacking |
| 21 | **UacMethodVFServerTaskSched** | `MethodVFServerTaskSched` | Win8 Blue | MAX | Virtualization-based task scheduler |
| 22 | **UacMethodVFServerDiagProf** | `MethodVFServerDiagProf` | Win7 RTM | MAX | Virtualization diagnostic profile |
| 23 | **UacMethodIscsiCpl** | `MethodIscsiCpl` | Win7 RTM | MAX | iSCSI control panel DLL hijacking |
| 24 | **UacMethodAtlHijack** | `MethodAtlHijack` | Win7 RTM | MAX | ATL COM DLL hijacking |
| 25 | **UacMethodQuickAssist** | `MethodQuickAssist` | Win10 RS5 | MAX | Quick Assist hijacking |
| 26 | **UacMethodCleanMgrAdmin** | `MethodCleanMgrAdmin` | Win10 21H2 | MAX | Clean Manager administrative hijacking |

### METHOD TECHNIQUE CLASSIFICATION

#### A. DLL HIJACKING VIA MISSING SYSTEM32 DLLs (hybrids.c - 1882 lines)
- **`ucmGenericAutoelevationEx()`**: Core function. Drops proxy DLL to target path in system32, executes auto-elevated application that loads the missing DLL.
- Used by: DISM, Wow64Logger, UiAccess, SXS, SXS DCCW, CorProfiler, IscsiCpl, Junction, VFServerTaskSched, VFServerDiagProf
- Cleanup: `ucmMethodCleanupSingleItemSystem32()` removes dropped files.

#### B. COM OBJECT ELEVATION (comsup.c - 644 lines)
- **`ucmAllocateElevatedObject()`**: `CoGetObject` with elevation moniker `Elevation:Administrator!new:` + CLSID. Gets elevated COM interface.
- Used by: CMLuaUtil method (via `ICMLuaUtil::ShellExec`), DccwCOM, EditionUpgradeManager

#### C. REGISTRY HIJACKING (shellsup.c - 610 lines)
- **`ucmxSetSlaveParams()`**: Sets `DelegateExecute` to empty, command line to payload.
- Shell registry key hijacks: sdclt.exe, eventvwr.exe, fodhelper.exe, compmgmtlauncher.exe
- Protocol handler hijacks: ms-settings, ms-store
- App Paths hijacks

#### D. ENVIRONMENT VARIABLE ABUSE (tyranid.c - 603 lines)
- **DiskCleanup Environment Variable**: Sets user `%windir%` environment variable to payload path, triggers `SilentCleanup` scheduled task.
- **EditionUpgradeManager**: Spoofs `%windir%` env var to redirect `clipup.exe` execution.
- Additional techniques from James Forshaw blog posts.

#### E. DIRECTORY MOCKING (dwells.c - 153 lines)
- **`ucmDirectoryMockMethod()`**: Creates fake `system32` in `%temp%`, copies auto-elevated exe + proxy DLL, creates fake Windows root directory via object manager symbolic link (`\RPC Control` prefix). Abuses `GetLongPathNameW` behavior during AppInfo.

#### F. APPINFO PARSER ABUSE (hakril.c - 270 lines)
- **`ucmHakrilMethod()`**: Embeds custom MMC snap-in with Shockwave Flash object in resource. Snap-in executes remote script at High IL via MMC.exe.

#### G. SSPI DATAGRAM ABUSE (antonioCoco.c - 905 lines)
- **`ucmSspiDatagramMethod()`**: Bypasses UAC via SSPI datagram context. Posts RPC messages to SCM (Service Control Manager) over local RPC transport. Creates and starts a service running as SYSTEM without triggering UAC prompt. Detailed RPC packet crafting.

#### H. ADDITIONAL TECHNIQUES (azagarampur.c - 2229 lines)
- **Multiple AzAgarampur methods**: `byeintegrity` series. Uses Program Compatibility Assistant (PCA) service. ngen.log timestamp checks. Elevated factory server COM objects. Task scheduler abuse.

#### I. SUPPORT INFRASTRUCTURE
- **WUSA/MSU Packaging** (wusa.c - 384 lines): Creates .cab/MSU cabinet files for WUSA-based methods
- **Masquerading** (sup.c): Process masquerading to trusted executables
- **LDR Resource Loading** (ldr.c): Loading embedded payloads from PE resources
- **Decompression**: RtlDecompressBuffer for embedded payloads

### UACME PAYLOAD DELIVERY METHODS (from methods.c)
- **FUBUKI_ID**: DLL proxy payload embedded as PE resource (most common)
- **FUBUKI32_ID**: 32-bit variant
- **AKATSUKI_ID**: Alternative payload DLL
- **KAMIKAZE_ID**: MMC snap-in payload for Hakril method
- **PAYLOAD_ID_NONE**: Method uses external command (no embedded payload)

### METHODS NOT IMPLEMENTED FOR WIN32
Methods restricted to x64 only: NICPoison, IeAddOnInstall, MsSettingsProtocol, MsStoreProtocol, CurVer, VFServerTaskSched, VFServerDiagProf, AtlHijack, QuickAssist, CleanMgrAdmin

---

## TECHNIQUE CROSS-REFERENCE MATRIX

| Technique Family | Sliver | Pupy | UACME |
|-----------------|--------|------|-------|
| **mTLS/TLS C2** | ✓ | ✓ (ssl, ssl_rsa) | - |
| **HTTP/HTTPS C2** | ✓ | ✓ | - |
| **DNS C2** | ✓ | ✓ (PicoCmd) | - |
| **WireGuard C2** | ✓ | - | - |
| **WebSocket C2** | - | ✓ | - |
| **UDP C2** | - | ✓ | - |
| **Obfuscation Transport** | - | ✓ (obfs3) | - |
| **Process Injection** | ✓ (5+ methods) | ✓ (3 methods) | - |
| **Reflective DLL** | ✓ (SRDI) | ✓ | - |
| **PowerShell Loader** | - | ✓ (PowerLoader) | - |
| **Shellcode Encoding** | ✓ (XOR, SGN) | - | - |
| **Donut** | ✓ | - | - |
| **BOF/COFF Loading** | ✓ | - | - |
| **DLL Hijacking** | ✓ (automated) | - | ✓ (primary technique) |
| **COM Elevation** | - | - | ✓ |
| **Registry Hijack UAC** | - | ✓ | ✓ |
| **Token Manipulation UAC** | ✓ (GetSystem) | ✓ | - |
| **Environment Variable Hijack** | - | - | ✓ |
| **AppInfo Parser Abuse** | - | - | ✓ |
| **SSPI Datagram Abuse** | - | - | ✓ |
| **Credential Dumping** | - | ✓ (creddump, mimikatz) | - |
| **Lateral Movement** | - | ✓ (PsExec, WMI) | - |
| **Linux Persistence** | - | ✓ (systemd, XDG, RC) | - |
| **Android Support** | - | ✓ | - |
| **AMSI Bypass** | ✓ | - | - |
| **ETW Bypass** | ✓ | - | - |
| **DLL Unhooking** | ✓ | - | - |
| **Parent PID Spoof** | ✓ | - | - |
| **Garble Obfuscation** | ✓ | - | - |
| **WASM Extensions** | ✓ | - | - |
