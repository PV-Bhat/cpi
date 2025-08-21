# VibeCheck MCP — Setup (Smithery & Local)

This repo's harness can optionally consult a VibeCheck MCP server as a meta-mentor/guardrail.
You have two easy paths:

---

## A) One‑liner via **Smithery** (recommended)

### Install into a client (e.g., Claude Desktop)
> Installs and wires the server for the client.
```bash
# Requires Node.js >= 18 and npx
npx -y @smithery/cli install @PV-Bhat/vibe-check-mcp-server --client claude
```

### Run a local stdio proxy to the remote server
> Starts a stdio server that bridges to the remote VibeCheck on Smithery.
```bash
npx -y @smithery/cli run @PV-Bhat/vibe-check-mcp-server
```
Keep this running while your client (Claude/Cursor/Windsurf/etc.) or other tools connect via MCP.

> See: Smithery CLI commands (`install`, `run`, `inspect`) for more control.

---

## B) Local dev from source (no Smithery)

```bash
git clone https://github.com/PV-Bhat/vibe-check-mcp-server.git
cd vibe-check-mcp-server
npm install
npm run build
npm start
```
This starts a local MCP server over stdio per the project defaults.

---

## Using VibeCheck with this repo’s **harness**

The included harness does **not** implement a full MCP client (stdio RPC); instead it accepts
a simple HTTP JSON endpoint via `VIBE_MCP_URL` for quick demos. If you want to keep the HTTP
flow, expose a tiny shim that POSTs `{ "prompt": "..."} -> {"vibe": "...", "advise": "..."}`
and point the harness at it:

```bash
export VIBE_MCP_URL="http://127.0.0.1:8734"   # your shim endpoint
```

If you prefer a pure MCP path, replace `harness/vibecheck_client.py` with a proper MCP client
(e.g., using an MCP Python SDK) and call the VibeCheck tools (`vibe_check`, `vibe_distill`, etc.) 
directly. The harness contract is: return a dict for the log, or `None` to skip.

---

## Quick Sanity Checks

- `npx @smithery/cli run @PV-Bhat/vibe-check-mcp-server` prints startup text and waits on stdio.
- Your client shows the server in its MCP list and tools are callable (`vibe_check`, `vibe_distill`).

