# TOOL-TO-TECHNIQUE MAP
> Generated from 25 Killer Queen skills — 556+ tools mapped to MITRE ATT&CK techniques and skill references.

---

## RECONNAISSANCE (TA0043)

### Subdomain & DNS Discovery
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| subfinder | T1596 — Search Open Technical Databases | awesome-redteam-toolkit, web-attacks |
| amass (OWASP) | T1596 — Search Open Technical Databases | awesome-redteam-toolkit |
| ksubdomain | T1596 — Search Open Technical Databases | awesome-redteam-toolkit |
| probable_subdomains | T1596 — Search Open Technical Databases | awesome-redteam-toolkit |
| dnsx | T1596 — DNS/Passive DNS | awesome-redteam-toolkit |
| adidnsdump | T1596 — Active Directory DNS Dump | awesome-redteam-toolkit, windows-red-team |
| dig / host | T1596 — DNS Queries | infrastructure-attacks, defensive-forensics |
| massdns | T1596 — High-Performance DNS Resolution | awesome-redteam-toolkit |

### Network Scanning
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| nmap | T1046 — Network Service Scanning | infrastructure-attacks, testing-methodology |
| masscan | T1046 — Network Service Scanning | awesome-redteam-toolkit |
| fscan | T1046 — Fast Intranet Scan | awesome-redteam-toolkit |
| kscan | T1046 — Network Service Scanning | awesome-redteam-toolkit |
| ENScan_GO | T1596 — Enterprise Info Scan | awesome-redteam-toolkit |
| SharpScan | T1046 — C# Intranet Scanner | awesome-redteam-toolkit, windows-red-team |
| TscanPlus | T1046 — Network Service Scanning | awesome-redteam-toolkit |
| zmap | T1046 — Internet-Wide Scanning | awesome-redteam-toolkit |

### Web Crawling & URL Discovery
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| katana | T1596 — Web Crawling | web-attacks, bughunter-methodology |
| gospider | T1596 — Web Crawling | web-attacks |
| waybackurls | T1596 — Archive History | web-attacks, bughunter-methodology |
| gau (getallurls) | T1596 — URL Collection | web-attacks, bughunter-methodology |
| hakrawler | T1596 — Web Crawling | web-attacks |
| httpx | T1596 — Live Host Discovery | web-attacks, bughunter-methodology |

### Technology Fingerprinting
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| whatweb | T1592 — Victim Host Information | testing-methodology, web-attacks |
| wappalyzer | T1592 — Victim Host Information | testing-methodology |
| FingerprintHub | T1592 — Fingerprint Database | awesome-redteam-toolkit |
| TideFinger_Go | T1592 — Technology Detection | awesome-redteam-toolkit |
| webanalyze | T1592 — Web Technology Fingerprint | web-attacks |
| testssl.sh | T1592 — SSL/TLS Analysis | testing-methodology |

### OSINT & Google Dorking
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Google Hacking DB | T1593 — Search Engines | awesome-redteam-toolkit |
| GitDorker | T1593 — Code Repository Search | awesome-redteam-toolkit |
| dorks_hunter | T1593 — Automated Dorking | awesome-redteam-toolkit |
| gitdorks_go | T1593 — GitHub Search | awesome-redteam-toolkit |
| Shodan | T1596 — Search Open Technical Databases | testing-methodology |
| truffleHog | T1552 — Unsecured Credentials | web-attacks, bughunter-methodology |
| gitleaks | T1552 — Git Secret Scanner | awesome-redteam-toolkit |

---

## INITIAL ACCESS (TA0001)

