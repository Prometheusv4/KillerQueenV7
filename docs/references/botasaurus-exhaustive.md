# Botasaurus Exhaustive Analysis — Cloudflare Bypass & Anti-Detection Framework

## Repository Overview
- **Repo**: omkarcloud/botasaurus  
- **Files analyzed**: 618 (excluding .git and node_modules)
- **Total size**: ~158MB
- **Language**: Python (backend), TypeScript (JS client), mix of JS/Python server

## Architecture Summary

Botasaurus is an "all-in-one web scraping framework" designed to build undetectable scrapers. It consists of:

1. **Python Decorator API** (`@browser`, `@request`, `@task`) — main scraper definitions
2. **Botasaurus Driver** (`botasaurus_driver`) — modified Selenium-based anti-detection browser
3. **Botasaurus Server** (`botasaurus_server`) — web UI for task management, filtering, sorting
4. **JS Client** (`botasaurus-js`) — Node.js/TypeScript port with Playwright
5. **Human Cursor** (`botasaurus_humancursor`) — Bezier-curve mouse movements
6. **Controls** (`botasaurus-controls`) — input UI controls for scraper configuration
7. **Desktop API** — Electron desktop app packaging
8. **BOTA CLI** — Kubernetes deployment, cluster management
9. **Cache Storage** — SQLite and PostgreSQL caching backends

---

## CLOUDFLARE BYPASS TECHNIQUES

### 1. Anti-Detection Browser Driver (botasaurus_driver)

The core bypass is in the `botasaurus_driver` package (modified Selenium), referenced as "AntiDetectDriver":

**Key bypass features from anti-detect-driver.md:**

| Technique | Implementation |
|-----------|---------------|
| **Google Referral Spoofing** | `driver.google_get()` — opens Google homepage first, then navigates to target, mimicking organic search traffic |
| **Referrer-Based Navigation** | `driver.get_by_current_page_referrer()` — navigates as if user clicked a link on current page |
| **Randomized Sleep** | `driver.short_random_sleep()` — random delays between actions |
| **Bot Detection Check** | `driver.is_bot_detected()` — checks for Cloudflare/PerimeterX detection triggers |
| **Cloudflare Turnstile Bypass** | `driver.get(url, bypass_cloudflare=True)` — directly bypasses Cloudflare WAF and Turnstile CAPTCHA |
| **Local Storage Manipulation** | `driver.local_storage.set_item/get_item/remove_item/clear()` |
| **Human-like Typing** | `driver.type(selector, text)` — simulates human typing patterns |
| **Execute External JS** | `driver.execute_file('make_red.js')` — injects custom JS |
| **BeautifulSoup Integration** | `driver.bs4` — parse page with BeautifulSoup |

### 2. Cloudflare Bypass in Practice (bot_detection_tests.py)

The file `bot_detection_tests.py` demonstrates bypassing these systems:

```
- Cloudflare WAF (nopecha.com/demo/cloudflare) — bypass_cloudflare=True
- Cloudflare Turnstile CAPTCHA (turnstile.zeroclover.io) — bypass_cloudflare=True
- BrowserScan Bot Detection (browserscan.net/bot-detection)
- Fingerprint Bot Detection (fingerprint.com/products/bot-detection/)
- Datadome Bot Detection (fingerprint-scan.com)
```

All tests use: `driver.get(url, bypass_cloudflare=True)`

### 3. Browser Launch Anti-Detection Flags (page.ts / playwright.ts)

The JS Playwright version launches Chrome with these anti-detection flags:

```
--start-maximized
--remote-allow-origins=*
--no-first-run
--no-service-autorun
--homepage=about:blank
--no-pings
--password-store=basic
--disable-infobars
--disable-breakpad
--disable-dev-shm-usage
--disable-session-crashed-bubble
--disable-features=IsolateOrigins,site-per-process
--disable-search-engine-choice-screen
```

Headless mode uses `--headless=new` (the newer, harder-to-detect headless mode).

**Critical**: Uses `rebrowser-playwright-core` instead of standard Playwright — a patched version that removes automation detection signals.

### 4. Chrome Launch via Chrome-Launcher (page.ts)

Uses `chrome-launcher` package (by Google) to launch Chrome with a random debugging port, then connects via CDP:

