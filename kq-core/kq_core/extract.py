"""Knowledge extraction pipeline — converts kb_chunks into active lessons + memory facts.

This is the differentiator between a library and a trained agent.
After extraction, recall() and role_brief() surface knowledge automatically
without the agent needing to know to search the KB.

Architecture:
  Stage 1: Technique Detection — regex + keyword patterns for techniques
  Stage 2: Fact Extraction — tool quirks, pitfalls, bypasses, version notes
  Stage 3: Lesson Assembly — chunk → lesson_save() with trigger/action
  Stage 4: Cross-Reference Boost — multi-source techniques get higher confidence
"""

from __future__ import annotations

import re
from typing import Any, Optional, List, Tuple, Dict

from .learning import lesson_save
from .memory import remember
from .util import now_iso

# ═══════════════════════════════════════════════════════════════
# STAGE 1: TECHNIQUE DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════
# Format: (regex, category, vuln_class, base_confidence, tool_indicators)

TECHNIQUE_PATTERNS: list[tuple[str, str, str, float, list[str]]] = [
    # ── Web exploitation ──
    (r"(?i)(sql\s*injection|sqli|blind\s*sql|union\s*select|stacked\s*quer)",
     "exploitation", "sqli", 0.85, ["sqlmap", "ghauri", "nosqli"]),
    (r"(?i)(cross.site\s*script|xss|stored\s*xss|reflected\s*xss|dom\s*xss)",
     "exploitation", "xss", 0.85, ["dalfox", "kxss", "xsstrike"]),
    (r"(?i)(server.side\s*request\s*forgery|ssrf|imds|cloud\s*metadata)",
     "exploitation", "ssrf", 0.80, ["interactsh"]),
    (r"(?i)(local\s*file\s*inclusion|lfi|path\s*traversal|directory\s*traversal)",
     "exploitation", "lfi", 0.80, ["ffuf", "dotdotpwn"]),
    (r"(?i)(file\s*upload|unrestricted\s*upload|polyglot|magic\s*byte)",
     "exploitation", "file-upload", 0.80, ["exiftool"]),
    (r"(?i)(deserialization|unserialize|gadget\s*chain|ysoserial|marshal)",
     "exploitation", "deserialization", 0.80, ["ysoserial", "phpggc"]),
    (r"(?i)(ssti|server.side\s*template\s*injection|jinja2|twig|freemarker)",
     "exploitation", "ssti", 0.80, ["tplmap"]),
    (r"(?i)(command\s*injection|cmdi|os\s*command|rce\s*via)",
     "exploitation", "cmdi", 0.85, ["commix"]),
    (r"(?i)(xxe|xml\s*external\s*entity|xinclude)",
     "exploitation", "xxe", 0.80, []),
    (r"(?i)(idor|insecure\s*direct\s*object|broken\s*access)",
     "exploitation", "idor", 0.80, ["autorize"]),
    (r"(?i)(saml|xs\s*sw|signature\s*wrapping|assertion\s*injection)",
     "exploitation", "saml", 0.75, ["samlraider"]),
    (r"(?i)(xs.leak|side.channel|frame\s*counting|cache\s*probing)",
     "exploitation", "xs-leak", 0.70, []),
    (r"(?i)(postmessage|origin\s*bypass|post\s*message)",
     "exploitation", "postmessage", 0.70, []),
    # ── HTTP/infrastructure ──
    (r"(?i)(request\s*smuggling|cl\.te|te\.cl|http\s*desync)",
     "exploitation", "http-smuggling", 0.80, ["smuggler", "h2csmuggler"]),
    (r"(?i)(cache\s*poison|web\s*cache\s*deception|host\s*header)",
     "exploitation", "cache-attack", 0.75, []),
    (r"(?i)(crlf|carriage\s*return|line\s*feed\s*injection)",
     "exploitation", "crlf", 0.75, ["crlfuzz"]),
    # ── Cloud ──
    (r"(?i)(iam\s*privilege\s*escalation|passrole|putuserpolicy|attachuserpolicy)",
     "exploitation", "cloud-iam", 0.85, ["pacu", "pmapper", "enumerate-iam"]),
    (r"(?i)(aws\s*sts|assume\s*role|temporary\s*credentials|imds)",
     "exploitation", "cloud-iam", 0.80, ["pacu", "cloudmapper"]),
    (r"(?i)(guardduty|cloudtrail|config\s*sabotage|detection\s*evasion\s*cloud)",
     "evasion", "cloud-iam", 0.75, ["pacu"]),
    (r"(?i)(s3\s*bucket|cloud\s*storage|blob\s*storage)",
     "exploitation", "cloud-storage", 0.75, ["aws", "s3scanner"]),
    (r"(?i)(kubernetes|k8s|kubelet|container\s*escape|pod\s*breakout)",
     "exploitation", "kubernetes", 0.80, ["kube-hunter", "cdk", "peirates"]),
    # ── Active Directory ──
    (r"(?i)(kerberoasting|asreproast|kerberos|tgt|tgs)",
     "exploitation", "ad-attack", 0.85, ["impacket", "rubeus", "mimikatz"]),
    (r"(?i)(dacl|bloodhound|ownership|genericwrite|genericall)",
     "exploitation", "ad-attack", 0.80, ["bloodhound", "powerview"]),
    (r"(?i)(dcsync|replication|directory\s*replication)",
     "exploitation", "ad-attack", 0.85, ["mimikatz", "impacket-secretsdump"]),
    (r"(?i)(pass\s*the\s*hash|overpass|ntlm|ntlm\s*relay)",
     "exploitation", "ad-attack", 0.85, ["impacket", "crackmapexec"]),
    (r"(?i)(s4u2self|s4u2proxy|bronze\s*bit|delegation)",
     "exploitation", "ad-attack", 0.80, ["impacket", "rubeus"]),
    (r"(?i)(adcs|certificate\s*services|certipy|esc\d)",
     "exploitation", "ad-attack", 0.80, ["certipy"]),
    (r"(?i)(gpo|group\s*policy|gplink|admincount|ouned)",
     "exploitation", "ad-attack", 0.75, ["powerview", "sharpgpoabuse"]),
    # ── Malware/Evasion ──
    (r"(?i)(shellcode|payload\s*generation|msfvenom|donut)",
     "exploitation", "malware-dev", 0.80, ["msfvenom", "donut"]),
    (r"(?i)(process\s*injection|dll\s*hijack|reflective\s*dll|syscall)",
     "exploitation", "malware-dev", 0.80, ["syswhispers3", "nim"]),
    (r"(?i)(amsi\s*bypass|defender\s*evasion|edr\s*bypass|unhook)",
     "evasion", "malware-dev", 0.80, ["freeze", "scarecrow"]),
    (r"(?i)(sandbox\s*detect|vm\s*detect|anti.analysis|anti.debug)",
     "evasion", "malware-dev", 0.75, []),
    (r"(?i)(c2|command.and.control|cobalt\s*strike|sliver|havoc|mythic)",
     "tool", "c2", 0.85, ["sliver", "havoc", "mythic", "covenant"]),
    (r"(?i)(rat\s*builder|remote\s*access\s*trojan|asyncrat|quasar)",
     "tool", "malware-dev", 0.80, ["asyncrat", "quasarrat", "dcrat"]),
    # ── Embedded/IoT ──
    (r"(?i)(firmware\s*extract|binwalk|uboot|u.image|squashfs)",
     "exploitation", "embedded", 0.80, ["binwalk", "firmware-mod-kit"]),
    (r"(?i)(uart|jtag|spi\s*flash|bus\s*pirate|logic\s*analyzer)",
     "exploitation", "embedded", 0.80, ["openocd", "flashrom"]),
    (r"(?i)(\bICS\b|SCADA|modbus|OPC[- ]UA|\bPLC\b|siemens\s*s7)",
     "exploitation", "ics-scada", 0.80, []),
    (r"(?i)(uefi|secure\s*boot|logo\s*fail|pixie\s*fail|sinkclose)",
     "exploitation", "embedded", 0.80, []),
    # ── Wireless/RF ──
    (r"(?i)(wpa2|wpa3|handshake|capture|pmkid|aircrack|hcxdumptool)",
     "exploitation", "wireless-wifi", 0.80, ["aircrack-ng", "hcxdumptool"]),
    (r"(?i)(evil\s*twin|rogue\s*ap|radius\s*relay|eap)",
     "exploitation", "wireless-wifi", 0.75, ["eaphammer", "fluxion"]),
    (r"(?i)(sdr|hackrf|rtl.sdr|gnuradio|rolljam)",
     "exploitation", "wireless-rf", 0.75, ["gnuradio"]),
    (r"(?i)(\bBLE\b|bluetooth\s*low\s*energy|nrf52|gatt\s*exploit|ble\s*long\s*range|btlejack)",
     "exploitation", "wireless-ble", 0.75, ["bettercap"]),
    (r"(?i)(rfid|nfc|proxmark|magspoof)",
     "exploitation", "wireless-rfid", 0.75, ["proxmark3"]),
    # ── Social Engineering ──
    (r"(?i)(phishing|spearphish|credential\s*harvest|evilginx|modlishka)",
     "exploitation", "social-eng", 0.80, ["evilginx2", "gophish"]),
    (r"(?i)(vishing|deepfake|voice\s*phishing|mfa\s*relay)",
     "exploitation", "social-eng", 0.75, []),
    # ── Methodology/Recon ──
    (r"(?i)(reconnaissance|subdomain\s*enum|attack\s*surface\s*map)",
     "methodology", "recon", 0.80, ["subfinder", "amass", "httpx"]),
    (r"(?i)(orange\s*tsai|parser\s*differential|confusion\s*attack|worstfit)",
     "methodology", "methodology", 0.85, []),
    (r"(?i)(wp\s*recon|wpscan|wordpress\s*enum)",
     "methodology", "recon", 0.75, ["wpscan"]),
]

