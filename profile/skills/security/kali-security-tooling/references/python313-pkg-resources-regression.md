# Python 3.13 + pkg_resources: Full Diagnostic

## Root cause

Python 3.13 + setuptools >= 68: `pkg_resources` was a standalone module
shipped inside setuptools. Setuptools 68+ deprecated and removed it.
The `eth` Python library (ethereum ecosystem) imports `pkg_resources`
at `eth/__init__.py` line 1 unconditionally:

```python
# eth/__init__.py (line 1)
import pkg_resources
```

This is a hard import — no fallback, no try/except. Any tool that
depends on `eth` (mythril, slither, brownie, web3.py CLIs, etc.)
will fail on Python 3.13 with `ModuleNotFoundError: No module named 'pkg_resources'`.

## Reproduction

```bash
pipx install mythril
myth version
# Traceback (most recent call last):
#   File ".../bin/myth", line 3, in <module>
#     from mythril.interfaces.cli import main
#   ...
#   File ".../eth/__init__.py", line 1, in <module>
#     import pkg_resources
# ModuleNotFoundError: No module named 'pkg_resources'
```

## Failed approach: pipx inject

```bash
pipx inject mythril setuptools
# reports: "injected package setuptools into venv mythril"
# BUT: myth version still fails with same ModuleNotFoundError
```

Why: `pipx inject` installs setuptools to the pipx-managed venv, but
on Kali 2026.x the pip inside the venv resolves packages differently
than expected. The setuptools wheel is installed but `pkg_resources`
is not importable from the tool entry point. Using `pipx inject setuptools==67.8.0`
has the same issue — the inject mechanism doesn't guarantee the
dependency resolution you'd expect.

## Working approach: direct venv pip

```bash
~/.local/share/pipx/venvs/mythril/bin/python -m pip install 'setuptools<68'
# Successfully uninstalled setuptools-82.0.1
# Successfully installed setuptools-67.8.0

myth version
# Mythril version v0.24.8
```

The venv's own `python -m pip` correctly downgrades setuptools and
restores `pkg_resources` importability. This is the reliable path.

## Affected tool list

| Tool | Status | Notes |
|------|--------|-------|
| mythril | Confirmed broken, fix works | v0.24.8 on py3.13 |
| slither | Likely affected | Also depends on eth via crytic-compile |
| brownie | Likely affected | Heavy eth dependency |
| web3.py CLI | Likely affected | Direct eth import |
| echidna | N/A | Rust binary, not Python |

## When to apply

Any tool whose traceback ends in:
```
from eth._utils.numeric import ...
File ".../eth/__init__.py", line 1, in <module>
    import pkg_resources
ModuleNotFoundError: No module named 'pkg_resources'
```

The fix is always: downgrade setuptools in that tool's venv to <68.
