# Consolidated HackerOne SQL Injection Techniques
## Source: h1-TOPSQLI.md (307 reports, ~41KB)

================================================================================
SECTION 1: INJECTION TYPES
================================================================================

## 1A. Error-Based SQL Injection
- Report #51: Error-Based & Time-Based SQLi in 'keyword' param of admin-search.php (Revive Adserver v6.0.0) — full database access
- Report #238: Error-based blind SQL injection (DoD)
- Report #305: Two Error-Based SQLi in courses.aspx (DoD)
- Report #216: SQL injection via errortoken.json (Android API, Pornhub)
- Report #189: Code source disclosure & ability to get database information "SQL injection" (Mail.ru)
- Report #300: SQL Injection - https://███/█████████/MSI.portal (DoD)

## 1B. Blind SQL Injection (Boolean-Based)
- Report #7: Blind SQL Injection (InnoGames, $2000)
- Report #10: Blind SQL Injection (Mail.ru, $5000)
- Report #18: Boolean-based SQL Injection on relap.io (Mail.ru)
- Report #19: Blind SQL Injection in city-mobil.ru domain (Mail.ru, $2000)
- Report #20: Blind SQL injection + making profile comments disappear via "like" function (Pornhub)
- Report #21: Blind SQL Injection on starbucks.com.gt + WAF Bypass (Starbucks)
- Report #23: Blind SQL injection on id.indrive.com (inDrive, $4134)
- Report #26: Blind SQL injection in Hall of Fap (Pornhub)
- Report #47: Blind sql-injection on turboslim.lady.mail.ru (Mail.ru, $5000)
- Report #58: Blind SQL Injection at easytopup.in.th via serial_no param (Razer, $1000)
- Report #61: Blind Sql Injection (DoD)
- Report #73: Blind SQL Injection in /php/geto2banner (Eternal/Zomato, $2000)
- Report #76: Blind SQL injection at tsftp.informatica.com (Informatica)
- Report #77: Boolean Based Blind Sql Injection Via User Agent (DoD)
- Report #84: Blind SQL injection in third-party software (Rocket.Chat)
- Report #86: SQL injection in 3rd party software Anomali (Uber, $2500)
- Report #90: Blind SQL Injection in /php/widgets_handler.php (Eternal/Zomato, $2000)
- Report #92: Blind SQL Injection on news.mail.ru (Mail.ru, $3000)
- Report #107: Blind SQL Injection (MTN Group)
- Report #110: Boolean SQLi - /█████.php (Eternal/Zomato, $1000)
- Report #116: Blind Sql Injection (DoD)
- Report #121: Boolean SQLi - /███████.php (Eternal/Zomato, $1000)
- Report #124: Time-based Blind SQLi on news.starbucks.com (Starbucks)
- Report #127: Blind SQL injection on honor.hi-tech.mail.ru (Mail.ru, $300)
- Report #132: Blind SQL injection on city-mobil.ru/taxiserv/ in filter{"id_locality"} (Mail.ru, $3500)
- Report #145: Blind SQL Injection via URI Path (Mars)
- Report #152: Blind Based SQL Injection in 3d.sc.money (CS Money)
- Report #159: SQL Injection, exploitable in boolean mode (Eternal/Zomato)
- Report #164: Blind SQL iNJECTION (DoD)
- Report #171: uchi.ru check_lessons Blind SQL Injection (Mail.ru, $750)
- Report #176: Blind SQL injection (DoD)
- Report #177: Boolean-based SQL injection (Razer)
- Report #179: Blind SQLi vulnerability (DoD)
- Report #181: Blind SQL injection (Hanno's projects)
- Report #194: Blind SQL Injection (Informatica)
- Report #200: Blind SQL Injection (ok.ru)
- Report #203: Blind SQL Injection (DoD)
- Report #207: Blind SQLi (DoD)
- Report #227: Weak credentials, Blind SQLi, Timing attack → web admin access (50m-ctf)
- Report #228: Boolean SQL Injection /personnel.php?content=profile&rcnum=* (DoD)
- Report #239: Blind sql injection (Mail.ru, $250)
- Report #248: Blind Sql Injection on caesary.yahoo.net (Yahoo!)
- Report #250: Blind Sql Injection (Yahoo!)
- Report #261: Blind SQL Injection (DoD)
- Report #295: Blind SQL INJ (Paragon Initiative Enterprises)
- Report #297: Blind SQL injection | Language choice in presentation (Gratipay)

