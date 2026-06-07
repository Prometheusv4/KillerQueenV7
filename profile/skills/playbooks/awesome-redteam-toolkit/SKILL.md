---
name: awesome-redteam-toolkit
description: Comprehensive red team toolkit catalogue with 556 GitHub repositories across 16 categories — C2 frameworks, payload generators, recon tools, credential attacks, privilege escalation, lateral movement, persistence, Active Directory, cloud/Kubernetes, evasion, social engineering, exploits/POC, labs, reverse engineering, crypto, and 298+ other tools. Every repo link preserved for rapid operational reference.
triggers:
  - red team toolkit
  - awesome list
  - tool catalogue
  - C2 list
  - recon tool
  - persistence tool
  - evasion tool
  - privesc tool
  - lateral movement
  - Active Directory tools
  - cloud red team
  - exploit POC
  - red team labs
---

# Awesome-Redteam Toolkit — Complete Repository Reference

556 GitHub repositories across 16 categories. Source: Threekiii/Awesome-Redteam. Every link preserved for operational reference during engagements.

---

## C2 FRAMEWORKS (19 repos)

| Tool | Repo | Notes |
|------|------|-------|
| Awesome CobaltStrike | https://github.com/zer0yu/Awesome-CobaltStrike | Curated CobaltStrike resources |
| C2ReverseProxy | https://github.com/Daybr4ak/C2ReverseProxy | C2 reverse proxy |
| dnscat2 | https://github.com/iagox86/dnscat2 | DNS tunnel C2 |
| ConfluenceMemshell | https://github.com/Lotus6/ConfluenceMemshell | Confluence memshell |
| CVE-2022-26134 Memshell | https://github.com/BeichenDream/CVE-2022-26134-Godzilla-MEMSHELL | Confluence CVE-2022-26134 |
| CVE-2023-22527 Memshell | https://github.com/Boogipop/CVE-2023-22527-Godzilla-MEMSHELL | Confluence CVE-2023-22527 |
| reverse-shell-generator | https://github.com/0dayCTF/reverse-shell-generator | Reverse shell payload generator |
| java-memshell-generator | https://github.com/pen4uin/java-memshell-generator | Java memory shell generator |
| MemShellParty | https://github.com/ReaJason/MemShellParty | MemShell community |
| Godzilla-Suo5MemShell | https://github.com/X1r0z/Godzilla-Suo5MemShell | Godzilla Suo5 memshell |
| webshell | https://github.com/tennc/webshell | Webshell collection |
| RMI_Inj_MemShell | https://github.com/novysodope/RMI_Inj_MemShell | RMI injection memshell |
| TomcatMemShell | https://github.com/ce-automne/TomcatMemShell | Tomcat memshell |
| wsMemShell | https://github.com/veo/wsMemShell | WebSocket memshell |
| WebShell-Bypass-Guide | https://github.com/AabyssZG/WebShell-Bypass-Guide | Webshell evasion |
| Webshell_Generate | https://github.com/cseroad/Webshell_Generate | Webshell generator |
| java-memshell-scanner | https://github.com/c0ny1/java-memshell-scanner | Detect Java memshells |
| ASP.NET-Memshell-Scanner | https://github.com/yzddmr6/ASP.NET-Memshell-Scanner | Detect ASP.NET memshells |
| CS_Decrypt | https://github.com/5ime/CS_Decrypt | CobaltStrike traffic decrypt |

---

## PAYLOAD GENERATORS (4 repos)

| Tool | Repo |
|------|------|
| File-Download-Generator | https://github.com/r0eXpeR/File-Download-Generator |
| sql-injection-payload-list | https://github.com/payloadbox/sql-injection-payload-list |
| PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings |
| shellcodeloader | https://github.com/knownsec/shellcodeloader |

---

## RECON / ENUMERATION (49 tools)

### Google Dorking
- Google Hacking DB: https://github.com/cipher387/Dorks-collections-list
- GitDorker (CLI): https://github.com/obheda12/GitDorker
- dorks_hunter: https://github.com/six2dez/dorks_hunter
- Github search: https://github.com/search/advanced
- gitdorks_go: https://github.com/damit5/gitdorks_go

### Network Scanning
- **fscan**: https://github.com/shadow1ng/fscan — Fast intranet scan
- **qscan**: https://github.com/qi4L/qscan
- **TscanPlus**: https://github.com/TideSec/TscanPlus
- **kscan**: https://github.com/lcvvvv/kscan
- **ENScan_GO**: https://github.com/wgpsec/ENScan_GO — Enterprise info scan
- **Amass**: https://github.com/owasp-amass/amass — Subdomain enumeration
- **ApolloScanner**: https://github.com/b0bac/ApolloScanner

### Fingerprint / Tech Detection
- fingerprint: https://github.com/r0eXpeR/fingerprint
- FingerprintHub: https://github.com/0x727/FingerprintHub
- Finger: https://github.com/EASY233/Finger
- TideFinger_Go: https://github.com/TideSec/TideFinger_Go

### Subdomain Enumeration
- subfinder: https://github.com/projectdiscovery/subfinder
- ksubdomain: https://github.com/knownsec/ksubdomain
- probable_subdomains: https://github.com/zzzteph/probable_subdomains

### Fuzzing & Wordlists
- wfuzz: https://github.com/xmendez/wfuzz
- fuzzDicts: https://github.com/TheKingOfDuck/fuzzDicts
- Web-Fuzzing-Box: https://github.com/gh0stkey/Web-Fuzzing-Box
- fuzz.txt: https://github.com/Bo0oM/fuzz.txt
- nuclei: https://github.com/projectdiscovery/nuclei
- nuclei-templates: https://github.com/projectdiscovery/nuclei-templates

### Vulnerability Scanners
- **TongdaScan_go**: https://github.com/Fu5r0dah/TongdaScan_go
- **nacosScan**: https://github.com/Whoopsunix/nacosScan
- **SpringBoot-Scan**: https://github.com/AabyssZG/SpringBoot-Scan
- **WeblogicScan**: https://github.com/dr0op/WeblogicScan / https://github.com/rabbitmask/WeblogicScan
- **weblogicScanner**: https://github.com/0xn0ne/weblogicScanner
- **Log4j2Scan**: https://github.com/whwlsfb/Log4j2Scan — Log4j vuln scanner
- **RouteVulScan**: https://github.com/F6JO/RouteVulScan — Router vuln scanner

### OOB / DNS Logging
- **Alphalog**: https://github.com/AlphabugX/Alphalog — dns/http/rmi/ldap
- **DNSLog-GO**: https://github.com/lanyi1998/DNSlog-GO
- **DNS-Shell**: https://github.com/sensepost/DNS-Shell — DNS tunnel shell

### App/Code Recon
- AppInfoScanner: https://github.com/kelvinBen/AppInfoScanner
- dnSpy: https://github.com/dnSpy/dnSpy — .NET decompiler

### System Enumeration (Linux/Windows)
- **SharpScan**: https://github.com/INotGreen/SharpScan — C# intranet scanner
- postenum: https://github.com/mostaphabahadou/postenum — Linux enumeration
- LinEnum: https://github.com/rebootuser/LinEnum — Linux enumeration
- GScan: https://github.com/grayddq/GScan — Linux post-exploit

### Active Directory Recon
- **PowerView**: https://github.com/PowerShellMafia/PowerSploit/blob/dev/Recon/PowerView.ps1
- adidnsdump: https://github.com/dirkjanm/adidnsdump — AD DNS dump

---

## CREDENTIALS / BRUTE FORCE (29 tools)

### Password Cracking
- **thc-hydra**: https://github.com/vanhauser-thc/thc-hydra — Network brute force
- **hashcat**: https://github.com/hashcat/hashcat — GPU password cracking
- **john**: https://github.com/openwall/john — John the Ripper
- Name-That-Hash: https://github.com/HashPals/Name-That-Hash — Hash type ID
- haiti: https://github.com/noraj/haiti — Hash type ID

### JWT Attacks
- jwtcrack: https://github.com/Sjord/jwtcrack
- c-jwt-cracker: https://github.com/brendan-rius/c-jwt-cracker
- jwt_tool: https://github.com/ticarpi/jwt_tool
- jwt-pwn: https://github.com/mazen160/jwt-pwn
- jwt-hack: https://github.com/hahwul/jwt-hack
- jwt.secrets.list: https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list

### Wordlists & Dictionaries
- **SecLists**: https://github.com/danielmiessler/SecLists — 46.4k stars
- SecDictionary: https://github.com/SexyBeast233/SecDictionary
- Dictionary-Of-Pentesting: https://github.com/insightglacier/Dictionary-Of-Pentesting
- PentesterSpecialDict: https://github.com/a3vilc0de/PentesterSpecialDict
- Assetnote wordlists: https://github.com/assetnote/wordlists
- Metasploit wordlists: https://github.com/rapid7/metasploit-framework/tree/master/data/wordlists
- commonspeak2: https://github.com/assetnote/commonspeak2-wordlists/tree/master/wordswithext
- bruteforce-lists: https://github.com/random-robbie/bruteforce-lists
- weakpass: https://github.com/zzzteph/weakpass
- pydictor: https://github.com/LandGrey/pydictor/ — Dictionary generator
- OneListForAll: https://github.com/six2dez/OneListForAll
- top25-parameter: https://github.com/lutfumertceylan/top25-parameter

### Default Credentials
- DefaultCreds-cheat-sheet: https://github.com/ihebski/DefaultCreds-cheat-sheet — 3,468 default passwords

### Secret Scanning
- **gitleaks**: https://github.com/gitleaks/gitleaks — Git secret scanner

### Database Cracking
- DruidCrack: https://github.com/rabbitmask/DruidCrack
- nacosleak: https://github.com/a1phaboy/nacosleak — Nacos credential leak

### App-Specific Decryptors
- CrackMinApp: https://github.com/Cherrison/CrackMinApp
- MobaXterm decrypt: https://github.com/HyperSine/how-does-MobaXterm-encrypt-password
- Navicat decrypt: https://github.com/Zhuoyuan1/navicat_password_decrypt / https://github.com/HyperSine/how-does-navicat-encrypt-password
- Sunflower decrypt: https://github.com/wafinfo/Sunflower_get_Password
- Xmanager decrypt: https://github.com/HyperSine/how-does-Xmanager-encrypt-password (v<7.0)