```javascript
const { port, kill } = await ChromeLauncher.launch({ chromeFlags: flags });
const browser = await chromium.connectOverCDP(`http://localhost:${port}`);
```

### 5. Human-like Mouse Movements (botasaurus_humancursor)

Fork of HumanCursor by riflosnake, adapted for botasaurus:

- **Bezier curve movements** — mathematically modeled human-like cursor paths
- **Randomized patterns** — variations to avoid fingerprintable patterns
- **Click, drag, scroll** — all with human-like behavior
- **Specifically designed to bypass security measures and bot detection software**

---

## BROWSER FINGERPRINTING EVASION

### 1. Profile Management (browser_decorator.py)

```python
@browser(profile="my_profile")  # Persistent browser profile
@browser(tiny_profile=True)     # Minimal profile to reduce fingerprint surface
```

### 2. User-Agent Rotation

```python
@browser(user_agent="Mozilla/5.0 ...")  # Custom UA
@browser(user_agent=lambda data: get_random_ua())  # Dynamic per-request
```

### 3. Proxy Support

```python
@browser(proxy="http://user:pass@host:port")  # Single proxy
@browser(proxy=["http://p1", "http://p2"])  # Proxy rotation (cycle)
@browser(proxy=lambda data: get_proxy_for(data))  # Dynamic per-item
```

### 4. Window Size Randomization

```python
@browser(window_size=lambda data: random.choice(["1920x1080", "1366x768"]))
```

### 5. Language Spoofing

```python
@browser(lang="en-US")  # Set browser language
```

### 6. Extension Support

```python
@browser(extensions=[path_to_crx])
```

### 7. Chrome Argument Injection

```python
@browser(add_arguments=["--disable-web-security"])
@browser(remove_default_browser_check_argument=True)  # Remove default check arg
```

### 8. Resource Blocking (Cost Reduction)

```python
@browser(block_images=True)       # Block images (reduce proxy cost)
@browser(block_images_and_css=True)  # Block images+CSS (max cost reduction)
```

---

## CAPTCHA SOLVING APPROACHES

### 1. Cloudflare Turnstile

Built-in bypass via `bypass_cloudflare=True` parameter on `driver.get()`. The actual solving logic is in `botasaurus_driver` (proprietary).

### 2. CAPTCHA Detection

`driver.is_bot_detected()` — checks for known Cloudflare/PerimeterX detection triggers on the current page.

### 3. Pause-on-Detect (Debug Mode)

```python
@browser(close_on_crash=False)  # Keeps browser open for manual CAPTCHA solving
```

---

## PROXY / INFRASTRUCTURE MANAGEMENT

### 1. IP Rotation Methods (change-ip.md)

| Method | Speed | Cost | Detection Risk |
|--------|-------|------|----------------|
| **Airplane Mode Toggle** | 10 seconds | Free | Low (real mobile IPs) |
| **Router Restart** | 2-3 min | Free | Low |
| **AWS API Gateway** | Instant | Very low ($/request) | Medium (datacenter) |
| **Proxy Services** (BrightData, Oxylab, IPRoyal) | Instant | $15/GB (residential) | Low |
| **Tor Network** (AnonSurf) | Slow | Free | High (known Tor IPs) |
| **VPN** (WindScribe, ProtonVPN) | Instant | Free/Paid | Medium-High |

### 2. IP Detection (ip_utils.py)

```python
from botasaurus.ip_utils import IPUtils
IPUtils.get_ip()          # Returns current public IP
IPUtils.get_ip_info()     # Returns geolocation, ISP, coordinates
# Falls back: checkip.amazonaws.com → api.ipify.org
```

### 3. Proxy Cycling

```python
@browser(proxy=["http://p1:8080", "http://p2:8080"])  
# Automatically cycles through proxies using itertools.cycle
```

### 4. Kubernetes Deployment (run-scraper-in-kubernetes.md)

- Google Cloud GKE cluster deployment
- GitHub Actions CI/CD pipeline
- Auto-scaling worker nodes
- Secrets management via GitHub Secrets
- BOTA CLI: `python -m bota create-cluster` / `delete-cluster`

### 5. Database Backends

- **SQLite** (default, file-based)
- **PostgreSQL** via Google Cloud SQL or Supabase
- Configurable via `Server.set_database_url()`

---

## REQUEST QUEUING AND SESSION HANDLING

### 1. Parallel Execution (p-limit)

All three decorators support `parallel` parameter:

```python
@browser(parallel=5)   # Run 5 browser instances in parallel
@request(parallel=10)  # Run 10 HTTP requests in parallel
@task(parallel=3)      # Run 3 tasks in parallel
```

Implementation uses `p-limit` library for concurrency control.

### 2. Async Queue Pattern

```python
@browser(async_queue=True)  # Returns queue object with .put() and .get()
queue = my_scraper()
queue.put(data1)
queue.put(data2)
results = queue.get()  # Drain and get results
```

### 3. Sequential Queue

```python
@browser(async_queue=True, sequential=True)
# Items processed one at a time in order
```

### 4. Duplicate Deduplication

```python
@browser(async_queue=True, skipDuplicateInput=True)
# Skips items already seen (uses Set with JSON serialization)
```

### 5. Caching System

```python
@browser(cache=True)                # Cache results to disk
@browser(cache="REFRESH")           # Force refresh cache
@browser(cache=True, expires_in=timedelta(hours=24))  # TTL
```

Cache backends: FileCacheStorage (default), SQLite, PostgreSQL.

Cache key: SHA256 hash of function name + serialized input data.

### 6. Retry Logic

```python
@browser(max_retry=3, retry_wait=5)  # Retry up to 3 times, wait 5s between
```

### 7. Session Reuse

```python
@browser(reuse_driver=True)  # Reuse browser instance across tasks
```

---

## SCRAPER TYPES

### 1. Browser Scraper (`@browser`)

Uses modified Selenium/Playwright with anti-detection. Supports:
- Headless mode
- XVFB virtual display (Linux headless servers)
- Profile persistence
- Extension loading
- Resource blocking

### 2. Request Scraper (`@request`)

Uses `botasaurus_requests` (wraps `requests` library with proxy/UA support):

```python
@request(proxy="http://proxy:8080", user_agent="...")
def my_scraper(request, data):
    response = request.get("https://example.com")
    return response.json()
