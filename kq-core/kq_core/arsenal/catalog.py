"""Curated Kali tool catalog (grounded in kali.org/tools/all-tools).

Each ToolSpec is a command TEMPLATE with placeholders the runner fills:
  {target} {ports} {wordlist} {threads} {rate} {extra}
Templates default to safe/standard usage; the agent supplies {extra} for customization.
Target types: web | url | host | network | domain | api | unknown.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ToolSpec:
    name: str
    binary: str
    category: str          # recon|dns|scan|web|fuzz|vuln|cred|wireless|exploit|postex|cloud|recon-osint|tls|sniff|c2|rat|malware|ad|evasion|firmware|iot|rf|ble|rfid|social|lateral|persistence|exfil
    template: str
    target_types: Tuple[str, ...]
    effectiveness: float = 0.6   # default rank within its target types (0..1)
    timeout: int = 600
    passive: bool = False        # passive/stealth-friendly vs active
    needs_wordlist: bool = False
    note: str = ""


def _t(*tts: str) -> Tuple[str, ...]:
    return tuple(tts)


# ── the catalog ───────────────────────────────────────────────────────────────
_SPECS: List[ToolSpec] = [
    # recon / dns / osint
    ToolSpec("subfinder", "subfinder", "dns", "subfinder -d {target} -silent {extra}", _t("domain"), 0.90, 300, True),
    ToolSpec("amass", "amass", "dns", "amass enum -d {target} {extra}", _t("domain"), 0.85, 900, True),
    ToolSpec("findomain", "findomain", "dns", "findomain -t {target} {extra}", _t("domain"), 0.75, 300, True),
    ToolSpec("dnsx", "dnsx", "dns", "dnsx -d {target} -silent {extra}", _t("domain"), 0.7, 300, True),
    ToolSpec("dnsrecon", "dnsrecon", "dns", "dnsrecon -d {target} {extra}", _t("domain"), 0.7, 300, True),
    ToolSpec("fierce", "fierce", "dns", "fierce --domain {target} {extra}", _t("domain"), 0.6, 300, True),
    ToolSpec("dnstwist", "dnstwist", "recon-osint", "dnstwist {target} {extra}", _t("domain"), 0.5, 300, True),
    ToolSpec("theharvester", "theHarvester", "recon-osint", "theHarvester -d {target} -b all {extra}", _t("domain"), 0.65, 300, True),

    # http probing / fingerprint
    ToolSpec("httpx", "httpx", "recon", "httpx -u {target} -silent -sc -title -tech-detect {extra}", _t("url", "web", "host"), 0.8, 300, True),
    ToolSpec("whatweb", "whatweb", "web", "whatweb {target} {extra}", _t("url", "web"), 0.7, 120, True),
    ToolSpec("wafw00f", "wafw00f", "web", "wafw00f {target} {extra}", _t("url", "web"), 0.65, 120, True),
    ToolSpec("katana", "katana", "recon", "katana -u {target} -silent {extra}", _t("url", "web"), 0.7, 300, True),
    ToolSpec("gau", "gau", "recon", "gau {target} {extra}", _t("domain", "url"), 0.6, 300, True),
    ToolSpec("waybackurls", "waybackurls", "recon", "waybackurls {target} {extra}", _t("domain", "url"), 0.55, 300, True),
    ToolSpec("eyewitness", "eyewitness", "recon", "eyewitness --web --single {target} {extra}", _t("url", "web"), 0.5, 300),

    # port / service scanning
    ToolSpec("nmap", "nmap", "scan", "nmap -sV -sC {ports} {extra} {target}", _t("host", "network"), 0.88, 1200),
    ToolSpec("rustscan", "rustscan", "scan", "rustscan -a {target} {extra}", _t("host", "network"), 0.8, 600),
    ToolSpec("masscan", "masscan", "scan", "masscan {target} -p{ports} --rate {rate} {extra}", _t("network", "host"), 0.75, 900, note="needs root"),
    ToolSpec("naabu", "naabu", "scan", "naabu -host {target} -silent {extra}", _t("host", "network"), 0.72, 600),
    ToolSpec("sslscan", "sslscan", "tls", "sslscan {target} {extra}", _t("host", "url", "web"), 0.6, 180, True),

    # vulnerability scanning
    ToolSpec("nuclei", "nuclei", "vuln", "nuclei -u {target} -silent {extra}", _t("url", "web", "host"), 0.95, 1200, True),
    ToolSpec("nikto", "nikto", "vuln", "nikto -host {target} {extra}", _t("url", "web"), 0.7, 900),
    ToolSpec("wpscan", "wpscan", "vuln", "wpscan --url {target} --enumerate vp,vt,u {extra}", _t("url", "web"), 0.85, 900),
    ToolSpec("searchsploit", "searchsploit", "vuln", "searchsploit {extra}", _t("unknown", "host", "url"), 0.6, 60, True),

    # content discovery / fuzzing (need wordlist)
    ToolSpec("ffuf", "ffuf", "fuzz", "ffuf -u {target}/FUZZ -w {wordlist} -t {threads} {extra}", _t("url", "web"), 0.85, 900, needs_wordlist=True),
    ToolSpec("feroxbuster", "feroxbuster", "fuzz", "feroxbuster -u {target} -w {wordlist} -t {threads} {extra}", _t("url", "web"), 0.85, 900, needs_wordlist=True),
    ToolSpec("gobuster", "gobuster", "fuzz", "gobuster dir -u {target} -w {wordlist} -t {threads} {extra}", _t("url", "web"), 0.8, 900, needs_wordlist=True),
    ToolSpec("dirsearch", "dirsearch", "fuzz", "dirsearch -u {target} {extra}", _t("url", "web"), 0.75, 900),
    ToolSpec("arjun", "arjun", "fuzz", "arjun -u {target} {extra}", _t("url", "web", "api"), 0.6, 600),

    # web exploitation
    ToolSpec("sqlmap", "sqlmap", "exploit", "sqlmap -u {target} --batch {extra}", _t("url", "web", "api"), 0.8, 1800, note="active injection"),
    ToolSpec("commix", "commix", "exploit", "commix -u {target} --batch {extra}", _t("url", "web"), 0.6, 1200, note="active injection"),
    ToolSpec("dalfox", "dalfox", "exploit", "dalfox url {target} {extra}", _t("url", "web"), 0.7, 900, note="xss"),
    ToolSpec("crlfuzz", "crlfuzz", "exploit", "crlfuzz -u {target} {extra}", _t("url", "web"), 0.5, 600),

    # credentials / brute (active — operator supplies users/wordlist via {extra})
    ToolSpec("hydra", "hydra", "cred", "hydra {extra} {target}", _t("host", "url"), 0.7, 1800, note="active brute; supply -L/-P/service via extra"),
    ToolSpec("medusa", "medusa", "cred", "medusa -h {target} {extra}", _t("host",), 0.6, 1800, note="active brute"),
    ToolSpec("john", "john", "cred", "john {extra}", _t("unknown",), 0.7, 1800, note="offline hash cracking"),
    ToolSpec("hashcat", "hashcat", "cred", "hashcat {extra}", _t("unknown",), 0.75, 3600, note="offline GPU cracking"),

    # SMB / AD / post-exploitation
    ToolSpec("enum4linux-ng", "enum4linux-ng", "postex", "enum4linux-ng {target} {extra}", _t("host",), 0.75, 600),
    ToolSpec("netexec", "netexec", "postex", "netexec {extra} {target}", _t("host", "network"), 0.85, 900, note="supply protocol+creds via extra"),
    ToolSpec("crackmapexec", "crackmapexec", "postex", "crackmapexec {extra} {target}", _t("host", "network"), 0.8, 900),
    ToolSpec("responder", "responder", "postex", "responder {extra}", _t("network",), 0.6, 600, note="LLMNR/NBNS poisoning; -I iface via extra"),
    ToolSpec("bloodhound-python", "bloodhound-python", "postex", "bloodhound-python -d {target} {extra}", _t("domain",), 0.7, 900, note="supply -u/-p/-c via extra"),
    ToolSpec("certipy", "certipy", "postex", "certipy {extra}", _t("domain", "host"), 0.65, 900, note="AD CS"),

    # cloud
    ToolSpec("cloud-enum", "cloud_enum", "cloud", "cloud_enum -k {target} {extra}", _t("domain", "unknown"), 0.6, 600, True),
    ToolSpec("cloudbrute", "cloudbrute", "cloud", "cloudbrute -d {target} {extra}", _t("domain",), 0.55, 600),
    ToolSpec("prowler", "prowler", "cloud", "prowler {extra}", _t("unknown",), 0.7, 1800, note="AWS/Azure/GCP checks"),
    ToolSpec("scoutsuite", "scout", "cloud", "scout {extra}", _t("unknown",), 0.65, 1800),

    # ── C2 Frameworks ────────────────────────────────────────
    ToolSpec("sliver", "sliver-server", "c2", "sliver-server {extra}", _t("host",), 0.90, 3600, note="Go C2, multi-protocol"),
    ToolSpec("havoc", "havoc", "c2", "havoc server --profile {extra}", _t("host",), 0.85, 3600, note="Modern C2, malleable profiles"),
    ToolSpec("mythic", "mythic-cli", "c2", "mythic-cli start {extra}", _t("host",), 0.85, 3600, note="Docker-based C2 platform"),
    ToolSpec("covenant", "covenant", "c2", "covenant {extra}", _t("host",), 0.75, 3600, note=".NET C2, requires dotnet"),
    ToolSpec("merlin", "merlin", "c2", "merlin server {extra}", _t("host",), 0.75, 3600, note="Go HTTP/2, JA3 randomization"),
    ToolSpec("empire", "empire", "c2", "empire --rest {extra}", _t("host",), 0.70, 3600, note="PowerShell/Python agents"),
    ToolSpec("metasploit", "msfconsole", "c2", "msfconsole -q {extra}", _t("host", "web"), 0.85, 3600, note="Framework, multi-protocol"),

    # ── Malware Development / Payload Generation ────────────
    ToolSpec("msfvenom", "msfvenom", "malware", "msfvenom -p {extra}", _t("host",), 0.90, 300, note="Multi-platform payload gen"),
    ToolSpec("donut", "donut", "malware", "donut -f {extra}", _t("host",), 0.85, 300, note="PE/.NET to shellcode"),
    ToolSpec("scarecrow", "ScareCrow", "evasion", "ScareCrow -I {extra}", _t("host",), 0.80, 300, note="ETW patching, syscall injection"),
    ToolSpec("freeze", "freeze", "evasion", "freeze {extra}", _t("host",), 0.75, 300, note="AMSI/ETW patching"),
    ToolSpec("syswhispers3", "syswhispers3", "evasion", "syswhispers3 {extra}", _t("host",), 0.80, 300, note="Direct syscall generation"),
    ToolSpec("veil", "veil", "evasion", "veil {extra}", _t("host",), 0.60, 300, note="Payload obfuscation framework"),

    # ── Active Directory Tools ───────────────────────────────
    ToolSpec("impacket-secretsdump", "impacket-secretsdump", "ad", "impacket-secretsdump {target} {extra}", _t("host",), 0.90, 600, note="DCSync/registry dump"),
    ToolSpec("impacket-GetUserSPNs", "impacket-GetUserSPNs", "ad", "impacket-GetUserSPNs {target} -request {extra}", _t("host",), 0.85, 600, note="Kerberoasting"),
    ToolSpec("impacket-GetNPUsers", "impacket-GetNPUsers", "ad", "impacket-GetNPUsers {target} -format hashcat {extra}", _t("host",), 0.85, 600, note="AS-REP roasting"),
    ToolSpec("impacket-psexec", "impacket-psexec", "ad", "impacket-psexec {target} {extra}", _t("host",), 0.85, 300, note="Remote exec via SMB"),
    ToolSpec("impacket-wmiexec", "impacket-wmiexec", "ad", "impacket-wmiexec {target} {extra}", _t("host",), 0.85, 300, note="Remote exec via WMI"),
    ToolSpec("mimikatz", "mimikatz", "ad", "mimikatz.exe 'privilege::debug' 'sekurlsa::logonpasswords' {extra}", _t("host",), 0.90, 300, note="Credential extraction"),
    ToolSpec("rubeus", "Rubeus.exe", "ad", "Rubeus.exe {extra}", _t("host",), 0.85, 300, note="Kerberos manipulation"),
    ToolSpec("certipy-ad", "certipy", "ad", "certipy {extra}", _t("host", "domain"), 0.85, 600, note="ADCS exploitation ESC1-13"),
    ToolSpec("petitpotam", "PetitPotam.exe", "ad", "PetitPotam.exe {extra}", _t("host",), 0.80, 300, note="NTLM coercion via EFSRPC"),
    ToolSpec("coercer", "coercer", "ad", "coercer {extra}", _t("host",), 0.80, 300, note="NTLM coercion multi-method"),

    # ── Kubernetes / Container ────────────────────────────
    ToolSpec("kube-hunter", "kube-hunter", "cloud", "kube-hunter --remote {extra}", _t("host", "cloud"), 0.85, 600, True, note="K8s vuln scanner"),
    ToolSpec("cdk", "cdk", "cloud", "cdk evaluate {extra}", _t("host", "cloud"), 0.80, 600, note="Container pentest toolkit"),
    ToolSpec("peirates", "peirates", "cloud", "peirates {extra}", _t("host", "cloud"), 0.80, 600, note="K8s post-exploitation"),
    ToolSpec("kubeletctl", "kubeletctl", "cloud", "kubeletctl {extra}", _t("host", "cloud"), 0.80, 300, note="Kubelet API exploit"),
    ToolSpec("trivy", "trivy", "cloud", "trivy image {extra}", _t("host", "cloud"), 0.75, 600, True, note="Container vuln scanner"),

    # ── AWS Cloud Specific ──────────────────────────────────
    ToolSpec("pacu", "pacu", "cloud", "pacu --session {extra}", _t("cloud",), 0.90, 1800, True, note="AWS exploitation framework"),
    ToolSpec("cloudmapper", "cloudmapper.py", "cloud", "cloudmapper.py collect --account {extra}", _t("cloud",), 0.85, 1800, True, note="AWS visualization+audit"),
    ToolSpec("enumerate-iam", "enumerate-iam", "cloud", "enumerate-iam --access-key {extra}", _t("cloud",), 0.85, 600, True, note="IAM permission enumeration"),
    ToolSpec("pmapper", "pmapper", "cloud", "pmapper graph --profile {extra}", _t("cloud",), 0.80, 900, True, note="IAM escalation path mapper"),
    ToolSpec("cloudsplaining", "cloudsplaining", "cloud", "cloudsplaining scan --input-file {extra}", _t("cloud",), 0.80, 300, True, note="IAM least-privilege audit"),
    ToolSpec("gcpbucketbrute", "gcpbucketbrute", "cloud", "gcpbucketbrute -f {extra}", _t("cloud",), 0.75, 600, True, note="GCP bucket enumeration"),

    # ── Firmware / IoT Tools ──────────────────────────────────
    ToolSpec("binwalk", "binwalk", "firmware", "binwalk -Me {extra}", _t("firmware", "iot"), 0.90, 1800, note="Firmware extraction+analysis"),
    ToolSpec("firmware-mod-kit", "extract-firmware.sh", "firmware", "extract-firmware.sh {extra}", _t("firmware", "iot"), 0.80, 1800, note="Firmware extraction+repack"),
    ToolSpec("openocd", "openocd", "iot", "openocd -f {extra}", _t("iot",), 0.80, 3600, note="On-chip debugger JTAG/SWD"),
    ToolSpec("flashrom", "flashrom", "iot", "flashrom -p {extra}", _t("iot",), 0.80, 600, note="SPI flash read/write/erase"),
    ToolSpec("bus-pirate", "bus-pirate", "iot", "bus-pirate {extra}", _t("iot",), 0.75, 3600, note="Universal bus interface"),

    # ── Wireless / WiFi Tools ────────────────────────────────
    ToolSpec("aircrack-ng", "aircrack-ng", "wireless", "aircrack-ng {extra}", _t("wireless",), 0.90, 3600, note="WPA/WPA2 cracking"),
    ToolSpec("hcxdumptool", "hcxdumptool", "wireless", "hcxdumptool {extra}", _t("wireless",), 0.85, 3600, note="PMKID/handshake capture"),
    ToolSpec("hcxtools", "hcxtools", "wireless", "hcxtools {extra}", _t("wireless",), 0.75, 600, note="WPA hash conversion"),
    ToolSpec("reaver", "reaver", "wireless", "reaver {extra}", _t("wireless",), 0.75, 3600, note="WPS PIN brute force"),
    ToolSpec("wifite", "wifite", "wireless", "wifite {extra}", _t("wireless",), 0.80, 3600, note="Automated wireless auditor"),
    ToolSpec("airgeddon", "airgeddon", "wireless", "airgeddon {extra}", _t("wireless",), 0.80, 3600, note="Multi-purpose wireless"),
    ToolSpec("eaphammer", "eaphammer", "wireless", "eaphammer {extra}", _t("wireless",), 0.80, 3600, note="Evil twin+RADIUS relay"),
    ToolSpec("bettercap", "bettercap", "wireless", "bettercap -eval '{extra}'", _t("wireless", "ble", "rfid"), 0.85, 3600, note="WiFi/BLE/HID Swiss knife"),

    # ── SDR / RF Tools ───────────────────────────────────────
    ToolSpec("gnuradio", "gnuradio-companion", "rf", "gnuradio-companion {extra}", _t("rf",), 0.70, 3600, note="SDR signal processing"),
    ToolSpec("hackrf", "hackrf_transfer", "rf", "hackrf_transfer {extra}", _t("rf",), 0.75, 600, note="SDR transceiver 1MHz-6GHz"),
    ToolSpec("rtl-sdr", "rtl_sdr", "rf", "rtl_sdr {extra}", _t("rf",), 0.70, 600, note="RTL-SDR receiver"),

    # ── Bluetooth / BLE Tools ───────────────────────────────
    ToolSpec("ubertooth", "ubertooth", "ble", "ubertooth {extra}", _t("ble",), 0.75, 600, note="Bluetooth packet capture"),

    # ── RFID / NFC Tools ─────────────────────────────────────
    ToolSpec("proxmark3", "pm3", "rfid", "pm3 {extra}", _t("rfid",), 0.85, 600, note="RFID/NFC research tool"),
    ToolSpec("mfoc", "mfoc", "rfid", "mfoc {extra}", _t("rfid",), 0.75, 600, note="MIFARE Classic cracker"),

    # ── Social Engineering Tools ─────────────────────────────
    ToolSpec("evilginx2", "evilginx2", "social", "evilginx2 -p {extra}", _t("social",), 0.85, 3600, note="MFA token capture"),
    ToolSpec("gophish", "gophish", "social", "gophish {extra}", _t("social",), 0.85, 3600, note="Phishing campaign framework"),
    ToolSpec("modlishka", "modlishka", "social", "modlishka {extra}", _t("social",), 0.75, 3600, note="Reverse proxy MFA bypass"),
    ToolSpec("setoolkit", "setoolkit", "social", "setoolkit {extra}", _t("social",), 0.70, 600, note="Multi-vector SET"),

    # ── Lateral Movement / Pivoting ──────────────────────────
    ToolSpec("chisel", "chisel", "lateral", "chisel {extra}", _t("host",), 0.85, 3600, note="TCP tunnel over HTTP"),
    ToolSpec("ligolo-ng", "ligolo-ng", "lateral", "ligolo-ng {extra}", _t("host",), 0.80, 3600, note="TUN reverse tunnel"),
    ToolSpec("socat", "socat", "lateral", "socat {extra}", _t("host",), 0.70, 300, note="Bidirectional relay"),
    ToolSpec("ncat", "ncat", "lateral", "ncat {extra}", _t("host",), 0.75, 300, note="SSL-enabled netcat"),

    # ── Persistence Tools ────────────────────────────────────
    ToolSpec("impacket-goldenpac", "impacket-goldenPac", "persistence", "impacket-goldenPac {target} {extra}", _t("host",), 0.85, 600, note="Golden ticket + PSExec"),

    # ── Exfiltration Tools ───────────────────────────────────
    ToolSpec("dnsteal", "dnsteal", "exfil", "dnsteal {extra}", _t("host",), 0.65, 3600, note="DNS exfiltration server"),
]

TOOLS: Dict[str, ToolSpec] = {s.name: s for s in _SPECS}
# Also index by binary so aliases (crackmapexec/netexec) resolve.
_BY_BINARY: Dict[str, ToolSpec] = {s.binary: s for s in _SPECS}


def get(name: str) -> Optional[ToolSpec]:
    return TOOLS.get(name) or _BY_BINARY.get(name)


def by_category(category: str) -> List[ToolSpec]:
    return sorted([s for s in _SPECS if s.category == category], key=lambda s: s.effectiveness, reverse=True)


def for_target_type(target_type: str, *, passive_only: bool = False) -> List[ToolSpec]:
    out = [s for s in _SPECS if target_type in s.target_types and (s.passive or not passive_only)]
    return sorted(out, key=lambda s: s.effectiveness, reverse=True)


def all_specs() -> List[ToolSpec]:
    return list(_SPECS)