### Domain Password Attacks
- **CrackMapExec**: https://github.com/byt3bl33d3r/CrackMapExec
- DomainPasswordSpray: https://github.com/dafthack/DomainPasswordSpray
- kerbrute: https://github.com/ropnop/kerbrute

### Other
- arthas: https://github.com/alibaba/arthas — Java diagnostic tool
- Cloud-Bucket-Leak-Detection: https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools

---

## PRIVILEGE ESCALATION (12 tools)

- **PEASS-ng (linpeas)**: https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite
- linpeas.sh: https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
- winPEAS.bat: https://github.com/carlospolop/PEASS-ng/blob/master/winPEAS/winPEASbat/winPEAS.bat
- winPEASexe: https://github.com/peass-ng/PEASS-ng/blob/master/winPEAS/winPEASexe/README.md
- linPEAS source: https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS
- **Windows-Exploit-Suggester**: https://github.com/AonCyberLabs/Windows-Exploit-Suggester
- windows-kernel-exploits: https://github.com/SecWiki/windows-kernel-exploits
- linux-exploit-suggester: https://github.com/The-Z-Labs/linux-exploit-suggester
- **PrivescCheck**: https://github.com/itm4n/PrivescCheck — PowerShell privesc audit
- SeBackupPrivilege: https://github.com/giuliano108/SeBackupPrivilege
- EnableSeBackupPrivilege: https://github.com/gtworek/PSBits/blob/master/Misc/EnableSeBackupPrivilege.ps1
- MS14-068: https://github.com/SecWiki/windows-kernel-exploits/blob/master/MS14-068/pykek/ms14-068.py

---

## LATERAL MOVEMENT (24 tools)

### Execution & Tunneling
- crowbar: https://github.com/galkan/crowbar — SSH key + OpenVPN brute
- nps-auth-bypass: https://github.com/carr0t2/nps-auth-bypass
- ClassHound: https://github.com/LandGrey/ClassHound
- ZeroOmega: https://github.com/zero-peak/ZeroOmega — Proxy SwitchyOmega v3
- NetExec: https://github.com/Pennyw0rth/NetExec
- **impacket**: https://github.com/fortra/impacket — Python AD exploitation library
- slinger: https://github.com/ghost-ng/slinger — Lightweight impacket CLI
- wmiexec-Pro: https://github.com/XiaoliChan/wmiexec-Pro — Evasive WMI exec
- WinPwn: https://github.com/S3cur3Th1sSh1t/WinPwn
- PowerSharpPack: https://github.com/S3cur3Th1sSh1t/PowerSharpPack

### Process/Network Hiding
- libprocesshider: https://github.com/gianlucaborello/libprocesshider — LD_PRELOAD hide Linux process
- Proxychains: https://github.com/haad/proxychains
- tcptunnel: https://github.com/vakuum/tcptunnel — Internal→DMZ→attacker

### Credential Theft
- dpapidump + regsecrets: https://github.com/fortra/impacket/pull/1898 — Win11/Server2022 tested
- FindToDeskPass: https://github.com/yangliukk/FindToDeskPass

### AD-Specific Lateral Movement
- goldenPac.py: https://github.com/fortra/impacket/blob/master/examples/goldenPac.py
- **ProxyLogon**: https://github.com/hausec/ProxyLogon
- proxyshell_rce.py: https://github.com/dmaasland/proxyshell-poc/blob/main/proxyshell_rce.py
- ProxyNotShell-PoC: https://github.com/testanull/ProxyNotShell-PoC
- **ntlmrelayx**: https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py
- findDelegation.py: https://github.com/fortra/impacket/blob/master/examples/findDelegation.py
- rbcd.py: https://github.com/fortra/impacket/blob/master/examples/rbcd.py

### Cloud Storage Tools
- aliyun-cli: https://github.com/aliyun/aliyun-cli — Alibaba Cloud OSS
- kodo-browser: https://github.com/qiniu/kodo-browser — Qiniu Cloud OSS

---

## PERSISTENCE (1 repos)

- **OpenArk**: https://github.com/BlackINT3/OpenArk — Anti-rootkit / persistence detection

---

## ACTIVE DIRECTORY (12 tools)

### Core AD Tools
- domain_hunter_pro: https://github.com/bit4woo/domain_hunter_pro — Domain collection
- pypykatz: https://github.com/skelsec/pypykatz — Pure Python mimikatz

### BloodHound Ecosystem
- **BloodHound**: https://github.com/SpecterOps/BloodHound — AD attack path analysis
- BloodHound.py: https://github.com/dirkjanm/BloodHound.py — Python collector
- SharpHound: https://github.com/BloodHoundAD/SharpHound — C# collector
- BloodHoundQueries: https://github.com/CompassSecurity/BloodHoundQueries
- SharpHound.ps1: https://github.com/SpecterOps/BloodHound-Legacy/blob/master/Collectors/SharpHound.ps1

### LDAP
- ldapdomaindump: https://github.com/dirkjanm/ldapdomaindump
- ldapsearch-ad: https://github.com/yaap7/ldapsearch-ad

### Certificate Services
- **Certipy**: https://github.com/ly4k/Certipy — AD CS exploitation
- ADCSPwn: https://github.com/bats3c/ADCSPwn — AD CS attack tool

### Other AD
- DCSync: https://github.com/n00py/DCSync

---

## CLOUD / KUBERNETES (36 tools)

### Cloud Security Labs
- **TerraformGoat**: https://github.com/HXSecurity/TerraformGoat
- **Kubernetes Goat**: https://github.com/madhuakula/kubernetes-goat
- AWSGoat: https://github.com/ine-labs/AWSGoat
- CloudGoat: https://github.com/RhinoSecurityLabs/cloudgoat
- Awesome-CloudSec-Labs: https://github.com/iknowjason/Awesome-CloudSec-Labs

### Cloud Security References
- awesome-cloud-security: https://github.com/teamssix/awesome-cloud-security
- lzCloudSecurity: https://github.com/EvilAnne/lzCloudSecurity

### Cloud Bug Bounty/Legal
- Awesome-Laws: https://github.com/Threekiii/Awesome-Laws

### Cloud Testing Tools
- cloudsword: https://github.com/wgpsec/cloudsword — Cloud service security testing
- CloudExplorer-Lite: https://github.com/CloudExplorer-Dev/CloudExplorer-Lite
- alicloud-tools: https://github.com/iiiusky/alicloud-tools — Alibaba Cloud security tools
- cloudSec: https://github.com/libaibaia/cloudSec — Multi-cloud web tool
- aksk_tool: https://github.com/wyzxxz/aksk_tool — Multi-cloud AK/SK tool
- cloudTools: https://github.com/dark-kingA/cloudTools — Multi-cloud security tools

### Tencent Cloud
- cosbrowser: https://github.com/TencentCloud/cosbrowser — COS browser
- tencentcloud-cli: https://github.com/TencentCloud/tencentcloud-cli
- Tencent_Yun_tools: https://github.com/freeFV/Tencent_Yun_tools

### Alibaba Cloud
- aliyun-cli: https://github.com/aliyun/aliyun-cli
- oss-browser: https://github.com/aliyun/oss-browser — GUI for OSS
- aliyun-accesskey-Tools: https://github.com/mrknow001/aliyun-accesskey-Tools
- AliyunAccessKeyTools: https://github.com/NS-Sp4ce/AliyunAccessKeyTools

### Docker
- dive: https://github.com/wagoodman/dive — Docker image layer analysis
- docker-bench-security: https://github.com/docker/docker-bench-security — Docker CIS benchmark
- dagda: https://github.com/eliasgranderubio/dagda/ — Docker image static analysis

### Kubernetes
- minikube: https://github.com/kubernetes/minikube — Local K8s cluster
- kind: https://github.com/kubernetes-sigs/kind — Docker-based K8s
- kubeadm: https://github.com/kubernetes/kubeadm — K8s deployment
- cri-tools: https://github.com/kubernetes-sigs/cri-tools — Kubelet CRI tools
- k9s: https://github.com/derailed/k9s — K8s terminal management
- etcd: https://github.com/etcd-io/etcd — K8s core component

### Kubernetes Red Team
- red-kube: https://github.com/lightspin-tech/red-kube — K8s red team tool
- KubeHound: https://github.com/DataDog/KubeHound — K8s attack path analysis
- peirates: https://github.com/inguardians/peirates — K8s penetration testing
- kube-bench: https://github.com/aquasecurity/kube-bench — K8s CIS benchmark
- kube-hunter: https://github.com/aquasecurity/kube-hunter — K8s weakness scanner

### Container Escape
- container-escape-check: https://github.com/teamssix/container-escape-check
- awesome-container-escape: https://github.com/brant-ruan/awesome-container-escape
- CDK: https://github.com/cdk-team/CDK — Container pentest toolkit
- veinmind-tools: https://github.com/chaitin/veinmind-tools — Container security

### Cloud Self-Hosted
- cloudreve: https://github.com/cloudreve/Cloudreve — Self-hosted multi-cloud file manager
- HummerRisk: https://github.com/HummerRisk/HummerRisk — Cloud-native security platform

---

## EVASION / OPSEC (6 tools)

- 403bypasser: https://github.com/yunemse48/403bypasser
- CVE-2021-44228-PoC-log4j-bypass-words: https://github.com/Puliczek/CVE-2021-44228-PoC-log4j-bypass-words
- bypassAV: https://github.com/pureqh/bypassAV
- GolangBypassAV: https://github.com/safe6Sec/GolangBypassAV
- BypassAntiVirus: https://github.com/TideSec/BypassAntiVirus
- AV_Evasion_Tool: https://github.com/1y0n/AV_Evasion_Tool

---

## SOCIAL ENGINEERING (1 repos)

- **gophish**: https://github.com/gophish/gophish — Open-source phishing toolkit

For comprehensive SE, see also the social-engineering-wireless skill.

---

## EXPLOITS / POC (43 repos)

