# WordPress Reconnaissance Playbook
## Lessons from live engagement against azzrk.com (WordPress 7.0 + Elementor 4.1.1)

### Phase 1: Passive Intel (0 touches)

1. **SSL certificate SAN extraction** — fastest subdomain discovery
```bash
openssl s_client -connect target.com:443 </dev/null 2>/dev/null | openssl x509 -text | grep DNS:
# Found: cpanel, webmail, webdisk, mail, autodiscover, cpcalendars, cpcontacts
```

2. **WHOIS** — reveals registrar (Dynadot), creation date (2022), nameservers (Contabo)
```bash
whois target.com | grep -iE 'Registrar|Creation|Name Server|Registrant'
```

3. **crt.sh** — certificate transparency logs
```bash
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u
```

### Phase 2: Technology Fingerprinting

1. **Server headers** — `curl -skI https://target.com/`
2. **Meta generator tags** — `grep -oP 'content="WordPress [^"]*"'`
3. **Plugin versions from CSS/JS** — `grep -oP 'wp-content/plugins/[^/"]+/[^"]+\.(css|js)\?ver=[^"]*'`
4. **Theme detection** — Kadence CSS in `wp-content/themes/kadence/`, inline `kadence-global-inline-css`

### Phase 3: User Enumeration

Priority order (most reliable first):
1. **REST API** — `GET /wp-json/wp/v2/users` — exposes ID, name, slug (username), author URL
2. **Password reset** — valid user → no error, invalid user → "no account exists" error
3. **Author archives** — `?author=1` through `?author=20`, check for 200 vs 404

### Phase 4: Plugin Exploitation Surface

For each detected plugin, check:
1. **Version in CVE databases** — searchsploit, wpscan, wordfence, patchstack
2. **Readme.txt** — often blocked by .htaccess, fallback to CSS/JS version detection
3. **AJAX handlers** — grep page source for `action=` parameters
4. **REST API routes** — `GET /wp-json/` lists all registered routes
5. **nopriv AJAX** — unauthenticated handlers are prime targets

### Phase 5: Common WordPress Dead Ends

These vectors ALWAYS fail on modern hardened WP:
- `xmlrpc.php` — disabled on 90% of sites (redirects to homepage)
- `wp-config.php~` — backup files blocked by `.htaccess`
- `.git/HEAD` — blocked
- Directory listing on `/wp-content/uploads/` — always disabled
- Default credentials — never work on production sites

### Phase 6: What ACTUALLY Works

On a well-hardened WordPress site, the most productive vectors are:
1. **Password brute force** — targeted wordlist from CeWL scraping + company intel
2. **File upload plugins at vulnerable versions** — dnd-upload-cf7, CF7 itself, Elementor addons
   - **dnd-upload-cf7 is the #1 priority target.** 16 CVEs, almost all unauthenticated file upload bypasses. See `references/dnd-upload-cf7-cve-history.md` for the complete version-to-exploit mapping.
   - Even at latest version (≥ 1.3.9.8), PNG-as-PHP upload may succeed — execution requires LFI or .htaccess injection.
3. **REST API enumeration** — users, pages, posts, media — always try this first
4. **cPanel/Webmail brute force** — if SSL cert reveals these subdomains
5. **PNG-as-PHP technique** — upload valid image with PHP code, then hunt for LFI to execute it

### Rate Limit Lessons

- cPanel brute force WILL IP-block you after ~10 attempts
- WordPress login throttles but is less aggressive
- Use `web_extract` as a fallback probing method (different outbound IP)
- Space all auth attempts 3-5 seconds apart
- Test rate limit sensitivity before scaling up
