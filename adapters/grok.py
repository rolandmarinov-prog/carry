"""
Nozzle: grok — Custom instructions / personalization (Grok → Settings → Customize).

One box. Stance first, then the Self.
"""
from adapters._shape import compact, fit

SLOT = "Grok → Settings → Customize / custom instructions (one box)"
LIMITS = {"custom instructions": 2000}    # ASSUMED; verify
LIMIT = "~2,000 chars (assumed; verify in the vendor UI)"
NOTE = "Stance first, then Self. Direct imperatives; keep the laws numbered."

def render(self_body, stance_body, meta):
    text = compact(stance_body) + "\n\n" + compact(self_body)
    return [("custom instructions", fit(text, LIMITS["custom instructions"]))]