### POC Collections
- POC: https://github.com/wy876/POC
- vulnerability: https://github.com/lal0ne/vulnerability
- POChouse: https://github.com/DawnFlame/POChouse
- Some-PoC-oR-ExP: https://github.com/coffeehb/Some-PoC-oR-ExP
- Library-POC: https://github.com/luck-ying/Library-POC
- Penetration_Testing_POC: https://github.com/Mr-xn/Penetration_Testing_POC
- PoC-in-GitHub: https://github.com/nomi-sec/PoC-in-GitHub
- PocOrExp_in_Github: https://github.com/ycdxsb/PocOrExp_in_Github
- 0day: https://github.com/helloexp/0day
- cve: https://github.com/trickest/cve
- xpoc: https://github.com/chaitin/xpoc

### JNDI/Java Exploitation
- JNDIExploit: https://github.com/vulhub/JNDIExploit
- JNDI-Injection-Exploit: https://github.com/welk1n/JNDI-Injection-Exploit
- JNDIExploit (WhiteHSBG): https://github.com/WhiteHSBG/JNDIExploit
- JNDInjector: https://github.com/rebeyond/JNDInjector
- attackRmi: https://github.com/A-D-Team/attackRmi

### Redis
- redis-rce: https://github.com/Ridter/redis-rce
- RedisEXP: https://github.com/yuyan-sec/RedisEXP
- RedisStudio: https://github.com/cinience/RedisStudio
- AnotherRedisDesktopManager: https://github.com/qishibo/AnotherRedisDesktopManager
- redis-rogue-server: https://github.com/n0b0dyCN/redis-rogue-server
- RedisWriteFile: https://github.com/r35tart/RedisWriteFile

### Specific Product Exploits
- ds_store_exp: https://github.com/lijiejie/ds_store_exp — .DS_Store info leak
- OA-EXPTOOL: https://github.com/LittleBear4/OA-EXPTOOL
- fastjson-exp: https://github.com/amaz1ngday/fastjson-exp
- CVE-2021-22205: https://github.com/Al1ex/CVE-2021-22205/
- NacosRce: https://github.com/c0olw/NacosRce/
- NacosExploitGUI: https://github.com/charonlight/NacosExploitGUI
- shiro_rce_tool: https://github.com/wyzxxz/shiro_rce_tool
- ShiroExploit: https://github.com/feihong-cs/ShiroExploit-Deprecated
- ShiroExp: https://github.com/safe6Sec/ShiroExp
- SpringBootVulExploit: https://github.com/LandGrey/SpringBootVulExploit
- Spring_All_Reachable: https://github.com/savior-only/Spring_All_Reachable — CVE-2022-22947/22963
- swagger-exp: https://github.com/lijiejie/swagger-exp
- CVE-2020-1938 Tomcat AJP: https://github.com/YDHCUI/CNVD-2020-10487-Tomcat-Ajp-lfi
- CVE-2020-14882 WebLogic: https://github.com/zhzyker/exphub/blob/master/weblogic/cve-2020-14882_rce.py
- API-Explorer: https://github.com/mrknow001/API-Explorer — AK/SK tool
- Linux_Exploit_Suggester: https://github.com/InteliSecureLabs/Linux_Exploit_Suggester
- SOAPHound: https://github.com/FalconForceTeam/SOAPHound

### Zerologon & PrintNightmare
- zerologon (SecuraBV): https://github.com/SecuraBV/CVE-2020-1472/blob/master/zerologon_tester.py
- zerologon (dirkjanm): https://github.com/dirkjanm/CVE-2020-1472
- zerologon (Potato): https://github.com/Potato-py/Potato/tree/03c3551e4770db440b27b0a48fc02b0a38a1cf04/exp/cve/CVE-2020-1472
- CVE-2021-1675 PrintNightmare: https://github.com/cube0x0/CVE-2021-1675 / https://github.com/calebstewart/CVE-2021-1675
- PrintNightmare-CVE-2021-34527: https://github.com/nemo-wq/PrintNightmare-CVE-2021-34527

### Coercion Tools
- **DFSCoerce**: https://github.com/Wh04m1001/DFSCoerce
- WSPCoerce: https://github.com/slemire/WSPCoerce
- ShadowCoerce: https://github.com/ShutdownRepo/ShadowCoerce
- Coercer: https://github.com/p0dalirius/Coercer

---

## LABS / TRAINING (10 repos)

- **echoCTF**: https://github.com/echoCTF/echoCTF.RED — CTF platform
- Sqli-labs: https://github.com/Audi-1/sqli-labs
- Upload-labs: https://github.com/c0ny1/upload-labs
- Xss-labs: https://github.com/do0dl3/xss-labs
- encrypt-labs: https://github.com/SwagXz/encrypt-labs — AES/DES/RSA
- **GOAD** (Game of Active Directory): https://github.com/Orange-Cyberdefense/GOAD
- DVWA: https://github.com/digininja/DVWA
- WebGoat: https://github.com/WebGoat/WebGoat
- Vulfocus: https://github.com/fofapro/vulfocus
- Vulstudy: https://github.com/c0ny1/vulstudy — 17 vuln platforms on Docker

### AD Lab Builders
- BadBlood: https://github.com/davidprowe/BadBlood — Creates example AD environment
- badPods: https://github.com/BishopFox/badPods
- Metarget: https://github.com/Metarget/metarget
- IoT-vulhub: https://github.com/firmianay/IoT-vulhub

---

## REVERSE ENGINEERING (5 repos)

- php-malware-finder: https://github.com/jvoisin/php-malware-finder
- **IDA Pro MCP**: https://github.com/mrexodia/ida-pro-mcp — AI-integrated IDA Pro
- android-reverse: https://github.com/WuFengXue/android-reverse
- IDAGolangHelper: https://github.com/sibears/IDAGolangHelper — Golang reversing
- AntiDebug_Breaker: https://github.com/0xsdeo/AntiDebug_Breaker

---

## CRYPTO / ENCODING (7 repos)

- CaptfEncoder: https://github.com/guyoung/CaptfEncoder
- hutool-crypto: https://github.com/dromara/hutool — Symmetric/asymmetric/digest
- GmSSL: https://github.com/guanzhi/GmSSL — SM2/SM3/SM4/SM9/SSL
- gmssl-python: https://github.com/gongxian-ding/gmssl-python — SM2/SM3/SM4/SM9
- ncDecode: https://github.com/1amfine2333/ncDecode — Yonyou NC decrypt
- PassDecode-jar: https://github.com/Rvn0xsy/PassDecode-jar — FanRuan/Seeyon decrypt
- **BurpCrypto**: https://github.com/whwlsfb/BurpCrypto — AES/RSA/DES/ExecJs in Burp

---

## OTHER TOOLS (298+ repos)

### Terminal / Shell Tools
- **ohmyzsh**: https://github.com/ohmyzsh/ohmyzsh — zsh enhancement
- clink: https://github.com/chrisant996/clink — cmd.exe enhancement
- rlwrap: https://github.com/hanslub42/rlwrap — readline wrapper
- tabby: https://github.com/Eugeny/tabby — Windows terminal
- **Warp**: https://github.com/warpdotdev/Warp — Mac terminal
- zellij: https://github.com/zellij-org/zellij — Terminal multiplexer
- tmux: https://github.com/tmux — Terminal multiplexer
- anew: https://github.com/tomnomnom/anew — Append new lines, skip dupes
- ripgrep: https://github.com/BurntSushi/ripgrep — Fast line search
- the-art-of-command-line: https://github.com/jlevy/the-art-of-command-line
- linux-command: https://github.com/jaywcjlove/linux-command — Online query
- pls: https://github.com/chenjiandongx/pls — Go command helper
- how: https://github.com/chenjiandongx/how — Python command helper

### Recon/Analysis Platforms
- **CyberChef**: https://github.com/gchq/CyberChef — Data transformation
- Ciphey: https://github.com/Ciphey/Ciphey — Auto decryption
- any-rule: https://github.com/any86/any-rule — Regex collection
- oktools: https://github.com/wangyiwy/oktools

### Scan & Discovery Frameworks
- **OneForAll**: https://github.com/shmilylty/OneForAll — Subdomain collection
- ShuiZe: https://github.com/0x727/ShuiZe_0x727 — Info gathering
- FofaX: https://github.com/xiecat/fofax — Fofa client
- Fofa Viewer: https://github.com/wgpsec/fofa_viewer
- EHole: https://github.com/EdgeSecurityTeam/EHole / https://github.com/lemonlove7/EHole_magic
- ObserverWard: https://github.com/0x727/ObserverWard
- dismap: https://github.com/zhzyker/dismap
- Kunyu: https://github.com/knownsec/Kunyu
- dddd: https://github.com/SleepingBag945/dddd
- AlliN: https://github.com/P1-Team/AlliN

### WAF Detection
- identYwaf: https://github.com/stamparm/identYwaf
- wafw00f: https://github.com/EnableSecurity/wafw00f

### Directory/File Brute Force
- gobuster: https://github.com/OJ/gobuster
- dirsearch: https://github.com/maurosoria/dirsearch
- dirmap: https://github.com/H4ckForJob/dirmap
- ffuf: https://github.com/ffuf/ffuf
- legba: https://github.com/evilsocket/legba/
- Arjun: https://github.com/s0md3v/Arjun — Parameter discovery

### Web Crawlers
- gospider: https://github.com/jaeles-project/gospider
- URLFinder: https://github.com/pingc0y/URLFinder

### Network Tools
- hping: https://github.com/antirez/hping
- misp-warninglists: https://github.com/MISP/misp-warninglists

### Phishing
- theHarvester: https://github.com/laramies/theHarvester — Also does subdomain
- SpoofWeb: https://github.com/5icorgi/SpoofWeb — Deploy phishing sites

### Vulnerability Scanners
- **xray**: https://github.com/chaitin/xray
- vulmap: https://github.com/zhzyker/vulmap
- afrog: https://github.com/zan8in/afrog
- gamma-gui: https://github.com/zeoxisca/gamma-gui
- zkar: https://github.com/phith0n/zkar

### Java Deserialization
- **ysoserial** (original): https://github.com/frohoff/ysoserial
- ysoserial (Y4er): https://github.com/Y4er/ysoserial
- ysomap: https://github.com/wh1t3p1g/ysomap
- marshalsec: https://github.com/mbechler/marshalsec
- JYso: https://github.com/qi4L/JYso
- ysoserial (DeEpinGh0st): https://github.com/DeEpinGh0st/ysoserial
- web-chains: https://github.com/Java-Chains/web-chains

