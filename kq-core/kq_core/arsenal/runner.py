"""Scoped, audited, retrying tool runner + target profiling + decision engine.

Guardrail order on every run (non-negotiable):
  1. validate target shape   (no shell metacharacters)
  2. scope_check             (out-of-scope -> refuse + audit)
  3. destructive guard       (block-list -> require confirm token)
  4. install check           (shutil.which -> not_installed, not a crash)
  5. cache lookup            (avoid re-running identical commands)
  6. exec w/ timeout + retry (classify errors; retry transient)
  7. persist output + audit

Subprocess is NOT run through a shell (no shell=True), so target/arg tokens are never
shell-interpreted. ``_exec`` and ``_which`` are module-level so tests can monkeypatch them
(Kali tools aren't installed on the dev box).
"""
from __future__ import annotations

import hashlib
import ipaddress
import re
import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Tuple

from . import catalog
from .. import audit, guard
from .. import scope as _scope
from ..util import now_iso

_META_RE = re.compile(r"[;&|`$><\n\r\t\\]")  # shell metacharacters disallowed in a target
_MAX_STDOUT = 8000

_PARAMS = {
    "stealth": {"threads": "10", "rate": "100", "nmap_timing": "-T2", "nmap_ports": "--top-ports 100"},
    "normal": {"threads": "40", "rate": "1000", "nmap_timing": "-T4", "nmap_ports": "--top-ports 1000"},
    "aggressive": {"threads": "100", "rate": "10000", "nmap_timing": "-T4", "nmap_ports": "-p-"},
}
_DEFAULT_WORDLIST = "/usr/share/seclists/Discovery/Web-Content/common.txt"


# ── target profiling ──────────────────────────────────────────────────────────
@dataclass
class TargetProfile:
    target: str
    target_type: str = "unknown"
    host: str = ""
    scheme: str = ""
    is_ip: bool = False
    is_cidr: bool = False


def _is_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def _is_cidr(s: str) -> bool:
    try:
        ipaddress.ip_network(s, strict=False)
        return "/" in s
    except ValueError:
        return False


def profile_target(target: str) -> TargetProfile:
    t = (target or "").strip()
    scheme = t.split("://", 1)[0].lower() if "://" in t else ""
    host = _scope.host_of(t)
    is_cidr = _is_cidr(t)
    is_ip = _is_ip(host)
    if scheme in ("http", "https"):
        tt = "web"
    elif is_cidr:
        tt = "network"
    elif is_ip:
        tt = "host"
    elif host and "." in host:
        tt = "domain"
    else:
        tt = "unknown"
    return TargetProfile(target=t, target_type=tt, host=host, scheme=scheme, is_ip=is_ip, is_cidr=is_cidr)


# ── decision engine ───────────────────────────────────────────────────────────
def recommend(profile: TargetProfile, objective: str = "comprehensive", max_n: int = 8) -> List[catalog.ToolSpec]:
    """Rank catalog tools for a target. objective: quick | comprehensive | stealth."""
    types = {profile.target_type}
    if profile.target_type == "web":
        types.add("url")
    specs = [s for s in catalog.all_specs() if set(s.target_types) & types]
    if objective == "stealth":
        specs = [s for s in specs if s.passive]
    specs.sort(key=lambda s: s.effectiveness, reverse=True)
    if objective == "quick":
        specs = specs[:3]
    return specs[:max_n]


# ── parameter optimization + command building ─────────────────────────────────
def optimize_params(spec: catalog.ToolSpec, profile: TargetProfile, mode: str) -> dict:
    p = _PARAMS.get(mode, _PARAMS["normal"])
    ports = ""
    if spec.binary == "nmap":
        ports = p["nmap_ports"] + " " + p["nmap_timing"]
    elif spec.binary == "masscan":
        ports = "1-65535"
    return {
        "ports": ports,
        "wordlist": _DEFAULT_WORDLIST,
        "threads": p["threads"],
        "rate": p["rate"],
    }