### Exploit Public-Facing Application
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| nuclei | T1190 — Exploit Public-Facing App | web-attacks, bughunter-methodology |
| nuclei-templates | T1190 — Template-Based Exploits | awesome-redteam-toolkit |
| metasploit-framework | T1190 — Exploit Framework | exploit-development, infrastructure-attacks |
| sqlmap | T1190 — SQL Injection Exploitation | web-attacks |
| ghauri | T1190 — SQL Injection Exploitation | web-attacks |
| Log4j2Scan | T1190 — Log4j Vulnerability Scanner | awesome-redteam-toolkit |
| SpringBoot-Scan | T1190 — Spring Boot Exploit Scanner | awesome-redteam-toolkit |
| WeblogicScan | T1190 — WebLogic Exploit Scanner | awesome-redteam-toolkit |
| TongdaScan_go | T1190 — Tongda OA Scanner | awesome-redteam-toolkit |

### Social Engineering & Phishing
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| GoPhish | T1566 — Phishing Framework | social-engineering-wireless |
| EvilGinx2 | T1566 — MFA Bypass Phishing | social-engineering-wireless |
| Modlishka | T1566 — Reverse Proxy Phishing | social-engineering-wireless |
| SET (Social Engineering Toolkit) | T1566 — Phishing Toolkit | social-engineering-wireless |
| SocialFish | T1566 — Phishing + 2FA Interception | social-engineering-wireless |
| King Phisher | T1566 — Phishing Campaigns | social-engineering-wireless |

### Credential Attacks
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| thc-hydra | T1110 — Brute Force | awesome-redteam-toolkit, infrastructure-attacks |
| hashcat | T1110 — Password Cracking | awesome-redteam-toolkit |
| john (John the Ripper) | T1110 — Password Cracking | awesome-redteam-toolkit |
| CrackMapExec | T1110 — Domain Password Spray | awesome-redteam-toolkit, windows-red-team |
| kerbrute | T1110 — Kerberos Brute Force | awesome-redteam-toolkit, windows-red-team |
| DomainPasswordSpray | T1110 — Domain Password Spray | awesome-redteam-toolkit, windows-red-team |
| DefaultCreds-cheat-sheet | T1078 — Default Credentials | awesome-redteam-toolkit |

---

## EXECUTION (TA0002)

### Command & Scripting
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| PowerShell (various) | T1059.001 — PowerShell | windows-red-team, malware-dev |
| Custom C++ injector | T1059 — Native Code Execution | windows-red-team |
| msfvenom | T1059 — Payload Generation | windows-red-team, exploit-development |
| shellcodeloader | T1059 — Shellcode Loader | awesome-redteam-toolkit |
| reverse-shell-generator | T1059 — Reverse Shell Generator | awesome-redteam-toolkit |

### Scheduled Tasks
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| schtasks.exe | T1053.005 — Scheduled Task | malware-dev, windows-red-team |
| at.exe | T1053.002 — At (Windows) | windows-red-team |

### Process Injection (30 Methods)
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Sliver (Go C2) | T1055 — Process Injection | malware-dev, windows-red-team |
| Pupy RAT | T1055 — Reflective DLL Injection | malware-dev |
| living-off-the-land | T1055.012 — Process Hollowing | malware-dev |
| SysWhispers | T1055 — Direct Syscall Injection | windows-red-team |
| Hells Gate | T1055 — Dynamic Syscall Resolution | windows-red-team |
| Halos Gate | T1055 — Syscall Recovery | windows-red-team |
| TokenPlayer | T1055 — Token Manipulation + Injection | windows-red-team |

---

## PERSISTENCE (TA0003)

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| QuasarRAT persistence | T1547.001 — Registry Run Keys | malware-dev |
| AsyncRAT persistence | T1547.001 — Registry Run Keys | malware-dev |
| Sliver persistence | T1547 — Boot/Logon Autostart | malware-dev |
| Pupy persistence | T1543 — Create/Modify System Process | malware-dev |
| schtasks.exe | T1053.005 — Scheduled Task | malware-dev |
| UACME | T1548.002 — Bypass User Account Control | malware-dev, windows-red-team |
| WMI Event Subscriptions | T1546.003 — WMI Event Subscription | windows-red-team |

---

## PRIVILEGE ESCALATION (TA0004)