### PHP Deserialization
- **phpggc**: https://github.com/ambionics/phpggc — PHP gadget chains

### Database Exploitation
- MDUT: https://github.com/SafeGroceryStore/MDUT — Multi-database exploit tool
- mysql-fake-server: https://github.com/4ra1n/mysql-fake-server
- evil-mysql-server: https://github.com/dushixiang/evil-mysql-server
- MySQL_Fake_Server: https://github.com/fnmsd/MySQL_Fake_Server
- odat: https://github.com/quentinhardy/odat — Oracle attack (RCE)
- SharpSQLTools: https://github.com/uknowsec/SharpSQLTools
- PySQLTools: https://github.com/Ridter/PySQLTools

### Git/Repo Exploitation
- **trufflehog**: https://github.com/trufflesecurity/trufflehog — Find/verify leaked credentials
- git-dumper: https://github.com/arthaud/git-dumper
- dvcs-ripper: https://github.com/kost/dvcs-ripper — .svn/.hg/.cvs
- Hawkeye: https://github.com/0xbug/Hawkeye — GitHub sensitive info monitor
- Apt_t00ls: https://github.com/White-hua/Apt_t00ls

### OA/Product Specific
- DecryptTools: https://github.com/wafinfo/DecryptTools — 22 crypto methods
- ezOFFICE_Decrypt: https://github.com/wafinfo/ezOFFICE_Decrypt
- LandrayDES: https://github.com/zhutougg/LandrayDES — Landray OA decrypt
- druid_sessions: https://github.com/yuyan-sec/druid_sessions

### Java Debugging
- jdwp-shellifier (py2): https://github.com/IOActive/jdwp-shellifier
- jdwp-shellifier: https://github.com/Lz1y/jdwp-shellifier

### Shiro
- shiro_attack: https://github.com/j1anFen/shiro_attack
- shiro_key: https://github.com/yanm1e/shiro_key — 1000+ keys

### Struts
- Struts2VulsTools: https://github.com/shack2/Struts2VulsTools

### Heap Dump Analysis
- heapdump_tool: https://github.com/wyzxxz/heapdump_tool
- JDumpSpider: https://github.com/whwlsfb/JDumpSpider

### ThinkPHP
- ThinkphpGUI: https://github.com/Lotus6/ThinkphpGUI
- thinkphp_gui_tools: https://github.com/bewhale/thinkphp_gui_tools

### WebLogic
- WeblogicTool: https://github.com/KimJun1010/WeblogicTool
- weblogic-framework: https://github.com/sv3nbeast/weblogic-framework

### vCenter
- VcenterKiller: https://github.com/Schira4396/VcenterKiller
- VcenterKit: https://github.com/W01fh4cker/VcenterKit
- vcenter_saml_login: https://github.com/horizon3ai/vcenter_saml_login — Extract IdP cert

### WebSocket
- wscat: https://github.com/websockets/wscat

### Burp Extensions
- **Yakit**: https://github.com/yaklang/yakit — Security platform
- FindSomething: https://github.com/ResidualLaugh/FindSomething — Find in JS/source
- Hack Bar: https://github.com/0140454/hackbar
- Cookie-Editor: https://github.com/Moustachauve/cookie-editor
- Disable JavaScript: https://github.com/dpacassi/disable-javascript
- Heimdallr: https://github.com/Ghr07h/Heimdallr — Honeypot detection
- anti-honeypot: https://github.com/cnrstar/anti-honeypot
- immersive-translate: https://github.com/immersive-translate/immersive-translate/
- json-formatter: https://github.com/callumlocke/json-formatter
- markdown-viewer: https://github.com/simov/markdown-viewer
- **HaE**: https://github.com/gh0stkey/HaE — Highlight and extract
- BurpAppletPentester: https://github.com/mrknow001/BurpAppletPentester — SessionKey decrypt
- HaeToYakit: https://github.com/youmulijiang/HaeToYakit

### Tabby / SCA
- **tabby**: https://github.com/wh1t3p1g/tabby — Static code analysis

### 403/401 Bypass
- byp4xx: https://github.com/lobuhi/byp4xx
- 4-ZERO-3: https://github.com/Dheerajmadhukar/4-ZERO-3
- nomore403: https://github.com/devploit/nomore403

### LFI
- lfimap: https://github.com/hansmach1ne/lfimap
- liffy: https://github.com/mzfr/liffy

### Gopher/SSRF
- Gopherus (py2): https://github.com/tarunkant/Gopherus
- Gopherus3 (py3): https://github.com/Esonhugh/Gopherus3

### Mini Programs / APK
- wxappUnpacker: https://github.com/xuedingmiaojun/wxappUnpacker
- e0e1-wx: https://github.com/eeeeeeeeee-code/e0e1-wx
- wxapkg: https://github.com/wux1an/wxapkg
- Apktool: https://github.com/iBotPeaches/Apktool
- wx_sessionkey_decrypt: https://github.com/mrknow001/wx_sessionkey_decrypt

### Code Generation / Obfuscation
- PHPFuck: https://github.com/splitline/PHPFuck
- yetAnotherObfuscator: https://github.com/0xb11a1/yetAnotherObfuscator

### Infrastructure
- f8x: https://github.com/ffffffff0x/f8x — Red/Blue team automation
- openvpn-install: https://github.com/hwdsl2/openvpn-install
- updog: https://github.com/sc0tfree/updog — HTTP/S upload/download

### Collaboration
- mattermost: https://github.com/mattermost/mattermost
- Rocket.Chat: https://github.com/RocketChat/Rocket.Chat
- codimd: https://github.com/hackmdio/codimd
- hedgedoc: https://github.com/hedgedoc/hedgedoc

### Internal Information Gathering
- **SharpHunter**: https://github.com/lintstar/SharpHunter — Auto host info collection
- netspy: https://github.com/shmilylty/netspy — Internal network probe
- SharpHostInfo: https://github.com/shmilylty/SharpHostInfo
- smbmap: https://github.com/ShawnDEvans/smbmap — SMB enumeration

### Credential Dumping
- **LaZagne**: https://github.com/AlessandroZ/LaZagne — Multi-app password recovery
- Pillager: https://github.com/qwqdanchun/Pillager/
- searchall: https://github.com/Naturehi666/searchall
- DonPAPI: https://github.com/login-securite/DonPAPI
- SharpDPAPI: https://github.com/GhostPack/SharpDPAPI
- dploot: https://github.com/zblurx/dploot — DPAPI
- lsassy: https://github.com/login-securite/lsassy — LSASS dump

### Browser Credentials
- **HackBrowserData**: https://github.com/moonD4rk/HackBrowserData
- BrowserGhost: https://github.com/QAX-A-Team/BrowserGhost
- firefox_decrypt: https://github.com/unode/firefox_decrypt

### Remote Desktop Tools Creds
- sundeskQ: https://github.com/milu001/sundeskQ — Sunflower + ToDesk
- securreCRT: https://github.com/depau/shcrt
- SharpDecryptPwd: https://github.com/RowTeam/SharpDecryptPwd
- SharpXDecrypt: https://github.com/JDArmy/SharpXDecrypt

### Metasploit Ecosystem
- **metasploit-framework**: https://github.com/rapid7/metasploit-framework

### Kerberos
- **Rubeus**: https://github.com/GhostPack/Rubeus
- Powermad: https://github.com/Kevin-Robertson/Powermad

### PowerShell Collections
- PowerSploit: https://github.com/PowerShellMafia/PowerSploit
- nishang: https://github.com/samratashok/nishang

### Multi-Purpose
- Ladon: https://github.com/k8gege/Ladon — Multi-function scanner
- Erebus: https://github.com/DeEpinGh0st/Erebus
- LSTAR: https://github.com/lintstar/LSTAR
- ElevateKit: https://github.com/rsmudge/ElevateKit — CobaltStrike UAC bypass

### Proxy & Tunneling
- pystinger: https://github.com/FunnyWolf/pystinger
- **LOLBAS**: https://github.com/LOLBAS-Project/LOLBAS-Project.github.io — Living off the land binaries
- **GTFOBins**: https://github.com/GTFOBins/GTFOBins.github.io — Unix binary exploitation

### C2 / Webshell Management
- GodzillaMemoryShellProject: https://github.com/BeichenDream/GodzillaMemoryShellProject
- jmg-for-Godzilla: https://github.com/1ucky7/jmg-for-Godzilla
- Behinder: https://github.com/rebeyond/Behinder
- Godzilla: https://github.com/BeichenDream/Godzilla
- skyscorpion: https://github.com/shack2/skyscorpion
- Platypus: https://github.com/WangYihang/Platypus

### Reverse Shell
- pwncat: https://github.com/calebstewart/pwncat — Python 3.9+
- pspy: https://github.com/DominicBreuker/pspy — Monitor Linux processes
- hoaxshell: https://github.com/t3l3machus/hoaxshell

### Payload Development
- SharpCollection: https://github.com/Flangvik/SharpCollection
- MailSniper: https://github.com/dafthack/MailSniper

### Privesc
- wesng: https://github.com/bitsadmin/wesng — Windows Exploit Suggester NG
- WindowsElevation: https://github.com/Al1ex/WindowsElevation
- BadPotato: https://github.com/BeichenDream/BadPotato/
- Kernelhub: https://github.com/Ascotbe/Kernelhub
- traitor: https://github.com/liamg/traitor — Linux privesc

### Linux Kernel
- linux_kernel_hacking: https://github.com/xcellerator/linux_kernel_hacking

### Python Embedded
- rpeloader: https://github.com/Teach2Breach/rpeloader — Python on Windows without install

### Proxy / Tunnel Tools
- **frp**: https://github.com/fatedier/frp — Fast reverse proxy
- frpModify: https://github.com/uknowsec/frpModify
- **suo5**: https://github.com/zema1/suo5 — HTTP tunnel
- Stowaway: https://github.com/ph4ntonn/Stowaway — Multi-level proxy
- Neo-reGeorg: https://github.com/L-codes/Neo-reGeorg
- nps: https://github.com/ehang-io/nps
- reGeorg: https://github.com/sensepost/reGeorg
- rakshasa: https://github.com/Mob2003/rakshasa
- Viper: https://github.com/FunnyWolf/Viper
- **ligolo-ng**: https://github.com/nicocha30/ligolo-ng — TUN interface
- gost: https://github.com/ginuerzh/gost — GO simple tunnel
- iodine: https://github.com/yarrick/iodine — DNS tunnel
- icmpsh: https://github.com/bdamele/icmpsh — ICMP tunnel