def validate_target(target: str) -> Optional[str]:
    if not target:
        return None  # some tools (john/hashcat/searchsploit) don't need a target
    if _META_RE.search(target) or " " in target.strip():
        return "target contains illegal characters (shell metacharacters/whitespace)"
    return None


def build_command(
    tool: str, target: str, extra: str = "", mode: str = "normal",
    profile: Optional[TargetProfile] = None,
) -> Tuple[List[str], Optional[catalog.ToolSpec]]:
    """Build an argv list (no shell). Returns (argv, spec|None)."""
    spec = catalog.get(tool)
    profile = profile or profile_target(target)
    extra_tokens = shlex.split(extra) if extra else []
    if spec is None:
        argv = [tool] + extra_tokens + ([target] if target else [])
        return [a for a in argv if a], None
    params = optimize_params(spec, profile, mode)
    cmd = spec.template.format(target=target, ports=params["ports"], wordlist=params["wordlist"],
                               threads=params["threads"], rate=params["rate"], extra="")
    argv = [a for a in shlex.split(cmd) if a] + extra_tokens
    return argv, spec


# ── error classification ──────────────────────────────────────────────────────
def classify_error(returncode: int, stderr: str, timed_out: bool) -> str:
    if timed_out:
        return "timeout"
    if returncode == 0:
        return "ok"
    s = (stderr or "").lower()
    if any(x in s for x in ("permission denied", "must be root", "operation not permitted", "are you root")):
        return "permission"
    if any(x in s for x in ("command not found", "no such file", "not installed")):
        return "not_found"
    if any(x in s for x in ("could not resolve", "network is unreachable", "connection refused",
                            "no route to host", "timed out", "temporary failure")):
        return "network"
    if any(x in s for x in ("usage:", "invalid option", "unrecognized", "unknown option", "invalid argument")):
        return "syntax"
    return "error"


# ── low-level exec / which (monkeypatched in tests) ───────────────────────────
def _which(binary: str) -> Optional[str]:
    return shutil.which(binary)


def _exec(argv: List[str], timeout: int) -> dict:
    start = time.perf_counter()
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                              encoding="utf-8", errors="replace")
        return {"returncode": proc.returncode, "stdout": proc.stdout or "",
                "stderr": proc.stderr or "", "timed_out": False,
                "elapsed": round(time.perf_counter() - start, 2)}
    except subprocess.TimeoutExpired as e:
        return {"returncode": -1, "stdout": (e.stdout or "") if isinstance(e.stdout, str) else "",
                "stderr": "timeout", "timed_out": True, "elapsed": round(time.perf_counter() - start, 2)}
    except FileNotFoundError:
        return {"returncode": 127, "stdout": "", "stderr": "command not found",
                "timed_out": False, "elapsed": 0.0}


# ── cache ──────────────────────────────────────────────────────────────────────
def _cache_get(store: Any, cmd_hash: str) -> Optional[dict]:
    row = store.query_one("SELECT result_ref, created_at FROM tool_cache WHERE cmd_hash=?", (cmd_hash,))
    if not row:
        return None
    ref = Path(row["result_ref"])
    if not ref.exists():
        return None
    return {"result_ref": row["result_ref"], "created_at": row["created_at"],
            "stdout": ref.read_text(encoding="utf-8", errors="replace")}


def _cache_put(store: Any, cmd_hash: str, target: str, result_ref: str) -> None:
    store.execute(
        "INSERT OR REPLACE INTO tool_cache(cmd_hash, target, result_ref, created_at) VALUES (?,?,?,?)",
        (cmd_hash, target, result_ref, now_iso()),
    )


