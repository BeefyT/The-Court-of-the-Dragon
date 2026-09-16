#!/usr/bin/env python3
"""patch_court.py BASE.json [OUT.json]

Adds the v0.10 content to the existing in-app Court of the Dragon homebrew.
Additive by design: existing entries are left byte-identical unless listed in
EDITS below. Re-running is safe - entries are matched by id and replaced, not
duplicated."""
import json, sys, copy

HB = 470028
SRC = "homebrew"
FC = "fc_dragoncourt"

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEF = os.path.join(ROOT, "data", "CourtOfTheDragon-TrenchCompanion.json")
BASE = sys.argv[1] if len(sys.argv) > 1 else DEF
OUT = sys.argv[2] if len(sys.argv) > 2 else DEF


def D(*p, t="paragraph"):
    return [{"tags": {"desc_type": t}, "content": x} for x in p]


def I(t):
    return [{"tags": {"desc_type": "italic"}, "content": t}]


def KWH(s):
    return f"kw_hb{HB}_{s}"


# ---------------------------------------------------------------- new keywords
def wkw(slug, name, desc):
    return {"id": KWH(slug), "source": SRC, "tags": [], "name": name,
            "contextdata": [], "description": D(desc)}


NEW_KEYWORDS = [
    wkw("chokedamp", "Choke-Damp",
        "A Ranged Attack made with this weapon may target a friendly model."),
    wkw("hookholds", "The Hook Holds",
        "When an enemy model within 1\" of the wielder takes a Retreat ACTION, place 1 BLOOD MARKER "
        "next to that enemy model before any Melee Attacks allowed by the retreat are resolved."),
    wkw("laidatthethroat", "Laid at the Throat",
        "+1 INJURY DICE against a model that has 1 or more BLOOD MARKERS."),
    wkw("ninewinters", "Nine Winters Buried",
        "Counts as Standard Armour. Increases the wearer's REGENERATE by 1, to a maximum of "
        "REGENERATE (2). The wearer's Movement is reduced by 1\"."),
    wkw("gravesmoke", "Grave-Smoke",
        "At the end of this model's Activation, place 1 BLOOD MARKER on 1 enemy model within 8\"."),
    wkw("chainedatshoulder", "Chained at the Shoulder",
        "At the start of each of the Leech's Activations, if a friendly Bled is within 2\", you may "
        "make an Injury Roll against that Bled. If you do, the Leech gains 1 Sated."),
    wkw("driventogether", "Driven Together",
        "While a friendly Bled is within 6\" of a model with a Herd-Bell, the range of its Cattle "
        "rule is 6\" instead of 3\"."),
    wkw("hewnfrozenlake", "Hewn from the Frozen Lake",
        "After the attack has been resolved, the area within 3\" of the target point is treated as "
        "Difficult terrain until the end of the following Turn. This affects all models, friend and "
        "foe."),
]

# ---------------------------------------------------------------- new faction rules
def rule(i, name, *p):
    return {"id": i, "name": name, "description": D(*p), "source": SRC,
            "tags": [], "contextdata": [], "options": []}