### AD Analysis Tools
- AD_Miner: https://github.com/AD-Security/AD_Miner
- RustHound: https://github.com/NH-RED-TEAM/RustHound
- Adinfo: https://github.com/lzzbb/Adinfo
- SharpADWS: https://github.com/wh0amitz/SharpADWS — ADWS protocol
- ldeep: https://github.com/franc-pentest/ldeep
- sccmhunter: https://github.com/garrettfoster13/sccmhunter
- SharpSCCM: https://github.com/Mayyhem/SharpSCCM
- bloodyAD: https://github.com/CravateRouge/bloodyAD

### AD Attack Automation
- noPac: https://github.com/Ridter/noPac
- zerologon-Shot: https://github.com/XiaoliChan/zerologon-Shot
- zerologon (risksense): https://github.com/risksense/zerologon
- privexchange: https://github.com/dirkjanm/privexchange/
- PTH_Exchange: https://github.com/Jumbo-WJB/PTH_Exchange

### NTLM Relay / Coercion
- **PetitPotam**: https://github.com/topotam/PetitPotam
- PrinterBug: https://github.com/leechristensen/SpoolSample
- PrivExchange: https://github.com/dirkjanm/privexchange/
- **Responder**: https://github.com/lgandx/Responder
- Responder-Windows: https://github.com/lgandx/Responder-Windows

### Kerberos Relay
- KrbRelayUp: https://github.com/Dec0ne/KrbRelayUp
- kerbrelayx: https://github.com/dirkjanm/krbrelayx
- SharpRBCD: https://github.com/Kryp7os/SharpRBCD
- Delegations: https://github.com/TheManticoreProject/Delegations

### AD CS
- **Certify**: https://github.com/GhostPack/Certify
- certi: https://github.com/zer1t0/certi
- PKINITtools: https://github.com/dirkjanm/PKINITtools
- PassTheCert: https://github.com/AlmondOffSec/PassTheCert

### Kerberoasting / Delegation
- pywhisker: https://github.com/ShutdownRepo/pywhisker
- targetedKerberoast: https://github.com/ShutdownRepo/targetedKerberoast
- copagent: https://github.com/LandGrey/copagent

### Blue Team / Detection
- BlueTeamTools: https://github.com/abc123info/BlueTeamTools
- Benchmarks: https://github.com/AV1080p/Benchmarks
- Shell_Script: https://github.com/xiaoyunjie/Shell_Script
- security_check: https://github.com/ppabc/security_check
- linux (T0xst): https://github.com/T0xst/linux
- LinuxCheck: https://github.com/al0ne/LinuxCheck
- Decryption-Tools: https://github.com/jiansiting/Decryption-Tools

### Honeypots
- awesome-honeypots: https://github.com/paralax/awesome-honeypots
- HFish: https://github.com/hacklcx/HFish
- conpot: https://github.com/mushorg/conpot — ICS/SCADA honeypot
- MysqlHoneypot: https://github.com/qigpig/MysqlHoneypot — MySQL honeypot for WeChat ID
- Ehoney: https://github.com/seccome/Ehoney

### Binary Analysis
- **Angr**: https://github.com/angr/angr — Binary analysis platform
- UPX: https://github.com/upx/upx
- checksec: https://github.com/slimm609/checksec
- Detect-It-Easy: https://github.com/horsicq/Detect-It-Easy
- ExeinfoPE: https://github.com/ExeinfoASL/ASL

### Java/Android Reversing
- **jadx**: https://github.com/skylot/jadx
- GDA: https://github.com/charles2gan/GDA-android-reversing-Tool
- jd-gui: https://github.com/java-decompiler/jd-gui
- jar-analyzer: https://github.com/jar-analyzer/jar-analyzer/
- scrcpy: https://github.com/Genymobile/scrcpy — Android screen mirroring

### Python Reverse Engineering
- pyinstaller: https://github.com/pyinstaller/pyinstaller — py→exe
- unpy2exe: https://github.com/matiasb/unpy2exe — exe→pyc
- pyinstxtractor: https://github.com/extremecoders-re/pyinstxtractor — exe→pyc
- python-uncompyle6: https://github.com/rocky/python-uncompyle6/ — pyc→py
- pycDcode: https://github.com/BarakAharoni/pycDcode

### Go/Rust Reversing
- golang_loader_assist: https://github.com/strazzere/golang_loader_assist
- rust-reversing-helper: https://github.com/cha5126568/rust-reversing-helper

### FastJson
- FastJsonParty: https://github.com/lemono0/FastJsonParty

### Database Tools
- Databasetools: https://github.com/Hel10-Web/Databasetools

### PPL / Protected Process
- PPLdump: https://github.com/itm4n/PPLdump — Protected Process LSASS read

### Large Language Model Knowledge
- 404StarLink: https://github.com/knownsec/404StarLink — Security knowledge graph
- 1earn: https://github.com/ffffffff0x/1earn
- Mindmap: https://github.com/Ignitetechnologies/Mindmap/ — Security mind maps
- WADComs: https://github.com/WADComs/WADComs.github.io — Windows/AD cheat sheet
- Red-team-Interview-Questions: https://github.com/HadessCS/Red-team-Interview-Questions
- Blue-Team-Notes: https://github.com/Purp1eW0lf/Blue-Team-Notes
- OPSEC-Tradecraft: https://github.com/WesleyWong420/OPSEC-Tradecraft
- google-hacking-assistant: https://github.com/Pa55w0rd/google-hacking-assistant — Chrome extension

### Emulation
- QEMU: https://github.com/qemu/qemu
- UTM: https://github.com/utmapp/UTM

### Windows Subsystem
- Windows-Crunch: https://github.com/shadwork/Windows-Crunch

---

---

## H4CKER EXHAUSTIVE EXPANSION — 16 Additional Domains

Source: The-Art-of-Hacking/h4cker by Omar Santos. 1,722 unique GitHub repositories (from 15,739 total link matches across 56,038 lines) covering 16 security domains. Every link preserved.

**Complete catalog available via skill references:**
- `skill_view(name='awesome-redteam-toolkit', file_path='references/h4cker-exhaustive-repos.md')` — Part 1: Exploit Dev, Post-Exploitation, Recon, Defense Evasion (~800 repos)
- `skill_view(name='awesome-redteam-toolkit', file_path='references/h4cker-exhaustive-repos-pt2.md')` — Part 2: Web Attacks, Privilege Escalation, Network Attacks, Cryptography, Social Engineering, Wireless/RF, Cloud, Mobile, IoT, Forensics, Governance, AI Security (~922 repos)
- Raw extraction: `/root/killer-queen-knowledge/h4cker_skill_simple.txt` (all 1,722 repos)
- Full source: `/root/killer-queen-knowledge/h4cker-exhaustive.md` (56,038 lines, 15,739 link matches)

### Distribution by Domain

| Domain | Repos | Source Lines |
|--------|-------|-------------|
| Exploit Development | 365 | 1-2,184 |
| Post-Exploitation | 381 | 2,185-4,992 |
| Recon / Enumeration | 378 | 4,993-8,199 |
| Defense Evasion | 134 | 8,200-11,252 |
| Web Attacks | 453 | 14,330-20,755 |
| Privilege Escalation | 2 | 11,253-14,329 |
| Network Attacks | 3 | 20,756-22,529 |
| Cryptography | 0 | 22,530-28,694 |
| Social Engineering | 0 | 28,695-29,714 |
| Wireless / RF | 2 | 29,715-35,408 |
| Cloud Security | 0 | 35,409-38,775 |
| Mobile Security | 1 | 38,776-41,788 |
| IoT / Embedded | 0 | 41,789-46,940 |
| Forensics / IR | 1 | 46,941-49,588 |
| Governance / Compliance | 0 | 49,589-52,041 |
| AI Security | 2 | 52,042-56,038 |
| **TOTAL** | **1,722** | **56,038 lines** |

Note: Domains with 0 repos in the Tools section contain their GitHub links within Techniques/Knowledge sections, which are captured in the complete extraction above.

### Key Repos Sampled Across All Domains

Red teaming LLMs, prompt injection, adversarial ML, AI supply chain.

| Tool | Repo | Notes |
|------|------|-------|
| PyRIT (Microsoft) | https://github.com/Azure/PyRIT | AI red teaming framework |
| Garak (NVIDIA) | https://github.com/NVIDIA/garak | LLM vulnerability scanner |
| Promptfoo | https://github.com/promptfoo/promptfoo | LLM testing & red teaming |
| PurpleLlama (Meta) | https://github.com/facebookresearch/PurpleLlama | AI security toolkit |
| NeMo Guardrails | https://github.com/NVIDIA/NeMo-Guardrails | LLM safety guardrails |
| Rebuff (ProtectAI) | https://github.com/protectai/rebuff | Prompt injection detection |
| LLM Guard | https://github.com/protectai/llm-guard | Input/output sanitization |
| Vigil LLM | https://github.com/deadbits/vigil-llm | Prompt injection/jailbreak detection |
| ART (Adversarial Robustness Toolbox) | https://github.com/Trusted-AI/adversarial-robustness-toolbox | Adversarial ML library |
| Foolbox | https://github.com/bethgelab/foolbox | Adversarial attacks on NNs |
| TextAttack | https://github.com/QData/TextAttack | NLP adversarial attacks |
| DeepSec | https://github.com/ryderling/DEEPSEC | ML security evaluation |
| Armory | https://github.com/twosixlabs/armory | Adversarial robustness eval |
| PromptInject | https://github.com/agencyenterprise/promptinject | Prompt injection framework |
| Awesome Prompt Injection | https://github.com/FonduAI/awesome-prompt-injection | Prompt injection catalogue |
| Prompt Injection Everywhere | https://github.com/TakSec/Prompt-Injection-Everywhere | Comprehensive PI resource |
| DefenseClaw (Cisco) | https://github.com/cisco-ai-defense/defenseclaw | AI defense toolkit |
| CoSAI Secure AI Tooling | https://github.com/cosai-oasis/secure-ai-tooling | AI risk map & controls |
| CoSAI WS3 Governance | https://github.com/cosai-oasis/ws3-ai-risk-governance | AI risk governance |
| Guardrails AI | https://github.com/guardrails-ai/guardrails | Guardrail framework |
| Semgrep AI Rules | https://github.com/semgrep/semgrep-rules | AI detection rules |
| MTEB Benchmark | https://github.com/embeddings-benchmark/mteb | Embedding model benchmark |
| Haystack | https://github.com/deepset-ai/haystack | NLP pipeline framework |
| LangChain | https://github.com/LangChain-ai/LangChain | LLM application framework |
| Embedchain | https://github.com/embedchain/embedchain | Chatbot over datasets |
| OpenLLMetry | https://github.com/traceloop/openllmetry | LLM observability |
| CrewAI | https://github.com/crewAIInc/crewAI | Multi-agent AI orchestration |
| Outlines | https://github.com/normal-computing/outlines | Constrained text generation |
| RAG for Cybersecurity | https://github.com/santosomar/RAG-for-cybersecurity | RAG training materials |