## 1C. Time-Based SQL Injection
- Report #3: Time-Based SQL injection at city-mobil.ru (Mail.ru, $15000)
- Report #34: Time Based SQL Injection on intensedebate.com /js/commentAction/ (Automattic)
- Report #45: Time based SQL injection (DoD)
- Report #51: Error-Based & Time-Based SQL Injection in 'keyword' param (Revive Adserver)
- Report #60: Time Based SQL Injection on intensedebate.com /changeReplaceOpt.php (Automattic)
- Report #70: Time Based SQL Injection on reviews.zomato.com (Eternal, $1000)
- Report #74: Blind SQL Injection (Time Based Payload) in easytopup.in.th via CheckuserForm[user_id] (Razer, $1000)
- Report #78: Time Based SQL Injection (U.S. Dept of State)
- Report #87: Time-base SQL Injection in Search Users (Concrete CMS)
- Report #94: Time-based blind SQL injection (DoD)
- Report #122: Time-based Blind SQLi on news.starbucks.com (Starbucks)
- Report #133: Time Based SQL-inject in post-param login[username] on youporn.com (Pornhub, $2500)
- Report #160: Time based SQL injection [HtUS] (DoD)
- Report #205: Time-based sql-injection on puzzle.mail.ru (Mail.ru, $300)
- Report #208: Time Based SQL Injection vulnerability (DoD)
- Report #224: Time Based SQL Injection on cfire.mail.ru (Mail.ru, $200)
- Report #233: SQL Injections on Referer Header exploitable via Time-Based method (DoD)
- Report #240: Time-Based SQL Injection on townwars.mail.ru (Mail.ru, $150)
- Report #253: Time Based SQL Injection vulnerability (DoD)
- Report #276: SQL injection, time zoom script, tile ID (Uzbey)
- Report #288: Time based sql injection (Mail.ru, $200)
- Report #296: Time Based SQL injection in url parameter (WebSummit)
- Report #298: Time Based SQL injection (DoD)
- Report #303: Time Based SQL Injection on cfire.mail.ru (Mail.ru, $150)

## 1D. Union-Based SQL Injection
- Report #32: SQL Injection Union Based (Automattic)
- Report #83: Union SQLi + Waf Bypass on zomato.com (Eternal, $1000)
- Report #131: SQL injection method: -1 OR 3*2*1=6 AND 000159=000159 (DoD)

## 1E. Stacked Queries
- Report #270: SQL injection (stacked queries) in export to Excel functionality on Vidyo Server (8x8)
- Report #141: Ability to escape database transaction through SQL injection → arbitrary code execution (HackerOne)

## 1F. Out-of-Band SQL Injection
- No explicitly labeled OOB SQLi reports in this dataset (typical for H1 — OOB is rare in disclosed reports)

## 1G. NoSQL Injection
- Report #143: NoSQL injection leaks visitor token and livechat messages (Rocket.Chat)
- Report #163: Pre-Auth Blind NoSQL Injection leading to Remote Code Execution (Rocket.Chat)
- Report #188: Post-Auth Blind NoSQL Injection in users.list API → RCE (Rocket.Chat)
- Report #212: NoSQL injection in listEmojiCustom method call (Rocket.Chat)
- Report #247: Golang: Add MongoDb NoSQL injection sinks (GitHub Security Lab)
- Report #272: NoSQL-Injection discloses S3 File Upload URLs (Rocket.Chat)
- Report #286: [Python] CWE-943: Add NoSQL Injection Query (GitHub Security Lab)

================================================================================
SECTION 2: INJECTION PARAMETER LOCATIONS (Unusual Vectors)
================================================================================

