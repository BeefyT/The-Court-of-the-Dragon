#!/usr/bin/env python3
"""check.py - verify the generated codex still matches the JSON.

Run after any edit (`make check`). Exits non-zero if the two artifacts have
drifted, which is the failure this repo exists to prevent."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = os.path.join(ROOT, "data", "CourtOfTheDragon-TrenchCompanion.json")
MD = os.path.join(ROOT, "docs", "Court-of-the-Dragon-Codex.md")

DISPLAY = {
    "Carlig": "Cârlig",
    "The Calusar": "The Călușar",
    "Calusar": "Călușar",
    "The Cup of Targoviste": "The Cup of Târgoviște",
    "Negru Voda": "Negru Vodă",
    "The Tablia": "The Tăblia",
}
INNATE = {"eq_dc_shrikeclaws", "eq_dc_deathshriek", "eq_dc_cullingknife"}
DUC, GLR = "\U0001F451", "\u263C"


def disp(n):
    for a, b in DISPLAY.items():
        n = n.replace(a, b)
    return n


def main():
    doc = json.load(open(JSON))
    B = {b["type"]: b["data"] for b in doc["files"]}
    md = open(MD).read()
    errs, warns = [], []

    byid = {e["id"]: e for e in B["equipment"]}

    # every purchasable item appears with its cost
    for rel in B["factionequipmentrelationship"]:
        eid = rel["equipment_id"]
        if eid in INNATE:
            continue
        eq = byid.get(eid)
        name = disp(eq["name"] if eq else rel["name"])
        sym = DUC if rel["costtype"] == 0 else GLR
        if name not in md:
            errs.append(f"equipment missing from codex: {name}")
        elif not re.search(re.escape(name) + r"[^|\n]*\|[^|\n]*\|?\s*"
                           + str(rel["cost"]) + re.escape(sym), md):
            errs.append(f"cost row not found: {name} @ {rel['cost']}{sym}")

    # every model appears with its cost
    for rel in B["factionmodelrelationship"]:
        m = next(x for x in B["model"] if x["id"] == rel["model_id"])
        sym = DUC if rel["cost_type"] == 0 else GLR
        head = f"{disp(m['name']).upper()} \u2014 {rel['cost']}{sym}"
        if head not in md.upper():
            errs.append(f"model heading not found: {head}")

    # every faction rule the faction lists is printed
    rules = {r["id"]: r for r in B["factionrule"]}
    for rid in B["faction"][0]["rules"]:
        r = rules.get(rid)
        if not r:
            errs.append(f"faction lists unknown rule: {rid}")
        elif disp(r["name"]).upper() not in md.upper():
            errs.append(f"rule missing from codex: {r['name']}")

    # rules defined but not listed by the faction will never print
    for rid, r in rules.items():
        if rid not in B["faction"][0]["rules"]:
            warns.append(f"rule defined but not listed on the faction: {r['name']}")

    # abilities referenced by models must exist
    abil = {a["id"] for a in B["ability"]}
    for m in B["model"]:
        for a in m["abilities"]:
            if a not in abil:
                errs.append(f"{m['id']} references missing ability {a}")

    # every non-innate court item needs a Battlekit or Cartulary entry
    for eq in B["equipment"]:
        if eq["id"] in INNATE or not eq["id"].startswith("eq_dc_"):
            continue
        if disp(eq["name"]) not in md:
            errs.append(f"court item has no codex entry: {eq['name']}")

    # version string
    ver = " ".join(d["content"] for d in doc["description"])
    m = re.search(r"Rules v([0-9]+(?:\.[0-9]+)*)", ver)
    print(f"rules version: v{m.group(1) if m else '?'}")
    print(f"entities: {sum(len(v) for v in B.values())} across {len(B)} blocks")

    for w in warns:
        print("  warn:", w)
    if errs:
        print(f"\nFAILED - {len(errs)} problem(s):")
        for e in errs:
            print("  !", e)
        sys.exit(1)
    print("\nOK - codex matches the JSON")


if __name__ == "__main__":
    main()
