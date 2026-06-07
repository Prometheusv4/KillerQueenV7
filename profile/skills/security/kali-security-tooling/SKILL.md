---
name: kali-security-tooling
description: Install, fix, and manage offensive-security and OSINT tools on Kali Linux. Covers pipx (PEP 668), Python version quirks, and common tool-specific fixes.
---

# Kali Security Tooling

Kali Linux enforces PEP 668 — you cannot `pip install` system-wide.
Use `pipx` for Python CLI tools. Python 3.13+ shipped with Kali 2026.x
removes `pkg_resources` from setuptools >= 68, which breaks tools
that depend on the `eth` library (mythril, slither, some web3 tooling).

## Trigger conditions

- Any Python tool install fails with PEP 668 message.
- `ModuleNotFoundError: No module named 'pkg_resources'` from a
  security tool that depends on `eth` or older setuptools APIs.
- Kali-specific package management questions.

## Installing Python tools on Kali

```bash
# NEVER: pip install <tool>      ← blocked by PEP 668
# ALWAYS:
pipx install <tool>
pipx ensurepath                  # if binaries not in PATH
```

After install, binaries live in `~/.local/bin/`. If not found, run
`pipx ensurepath --force` and reload shell or export PATH manually.

## Python 3.13 + pkg_resources regression

**Symptom:**
```
ModuleNotFoundError: No module named 'pkg_resources'
```
Any tool importing the `eth` Python library (mythril, slither,
web3.py-based tools) will hit this on Python 3.13 because setuptools
>= 68 removed the standalone `pkg_resources` module that `eth`
imports at `eth/__init__.py` line 1.

**Fix — downgrade setuptools in the affected pipx venv:**
```bash
# Step 1: Find the venv
ls ~/.local/share/pipx/venvs/<tool-name>/

# Step 2: Install setuptools<68 via the venv's Python directly
# (pipx inject often installs silently to wrong location)
~/.local/share/pipx/venvs/<tool-name>/bin/python -m pip install 'setuptools<68'

# Step 3: Verify
<tool> version
```

**Why pipx inject fails silently:** `pipx inject <tool> setuptools`
may install setuptools but the venv's pip sometimes resolves to a
different site-packages. Using the venv's own `python -m pip` directly
is reliable.

**Affected tools (confirmed):**
- mythril — `eth/__init__.py` line 1: `import pkg_resources`
- Any tool with `eth` in its dependency tree (slither, web3.py CLI tools)

## Kali package management cheat sheet

| Goal | Command |
|------|---------|
| Search apt for security tool | `apt-cache search <tool>` |
| Install from Kali repo | `apt install -y <tool>` |
| Python CLI tool | `pipx install <tool>` |
| Python library (imported) | `apt install python3-<lib>` if packaged; else `pipx inject <existing-venv> <lib>` |
| Go tool | `go install <module>@latest` or `apt install <tool>` |
| Rust/cargo tool | `cargo install <tool>` |
| Node/npm tool | `npm install -g <tool>` |
| Binary from GitHub release | Download, review, extract to `/usr/local/bin/` |
| Check if installed | `which <tool>` or `dpkg -l \| grep <tool>` or `pipx list` |

## Tool-specific known fixes

### mythril (v0.24.x on Python 3.13)
```bash
pipx install mythril
~/.local/share/pipx/venvs/mythril/bin/python -m pip install 'setuptools<68'
myth version  # should output version, not traceback
```

### echidna (Solidity fuzzer)
Not in Kali apt. Not installable via `cargo install` (library-only crate).
Install from GitHub binary release or Docker:
```bash
# Option A: Docker (preferred)
docker pull ghcr.io/crytic/echidna/echidna:latest
alias echidna='docker run --rm -v $(pwd):/src ghcr.io/crytic/echidna/echidna:latest'

# Option B: Pre-built binary
# Check https://github.com/crytic/echidna/releases for latest Ubuntu tarball
```

### pwntools
```bash
pipx install pwntools
# CLI: pwn, checksec, cyclic, etc.
# Python import: from pwn import *  (works in venv/script context)
```

### claw-code (AI code generation CLI)
Rust binary. Clone and build from source — the `install.sh` script handles
everything (Rust toolchain check, cargo build, verification).
```bash
git clone https://github.com/ultraworkers/claw-code.git /opt/claw-code
cd /opt/claw-code && bash install.sh --release
cp rust/target/release/claw /usr/local/bin/claw
claw --version
```
Requires: rustc + cargo (already on Kali 2026.x). Build time ~2 min.
The binary is standalone — repo can be left at /opt/claw-code for updates.
Authenticate with `export ANTHROPIC_API_KEY=...` or `claw login` (OAuth).

### Robin (dark-web .onion summarizer)
Streamlit-based Tor scraper with LLM summarization via AgentRouter or
OpenRouter. Presumes a running Tor SOCKS proxy on localhost:9050.
```bash
# Clone to /opt/robin
git clone https://github.com/apurvsinghgautam/robin.git /opt/robin
cd /opt/robin
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# Configure LLM backend in .env:
#   AGENTROUTER_API_KEY=sk-...
#   AGENTROUTER_BASE_URL=https://agentrouter.org/v1
#   OPENROUTER_API_KEY=sk-or-...   (fallback)
# Launch:
.venv/bin/streamlit run ui.py --server.port 8501
```
API keys are stored in `/opt/robin/.env`. The AgentRouter key enables
access to multiple LLM backends through a single endpoint.

## Webshell & payload collections

Kali ships webshells in `/usr/share/webshells/`, `/usr/share/laudanum/`,
and `/usr/share/seclists/Web-Shells/`. An additional 216 deduplicated
BlackArch webshells are installed at `/opt/blackarch-webshells/` (PHP,
ASP, ASPX, JSP, CFM, Perl, Ruby). See full inventory, language breakdown,
and dedup methodology in `references/webshell-collections.md`.

## Pitfalls

- **Do not** use `pip install --break-system-packages` on Kali. It corrupts
  the system Python and apt-managed packages will break.
- `pipx inject` may report success but not actually make the package
  importable. Always verify with the tool itself, not the inject output.
- Python 3.13 removed many deprecated stdlib modules. Security tools
  from before ~2024 may need patches. Check the tool's GitHub issues
  for "Python 3.13" before spending time debugging.
- Some tools (metasploit, nuclei, amass) ship as Kali apt packages —
  prefer `apt install` over manual install for these to get updates.