NEW_RULES = [
    rule("rl_dragoncourt_neithershepherd", "Neither Shepherd Nor Wolf",
         "For Mercenary recruitment, a Court of the Dragon Warband is neither Faithful nor Fallen. "
         "It may not recruit the Mercenaries in Warbands of Trench Crusade - including those "
         "available to any Warband - and may instead recruit the Court Mercenaries. Each is 0-1."),
    rule("rl_dragoncourt_gloryitems", "Court Glory Items",
         "A Court of the Dragon Warband may purchase the Court Glory Items. It may also purchase "
         "Glory Items available to any Warband, with two exceptions: it may not purchase a Trench "
         "Dog (see The Grey Brothers) or a Sniper Scope (see Nightglass Sight)."),
    rule("rl_dragoncourt_longhunger", "Campaign Play: The Long Hunger",
         "This replaces the Trauma Step for a Court Warband. All other Campaign Phase steps are "
         "unchanged. The herd - the Bled and the Strix - are mortal and live and die by the standard "
         "rules. All rates in this rule are provisional.",
         "The Thirst: an ELITE vampire never rolls on the Trauma Table and never gains Battle Scars. "
         "Instead, in the Trauma Step, if it was taken Out of Action during the game it gains 1 "
         "Thirst Marker. 1 Thirst - Fraying: it becomes Blood-Crazed at 4+ Sated instead of 5+. "
         "2 Thirst - Slipping: halve its Leash ranges, both projected and received. 3 Thirst - Lost: "
         "replace its entry on your Warband Roster with a Shrike; its Experience and Skills are gone "
         "and its Battlekit moves to your Arsenal.",
         "If the Voivode is Lost, promote one Boyar to Voivode - keeping its Experience, Skills and "
         "any Battlekit it can legally carry - or recruit a new Voivode at the Quartermaster Step.",
         "Torpor: the Shrike and the Leech make Survival Rolls as normal Troops, but on a 1-2 they "
         "are not removed from your roster - they enter Torpor and miss the next battle.",
         "The Vintage: when your Warband collects Loot in the Exploration Step, you may take any "
         "portion of it as Vintage instead of ducats, at 10 ducats = 1 Vintage. Vintage cannot be "
         "spent on Battlekit, Glory Items or recruits. In the Quartermaster Step you may spend 10 "
         "Vintage to remove 1 Thirst Marker from one vampire, no more than once per Campaign Phase."),
]

# ---------------------------------------------------------------- mercenary abilities
def ab(i, name, *p):
    return {"id": i, "name": name, "source": SRC,
            "tags": {"trait": True, "homebrew_id": HB}, "contextdata": [],
            "description": D(*p), "options": []}


NEW_ABILITIES = [
    ab("ab_dc_stanchthevein", "Stanch the Vein",
       "Once per Turn, when a friendly VAMPIRE resolves a Feed ACTION or Offer the Vein against a "
       "friendly Bled within 3\", the Bled suffers no Injury Roll and gains no BLOOD MARKER."),
    ab("ab_dc_anexactscience", "An Exact Science",
       "+1 DICE to the Risky Success Roll for a Treat ACTION carried out by the Vein-Wife."),
    ab("ab_dc_thecircle", "The Circle",
       "While not Down, a Calusar counts as 3 models for the purposes of controlling Objectives."),
    ab("ab_dc_unmoved", "Unmoved",
       "A Calusar cannot be moved by any rule other than its own Activation."),
    ab("ab_dc_thedance", "The Dance (ACTION)",
       "Take a Risky Success Roll. On a Failure the Calusar's Activation ends. On a Success or "
       "Critical Success, remove 2 Sated from a friendly VAMPIRE within 3\"."),
    ab("ab_dc_therainbook", "The Rain-Book (ACTION)",
       "Take a Risky Success Roll. On a Failure the Solomonar's Activation ends. On a Success pick "
       "one of the following; on a Critical Success pick one or both. The effect lasts until the "
       "start of his next Activation. Hail: -1 DICE to all Ranged Attacks made by any model. "
       "Mountain Fog: no model may be targeted by a Ranged Attack made from more than 12\" away."),
    ab("ab_dc_mistofthepasses", "Mist of the Passes",
       "-1 DICE to Ranged Attacks that target the Solomonar."),
    ab("ab_dc_rendingclaws", "Rending Claws",
       "A Priculici can make a Melee Attack with IGNORE ARMOUR even though it has no Melee Weapon."),
    ab("ab_dc_prisetheshell", "Prise the Shell",
       "+1 INJURY DICE to Melee Attacks made by a Priculici if the target has the ARTIFICIAL keyword "
       "or has a piece of Armour Battlekit."),
    ab("ab_dc_sworntotheblood", "Sworn to the Blood",
       "When you recruit a Priculici, before adding it to your roster, you can say it will form a "
       "FIRETEAM with 1 other model in your Warband. Both models gain the FIRETEAM keyword. This "
       "Fireteam is in addition to any other Fireteams your Warband can have."),
    ab("ab_dc_themastersdebt", "The Master's Debt",
       "When the Priculici's Fireteam partner is taken Out of Action, the Priculici becomes "
       "Blood-Crazed for the rest of the game. While Blood-Crazed its Melee Attacks gain +1 INJURY "
       "DICE, it may take no ACTION other than Move, Dash, Charge or Fight, and it must Charge the "
       "model that took its partner Out of Action if able, or the nearest enemy model if it cannot."),
    ab("ab_dc_mercpotential", "Limited Potential",
       "This model cannot have more than 7 Experience Points."),
]

