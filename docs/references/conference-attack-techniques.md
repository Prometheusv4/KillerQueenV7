# Conference Attack Techniques — Killer Queen's Reference

> "Black Hat and USENIX are where attack classes are born. Study them before they're in the tools."
> — Killer Queen

## 1. Black Hat Attack Classes (2015-2017)

### 1.1 TrustZone & TEE Exploitation
**Core technique**: ARM TrustZone creates a hardware-enforced split between "Normal World" and "Secure World." The attack targets the interface between them.

- Secure monitor calls (SMCs) from Normal to Secure World
- Memory corruption in TEE (Trusted Execution Environment) code
- Once in Secure World: access to keys, DRM secrets, fingerprint data
- Qualcomm Secure Execution Environment (QSEE) was a primary target

### 1.2 Serverless Runtime Attacks
**Core technique**: Function-as-a-Service platforms re-use execution environments.

- Cold start vs warm start: warm starts may leak previous execution data
- /tmp directory persistence across invocations
- Process reuse → memory disclosure between tenants
- Event injection: control event payload → execute in function's context

### 1.3 New SSRF Classes
**Core technique**: Server-Side Request Forgery is not just about internal networks — it's about trust boundaries.

- **SSRF to cloud metadata**: 169.254.169.254 → IAM credentials
- **SSRF to Unix sockets**: docker.sock, MySQL socket, Redis socket
- **SSRF to internal APIs**: localhost-only endpoints, admin panels
- **SSRF via URL parser confusion**: different parsers see different hosts
- **Blind SSRF**: can't see response, but can trigger actions (send email, create resources)

### 1.4 Cache Deception (Web Cache Deception)
**Core technique**: Trick the cache into storing sensitive responses as public static assets.

Attack flow:
```
1. Attacker requests: /sensitive-page/../non-existent.css
2. Origin server: URL has .css extension → serves /sensitive-page content with public Cache-Control
3. Cache: stores under /sensitive-page/../non-existent.css as CSS
4. Attacker (or victim) requests same URL → gets cached sensitive content
```

### 1.5 Container Orchestration Attacks
**Core technique**: Kubernetes/Docker/Mesos security boundaries.

- **Docker API exposure**: Port 2375/2376 without auth → full host compromise
- **Kubernetes RBAC bypass**: over-privileged service accounts
- **etcd exposure**: Kubernetes secrets in plaintext
- **Container escape**: privileged containers, host PID namespace, host mounts
- **Helm/Tiller**: pre-v3 had no authentication

### 1.6 Multi-Target SQLite Exploitation
**Core technique**: SQLite is embedded everywhere — browsers, phones, IoT, desktop apps.

- Shared memory exploits: SQLite WAL mode uses shared memory → multi-process attacks
- FTS (Full-Text Search) vulnerabilities: tokenizer overflows
- Extension loading: if you can control the extension path → code execution
- `SELECT load_extension()`: if enabled, trivial RCE
- Memory-mapped I/O: mmap'd databases can be corrupted across process boundaries

## 2. USENIX Security 2025/2026 — Attack Primitives

### 2.1 Firmware Fuzzing (AidFuzzer)
**Primitive**: AI-assisted fuzzing of firmware blobs using learned models of expected behavior.
- Targets: UEFI drivers, BMC firmware, peripheral firmware
- Approach: Train model on known-good firmware behavior → mutate inputs → detect deviations
- Impact: Finds bugs in code that traditional fuzzers can't reach (no source, no emulation)

### 2.2 Architectural Attacks (StackWarp)
**Primitive**: New class of microarchitectural attacks targeting stack operations.
- Exploits speculative execution in stack engine
- Leaks data across privilege boundaries
- Similar to Spectre but targeting a different microarchitectural component
- Mitigation: likely requires silicon fixes

### 2.3 OAuth Abuse Patterns
**Primitive**: OAuth 2.0 and OpenID Connect implementation bugs.

- **Redirect URI validation bypass**: pattern matching failures, open redirectors
- **State parameter missing**: CSRF on OAuth flow → link victim's account to attacker's
- **PKCE bypass**: authorization code interception when PKCE is missing or incorrectly implemented
- **Scope upgrade**: incremental consent without re-authorization
- **Client secret extraction**: mobile apps, SPAs can't protect secrets

