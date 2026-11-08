"""Verify the English edition: structure, links, and translation hygiene.

Checks (no browser needed):
  1. assets/course.en.json and assets/concepts.en.json are valid JSON whose module
     sets and per-module lesson/entry counts match the Chinese data exactly.
  2. Every generated *.en.html exists for every module (index, curriculum, all lessons)
     plus the root and reference pages.
  3. All internal href/src targets in *.en.html resolve to existing files.
  4. No leftover CJK or full-width characters in any *.en.html, *.en.json, or *.en.md.
  5. Lesson pages carry the five expected section headings and a fold-out solution.
Exit code 0 = all green.
"""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
CJK = re.compile(r'[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]')
HREF = re.compile(r'(?:href|src)="([^"#]+)"')
problems = []

zh_course = json.loads((root / 'assets/course.json').read_text(encoding='utf-8'))
en_course = json.loads((root / 'assets/course.en.json').read_text(encoding='utf-8'))
zh_concepts = json.loads((root / 'assets/concepts.json').read_text(encoding='utf-8'))
en_concepts = json.loads((root / 'assets/concepts.en.json').read_text(encoding='utf-8'))

if [m[0] for m in zh_course] != [m[0] for m in en_course]:
    problems.append('course.en.json module order/set differs from course.json')
for mz, me in zip(zh_course, en_course):
    if len(mz[5]) != len(me[5]):
        problems.append(f'{mz[0]}: lesson count {len(me[5])} != Chinese {len(mz[5])}')
    for i, les in enumerate(me[5]):
        if len(les) != 5 or not all(isinstance(x, str) and x.strip() for x in les):
            problems.append(f'{mz[0]} lesson {i+1}: malformed fields')
if set(zh_concepts) != set(en_concepts):
    problems.append('concepts.en.json module set differs from concepts.json')
for k in zh_concepts:
    if len(zh_concepts[k]) != len(en_concepts.get(k, [])):
        problems.append(f'{k}: concept entry count differs')
    for ez, ee in zip(zh_concepts[k], en_concepts.get(k, [])):
        if len(ez['items']) != len(ee['items']):
            problems.append(f'{k}/{ez["file"]}: concept item count differs')

# ---- expected English pages exist
expected = {root / 'index.en.html'}
for folder, title, subs, pre, source, lessons in en_course:
    expected |= {root / folder / 'index.en.html', root / folder / 'curriculum.en.html'}
    expected |= {root / folder / 'lessons' / f'{i:02}.en.html' for i in range(1, len(lessons) + 1)}
expected |= {root / f'reference/{n}.en.html' for n in
             ('glossary', 'labs', 'resources', 'classification', 'curriculum', 'concepts')}
expected |= {root / 'assets/widgets.en.js'}
for p in sorted(expected):
    if not p.exists():
        problems.append(f'missing generated file: {p.relative_to(root)}')

# ---- links resolve + CJK hygiene over all English artifacts
# The one allowed Chinese string is the deliberate language-switch endonym "中文".
LANG_LINK = re.compile(r'<a href="[^"]*">中文</a>')
pages = [p for p in root.rglob('*.en.html')]
for p in pages:
    text = p.read_text(encoding='utf-8')
    hits = sorted(set(CJK.findall(LANG_LINK.sub('', text))))
    if hits:
        problems.append(f'{p.relative_to(root)}: CJK/fullwidth remnants {hits}')
    for target in HREF.findall(text):
        if target.startswith(('http://', 'https://', 'mailto:', 'data:')):
            continue
        dest = (p.parent / target.split('#')[0]).resolve()
        if not dest.exists():
            problems.append(f'{p.relative_to(root)}: broken link {target}')
    if p.name.endswith('lessons' + '\\' + '') or '\\lessons\\' in str(p):
        for heading in ('Intuition First, Then Symbols', 'A Derivation, Step by Step',
                        'Pause and Try It', 'Closed-Book Recall', 'Further Reading'):
            if heading not in text:
                problems.append(f'{p.relative_to(root)}: missing section "{heading}"')
        if '<details><summary>Show the solution' not in text:
            problems.append(f'{p.relative_to(root)}: missing fold-out solution')

for p in [root / 'assets/course.en.json', root / 'assets/concepts.en.json',
          root / 'assets/widgets.en.js']:
    hits = sorted(set(CJK.findall(p.read_text(encoding='utf-8'))))
    if hits:
        problems.append(f'{p.relative_to(root)}: CJK/fullwidth remnants {hits}')
for p in list(root.glob('*.en.md')) + list((root / 'learning-records').glob('*.en.md')):
    hits = sorted(set(CJK.findall(p.read_text(encoding='utf-8'))))
    if hits:
        problems.append(f'{p.relative_to(root)}: CJK/fullwidth remnants {hits}')

# ---- labs widgets: every slider/svg/output id on the labs page must be wired in widgets.en.js
lab = (root / 'reference/labs.en.html').read_text(encoding='utf-8')
js = (root / 'assets/widgets.en.js').read_text(encoding='utf-8')
for i in re.findall(r'id="([\w-]+)"', lab):
    if (i.endswith(('-svg', '-out')) or i in ('h', 'a', 'p', 'step', 'n', 'x0', 'ea', 'eb', 'ed')) \
            and f"'{i}'" not in js:
        problems.append(f'labs widget id {i} not wired in assets/widgets.en.js')

n_lessons = sum(len(m[5]) for m in en_course)
print(f'English edition: {len(en_course)} modules, {n_lessons} lessons, '
      f'{len(pages)} generated pages checked.')
if problems:
    print(f'{len(problems)} problem(s) found:')
    for x in problems:
        print(' -', x)
    sys.exit(1)
print('verify_course_en: all green.')