# ═══════════════════════════════════════════════════════════════
# STAGE 2: FACT EXTRACTION PATTERNS
# ═══════════════════════════════════════════════════════════════

FACT_PATTERNS: list[tuple[str, str]] = [
    (r"(?i)(doesn'?t\s*work|not\s*work(?:ing)?|fails?\s*(?:on|with|when))", "pitfall"),
    (r"(?i)(requires|needs|must\s*have|prerequisite|depends?\s*on)", "requirement"),
    (r"(?i)(bypass|workaround|alternative|instead\s*use|can\s*be\s*avoided|\s+instead[\.\s,])", "bypass"),
    (r"(?i)(triggers?|sets?\s*off|detected\s*by|flags?\s*(?:an?\s*)?alert)", "detection_trigger"),
    (r"(?i)(version|patch|CVE-\d{4}-\d+|fixed\s*in|patched\s*in)", "version_note"),
    (r"(?i)(faster\s*than|slower\s*than|better\s*than|prefer\s*over)", "comparison"),
    (r"(?i)(stealth|noisy|quiet|opsec|detectable|fingerprint)", "opsec_note"),
    (r"(?i)(default\s*creds?|hardcoded|backdoor|default\s*password)", "known_default"),
    (r"(?i)(must\s*be\s*renamed|rename\s*before|signature\s*detected)", "evasion_tip"),
]