# ---------------------------------------------------------------- mercenary models
ALLCAT = ["equipment", "melee", "ranged", "grenade", "armour", "shield"]


def norestrict(cats=None):
    return {"removed": [{"category": c, "res_type": "all", "value": ""}
                        for c in (cats or ALLCAT)]}


def model(i, name, mv, rng, mel, arm, bs, kws, abs_, desc, lore,
          movetype=0, potential=0, regen=None, restrict=None):
    ctx = {}
    if restrict:
        ctx["model_equipment_restriction"] = restrict
    if regen:
        ctx["regenerate_mod"] = {"value": regen}
    return {"id": i, "name": name, "source": SRC, "tags": [],
            "contextdata": ctx if ctx else [],
            "description": D(desc, t="default"), "lore": I(lore), "team": "none",
            "stats": {"movement": mv, "melee": mel, "ranged": rng, "base": [bs],
                      "armour": arm, "movetype": movetype, "potential": potential},
            "keywords": kws, "abilities": abs_}


NEW_MODELS = [
    model("md_dragoncourt_veinwife", "The Vein-Wife", 6, 0, 0, -1, 25,
          ["kw_negate"], ["ab_dc_stanchthevein", "ab_dc_anexactscience", "ab_dc_mercpotential"],
          "The Vein-Wife has Standard Armour, a Gas Mask, a Medi-kit and a Culling Knife.",
          "She knows exactly how much a body can give and still stand at the plough.",
          restrict=norestrict()),
    model("md_dragoncourt_calusar", "The Calusar", 6, 0, 1, 0, 32,
          ["kw_negate", "kw_tough"],
          ["ab_dc_thecircle", "ab_dc_unmoved", "ab_dc_thedance", "ab_dc_mercpotential"],
          "The Calusar has a Trench Club (the ritual staff) and a Sword/Axe (the wooden sword, "
          "iron-shod).",
          "He does not consider himself a mercenary. He is a physician.", restrict=norestrict()),
    model("md_dragoncourt_solomonar", "The Solomonar", 6, 1, 0, 0, 32,
          ["kw_negate"],
          ["ab_dc_therainbook", "ab_dc_mistofthepasses", "ab_dc_mercpotential"],
          "The Solomonar has a Polearm - an iron-shod weather-staff.",
          "Ten scholars enter the Scholomance; nine walk out. He paid, and owes nothing to anyone "
          "since.", restrict=norestrict()),
    model("md_dragoncourt_priculici", "The Priculici", 10, 0, 2, 0, 40,
          ["kw_fear", "kw_flying", "kw_fireteam"],
          ["ab_dc_rendingclaws", "ab_dc_prisetheshell", "ab_dc_sworntotheblood",
           "ab_dc_themastersdebt", "ab_dc_mercpotential"],
          "A Priculici cannot have any Battlekit.",
          "Some the blood took further down, until the man was gone and only the appetite and the "
          "wings remained.", movetype=1, regen=1, restrict=norestrict()),
]

NEW_FMR = [
    ("md_dragoncourt_veinwife", 3), ("md_dragoncourt_calusar", 5),
    ("md_dragoncourt_solomonar", 6), ("md_dragoncourt_priculici", 6),
]
NEW_FACTIONMODELREL = [
    {"id": f"rel_dragoncourt_fc_{mid}", "source": SRC, "tags": [], "name": "",
     "contextdata": {"option_search_viable": []}, "options": [], "faction_id": [FC],
     "model_id": mid, "captain": False, "mercenary": True, "cost": c, "cost_type": 1,
     "restricted_models": [], "warband_minimum": 0, "warband_maximum": 1}
    for mid, c in NEW_FMR
]