```

### 3. Task Scraper (`@task`)

Pure data processing, no network:

```python
@task(parallel=10)
def process_data(data):
    return transform(data)
```

---

## SERVER-SIDE FEATURES

### 1. Master/Worker Architecture

- `MasterExecutor` — distributes tasks to workers
- `WorkerExecutor` — executes tasks on worker nodes
- `TaskExecutor` — standalone execution
- Kubernetes-native with auto-scaling

### 2. Rate Limiting

```python
Server.rate_limit = {"browser": 1, "request": 30, "task": 30}
```

### 3. Data Filtering & Sorting

Built-in UI for filtering scraped data:
- SearchTextInput, MinNumberInput, MaxNumberInput
- SingleSelectDropdown, MultiSelectDropdown, BoolSelectDropdown
- IsTrueCheckbox, IsNullCheckbox, etc.

### 4. Data Views

Multiple views of the same scraped data:
- Field (single field with optional map function)
- CustomField (derived from multiple fields)
- ExpandDictField (flatten nested dicts)
- ExpandListField (expand array items to rows)

### 5. Export Formats

- JSON, CSV, Excel, NDJSON
- Streamed writing for large datasets
- S3 upload support

---

## CRITICAL DEPENDENCIES (RELEVANT TO BYPASS)

| Package | Purpose |
|---------|---------|
| `rebrowser-playwright-core` | Patched Playwright without automation detection |
| `chrome-launcher` | Launch Chrome with custom flags via CDP |
| `botasaurus_driver` | Modified Selenium with anti-detection (proprietary) |
| `botasaurus_humancursor` | Bezier curve mouse movements |
| `botasaurus_requests` | HTTP requests with proxy/UA support |
| `botasaurus-controls` | Input UI controls |
| `p-limit` | Concurrency limiting |

---

## DETECTION EVASION SUMMARY

The framework's anti-detection strategy follows these layers:

1. **Network Layer**: Proxy rotation, IP diversity (mobile, residential, AWS API Gateway)
2. **TLS/HTTP Layer**: botasaurus_requests with proper headers, UA rotation
3. **Browser Fingerprint Layer**: Profile management, randomized window size, language, extensions
4. **Behavioral Layer**: HumanCursor Bezier movements, randomized sleep, referrer spoofing
5. **JavaScript VM Layer**: rebrowser-playwright-core removes `navigator.webdriver` and other automation markers
6. **Challenge Response Layer**: Cloudflare Turnstile/WAF bypass, bot detection checks
7. **Infrastructure Layer**: Kubernetes with multiple IPs, auto-scaling workers
