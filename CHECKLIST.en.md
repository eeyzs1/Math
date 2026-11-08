# Maintenance Checklist

Half of this repository is generated artifacts and half is hand-maintained documentation. Know which is which before you start.

## Quick Reference for File Ownership

| Category | Files | How to change |
|---|---|---|
| Generators | `tools/build_course.py`, `tools/extend_atlas.py` | Edit directly, then rebuild |
| Generated pages | `index.html`, `NN-*/` (incl. lessons, curriculum), `reference/*.html`, `README.md`, `assets/style.css`, `assets/widgets.js`, `assets/course.json`, `assets/sources.json`, `assets/classification-audit.json` | **Do not hand-edit**; change the generators and rebuild |
| Hand-maintained | `MISSION.md`, `NOTES.md`, `RESOURCES.md`, `learning-records/`, `CHECKLIST.md`, `assets/concepts.json` (core-concept checklist data) | Edit directly; rebuilding will not overwrite |
| English-edition generators | `tools/build_course_en.py`, `tools/extend_atlas_en.py` (page templates; data comes from `assets/course.en.json`) | Edit templates directly, then rebuild via the English routine below |
| English-edition generated pages | `*.en.html` in every directory (index/curriculum/lessons), `reference/*.en.html`, `assets/widgets.en.js` | **Do not hand-edit**; change the generators or the data, then rebuild |
| English-edition hand-maintained | `README.en.md`, `MISSION.en.md`, `NOTES.en.md`, `RESOURCES.en.md`, `CHECKLIST.en.md`, `REVIEW.en.md`, `learning-records/README.en.md`, `assets/course.en.json`, `assets/concepts.en.json` | Edit directly; the terminology standard is `tools/en-src/GLOSSARY.md` |
| Source data | `assets/msc2020.csv` (latin1), `assets/msc2020.tex` (UTF-8) | Replace with the official downloads, keeping the original encodings |
| Verification | `tools/verify_course.py`, `tools/verify_course_en.py`, `requirements.txt` | Edit directly |

## Fixed Routine After Every Change

- [ ] `python tools/build_course.py`
- [ ] `python tools/extend_atlas.py` (the order matters: build rewrites the pages, extend appends classification and staged routes)
- [ ] `python tools/verify_course.py` all green (first time: `pip install -r requirements.txt`)
- [ ] Browser spot-check: `index.html` home page, any lesson page, drag sliders in `reference/labs.html`, search in `reference/classification.html`
- [ ] `git add -A && git commit && git push`

## English Edition (*.en.html / *.en.md): Rebuild and Sync

- [ ] After changing Chinese course content (`tools/build_course.py` data or `assets/concepts.json`), mirror the change in the corresponding entries of `assets/course.en.json` / `assets/concepts.en.json`, then rebuild the English edition
- [ ] `python tools/build_course_en.py` (reads `assets/course.en.json` and `RESOURCES.en.md`; generates all `*.en.html` pages and `assets/widgets.en.js`)
- [ ] `python tools/extend_atlas_en.py` (generates the English staged-curriculum, classification, and concept-checklist pages; it never touches the Chinese pages)
- [ ] `python tools/verify_course_en.py` all green (lesson counts match the Chinese edition, internal links exist, no leftover Chinese characters in English files)
- [ ] Browser spot-check: `index.en.html`, any `.en.html` lesson page, `reference/labs.en.html`
- [ ] Terminology follows `tools/en-src/GLOSSARY.md`; the English and Chinese data files correspond field by field — changing one requires syncing the other

## Adding a Lesson

- [ ] Append `(title, intuition-and-definition, worked derivation, exercise, solution)` to the data tuple of the right module in `tools/build_course.py`
- [ ] Append the lesson's concept entry to `assets/concepts.json` (3–4 items, in the "can explain / can derive / can transfer" rubric; `extend_atlas.py` asserts that entry counts match lesson counts)
- [ ] Mirror both changes in `assets/course.en.json` and `assets/concepts.en.json` for the English edition
- [ ] No count or navigation changes needed: previous/next links, the "N lessons" copy, and the module/lesson counts on the home page and README are all generated dynamically
- [ ] Run the full routine: rebuild + verify + commit (Chinese and English)

## Adding a Module

- [ ] Add a tuple to `data` in `build_course.py`: `(folder, title, subfields separated by ;, prerequisites, textbook key, lesson list)`
- [ ] The textbook key must exist in the `sources` dict (currently: discrete/pre/linear/calculus/statistics/ode/topology); adding a source also requires updating `RESOURCES.md` (hand-maintained)
- [ ] Folder names use the `NN-slug` format (two-digit prefix)
- [ ] If the module corresponds to MSC research classes: update the `groups` mapping; `cn` is a "code → Chinese name" dict asserted against the CSV's class set — a mismatch fails loudly
- [ ] Add the module's 5-stage route (L0–L4) to `paths` in `tools/extend_atlas.py`, and mirror the module in `assets/course.en.json` plus the English templates
- [ ] Check whether the README's "Recommended Study Paths" should attach the new module to a route (that section lives in the build template, not in hand-written copy)
- [ ] Full routine: rebuild + verify + commit

## Updating the MSC2020 Source Data

- [ ] Replace `assets/msc2020.csv` and `assets/msc2020.tex`
- [ ] `build_course.py` asserts that the `cn` dict matches the CSV's 63 major classes; `extend_atlas.py` asserts that the CSV codes match the TeX label set — if either fails, reconcile the data before touching the mappings
- [ ] `assets/classification-audit.json` and the README counts recompute automatically; if the totals change, update the assertions in `tools/verify_course.py` (`.major==63`, `.entry==6006`, etc.) accordingly
- [ ] Re-check whether the README's "counting note" (official claims 63/529/6,022 vs. measured counts) still holds

## What verify_course.py Covers Automatically

- All local link targets on the site exist (rglob over every HTML file's href/src)
- The seven lab sliders' endpoint values (h=0.01, a=0/−2, p=0/1, step=1.2, n=1/50, x0=0/±2.5, ea/eb/ed endpoints) produce NaN-free output
- Answer `<details>` can be expanded; no horizontal overflow at a 390px viewport
- classification: major/entry counts dynamically checked against `assets/classification-audit.json`, exact-code search, no-results, clear-to-restore, hash deep links
- Every module's curriculum page has exactly 5 stages; page JS has no uncaught errors
- The concepts checklist's module and item counts are dynamically checked against `assets/concepts.json`
- Writes 3 QA screenshots to `assets/` (gitignored; do not commit)

`tools/verify_course_en.py` performs the English-edition counterparts that do not need a browser: JSON validity, per-module lesson counts against the Chinese data, internal link targets, and a scan for leftover Chinese/full-width characters in all `*.en.html`, `*.en.json`, and `*.en.md` files.

## Known Leftovers (Low Priority, Handle as Needed)

- [ ] A few classification entries retain TeX literals (e.g. `\{For ...\}`); they come from the official source data and stay as-is

Older leftovers already resolved: the site has `<meta name="description">` everywhere; branch-page bibliography links point to the generated `reference/resources.html` (the source remains the hand-maintained `RESOURCES.md`); the labs binomial chart gained a baseline axis; `widgets.js` loads only on the labs page (the print-expand logic is inlined into every page template); the companion lab for the 04 eigenvalue lesson (circle to ellipse) is live.
