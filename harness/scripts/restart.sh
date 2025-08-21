#!/usr/bin/env bash
set -euo pipefail

PAUSE_BETWEEN_RUNS_SECONDS="${PAUSE_BETWEEN_RUNS_SECONDS:-5}"
PROBLEM="${1:-P1}"   # P1 or P2

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPO="$ROOT/harness/problems/$PROBLEM"
OUT="$ROOT/traces/${PROBLEM}-runs"
mkdir -p "$OUT"
cd "$REPO"

while true; do
  # Reset working copy to clean HEAD
  git reset --hard >/dev/null 2>&1 || true
  if [[ "${GIT_CLEAN:-0}" == "1" ]]; then git clean -fdx >/dev/null 2>&1 || true; fi

  timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
  LOG_FILE="$OUT/${PROBLEM}_${timestamp}.txt"
  if [[ "$PROBLEM" == "P1" ]]; then
    echo "=== RUN P1 $timestamp ===" > "$LOG_FILE"
    python run.py >> "$LOG_FILE" 2>&1 || true
  else
    echo "=== RUN P2 $timestamp ===" > "$LOG_FILE"
    python deletekeys.py >> "$LOG_FILE" 2>&1 || true
  fi

  sleep "$PAUSE_BETWEEN_RUNS_SECONDS"
done