### Linux
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| linpeas.sh (PEASS-ng) | T1068 — Exploitation for Privilege Escalation | infrastructure-attacks |
| linux-exploit-suggester | T1068 — Kernel Exploit Suggester | infrastructure-attacks |
| GTFOBins | T1548 — Abuse Elevation Control Mechanism | infrastructure-attacks |
| pwnkit (CVE-2021-4034) | T1068 — Polkit Exploit | infrastructure-attacks |
| OverlayFS (CVE-2021-3493) | T1068 — Kernel Exploit | infrastructure-attacks |
| postenum | T1068 — Linux Enumeration | awesome-redteam-toolkit |
| LinEnum | T1068 — Linux Enumeration | awesome-redteam-toolkit |
| GScan | T1068 — Linux Post-Exploit Scanner | awesome-redteam-toolkit |

### Windows
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| winPEAS (PEASS-ng) | T1068 — Windows Privilege Escalation | awesome-redteam-toolkit |
| Windows-Exploit-Suggester | T1068 — Windows Exploit Suggester | awesome-redteam-toolkit |
| PrivescCheck | T1068 — PowerShell Privesc Audit | awesome-redteam-toolkit |
| SeBackupPrivilege | T1134.002 — Token Impersonation | awesome-redteam-toolkit, windows-red-team |
| UACME (60+ methods) | T1548.002 — Bypass UAC | malware-dev, windows-red-team |

### Cloud IAM
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Pacu | T1068 — AWS Exploitation Framework | cloud-iam-attacks |
| ScoutSuite | T1526 — Cloud Security Audit | cloud-iam-attacks |
| cloudsplaining | T1068 — IAM Least Privilege Audit | cloud-iam-attacks |
| enumerate-iam | T1068 — IAM Permission Enumeration | cloud-iam-attacks |

---

## DEFENSE EVASION (TA0005)

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| SysWhispers | T1027 — Direct Syscall | windows-red-team |
| Hells Gate | T1027 — Dynamic Syscall Resolution | windows-red-team |
| RefleXXion | T1562.001 — API Unhooking | windows-red-team |
| SharpUnhooker | T1562.001 — API Unhooking | windows-red-team |
| certutil.exe | T1105 — Ingress Tool Transfer | windows-red-team |
| Cloudflare Bypass tools | T1036 — Masquerading | cloudflare-bypass |
| Botasaurus | T1036 — Browser Fingerprint Spoofing | cloudflare-bypass |
| CloakBrowser | T1036 — Stealth Chromium | cloudflare-bypass |
| undetected-chromedriver | T1036 — Selenium Anti-Detection | cloudflare-bypass |
| patchright | T1036 — Undetected Playwright | cloudflare-bypass |

---

## CREDENTIAL ACCESS (TA0006)

### Credential Dumping
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| mimikatz | T1003.001 — LSASS Memory | windows-red-team |
| creddump7 | T1003 — Credential Dumping | malware-dev |
| wdigest | T1003.001 — LSASS Memory | malware-dev |
| volatility3 (hashdump) | T1003 — SAM Dump | defensive-forensics |
| volatility3 (lsadump) | T1003 — LSA Secrets | defensive-forensics |

### Kerberos Attacks
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Rubeus | T1558.003 — Kerberoasting | windows-red-team |
| GetUserSPNs.py (Impacket) | T1558.003 — Kerberoasting | windows-red-team |
| kerbrute | T1558.003 — Kerberos Brute Force | awesome-redteam-toolkit |
| mimikatz (Golden/Silver Ticket) | T1558.002 — Silver Ticket | windows-red-team |

### Password Cracking
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| hashcat | T1110.002 — Password Cracking | awesome-redteam-toolkit |
| john | T1110.002 — Password Cracking | awesome-redteam-toolkit |
| Name-That-Hash | T1110 — Hash Type Identification | awesome-redteam-toolkit |
| haiti | T1110 — Hash Type Identification | awesome-redteam-toolkit |

