"""Dependency-free checks shared by both editions on Windows and Unix."""
from html.parser import HTMLParser
import csv
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from site_common import inline

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r'[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]')
TAGS = set('html head meta title link body main nav a header p h1 h2 h3 h4 section div span ol ul li article footer details summary label input textarea button output svg script b i em strong code br sub sup noscript'.split())


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.unknown, self.paragraphs, self.text = [], [], [], [], []
        self._paragraph = None
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag not in TAGS:
            self.unknown.append(self.get_starttag_text())
        for key, value in attrs:
            if key == 'id':
                self.ids.append(value)
            elif key in ('href', 'src') and value:
                self.links.append(value)
        if tag == 'p':
            self._paragraph = []

    def handle_endtag(self, tag):
        if tag == 'p' and self._paragraph is not None:
            self.paragraphs.append(''.join(self._paragraph))
            self._paragraph = None

    def handle_data(self, data):
        self.text.append(data)
        if self._paragraph is not None:
            self._paragraph.append(data)


def load(name):
    return json.loads((ROOT / 'assets' / name).read_text(encoding='utf-8'))


def verify_static(language=None):
    """Return actionable failures. language=None checks both editions."""
    problems = []

    def check(condition, message):
        if not condition:
            problems.append(message)

    course, english = load('course.json'), load('course.en.json')
    concepts, en_concepts = load('concepts.json'), load('concepts.en.json')
    sources = load('sources.json')
    for label, modules, checklist in [('zh', course, concepts), ('en', english, en_concepts)]:
        folders = [m[0] for m in modules]
        check(len(folders) == len(set(folders)), f'{label}: duplicate module folders')
        check(set(folders) == set(checklist), f'{label}: concept module set differs')
        for module in modules:
            folder = module[0]
            valid = (len(module) == 6 and all(isinstance(x, str) and x.strip() for x in module[:5])
                     and isinstance(module[5], list) and bool(module[5]))
            check(valid, f'{label}/{folder}: malformed module')
            if not valid:
                continue
            check(bool(re.fullmatch(r'\d{2}-[a-z-]+', folder)), f'{label}: invalid folder {folder}')
            check(module[4] in sources, f'{label}/{folder}: unknown source key')
            entries = checklist.get(folder, [])
            check(len(entries) == len(module[5]), f'{label}/{folder}: concept lesson count differs')
            for n, lesson in enumerate(module[5], 1):
                check(isinstance(lesson, list) and len(lesson) == 5
                      and all(isinstance(x, str) and x.strip() for x in lesson),
                      f'{label}/{folder}/{n:02}: expected five nonempty text fields')
            for n, entry in enumerate(entries, 1):
                check(entry.get('file') == f'{n:02}', f'{label}/{folder}: wrong concept file/order at {n}')
                items = entry.get('items')
                check(isinstance(items, list) and bool(items)
                      and all(isinstance(x, str) and x.strip() for x in items),
                      f'{label}/{folder}/{n:02}: malformed concept items')
    check([m[0] for m in course] == [m[0] for m in english], 'English module order differs')
    for zh, en in zip(course, english):
        check(zh[4] == en[4], f'{zh[0]}: translated source key differs')
        check(len(zh[5]) == len(en[5]), f'{zh[0]}: translated lesson count differs')
        for z, e in zip(concepts.get(zh[0], []), en_concepts.get(en[0], [])):
            check(z['file'] == e['file'] and len(z['items']) == len(e['items']),
                  f'{zh[0]}/{z["file"]}: translated checkbox IDs differ')

    documents = {}
    for path in ROOT.rglob('*.html'):
        source = path.read_text(encoding='utf-8')
        doc = documents[path.resolve()] = Document(source)
        check(len(doc.ids) == len(set(doc.ids)), f'{path.relative_to(ROOT)}: duplicate IDs')
        check(not doc.unknown, f'{path.relative_to(ROOT)}: unexpected HTML {doc.unknown[:2]}')
        check('<meta name="description"' in source, f'{path.relative_to(ROOT)}: missing description')
        check('{printjs}' not in source and 'beforeprint' in source,
              f'{path.relative_to(ROOT)}: print script missing or template placeholder leaked')
    for path, doc in documents.items():
        for link in doc.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            prefix = f'{path.relative_to(ROOT)}: {link}'
            if not target.is_relative_to(ROOT):
                problems.append(prefix + ' escapes repository')
            elif not target.exists():
                problems.append(prefix + ' is missing')
            elif parsed.fragment and target in documents:
                check(unquote(parsed.fragment) in documents[target].ids, prefix + ' has no matching anchor')

    for lang, suffix, modules in [('zh', '', course), ('en', '.en', english)]:
        if language and language != lang:
            continue
        expected = {ROOT / f'index{suffix}.html'}
        for folder, _, _, _, _, lessons in modules:
            expected.update(ROOT / folder / f'{name}{suffix}.html' for name in ('index', 'curriculum'))
            for n, lesson in enumerate(lessons, 1):
                path = ROOT / folder / 'lessons' / f'{n:02}{suffix}.html'
                expected.add(path)
                if path in documents and len(lesson) == 5:
                    for field, text in zip(('concept', 'example', 'exercise', 'solution'), lesson[1:]):
                        visible = ''.join(Document(inline(text)).text)
                        check(visible in documents[path].paragraphs,
                              f'{path.relative_to(ROOT)}: {field} text lost or stale')
                    source = path.read_text(encoding='utf-8')
                    check(f'<h1>{inline(lesson[0])}</h1>' in source,
                          f'{path.relative_to(ROOT)}: lesson title lost or stale')
                    headings = ('先理解，再写符号', '一步步推导', '停下来试一试', '闭卷回想', '延伸阅读') if not suffix else (
                        'Intuition First, Then Symbols', 'A Derivation, Step by Step',
                        'Pause and Try It', 'Closed-Book Recall', 'Further Reading')
                    check(all(f'<h2>{heading}</h2>' in source for heading in headings),
                          f'{path.relative_to(ROOT)}: missing teaching sections')
                    check('<details><summary>' in source,
                          f'{path.relative_to(ROOT)}: missing solution')
            actual = set((ROOT / folder / 'lessons').glob(f'*{suffix}.html'))
            if not suffix:
                actual = {p for p in actual if not p.name.endswith('.en.html')}
            wanted = {ROOT / folder / 'lessons' / f'{n:02}{suffix}.html' for n in range(1, len(lessons) + 1)}
            check(actual == wanted, f'{folder}: missing or obsolete {lang} lesson pages')
        expected.update(ROOT / 'reference' / f'{name}{suffix}.html' for name in
                        ('glossary', 'labs', 'resources', 'classification', 'curriculum', 'concepts'))
        expected.update(ROOT / 'assets' / f'{name}{suffix}.js' for name in ('widgets', 'concepts'))
        for path in expected:
            check(path.exists(), f'missing generated file: {path.relative_to(ROOT)}')

    with (ROOT / 'assets/msc2020.csv').open(encoding='latin1', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    codes = [row['code'] for row in rows]
    check(len(codes) == len(set(codes)), 'duplicate MSC codes')
    patterns = {'major': r'\d{2}-XX', 'middle': r'\d{2}[A-Z]xx',
                'subject_leaf': r'\d{2}[A-Z]\d{2}', 'general_leaf': r'\d{2}-\d{2}'}
    audit = {kind: sum(bool(re.fullmatch(pattern, c)) for c in codes) for kind, pattern in patterns.items()}
    audit['total'] = len(rows)
    check(audit == load('classification-audit.json'), 'MSC audit differs from source CSV')
    check(sum(audit[k] for k in patterns) == len(rows), 'unrecognized MSC code format')
    tex = (ROOT / 'assets/msc2020.tex').read_text(encoding='utf-8')
    check(set(re.findall(r'\\label\{([^}]+)\}', tex)) == set(codes), 'MSC CSV/TeX code sets differ')
    for suffix in ('', '.en'):
        path = ROOT / 'reference' / f'classification{suffix}.html'
        if path in documents:
            check(set(codes).issubset(documents[path].ids), f'{path.name}: missing MSC anchors')

    if language != 'zh':
        for path in ROOT.rglob('*.en.html'):
            source = re.sub(r'<a href="[^"]*">中文</a>', '', path.read_text(encoding='utf-8'))
            check(not CJK.search(source), f'{path.relative_to(ROOT)}: untranslated CJK/fullwidth text')
        for path in [*ROOT.glob('*.en.md'), *(ROOT / 'learning-records').glob('*.en.md'),
                     ROOT / 'assets/course.en.json', ROOT / 'assets/concepts.en.json',
                     ROOT / 'assets/widgets.en.js', ROOT / 'assets/concepts.en.js']:
            if path.exists():
                check(not CJK.search(path.read_text(encoding='utf-8')),
                      f'{path.relative_to(ROOT)}: untranslated CJK/fullwidth text')
    return problems


def run_static(language=None):
    problems = verify_static(language)
    if problems:
        raise SystemExit('\n'.join(['Verification failed:'] + [' - ' + p for p in problems]))
    print('PASS: bilingual data, generated lesson text, local links and anchors, MSC audit, translation hygiene')
