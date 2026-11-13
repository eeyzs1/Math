"""Split zh source data into per-module fragments for translation, then reassemble.

Usage:
  python tools/en-src/split.py          # write tools/en-src/zh/*.json fragments
  python tools/en-src/split.py assemble # merge tools/en-src/en/*.json -> assets/*.en.json
"""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
ZH_COURSE = root / 'assets/course.json'
ZH_CONCEPTS = root / 'assets/concepts.json'


def split():
    src = json.loads(ZH_COURSE.read_text(encoding='utf-8'))
    out_c = root / 'tools/en-src/zh/course'
    out_c.mkdir(parents=True, exist_ok=True)
    (root / 'tools/en-src/en/course').mkdir(parents=True, exist_ok=True)
    for folder, title, subs, pre, source, lessons in src:
        frag = {"folder": folder, "title": title, "subs": subs,
                "pre": pre, "source": source, "lessons": lessons}
        (out_c / f'{folder}.json').write_text(
            json.dumps(frag, ensure_ascii=False, indent=1), encoding='utf-8')
    concepts = json.loads(ZH_CONCEPTS.read_text(encoding='utf-8'))
    out_k = root / 'tools/en-src/zh/concepts'
    out_k.mkdir(parents=True, exist_ok=True)
    (root / 'tools/en-src/en/concepts').mkdir(parents=True, exist_ok=True)
    for k, v in concepts.items():
        (out_k / f'{k}.json').write_text(
            json.dumps({k: v}, ensure_ascii=False, indent=1), encoding='utf-8')
    print('modules:', len(src), '| lessons:', sum(len(m[5]) for m in src),
          '| concept modules:', len(concepts))


CJK = re.compile(r'[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]')


def check_clean(path, text):
    hits = sorted(set(CJK.findall(text)))
    assert not hits, f'{path}: CJK/fullwidth remnants {hits}'


def assemble():
    order = [m[0] for m in json.loads(ZH_COURSE.read_text(encoding='utf-8'))]
    zh = {m[0]: m for m in json.loads(ZH_COURSE.read_text(encoding='utf-8'))}
    en_dir = root / 'tools/en-src/en/course'
    merged = []
    for folder in order:
        p = en_dir / f'{folder}.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        check_clean(p, p.read_text(encoding='utf-8'))
        assert d['folder'] == folder, f'{folder}: folder mismatch'
        assert set(d) == {'folder', 'title', 'subs', 'pre', 'source', 'lessons'}
        assert d['source'] == zh[folder][4], f'{folder}: source key changed'
        assert len(d['lessons']) == len(zh[folder][5]), f'{folder}: lesson count mismatch'
        for i, les in enumerate(d['lessons']):
            assert isinstance(les, list) and len(les) == 5, f'{folder} lesson {i+1}: need 5 fields'
            assert all(isinstance(x, str) and x.strip() for x in les), f'{folder} lesson {i+1}: empty field'
        assert ';' in d['subs'], f'{folder}: subs should be "; "-separated'
        merged.append([d['folder'], d['title'], d['subs'], d['pre'], d['source'], d['lessons']])
    (root / 'assets/course.en.json').write_text(
        json.dumps(merged, ensure_ascii=False, indent=1), encoding='utf-8')

    zh_concepts = json.loads(ZH_CONCEPTS.read_text(encoding='utf-8'))
    kc = root / 'tools/en-src/en/concepts'
    out = {}
    for folder in order:
        p = kc / f'{folder}.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        check_clean(p, p.read_text(encoding='utf-8'))
        assert set(d) == {folder}, f'{folder}: concepts fragment keys {set(d)}'
        entries = d[folder]
        assert len(entries) == len(zh_concepts[folder]), f'{folder}: concepts entry count mismatch'
        for e, ezh in zip(entries, zh_concepts[folder]):
            assert e['file'] == ezh['file'], f'{folder}: concepts file key mismatch'
            assert len(e['items']) == len(ezh['items']), f'{folder} {e["file"]}: item count mismatch'
            assert all(isinstance(t, str) and t.strip() for t in e['items'])
        out[folder] = entries
    (root / 'assets/concepts.en.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('assembled: assets/course.en.json |',
          sum(len(m[5]) for m in merged), 'lessons |',
          sum(len(v) for v in out.values()), 'concept entries')


if __name__ == '__main__':
    assemble() if len(sys.argv) > 1 and sys.argv[1] == 'assemble' else split()