### JWT Attacks
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| jwt_tool | T1606 — Forge Web Credentials | awesome-redteam-toolkit, web-attacks |
| jwtcrack | T1110 — JWT Secret Cracking | awesome-redteam-toolkit |
| c-jwt-cracker | T1110 — JWT Secret Cracking | awesome-redteam-toolkit |
| jwt-hack | T1606 — JWT Manipulation | awesome-redteam-toolkit |
| jwt-pwn | T1606 — JWT Exploitation | awesome-redteam-toolkit |

---

## DISCOVERY (TA0007)

### AD Enumeration
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| PowerView | T1087 — Account Discovery | awesome-redteam-toolkit, windows-red-team |
| BloodHound | T1087 — Domain Trust Discovery | windows-red-team |
| SharpHound | T1087 — BloodHound Data Collector | windows-red-team |
| adidnsdump | T1087 — AD DNS Dump | awesome-redteam-toolkit |

### Network Discovery
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| nmap | T1046 — Network Service Scanning | infrastructure-attacks |
| netstat / ss | T1049 — System Network Connections | infrastructure-attacks |
| ARP scan | T1018 — Remote System Discovery | infrastructure-attacks |
| SMB enumeration | T1135 — Network Share Discovery | windows-red-team |

### File & Directory Discovery
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| gobuster | T1083 — File/Directory Discovery | web-attacks |
| ffuf | T1083 — File/Directory Fuzzing | web-attacks |
| feroxbuster | T1083 — File/Directory Discovery | web-attacks |
| dirsearch | T1083 — Directory Brute Force | web-attacks |
| wfuzz | T1083 — Web Fuzzing | awesome-redteam-toolkit |

---

## LATERAL MOVEMENT (TA0008)

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| PsExec | T1021.002 — SMB/Windows Admin Shares | windows-red-team |
| Impacket (wmiexec, smbexec, atexec) | T1021.006 — WinRM, T1047 — WMI | windows-red-team |
| CrackMapExec | T1021 — Remote Services | windows-red-team |
| WinRM | T1021.006 — Windows Remote Management | windows-red-team |
| Pass-the-Hash (mimikatz) | T1550.002 — Pass the Hash | windows-red-team |
| Pass-the-Ticket | T1550.003 — Pass the Ticket | windows-red-team |

---

## COMMAND & CONTROL (TA0011)

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Sliver | T1573 — Encrypted Channel (mTLS/HTTPS) | malware-dev |
| Pupy RAT | T1573 — Multi-Transport (obfs3/DNS) | malware-dev |
| CobaltStrike | T1573 — Encrypted Channel | awesome-redteam-toolkit |
| dnscat2 | T1071.004 — DNS C2 | awesome-redteam-toolkit |
| QuasarRAT | T1573 — TLS C2 | malware-dev |
| AsyncRAT | T1573 — Encrypted Channel | malware-dev |
| Mirai | T1071 — Telnet C2 | malware-dev |
| Godzilla (memshell) | T1105 — Java Memory Shell | awesome-redteam-toolkit |
| DNS-Shell | T1071.004 — DNS Tunnel Shell | awesome-redteam-toolkit |
| C2ReverseProxy | T1090 — Connection Proxy | awesome-redteam-toolkit |

---

## EXFILTRATION (TA0010)

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| DNS tunneling | T1048.001 — Exfil Over DNS | defensive-forensics |
| interactsh-client | T1048 — OOB Exfiltration | web-attacks, bughunter-methodology |
| Burp Collaborator | T1048 — OOB Confirmation | web-attacks |
| Alphalog | T1048 — DNS/HTTP/RMI/LDAP Logging | awesome-redteam-toolkit |
| DNSLog-GO | T1048 — DNS Logging | awesome-redteam-toolkit |

---

## IMPACT (TA0040)

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| vssadmin.exe | T1490 — Inhibit System Recovery | windows-red-team, malware-dev |
| wbadmin.exe | T1490 — Backup Deletion | windows-red-team |
| ransomware patterns | T1486 — Data Encrypted for Impact | malware-dev |

---

## WEB APPLICATION ATTACKS

### SQL Injection
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| sqlmap | T1190 — SQL Injection | web-attacks |
| ghauri | T1190 — SQL Injection | web-attacks |
| sql-injection-payload-list | T1190 — Payload Library | awesome-redteam-toolkit |

