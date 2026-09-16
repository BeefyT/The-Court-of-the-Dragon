#!/usr/bin/env python3
"""gen_codex.py [SRC.json] [OUT.md]

Generates the Court of the Dragon codex from the Trench Companion JSON, which is
the authoritative artifact. Mechanical sections (armoury, battlekit, warband
entries, mercenaries, glory items, special rules, campaign) are derived from the
data so codex and app cannot drift. Prose sections that have no representation in
the app schema (the opening lore, the Bloodlines ladders) are held here as text."""
import json, sys, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(ROOT, "data", "CourtOfTheDragon-TrenchCompanion.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else \
    os.path.join(ROOT, "docs", "Court-of-the-Dragon-Codex.md")
SNAP = os.path.join(ROOT, "data", "core-keywords.json")

doc = json.load(open(SRC))
B = {b["type"]: {o["id"]: o for o in b["data"]} for b in doc["files"]}
ORDER = {b["type"]: [o["id"] for o in b["data"]] for b in doc["files"]}

# keyword display names: core snapshot + this homebrew
KWN = {}
try:
    KWN.update(json.load(open(SNAP)))
except FileNotFoundError:
    print("warning: data/core-keywords.json missing; core keyword names will "
          "fall back to their ids", file=sys.stderr)
for k in B.get("keyword", {}).values():
    KWN[k["id"]] = k["name"]

DUC, GLR = "\U0001F451", "\u263C"


DISPLAY = {
    "Carlig": "C\u00e2rlig",
    "The Calusar": "The C\u0103lu\u0219ar",
    "Calusar": "C\u0103lu\u0219ar",
    "The Cup of Targoviste": "The Cup of T\u00e2rgovi\u0219te",
    "Negru Voda": "Negru Vod\u0103",
    "The Tablia": "The T\u0103blia",
}


def disp(name):
    return DISPLAY.get(name, name)


def polish(t):
    """restore typography the app-safe JSON had to flatten"""
    for a, b in DISPLAY.items():
        t = t.replace(a, b)
    t = t.replace(" - ", " \u2014 ")
    t = re.sub(r"\+1 Glory\b", "+1\u263c", t)
    t = re.sub(r"\(\+1\u263c for", "(+1\u263c for", t)
    return t


def text(obj, joiner="\n"):
    return polish(joiner.join(d.get("content", "")
                              for d in obj.get("description", [])))


def paras(obj):
    return [polish(d.get("content", "")) for d in obj.get("description", [])]


def kwname(kid):
    return KWN.get(kid, kid.replace("kw_hb470028_", "").replace("kw_", "").upper())


def dice(n):
    return "\u2014" if n is None else (f"+{n} DICE" if n >= 0 else f"\u2212{abs(n)} DICE")


def movestr(m):
    return f"{m['movement']}\"/" + ("Flying" if m.get("movetype") == 1 else "Infantry")


def statline(m):
    s = m["stats"]
    rng = "\u2014" if s["ranged"] == 0 and not has_ranged(m["id"]) else dice(s["ranged"])
    arm = s["armour"] if s["armour"] else 0
    arm = f"\u2212{abs(arm)}" if arm < 0 else str(arm)
    return (f"| {movestr(s)} | {rng} | {dice(s['melee'])} | {arm} | {s['base'][0]}mm |")


def has_ranged(mid):
    """a model has a ranged characteristic if it can carry or is given ranged kit"""
    for r in B.get("modelequipmentrelationship", {}).values():
        if mid in r.get("model_id", []):
            for e in r.get("mandatory_equipment", []):
                if B.get("equipment", {}).get(e, {}).get("category") == "ranged":
                    return True
    m = B["model"][mid]
    restr = m.get("contextdata") or {}
    removed = (restr.get("model_equipment_restriction") or {}).get("removed", []) \
        if isinstance(restr, dict) else []
    blocked = {x["category"] for x in removed}
    return "ranged" not in blocked and m["stats"]["ranged"] != 0


def regen(m):
    c = m.get("contextdata")
    if isinstance(c, dict) and "regenerate_mod" in c:
        return c["regenerate_mod"]["value"]
    return None


def kwline(m):
    ks = [kwname(k) for k in m["keywords"]]
    r = regen(m)
    if r:
        ks.append(f"REGENERATE ({r})")
    return ", ".join(ks)


def eqcost(eid):
    for r in B["factionequipmentrelationship"].values():
        if r["equipment_id"] == eid:
            return r
    return None


def restriction_note(rel):
    c = rel.get("contextdata")
    if not isinstance(c, dict):
        return ""
    perm = (c.get("faction_eq_restriction") or {}).get("permitted", [])
    out = []
    for p in perm:
        if p["res_type"] == "keyword":
            out.append(f"{kwname(p['value'])} only")
        else:
            nm = disp(B["model"].get(p["value"], {}).get("name", p["value"]))
            out.append(f"{nm} only")
    return ", ".join(out)


def rowlabel(rel):
    eq = B["equipment"].get(rel["equipment_id"])
    name = disp(eq["name"] if eq else rel["name"])
    mark = " [\u2022]" if rel["equipment_id"].startswith("eq_dc_") else ""
    bits = []
    note = restriction_note(rel)
    if note:
        bits.append(note)
    if rel.get("limit"):
        bits.append(f"Limit {rel['limit']}")
    tail = f" \u2014 {', '.join(bits)}" if bits else ""
    return f"{name}{mark}{tail}"


# ---------------------------------------------------------------- prose blocks
LORE = """# THE COURT OF THE DRAGON
### A Warband for Trench Crusade

---

## THE DAMNED OF WALLACHIA

In the year 1573, when Byzantium had fallen and the Infernal advance crept north, the Sacred Order of the Dragon held the line in the hills of Wallachia. A million Heretics were impaled in those hills, and Heaven called it a miracle.

It was no miracle. It was a bargain.

The knights of the Order had gone to the Scholomance \u2014 the Devil's school hidden beneath the Carpathian peaks \u2014 and struck a pact for power enough to hold. Immortality. Blood-sorcery. The strength to drink the war itself. They took the loan meaning never to repay it: to turn Hell's own gift against Hell's own servants, and to keep the borrowed eternity for themselves.

Heaven named them apostates and shut its gates. Hell, whose every law is written in contracts and collateral, named them thieves \u2014 for in the theology of the Pit there is no sin worse than welshing on a debt. So the Court belongs to neither power. They are hunted by the angels they betrayed and the devils they cheated, and they answer to no master at all.

They answer only to the blood. For the power the Order stole was never truly theirs \u2014 they drank it, long ago, from three things older and hungrier that still sleep in the crypts beneath Castle Dracula. The Voivode rules the Court, deadliest of all his kind; yet even he is a child beside the Elders downstairs, from whose veins his own gift first came.

Now they march to the great war in greatcoats and grave-dust, a handful of immortal predators trailing a herd of the dominated and the bled. They are slow. They are few. And the longer the killing lasts, the stronger they become."""

BLOODLINES = """## THE BLOODLINES

The Court's power flows from three Elders sleeping in the crypts beneath Castle Dracula \u2014 the things the Voivode himself first drank from.

**Pledge.** At Warband creation, each **ELITE** vampire pledges to **one** Elder as its origin blood. This is per-model: a Warband may field a Mara Voivode beside a Cazimir Boyar. Origin blood is fixed and never changes. Pledging grants access to that Elder's **Elder Blood** purchase.

**Elder Blood** \u2014 bought with ducats at Warband creation. A vampire may take **1** Elder Blood gift, from its pledged Elder only.

**Bloodline Ladders** \u2014 earned in campaign. Every Elder has a three-rung ladder. An ELITE vampire may climb **any** Elder's ladder, not only its pledged one \u2014 power pulls the blood. Each ladder is climbed **bottom-up**: a rung may be taken only if the rung below it on that ladder is already held.

**Advancement \u2014 choose, don't roll.** When a Court ELITE vampire would make an Advancement Roll, it does not roll on the standard Skill Tables. Instead, choose any one Bloodline rung the model is currently eligible for and the model learns it.

---

### MARA, THE RED FAMINE

*The eldest and hungriest. Her blood is appetite; it climbs by killing and drinking, and it pays the whole Court back.*

**Elder Blood**

- **Glutton for Blood** *(25{DUC})* \u2014 its Feed ACTION grants 2 Sated instead of 1.

**Ladder**

1. **Sate the Kill** \u2014 when this model takes an enemy Out of Action with a Melee Attack, it gains 1 Sated (no action, no roll).
2. **Shared Feast** *(needs Sate the Kill)* \u2014 whenever this model gains Sated from Feeding or from Sate the Kill, one friendly VAMPIRE within 6" also gains 1 Sated. Once per Activation.
3. \u2605 **The Red Famine** *(needs Shared Feast)* \u2014 while Ascended, its Melee Attacks gain +1 INJURY DICE against any model carrying 1 or more BLOOD MARKERS.

### NEGRU VOD\u0102, THE THRONE OF THORNS

*The Black Voivode who ruled these mountains first. His blood is rulership \u2014 this ladder grows by holding the leash.*

**Elder Blood**

- **Crown of Dread** *(25{DUC})* \u2014 \u22121 DICE to all Success Rolls for enemy models within 6". With the bearer's FEAR, melee attacks against it suffer \u22122 in total. A model cannot suffer this penalty from more than one Crown of Dread.

**Ladder**

1. **Seat of Command** \u2014 gains the DOMINION keyword.
2. **The Driven Hunt** *(needs Seat of Command)* \u2014 friendly Blood-Crazed models within this model's Leash add +1 DICE to their Melee Attacks.
3. \u2605 **The Throne of Thorns** *(needs The Driven Hunt)* \u2014 enemies treat the area within 6" of this model as Difficult terrain, and while this model is on the battlefield and not Down, your Warband ignores the Shaken rule.

### CAZIMIR, THE HUNDRED-GRAVED

*Buried a hundred times, risen from every grave. His blood is the curse that will not let the body rest. It climbs by refusing to die.*

**Elder Blood**

- **Unhallowed Flesh** *(25{DUC})* \u2014 permanent \u22121 INJURY MODIFIER, which stacks with worn armour.

**Ladder**

1. **Knit the Wound** \u2014 its REGENERATE value rises by 1.
2. **Rise from the Mire** *(needs Knit the Wound)* \u2014 the first time it is taken Down each game, it immediately stands and may move 3". This does not trigger on a Grave-Law reform.
3. \u2605 **The Hundred Graves** *(needs Rise from the Mire)* \u2014 the first time this model would be taken Out of Action each game, it is instead removed and reforms at a friendly board edge at the start of your next Turn with 2 Sated. This does not trigger if the wound was caused by a FIRE or BLESSED attack.""".replace("{DUC}", DUC)

WARBAND_CREATION = f"""## WARBAND CREATION

- A starting Warband has **700 ducats ({DUC})**.
- It must include exactly one **Voivode**, who is its Leader.
- It may include no more than **6 models with the ELITE keyword**.
- Each ELITE vampire pledges to one Elder Bloodline (Mara, Negru Vod\u0103, or Cazimir) when it is recruited, and may buy 1 Elder Blood gift from that Elder.
- **Limited Potential:** the Shrike and the Leech cannot exceed 7 Experience Points, even if Promoted to ELITE.
- Mercenaries are hired with Glory ({GLR}) and follow **Neither Shepherd Nor Wolf**.
- Glory Items are purchased with Glory ({GLR}); see **Glory Items**.
- All other limits follow the standard rules of *Trench Crusade*."""

# ---------------------------------------------------------------- build
out = [LORE, "\n---\n"]

# --- special rules (core faction rules, in file order, minus the sectioned ones)
SECTIONED = {"rl_dragoncourt_longhunger", "rl_dragoncourt_gloryitems",
             "rl_dragoncourt_neithershepherd"}
out.append("## SPECIAL RULES\n")
out.append("These rules apply to every Court of the Dragon Warband.\n")
for rid in B["faction"]["fc_dragoncourt"]["rules"]:
    if rid in SECTIONED:
        continue
    r = B["factionrule"][rid]
    out.append(f"### {disp(r['name']).upper()}\n")
    for p in paras(r):
        out.append(p + "\n")

# --- new keywords
out.append("---\n")
out.append("## NEW KEYWORDS\n")
for kid in ORDER["keyword"]:
    k = B["keyword"][kid]
    tags = k.get("tags")
    if not (isinstance(tags, dict) and tags.get("type") == "tag"):
        continue
    out.append(f"**{disp(k['name'])}** \u2014 {text(k)}\n")

out.append("---\n")
out.append(BLOODLINES)
out.append("\n---\n")

# --- armoury
CATS = [("ranged", "Ranged Weapons"), ("melee", "Melee Weapons"),
        ("grenade", "Grenades & Indirect"), ("shield", "Shields"),
        ("armour", "Armour"), ("equipment", "Equipment")]
out.append("## ARMOURY\n")
out.append("Items marked [\u2022] are unique to the Court; their rules follow in "
           "**Court Battlekit**. Innate weapons are listed on their model's entry.\n")
INNATE = {"eq_dc_shrikeclaws", "eq_dc_deathshriek", "eq_dc_cullingknife"}
for cat, label in CATS:
    rows = [r for r in B["factionequipmentrelationship"].values()
            if r["costtype"] == 0 and r["equipment_id"] not in INNATE
            and B["equipment"].get(r["equipment_id"], {}).get("category") == cat]
    if not rows:
        continue
    rows.sort(key=lambda r: (r["cost"], rowlabel(r)))
    out.append(f"**{label}**\n")
    out.append("| Item | Cost |")
    out.append("|---|---|")
    for r in rows:
        out.append(f"| {rowlabel(r)} | {r['cost']}{DUC} |")
    out.append("")

# core equipment with no category in this file (imported ids) get their own table
misc = [r for r in B["factionequipmentrelationship"].values()
        if r["costtype"] == 0 and r["equipment_id"] not in INNATE
        and r["equipment_id"] not in B["equipment"]]
if misc:
    misc.sort(key=lambda r: (r["cost"], r["name"]))
    out.append("**From the Standard Armoury**\n")
    out.append("| Item | Cost |")
    out.append("|---|---|")
    for r in misc:
        out.append(f"| {rowlabel(r)} | {r['cost']}{DUC} |")
    out.append("")

# --- court battlekit
out.append("### Court Battlekit [\u2022]\n")
for eid in ORDER["equipment"]:
    eq = B["equipment"][eid]
    rel = eqcost(eid)
    if rel is None or rel["costtype"] == 1:
        continue
    if eid in INNATE:
        continue
    s = eq.get("stats") or {}
    bits = []
    if s.get("hands_melee"):
        bits.append(f"{s['hands_melee']}-Handed Melee")
    elif s.get("melee"):
        bits.append("Melee")
    if s.get("hands_ranged"):
        bits.append(f"{s['hands_ranged']}-Handed")
    if eq.get("distance"):
        bits.append(f"{eq['distance']}\"")
    cat = eq.get("category")
    if cat in ("shield", "armour", "equipment", "grenade") and not bits:
        bits.append(cat.capitalize())
    kws = [kwname(k) for k in eq.get("keywords", []) if not k.startswith("kw_hb")]
    head = " \u00b7 ".join(bits + kws) if (bits or kws) else cat.capitalize()
    out.append(f"**{disp(eq['name'])}** \u00b7 *{head}*  ")
    out.append(text(eq) + "\n")

out.append("---\n")

# --- warband entries
def entry_block(mid, rel):
    m = B["model"][mid]
    cost = f"{rel['cost']}{DUC}" if rel["cost_type"] == 0 else f"{rel['cost']}{GLR}"
    mx = rel["warband_maximum"]
    limit = "0\u20131 per Warband" if mx == 1 else \
        (f"0\u2013{mx} per Warband" if mx and mx > 0 else None)
    if rel["warband_minimum"] == 1 and mx == 1:
        limit = "1 per Warband"
    lines = [f"### {disp(m['name']).upper()} \u2014 {cost}\n"]
    lore = polish(" ".join(d.get("content", "") for d in m.get("lore", [])))
    intro = " ".join(x for x in [limit + "." if limit else "", lore] if x).strip()
    if intro:
        lines.append(f"*{intro}*\n")
    lines.append("| Movement | Ranged | Melee | Armour | Base |")
    lines.append("|---|---|---|---|---|")
    lines.append(statline(m) + "\n")
    desc = text(m)
    if desc:
        lines.append(f"**Battlekit:** {desc}  ")
    lines.append(f"**Keywords:** {kwline(m)}\n")
    for aid in m["abilities"]:
        a = B["ability"].get(aid)
        if not a:
            continue
        ps = paras(a)
        lines.append(f"**{disp(a['name'])}:** {ps[0]}\n")
        for extra in ps[1:]:
            lines.append(f"- {extra}\n")
    # orders / upgrades available to this model
    ups = [(u, r) for r in B.get("modelupgraderelationship", {}).values()
           if mid in r["model_id_set"]
           for u in [B["upgrade"][r["upgrade_id"]]]
           if not (isinstance(u.get("tags"), dict)
                   and u["tags"].get("special_category") == "bloodline")]
    if ups:
        lines.append("**Orders** \u2014 chosen when recruited.\n")
        for u, r in sorted(ups, key=lambda x: x[1]["cost"]):
            lines.append(f"- **{disp(u['name'])}** *({r['cost']}{DUC})* \u2014 {text(u)}\n")
    return "\n".join(lines)


ELITE = [mid for mid in ORDER["model"] if "kw_elite" in B["model"][mid]["keywords"]]
MERCS = [r["model_id"] for r in B["factionmodelrelationship"].values() if r["mercenary"]]
TROOPS = [mid for mid in ORDER["model"] if mid not in ELITE and mid not in MERCS]
RELBY = {r["model_id"]: r for r in B["factionmodelrelationship"].values()}

out.append("## ELITE WARBAND ENTRIES\n")
for mid in ELITE:
    out.append(entry_block(mid, RELBY[mid]))
out.append("---\n")
out.append("## TROOPS WARBAND ENTRIES\n")
for mid in TROOPS:
    out.append(entry_block(mid, RELBY[mid]))
out.append("---\n")

# --- mercenaries
out.append("## MERCENARIES\n")
r = B["factionrule"]["rl_dragoncourt_neithershepherd"]
out.append(f"**{r['name']}.** {text(r)}\n")
for mid in MERCS:
    out.append(entry_block(mid, RELBY[mid]))
out.append("---\n")

# --- glory items
out.append("## GLORY ITEMS\n")
gr = B["factionrule"]["rl_dragoncourt_gloryitems"]
out.append(text(gr) + "\n")
glory = [r for r in B["factionequipmentrelationship"].values() if r["costtype"] == 1]
glory.sort(key=lambda r: (r["cost"], r["name"]))
out.append("| Item | Stipulation | Cost |")
out.append("|---|---|---|")
for r in glory:
    bits = []
    note = restriction_note(r)
    if note:
        bits.append(note)
    if r.get("limit"):
        bits.append(f"Limit {r['limit']}")
    eq = B["equipment"].get(r["equipment_id"])
    nm = disp(eq["name"] if eq else r["name"])
    out.append(f"| {nm} | {', '.join(bits) or '\u2014'} | {r['cost']}{GLR} |")
out.append("")
out.append("### Glory Item Cartulary [\u2022]\n")
for r in glory:
    eq = B["equipment"].get(r["equipment_id"])
    if not eq:
        continue
    body = re.sub(r"^GLORY ITEM\.\s*", "", text(eq))
    body = re.sub(r"^(VAMPIRE only|ELITE only|DOMINION only|Consumable|Limit \d+)"
                  r"(, [^.]*)?\.\s*", "", body)
    out.append(f"**{disp(eq['name'])}**  ")
    out.append(body + "\n")

out.append("---\n")
out.append(WARBAND_CREATION)
out.append("\n---\n")

# --- campaign
lh = B["factionrule"]["rl_dragoncourt_longhunger"]
out.append("## CAMPAIGN PLAY \u2014 THE LONG HUNGER\n")
for p in paras(lh):
    out.append(p + "\n")

md = "\n".join(out)
md = re.sub(r"\n{3,}", "\n\n", md)
open(OUT, "w").write(md + "\n")
print("wrote", OUT, "|", len(md.split("\n")), "lines")
print("  elite:", len(ELITE), "troops:", len(TROOPS), "mercs:", len(MERCS),
      "glory:", len(glory))
