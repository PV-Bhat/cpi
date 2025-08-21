
#!/usr/bin/env python3
import os, json, sys, time, hashlib, random
from pathlib import Path
from providers import GeminiCLI, ProviderBase
from vibecheck_client import VibeCheckClient

ROOT = Path(__file__).resolve().parents[1]

def load_config(path):
    import yaml
    return yaml.safe_load(Path(path).read_text())

def select_provider(name: str) -> ProviderBase:
    if name == "gemini_cli":
        return GeminiCLI()
    raise SystemExit(f"Unknown provider: {name}")

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default=str(ROOT / "traces" / "runs"))
    ap.add_argument("--audit", default=str(ROOT / "audit" / "runs.audit.jsonl"))
    args = ap.parse_args()

    cfg = load_config(args.config)
    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    Path(args.audit).parent.mkdir(parents=True, exist_ok=True)

    provider_name = os.getenv("PROVIDER", "gemini_cli")
    provider = select_provider(provider_name)
    vibe = VibeCheckClient()
    seed = int(os.getenv("RUN_SEED", "42"))
    random.seed(seed)

    for i, task in enumerate(cfg.get("tasks", []), 1):
        prompt = task.get("prompt","")
        vc = vibe.advise(prompt)
        reply = provider.complete(prompt)
        run_id = f"RUN_{i:04d}_" + hashlib.md5(prompt.encode()).hexdigest()[:8]
        trace = f"""RUN_ID: {run_id}
ARM: {'CPI' if vc else 'No-CPI'}
SEED: {seed}
PROMPT:
{prompt}

VIBE:
{json.dumps(vc, ensure_ascii=False) if vc else "None"}

REPLY:
{reply}
"""
        (out_dir / f"{run_id}.txt").write_text(trace, encoding="utf-8")
        audit = {
            "run_id": run_id,
            "arm": "CPI" if vc else "No-CPI",
            "provider": provider_name,
            "prompt_chars": len(prompt),
            "reply_chars": len(reply),
            "timestamp": time.time(),
            "seed": seed
        }
        with open(args.audit, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