# ---------------------------------------------------------------- new equipment
def eqp(i, name, cat, dist, stats, kws, desc, ctx=None):
    c = {"get_weapon": []} if cat in ("ranged", "melee", "grenade") else {}
    if ctx:
        c.update(ctx)
    return {"id": i, "name": name, "source": SRC,
            "tags": {"trait": True, "homebrew_id": HB},
            "category": cat, "distance": dist, "stats": stats,
            "contextdata": c if c else [], "description": D(desc, t="default"),
            "lore": [], "options": [], "keywords": kws, "modifiers": [], "abilities": []}


R1 = {"hands_ranged": 1, "ranged": True}
R2 = {"hands_ranged": 2, "ranged": True}
M1 = {"hands_melee": 1, "melee": True}

NEW_EQUIP = [
    eqp("eq_dc_herdbell", "Herd-Bell", "equipment", None, [], [KWH("driventogether")],
        "Limit 1. A cracked bellwether's bell; the herd has stopped noticing which of them is "
        "wearing it. Driven Together: while a friendly Bled is within 6\" of a model with a "
        "Herd-Bell, the range of its Cattle rule is 6\" instead of 3\"."),
    # --- v0.10 armoury additions
    eqp("eq_dc_gravedampsprayer", "Grave-Damp Sprayer", "ranged", 8, R2,
        ["kw_flamethrower", "kw_gas", KWH("chokedamp")],
        "2-Handed, 8\", -1 INJURY DICE, FLAMETHROWER, GAS. A brass pump and a bladder of tomb air "
        "drawn off the deep vaults; it does not burn, it simply is not breathable. Choke-Damp: a "
        "Ranged Attack made with a Grave-Damp Sprayer may target a friendly model.",
        ctx={"injury_dice_mod": {"modifiers": [-1]}}),
    eqp("eq_dc_carlig", "Carlig", "melee", None, M1, [KWH("hookholds")],
        "1-Handed Melee. A flesh-hook on a short chain; it is not for killing. The Hook Holds: when "
        "an enemy model within 1\" of a model with a Carlig takes a Retreat ACTION, place 1 BLOOD "
        "MARKER next to that enemy model before any Melee Attacks allowed by the retreat are "
        "resolved."),
    eqp("eq_dc_gravesickle", "Grave-Sickle", "melee", None, M1, [KWH("laidatthethroat")],
        "1-Handed Melee. The sickle laid at a strigoi's throat before the lid goes down. Laid at the "
        "Throat: +1 INJURY DICE against a model that has 1 or more BLOOD MARKERS."),
    eqp("eq_dc_buzdugan", "Buzdugan", "melee", None, M1, ["kw_block"],
        "1-Handed Melee, BLOCK, +1 INJURY MODIFIER. The voivode's mace of office, unchanged since "
        "it was a symbol rather than a tool.",
        ctx={"injury_flat_mod": {"modifiers": [1]}}),
    eqp("eq_dc_graveiron", "Grave-Iron", "armour", None, [], [KWH("ninewinters")],
        "Mail buried nine winters and dug up rusted shut. Counts as Standard Armour. Nine Winters "
        "Buried: increases the wearer's REGENERATE by 1, to a maximum of REGENERATE (2). The "
        "wearer's Movement is reduced by 1\".",
        ctx={"upgrade_stat": {"upgrades": [{"stat": "armour", "value": -1}]},
             "injury_flat_mod": {"modifiers": [-1]}}),
    eqp("eq_dc_censerofgravesoil", "Censer of Grave-Soil", "equipment", None, [],
        [KWH("gravesmoke")],
        "Limit 2. Earth from nine graves burned with myrrh in a pierced brass ball; the dead find it "
        "comforting, the living cannot breathe it. Grave-Smoke: at the end of this model's "
        "Activation, place 1 BLOOD MARKER on 1 enemy model within 8\"."),
    eqp("eq_dc_yokeoftheherd", "Yoke of the Herd", "equipment", None, [],
        [KWH("chainedatshoulder")],
        "Leech only. A Bled chained at the shoulder, walking where it is walked. Chained at the "
        "Shoulder: at the start of each of the Leech's Activations, if a friendly Bled is within 2\", "
        "you may make an Injury Roll against that Bled. If you do, the Leech gains 1 Sated."),
    eqp("eq_dc_cullingknife", "Culling Knife", "melee", None, M1, ["kw_critical"],
        "Counts as a Misericordia.", ctx={"unremovable": []}),
    # --- glory items
    eqp("eq_dc_greybrothers", "The Grey Brothers", "equipment", None, [], ["kw_deployable"],
        "GLORY ITEM. Limit 1. Uses the Trench Dog rules in full - 25mm base, 8\"/Infantry, Melee +0 "
        "DICE, Armour 0 - including Four Paws, Pack Loyalty (it gains DRAGON COURT), Teeth and "
        "Claws, The Dogs of War, and Loyal Hound (+1 Glory for FIRETEAM). Not of the Herd: a vampire "
        "that takes a Feed ACTION against a Grey Brother must make an Injury Roll against it, as "
        "Offer the Vein. Special Training (+1 Glory) - Sentinel of the Tree Line: enemy models may "
        "not use INFILTRATOR to deploy within 12\" of the Grey Brother."),
    eqp("eq_dc_hailstonephial", "Hailstone Phial", "grenade", 8, R1,
        ["kw_assault", "kw_blast", "kw_scatter", "kw_consumable", KWH("hewnfrozenlake")],
        "GLORY ITEM. Consumable, Limit 2. 8\", ASSAULT, BLAST 3\", -1 INJURY DICE, IGNORE COVER, "
        "SCATTER. A finger of ice hewn from the frozen lake above the clouds, sealed in lead and "
        "wax; it does not melt. Hewn from the Frozen Lake: after the attack has been resolved, the "
        "area within 3\" of the target point is treated as Difficult terrain until the end of the "
        "following Turn. This affects all models, friend and foe.",
        ctx={"blast_mod": {"modifiers": [3]}, "injury_dice_mod": {"modifiers": [-1]},
             "ignore_mod": {"modifiers": ["cover"]}}),
    eqp("eq_dc_caskcart", "The Cask Cart", "equipment", None, [], [],
        "GLORY ITEM. Limit 1. A herd drunk dry yields one night's strength; a herd kept yields a "
        "cellar. The Tithe, Not the Slaughter: a Cask Cart is not allocated to a model; add it to "
        "your Arsenal. At the end of each game, for each friendly Bled that is on the battlefield "
        "and has 1 or more BLOOD MARKERS, your Warband gains 1 Vintage, to a maximum of 3 Vintage "
        "per game. See Campaign Play: The Long Hunger."),
    eqp("eq_dc_gravenail", "The Grave-Nail", "melee", None, M1, ["kw_armourpiercing"],
        "GLORY ITEM. 1-Handed Melee, ARMOUR PIERCING. Gravediggers hammer a square iron nail "
        "through the skull before the lid goes down, so that what is in the box stays in the box. "
        "Drawn out and set into a haft, it keeps the only trick it ever knew."),
    eqp("eq_dc_cupoftargoviste", "The Cup of Targoviste", "equipment", None, [],
        ["kw_deployable"],
        "GLORY ITEM. VAMPIRE only, Limit 1. Represented by a model or marker on a 25mm base. What is "
        "in it is not water. Set Out at the Fountain: after you deploy the model that has the Cup, "
        "you may also deploy the Cup anywhere on the battlefield more than 6\" from any enemy model; "
        "that model is then no longer carrying it, and the Cup cannot be moved, attacked or removed "
        "for the rest of the game. Drink ACTION: any model, friend or foe, within 1\" of the Cup may "
        "take a Drink ACTION, removing 1 BLOOD MARKER from it, or 2 BLOOD MARKERS if it is an enemy "
        "model; once per game per model. The Debt of Hospitality: if the model taking the Drink "
        "ACTION is an enemy model, the closest friendly model with the VAMPIRE keyword gains 1 "
        "Sated."),
    eqp("eq_dc_draconistcollar", "Draconist Collar", "equipment", None, [], [],
        "GLORY ITEM. ELITE only, Limit 3. The red cross that lay across their backs has been ground "
        "off with a file - not prised away, not lost, filed. The Oath Half-Kept: a model with a "
        "Draconist Collar may take a Feed ACTION against a model that has 1 or more BLESSING "
        "MARKERS, despite The Sanctified. If the Feed ACTION is a Success or Critical Success, "
        "remove 1 BLESSING MARKER from the target and place it next to the feeding model. Grace Does "
        "Not Keep: at the end of each Turn, remove all BLESSING MARKERS from models with the DRAGON "
        "COURT keyword."),
    eqp("eq_dc_forestoftheimpaled", "The Forest of the Impaled", "equipment", None, [], [],
        "GLORY ITEM. Limit 1. The Order learned in 1462 that an army can be turned without being "
        "fought. The Practice: not allocated to a model; add it to your Arsenal. After both sides "
        "have deployed, place 2 Impaled Markers anywhere on the battlefield more than 12\" from any "
        "enemy model. What the Sultan Saw: an enemy model within 3\" of an Impaled Marker must treat "
        "all of its Success Rolls as Risky Success Rolls. This does not apply to Morale Checks."),
    eqp("eq_dc_nightglasssight", "Nightglass Sight", "equipment", None, [], [],
        "GLORY ITEM. VAMPIRE only, Limit 2. Smoked crystal ground in the cellars of the "
        "Scholomance; the lens does nothing a mortal could measure, it simply stops the dark from "
        "being far away. Cold Sight: when this Glory Item is given to a model, choose 1 Ranged "
        "Weapon that the model has and which does not have the AUTOMATIC or BLAST keyword. That "
        "Weapon gains the IGNORE LONG RANGE keyword. A Nightglass Sight cannot be reallocated during "
        "the Quartermaster Step."),
    eqp("eq_dc_rookery", "The Rookery", "equipment", None, [], [],
        "GLORY ITEM. Limit 1. A wicker loft strapped to the baggage wagon; what lives in it is not "
        "tame and is not fed enough to leave. The Loft Is Never Empty: not allocated to a model; add "
        "it to your Arsenal. In each game you may deploy 1 Strix in addition to the models in your "
        "Warband. It does not count towards your Warband's model count, Threshold Value or Field "
        "Strength, and is not counted as part of your Warband for Morale Checks. If it is taken Out "
        "of Action, do not roll for its survival - it is replaced free of charge before your next "
        "game."),
    eqp("eq_dc_thirstingrounds", "Thirsting Rounds", "equipment", None, [], ["kw_ammunition"],
        "GLORY ITEM. VAMPIRE only, Limit 1. AMMUNITION. A chipped fang set in the mould and the lead "
        "poured around it; the tooth does the work wherever the ball lands. Drink at Distance: the "
        "first time in each Activation that a Ranged Attack made with the chosen Weapon wounds a "
        "model, the firing model gains 1 Sated. This does not happen if the target has 1 or more "
        "BLESSING MARKERS or has the ARTIFICIAL keyword."),
    eqp("eq_dc_vesperbell", "The Vesper Bell", "equipment", None, [], [],
        "GLORY ITEM. VAMPIRE only, Limit 1. Cast to call a congregation in at dusk; filed of its "
        "cross, it still does - the Order only changed which one. Ring for Evensong ACTION: take a "
        "Risky Success Roll and add +1 DICE. On a Failure nothing happens and the model's Activation "
        "ends. On a Success or Critical Success, choose 1 enemy model within 12\" in Line of Sight; "
        "for the rest of the game, attacks made against that model by friendly models have the "
        "IGNORE ARMOUR keyword. Once successfully used, it may not be used again in the same game."),
    eqp("eq_dc_buciumofthepass", "The Bucium of the Pass", "equipment", None, [], ["kw_held"],
        "GLORY ITEM. DOMINION only, Limit 1. HELD. Four feet of fir wound in cherry bark, made to "
        "call a flock down off the mountain before weather; it still does that, but the flock is "
        "different. Sound the Recall ACTION: take a Risky Success Roll and add +1 DICE. On a Failure "
        "nothing happens and the model's Activation ends. On a Success or Critical Success, until "
        "the end of the Turn, friendly Blood-Crazed models within 18\" of the bearer are not "
        "compelled to take a Charge ACTION and may take any ACTION."),
]


