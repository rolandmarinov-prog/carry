"""
Nozzle: claude — the preferences slot (claude.ai → Settings → Profile → preferences).

Carries the STANCE only. Claude's preferences ride into every conversation, so the Self is
pasted per session, on request — that is what the no-state clause is for. Reference output: a
prose block that passed a cold-session test on 2026-09-23 — one block, laws inline, register,
the no-state clause, the source-of-truth line last.
"""
from adapters._shape import compact, fit

SLOT = "claude.ai → Settings → Profile → 'personal preferences' (rides into every chat)"
LIMITS = {"preferences": 2000}        # ASSUMED, not verified — the acceptance run verifies it
LIMIT = "preferences ~2,000 chars (assumed; verify in the vendor UI)"
NOTE = "Responds to plain declaratives. One block. Stance only; ask for the Self each session."

def render(self_body, stance_body, meta):
    block = compact(stance_body)
    return [("preferences", fit(block, LIMITS["preferences"]))]
