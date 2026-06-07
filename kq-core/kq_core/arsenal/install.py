"""Tool installation registry and auto-installer.

Maps each tool in the catalog to its install method.
Supports: apt, pip, git, go, docker, curl, pipx, kali meta-package, builtin.
"""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from typing import Optional

# ═══════════════════════════════════════════════════════════
# INSTALL METHOD REGISTRY
# ═══════════════════════════════════════════════════════════
# Format: tool_name → "method:package_or_url"
# Methods: apt, pip, git, go, docker, curl, pipx, kali, builtin, manual

INSTALL_METHODS: dict[str, str] = {
    # ── Recon / DNS (built-in or apt) ──
    "subfinder":     "apt:subfinder",
    "amass":         "apt:amass",
    "findomain":     "apt:findomain",
    "dnsx":          "apt:dnsx",
    "dnsrecon":      "apt:dnsrecon",
    "fierce":        "apt:fierce",
    "dnstwist":      "apt:dnstwist",
    "theharvester":  "apt:theharvester",

    # ── HTTP / Web ──
    "httpx":         "apt:httpx-toolkit",
    "whatweb":       "apt:whatweb",
    "wafw00f":       "apt:wafw00f",
    "gau":           "go:github.com/lc/gau/v2/cmd/gau",
    "katana":        "go:github.com/projectdiscovery/katana/cmd/katana",
    "waybackurls":   "go:github.com/tomnomnom/waybackurls",
    "eyewitness":    "apt:eyewitness",

    # ── Scanning ──
    "nmap":          "builtin",
    "rustscan":      "git:https://github.com/RustScan/RustScan",
    "masscan":       "apt:masscan",
    "naabu":         "apt:naabu",
    "sslscan":       "apt:sslscan",

    # ── Vuln scanning ──
    "nuclei":        "apt:nuclei",
    "nikto":         "apt:nikto",
    "wpscan":        "apt:wpscan",
    "searchsploit":  "builtin",

    # ── Fuzzing ──
    "ffuf":          "apt:ffuf",
    "feroxbuster":   "apt:feroxbuster",
    "gobuster":      "apt:gobuster",
    "dirsearch":     "apt:dirsearch",
    "arjun":         "pip:arjun",

    # ── Web exploitation ──
    "sqlmap":        "apt:sqlmap",
    "commix":        "apt:commix",
    "dalfox":        "go:github.com/hahwul/dalfox/v2",
    "crlfuzz":       "go:github.com/dwisiswant0/crlfuzz/cmd/crlfuzz",

    # ── Credentials ──
    "hydra":         "apt:hydra",
    "medusa":        "apt:medusa",
    "john":          "apt:john",
    "hashcat":       "apt:hashcat",

    # ── Post-exploitation ──
    "enum4linux-ng": "apt:enum4linux-ng",
    "netexec":       "apt:netexec",
    "crackmapexec":  "apt:crackmapexec",
    "responder":     "apt:responder",
    "bloodhound-python": "pip:bloodhound",
    "certipy":       "pip:certipy-ad",
    "certipy-ad":    "pip:certipy-ad",

    # ── Cloud (apt/pip) ──
    "cloud-enum":    "apt:cloud-enum",
    "cloudbrute":    "apt:cloudbrute",
    "prowler":       "git:https://github.com/prowler-cloud/prowler",
    "scoutsuite":    "git:https://github.com/nccgroup/ScoutSuite",
    "pacu":          "git:https://github.com/RhinoSecurityLabs/pacu",
    "cloudmapper":   "git:https://github.com/duo-labs/cloudmapper",
    "enumerate-iam": "git:https://github.com/andresriancho/enumerate-iam",
    "pmapper":       "pip:principalmapper",
    "cloudsplaining":"pip:cloudsplaining",
    "gcpbucketbrute":"git:https://github.com/RhinoSecurityLabs/GCPBucketBrute",
    "kube-hunter":   "pip:kube-hunter",
    "cdk":           "git:https://github.com/cdk-team/CDK",
    "peirates":      "git:https://github.com/inguardians/peirates",
    "kubeletctl":    "git:https://github.com/cyberark/kubeletctl",
    "trivy":         "apt:trivy",

    # ── C2 Frameworks ──
    "sliver":        "git:https://github.com/BishopFox/sliver",
    "havoc":         "git:https://github.com/HavocFramework/Havoc",
    "mythic":        "git:https://github.com/its-a-feature/Mythic",
    "covenant":      "git:https://github.com/cobbr/Covenant",
    "merlin":        "git:https://github.com/Ne0nd0g/merlin",
    "empire":        "git:https://github.com/BC-SECURITY/Empire",
    "metasploit":    "apt:metasploit-framework",

    # ── Malware dev ──
    "msfvenom":      "builtin",  # part of metasploit
    "donut":         "git:https://github.com/TheWover/donut",
    "scarecrow":     "git:https://github.com/Tylous/ScareCrow",
    "freeze":        "git:https://github.com/optiv/Freeze",
    "syswhispers3":  "git:https://github.com/klezVirus/SysWhispers3",
    "veil":          "apt:veil",

    # ── AD Tools ──
    "impacket-secretsdump": "apt:impacket-scripts",
    "impacket-GetUserSPNs": "apt:impacket-scripts",
    "impacket-GetNPUsers":  "apt:impacket-scripts",
    "impacket-psexec":      "apt:impacket-scripts",
    "impacket-wmiexec":     "apt:impacket-scripts",
    "impacket-goldenpac":   "apt:impacket-scripts",
    "mimikatz":      "git:https://github.com/gentilkiwi/mimikatz",
    "rubeus":        "git:https://github.com/GhostPack/Rubeus",
    "petitpotam":    "git:https://github.com/topotam/PetitPotam",
    "coercer":       "git:https://github.com/p0dalirius/Coercer",

    # ── Firmware / IoT ──
    "binwalk":       "apt:binwalk",
    "firmware-mod-kit": "apt:firmware-mod-kit",
    "openocd":       "apt:openocd",
    "flashrom":      "apt:flashrom",
    "bus-pirate":    "manual:hardware — requires physical Bus Pirate device + firmware",

    # ── Wireless ──
    "aircrack-ng":   "apt:aircrack-ng",
    "hcxdumptool":   "apt:hcxdumptool",
    "hcxtools":      "apt:hcxtools",
    "reaver":        "apt:reaver",
    "wifite":        "apt:wifite",
    "airgeddon":     "apt:airgeddon",
    "eaphammer":     "git:https://github.com/s0lst1c3/eaphammer",
    "bettercap":     "apt:bettercap",

    # ── RF / SDR ──
    "gnuradio":      "apt:gnuradio",
    "hackrf":        "apt:hackrf",
    "rtl-sdr":       "apt:rtl-sdr",

    # ── BLE ──
    "ubertooth":     "apt:ubertooth",

    # ── RFID ──
    "proxmark3":     "apt:proxmark3",
    "mfoc":          "apt:mfoc",

    # ── Social Engineering ──
    "evilginx2":     "git:https://github.com/kgretzky/evilginx2",
    "gophish":       "git:https://github.com/gophish/gophish",
    "modlishka":     "git:https://github.com/drk1wi/Modlishka",
    "setoolkit":     "apt:setoolkit",

    # ── Lateral / Pivoting ──
    "chisel":        "apt:chisel",
    "ligolo-ng":     "git:https://github.com/nicocha30/ligolo-ng",
    "socat":         "apt:socat",
    "ncat":          "apt:ncat",

    # ── Exfiltration ──
    "dnsteal":       "git:https://github.com/m57/dnsteal",
}

