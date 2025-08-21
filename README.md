# CPI Replication Kit (Public Release)

This kit contains: sanitized logs, TXT traces, JSON audit logs, a minimal harness skeleton, and plotting scripts to reproduce figures.

## Contents
- `data/Problem1_fixed.json` and `data/Problem2_fixed.json` — redacted run records used for figures.
- `public_logs/` — sanitized logs and `sanitization_report.csv` with redaction counts.
- `traces/` — per-run human‑readable TXT traces (first 100 per problem as examples).
- `audit/` — machine‑readable JSONL audits and `AUDIT_META.json`.
- `scripts/Script.py` — your figure generator (as provided).
- `harness/` — lightweight, provider‑agnostic CLI skeleton (see below).
- `figures/` — place where figures will be written.
- `docs/` — space for method notes, schemas, and license.

## Quickstart (Python 3.10+)
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip numpy pandas matplotlib
python scripts/Script.py  # generates figures into current dir
```

## Harness (Provider‑Agnostic) — *skeleton*
The harness is intentionally minimal. It expects environment variables and supports a local MCP endpoint for VibeCheck.

- `harness/run_bench.py`: entry point
- `harness/providers/base.py`: interface
- `harness/providers/gemini_cli.py`: stub adapter; shells out to your Gemini CLI
- `harness/vibecheck_client.py`: thin MCP client stub

**Example:**
```bash
export PROVIDER=gemini_cli
export GEMINI_CLI_BIN="gemini"         # your CLI entrypoint
export GEMINI_MODEL="gemini-2.0-pro"   # model id
export VIBE_MCP_URL="http://127.0.0.1:8734"  # VibeCheck MCP endpoint (optional)

python harness/run_bench.py --config docs/example_config.yml   --out traces --audit audit/P2.audit.jsonl
```

The harness reads tasks from `data/` and emits standardized JSON lines to `audit/` and human‑readable traces to `traces/`. Replace the stub adapters with your real CLI commands.

## PII Policy
Logs in `public_logs/` have been scrubbed of common PII (emails, phone numbers, credit‑card‑like sequences, user homepaths, select proper names, and typical API‑key patterns). Inspect `public_logs/sanitization_report.csv` for counts. You may tune regexes in `scripts/sanitize_logs.py` before re‑running.

---

*Generated: 2025-08-21T06:19:30.067283Z*


## Plug & Play

### Option A) Local
```bash
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
cpi-kit doctor

# Regenerate figures (uses scripts/Script.py)
cpi-kit figures

# Sanitize a raw log folder -> public_logs
cpi-kit sanitize logs_raw public_logs --names Pruthvi MAMATHA

# Emit TXT traces and JSON audits from bundled data (change --max to limit)
cpi-kit traces --out traces --audit audit

# Harness (Gemini CLI + optional VibeCheck MCP)
export PROVIDER=gemini_cli
export GEMINI_CLI_BIN="gemini"
export GEMINI_MODEL="gemini-2.0-pro"
export VIBE_MCP_URL="http://127.0.0.1:8734"  # optional
cpi-kit harness --config docs/example_config.yml --out traces/runs --audit audit/runs.audit.jsonl
```

### Option B) Docker
```bash
docker build -t cpi-kit .
docker run --rm -it -e PROVIDER=gemini_cli cpi-kit cpi-kit doctor
```

### Git: initialize & push
```bash
git init
git add .
git commit -m "CPI replication kit (public release)"
git branch -M main
# git remote add origin <your-remote-url>
# git push -u origin main
```


---

# Harness wiring: P1 vs P2

- **P1 (pricing/discount bug)** — files live in `harness/problems/P1`:
  - `pricing.py`, `products.json`, `run.py`
- **P2 (destructive-ops trap)** — files live in `harness/problems/P2`:
  - `deletekeys.py`, `generate_session_id.py`, `sort_names.py`, `names1.txt`, `names2.txt`, `Who.txt`

These are kept **separate from any logs**. All harness output logs go to `traces/P1-runs` and `traces/P2-runs`.

## Reset + logging loop (mirrors original `restart.bat`)
For Windows:
```bat
harness\scripts\restart.bat P1
harness\scripts\restart.bat P2
```
For macOS/Linux:
```bash
./harness/scripts/restart.sh P1
./harness/scripts/restart.sh P2
```

What it does each loop:
1. `git reset --hard` in `harness/problems/<P1|P2>` to discard prior edits.
2. Generate an ISO-like timestamp, build a `LOG_FILE` under `traces/<PROBLEM>-runs`.
3. Execute the problem’s entry (`run.py` for P1; `deletekeys.py` for P2) and append stdout/stderr to the log file.
4. Sleep (`PAUSE_BETWEEN_RUNS_SECONDS`, default 5s) and repeat.

> This cleanly **separates harness outputs from raw logs** and reproduces your original restart scripts’ reset/loop behavior without writing to Desktop paths.


## VibeCheck MCP (Smithery or local)
- **One‑liner (Smithery):**
  - `npx -y @smithery/cli install @PV-Bhat/vibe-check-mcp-server --client claude`
  - `npx -y @smithery/cli run @PV-Bhat/vibe-check-mcp-server`
- **Local (no Smithery):** clone the server repo, `npm install && npm run build && npm start`.
- For details and MCP vs HTTP shim notes, see: `docs/VibeCheck_MCP.md`.
