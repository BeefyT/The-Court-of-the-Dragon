# Setting this up locally

> **Windows:** use `.\build.ps1` wherever this guide says `make`
> (`.\build.ps1 check` for `make check`). PowerShell may need
> `Set-ExecutionPolicy -Scope Process RemoteSigned` once per session. Also avoid
> `>>` to append to files in PowerShell 5.1 — it writes UTF-16 and will corrupt
> the UTF-8 markdown.

## 1. Put it somewhere permanent

```sh
mkdir -p ~/projects
cd ~/projects
# unzip the archive here, so you end up with ~/projects/court-of-the-dragon
unzip ~/Downloads/court-of-the-dragon.zip
cd court-of-the-dragon
```

## 2. Start the repo

```sh
git init
git add .
git commit -m "Court of the Dragon v0.10 - JSON as source of truth, generated codex"
```

## 3. Push it to GitHub

Create an empty repo on GitHub (no README, no .gitignore - this already has
both), then:

```sh
git remote add origin git@github.com:<you>/court-of-the-dragon.git
git branch -M main
git push -u origin main
```

If you make it public, I can read it directly in future sessions from
`raw.githubusercontent.com` - no uploading required. Private also works, you
just attach the JSON when we need it.

## 4. Install the build dependencies

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

WeasyPrint needs system libraries:

- macOS: `brew install pango gdk-pixbuf libffi`
- Debian/Ubuntu: `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`
- Windows: install the GTK3 runtime
  (github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer), then
  reopen your terminal. If WeasyPrint still fails to import, the codex and
  changelog markdown are unaffected — only PDF rendering needs it.

## 5. Prove the pipeline works

```sh
make check   # should print "OK - codex matches the JSON"
make         # regenerates the codex and all three PDFs
git diff     # should be empty, or show only intentional changes
```

If `make` produces a diff on a clean checkout, something is off - tell me and
I'll look at it.

## The workflow from here

1. Edit `data/CourtOfTheDragon-TrenchCompanion.json`.
2. `make && make check`
3. Write the changelog entry in `docs/CHANGELOG.md`.
4. `git commit`
5. Import the JSON into Trench Companion.

Never hand-edit `docs/Court-of-the-Dragon-Codex.md` - it gets overwritten.

## One habit worth keeping

Tag a release when you play with it:

```sh
git tag -a v0.10 -m "Glory Items, armoury expansion, codex reconciliation"
git push --tags
```

Then "which rules did we use in that game?" has an answer.
