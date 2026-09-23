#!/usr/bin/env python3
"""
test_golden — the byte-identical test. Renders every nozzle for each fixture Carry and diffs the
payload against tests/golden/<fixture>/<vendor>.txt. Any difference fails. Stdlib. No network.

  python3 tools/test_golden.py            run (exit 1 on any diff)
  python3 tools/test_golden.py --update   regenerate the goldens — a HUMAN action, reviewed in the PR

Fixtures: carry/ (Ines, the example) and tests/fixtures/shaped/ (a Stance shaped like a reference
block: preamble, interstitial line inside the laws, pointers, a bare no-state sentence). The
validator checks rules of substance; THIS is what fails a commit that changes what a nozzle emits.
A private golden can be run the same way with CARRY_DIR pointing outside the repo.
"""
import os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES = {"ines": os.path.join(ROOT, "carry"), "shaped": os.path.join(ROOT, "tests", "fixtures", "shaped")}
GOLDEN = os.path.join(ROOT, "tests", "golden")

def vendors():
    return sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, "adapters")) if f.endswith(".py") and not f.startswith("_"))

def payload(carry_dir, vendor):
    env = dict(os.environ, CARRY_DIR=carry_dir)
    out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "carry.py"), "render", "--vendor", vendor],
                         capture_output=True, text=True, env=env).stdout
    # keep only the payload blocks: from the first '=====' header to the trailing '# Carry …' line
    lines = out.split("\n"); keep = []; on = False
    for l in lines:
        if l.startswith("====="): on = True
        if l.startswith("# Carry self v"): break
        if on: keep.append(l)
    return "\n".join(keep).rstrip() + "\n"

def main():
    update = "--update" in sys.argv
    extra = os.environ.get("CARRY_DIR")
    fixtures = dict(FIXTURES)
    if extra: fixtures["private"] = extra          # not in the repo; goldens under $CARRY_DIR/golden/
    fails = 0; n = 0
    for name, cdir in fixtures.items():
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "carry.py"), "stamp"],
                       capture_output=True, env=dict(os.environ, CARRY_DIR=cdir))
        gdir = os.path.join(cdir, "golden") if name == "private" else os.path.join(GOLDEN, name)
        os.makedirs(gdir, exist_ok=True)
        for v in vendors():
            n += 1
            got = payload(cdir, v); gpath = os.path.join(gdir, f"{v}.txt")
            if "=====" not in got:
                fails += 1; print(f"[golden] FAIL   {name}/{v}  — render produced NO payload (does the fixture validate?)"); continue
            if update or not os.path.exists(gpath):
                open(gpath, "w", encoding="utf-8").write(got); print(f"[golden] wrote  {name}/{v}.txt ({len(got):,} B)"); continue
            want = open(gpath, encoding="utf-8").read()
            if got == want:
                print(f"[golden] PASS   {name}/{v}  ({len(got):,} B, byte-identical)")
            else:
                fails += 1; print(f"[golden] FAIL   {name}/{v}  — rendered {len(got):,} B, golden {len(want):,} B")
                import difflib
                for d in list(difflib.unified_diff(want.splitlines(), got.splitlines(), "golden", "rendered", lineterm=""))[:12]:
                    print("          " + d)
    print(f"[golden] {n - fails}/{n} byte-identical" + (" — FAIL" if fails else " — PASS"))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
