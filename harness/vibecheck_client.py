
import os, json, urllib.request

class VibeCheckClient:
    def advise(self, prompt: str):
        url = os.getenv("VIBE_MCP_URL")
        if not url:
            return None
        try:
            data = json.dumps({"prompt": prompt}).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            # Non-fatal; treat as No-CPI
            return None