## User-Agent Header Injection
- Report #2: SQL injection via User-agent header (GSA Bounty, 694 upvotes)
- Report #77: Boolean Based Blind Sql Injection Via User Agent (DoD)
- Report #150: Blind User-Agent SQL Injection → Blind Remote OS Command Execution (Sony)

## Cookie Injection
- Report #12: SQL Injection on cookie parameter (MTN Group, 320 upvotes)

## URL Path Injection
- Report #31: SQLi in URL paths (MTN Group, 147 upvotes)
- Report #42: SQL injection in URL path → Database Access (MTN Group, 110 upvotes)
- Report #123: SQL injection in URL path processing on www.ibm.com (IBM)
- Report #145: Blind SQL Injection via URI Path (Mars)
- Report #222: SQL Injection in URI Path → Full Database Disclosure (DoD)
- Report #229: SQL Injection via URL (DoD)

## Referer Header Injection
- Report #233: SQL Injections on Referer Header exploitable via Time-Based method (DoD)

## JSON Parameter Injection
- Report #236: SQL Injection - JSON 'name' parameter (DoD)
- Report #75: SQL injection in JSONField KeyTransform (Django)

## GraphQL Endpoint Injection
- Report #27: SQL injection in GraphQL endpoint through embedded_submission_form_uuid parameter (HackerOne, 172 upvotes)

## Other Notable Locations
- Report #235: SQL Injection - data[account][id] parameter (DoD)
- Report #237: SQL Injection - entryid parameter in 'formbuilderv2-confirmation.php' (DoD)
- Report #262: SQL injection in POST param (DoD)
- Report #8: countryFilter[] array parameter (Valve, $25000)
- Report #36: list[] array parameter (Razer)
- Report #105: filter{"id_locality"} JSON-like param (Mail.ru)
- Report #109: Multiple SQL Injections + constrained LFI in esk-static.3igames.mail.ru (Mail.ru, $1500)

================================================================================
SECTION 3: WAF BYPASS TECHNIQUES
================================================================================

## Explicit WAF Bypass Reports
- Report #21: Blind SQL Injection on starbucks.com.gt and WAF Bypass (Starbucks, 209 upvotes)
- Report #83: Union SQLi + Waf Bypass on zomato.com (Eternal/Zomato, $1000)
- Report #120: SQL Injection Detection Bypass in AWS WAF Managed Rules (AWSManagedSQLiRuleSet) (AWS VDP, 36 upvotes)
- Report #196: MSSQL injection via param Customwho + WAF bypass (DoD)

## Signature/Validation Bypass
- Report #16: SQL Injection at fortumo via TransID param — Bypassing Signature Validation (Razer, $4000)
- Report #183: SQL Injection in cashcard via card_no param — Bypassing IP whitelist (Razer)
- Report #29: bypass sql injection #1109311 (Acronis, 162 upvotes) — WAF bypass follow-up

## Implied WAF Evasion Patterns
- Reports using User-Agent, Cookie, Referer, and URL-path injection vectors often bypass WAF rules that only inspect GET/POST body params
- Reports injecting into JSON, GraphQL, and nested array params (filter{}, data[account][id]) evade signature-based WAFs
- Time-based blind SQLi used specifically to evade WAFs that block error-based/union output

================================================================================
SECTION 4: DBMS-SPECIFIC PAYLOADS AND TECHNIQUES
================================================================================

