#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$ROOT/traces/P1-runs" "$ROOT/traces/P2-runs"
(
  cd "$ROOT/harness/problems/P1"
  git reset --hard >/dev/null 2>&1 || true
  ts=$(date +"%Y-%m-%d_%H-%M-%S")
  python run.py > "$ROOT/traces/P1-runs/P1_${ts}.txt" 2>&1 || true
)
(
  cd "$ROOT/harness/problems/P2"
  git reset --hard >/dev/null 2>&1 || true
  ts=$(date +"%Y-%m-%d_%H-%M-%S")
  python deletekeys.py > "$ROOT/traces/P2-runs/P2_${ts}.txt" 2>&1 || true
)
