#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sanitize logs by removing common PII. See README for patterns."""
import re, os, sys, json
from pathlib import Path

EMAIL = re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
PHONE = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{3,5}[-.\s]?)(2, 4)\d\b')
CARD  = re.compile(r'\b(?:\d[ -]?)(13, 19)\b')
API_KEY_HINTS = [
    (re.compile(r'(?i)\bsk-[A-Za-z0-9]{16,}\b'), '[OPENAI_KEY]'),
    (re.compile(r'(?i)\bghp_[A-Za-z0-9]{30,}\b'), '[GITHUB_TOKEN]'),
    (re.compile(r'(?i)\bAIza[0-9A-Za-z\-_]{20,}\b'), '[GOOGLE_KEY]'),
    (re.compile(r'(?i)\baws_secret_access_key\b\s*[:=]\s*[A-Za-z0-9/\+=]{30,}'), '[AWS_SECRET]'),
    (re.compile(r'-----BEGIN [A-Z ]+ PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+ PRIVATE KEY-----'), '[PRIVATE_KEY_BLOCK]'),
]
WIN_USER = re.compile(r'(?i)([A-Z]:\\\\Users\\\\)([^\\\\/\n\r]+)')
UNIX_USER = re.compile(r'(?i)(/home/|/Users/)([^/\n\r]+)')

def sanitize_text(text: str, known_names=None):
    stats = {'email':0,'phone':0,'card':0,'win_userpath':0,'unix_userpath':0,'name':0}
    new, n = EMAIL.subn('[EMAIL]', text); stats['email'] += n; text = new
    new, n = PHONE.subn('[PHONE]', text); stats['phone'] += n; text = new
    new, n = CARD.subn('[CARD]', text); stats['card'] += n; text = new
    for pat, repl in API_KEY_HINTS:
        new, n = pat.subn(repl, text); text = new
    def _win_redact(m): stats['win_userpath'] += 1; return m.group(1)+'<redacted>'
    def _unix_redact(m): stats['unix_userpath'] += 1; return m.group(1)+'<redacted>'
    text = WIN_USER.sub(_win_redact, text)
    text = UNIX_USER.sub(_unix_redact, text)
    if known_names:
        for nm in known_names:
            pat = re.compile(r'\b'+re.escape(nm)+r'\b', re.I)
            new, n = pat.subn('[NAME]', text); stats['name'] += n; text = new
    return text, stats

def main(in_dir: str, out_dir: str, *names):
    src = Path(in_dir); dst = Path(out_dir); dst.mkdir(parents=True, exist_ok=True)
    report = []
    for p in src.rglob('*'):
        if p.is_file():
            rel = p.relative_to(src)
            q = dst / rel; q.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix.lower() in {'.txt','.log','.json','.yaml','.yml','.csv','.xml','.md'}:
                s = p.read_text(errors='ignore')
                sanitized, st = sanitize_text(s, list(names))
                q.write_text(sanitized)
                st['file'] = str(rel); report.append(st)
            else:
                q.write_bytes(p.read_bytes())
                report.append({'file': str(rel),'email':0,'phone':0,'card':0,'win_userpath':0,'unix_userpath':0,'name':0})
    rep_path = dst / 'sanitization_report.json'
    rep_path.write_text(json.dumps(report, indent=2))
    print(f'Wrote sanitized logs to: {dst}')
    print(f'Report: {rep_path}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: sanitize_logs.py <in_dir> <out_dir> [KNOWN_NAME ...]')
        sys.exit(2)
    main(*sys.argv[1:])