## 4A. MySQL / MariaDB
- Report #32: Union Based SQLi (Automattic — WordPress/MySQL stack)
- Report #34: Time Based on intensedebate.com (Automattic — MySQL)
- Report #43: SQL Injection intensedebate.com (Automattic — MySQL)
- Report #60: Time Based on intensedebate.com /changeReplaceOpt.php (Automattic — MySQL)
- Report #46: Woocommerce SQL Injection in WC_Report_Coupon_Usage (Automattic — WordPress/MySQL)
- Report #115: SQL injection in Wordpress Plugin Huge IT Video Gallery (Uber, $3000)
- Report #169: WordPress DB Class bad prepare() → sqli + info disclosure (WordPress)
- Report #96: SQL injection vulnerability in Vanilla (Vanilla, $600)
- Report #103: Vanilla SQL Injection Vulnerability (Vanilla, $600)
- Report #87: Time-base SQL Injection in Search Users (Concrete CMS)
- Report #267: SQL injection in conc/index.php/ccm/system/search/users/submit (Concrete CMS)
- Report #293: SQL Injection Vulnerability in Concrete5 v5.7.3.1 (Concrete CMS)
- Report #156: Drupal 7 pre-auth SQL injection → RCE (Internet Bug Bounty)
- Report #136: SQL Injection through /include/findusers.php (ImpressCMS)
- Report #184: SQL injection when configuring a database (ImpressCMS)
- Report #35: SQL injection in structure plugin (ExpressionEngine)
- Report #113: Type Juggling → PHP Object Injection → SQL Injection Chain (ExpressionEngine)
- Report #221: SQL injection at /admin.php?/cp/members/create (ExpressionEngine)
- Report #131: SQL injection method: -1 OR 3*2*1=6 AND 000159=000159 (classic MySQL boolean blind)

## 4B. PostgreSQL
- Report #50: SQL Injection on prod.oidc-proxy.prod.webservices.mozgcp.net via invite_code (Mozilla)
- Report #97: Potential SQL Injection when annotating FilteredRelation on PostgreSQL (Django, 51 upvotes)
- Report #172: C++: Support Pqxx connector to search for sql injections to Postgres (GitHub Security Lab, $4500)
- Report #278: Active Record SQL Injection Vulnerability Affecting PostgreSQL (Ruby on Rails)
- Report #279: Active Record SQL Injection Vulnerability Affecting PostgreSQL (Ruby on Rails)
- Report #63: Arbitrary SQL command injection (Nextcloud — PostgreSQL-backed)
- Report #72: SQL Injection in Column Type Parameter Allows Arbitrary SQL Execution (Nextcloud)
- Report #118: SQL Injection in NextCloud Android App Content Provider (Nextcloud, $150)
- Report #161: SQLi allow query restriction bypass on exposed FileContentProvider (Nextcloud, $100)
- Report #204: SQL injection via vulnerable doctrine/dbal version (Nextcloud)

## 4C. Microsoft SQL Server (MSSQL)
- Report #196: MSSQL injection via param Customwho + WAF bypass (DoD)
- Report #8: SQL Injection in report_xml.php through countryFilter[] parameter (Valve, $25000) — likely MSSQL (Valve/Steam infrastructure)
- Report #112: SQL injection in /errors/viewbuild/ (Valve) — likely MSSQL
- Report #270: SQL injection (stacked queries) in export to Excel on Vidyo Server (8x8) — stacked queries typical of MSSQL

## 4D. Oracle
- Report #82: CVE-2024-53908 — Django Potential SQL injection in HasKey(lhs, rhs) on Oracle (Internet Bug Bounty, 61 upvotes)
- Report #144: Sql injection Oracle on ipm.informatica.com (Informatica)
- Report #199: Sql injection Oracle on afocusp.informatica.com:37777 (Informatica)
- Report #146: SQL Injection on /cs/Satellite path (LocalTapiola) — Oracle WebLogic/Satellite

## 4E. ClickHouse
- Report #62: SQL injection delivery-club.ru (ClickHouse) (Mail.ru, $5000)
  - Notable: ClickHouse-specific injection — different syntax from MySQL/PostgreSQL

## 4F. MongoDB / NoSQL
- Report #143: NoSQL injection leaks visitor token + livechat messages (Rocket.Chat)
- Report #163: Pre-Auth Blind NoSQL Injection → RCE (Rocket.Chat, 19 upvotes)
- Report #188: Post-Auth Blind NoSQL Injection in users.list API → RCE (Rocket.Chat)
- Report #212: NoSQL injection in listEmojiCustom method call (Rocket.Chat)
- Report #272: NoSQL-Injection discloses S3 File Upload URLs (Rocket.Chat)
- Report #247: Golang: MongoDB NoSQL injection sinks (GitHub Security Lab)
- Report #286: Python: NoSQL Injection Query (GitHub Security Lab)