def perm_kw(kw):
    return {"faction_eq_restriction": {"permitted": [{"res_type": "keyword", "value": kw}]}}


def perm_md(mid):
    return {"faction_eq_restriction": {"permitted": [{"res_type": "id", "value": mid}]}}


NEW_FER = [
    ("eq_dc_carlig", "Carlig", 8, 0, 0, None),
    ("eq_dc_gravesickle", "Grave-Sickle", 10, 0, 0, None),
    ("eq_dc_buzdugan", "Buzdugan", 14, 0, 0, None),
    ("eq_dc_gravedampsprayer", "Grave-Damp Sprayer", 30, 0, 2, None),
    ("eq_dc_graveiron", "Grave-Iron", 35, 0, 0, None),
    ("eq_dc_censerofgravesoil", "Censer of Grave-Soil", 20, 0, 2, None),
    ("eq_dc_yokeoftheherd", "Yoke of the Herd", 20, 0, 0, perm_md("md_dragoncourt_leech")),
    ("eq_dc_cullingknife", "Culling Knife", 0, 0, 1, perm_md("md_dragoncourt_veinwife")),
    ("eq_dc_herdbell", "Herd-Bell", 10, 0, 1, None),
    ("eq_medikit", "Medi-kit", 10, 0, 0, None),
    ("eq_dc_greybrothers", "The Grey Brothers", 1, 1, 1, None),
    ("eq_dc_hailstonephial", "Hailstone Phial", 2, 1, 2, None),
    ("eq_dc_caskcart", "The Cask Cart", 3, 1, 1, None),
    ("eq_dc_gravenail", "The Grave-Nail", 3, 1, 2, None),
    ("eq_dc_cupoftargoviste", "The Cup of Targoviste", 4, 1, 1, perm_kw("kw_vampire")),
    ("eq_dc_nightglasssight", "Nightglass Sight", 4, 1, 2, perm_kw("kw_vampire")),
    ("eq_dc_rookery", "The Rookery", 4, 1, 1, None),
    ("eq_dc_draconistcollar", "Draconist Collar", 5, 1, 3, perm_kw("kw_elite")),
    ("eq_dc_thirstingrounds", "Thirsting Rounds", 5, 1, 1, perm_kw("kw_vampire")),
    ("eq_dc_vesperbell", "The Vesper Bell", 7, 1, 1, perm_kw("kw_vampire")),
    ("eq_dc_buciumofthepass", "The Bucium of the Pass", 8, 1, 1, perm_kw("kw_dominion")),
    ("eq_dc_forestoftheimpaled", "The Forest of the Impaled", 10, 1, 1, None),
]
NEW_FACTIONEQUIPREL = [
    {"id": f"rel_dragoncourt_fc_{eid}", "source": SRC, "tags": [], "name": nm,
     "contextdata": res if res else [], "faction_id": [FC], "equipment_id": eid,
     "cost": c, "costtype": ct, "limit": lim}
    for eid, nm, c, ct, lim, res in NEW_FER
]


