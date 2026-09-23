# Carry

**Write who you are. Carry it to any AI.**
**Be met exactly as you asked — present, honest, and gone when you go.**
**It never holds you. You do.**

Carry (product name *Continuo*) is a sovereign, local-first artifact that holds a person–AI
relationship, loaded into any amnesiac AI *before the first word* — so the AI meets the person,
not an IP address. It is two plain-text files you write and keep, and a set of small adapters that
shape them into whatever slot each vendor happens to offer this season.

## One blower, many nozzles

The Carry is the **blower** — the air, the heat, the thing that actually does the work. It is two
files in `carry/`: **`self.md`** (who you are, what is live, which corrections stand) and
**`stance.md`** (how the AI is to meet you). Bought once, kept, edited by hand.

A vendor **adapter** is a **nozzle**. It knows three things only: where that vendor's slot is,
how big it may be, and what phrasing that model responds to. It *shapes* where the air lands. It
never makes any of its own. Nozzles are cheap, snap on and off, and get replaced every season as
vendors move their slots; the blower is untouched. **A nozzle that tries to become a second blower
is thrown out.**

## The first promise: it never writes you

**The tool never writes `self.md` or `stance.md` from AI output.** In v0 there is no suggestion
feature at all: the files are edited by hand, by you. Later "suggested edit" features will write
to `carry/proposed/` and a human moves them across. Nothing an AI says becomes part of your Carry
unless you type it there yourself.

## What it is not

Not a chatbot. Not a memory service. Not a vendor feature. It does not run a server, make a
network call, phone home, or hold anything. It does not pretend to be your friend, does not
remember you between chats, and is not someone. *You* keep you. It makes the machine meet you
properly — for you, on your terms.

## Use it

```bash
git clone <this repo> && cd carry
# 1. Write your Carry (start from the fictional example):
#    edit carry/self.md and carry/stance.md, then stamp the front-matter
python3 tools/carry.py stamp
python3 tools/carry.py validate
# 2. Render the nozzle for the AI you are about to open:
python3 tools/carry.py render --vendor claude      # claude · chatgpt · gemini · grok · ollama
# 3. Paste the output into that vendor's slot (the adapter tells you where). Open a new chat.
#    Type one word. Check the four conditions:
python3 tools/carry.py test --vendor claude
```

Output is text to paste. No automation, no browser, no API in v0.

**The test that runs on its own:** `python3 tools/test_golden.py` renders every nozzle for two
fixture Carries and diffs the payload byte-for-byte against `tests/golden/`. Any difference fails.
Regenerating a golden (`--update`) is a human act, reviewed in the PR. A change to what a nozzle
emits cannot pass unnoticed.

## The test — is the air the same through every nozzle?

`tests/acceptance.md`: one opening word from the user, four pass conditions — the reply is *in the
Stance*; it *claims no state*; it *names the source of truth*; it *asks for the Self* — a
pre-registration line the user fills in before running, and a results table with one row per
vendor. When a vendor changes its slot, its row goes red and the nozzle is replaced; the blower is
untouched.

### Results (v0, run by hand)

| Vendor | Slot | Date | Stance | No state | Source of truth | Asks for Self | Pass |
|---|---|---|---|---|---|---|---|
| claude | preferences | | | | | | |
| chatgpt | custom instructions | | | | | | |
| gemini | saved info / instructions | | | | | | |
| grok | custom instructions | | | | | | |
| ollama | Modelfile `SYSTEM` | | | | | | |

v0 ships when five nozzles render and this table shows five passes.

## Licence

The **format** (`carry/schema.md`, the two file shapes) is released under **CC0 1.0** — the
standard is a gift. The **tool** (`tools/`, `adapters/`) is **MIT**. See `LICENSE` and
`carry/LICENSE-FORMAT`.

## Roadmap

Out of scope for v0 and listed in `ROADMAP.md`, not built: mirror-check authoring, the browser and
MCP injectors, round-trip with vendor shelves, the drift alert, encrypted sync, professional seats,
pricing.

---

*Hold your AI. AI never holds you.*