### MOBILE SECURITY (3,013 lines)

Android/iOS app analysis, reversing, exploitation.

| Tool | Repo | Notes |
|------|------|-------|
| jadx | https://github.com/skylot/jadx | Java/Android decompiler |
| GDA | https://github.com/charles2gan/GDA-android-reversing-Tool | Android reversing |
| Apktool | https://github.com/iBotPeaches/Apktool | APK reverse engineering |
| scrcpy | https://github.com/Genymobile/scrcpy | Android screen mirroring |
| wxappUnpacker | https://github.com/xuedingmiaojun/wxappUnpacker | WeChat miniapp unpacker |
| Android Reverse | https://github.com/WuFengXue/android-reverse | Android reversing guide |
| wxapkg | https://github.com/wux1an/wxapkg | WeChat miniapp unpacker |
| e0e1-wx | https://github.com/eeeeeeeeee-code/e0e1-wx | WeChat tools |

### IoT / EMBEDDED (5,152 lines)

Firmware analysis, ICS/SCADA, automotive, hardware hacking.

| Tool | Repo | Notes |
|------|------|-------|
| binwalk (ReFirmLabs) | https://github.com/ReFirmLabs/binwalk | Firmware analysis |
| Firmware Reverse Engineering Workshop | https://github.com/emproof-com/workshop_firmware_reverse_engineering | Training materials |
| RHme 2016 | https://github.com/Riscure/Rhme-2016 | Embedded CTF challenges |
| RHme 2017 | https://github.com/Riscure/Rhme-2017 | Embedded CTF challenges |
| Caring Caribou | https://github.com/CaringCaribou/caringcaribou | Vehicle security scanner |
| CanCat | https://github.com/atlas0fd00m/CanCat | CAN bus swiss-army knife |
| CANalyzat0r | https://github.com/schutzwerk/CANalyzat0r | CAN analysis toolkit |
| CANdevStudio | https://github.com/GENIVI/CANdevStudio | CAN bus simulation |
| SocketCAN Utils | https://github.com/linux-can/can-utils | Linux CAN utilities |
| Python-CAN | https://github.com/hardbyte/python-can | Python CAN interface |
| cantools | https://github.com/eerimoq/cantools | CAN message decode/encode |
| canmatrix | https://github.com/ebroecker/canmatrix | CAN matrix library |
| UDSim | https://github.com/zombieCraig/UDSim | UDS ECU simulator |
| CANToolz | https://github.com/eik00d/CANToolz | CAN analysis framework |
| openpilot (comma.ai) | https://github.com/commaai/openpilot | Driving agent |
| openalpr | https://github.com/openalpr/openalpr | License plate recognition |
| BlackFlag ECU | https://github.com/bad-antics/blackflag-ecu | Automotive ECU diagnostic |
| NullKia | https://github.com/bad-antics/nullkia | Kia/Hyundai infotainment |
| OSCC (PolySync) | https://github.com/PolySync/OSCC | Open Source Car Control |
| Open Vehicle Monitoring | https://github.com/openvehicles/Open-Vehicle-Monitoring-System | Vehicle monitoring |
| CANdiy-Shield | https://github.com/watterott/CANdiy-Shield | Arduino CAN shield |
| awesome-vehicle-security | https://github.com/jaredmichaelsmith/awesome-vehicle-security | Vehicle security catalogue |
| automotive-security-research | https://github.com/ps1337/automotive-security-research | Auto security research |

### FORENSICS / IR (2,648 lines)

Memory forensics, disk analysis, incident response tooling.

| Tool | Repo | Notes |
|------|------|-------|
| Volatility 3 | https://github.com/volatilityfoundation/volatility3.git | Memory forensics (recommended) |
| Volatility 2 | https://github.com/volatilityfoundation/volatility.git | Memory forensics (legacy) |
| LiME | https://github.com/504ensicsLabs/LiME | Linux Memory Extractor |
| bulk_extractor | https://github.com/simsong/bulk_extractor | Forensics data carving |
| EVTXtract | https://github.com/williballenthin/EVTXtract | Windows event log carving |
| Scalpel | https://github.com/sleuthkit/scalpel | Data carving tool |
| hachoir3 | https://github.com/vstinner/hachoir3 | Binary stream parsing |
| SFlock | https://github.com/jbremer/sflock | Nested archive extraction |
| Mac APR | https://github.com/ydkhatri/mac_apt | macOS artifact parsing |
| OSX Auditor | https://github.com/jipegit/OSXAuditor | Mac forensics tool |
| OSX Collector | https://github.com/yelp/osxcollector | Live response for macOS |
| knockknock | https://github.com/synack/knockknock | macOS persistence detection |
| Linux Memory Grabber | https://github.com/halpomeranz/lmg | Linux memory dump |
| VolatilityBot | https://github.com/mkorman90/VolatilityBot | Volatility automation |
| VolDiff | https://github.com/aim4r/VolDiff | Malware memory footprint diff |
| inVtero.net | https://github.com/ShaneK2/inVtero.net | Windows memory analysis |
| Evolve | https://github.com/JamesHabben/evolve | Volatility web interface |
| CIRTKit | https://github.com/byt3smith/CIRTKit | IR toolkit collection |
| FastIR Collector Linux | https://github.com/SekoiaLab/Fastir_Collector_Linux | Linux evidence collection |
| GRR (Google) | https://github.com/google/grr | Remote live forensics |
| MozDef (Mozilla) | https://github.com/mozilla/MozDef | Defense platform |
| nightHawk Response | https://github.com/biggiesmallsAG/nightHawkResponse | IR platform |
| Zentral | https://github.com/zentralopensource/zentral | Endpoint fleet management |
| Bitscout | https://github.com/vitaly-kamluk/bitscout | Remote forensics builder |
| CDQR (Cold Disk Quick Response) | https://github.com/rough007/CDQR | Quick disk triage |
| CCF-VM | https://github.com/rough007/CCF-VM | Forensics VM |
| Security Onion | https://github.com/Security-Onion-Solutions/security-onion | Network security monitoring |
| Doorman | https://github.com/mwielgoszewski/doorman | Osquery fleet manager |
| Envdb | https://github.com/mephux/envdb | Environment data collector |
| Falcon Orchestrator | https://github.com/CrowdStrike/falcon-orchestrator | CrowdStrike IR orchestration |
| LimaCharlie | https://github.com/refractionpoint/limacharlie | Endpoint security platform |
| CimSweep | https://github.com/PowerShellMafia/CimSweep | WMI-based remote IR |
| ir-rescue | https://github.com/diogo-fernan/ir-rescue | Windows IR batch script |
| Logdissect | https://github.com/dogoncouch/logdissect | Log analysis CLI |
| FIR (Fast Incident Response) | https://github.com/certsocietegenerale/FIR | IR management platform |
| threat_note | https://github.com/defpoint/threat_note | Investigation notebook |
| IRM | https://github.com/certsocietegenerale/IRM | IR methodologies |
| PagerDuty IR Docs | https://github.com/PagerDuty/incident-response-docs | IR documentation |

### Malware Analysis / Sandboxing

| Tool | Repo | Notes |
|------|------|-------|
| de4dot | https://github.com/0xd4d/de4dot | .NET deobfuscator |
| FLOSS (FireEye) | https://github.com/fireeye/flare-floss | Obfuscated string solver |
| NoMoreXOR | https://github.com/hiddenillusion/NoMoreXOR | XOR key guesser |
| PackerAttacker | https://github.com/BromiumLabs/PackerAttacker | Hidden code extractor |
| unpacker | https://github.com/malwaremusings/unpacker | Windows malware unpacker |
| unxor | https://github.com/tomchop/unxor | XOR known-plaintext attack |
| xortool | https://github.com/hellman/xortool | XOR key length/guess |
| VirtualDeobfuscator | https://github.com/jnraber/VirtualDeobfuscator | Virtualization-based deobfuscation |
| box-js | https://github.com/CapacitorSet/box-js | JavaScript malware analysis |
| malpdfobj | https://github.com/9b/malpdfobj | Malicious PDF deconstructor |
| PDF X-Ray Lite | https://github.com/9b/pdfxray_lite | PDF analysis |
| AnalyzePDF | https://github.com/hiddenillusion/AnalyzePDF | PDF threat analysis |
| Viper | https://github.com/viper-framework/viper | Binary analysis framework |
| Cuckoo-modified | https://github.com/spender-sandbox/cuckoo-modified | Modified Cuckoo sandbox |
| Mastiff | https://github.com/KoreLogicSecurity/mastiff | Static analysis framework |
| Visualize_Logs | https://github.com/keithjjones/visualize_logs | Log visualization |
| Lorg | https://github.com/jensvoid/lorg | HTTPD log security analysis |
| dnSpy | https://github.com/0xd4d/dnSpy | .NET reverse engineering |

### Log / Evidence Collection

