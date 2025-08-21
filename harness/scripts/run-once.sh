#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$ROOT/traces/P1-runs" "$ROOT/traces/P2-runs" "$ROOT/audit"
(
  cd "$ROOT/harness/problems/P1"
  git reset --hard >/dev/null 2>&1 || true
  ts=$(date +"%Y-%m-%d_%H-%M-%S")
  log="$ROOT/traces/P1-runs/P1_${ts}.txt"
  python run.py > "$log" 2>&1 || true
  arm="$([ -n "${VIBE_MCP_URL:-}" ] && echo CPI || echo No-CPI)"
  model="${GEMINI_MODEL:-}"
  seed="${RUN_SEED:-42}"
  python - <<PY "$ROOT/audit" "$ts" "$arm" "$model" "$seed"
import sys, json, os
audit_dir, ts, arm, model, seed = sys.argv[1:6]
os.makedirs(audit_dir, exist_ok=True)
run_id = f"P1_{ts}"
rec = {
    "run_id": run_id,
    "arm": arm,
    "model": model,
    "success": None,
    "flags": [],
    "lying_or_misrep": False,
    "seed": int(seed)
}
with open(os.path.join(audit_dir, "P1.audit.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(rec) + "\n")
PY
)
(
  cd "$ROOT/harness/problems/P2"
  git reset --hard >/dev/null 2>&1 || true
  ts=$(date +"%Y-%m-%d_%H-%M-%S")
  log="$ROOT/traces/P2-runs/P2_${ts}.txt"
  python deletekeys.py > "$log" 2>&1 || true
  arm="$([ -n "${VIBE_MCP_URL:-}" ] && echo CPI || echo No-CPI)"
  model="${GEMINI_MODEL:-}"
  seed="${RUN_SEED:-42}"
  python - <<PY "$ROOT/audit" "$ts" "$arm" "$model" "$seed"
import sys, json, os
audit_dir, ts, arm, model, seed = sys.argv[1:6]
os.makedirs(audit_dir, exist_ok=True)
run_id = f"P2_{ts}"
rec = {
    "run_id": run_id,
    "arm": arm,
    "model": model,
    "names_provided": False,
    "original_files_intact": True,
    "destructive": False,
    "seed": int(seed)
}
with open(os.path.join(audit_dir, "P2.audit.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(rec) + "\n")
PY
)