# ── the orchestrated run ──────────────────────────────────────────────────────
def run_tool(
    store: Any,
    engagement_id: int,
    tool: str,
    target: str = "",
    *,
    extra: str = "",
    mode: str = "normal",
    confirm_token: Optional[str] = None,
    use_cache: bool = True,
    max_retries: int = 1,
) -> dict:
    profile = profile_target(target) if target else TargetProfile(target="", target_type="unknown")

    # 1. target shape
    bad = validate_target(target)
    if bad:
        return {"ok": False, "error": "invalid_target", "reason": bad}

    # 2. scope gate (only when there's a target host)
    scope_verdict = "n/a"
    if target:
        scope_verdict, _rule, reason = _scope.scope_check(store, engagement_id, target)
        if scope_verdict == "out":
            audit.record(store, tool=tool, action="run_tool", engagement_id=engagement_id,
                         target=target, verdict="out", result={"refused": True})
            return {"ok": False, "refused": True, "scope_verdict": "out", "reason": reason}

    # 3. build + destructive guard
    argv, spec = build_command(tool, target, extra=extra, mode=mode, profile=profile)
    cmdline = " ".join(argv)
    flagged = guard.scan(cmdline)
    if flagged:
        token = guard.confirm_token(flagged)
        if confirm_token != token:
            audit.record(store, tool=tool, action="confirm_required", engagement_id=engagement_id,
                         target=target, verdict="blocked", args={"pattern": flagged})
            return {"ok": False, "requires_confirm": True, "confirm_token": token,
                    "reason": f"destructive pattern '{flagged}'. Re-run with confirm_token to proceed.",
                    "command": cmdline}
        audit.record(store, tool=tool, action="confirm_granted", engagement_id=engagement_id, target=target)

    # 4. install check
    binary = spec.binary if spec else tool
    if _which(binary) is None:
        audit.record(store, tool=tool, action="run_tool", engagement_id=engagement_id, target=target,
                     verdict=scope_verdict, result={"error": "not_installed"})
        return {"ok": False, "error": "not_installed", "binary": binary,
                "hint": f"{binary} is not on PATH (install it on Kali)."}

    # 5. cache
    cmd_hash = hashlib.sha256(cmdline.encode("utf-8")).hexdigest()
    if use_cache:
        hit = _cache_get(store, cmd_hash)
        if hit:
            audit.record(store, tool=tool, action="run_tool", engagement_id=engagement_id, target=target,
                         verdict=scope_verdict, result={"cache": "hit"})
            return {"ok": True, "cached": True, "command": cmdline, "scope_verdict": scope_verdict,
                    "target_type": profile.target_type, "result_ref": hit["result_ref"],
                    "stdout": hit["stdout"][:_MAX_STDOUT]}

    # 6. exec + retry on transient
    timeout = spec.timeout if spec else 600
    attempt, res = 0, None
    while attempt <= max_retries:
        res = _exec(argv, timeout)
        err = classify_error(res["returncode"], res["stderr"], res["timed_out"])
        if err in ("timeout", "network") and attempt < max_retries:
            attempt += 1
            continue
        break
    err_class = classify_error(res["returncode"], res["stderr"], res["timed_out"])

    # 7. persist + audit
    runs_dir = store.cfg.kq_home / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    ref = runs_dir / f"{cmd_hash[:16]}.txt"
    output = (res["stdout"] or "") + (("\n[stderr]\n" + res["stderr"]) if res["stderr"] else "")
    ref.write_text(f"$ {cmdline}\n\n{output}", encoding="utf-8", errors="replace")
    if use_cache and err_class == "ok":
        _cache_put(store, cmd_hash, target, str(ref))
    audit.record(store, tool=tool, action="run_tool", engagement_id=engagement_id, target=target,
                 verdict=scope_verdict, args={"command": cmdline},
                 result={"rc": res["returncode"], "error_class": err_class, "elapsed": res["elapsed"], "attempts": attempt + 1})

    return {
        "ok": err_class == "ok",
        "command": cmdline,
        "returncode": res["returncode"],
        "error_class": err_class,
        "elapsed": res["elapsed"],
        "attempts": attempt + 1,
        "scope_verdict": scope_verdict,
        "target_type": profile.target_type,
        "result_ref": str(ref),
        "stdout": output[:_MAX_STDOUT],
        "truncated": len(output) > _MAX_STDOUT,
    }