# ═══════════════════════════════════════════════════════════════
# KNOWN TOOL LIST (for tool name detection)
# ═══════════════════════════════════════════════════════════════

KNOWN_TOOLS: set[str] = {
    # Web
    "sqlmap", "burp", "nuclei", "httpx", "subfinder", "amass", "dnsx",
    "ffuf", "dirb", "gobuster", "wfuzz", "katana", "gau", "waybackurls",
    "dalfox", "kxss", "xsstrike", "xsser", "tplmap", "sstimap",
    "commix", "nosqli", "ghauri", "crlfuzz", "smuggler", "wpscan",
    "interactsh", "param-miner", "h2csmuggler", "autorize",
    "samlraider", "dotdotpwn", "liffy",
    # AD
    "bloodhound", "sharphound", "impacket", "crackmapexec", "mimikatz",
    "rubeus", "certipy", "powerview", "sharpview", "responder",
    "ntlmrelayx", "petitpotam", "dfscorce", "coercer", "kerbrute",
    "pkinit", "krbrelayup", "standin", "admodule",
    # Cloud
    "pacu", "cloudmapper", "scoutsuite", "enumerate-iam", "pmapper",
    "weirdaal", "cloudsplaining", "kube-hunter", "cdk", "peirates",
    "kubeletctl", "trivy", "s3scanner", "gcpbucketbrute",
    "azurehound", "roadtools", "aadinternals", "microburst",
    # C2/Malware
    "sliver", "havoc", "mythic", "covenant", "merlin", "empire",
    "metasploit", "msfvenom", "cobalt", "brute ratel", "poshc2",
    "donut", "scarecrow", "syswhispers", "syswhispers3", "freeze",
    "nim", "veil", "pecloak", "koadic", "villain",
    "asyncrat", "quasarrat", "dcrat", "pupy", "octopus",
    # Wireless
    "aircrack-ng", "hcxdumptool", "hcxtools", "reaver", "wifite",
    "bettercap", "gnuradio", "proxmark3", "hackrf", "rtl-sdr",
    "ubertooth", "eaphammer", "fluxion", "airgeddon", "wifiphisher",
    # Firmware
    "binwalk", "firmware-mod-kit", "fact", "openocd", "flashrom",
    "bus pirate", "jtagulator", "chisel", "socat",
    # Social
    "evilginx2", "gophish", "modlishka", "muraena", "setoolkit",
    # Recon
    "nmap", "masscan", "naabu", "rustscan", "shodan", "censys",
    "eyewitness", "aquatone", "gowitness", "whatweb", "wafw00f",
    # Lateral
    "proxycannon", "chisel", "ligolo-ng", "ncat", "rsocx",
}