def mer(rid, name, mid, items):
    return {"id": rid, "source": SRC, "tags": [], "name": name, "contextdata": [],
            "options": [], "model_id": [mid], "mandatory_equipment": items,
            "removable": False}


NEW_MODELEQUIPREL = [
    mer("rel_dragoncourt_md_eq_veinwife", "Vein-Wife Kit", "md_dragoncourt_veinwife",
        ["eq_standardarmour", "eq_gasmask", "eq_medikit", "eq_dc_cullingknife"]),
    mer("rel_dragoncourt_md_eq_calusar", "Calusar Kit", "md_dragoncourt_calusar",
        ["eq_trenchclub", "eq_swordaxe"]),
    mer("rel_dragoncourt_md_eq_solomonar", "Weather-Staff", "md_dragoncourt_solomonar",
        ["eq_trenchpolearm"]),
]

ADDITIONS = {
    "keyword": NEW_KEYWORDS,
    "factionrule": NEW_RULES,
    "ability": NEW_ABILITIES,
    "model": NEW_MODELS,
    "factionmodelrelationship": NEW_FACTIONMODELREL,
    "equipment": NEW_EQUIP,
    "factionequipmentrelationship": NEW_FACTIONEQUIPREL,
    "modelequipmentrelationship": NEW_MODELEQUIPREL,
}

