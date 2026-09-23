"""
Shaping helpers shared by nozzles. Shaping = layout, order, trimming to a slot. Never content.
"""
import re

def strip_title(md):
    """Drop the H1 line and the italic example note, if present."""
    lines = md.strip().split("\n")
    lines = [l for l in lines if not l.startswith("# ")]
    lines = [l for l in lines if not (l.startswith("*") and l.endswith("*") and "example" in l.lower())]
    return "\n".join(lines).strip()

def compact(md):
    """Markdown sections → one prose block: `## Heading` becomes `Heading:`; numbered items become
    `(1) …`; bullets become `— …`; blank lines collapse. The words are untouched."""
    out = []
    for l in strip_title(md).split("\n"):
        s = l.strip()
        if not s: continue
        m = re.match(r"#+\s*(.+)", s)
        if m: out.append(f"{m.group(1).rstrip(':')}:"); continue
        m = re.match(r"(\d+)\.\s+(.+)", s)
        if m: out.append(f"({m.group(1)}) {m.group(2)}"); continue
        m = re.match(r"[-*]\s+(.+)", s)
        if m: out.append(f"— {m.group(1)}"); continue
        out.append(s)
    return " ".join(out)

def sections(md):
    """[(heading, text)] preserving order; text keeps its line structure."""
    res, cur, buf = [], None, []
    for l in strip_title(md).split("\n"):
        m = re.match(r"#+\s*(.+)", l.strip())
        if m:
            if cur is not None: res.append((cur, "\n".join(buf).strip()))
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(l)
    if cur is not None: res.append((cur, "\n".join(buf).strip()))
    return res

def fit(text, limit, marker="\n[… trimmed by the nozzle to fit the slot — the Carry is unchanged]"):
    """Trim to a slot's limit at a sentence boundary, with an explicit marker. Never silent."""
    if limit is None or len(text) <= limit: return text
    cut = text[:limit - len(marker)]
    cut = cut[:max(cut.rfind(". "), cut.rfind("\n"), 0) + 1] or cut
    return cut.rstrip() + marker
