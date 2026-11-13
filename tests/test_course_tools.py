"""Regressions for mathematical text that used to disappear as HTML tags."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from site_common import inline


class Text(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.parts, self.links = [], []
        self.feed(source)

    def handle_data(self, text):
        self.parts.append(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs)['href'])


class CourseTextTests(unittest.TestCase):
    def test_chained_inequalities_remain_visible(self):
        for source in ('0<y<1 and y>1', '1<r<3 收敛，r>3 分岔', '|x−a|<δ', 'A&B'):
            with self.subTest(source=source):
                self.assertEqual(''.join(Text(inline(source)).parts), source)

    def test_links_and_notation_coexist(self):
        rendered = Text(inline('0<x<1: <a href="../06-analysis/lessons/01.html">极限</a>'))
        self.assertEqual(''.join(rendered.parts), '0<x<1: 极限')
        self.assertEqual(rendered.links, ['../06-analysis/lessons/01.html'])

    def test_existing_entities_do_not_double_escape(self):
        self.assertEqual(''.join(Text(inline('x&lt;y &amp; z&gt;0')).parts), 'x<y & z>0')

    def test_unsupported_markup_is_visible_text(self):
        source = '<script>alert(1)</script>'
        self.assertEqual(''.join(Text(inline(source)).parts), source)

    def test_unsafe_link_scheme_is_not_active(self):
        self.assertEqual(Text(inline('<a href="javascript:alert(1)">link</a>')).links, [])


if __name__ == '__main__':
    unittest.main()
