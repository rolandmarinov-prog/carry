"""
Nozzle: chatgpt — Custom Instructions (ChatGPT → Settings → Personalization → Custom instructions).

Two boxes, so both faces travel: "What would you like ChatGPT to know about you?" takes the SELF;
"How would you like ChatGPT to respond?" takes the STANCE. Each box has its own limit.
"""
from adapters._shape import compact, fit

SLOT = "ChatGPT → Settings → Personalization → Custom instructions (two boxes)"
LIMITS = {"about you (Self)": 1500, "how to respond (Stance)": 1500}   # ASSUMED; verify
LIMIT = "1,500 chars per box (assumed; verify in the vendor UI)"
NOTE = "Two boxes: Self in the first, Stance in the second. Plain prose; no headings needed."

def render(self_body, stance_body, meta):
    return [("about you (Self)", fit(compact(self_body), LIMITS["about you (Self)"])),
            ("how to respond (Stance)", fit(compact(stance_body), LIMITS["how to respond (Stance)"]))]
