# The Carry format (v0) — CC0 1.0

Two plain-text Markdown files. Human-readable, git-friendly, no database. Each begins with a
front-matter block, then the body. The body is the person's own words. Nothing else is required.

## Front-matter (both files)

```
---
carry: 0            # format version
face: self | stance
version: 3          # the person's own edit counter; bump when you change the body
date: 2026-09-23    # when this version was written
hash: 3f9a1c0d2b7e  # sha256 of the body (everything after the closing ---), first 12 hex
---
```

`tools/carry.py stamp` fills `date` and `hash` from the body. It never touches the body.

## `self.md` — the Self: who the person is, what is live, which corrections stand

Size: L2 — a few thousand tokens at most (validator warns above ~12,000 characters). Sections are
free, but these three answer the questions an AI will otherwise guess at:

1. **Who I am** — name or handle, what you do, what you already know (so it stops explaining),
   what you are working on. Facts you are willing to have any AI read.
2. **What is live** — the open threads a fresh AI should know the *state* of. Dated. Remove what
   has closed.
3. **Corrections that stand** — things AIs have got wrong about you that you do not want to
   re-teach. "I am not a beginner at X." "Do not assume Y."

## `stance.md` — the Stance: how the AI is to meet the person

Size: small — it rides into the vendor's smallest slot. Four parts, all required by the validator:

1. **Laws** — the few rules that are not negotiable in how you are met (honesty, no flattery,
   whatever yours are). Number them.
2. **Register** — how you want to be spoken to: length, tone, what to do when it disagrees.
3. **The no-state clause** — the AI must open a new session by saying it holds no memory of you
   and claims none, and by asking for the Self. Required wording, in substance:
   *"I don't carry state between sessions and won't claim any. Send the Self, or say what we're on."*
4. **The source-of-truth line** — the last line, verbatim:
   *"Source of truth: the Carry on my own machine, never this note."*
   (Substitute the location if yours differs; keep the shape.)

## What may never be in either file

Nothing written by an AI that the person has not typed in themselves. Nothing a vendor adapter
added. The format has no field for "generated"; if it appears, the file is wrong.