### XSS & Client-Side
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| dalfox | T1189 — XSS Scanner | web-attacks |
| XSStrike | T1189 — XSS Detection | web-attacks |
| DOM Invader | T1189 — DOM XSS | web-attacks, browser-exploitation |
| BeEF | T1189 — Browser Exploitation Framework | browser-exploitation |

### SSRF & Server-Side
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| ssrfmap | T1190 — SSRF Exploitation | web-attacks |
| interactsh-client | T1190 — OOB SSRF Confirmation | web-attacks |
| Burp Collaborator | T1190 — SSRF Confirmation | web-attacks |

### Command Injection
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| commix | T1190 — Command Injection Exploitation | web-attacks |

### SSTI
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| tplmap | T1190 — SSTI Exploitation | web-attacks |

### File Upload
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| fuxploider | T1190 — File Upload Exploitation | web-attacks |

### Web Cache & Smuggling
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| smuggler | T1190 — HTTP Request Smuggling | web-attacks |
| HTTP Request Smuggler (Burp) | T1190 — Request Smuggling | web-attacks |
| Turbo Intruder | T1190 — Race/Smuggling | web-attacks |
| toxicache | T1190 — Cache Poisoning | web-attacks |

### WordPress
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| wpscan | T1190 — WordPress Vulnerability Scanner | wordpress-pentesting, wordpress-recon |
| wp-cli | T1190 — WordPress CLI | wordpress-pentesting |

### API / GraphQL
| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| clairvoyance | T1190 — GraphQL Schema Enumeration | web-attacks |
| InQL (Burp) | T1190 — GraphQL Introspection | web-attacks |
| Postman | T1190 — REST API Testing | testing-methodology |

---

## MOBILE ATTACKS

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| adb | T1456 — Drive-by Compromise / App Install | mobile-attacks |
| apktool | T1406 — APK Reverse Engineering | mobile-attacks |
| jadx / jadx-gui | T1406 — Java Decompilation | mobile-attacks |
| apksigner | T1406 — APK Repackaging | mobile-attacks |
| zipalign | T1406 — APK Alignment | mobile-attacks |
| Frida | T1406 — Dynamic Instrumentation | mobile-attacks |
| objection | T1406 — Runtime Security Assessment | mobile-attacks |
| apkanalyzer | T1406 — Manifest Analysis | mobile-attacks |

---

## EMBEDDED / IOT / ICS

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| unblob | T1592 — Firmware Extraction | embedded-iot-attacks |
| binwalk | T1592 — Firmware Analysis | embedded-iot-attacks |
| EMBA | T1592 — Firmware Analysis Platform | embedded-iot-attacks |
| flashrom | T1592 — SPI Flash Dump | embedded-iot-attacks |
| OpenOCD | T1592 — JTAG Debugging | embedded-iot-attacks |
| QEMU | T1592 — Firmware Emulation | embedded-iot-attacks |
| Qiling Framework | T1592 — Binary Emulation | embedded-iot-attacks |
| Bus Pirate | T1592 — Hardware Debug Interface | embedded-iot-attacks |
| cwe_checker | T1592 — Vulnerability Detection | embedded-iot-attacks |
| firmwalker | T1592 — Firmware Recon | embedded-iot-attacks |
| FirmAE | T1592 — Firmware Emulation | embedded-iot-attacks |
| Firmadyne | T1592 — Firmware Emulation | embedded-iot-attacks |

---

## CLOUD / AWS ATTACKS

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Pacu | T1526 — AWS Exploitation Framework | cloud-iam-attacks |
| ScoutSuite | T1526 — Multi-Cloud Security Audit | cloud-iam-attacks |
| cloudsplaining | T1526 — IAM Policy Audit | cloud-iam-attacks |
| enumerate-iam | T1526 — IAM Permission Enumeration | cloud-iam-attacks |
| CloudSploit | T1526 — Cloud Security Scanning | cloud-iam-attacks |
| CloudGoat | T1526 — AWS Vulnerable-by-Design Lab | cloud-iam-attacks, embedded-iot-attacks |
| AWS CLI | T1526 — AWS API Access | cloud-iam-attacks |

