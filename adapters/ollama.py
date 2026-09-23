"""
Nozzle: ollama — a Modelfile SYSTEM block. Prior art: the CAMK3 Modelfile (laws first, then the
facts as of a date, then the register). Output is a complete Modelfile; `FROM` is a placeholder
the person sets. No TEMPLATE line — the base model's own chat template is inherited.

    ollama create mycarry -f Modelfile
"""
from adapters._shape import sections, strip_title

SLOT = "a Modelfile → SYSTEM \"\"\"…\"\"\" (local; `ollama create NAME -f Modelfile`)"
LIMITS = {"Modelfile": None}      # local: the model's context window is the only limit
LIMIT = "no slot limit (local); keep it short anyway — small models follow short systems better"
NOTE = "Laws first, then the Self as dated facts, then the register. Line structure preserved."

def render(self_body, stance_body, meta):
    date = meta["self"].get("date", "")
    st = sections(stance_body); sf = sections(self_body)
    parts = []
    for h, t in st:
        if h.lower().startswith("laws"): parts.append(f"LAWS\n{t}")
    parts.append(f"FACTS (as of {date})\n" + "\n\n".join(f"{h}\n{t}" for h, t in sf))
    for h, t in st:
        if not h.lower().startswith("laws"): parts.append(f"{h.upper()}\n{t}")
    system = "\n\n".join(parts)
    mf = ("# Modelfile rendered by the carry `ollama` nozzle — set FROM to your base model.\n"
          "FROM qwen3:14b\n"
          "PARAMETER temperature 0.4\n"
          'SYSTEM """\n' + system + '\n"""\n')
    return [("Modelfile", mf)]
