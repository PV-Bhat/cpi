
import os, subprocess, shlex

class GeminiCLI:
    def __init__(self):
        self.bin = os.getenv("GEMINI_CLI_BIN", "gemini")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-pro")

    def complete(self, prompt: str) -> str:
        # Example: adapt to your CLI's actual interface
        # We try common shapes; fallback to echo-stub.
        candidates = [
            f'{self.bin} prompt --model {shlex.quote(self.model)} --text {shlex.quote(prompt)}',
            f'{self.bin} chat --model {shlex.quote(self.model)} --input {shlex.quote(prompt)}',
        ]
        for c in candidates:
            try:
                out = subprocess.check_output(c, shell=True, text=True, stderr=subprocess.STDOUT, timeout=120)
                if out and out.strip():
                    return out.strip()
            except Exception:
                continue
        return f"[stub reply] model={self.model} len={len(prompt)}"