| Tool | Repo | Notes |
|------|------|-------|
| boomerang | https://github.com/EmersonElectricCo/boomerang | Consistent log collection |
| dnstwist | https://github.com/elceef/dnstwist | Domain typo-squatting detection |
| IPinfo | https://github.com/hiddenillusion/IPinfo | IP/domain information |
| Machinae | https://github.com/hurricanelabs/machinae | OSINT information gathering |
| mailchecker | https://github.com/FGRibreau/mailchecker | Temp email detection |
| MaltegoVT | https://github.com/michael-yip/MaltegoVT | VirusTotal Maltego transform |

### Endpoint / IR Frameworks

| Tool | Repo | Notes |
|------|------|-------|
| PowerForensics | https://github.com/Invoke-IR/PowerForensics | Windows disk forensics |
| HELK | https://github.com/Cyb3rWard0g/HELK | Hunting ELK stack |

---

### CLOUD SECURITY (3,367 lines — extended from original)

Cloud infrastructure tools, container/K8s security, CI/CD pipelines.

| Tool | Repo | Notes |
|------|------|-------|
| Prowler | https://github.com/prowler-cloud/prowler | Multi-cloud security scanner |
| ScoutSuite | https://github.com/nccgroup/ScoutSuite | Multi-cloud auditing |
| SkyArk | https://github.com/cyberark/SkyArk | AWS privileged entity scanner |
| Pacu | https://github.com/RhinoSecurityLabs/pacu | AWS exploitation framework |
| Cloudsplaining | https://github.com/salesforce/cloudsplaining | AWS IAM least-privilege |
| Cloudsploit (Aqua) | https://github.com/aquasecurity/cloudsploit | Cloud security scanner |
| Trivy | https://github.com/aquasecurity/trivy | Container vulnerability scanner |
| Falco | https://github.com/falcosecurity/falco | Container runtime security |
| kube-bench | https://github.com/aquasecurity/kube-bench | K8s CIS benchmark |
| kube-hunter | https://github.com/aquasecurity/kube-hunter | K8s weakness scanner |
| kubectl-who-can | https://github.com/aquasecurity/kubectl-who-can | K8s RBAC analysis |
| KubiScan | https://github.com/cyberark/KubiScan | K8s risky permissions scanner |
| CDK | https://github.com/cdk-team/CDK | Container pentest toolkit |
| peirates | https://github.com/inguardians/peirates | K8s penetration testing |
| Kubernetes Goat | https://github.com/madhuakula/kubernetes-goat | Vulnerable K8s lab |
| KubeHound | https://github.com/DataDog/KubeHound | K8s attack path analysis |
| Metadata Goat | https://github.com/BishopFox/badPods | K8s pod security |
| Clair | https://github.com/coreos/clair | Container static analysis |
| Dagda | https://github.com/eliasgranderubio/dagda | Docker image analysis |
| docker-bench-security | https://github.com/docker/docker-bench-security | Docker CIS benchmark |
| bane | https://github.com/genuinetools/bane | Docker AppArmor generator |
| CIS Docker Benchmark | https://github.com/dev-sec/cis-docker-benchmark | InSpec Docker compliance |
| notary | https://github.com/theupdateframework/notary | Trusted content collections |
| OpenSCAP | https://github.com/OpenSCAP/openscap | Docker/container SCAP |
| AWS Security Hub Auto Remediation | https://github.com/awslabs/aws-security-hub-automated-response-and-remediation | AWS automated response |
| PurpleCloud | https://github.com/iknowjason/PurpleCloud | Hybrid identity cyber range |
| K8s CKA Course | https://github.com/kodekloudhub/certified-kubernetes-administrator-course | CKA training |
| K8s CKS Study Guide | https://github.com/stackrox/Kubernetes_Security_Specialist_Study_Guide | CKS training |
| MetalK8s | https://github.com/scality/metalk8s | On-prem K8s |
| SOPS (Mozilla) | https://github.com/mozilla/sops | Encrypted secrets in git |
| ManageIQ | https://github.com/ManageIQ/manageiq | Hybrid cloud management |
| CloudSlang | https://github.com/CloudSlang/cloud-slang | Docker process automation |
| Mantl | https://github.com/mantl/mantl | Distributed service platform |
| Traefik | https://github.com/containous/traefik | Container reverse proxy |
| fabio | https://github.com/fabiolb/fabio | Zero-conf HTTP/TCP proxy |
| Anchore | https://github.com/anchore/anchore | Image vulnerability analysis |
| Flagger | https://github.com/weaveworks/flagger | K8s progressive delivery |
| Flux | https://github.com/fluxcd/flux | GitOps for K8s |
| Nomad | https://github.com/hashicorp/nomad | Container orchestration |
| Rancher | https://github.com/rancher/rancher | K8s management |
| Mesos | https://github.com/apache/mesos | Container orchestration |
| Marathon | https://github.com/mesosphere/marathon | Container PaaS |
| Kubernetes | https://github.com/kubernetes/kubernetes | Core K8s |
| Ignite | https://github.com/weaveworks/ignite | VM with container UX |
| OctoDNS | https://github.com/github/octodns | DNS management |
| cAdvisor | https://github.com/google/cadvisor | Container resource monitoring |
| Glances | https://github.com/nicolargo/glances | System monitoring |
| Awesome IAM | https://github.com/kdeldycke/awesome-iam | IAM resource catalogue |
| Awesome K8s | https://github.com/ramitsurana/awesome-kubernetes | K8s resource catalogue |
| Awesome Linux Containers | https://github.com/Friz-zy/awesome-linux-containers | Container resource catalogue |

### CI/CD & DevOps Pipeline

| Tool | Repo | Notes |
|------|------|-------|
| Drone | https://github.com/drone/drone | Container-native CD |
| Evergreen | https://github.com/evergreen-ci/evergreen | Distributed CI |
| GitHub Actions | https://github.com/features/actions | CI/CD automation |
| Phabricator | https://github.com/phacility/phabricator | Code review platform |
| Gitblit | https://github.com/gitblit/gitblit | Git server |
| Uwsgi | https://github.com/unbit/uwsgi | App server container |

### Docker Tooling

| Tool | Repo | Notes |
|------|------|-------|
| bocker | https://github.com/icy/bocker | Dockerfile in Bash |
| box | https://github.com/box-builder/box | Dockerfile with mruby |
| Composerize | https://github.com/magicmark/composerize | docker run → compose |
| Habitus | https://github.com/cloud66/habitus | Docker build flow |
| Rocker | https://github.com/grammarly/rocker | Extended Dockerfile builder |
| Centurion | https://github.com/newrelic/centurion | Mass Docker deployment |
| Helios (Spotify) | https://github.com/spotify/helios | Container fleet management |
| Swarmpit | https://github.com/swarmpit/swarmpit | Docker Swarm UI |
| Capitan | https://github.com/byrnedo/capitan | Docker orchestration |
| Logspout | https://github.com/gliderlabs/logspout | Docker log routing |
| netshoot | https://github.com/nicolaka/netshoot | Docker network troubleshooting |
| Flannel | https://github.com/coreos/flannel | Container overlay network |
| Kontena | https://github.com/kontena/kontena | Container platform |
| Clocker | https://github.com/brooklyncentral/clocker | Docker cloud management |
| Zabbix Docker | https://github.com/monitoringartist/Zabbix-Docker-Monitoring | Container monitoring |
| Crowdr | https://github.com/polonskiy/crowdr | Multi-container management |

---

### GOVERNANCE / COMPLIANCE (2,453 lines)

Risk frameworks, standards, certifications.

| Tool | Repo | Notes |
|------|------|-------|
| Foundry Security Spec (Cisco) | https://github.com/CiscoDevNet/foundry-security-spec | AI security specification |
| GitHub spec-kit | https://github.com/github/spec-kit | Specification toolkit |
| MITRE ATLAS Data | https://github.com/mitre-atlas/atlas-data | AI threat matrix data |
| MITRE ATLAS Navigator | https://github.com/mitre-atlas/atlas-navigator | ATLAS visualization |
| MITRE ATLAS Arsenal | https://github.com/mitre-atlas/arsenal | CALDERA AI adversary plugin |
| certs (santosomar) | https://github.com/santosomar/certs | Certification roadmap |
| Sysmon Modular | https://github.com/olafhartong/sysmon-modular | Sysmon config + ATT&CK mapping |
| Selefra | https://github.com/selefra/selefra | Policy-as-code |

---

### NETWORK ATTACKS (1,774 lines)

Network protocols, packet manipulation, MITM, DNS attacks.

| Tool | Repo | Notes |
|------|------|-------|
| Scapy | https://github.com/secdev/scapy | Packet manipulation |
| DotDotPwn | https://github.com/wireghoul/dotdotpwn | Directory traversal fuzzer |
| PowerSploit | https://github.com/PowerShellMafia/PowerSploit | PowerShell post-exploitation |
| Empire | https://github.com/BC-SECURITY/Empire | PowerShell/RAT post-exploitation |
| ROPgadget | https://github.com/JonathanSalwan/ROPgadget | ROP gadget finder |

### CRYPTOGRAPHY (6,165 lines)

Encryption, hashing, key management, crypto attacks.

| Tool | Repo | Notes |
|------|------|-------|
| Themis | https://github.com/cossacklabs/themis | Cross-platform crypto library |
| CIRCL (Cloudflare) | https://github.com/cloudflare/circl | Cryptographic library |

### WEB ATTACKS (6,426 lines — extended Burp Suite catalogue)

Hundreds of Burp Suite extensions covering every phase of web application testing. Category coverage includes: OAuth/SAML/JWT auth testing, GraphQL API testing, JavaScript analysis, cloud (AWS/GCP/Azure) scanner extensions, HTTP smuggling detection, serialization testing (Java/PHP/.NET), WebSocket testing, Blazor/SignalR, Protobuf/AMF, and many more.

**Notable Burp Extensions referenced in h4cker:**

