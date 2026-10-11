#!/usr/bin/env bash
# Run from your repo root (where life.py lives) after copying these files in.
# Creates one clear commit per file, then you can `git push`.
set -e
c() { git add "$1" && git commit -m "$2"; }
c .gitignore     "Add .gitignore for Python and generated HTML"
c LICENSE        "Add MIT license"
c test_life.py   "Add unit tests for rules, torus wrapping and patterns"
c rle.py         "Add RLE import/export for community pattern files"
c stats.py       "Add headless population sparkline"
c export_html.py "Add self-contained HTML animation export"
c Makefile       "Add Makefile shortcuts"
c README.md      "Add README documenting the project"
git log --oneline | head -8
