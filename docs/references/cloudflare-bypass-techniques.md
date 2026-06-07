# Cloudflare Bypass Techniques & Tools Reference

## Overview
Compiled from GitHub Topics: `cloudflare-bypass`, `bypass-cloudflare`, `cloudflare-turnstile-bypass`, and pkg.go.dev analysis. 238+ repositories across all three topics.

---

## 1. Core Challenge Types Bypassed

| Challenge | Description | Bypass Approach |
|-----------|-------------|-----------------|
| **IUAM (I'm Under Attack Mode)** | JavaScript challenge served during DDoS protection | Browser fingerprinting, JS execution via headless browsers |
| **5-Second Challenge** | Classic Cloudflare JS challenge page | Automated browser solving, cookie relay |
| **Turnstile** | Cloudflare's CAPTCHA replacement (invisible/managed) | Real browser automation, API solvers, ML-based solvers |
| **WAF (Web Application Firewall)** | Layer 7 rule-based blocking | Header spoofing, request mimicry, proxy rotation |
| **Bot Fight Mode (BFM)** | Behavioral bot detection | Real browser profiles, human-like interaction patterns |
| **Browser Fingerprinting** | Canvas/WebGL/font detection | Source-level Chromium patches to spoof fingerprints |

---

## 2. Stealth Browsers & Driver Patches

The primary technique: **modify Chromium/Playwright/Puppeteer at the source level** to remove bot detection markers.

### Key Repositories

| Tool | Author | Technique |
|------|--------|-----------|
| **CloakBrowser** | CloakHQ | Stealth Chromium with source-level fingerprint patches; drop-in Playwright replacement; passes 30/30 bot detection tests |
| **undetected-chromedriver** | ultrafunkamsterdam | Custom Selenium Chromedriver that patches all automation detection vectors (Distil/Imperva/DataDome/Cloudflare IUAM) at the binary level |
| **camofox-browser** | jo-inc | Stealth headless browser for AI agents; drop-in Puppeteer/Playwright replacement |
| **puppeteer-real-browser** | ZFC-Digital | Puppeteer package that acts like a real browser, bypasses Cloudflare captchas |
| **patchright** | Kaliiiiiiiiii-Vinyzu | Undetected version of Playwright testing library (Python) |
| **patchright-nodejs** | Kaliiiiiiiiii-Vinyzu | Undetected NodeJS version of Playwright |
| **CloakQuest3r** | spyboy-productions | Security research tool for identifying origin IP exposure behind Cloudflare |

### Patching Techniques Used:
- Binary patching of `cdp`/`chromedriver` to remove `navigator.webdriver` flag
- Removing automation-specific JavaScript properties (`window.chrome`, `navigator.plugins`)
- Spoofing WebGL vendor/renderer strings
- Customizing font enumeration to appear natural
- Modifying network stack fingerprint (TLS cipher suites, HTTP/2 settings)
- Disabling automation extension detection

---

## 3. Scraping & Automation Frameworks

All-in-one solutions that combine multiple bypass layers.

| Tool | Author | Key Features |
|------|--------|--------------|
| **botasaurus** | omkarcloud | "All in One Framework to Build Undefeatable Scrapers" - tagged in both cloudflare-bypass and bypass-cloudflare |
| **zendriver** | cdpdriver | Blazing fast async-first undetectable web scraping; based on ultrafunkamsterdam/nodriver; Docker support |
| **reader** | vakra-dev | Open source web infra for AI - scrape, crawl, automate, clean markdown, browser sessions |
| **stealth-browser-mcp** | vibheksoni | AI-driven browser automation that bypasses anti-bot; writes network hooks; clones UIs |

---

## 4. Cloudflare-Specific Challenge Solvers

Tools that directly handle Cloudflare challenge pages.

| Tool | Author | Technique |
|------|--------|-----------|
| **cloudscraper** | VeNoMouS | Python module that identifies the IUAM challenge, solves the JavaScript, and resubmits with the clearance cookie |
| **CloudflareBypassForScraping** | sarperavci | Verification bypass script for web scraping |
| **cf-clearance** | vvanglro | Passes Cloudflare v2 challenge; obtains cf_clearance cookie with matching IP+UA |
| **cloudflare-solver** | Rutenoze | Solve Cloudflare Challenge 5s and Turnstile Captcha with Python |
| **BCFlare** | I2rys | NodeJS module to GET/POST and bypass website's Cloudflare |
| **cfbypass** | scaredos | CloudFlare Bypass/Resolver in Python (patched) |

### cf_clearance Cookie Relay Pattern:
1. Use a real browser (or patched driver) to solve the challenge once
2. Extract the `cf_clearance` cookie and User-Agent
3. Relay both cookie and matching UA to subsequent requests (curl, requests, etc.)
4. Cookie valid for the same IP; expires after ~30 min

---

## 5. Proxy & Infrastructure Bypasses

| Tool | Author | Technique |
|------|--------|-----------|
| **CloudProxy** | NoahCardoza | Proxy server that sits between client and target, handling Cloudflare challenges transparently |
| **pupflare** | unixfox | Webpage proxy that routes requests through Chromium (Puppeteer); bypasses Cloudflare anti-bot for any application (curl, etc.) |
| **docker-cloudflare-bypasser** | frederik-uni | Simple API running in container, returns user-agent and cookies |
| **aiohttp_chromium** | milahu | aiohttp-like interface to chromium; based on selenium_driverless |
| **chromedl** | rusq | Go library for scraping/downloading bypassing Cloudflare and browser checks |
| **curl-adapter** | el1s7 | Curl HTTP adapter switch for requests library; browser-like requests with custom TLS fingerprints |

---

## 6. Origin IP Discovery (WAF Bypass via Origin Exposure)

| Tool | Author | Technique |
|------|--------|-----------|
| **CloudPeler / CrimeFlare** | zidansec | Bypass Cloudflare WAF by discovering real IP; DNS history, certificate transparency logs |
| **CloudHound** | GuardIran | DNS history checkup, cross-site port attack, and other methods to detect original server IP |
| **bypass-cloudflare-get-real-IP** | bimantaraz | Subdomain enumeration, DNS lookup, MX check to find origin IP |
| **fav-up** | pielco11 | Favicon-based technique for origin IP discovery |

### Origin IP Discovery Techniques:
- **DNS History:** Check historical DNS records (SecurityTrails, crt.sh) before Cloudflare was enabled
- **Certificate Transparency Logs:** Search CT logs for subdomains pointing to origin
- **Subdomain Enumeration:** Brute-force subdomains that may resolve directly to origin
- **MX/SPF Records:** Mail server records often reveal origin IP
- **Cross-Site Port Attack:** Scan common ports on subdomains to find origin
- **Favicon Hash Matching:** Shodan search by favicon hash to find origin servers

---

## 7. Turnstile-Specific Solvers

Cloudflare Turnstile is their newer CAPTCHA replacement - a separate attack surface.

| Tool | Author | Technique |
|------|--------|-----------|
| **Turnstile-Solver** | Theyka | Python-based solver using patchright library; multi-threaded; API integration |
| **EzSolver** | ismoiloffS | Real Chrome browser solver; no paid APIs; local HTTP API; solves invisible + managed widgets; Windows/Linux |
| **turnstile_solver** | odell0111 | Python server; average solving time: 2 seconds |
| **Turnstile-Slip** | Iruko233 | Automated Cloudflare Turnstile challenge bypass; retrieves cf_clearance without human intervention |
| **Turnstile-Solver** | x404xx | REST API for bypassing Cloudflare Turnstile |
| **captcha_bypass** | lvjin521 | Python tool using YesCaptcha API |

### Turnstile Bypass Approaches:
- **Real Browser Automation:** Launch real Chrome, navigate to page, interact with checkbox, wait for token
- **API-Based Solvers:** Use captcha solving services (YesCaptcha, CapSolver, 2Captcha)
- **Embedded Browser Libraries:** patchright, playwright-stealth, puppeteer-extra with stealth plugin
- **Local HTTP API Pattern:** Run solver as local service → POST challenge params → get token back

---

## 8. DDoS Tools with Bypass Modules

These are attack tools that include Cloudflare bypass as a feature:

| Tool | Author | Description |
|------|--------|-------------|
| **MHDDoS** | MatrixTM | DDoS Attack Script Python3 with 56 methods; includes Cloudflare bypass |
| **KARMA-DDoS** | HyukIsBack | DDoS Panel with multiple bypasses (Cloudflare UAM, CAPTCHA, BFM, NOSEC / DDoS Guard / Google Shield / V Shield / Amazon) |
| **slowloris** | nikannafas04-sketch | Classic slowloris DDoS with Cloudflare bypass variant |

---

## 9. Commercial/API Services

| Service | Description |
|---------|-------------|
| **ScrapingBypass** | Web scraping API (Python, Curl, NodeJS, Java); dedicated Cloudflare bypass endpoints |
| **Bright Data** | Proxy + unblocking infrastructure with Cloudflare bypass |
| **luminati-io/bypass-cloudflare** | Methods to bypass Cloudflare using proxies, header spoofing, CAPTCHA solving, headless browsers |
| **solvercaptcha/cloudflare-demo** | Demo of CapSolver integration for Cloudflare Turnstile |

---

## 10. Key Technical Patterns Summary

### Fingerprint Evasion:
- `navigator.webdriver` = false/undefined
- `navigator.plugins.length` > 0
- `navigator.languages` = ["en-US", "en"]
- `window.chrome` object present
- WebGL renderer: matches real GPU
- Canvas fingerprint: stable across loads
- Font enumeration: realistic set
- `navigator.hardwareConcurrency`: matches real CPU
- Screen resolution/colorDepth: realistic

### Network-Level Evasion:
- TLS fingerprint matching real browsers (JA3/JA4 fingerprints)
- HTTP/2 settings matching Chrome/Firefox
- Header order matching real browsers
- Accept-Language, Accept-Encoding, Sec-Ch-UA headers

### Challenge Solving Flow:
```
Request → 403/503 + Challenge Page
  → Extract challenge script
  → Execute JS in real browser context
  → Submit solution → Get cf_clearance cookie
  → Relay cookie + matching UA + IP to actual requests
```

### Anti-Detection for Automation Frameworks:
- Source-level CDP (Chrome DevTools Protocol) patches
- Binary modification of chromedriver/playwright driver
- Disabling `--enable-automation` flag
- Loading browser extensions to mask automation
- Human-like mouse movements and timing
- Random delays between actions