# ═══════════════════════════════════════════════════════════
# INSTALLER
# ═══════════════════════════════════════════════════════════

def install_tool(tool_name: str, method: Optional[str] = None) -> dict:
    """Install a single tool using its registered method.

    Returns dict with: ok, tool, method, output, error
    """
    if method is None:
        method = INSTALL_METHODS.get(tool_name)
        if method is None:
            return {"ok": False, "tool": tool_name, "error": "no install method registered"}

    parts = method.split(":", 1)
    meth, target = parts[0], parts[1] if len(parts) > 1 else ""

    try:
        if meth == "builtin":
            return {"ok": True, "tool": tool_name, "method": "builtin",
                    "output": "already available on Kali"}

        elif meth == "apt":
            result = subprocess.run(
                ["apt-get", "install", "-y", "-qq", target],
                capture_output=True, text=True, timeout=300
            )
            ok = result.returncode == 0
            return {"ok": ok, "tool": tool_name, "method": f"apt:{target}",
                    "output": result.stdout[-500:], "error": result.stderr[-200:] if not ok else ""}

        elif meth == "pip":
            # Try multiple pip approaches for venv/container compatibility
            result = None
            for cmd in [
                [sys.executable, "-m", "pip", "install", target, "--break-system-packages"],
                ["pip3", "install", target, "--break-system-packages"],
                ["python3", "-m", "pip", "install", target, "--break-system-packages"],
            ]:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    if result.returncode == 0:
                        break
                except Exception:
                    continue
            if result is None:
                return {"ok": False, "tool": tool_name, "error": "no working pip found"}
            ok = result.returncode == 0
            return {"ok": ok, "tool": tool_name, "method": f"pip:{target}",
                    "output": result.stdout[-500:], "error": result.stderr[-200:] if not ok else ""}

        elif meth == "git":
            # Clone to /opt/kq-tools/<name>
            import os
            dest = f"/opt/kq-tools/{tool_name}"
            if os.path.exists(dest):
                return {"ok": True, "tool": tool_name, "method": f"git:{target}",
                        "output": f"already cloned at {dest}"}
            os.makedirs("/opt/kq-tools", exist_ok=True)
            result = subprocess.run(
                ["git", "clone", "--depth", "1", target, dest],
                capture_output=True, text=True, timeout=600
            )
            ok = result.returncode == 0
            msg = f"cloned to {dest}"
            # Try pip install if setup.py/pyproject.toml exists
            if ok and (os.path.exists(f"{dest}/setup.py") or os.path.exists(f"{dest}/pyproject.toml")):
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", dest, "--break-system-packages"],
                    capture_output=True, text=True, timeout=300
                )
                msg += " + pip installed"
            return {"ok": ok, "tool": tool_name, "method": f"git:{target}",
                    "output": msg, "error": result.stderr[-200:] if not ok else ""}

        elif meth == "go":
            result = subprocess.run(
                ["go", "install", target + "@latest"],
                capture_output=True, text=True, timeout=300
            )
            ok = result.returncode == 0
            return {"ok": ok, "tool": tool_name, "method": f"go:{target}",
                    "output": result.stdout[-300:], "error": result.stderr[-200:] if not ok else ""}

        elif meth == "docker":
            result = subprocess.run(
                ["docker", "pull", target],
                capture_output=True, text=True, timeout=600
            )
            ok = result.returncode == 0
            return {"ok": ok, "tool": tool_name, "method": f"docker:{target}",
                    "output": result.stdout[-300:], "error": result.stderr[-200:] if not ok else ""}

        elif meth == "curl":
            dest = f"/usr/local/bin/{tool_name}"
            result = subprocess.run(
                ["curl", "-sSL", target, "-o", dest],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
            ok = result.returncode == 0
            return {"ok": ok, "tool": tool_name, "method": f"curl:{target}",
                    "output": f"downloaded to {dest}", "error": result.stderr[-200:] if not ok else ""}

        elif meth == "manual":
            return {"ok": True, "tool": tool_name, "method": "manual",
                    "output": f"Manual install required. See: {target}"}

        else:
            return {"ok": False, "tool": tool_name, "error": f"unknown method: {meth}"}

    except subprocess.TimeoutExpired:
        return {"ok": False, "tool": tool_name, "error": "installation timed out"}
    except Exception as e:
        return {"ok": False, "tool": tool_name, "error": str(e)}


def install_all(categories: Optional[list[str]] = None, skip_builtin: bool = True,
                skip_manual: bool = True, skip_git: bool = False) -> dict:
    """Install all registered tools, optionally filtered by category.

    Returns: total, ok, failed, skipped, results per tool
    """
    results = {}
    ok_count = 0
    fail_count = 0
    skip_count = 0

    for tool_name, method in sorted(INSTALL_METHODS.items()):
        parts = method.split(":", 1)
        meth = parts[0]

        # Skip logic
        if skip_builtin and meth == "builtin":
            skip_count += 1
            continue
        if skip_manual and meth == "manual":
            skip_count += 1
            continue
        if skip_git and meth == "git":
            skip_count += 1
            continue
        # Skip if binary already exists
        if meth == "apt":
            bin_check = parts[1] if len(parts) > 1 else tool_name
        else:
            bin_check = tool_name
        # Don't skip git clones — check repo dir instead
        if meth != "git":
            import shutil
            if shutil.which(bin_check):
                skip_count += 1
                results[tool_name] = {"ok": True, "action": "skipped", "reason": "already installed"}
                continue

        # Category filter
        if categories:
            from .catalog import get as get_tool
            spec = get_tool(tool_name)
            if spec and spec.category not in categories:
                skip_count += 1
                continue

        result = install_tool(tool_name, method)
        results[tool_name] = result
        if result["ok"]:
            ok_count += 1
        else:
            fail_count += 1

    return {
        "total": len(INSTALL_METHODS),
        "ok": ok_count,
        "failed": fail_count,
        "skipped": skip_count,
        "results": results,
    }


def check_missing(tool_name: str) -> bool:
    """Return True if the tool's binary is NOT found on PATH."""
    import shutil
    method = INSTALL_METHODS.get(tool_name)
    if not method:
        return False  # unknown tools assumed present
    parts = method.split(":", 1)
    meth = parts[0]
    if meth in ("git", "docker", "manual"):
        # git/docker tools check for cloned dir or image
        if meth == "git":
            import os
            return not os.path.exists(f"/opt/kq-tools/{tool_name}")
        return False  # docker/manual assumed present
    if meth == "builtin":
        return False
    binary = parts[1] if len(parts) > 1 else tool_name
    return shutil.which(binary) is None


def ensure_installed(tool_name: str) -> dict:
    """Check if tool is installed; if not, install it. Returns status."""
    if not check_missing(tool_name):
        return {"ok": True, "tool": tool_name, "action": "already_installed"}
    return install_tool(tool_name)
