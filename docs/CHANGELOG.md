# THE COURT OF THE DRAGON
### Changelog

*Version history prior to v0.10 was not preserved as a document. The v0.6–v0.8.1 rules changes survive in the Trench Companion JSON, which is now the authoritative artifact.*

---

## v0.10 — Glory Items, the Armoury Expansion & Reconciliation

### Fixed — the codex was four releases stale

The codex markdown was discovered to predate v0.6, having been rebuilt at some point from an older source. It was missing the entire v0.8 "Arms of the Old Country" armoury expansion and the v0.7 Bloodlines rewrite, and it contradicted the app on roughly ten data points — the Sanguine Reaver nerf, both Leash reductions, the Shrike's claws, Leech stats, Bled and Strix costs, and the Impaler's Stake price.

- **The codex is now generated from the JSON** by `gen_codex.py`. Armoury tables, Court Battlekit, all Warband Entries, Mercenaries, Glory Items, Special Rules and the campaign section are derived from the data, so the two artifacts cannot drift again. Only the opening lore and the Bloodlines ladders — neither of which the app schema can represent — are held as prose in the generator.
- Restored to the codex: the v0.8 armoury (Wheellock Culverin, The Arcan, Organ Gun, Bombard, Widow's Knives, Grave-Iron Halberd, Coffin-Lid Pavise, Grave-Soil Plate, Shroud of the Bled, A Copy of the Usages, Pouch of Grave-Earth) and the full v0.7 Bloodlines system — per-model pledge, one-pick Elder Blood, three three-rung ladders climbed bottom-up, choose-don't-roll advancement, and Limited Potential on the Shrike and the Leech.

### Added — Glory Items

Twelve entries in one open table, not gated by Elder. The pledge is the faction's customization axis; the ☼ table covers what bloodlines cannot reach — ranged, armour bypass, objective play, body count, and the campaign layer.

| Item | Stipulation | Cost |
|---|---|---|
| The Grey Brothers | Limit 1 | 1☼ |
| Hailstone Phial | Consumable, Limit 2 | 2☼ |
| The Cask Cart | Limit 1 | 3☼ |
| The Grave-Nail | Limit 2 | 3☼ |
| The Cup of Târgoviște | VAMPIRE only, Limit 1 | 4☼ |
| Nightglass Sight | VAMPIRE only, Limit 2 | 4☼ |
| The Rookery | Limit 1 | 4☼ |
| Draconist Collar | ELITE only, Limit 3 | 5☼ |
| Thirsting Rounds | VAMPIRE only, Limit 1 | 5☼ |
| The Vesper Bell | VAMPIRE only, Limit 1 | 7☼ |
| The Bucium of the Pass | DOMINION only, Limit 1 | 8☼ |
| The Forest of the Impaled | Limit 1 | 10☼ |

A Court Warband may also buy Glory Items available to any Warband, excepting the **Trench Dog** (replaced by The Grey Brothers) and the **Sniper Scope** (replaced by Nightglass Sight).

### Added — Armoury

| Item | Notes | Cost |
|---|---|---|
| Cârlig | 1-Handed Melee | 8👑 |
| Grave-Sickle | 1-Handed Melee | 10👑 |
| Herd-Bell | Reworked: *Driven Together* (was a Musical Instrument at 5👑) | 10👑 |
| Buzdugan | 1-Handed Melee, BLOCK, +1 INJURY MODIFIER | 14👑 |
| Censer of Grave-Soil | Equipment, Limit 2 | 20👑 |
| Yoke of the Herd | Equipment, Leech only | 20👑 |
| Grave-Damp Sprayer | 2-Handed, 8", FLAMETHROWER, GAS | 30👑 |
| Grave-Iron | Armour | 35👑 |

Three build axes now exist that did not before: blood-marker synergy (Censer → Cârlig → Grave-Sickle, feeding the Witch's spell costs), a REGENERATE axis (Grave-Iron), and a herd engine (Yoke + Herd-Bell + Sprayer, pulling against the Cask Cart's Vintage income).

### Added — Mercenaries

The Vein-Wife (3☼), the Călușar (5☼), the Solomonar (6☼) and the Priculici (6☼), governed by **Neither Shepherd Nor Wolf**: the Court is neither Faithful nor Fallen and may not hire the standard mercenaries. Each is 0-1.

### Added — Campaign Play

**The Long Hunger** (v0.5, provisional) replaces the Trauma Step. ELITE vampires never gain Battle Scars and instead accumulate permanent **Thirst Markers** — Fraying at 1, Slipping at 2, Lost at 3. Shrikes and Leeches enter **Torpor** rather than dying. **Vintage** (10👑 = 1, converted from Loot) quenches Thirst at 10 per marker, once per Campaign Phase. Full design commentary in `Court-of-the-Dragon-Campaign.md`.

### Fixed — two rules that existed only in prose

Both were in the old codex but had no representation in the app data, so the first generated codex dropped them. Now stated as faction rules in the JSON, which means they appear in both artifacts:

- **Blood-Crazed Behaviour** — a Blood-Crazed model may take no ACTION other than Move, Dash, Charge or Fight, and must Charge if able; The Leash determines which model. The Bucium of the Pass lifts this restriction, so it needed to exist as a rule for the Glory Item to mean anything.
- **Undead Fortitude** — a VAMPIRE relies on REGENERATE rather than medical treatment: no Medi-kit, no Treat ACTION. This matters more now that Medi-kit is in the armoury at 10👑 for the Vein-Wife's kit.

### Changed

- **Knit the Flesh** is now *X Sated: remove X BLOOD MARKERS, to a maximum of 2*, from 1 Sated for 2 markers. Playtest feedback was that regeneration plus blood-marker removal was too forgiving. Ascended sits at 3+ Sated, so a full heal usually drops the Voivode out of Ascended — the brake runs through the state ladder rather than a flat cap.
- **The Leech** may now take any Battlekit from the Court Armoury (was Melee Weapons and Equipment only).
- **CLEAVE values do not stack** — a model whose weapon would gain CLEAVE from more than one source uses the highest value. Without this, a Butcher Boyar carrying a Draconist Sabre read as CLEAVE 4, since both grant CLEAVE 2 on the same Ascended trigger.
- **Grave-Damp Sprayer** carries no IGNORE ARMOUR, unlike the official Flamethrower it is priced against. The Court pays for armour bypass through the Grave-Nail and the Vesper Bell; the Sprayer trades that keyword for GAS and the friendly-targeting clause.

### Cut or tabled

- **The Poterăș** (mortal bounty-hunter marksman) — cut, preserving the all-vampire ELITE identity. Whether the Court needs a dedicated ranged unit is now a playtest question.
- **The Vătaf** (herd overseer) — undecided, pending playtest.
- **The Tăblia** — cut on discovery that the Coffin-Lid Pavise already occupied the same slot.
- **Scholomance Seal** — cut. Would have let a vampire hold gifts from a second Elder outside its pledge.
- **Pens of the Bled** — superseded by the Cask Cart, which pays in Vintage and rewards drinking from the herd without killing it.
- **Vârcolac's Tooth** (weather version) — cut. Duplicated the Solomonar's *Rain-Book*.
- **The Eclipse-Tooth** (warband-wide Sated burst) — tabled. The eclipse concept is worth keeping; handing out Sated is not the mechanic for it.

### Considered and rejected

Recorded so they are not rediscovered: a **DOMINION-relay Strix** (a flying Leash would gut the faction's central tension), and **Seasoned Stakes** on the Forest of the Impaled (an unbreakable Impaler's Stake deletes the kill-or-keep decision the weapon is built on).

### Watch list

1. **Thirsting Rounds** — free Sated at no risk from across the table is a genuine change to an economy built on 1" Risky actions.
2. **Draconist Collar at Limit 3** — three collared lords convert the Faithful matchup from worst to best. Drop the Limit to 2 before touching the cost.
3. **The Forest of the Impaled** stacked with a Negru Vodă lord holding *The Throne of Thorns* — not unbalanced, potentially miserable to play against. Restrict the aura to the two pre-planted markers if so.
4. **Grave-Iron on a Shrike** — 105👑 for a REGENERATE (2), always-Blood-Crazed INFILTRATOR that enters from any board edge. The −1" movement barely touches something that charges every Turn.
5. **Censer of Grave-Soil** — a guaranteed BLOOD MARKER every Activation with no roll. If it becomes an auto-include across the roster, cut the Limit to 1.
6. **Coffin-Lid Pavise vs Grave-Iron vs Grave-Soil Plate** — three overlapping defensive options at 12/35/20👑. Grave-Soil Plate is arguably the best value of the three.

### Tooling

- `patch_court.py` — additive merge of v0.10 content into the app JSON. Matches by id, supersedes stale relationship rows, and leaves everything else byte-identical.
- `gen_codex.py` — generates the codex from the JSON.
- `mkpdf.py` — WeasyPrint renderer, rebuilt this session.
- **The JSON is the source of truth.** It is the only artifact carrying v0.6–v0.8.1 and must be kept outside the container.