================================================================================
SECTION 5: CVEs REFERENCED
================================================================================

## Django ORM SQL Injection CVEs
- CVE-2024-53908 (Report #82): Django Potential SQL injection in HasKey(lhs, rhs) on Oracle
  - Affects: Django HasKey lookup on Oracle backend
  - Bounty: $0 (Internet Bug Bounty, 61 upvotes)

- CVE-2024-42005 (Report #95): Potential SQL injection in QuerySet.values() and values_list()
  - Affects: Django QuerySet.values()/values_list()
  - Bounty: $4263 (Internet Bug Bounty, 51 upvotes)

- Report #48: SQL Injection when using FilteredRelation (Django, 93 upvotes)
  - Likely assigned a CVE (FilteredRelation SQL injection vector)

- Report #65: SQL Injection in Django ORM via Unvalidated `_connector` in Q Objects (Django, 75 upvotes)
  - Likely assigned a CVE (Q object _connector injection)

- Report #75: SQL injection in JSONField KeyTransform (Django, 68 upvotes)
  - Likely assigned a CVE (JSONField key transform injection)

- Report #97: Potential SQL Injection when annotating FilteredRelation on PostgreSQL (Django, 51 upvotes)
  - Likely assigned a CVE (FilteredRelation + PostgreSQL-specific)

## Other CVEs
- CVE-2021-38159 (Report #37): SQL Injection at files.palantir.com (Palantir, 120 upvotes)
  - Related to an Apache module or library vulnerability

- Report #156: Drupal 7 pre-auth SQL injection → RCE (Internet Bug Bounty)
  - This is the infamous Drupalgeddon (CVE-2014-3704 / SA-CORE-2014-005)

- Report #125: Apache Airflow SQL injection by authenticated user (Internet Bug Bounty, $505)
  - Likely assigned a CVE

- Report #204: SQL injection via vulnerable doctrine/dbal version (Nextcloud)
  - Doctrine DBAL CVE

================================================================================
SECTION 6: REAL-WORLD EXPLOIT CHAINS
================================================================================

## 6A. SQL Injection → Remote Code Execution (SQLi→RCE)

### Chain: SQLi on contactws.contact-sys.com (QIWI) — Multiple Reports, Same Endpoint
- Report #6: SQL injection in TScenObject action ScenObjects → RCE (475 upvotes, $0)
- Report #24: SQL injection in TCertObject operation "Delete" → RCE (194 upvotes, $0)
- Report #40: SQL injection in TRateObject.AddForOffice in USER_ID param → RCE (118 upvotes, $0)
- Report #57: SQL injection in TAktifBankObject.GetOrder in DOC_ID param → RCE (84 upvotes, $0)
- Report #93: SQL injection in TPrabhuObject.BeginOrder in DOC_ID param → RCE (52 upvotes, $0)
- Method: SQL injection → database takeover → ability to write files or execute stored procedures → RCE on Windows/IIS MSSQL stack

### Chain: Blind SQLi → RCE (Starbucks)
- Report #15: Blind SQLi → RCE, Unauthenticated access to test API Webservice (235 upvotes, $0)
- Method: Blind SQL injection chained to command execution through database features

### Chain: SQL Injection + Insecure Deserialization → RCE
- Report #39: SQL Injection + Insecure Deserialization → RCE on krisp.ai (119 upvotes, $0)
- Method: SQL injection extracts serialized objects → insecure deserialization → code execution
- Report #167: Unsafe deserialization in Libera Pay escalates SQLi → RCE (Liberapay, 18 upvotes)
- Method: SQL injection → manipulate serialized data → deserialization → command execution

### Chain: SQLi → Database Escape → Arbitrary Code Execution
- Report #141: Ability to escape database transaction through SQL injection → ACE (HackerOne, 29 upvotes)
- Method: SQL injection allows escaping the database transaction context → arbitrary code execution

### Chain: Blind User-Agent SQLi → Blind Remote OS Command Execution
- Report #150: Blind User-Agent SQL Injection → Blind Remote OS Command Execution (Sony, 26 upvotes)
- Method: SQLi via User-Agent header → xp_cmdshell or equivalent → OS command execution (blind)

### Chain: Drupal 7 Pre-Auth SQLi → RCE (Drupalgeddon)
- Report #156: Drupal 7 pre-auth SQL injection → RCE (Internet Bug Bounty, 21 upvotes)
- CVE: CVE-2014-3704 (SA-CORE-2014-005)
- Method: Pre-auth SQLi → database manipulation → code execution via Drupal's render pipeline

### Chain: Pre-Auth Blind NoSQL Injection → RCE
- Report #163: Pre-Auth Blind NoSQL Injection → RCE (Rocket.Chat, 19 upvotes)
- Method: NoSQL injection → extract admin credentials/tokens → RCE via application features

### Chain: Post-Auth Blind NoSQL Injection → RCE
- Report #188: Post-Auth Blind NoSQL Injection in users.list API → RCE (Rocket.Chat, 13 upvotes)
- Method: Authenticated NoSQL injection → escalate to RCE

### Chain: Type Juggling → PHP Object Injection → SQL Injection
- Report #113: Type Juggling → PHP Object Injection → SQL Injection Chain (ExpressionEngine, 40 upvotes)
- Method: PHP type juggling → object injection → SQL injection (multi-stage chain)

### Chain: SQLi + LFI
- Report #109: Multiple SQL Injections + constrained LFI in esk-static.3igames.mail.ru (Mail.ru, $1500)
- Method: SQL injection combined with local file inclusion

## 6B. SQL Injection → Data Exfiltration

### Full Database Extraction
- Report #1: SQL Injection Extracts Starbucks Enterprise Accounting, Financial, Payroll Database (790 upvotes, $0)
  - Impact: Full enterprise financial/accounting/payroll database exfiltration

- Report #220: SQL Injection leads to retrieve the contents of an entire database (BlockDev, 8 upvotes)

- Report #222: SQL Injection in URI Path → Full Database Disclosure (DoD, 8 upvotes)

- Report #42: SQL injection in URL path → Database Access (MTN Group, 110 upvotes)

### Sensitive User Data Exposure
- Report #106: SQLI on uberpartner.eu → exposure of sensitive user data of Uber partners (Uber, $1500)

- Report #197: SQL Injection + plaintext passwords via User Search (IBM)

- Report #143: NoSQL injection leaks visitor token + livechat messages (Rocket.Chat)

- Report #272: NoSQL-Injection discloses S3 File Upload URLs (Rocket.Chat)

### Code Source Disclosure + DB Info
- Report #189: Code source disclosure & ability to get database information "SQL injection" on townwars.mail.ru (Mail.ru)

================================================================================
SECTION 7: FRAMEWORK/ORM-SPECIFIC INJECTIONS
================================================================================

## Django ORM
- FilteredRelation SQL injection (Reports #48, #97)
- Q object _connector injection (Report #65)
- JSONField KeyTransform injection (Report #75)
- HasKey lookup on Oracle (CVE-2024-53908, Report #82)
- QuerySet.values()/values_list() (CVE-2024-42005, Report #95)

## Ruby on Rails / Active Record
- Active Record SQL Injection Affecting PostgreSQL (Reports #278, #279)
- Method: ActiveRecord's PG connector vulnerable to SQL injection

## Node.js / TypeORM
- Report #175: TypeORM SQL injection (Node.js third-party modules)
- Report #297: typeorm does not properly escape parameters → SQLi
- Report #283: `sql` module does not properly escape parameters → SQLi
- Report #182: untitled-model sql injection
- Report #218: SQL Injection or DoS due to Prototype Pollution
- Report #299: increments sql injection

## WordPress
- Report #46: Woocommerce SQL Injection in WC_Report_Coupon_Usage
- Report #115: SQL injection in Wordpress Plugin Huge IT Video Gallery (Uber)
- Report #169: WordPress DB Class bad prepare() → sqli + information disclosure

## PHP CMS
- Concrete5/Concrete CMS (Reports #87, #267, #293)
- Drupal 7 Drupalgeddon (Report #156)
- Vanilla Forums (Reports #96, #103)
- ExpressionEngine (Reports #35, #113, #221)
- ImpressCMS (Reports #136, #184)
- Serendipity (Report #258)

## Other
- Apache Airflow authenticated SQLi (Report #125)
- Nextcloud (Reports #63, #72, #118, #161, #204)

================================================================================
SECTION 8: NOTABLE HIGH-IMPACT REPORTS (Sorted by Upvotes)
================================================================================

| Upvotes | Bounty  | Company      | Description                                                |
|---------|---------|--------------|------------------------------------------------------------|
| 790     | $0      | Starbucks    | SQLi extracts enterprise accounting/financial/payroll DB   |
| 694     | $0      | GSA Bounty   | SQLi via User-Agent header                                 |
| 631     | $15,000 | Mail.ru      | Time-Based SQLi at city-mobil.ru                           |
| 580     | $2,000  | Razer        | SQLi via txid parameter                                    |
| 528     | $2,000  | Razer        | SQLi in getInviteHistoryLog                                |
| 475     | $0      | QIWI         | SQLi on contactws → RCE (TScenObject)                      |
| 432     | $2,000  | InnoGames    | Blind SQL Injection                                        |
| 401     | $25,000 | Valve        | SQLi in report_xml.php via countryFilter[] (HIGHEST BOUNTY)|
| 372     | $10,000 | Mail.ru      | SQLi at fleet.city-mobil.ru                                |
| 330     | $5,000  | Mail.ru      | Blind SQLi on windows10.hi-tech.mail.ru                    |
| 321     | $4,500  | Eternal      | SQLi on zomato.com - item_id                               |
| 320     | $0      | MTN Group    | SQLi on cookie parameter                                   |
| 240     | $2,000  | Razer        | SQLi via period-hour parameter                             |
| 236     | $0      | Acronis      | SQLi in agent-manager                                      |
| 235     | $0      | Starbucks    | Blind SQLi → RCE, unauthenticated                          |

================================================================================
SECTION 9: KEY TAKEAWAYS AND PATTERNS
================================================================================

1. Most Common Injection Type: Blind SQL Injection (Boolean + Time-based dominate the list)

2. Most Valuable Targets:
   - Enterprise financial/payroll databases (Starbucks #1)
   - E-commerce/transaction systems (Razer, Mail.ru fleet)
   - Gaming platforms (Valve, Mail.ru games)

3. WAF Evasion Techniques Observed:
   - Injecting in HTTP headers (User-Agent, Cookie, Referer)
   - URL path injection (bypasses parameter-based WAF rules)
   - JSON/GraphQL body injection
   - Nested array parameters (filter{}, arr[])
   - Time-based blind (no output to signature-match)
   - Signature validation bypass (Razer reports)

4. Most Dangerous Chains:
   - SQLi → RCE via MSSQL xp_cmdshell or file write (QIWI contactws cluster)
   - SQLi → Insecure Deserialization → RCE
   - NoSQLi → RCE (Rocket.Chat)
   - SQLi → Full Database Exfiltration

5. ORM/Third-Party Risks:
   - Django ORM had 6+ distinct SQLi vectors (FilteredRelation, Q objects, JSONField, HasKey, values())
   - TypeORM and Node.js SQL builders consistently fail at parameter escaping
   - CMS plugins (WordPress, Drupal, Concrete5) are recurring vectors

6. Highest Bounties:
   - $25,000: Valve (report_xml.php SQLi)
   - $15,000: Mail.ru (Time-Based SQLi)
   - $10,000: Mail.ru (fleet.city-mobil.ru SQLi)
   - $5,000: Mail.ru ×2 (Blind SQLi, ClickHouse SQLi)

7. Zero-Dollar High-Impact Reports: Many of the highest-upvoted reports ($0 bounty) led to critical fixes
   and significant reputation gains for the researchers despite no monetary reward.
