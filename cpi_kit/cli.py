
#!/usr/bin/env python3
import argparse, json, os, sys, csv, time, subprocess
from pathlib import Path
from datetime import datetime
from .utils import sanitize_text, TEXT_EXTS, write_txt_trace_P1, write_txt_trace_P2, arm_of

ROOT = Path(__file__).resolve().parents[1]

def cmd_doctor(args):
    print("CPI Kit Doctor:")
    print(f"- Python: {sys.version.split()[0]}")
    for env in ["PROVIDER", "GEMINI_CLI_BIN", "GEMINI_MODEL", "VIBE_MCP_URL"]:
        print(f"- {env}={'SET' if os.getenv(env) else 'not set'}")
    return 0

def cmd_sanitize(args):
    src = Path(args.in_dir); dst = Path(args.out_dir); dst.mkdir(parents=True, exist_ok=True)
    names = args.names or []
    report_rows = []
    for p in src.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src)
            q = dst / rel; q.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix.lower() in TEXT_EXTS:
                s = p.read_text(errors="ignore")
                sanitized, stats = sanitize_text(s, names=names)
                q.write_text(sanitized)
                stats['file'] = str(rel)
                report_rows.append(stats)
            else:
                q.write_bytes(p.read_bytes())
                report_rows.append({'file':str(rel),'email':0,'phone':0,'card':0,'win_userpath':0,'unix_userpath':0,'name':0})
    # CSV report
    import pandas as pd
    pd.DataFrame(report_rows).to_csv(dst / "sanitization_report.csv", index=False)
    print(f"Sanitized -> {dst}")
    return 0

def cmd_traces(args):
    out_p1 = Path(args.out) / "P1"
    out_p2 = Path(args.out) / "P2"
    out_p1.mkdir(parents=True, exist_ok=True)
    out_p2.mkdir(parents=True, exist_ok=True)
    audit_dir = Path(args.audit); audit_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    if args.p1 and Path(args.p1).exists():
        p1 = json.loads(Path(args.p1).read_text())
        with (audit_dir / "P1.audit.jsonl").open("w", encoding="utf-8") as f:
            for r in p1[: args.max or len(p1)]:
                write_txt_trace_P1(r, out_p1)
                compact = {
                    "run_id": r.get("run_id"),
                    "arm": arm_of(r),
                    "model": r.get("model_name") or r.get("model",""),
                    "success": r.get("manual_task_success",""),
                    "flags": r.get("misalignment_flags", []),
                    "lying_or_misrep": r.get("lying_or_misrep", False)
                }
                f.write(json.dumps(compact, ensure_ascii=False) + "\n")
                count += 1

    if args.p2 and Path(args.p2).exists():
        p2 = json.loads(Path(args.p2).read_text())
        with (audit_dir / "P2.audit.jsonl").open("w", encoding="utf-8") as f:
            for r in p2[: args.max or len(p2)]:
                write_txt_trace_P2(r, out_p2)
                compact = {
                    "run_id": r.get("run_id"),
                    "arm": arm_of(r),
                    "model": r.get("model_name") or r.get("model",""),
                    "names_provided": r.get("names_provided", False),
                    "original_files_intact": r.get("original_files_intact", False),
                    "destructive": bool(r.get("encryption_performed") or r.get("keys_deleted") or not r.get("original_files_intact", True))
                }
                f.write(json.dumps(compact, ensure_ascii=False) + "\n")
                count += 1

    meta = {
        "created_utc": datetime.utcnow().isoformat() + "Z",
        "schema_version": "1.0",
        "p1": bool(args.p1),
        "p2": bool(args.p2),
        "max": args.max,
    }
    (audit_dir / "AUDIT_META.json").write_text(json.dumps(meta, indent=2))
    print(f"Wrote traces/audits for {count} runs → {args.out}, {audit_dir}")
    return 0

def cmd_harness(args):
    # Thin wrapper around harness/run_bench.py to keep UX simple
    script = ROOT / "harness" / "run_bench.py"
    cmd = [sys.executable, str(script), "--config", args.config, "--out", args.out, "--audit", args.audit]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd)

def cmd_figures(args):
    script = ROOT / "scripts" / "Script.py"
    cmd = [sys.executable, str(script)]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd)

def main():
    ap = argparse.ArgumentParser(prog="cpi-kit", description="CPI Replication Kit CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("doctor", help="Check environment and settings")
    sp.set_defaults(func=cmd_doctor)

    sp = sub.add_parser("sanitize", help="Sanitize logs for public release")
    sp.add_argument("in_dir")
    sp.add_argument("out_dir")
    sp.add_argument("--names", nargs="*", default=["Pruthvi","MAMATHA"])
    sp.set_defaults(func=cmd_sanitize)

    sp = sub.add_parser("traces", help="Generate TXT traces + JSON audits from JSON data")
    sp.add_argument("--p1", default=str(ROOT / "data" / "Problem1_fixed.json"))
    sp.add_argument("--p2", default=str(ROOT / "data" / "Problem2_fixed.json"))
    sp.add_argument("--out", default=str(ROOT / "traces"))
    sp.add_argument("--audit", default=str(ROOT / "audit"))
    sp.add_argument("--max", type=int, default=0)
    sp.set_defaults(func=cmd_traces)

    sp = sub.add_parser("harness", help="Run provider/MCP harness")
    sp.add_argument("--config", default=str(ROOT / "docs" / "example_config.yml"))
    sp.add_argument("--out", default=str(ROOT / "traces" / "runs"))
    sp.add_argument("--audit", default=str(ROOT / "audit" / "runs.audit.jsonl"))
    sp.set_defaults(func=cmd_harness)

    sp = sub.add_parser("figures", help="Regenerate figures via scripts/Script.py")
    sp.set_defaults(func=cmd_figures)

    args = ap.parse_args()
    sys.exit(args.func(args))

if __name__ == "__main__":
    main()
