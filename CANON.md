# CANON — durable decisions (by PR)

- **2026-09-23 · v0 shape.** One blower, many nozzles. The two files in `carry/` are the only
  source of content. An adapter knows where the slot is, how big it may be, and what phrasing the
  model responds to — and never adds content. An adapter that carries content is a bug.
- **2026-09-23 · Non-authoring.** The tool never writes `self.md` or `stance.md` from AI output.
  v0 has no suggestion feature. Later suggestions land in `carry/proposed/`; a human moves them.
- **2026-09-23 · Which face goes where.** Claude preferences: Stance only (Self is pasted per
  session). ChatGPT: Self in "about you", Stance in "how to respond". Gemini, Grok: Stance first,
  then Self, one box. Ollama: Modelfile SYSTEM, laws → facts → register (CAMK3 is the prior art).
  Reason: a slot that rides into every conversation on a surface with an autonomous editor may
  carry a Stance, never a Self.
- **2026-09-23 · Limits are assumed until the acceptance run verifies them.** Every `LIMITS`
  value in `adapters/` is marked assumed; the results table is where they become facts.
- **2026-09-23 · Compatibility is the acceptance criterion.** v0 ships when five nozzles render and
  the README table shows five hand-run passes. No telemetry, no server, no network calls.
- **2026-09-23 · Licences.** Format CC0 1.0 (the standard is a gift). Tool MIT. Paid layer later.
- **2026-09-23 · The validator checks the no-state clause in substance, not in one wording.** The
  first regex would have failed the very block that passed the reference cold test ("does not
  claim a state it has not been given"; "asks for the bundle"). Loosened to negation + claim/carry
  /hold + state/memory, and Self/bundle/what-we-are-on. The standard for a nozzle is stricter than
  the validator's: rendered through `claude`, a Stance holding the reference block reproduced it
  **byte-for-byte (1,279 B)**. That is the test any future nozzle change must still pass.
- **2026-09-23 · Byte-identical is a test, not a sentence** (CAM's T-2 challenge). `tools/test_golden.py`
  renders every nozzle for two fixtures — Ines, and a fictional Stance shaped like the reference block
  (preamble, interstitial line, pointers, bare no-state sentence) — and diffs against `tests/golden/`.
  An empty render is a FAIL, never a golden (the first run minted 1-byte goldens; caught the same hour).
  The real reference block stays out of this public repo by the sweep rules; it is tested privately
  through `CARRY_DIR` with the same script.
