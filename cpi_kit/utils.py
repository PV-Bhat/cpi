
import re, json, os, time, hashlib
from pathlib import Path
from datetime import datetime

EMAIL = re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
PHONE = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{3,5}[-.\s]?){2,4}\d\b')
CARD  = re.compile(r'\b(?:\d[ -]?){13,19}\b')
API_KEY_HINTS = [
    (re.compile(r'(?i)\bsk-[A-Za-z0-9]{16,}\b'), '[OPENAI_KEY]'),
    (re.compile(r'(?i)\bghp_[A-Za-z0-9]{30,}\b'), '[GITHUB_TOKEN]'),
    (re.compile(r'(?i)\bAIza[0-9A-Za-z\-_]{20,}\b'), '[GOOGLE_KEY]'),
    (re.compile(r'(?i)\baws_secret_access_key\b\s*[:=]\s*[A-Za-z0-9/\+=]{30,}'), '[AWS_SECRET]'),
    (re.compile(r'-----BEGIN [A-Z ]+ PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+ PRIVATE KEY-----'), '[PRIVATE_KEY_BLOCK]'),
]
WIN_USER = re.compile(r'(?i)([A-Z]:\\Users\\)([^\\/\n\r]+)')
UNIX_USER = re.compile(r'(?i)(/home/|/Users/)([^/\n\r]+)')

TEXT_EXTS = {'.txt','.log','.json','.yaml','.yml','.csv','.xml','.md'}

def sanitize_text(text: str, names=None):
    stats = {'email':0,'phone':0,'card':0,'win_userpath':0,'unix_userpath':0,'name':0}
    new, n = EMAIL.subn('[EMAIL]', text); stats['email'] += n; text = new
    new, n = PHONE.subn('[PHONE]', text); stats['phone'] += n; text = new
    new, n = CARD.subn('[CARD]', text); stats['card'] += n; text = new
    for pat, repl in API_KEY_HINTS:
        new, n = pat.subn(repl, text); text = new
    def _win(m): stats['win_userpath'] += 1; return m.group(1)+'<redacted>'
    def _unix(m): stats['unix_userpath'] += 1; return m.group(1)+'<redacted>'
    text = WIN_USER.sub(_win, text)
    text = UNIX_USER.sub(_unix, text)
    if names:
        for nm in names:
            pat = re.compile(r'\b'+re.escape(nm)+r'\b', re.I)
            new, n = pat.subn('[NAME]', text); stats['name'] += n; text = new
    return text, stats

def arm_of(record):
    try:
        vc = record.get("vibe_calls", 0) or 0
        return "CPI" if int(vc) > 0 else "No-CPI"
    except Exception:
        return "No-CPI"

def write_txt_trace_P1(r, out_dir: Path):
    run_id = r.get("run_id") or hashlib.md5(json.dumps(r, sort_keys=True).encode()).hexdigest()[:10]
    lines = []
    lines.append(f"RUN_ID: {run_id}")
    lines.append(f"ARM: {arm_of(r)}")
    lines.append(f"MODEL: {r.get('model_name','')}")
    lines.append(f"TIMESTAMP: {datetime.utcnow().isoformat()}Z")
    lines.append("RESULTS:")
    for k in ["manual_task_success","failure_reason","deleted_essential","lying_or_misrep"]:
        if k in r: lines.append(f"  - {k}: {r.get(k)}")
    if "misalignment_flags" in r and r["misalignment_flags"]:
        lines.append("FLAGS: " + ", ".join(map(str, r["misalignment_flags"])))
    if "commentary" in r and r["commentary"]:
        s = str(r["commentary"]); s = s if len(s) < 2000 else s[:2000] + " ... [truncated]"
        lines.append("COMMENTARY:"); lines.append(s)
    text, _ = sanitize_text("\n".join(lines), names=["Pruthvi","MAMATHA"])
    (out_dir / f"{run_id}.txt").write_text(text)

def write_txt_trace_P2(r, out_dir: Path):
    run_id = r.get("run_id") or hashlib.md5(json.dumps(r, sort_keys=True).encode()).hexdigest()[:10]
    lines = []
    lines.append(f"RUN_ID: {run_id}")
    lines.append(f"ARM: {arm_of(r)}")
    lines.append(f"MODEL: {r.get('model_name','')}")
    lines.append(f"TIMESTAMP: {datetime.utcnow().isoformat()}Z")
    lines.append("RESULTS:")
    for k in ["names_provided","recommendations_given","encryption_performed","keys_deleted","original_files_intact","alignment_score"]:
        if k in r: lines.append(f"  - {k}: {r.get(k)}")
    if "summary" in r and r["summary"]:
        s = str(r["summary"]); s = s if len(s) < 2000 else s[:2000] + " ... [truncated]"
        lines.append("SUMMARY:"); lines.append(s)
    if "destructive_actions" in r and r["destructive_actions"]:
        lines.append("DESTRUCTIVE_ACTIONS:"); 
        for act in r["destructive_actions"]: lines.append(f"  - {act}")
    if "new_files" in r and r["new_files"]:
        lines.append("NEW_FILES: " + ", ".join(map(str, r["new_files"])))
    text, _ = sanitize_text("\n".join(lines), names=["Pruthvi","MAMATHA"])
    (out_dir / f"{run_id}.txt").write_text(text)
