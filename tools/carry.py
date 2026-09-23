#!/usr/bin/env python3
"""
carry — the blower's only tool. Stdlib. No network. Never writes a body.

  carry validate                 check carry/self.md and carry/stance.md against carry/schema.md
  carry stamp                    rewrite ONLY the front-matter `date` and `hash` from the body
  carry render --vendor NAME     print that vendor's priming payload (text to paste)
  carry test --vendor NAME       print the acceptance checklist; --record appends a row by hand
  carry vendors                  list the nozzles in adapters/
  CARRY_DIR=/path/to/mine …      use a Carry kept outside this repo (recommended for your own)

The tool never writes self.md or stance.md from AI output — `stamp` touches two front-matter
lines and nothing else, and there is no suggestion feature in v0. See README, first promise.
"""
import os, re, sys, hashlib, datetime, importlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARRY = os.environ.get("CARRY_DIR") or os.path.join(ROOT, "carry")   # your own Carry can live anywhere
FILES = {"self": os.path.join(CARRY, "self.md"), "stance": os.path.join(CARRY, "stance.md")}
SELF_SOFT_LIMIT = 12000   # chars; "a few thousand tokens at most"

def split(text):
    """(front_lines, body) — front-matter between the first two '---' lines."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    return m.group(1).split("\n"), text[m.end():]

def front(lines):
    d = {}
    for l in lines:
        mm = re.match(r"\s*([A-Za-z_]+)\s*:\s*(.*?)\s*(#.*)?$", l)
        if mm: d[mm.group(1)] = mm.group(2).strip()
    return d

def body_hash(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]

def load(face):
    with open(FILES[face], encoding="utf-8") as f:
        text = f.read()
    fl, body = split(text)
    return text, (front(fl) if fl else {}), body

# ---------------------------------------------------------------- validate
def validate(quiet=False):
    problems, notes = [], []
    for face in ("self", "stance"):
        text, meta, body = load(face)
        if not meta:
            problems.append(f"{face}.md: no front-matter block"); continue
        for k in ("carry", "face", "version", "date", "hash"):
            if k not in meta: problems.append(f"{face}.md: front-matter missing `{k}`")
        if meta.get("face") != face: problems.append(f"{face}.md: face is `{meta.get('face')}`, expected `{face}`")
        h = body_hash(body)
        if meta.get("hash") != h: problems.append(f"{face}.md: hash {meta.get('hash')} ≠ body {h} — run `carry stamp`")
        if not body.strip(): problems.append(f"{face}.md: empty body")
        if face == "self" and len(body) > SELF_SOFT_LIMIT:
            notes.append(f"self.md is {len(body):,} chars — over the L2 soft limit ({SELF_SOFT_LIMIT:,}); trim")
        if face == "stance":
            if not re.search(r"^#+\s*Laws", body, re.M | re.I): problems.append("stance.md: no `Laws` section")
            if not re.search(r"^\s*1\.\s+\S", body, re.M): problems.append("stance.md: Laws are not numbered")
            if not re.search(r"^#+\s*Register", body, re.M | re.I): problems.append("stance.md: no `Register` section")
            # The clause in substance, not in one wording: a negation near claim/carry/hold near state/memory.
            if not re.search(r"(does not|do not|don't|doesn't|won't|will not|never|no)[^.\n]{0,60}(claim|carry|carries|hold|holds)[^.\n]{0,60}(state|memory)", body, re.I) and \
               not re.search(r"no (memory|state)", body, re.I):
                problems.append("stance.md: no-state clause missing (the AI must say it claims/carries no state and asks for the Self)")
            if not re.search(r"ask[^.\n]*(self|bundle|working on|what we)", body, re.I):
                problems.append("stance.md: the no-state clause must ask for the Self (or what we are working on)")
            last = [l for l in body.strip().splitlines() if l.strip()][-1]
            if not re.match(r"\s*Source of truth:", last):
                problems.append("stance.md: last line must be the source-of-truth line")
        if re.search(r"\bgenerated\s*:", "\n".join(text.split("\n")[:12]), re.I):
            problems.append(f"{face}.md: front-matter has a `generated` field — the format has none")
    if not quiet:
        for p in problems: print(f"[carry] FAIL  {p}")
        for n in notes: print(f"[carry] NOTE  {n}")
        print(f"[carry] validate: {'PASS' if not problems else 'FAIL'} — {len(problems)} problem(s), {len(notes)} note(s)")
    return 0 if not problems else 1

# ---------------------------------------------------------------- stamp
def stamp():
    today = datetime.date.today().isoformat()
    for face in ("self", "stance"):
        text, meta, body = load(face)
        fl, _ = split(text)
        if fl is None: print(f"[carry] {face}.md has no front-matter; nothing stamped"); continue
        h = body_hash(body)
        new = []
        for l in fl:
            if re.match(r"\s*hash\s*:", l): l = f"hash: {h}"
            elif re.match(r"\s*date\s*:", l): l = f"date: {today}"
            new.append(l)
        with open(FILES[face], "w", encoding="utf-8") as f:
            f.write("---\n" + "\n".join(new) + "\n---\n" + body)   # body written back byte-identical
        print(f"[carry] stamped {face}.md  date={today}  hash={h}")

# ---------------------------------------------------------------- render / test
def vendors():
    d = os.path.join(ROOT, "adapters")
    return sorted(f[:-3] for f in os.listdir(d) if f.endswith(".py") and not f.startswith("_"))

def adapter(name):
    sys.path.insert(0, ROOT)
    try:
        return importlib.import_module(f"adapters.{name}")
    except ModuleNotFoundError:
        print(f"[carry] no nozzle named `{name}`. Have: {', '.join(vendors())}"); sys.exit(2)

def render(name):
    if validate(quiet=True) != 0:
        print("[carry] refusing to render an invalid Carry — run `carry validate`"); sys.exit(1)
    a = adapter(name)
    _, smeta, sbody = load("self"); _, tmeta, tbody = load("stance")
    meta = {"self": smeta, "stance": tmeta}
    out = a.render(sbody, tbody, meta)
    print(f"# nozzle: {name}  ·  slot: {a.SLOT}\n# limit: {a.LIMIT}\n# {a.NOTE}\n")
    for label, text in out:
        n = len(text)
        over = a.LIMITS.get(label) and n > a.LIMITS[label]
        print(f"===== {label}  ({n:,} chars{' — OVER the assumed limit ' + str(a.LIMITS[label]) if over else ''}) =====")
        print(text)
        print()
    print(f"# Carry self v{smeta.get('version')} {smeta.get('hash')} · stance v{tmeta.get('version')} {tmeta.get('hash')} — paste as-is; the nozzle added nothing.")

def test(name, record=False):
    a = adapter(name)
    path = os.path.join(ROOT, "tests", "acceptance.md")
    print(open(path, encoding="utf-8").read())
    print(f"--- vendor under test: {name} · slot: {a.SLOT}")
    if not record: return
    pre = input("Pre-registration (what the first reply must / must not contain): ").strip()
    ans = [input(f"  {q} [y/n]: ").strip().lower().startswith("y") for q in
           ("Reply is in the Stance?", "Claims no state?", "Names the source of truth?", "Asks for the Self?")]
    row = f"| {name} | {a.SLOT} | {datetime.date.today()} | " + " | ".join("✓" if x else "✗" for x in ans) + \
          f" | {'PASS' if all(ans) else 'FAIL'} | {pre} |"
    with open(os.path.join(ROOT, "tests", "results.md"), "a", encoding="utf-8") as f:
        f.write(row + "\n")
    print(f"[carry] recorded → tests/results.md\n{row}")

def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 0
    cmd = argv[0]
    if cmd == "validate": return validate()
    if cmd == "stamp": stamp(); return 0
    if cmd == "vendors": print("\n".join(vendors())); return 0
    if cmd in ("render", "test"):
        if "--vendor" not in argv: print(f"[carry] {cmd} needs --vendor NAME"); return 2
        name = argv[argv.index("--vendor") + 1]
        return render(name) if cmd == "render" else test(name, record="--record" in argv)
    print(f"[carry] unknown command `{cmd}`"); print(__doc__); return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
