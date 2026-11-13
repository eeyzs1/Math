# Maintenance Checklist

See [CONTRIBUTING.md](CONTRIBUTING.md) for source ownership, complete commands and backup format.

## Content changes

- [ ] Update Chinese content in `tools/build_course.py` and English in `assets/course.en.json`.
- [ ] Update both `concepts*.json` files. Keep module/lesson/item identities aligned; append new items rather than reordering existing ones.
- [ ] Include hypotheses, prerequisites, worked examples, exercises and solutions. New modules also need L0-L4 routes and MSC mappings in both atlas builders.
- [ ] Edit shared browser logic in `tools/static/*.js` and localized messages in `tools/site_common.py`; regenerate `assets/*.js`.

## Verification

```sh
python tools/build_all.py
python -m unittest discover -s tests
python tools/verify_course.py
```

Install browser dependencies once with `python -m pip install -r requirements.txt` and `python -m playwright install chromium`. Use `python tools/verify_course.py --static-only` without Playwright. `verify_course_en.py` remains an English static-check entry point.

- [ ] Review source and generated diffs together after all checks pass.
- [ ] Inspect the homepage, changed lessons, labs and checklist, including backup transfer when relevant.
- [ ] A second rebuild must introduce no further changes. Commit as needed; CI checks rebuild consistency on Linux.

## Automated coverage

- Bilingual module structure, lesson fields, concept file order and stable IDs; visible lesson text matches source data.
- Local HTML paths, decoded URLs, fragment anchors, duplicate IDs, leaked placeholders and untranslated English artifacts.
- MSC CSV/TeX code sets and measured audit counts; search and hash navigation after filtering.
- Both editions' slider endpoints, probability normalization, sampling moments, shared density scales, true Newton geometry and eigen semiaxes.
- Progress persistence, cross-language backups, invalid-import preservation, malformed data and blocked storage.
- Actual print expansion and restoration after repeated events; all 364 pages at 320px without horizontal overflow.

## Source classification changes

- [ ] Preserve CSV latin1 and TeX UTF-8 encodings, check mappings, then rebuild.
- [ ] Counts are derived dynamically. Recheck README claims about official published counts if source data changes.
- [ ] Retain official TeX literals in descriptions. Classification inclusion does not mean a lesson exists for every research topic.
