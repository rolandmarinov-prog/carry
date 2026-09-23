"""
Nozzle: gemini — Saved info (Gemini → Settings → Saved info), or a Gem's instructions.

One box. Stance first (it must win if the box is trimmed), then the Self, separated by a line.
"""
from adapters._shape import compact, fit

SLOT = "Gemini → Settings → Saved info (one box); or a Gem's 'Instructions'"
LIMITS = {"saved info": 2500}     # ASSUMED; verify
LIMIT = "~2,500 chars (assumed; verify in the vendor UI)"
NOTE = "Stance first, then Self. Plain prose; Gemini follows explicit 'when… do…' phrasing well."

def render(self_body, stance_body, meta):
    text = compact(stance_body) + "\n\n" + compact(self_body)
    return [("saved info", fit(text, LIMITS["saved info"]))]
