# Webshell Collections on Kali

## Default (apt-installed)

### /usr/share/webshells/
Base Kali webshells — small, focused collection:

| Dir | Files |
|-----|-------|
| php/ | php-backdoor.php, php-reverse-shell.php, qsd-php-backdoor.php, simple-backdoor.php, findsocket/php-findsock-shell.php |
| asp/ | cmdasp.asp, cmd-asp-5.1.asp |
| aspx/ | cmdasp.aspx |
| jsp/ | cmdjsp.jsp, jsp-reverse.jsp |
| cfm/ | cfexec.cfm |
| perl/ | perlcmd.cgi, perl-reverse-shell.pl |

Also symlinks: laudanum -> /usr/share/laudanum, seclists -> /usr/share/seclists/Web-Shells

### /usr/share/laudanum/
Injectable proxy/shell/DNS/file tools in PHP, ASP, ASPX, JSP, CFM. Includes WordPress plugin shell (laudanum.php) with templates for reverse shell, proxy, file browser, DNS, and host enumeration.

### /usr/share/seclists/Web-Shells/
61 files across PHP, JSP, CFM, WordPress, Magento, Vtiger, FuzzDB collections. Includes obfuscated variants, plugin shells, and login bypass shells.

## BlackArch (manually installed)

### /opt/blackarch-webshells/
216 net-new webshells from https://github.com/blackarch/webshells (deduplicated against all Kali defaults above).

| Language | Count | Highlights |
|----------|-------|------------|
| PHP | 206 | b374k (9.5K-line monster), c99 family (madnet/locus7s/PSych0/w4cking/unlimited), r57 family (kartal/Mohajer22/iFX/1.40/2.0), p0wny (411 lines), pws, WordPress CMSmap plugin shell, Safe Mode bypasses (PHP 4.4.2/5.1.2), Crystal, DxShell, Cyber, NCC, Liz0ziM, and ~180 more |
| Perl | 3 | dc.pl, perlweb_shell.pl, Perl Web Shell by RST-GHC |
| ASPX | 3 | aspxshell.aspx, cmd.asmx (SOAP web service shell — unique), shell.aspx |
| ASP | 1 | cmd-asp-5.1.asp (different variant from Kali's) |
| JSP | 1 | cmd.jsp |
| Ruby | 1 | srwsh.rb (CGI shell — Kali has zero Ruby webshells by default) |

## Deduplication methodology

When adding a new webshell collection, compare by SHA-256 hash against all existing collections to avoid duplicates:

```bash
# 1. Hash all existing webshells
find /usr/share/webshells /usr/share/laudanum /usr/share/seclists/Web-Shells \
  -type f -exec sha256sum {} \; > /tmp/installed.hashes

# 2. Hash new collection
cd /path/to/new/collection
find . -type f -exec sha256sum {} \; > /tmp/new.hashes

# 3. Find unique hashes (net-new files)
cut -d' ' -f1 /tmp/installed.hashes | sort > /tmp/ih.txt
cut -d' ' -f1 /tmp/new.hashes | sort > /tmp/nh.txt
comm -13 /tmp/ih.txt /tmp/nh.txt > /tmp/unique.hashes

# 4. Map hashes back to filenames and install
# (resolve filenames, copy unique files to target directory)
```

12 exact duplicates existed between BlackArch and Kali defaults (php-backdoor, php-reverse, simple-backdoor, php-findsock, findsock.c, perlcmd, perl-reverse, jsp-reverse, cmdjsp, cfexec, cmdasp.aspx, cmdasp.asp).

## Nuclei detection signatures

`/root/nuclei-templates/file/webshell/` — defensive signatures for detecting webshells. Useful for testing evasion.