# The only changes to existing entries, both agreed in the v0.10 session.
KNIT = ("Knit the Flesh (1 Sated): remove 2 BLOOD MARKERS from himself or a friendly vampire "
        "within 6\".")
KNIT_NEW = ("Knit the Flesh (X Sated): remove X BLOOD MARKERS, to a maximum of 2, from himself or "
            "a friendly vampire within 6\".")
LEECH_OLD = "The Leech may take Melee Weapons and Equipment from the Court Armoury."
LEECH_NEW = "The Leech may take any Battlekit from the Court Armoury."


def main():
    doc = json.load(open(BASE))
    blocks = {b["type"]: b for b in doc["files"]}
    report = []

    for btype, items in ADDITIONS.items():
        if btype not in blocks:
            blocks[btype] = {"type": btype, "data": []}
            doc["files"].append(blocks[btype])
            report.append(f"created block   {btype}")
        data = blocks[btype]["data"]
        # relationship blocks: also supersede any existing row pointing at the
        # same equipment/model, even if its id differs from ours
        subject = {"factionequipmentrelationship": "equipment_id",
                   "factionmodelrelationship": "model_id"}.get(btype)
        dropped = 0
        if subject:
            targets = {o.get(subject) for o in items}
            keep = [o for o in data
                    if not (o.get(subject) in targets
                            and o["id"] not in {x["id"] for x in items})]
            dropped = len(data) - len(keep)
            data[:] = keep
        index = {o["id"]: n for n, o in enumerate(data)}
        added = replaced = 0
        for obj in items:
            if obj["id"] in index:
                data[index[obj["id"]]] = obj
                replaced += 1
            else:
                data.append(obj)
                added += 1
        note = f", {dropped} superseded" if dropped else ""
        report.append(f"{btype:30} +{added} added, {replaced} replaced{note}, "
                      f"{len(data)} total")

    # wire the new rules into the faction
    fac = blocks["faction"]["data"][0]
    for rid in [r["id"] for r in NEW_RULES]:
        if rid not in fac["rules"]:
            fac["rules"].append(rid)
    report.append(f"faction rules -> {len(fac['rules'])}")

    # the two agreed edits to existing entries
    edits = 0
    for a in blocks["ability"]["data"]:
        for blk in a["description"]:
            if blk.get("content") == KNIT:
                blk["content"] = KNIT_NEW
                edits += 1
    for m in blocks["model"]["data"]:
        for blk in m.get("description", []):
            if blk.get("content") == LEECH_OLD:
                blk["content"] = LEECH_NEW
                edits += 1
    report.append(f"agreed edits applied: {edits} of 2")

    json.dump(doc, open(OUT, "w"), indent=2, ensure_ascii=False)
    print("base:", BASE)
    print("out: ", OUT)
    for line in report:
        print(" ", line)

    # validation
    ids = {}
    dupes = []
    for b in doc["files"]:
        for o in b["data"]:
            key = (b["type"], o["id"])
            if key in ids:
                dupes.append(key)
            ids[key] = True
    alleq = {o["id"] for o in blocks["equipment"]["data"]}
    allmd = {o["id"] for o in blocks["model"]["data"]}
    allab = {o["id"] for o in blocks["ability"]["data"]}
    allkw = {o["id"] for o in blocks["keyword"]["data"]}
    allrl = {o["id"] for o in blocks["factionrule"]["data"]}
    CORE_OK = {"eq_", "kw_", "md_"}
    errs = list({f"duplicate id {d}" for d in dupes})
    for m in blocks["model"]["data"]:
        errs += [f"{m['id']}: ability {a}" for a in m["abilities"] if a not in allab]
    for r in blocks["factionmodelrelationship"]["data"]:
        if r["model_id"] not in allmd:
            errs.append(f"FMR: model {r['model_id']}")
    for r in blocks["factionequipmentrelationship"]["data"]:
        if r["equipment_id"] not in alleq and not r["equipment_id"].startswith("eq_"):
            errs.append(f"FER: equipment {r['equipment_id']}")
    errs += [f"faction rule {x}" for x in fac["rules"] if x not in allrl]
    print("  validation:", errs or "clean")


if __name__ == "__main__":
    main()
