# The Court of the Dragon

An original homebrew faction for *Trench Crusade* by Well Done Minis. Apostate
vampire knights of 1573 Wallachia, anathema to Heaven and in arrears to Hell.

Free community content. Requires the Trench Crusade rulebook. Original IP by
Well Done Minis.

---

**New here, or coming back after a break? Read [WORKFLOW.md](WORKFLOW.md).**

## The one rule of this repo

**`data/CourtOfTheDragon-TrenchCompanion.json` is the source of truth.**

Everything in `docs/` and `dist/` is generated from it. Never hand-edit the
codex — edit the JSON and regenerate. This repo exists because the codex and the
app data once drifted four releases apart, and nobody noticed until a design
session accidentally reinvented a weapon that already existed.

If a rules change needs making:

1. Edit `data/CourtOfTheDragon-TrenchCompanion.json`.
2. Run `make` to regenerate the codex and PDFs.
3. Add a changelog entry in `docs/CHANGELOG.md`.
4. Commit. Re-import the JSON into Trench Companion.

## Layout

```
data/
  CourtOfTheDragon-TrenchCompanion.json   source of truth; the app import file
  core-keywords.json                      id -> display-name map for core keywords
tools/
  gen_codex.py    JSON -> docs/Court-of-the-Dragon-Codex.md
  patch_court.py  additive merge of new content into the JSON
  mkpdf.py        markdown -> PDF (WeasyPrint)
docs/
  Court-of-the-Dragon-Codex.md    GENERATED - do not hand-edit
  CHANGELOG.md                    hand-written
  Court-of-the-Dragon-Campaign.md The Long Hunger, with design commentary
  archive/                        superseded docs, kept for their reasoning
dist/
  *.pdf                           GENERATED
```

## Setup

Python 3.10+.

```sh
pip install -r requirements.txt
```

WeasyPrint needs system libraries. On macOS: `brew install pango gdk-pixbuf
libffi`. On Debian/Ubuntu: `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`.

## Build

```sh
make          # regenerate the codex, then all three PDFs
make codex    # JSON -> docs/Court-of-the-Dragon-Codex.md
make pdf      # markdown -> dist/*.pdf
make check    # verify every JSON entity and cost appears in the codex
make clean    # remove generated PDFs
```

## What lives only in the generator

Two sections of the codex have no representation in the Trench Companion
schema, so they are held as prose constants inside `tools/gen_codex.py`:

- the opening lore (**THE DAMNED OF WALLACHIA**)
- **THE BLOODLINES** — the Elder ladders. The app can express the three Elder
  Blood purchases as upgrades, but not the three-rung skill ladders.

Everything else — armoury tables, Court Battlekit, all warband entries,
mercenaries, glory items, special rules, the campaign section — is derived from
the JSON.

## A note for contributors

Every file in this repo is UTF-8 — the data uses 👑, ☼ and Romanian
diacritics throughout. The scripts open files with an explicit
`encoding="utf-8"` because Windows otherwise defaults to cp1252 and the JSON
fails to parse. Keep that explicit in anything new, and avoid PowerShell's `>>`
redirection on these files (it writes UTF-16).

## CI

`.github/workflows/build.yml` regenerates the codex, runs the drift check and
renders the PDFs on every push that touches `data/`, `docs/` or `tools/`, then
commits the results back. WeasyPrint's system libraries install cleanly on
Linux, so PDFs are built there rather than on a Windows desktop. You can also
trigger it by hand from the Actions tab.

This means local PDF rendering is optional: edit the JSON, commit, push, and the
PDFs update themselves.

## Versioning

The rules version lives in the JSON's top-level `description`. Bump it there and
it flows into the app; note the change in `docs/CHANGELOG.md`.

## Trench Companion

The JSON is a homebrew import bundle: `{"files": [{"type": ..., "data": [...]}]}`,
tied to `homebrew_id 470028`. Re-importing updates the faction in place because
the ids are stable. Two schema notes worth remembering:

- Valued keywords are bound through `contextdata`, not keyword strings:
  `blast_mod`, `injury_dice_mod`, `cleave_mod`, `automatic_mod`, `plus_dice`,
  `injury_flat_mod`, `regenerate_mod`, `upgrade_stat`.
- Equipment restrictions use `faction_eq_restriction.permitted` with
  `res_type: "keyword"` or `res_type: "id"`.

## Status

Rules v0.11. Four physical playtests behind it. The Long Hunger
campaign layer is v0.5 and provisional — all its rates are dials.

Open: the Vătaf (undecided, pending playtest), the Eclipse-Tooth glory item
(tabled), and a defensive-gear pass — Coffin-Lid Pavise, Grave-Soil Plate and
Grave-Iron overlap at 12/20/35 ducats.
