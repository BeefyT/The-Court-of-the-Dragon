PY ?= python3
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all codex pdf check clean

all: codex pdf

codex:
	$(PY) tools/gen_codex.py

pdf:
	$(PY) tools/mkpdf.py docs/Court-of-the-Dragon-Codex.md dist/Court-of-the-Dragon-Codex.pdf "Court of the Dragon"
	$(PY) tools/mkpdf.py docs/CHANGELOG.md dist/Court-of-the-Dragon-Changelog.pdf "Court of the Dragon — Changelog"
	$(PY) tools/mkpdf.py docs/Court-of-the-Dragon-Campaign.md dist/Court-of-the-Dragon-Campaign.pdf "Court of the Dragon — The Long Hunger"

check:
	$(PY) tools/check.py

clean:
	rm -f dist/*.pdf