| Extension | Repo | Notes |
|-----------|------|-------|
| Hackvertor | https://github.com/hackvertor/hackvertor | Tag-based data transformation |
| SAML Raider | https://github.com/SAMLRaider/SAMLRaider | SAML message manipulation |
| InQL Scanner | https://github.com/doyensec/inql | GraphQL introspection + testing |
| HTTP Request Smuggler | https://github.com/portswigger/http-request-smuggler | HTTP smuggling detection |
| AWS Extender | https://github.com/VirtueSecurity/aws-extender | AWS storage testing |
| AWS Security Checks | https://github.com/PortSwigger/aws-security-checks | AWS vulnerability scan |
| HaE | https://github.com/gh0stkey/HaE | Highlight and extract |
| GAP Burp Extension | https://github.com/xnl-h4ck3r/GAP-Burp-Extension | API endpoint discovery |
| PwnFox | https://github.com/B-i-t-K/PwnFox | Firefox/Burp integration |
| Burp Bounty | https://github.com/wagiro/BurpBounty | Custom scan checks |
| Burp Suite Sharpener | https://github.com/mdsecresearch/BurpSuiteSharpener | UX enhancements |
| Piper | https://github.com/silentsignal/burp-piper | Flexible data processing |
| Reshaper | https://github.com/synfron/ReshaperForBurp | Configurable traffic rules |
| WebSocket Turbo Intruder | https://github.com/Hannah-PortSwigger/WebSocketTurboIntruder | WebSocket fuzzing |
| BlazorTrafficProcessor | https://github.com/AonCyberLabs/BlazorTrafficProcessor | Blazor message testing |
| GQL Raider | https://github.com/denniskniep/GQLRaider | GraphQL testing suite |
| DNS Analyzer | https://github.com/The-Login/DNS-Analyzer | DNS vulnerability detection |
| PasskeyScanner | https://github.com/alexcowperthwaite/PasskeyScanner | WebAuthn/passkey testing |
| Host Header Inchecktion | https://github.com/fabianbinna/host_header_inchecktion | Host header injection |
| Server-Side Prototype Pollution | https://github.com/hackvertor/server-side-prototype-pollution | Prototype pollution scan |
| CSP Auditor | https://github.com/GoSecure/csp-auditor | CSP configuration audit |
| js-miner | https://github.com/portswigger/js-miner | JS endpoint extraction |
| Taborator | https://github.com/hackvertor/taborator | Collaborator client |
| SignSaboteur | https://github.com/d0ge/sign-saboteur | Signed token testing |
| JWT Editor | https://github.com/DolphFlynn/jwt-editor | JWT creation/editing |
| EsPReSSO | https://github.com/RUB-NDS/BurpSSOExtension | SSO protocol testing |
| ParamMiner | https://github.com/PortSwigger/param-miner | Parameter discovery |
| JSpector | https://github.com/hisxo/JSpector | JS analysis |
| Burp DOM Scanner | https://github.com/fcavallarin/burp-dom-scanner | DOM-based vuln scanner |
| Trishul | https://github.com/gauravnarwani97/Trishul | Common vulnerability scan |
| Agartha | https://github.com/volkandindar/agartha | Auth/pentest platform |
| 403Bypasser | https://github.com/sting8k/BurpSuite_403Bypasser | 403 bypass |
| BurpShiroPassiveScan | https://github.com/pmiaowu/BurpShiroPassiveScan | Shiro detection |
| Log4j2Scan | https://github.com/whwlsfb/Log4j2Scan | Log4j RCE scan |
| Cypher Injection Scanner | https://github.com/morkin1792/cypher-injection-scanner | Cypher injection |
| FlareQuench | https://github.com/aress31/flarequench | Cloudflare bypass |
| iRule Detector | https://github.com/kugg/irule-detector | F5 BigIP RCE |
| Burp AEM Scanner | https://github.com/thomashartm/burp-aem-scanner | AEM configuration |
| AWS Signer | https://github.com/NetSPI/AWSSigner | AWS SigV4 signing |
| IP Rotate | https://github.com/RhinoSecurityLabs/IPRotate_Burp_Extension | IP rotation via AWS API GW |
| Custom Send To | https://github.com/PortSwigger/custom-send-to | Customizable send-to menu |
| Stepper | https://github.com/CoreyD97/Stepper | Multi-stage repeater |
| Bookmarks | https://github.com/TypeError/Bookmarks | Request bookmarking |
| Copy As Python-Requests | https://github.com/portswigger/copy-as-python-requests | Copy to Python code |
| Decoder Improved | https://github.com/nccgroup/Decoder-Improved | Enhanced decoder |
| JSON Beautifier | https://github.com/NetSPI/JSONBeautifier | JSON formatting |
| ViewState Editor | https://github.com/portswigger/viewstate-editor | ASP.NET ViewState |
| BurpKit | https://github.com/allfro/BurpKit | WebKit rendering engine |
| Jython Tab | https://github.com/mwielgoszewski/burp-jython-tab | Jython scripting |
| Buby | https://github.com/tduehr/buby | JRuby Burp interface |
| SAMLReQuest | https://github.com/ernw/burpsuite-extensions | SAML message viewer |
| Dupe Key Injector | https://github.com/pwntester/DupeKeyInjector | Duplicate key injection |
| OAUTHScan | https://github.com/akabe1/OAUTHScan | OAuth 2.0/OpenID scan |

---

### EXPLOIT DEVELOPMENT (2,176 lines)

Binary analysis, reversing, debuggers, exploit frameworks, CTF/challenges.

| Tool | Repo | Notes |
|------|------|-------|
| pwndbg | https://github.com/pwndbg/pwndbg | GDB exploitation enhancement |
| peda | https://github.com/longld/peda | Python Exploit Development Assistance |
| ROPgadget | https://github.com/JonathanSalwan/ROPgadget | ROP gadget finder |
| Medusa | https://github.com/wisk/medusa | Cross-platform disassembler |
| plasma | https://github.com/joelpx/plasma | x86/ARM/MIPS disassembler |
| Voltron | https://github.com/snare/voltron | Debugger UI toolkit |
| rVMI (FireEye) | https://github.com/fireeye/rVMI | VMI-based debugger |
| PyREBox (Cisco) | https://github.com/Cisco-Talos/pyrebox | Python scriptable RE sandbox |
| Binary Exploitation Course (RPISEC) | https://github.com/RPISEC/MBE | University-level binary exploitation |
| Exploit Challenges | https://github.com/Billy-Ellis/Exploit-Challenges | CTF exploit collection |
| Metasploit Framework | https://github.com/rapid7/metasploit-framework | Exploitation framework |
| TARS (AI pentest) | https://github.com/osgil-defense/TARS | AI-powered pentest automation |
| Reaper (AI web scanner) | https://github.com/ghostsecurity/reaper | AI-augmented web scanner |
| Fabric Agent Action | https://github.com/xvnpw/fabric-agent-action | LLM-based security testing |
| Floki | https://github.com/Cyb3rWard0g/floki | AI-driven security workflows |
| NullSec Linux | https://github.com/bad-antics/nullsec-linux | Security-focused Linux distro |
| n01d Machine | https://github.com/bad-antics/n01d-machine | Secure cross-platform VM manager |
| Awesome Python | https://github.com/vinta/awesome-python | Python resource catalogue |
| Awesome JavaScript | https://github.com/sorrycc/awesome-javascript | JS resource catalogue |

### Honeypots / Threat Intelligence

| Tool | Repo | Notes |
|------|------|-------|
| T-Pot | https://github.com/telekom-security/tpotce | Multi-honeypot platform |
| ADBHoney | https://github.com/huuck/ADBHoney | Android ADB honeypot |
| Cowrie | https://github.com/cowrie/cowrie | SSH/Telnet honeypot |
| Dionaea | https://github.com/DinoTools/dionaea | Malware capture honeypot |
| Glutton | https://github.com/mushorg/glutton | Multi-protocol honeypot |
| Heralding | https://github.com/johnnykv/heralding | Credential honeypot |
| HoneyPy | https://github.com/foospidy/HoneyPy | Low-interaction honeypot |
| HoneySAP | https://github.com/SecureAuthCorp/HoneySAP | SAP honeypot |
| Honeytrap | https://github.com/armedpot/honeytrap | Network security monitor |
| Mailoney | https://github.com/awhitehatter/mailoney | SMTP honeypot |
| Medpot | https://github.com/schmalle/medpot | HL7/FHIR honeypot |
| RDPY | https://github.com/citronneur/rdpy | RDP honeypot |
| Cisco ASA Honeypot | https://github.com/Cymmetria/ciscoasa_honeypot | Cisco ASA honeypot |
| Citrix Honeypot | https://github.com/MalwareTech/CitrixHoneypot | Citrix CVE-2019-19781 detection |
| DICOMpot | https://github.com/nsmfoo/dicompot | DICOM protocol honeypot |
| Conpot | https://github.com/mushorg/conpot | ICS/SCADA honeypot |
| Vortex | https://github.com/bad-antics/vortex | Threat intel fusion platform |

### Additional Resources

| Tool | Repo | Notes |
|------|------|-------|
| The Art of Hacking | https://github.com/The-Art-of-Hacking/h4cker | Main h4cker repository |
| The Art of Hacking (old) | https://github.com/The-Art-of-Hacking/art-of-hacking | Legacy repository |
| NullSec WebFuzz | https://github.com/bad-antics/nullsec-webfuzz | High-performance web fuzzer |
| NullSec Tools | https://github.com/bad-antics/nullsec-tools | Python/Go/Rust/C security toolkit |
| SecLists | https://github.com/danielmiessler/SecLists | Penetration testing wordlists |
| LinkedIn Scraper (TTSL) | https://github.com/dchrastil/TTSL | LinkedIn scraping |
| certs (Omar) | https://github.com/santosomar/certs | Cybersecurity certification roadmap |

---

## Usage Notes

- Load this skill when planning red team engagements, building toolkits, or doing tool reconnaissance
- All GitHub URLs preserved for direct tool access during operations
- Cross-reference with social-engineering-wireless skill for phishing/wireless/physical tools
- Cross-reference with h1-bug-bounty-patterns for vulnerability methodology
- Categories organized for rapid operational lookup: find the phase of engagement → pick tools from that section
- "👍" indicators in original source denote particularly useful/popular tools
- **H4CKER EXPANSION**: Complete 1,722-repo catalog across 16 domains available via `skill_view(name='awesome-redteam-toolkit', file_path='references/h4cker-exhaustive-repos.md')` and part 2
- Total combined catalogue: 556 (original Awesome-Redteam) + 1,722 (h4cker exhaustive) = 2,278 indexed tools across 30+ domains
- Raw source file for all 15,739 link matches: `/root/killer-queen-knowledge/h4cker-exhaustive.md`