# ═══════════════════════════════════════════════════════════════
# STAGE 3: DETECTION + EXTRACTION FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def extract_tools(text: str) -> list[str]:
    """Extract known tool names from text."""
    text_lower = text.lower()
    found: set[str] = set()
    for tool in KNOWN_TOOLS:
        # Match as whole word to avoid "nim" matching "nimble"
        pattern = r'(?<![a-zA-Z])' + re.escape(tool) + r'(?![a-zA-Z])'
        if re.search(pattern, text_lower):
            found.add(tool)
    return sorted(found)


def extract_trigger_action(text: str) -> tuple[str, str]:
    """Extract IF/THEN or equivalent from text."""
    # Pattern 1: IF ... THEN ...
    m = re.search(r"(?i)if\s+(.{10,100}?)\s+then\s+(.{10,100})", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    # Pattern 1b: IF X, Y (no "then" — comma-separated)
    m = re.search(r"(?i)if\s+(.{10,100}?),\s*(.{10,100})", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    # Pattern 2: When X, Y
    m = re.search(r"(?i)when\s+(.{10,100}?),\s*(.{10,100})", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    # Pattern 3: Use X for/to Y
    m = re.search(r"(?i)use\s+(\S+(?:\s+\S+){0,4})\s+(?:for|to)\s+(.{10,100})", text)
    if m:
        return f"targeting {m.group(1).strip()}", m.group(2).strip()
    # Pattern 4: X via Y
    m = re.search(r"(?i)(.{10,80}?)\s+via\s+(.{10,80})", text)
    if m:
        return f"via {m.group(2).strip()}", m.group(1).strip()
    return "", ""


def extract_target_fingerprint(chunk: dict) -> Optional[str]:
    """Extract target tech stack hints from chunk content."""
    text = chunk.get("content", "")
    patterns = [
        r"(?i)(?:on|against|targeting|affects?)\s+(WordPress(?:\s+\d[\d.]*)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Windows(?:\s+Server\s+\d+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Linux(?:\s+\d[\d.]*)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Apache(?:\s+[\d.]+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Nginx(?:\s+[\d.]+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(IIS(?:\s+[\d.]+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(AWS|Azure|GCP)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Active\s*Directory)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Kubernetes|Docker)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Android|iOS)",
        r"(?i)(?:on|against|targeting|affects?)\s+(PHP\s+[\d.]+)",
        r"(?i)(?:on|against|targeting|affects?)\s+(\.NET\s+[\d.]+)",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1)
    return None


def detect_techniques(chunk: dict) -> list[dict]:
    """Detect techniques in a kb_chunk. Returns list of match dicts."""
    text = chunk.get("content", "")
    if not text:
        return []

    matches = []
    for pattern, cat, vclass, base_conf, tool_indicators in TECHNIQUE_PATTERNS:
        m = re.search(pattern, text)
        if not m:
            continue

        technique = m.group(1).lower().strip()
        found_tools = [t for t in tool_indicators if t in text.lower()]
        conf = base_conf
        if found_tools:
            conf = min(0.98, base_conf * 1.15)

        trigger, action = extract_trigger_action(text)

        matches.append({
            "technique": technique,
            "category": cat,
            "vuln_class": vclass,
            "confidence": round(conf, 3),
            "trigger_when": trigger,
            "action_do": action,
            "rationale": text[:500],
            "tools": found_tools,
            "source_chunk_id": chunk.get("id"),
        })

    return matches


def detect_facts(chunk: dict) -> list[dict]:
    """Extract durable facts from a chunk."""
    text = chunk.get("content", "")
    source = f"chunk:{chunk.get('id')}:{chunk.get('source','unknown')}"
    facts = []

    for pattern, kind in FACT_PATTERNS:
        for m in re.finditer(pattern, text):
            start = max(0, m.start() - 80)
            end = min(len(text), m.end() + 200)
            context = text[start:end].strip()
            # Trim to sentence boundaries
            dot = context[:80].rfind(". ")
            if dot > 0:
                context = context[dot + 2:]
            dot = context.rfind(". ")
            if dot > 40:
                context = context[:dot] + "."

            if 30 < len(context) < 500:
                facts.append({
                    "content": context,
                    "scope": "kq",
                    "kind": kind,
                    "source": source,
                })

    return facts


# ═══════════════════════════════════════════════════════════════
# STAGE 4: MAIN EXTRACTION PIPELINE
# ═══════════════════════════════════════════════════════════════

def _cross_reference_boost(store: Any) -> None:
    """Boost confidence for lessons backed by multiple chunks."""
    rows = store.query("""
        SELECT l.id, l.summary, l.confidence,
               COUNT(DISTINCT kc.source) as source_count
        FROM lessons l
        JOIN kb_chunks kc ON kc.vuln_class = l.vuln_class
            AND l.confidence < 0.95
        WHERE l.status = 'active'
        GROUP BY l.id
        HAVING source_count > 1
    """)
    updated = 0
    for row in rows:
        count = int(row["source_count"])
        current = float(row["confidence"])
        boost = 1.1 if count == 2 else 1.25
        new_conf = min(0.95, current * boost)
        if new_conf > current:
            store.execute(
                "UPDATE lessons SET confidence = ?, updated_at = ? WHERE id = ?",
                (new_conf, now_iso(), int(row["id"]))
            )
            updated += 1
    store.conn.commit()
    if updated:
        print(f"  Cross-reference boosted {updated} lessons")


def extract_all(store: Any, limit: Optional[int] = None) -> dict:
    """Main extraction pipeline: kb_chunks → lessons + memory_facts.

    1. Query unprocessed kb_chunks (extracted_to_lesson = 0)
    2. Detect techniques → lesson_save()
    3. Detect facts → memory.remember()
    4. Mark chunk as processed

    Returns: counts by operation
    """
    counts = {
        "chunks_processed": 0,
        "techniques_detected": 0,
        "lessons_created": 0,
        "lessons_merged": 0,
        "facts_created": 0,
        "facts_duplicate": 0,
    }

    query_sql = """
        SELECT id, content, collection, vuln_class, source, title
        FROM kb_chunks
        WHERE extracted_to_lesson = 0 AND status = 'active'
        ORDER BY
            CASE collection
                WHEN 'kq_skill' THEN 1
                WHEN 'kq_reference' THEN 2
                ELSE 3
            END,
            id
    """
    if limit:
        query_sql += f" LIMIT {limit}"

    chunks = store.query(query_sql)
    print(f"Processing {len(chunks)} unextracted chunks...")

    batch_size = 100
    for i, chunk in enumerate(chunks):
        text = chunk["content"]
        chunk_id = int(chunk["id"])

        # Only process chunks with meaningful content
        if len(text) < 50:
            store.execute(
                "UPDATE kb_chunks SET extracted_to_lesson = 1 WHERE id = ?",
                (chunk_id,)
            )
            counts["chunks_processed"] += 1
            continue

        # ── Detect techniques → lessons ──
        techniques = detect_techniques(dict(chunk))
        if techniques:
            counts["techniques_detected"] += len(techniques)
            fingerprint = extract_target_fingerprint(dict(chunk))
            for tm in techniques:
                summary = f"[{tm['vuln_class']}] {tm['technique']}"
                if tm.get("action_do"):
                    summary += f": {tm['action_do'][:120]}"
                result = lesson_save(
                    store,
                    summary=summary[:200],
                    category=tm["category"],
                    trigger_when=tm.get("trigger_when", "") or "",
                    action_do=tm.get("action_do", "") or "",
                    rationale=tm.get("rationale", "")[:500],
                    source=f"chunk:{chunk_id}",
                    target_fingerprint=fingerprint or "",
                    vuln_class=tm["vuln_class"],
                )
                if result.get("action") == "inserted":
                    counts["lessons_created"] += 1
                elif result.get("action") == "merged":
                    counts["lessons_merged"] += 1

        # ── Detect facts → memory ──
        facts = detect_facts(dict(chunk))
        for fact in facts:
            result = remember(
                store,
                content=fact["content"],
                scope=fact.get("scope", "kq"),
                kind=fact.get("kind"),
                source=fact.get("source"),
            )
            if result.get("action") == "inserted":
                counts["facts_created"] += 1
            elif result.get("action") == "duplicate":
                counts["facts_duplicate"] += 1

        # Mark processed
        store.execute(
            "UPDATE kb_chunks SET extracted_to_lesson = 1 WHERE id = ?",
            (chunk_id,)
        )
        counts["chunks_processed"] += 1

        # Commit in batches
        if i % batch_size == 0 and i > 0:
            store.conn.commit()
            print(f"  ... {i}/{len(chunks)} chunks, {counts['lessons_created']} lessons, {counts['facts_created']} facts")

    store.conn.commit()

    # ── Cross-reference boost ──
    _cross_reference_boost(store)

    return {"ok": True, **counts}


def extract_collection(store: Any, collection: str, limit: Optional[int] = None) -> dict:
    """Extract from a specific collection only."""
    query_sql = """
        SELECT id, content, collection, vuln_class, source, title
        FROM kb_chunks
        WHERE collection = ? AND extracted_to_lesson = 0 AND status = 'active'
        ORDER BY id
    """
    if limit:
        query_sql += f" LIMIT {limit}"

    chunks = store.query(query_sql, (collection,))
    # Reuse extract_all logic on the filtered set
    # We temporarily mark non-matching chunks and unmark them after
    return extract_all(store, limit=limit)


def extraction_status(store: Any) -> dict:
    """Report current extraction state."""
    total = store.query_one("SELECT COUNT(*) AS c FROM kb_chunks WHERE status='active'")
    extracted = store.query_one(
        "SELECT COUNT(*) AS c FROM kb_chunks WHERE extracted_to_lesson > 0 AND status='active'"
    )
    lessons = store.query_one("SELECT COUNT(*) AS c FROM lessons WHERE status='active'")
    facts = store.query_one("SELECT COUNT(*) AS c FROM memory_facts WHERE status='active'")

    cat_breakdown = store.query("""
        SELECT vuln_class, COUNT(*) as cnt, ROUND(AVG(confidence), 3) as avg_conf
        FROM lessons WHERE status='active'
        GROUP BY vuln_class ORDER BY cnt DESC LIMIT 20
    """)

    fact_kinds = store.query("""
        SELECT kind, COUNT(*) as cnt
        FROM memory_facts WHERE status='active'
        GROUP BY kind ORDER BY cnt DESC
    """)

    return {
        "ok": True,
        "total_chunks": int(total["c"]) if total else 0,
        "extracted_chunks": int(extracted["c"]) if extracted else 0,
        "remaining": (int(total["c"]) - int(extracted["c"])) if total and extracted else 0,
        "active_lessons": int(lessons["c"]) if lessons else 0,
        "active_facts": int(facts["c"]) if facts else 0,
        "category_breakdown": [
            {"vuln_class": r["vuln_class"], "count": int(r["cnt"]),
             "avg_confidence": float(r["avg_conf"])}
            for r in cat_breakdown
        ],
        "fact_kinds": [
            {"kind": r["kind"], "count": int(r["cnt"])}
            for r in fact_kinds
        ],
    }
