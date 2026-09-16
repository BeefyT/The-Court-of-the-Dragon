# Workflow

How to change the Court of the Dragon rules now that the pipeline exists.

---

## The one thing to remember

**`data/CourtOfTheDragon-TrenchCompanion.json` is the source of truth.**

The codex markdown and all three PDFs are generated from it. Editing the codex
by hand does nothing useful — the next build overwrites it.

```
data/…json  ──gen_codex.py──▶  docs/…Codex.md  ──mkpdf.py──▶  dist/…Codex.pdf
     │
     └──▶ imported into Trench Companion
```

---

## Making a rules change

### 1. Edit the JSON

Small changes — a price, a range, a line of rules text — are fastest done by
hand. Find the entry by its `id` and edit it. The blocks you'll touch most:

| Block | Holds |
|---|---|
| `equipment` | weapon and gear profiles, their rules text |
| `factionequipmentrelationship` | what each item costs and its limit |
| `model` | stats, keywords, which abilities a model has |
| `factionmodelrelationship` | model costs, 0-1 limits, mercenary flag |
| `ability` | the named rules printed on a model's entry |
| `factionrule` | faction-wide special rules |
| `upgrade` + `modelupgraderelationship` | Orders and Elder Blood, and their costs |

For anything touching several entries at once — a new Glory Item needs an
`equipment` entry, a `factionequipmentrelationship`, and often a keyword — ask
Claude for a patch script instead. Hand-editing JSON in three places is where
mistakes happen. Patch scripts go in `tools/`, get committed, and are safe to
re-run (they match by `id` and replace rather than duplicate).

### 2. Build and verify

```powershell
.\build.ps1 codex     # regenerate docs/Court-of-the-Dragon-Codex.md
.\build.ps1 check     # verify the codex matches the JSON
```

`check` must print **"OK - codex matches the JSON"**. If it fails, don't commit
— fix it or paste the error to Claude. It catches:

- an item or model missing from the codex
- a cost in the codex that disagrees with the JSON
- a rule defined but not listed on the faction, so it never prints
- a model referencing an ability that doesn't exist

That third one is the reason `check` exists. Two rules — Blood-Crazed Behaviour
and Undead Fortitude — once went missing exactly that way.

### 3. Write the changelog

Add an entry to `docs/CHANGELOG.md` by hand. This is the one document that is
*not* generated, because the reasoning behind a change can't be derived from the
data. Record what changed, and why.

Bump the rules version in the JSON's top-level `description` when the change is
significant enough to matter at a table.

### 4. Commit and push

```powershell
git add -A
git commit -m "v0.11: <what changed>"
git push
```

CI then regenerates the codex, re-runs `check`, renders all three PDFs and
commits them back. Watch the Actions tab; a red X means `check` failed.

Because CI commits, your next push may need a `git pull` first.

### 5. Re-import into Trench Companion

The step outside the repo, and the easiest to forget. Import
`data/CourtOfTheDragon-TrenchCompanion.json`. Ids are stable and tied to
`homebrew_id 470028`, so it updates the faction in place rather than making a
second copy.

### 6. Tag it when you play

```powershell
git tag -a v0.11 -m "<short description>"
git push --tags
```

Then "which rules did we use in that game?" has an answer. Worth the ten
seconds — the inability to answer that question is what caused the drift this
pipeline was built to prevent.

---

## Commands

| Command | Does |
|---|---|
| `.\build.ps1` | codex + all PDFs |
| `.\build.ps1 codex` | JSON → codex markdown |
| `.\build.ps1 check` | verify codex matches JSON |
| `.\build.ps1 pdf` | markdown → PDFs (needs WeasyPrint + GTK) |
| `.\build.ps1 clean` | delete generated PDFs |

If PowerShell blocks the script after a fresh download:

```powershell
Get-ChildItem -Recurse | Unblock-File
Set-ExecutionPolicy -Scope Process Bypass
```

Or skip the script and call Python directly:

```powershell
python tools\gen_codex.py
python tools\check.py
```

**Local PDF rendering is optional.** WeasyPrint needs GTK on Windows and is
fiddly to install. CI renders the PDFs on every push, so `git pull` gets you
current ones. `codex` and `check` are pure Python and always work.

---

## Where each piece of the codex comes from

Almost all of it is generated. Two sections are prose constants inside
`tools/gen_codex.py`, because the Trench Companion schema can't express them:

- **THE DAMNED OF WALLACHIA** — the opening lore
- **THE BLOODLINES** — the Elder ladders. The app can hold the three Elder Blood
  purchases as upgrades, but not the three-rung skill ladders.

To change either, edit the `LORE` or `BLOODLINES` constant in `gen_codex.py`,
then rebuild. Everything else — armoury tables, Court Battlekit, all warband
entries, mercenaries, glory items, special rules, the campaign section — comes
from the JSON.

`WARBAND_CREATION` is also a constant there.

---

## Schema notes worth not relearning

Painfully earned, all of them:

- **Import envelope:** `{"id", "name", "author", "description", "files": [{"type", "data"}]}`.
  Valid types include `faction`, `keyword`, `factionrule`, `ability`, `model`,
  `upgrade`, `equipment`, and the four relationship types. Not the snapshot
  repo's directory layout — that's the app's internal data dump, a different
  thing.
- **Homebrew objects** use `"source": "homebrew"`, with `tags` and `contextdata`
  as `[]` when empty, and carry `"homebrew_id": 470028`.
- **Numeric keywords are bound through `contextdata`**, not keyword strings:
  `blast_mod`, `injury_dice_mod`, `cleave_mod`, `automatic_mod`, `plus_dice`,
  `injury_flat_mod`, `regenerate_mod`, `upgrade_stat`. Text-only rules become a
  custom `kw_hb470028_*` keyword plus the description.
- **Restrictions:** `contextdata.faction_eq_restriction.permitted`, with
  `res_type: "keyword"` (e.g. `kw_elite`, `kw_vampire`) or `res_type: "id"` for
  a single model.
- **Costs:** `costtype: 0` is ducats and `1` is glory on equipment relationships;
  the field is `cost_type` on model relationships. `warband_maximum: -1` is
  unlimited.
- **Everything is UTF-8.** The data uses 👑, ☼ and Romanian diacritics. The
  scripts open files with explicit `encoding="utf-8"` because Windows defaults
  to cp1252 and the JSON won't parse. Never use PowerShell's `>>` on these
  files — it writes UTF-16.

---

## If something looks wrong

| Symptom | Likely cause |
|---|---|
| `check` says an item is missing | equipment entry exists but has no `factionequipmentrelationship` |
| A rule doesn't print in the codex | defined in `factionrule` but not listed in the faction's `rules` array |
| Cost in the codex disagrees with the app | you edited the codex instead of the JSON |
| `UnicodeDecodeError: charmap` | a script is opening a file without `encoding="utf-8"` |
| Whole-file diff after every build | line endings; `.gitattributes` should pin LF |
| Glory item shows a ducat cost | `costtype` is 0 where it should be 1 |