---

## FORENSICS & DEFENSE

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Volatility3 | T1583 — Memory Forensics | defensive-forensics |
| Wireshark / tshark | T1040 — Network Packet Analysis | defensive-forensics |
| snort / suricata | T1040 — Network IDS/IPS | defensive-forensics |
| Zeek (Bro) | T1040 — Network Security Monitoring | defensive-forensics |
| LiME | T1583 — Linux Memory Acquisition | defensive-forensics |
| winpmem | T1583 — Windows Memory Acquisition | defensive-forensics |
| FTK Imager | T1583 — Disk/Memory Imaging | defensive-forensics |
| YARA | T1583 — Malware Signature Scanning | defensive-forensics |
| smtpdump | T1040 — SMTP Protocol Analysis | defensive-forensics |
| dd / dcfldd | T1583 — Disk Imaging | defensive-forensics |

---

## PASSWORD / WORDLIST RESOURCES

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| SecLists | T1110 — Wordlists/Dictionaries | awesome-redteam-toolkit |
| PayloadsAllTheThings | T1190 — Payload Library | awesome-redteam-toolkit, web-attacks |
| Assetnote wordlists | T1110 — Wordlists | awesome-redteam-toolkit |
| fuzzDicts | T1110 — Fuzzing Dictionaries | awesome-redteam-toolkit |
| OneListForAll | T1110 — Combined Wordlist | awesome-redteam-toolkit |
| pydictor | T1110 — Dictionary Generator | awesome-redteam-toolkit |

---

## WIRELESS / RF / PHYSICAL

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| aircrack-ng suite | T1592 — WiFi Attacks | social-engineering-wireless |
| HackRF One | T1592 — SDR Attacks | social-engineering-wireless |
| Proxmark3 | T1592 — RFID/NFC Attacks | social-engineering-wireless |
| Ubertooth One | T1592 — Bluetooth/BLE | social-engineering-wireless |
| USB Rubber Ducky | T1091 — HID Injection | social-engineering-wireless |
| Bash Bunny | T1091 — USB Attack Platform | social-engineering-wireless |

---

## C2 FRAMEWORKS

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| Sliver | T1071 — Go C2 Framework | malware-dev |
| CobaltStrike | T1071 — C2 Framework | awesome-redteam-toolkit |
| Pupy RAT | T1071 — Python C2 | malware-dev |
| QuasarRAT | T1071 — C# RAT | malware-dev |
| AsyncRAT | T1071 — C# RAT | malware-dev |
| dnscat2 | T1071.004 — DNS C2 | awesome-redteam-toolkit |
| Mirai | T1071 — IoT Botnet | malware-dev |

---

## EXPLOIT DEVELOPMENT

| Tool | Technique | Skill Reference |
|------|-----------|-----------------|
| GDB / pwndbg / gef | T1587.004 — Debugging | exploit-development |
| WinDbg | T1587.004 — Windows Debugging | exploit-development, browser-exploitation |
| Frida | T1587.004 — Dynamic Instrumentation | exploit-development, browser-exploitation |
| d8 (V8 shell) | T1587.004 — JS Engine Debugging | browser-exploitation |
| Fuzzilli | T1587.002 — JS Engine Fuzzing | browser-exploitation |
| domato | T1587.002 — DOM Fuzzer | browser-exploitation |
| ropper / ROPgadget | T1587.004 — ROP Chain Building | exploit-development |
| pwntools | T1587.004 — Exploit Development Library | exploit-development |
| Unicorn Engine | T1587.004 — CPU Emulation | exploit-development, embedded-iot-attacks |

---

> 556+ tools mapped across 15 MITRE ATT&CK tactics, web/mobile/embedded/cloud/wireless/forensics domains.
> Reference skills in `/root/prometheus-agent/skills-backup/` for full command references.