### 2.4 Micro-architectural Attacks
**Primitive class**: Side-channel attacks via shared CPU resources.

- Cache timing (Flush+Reload, Prime+Probe, Flush+Flush)
- Branch predictor poisoning
- Speculative execution (Spectre variants)
- DRAM disturbance (Rowhammer)
- Power analysis, EM analysis

## 3. Cross-Cutting Attack Patterns

### 3.1 Parser Differential Attacks
When two different parsers process the same input:
```
Parser A: sees request to /public/file.css  → allowed
Parser B: sees request to /admin/secret     → served
```
This pattern recurs in: URL parsers, HTTP parsers, SMTP parsers, DNS parsers, JSON/XML parsers, and encoding converters.

### 3.2 Trust Boundary Confusion
Any gateway, proxy, or middleware is a trust boundary. The bug is in the assumption.
```
Frontend assumes: "I've validated the user, backend can trust this request"
Backend assumes: "Frontend validated this, so I can process it"
Attacker: "I'll bypass the frontend's validation and talk to the backend directly"
```

### 3.3 State Machine Attacks
Protocols with complex state machines (TLS, OAuth, IPsec, 5G) are vulnerable to:
- State skipping (jump to authenticated state)
- State replay (reuse previous state transition)
- State confusion (component A thinks state X, component B thinks state Y)

### 3.4 Serialization/Deserialization Mismatch
Different deserializers handle the same format differently:
- JSON duplicate key handling: last-key-wins vs first-key-wins vs error
- XML entity expansion (billion laughs)
- Java deserialization gadgets
- Python pickle RCE
- PHP unserialize() object injection

## 4. Attack Techniques the Conferences Validated

### Techniques that became mainstream:
1. **SSRF is the new SQLi** — it's everywhere, and it leads to RCE via metadata endpoints
2. **OAuth is broken everywhere** — implementation bugs are universal
3. **Containers are not security boundaries** — don't treat them as such
4. **Cache is attack surface** — not just performance optimization
5. **Parsers are bug factories** — every new format creates new bugs
6. **JavaScript engines will never be secure** — the complexity is too high
7. **Hardware has bugs** — Spectre/Meltdown proved this definitively
8. **Pre-installed apps are backdoors** — vendor bloatware is under-attacked

### Techniques that are emerging:
1. **AI/ML supply chain attacks** — model poisoning, dataset backdoors
2. **eBPF exploitation** — kernel-level programmability is a double-edged sword
3. **WebAssembly sandbox escapes** — WASM is the new Flash (same promise, same risks)
4. **Federated learning attacks** — model inversion, gradient leakage
5. **Quantum-safe transition attacks** — protocol downgrade during migration

## 5. Killer Queen's Conference-Based Hunting Guide

```
When new research is published:
1. Read the ATTACK PRIMITIVE, not just the specific bug
2. Ask: "Where else does this pattern apply?"
3. Generalize: one parser confusion → check ALL parser boundaries
4. Weaponize: can I operationalize this into a tool or skill?
5. Combine: how does this attack class chain with others I know?

Current Hunting Focus:
- OAuth/OIDC implementations: redirect_uri validation bypass everywhere
- SSRF to internal services: cloud metadata, Unix sockets, internal APIs
- Cache poisoning/deception: every CDN, every reverse proxy
- Parser differentials: URL, JSON, HTTP, XML in every gateway
- Container orchestration: misconfigured Kubernetes, exposed Docker APIs
- Serverless: event injection, dependency confusion, environment variable theft
```

## 6. Key References

- Black Hat USA briefings: https://blackhat.com/us-15/ through us-24/
- USENIX Security: https://www.usenix.org/conference/usenixsecurity25/
- Community notes (BH 2017): https://gist.github.com/naotokatsumi/e0672ebeeeb5f9a4dede1d1444feba5f
- Orange Tsai slides: https://github.com/orangetw/My-Presentation-Slides
- Project Zero 0-days: https://googleprojectzero.github.io/0days-in-the-wild/rca.html
