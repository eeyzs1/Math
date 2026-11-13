"""Browser regressions for both offline editions, including numerical semantics."""
import json
import math
import os
from pathlib import Path
import re

from verify_common import ROOT, load


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def slider(page, name, value):
    page.locator('#' + name).evaluate(
        '(el,value)=>{el.value=value;el.dispatchEvent(new Event("input",{bubbles:true}))}', str(value))


def points(page, selector):
    return page.locator(selector).evaluate(
        'el=>el.getAttribute("points").split(/\\s+/).map(p=>p.split(",").map(Number))')


def launch(playwright):
    candidates = [{}]
    if os.environ.get('MATH_BROWSER_PATH'):
        candidates.insert(0, {'executable_path': os.environ['MATH_BROWSER_PATH']})
    candidates.extend([{'channel': 'chrome'}, {'channel': 'msedge'}])
    failures = []
    for options in candidates:
        try:
            return playwright.chromium.launch(headless=True, **options)
        except Exception as error:
            failures.append(str(error).splitlines()[0])
    raise RuntimeError('No browser available. Run: python -m playwright install chromium\n'
                       + '\n'.join(failures))


def check_labs(page, suffix):
    page.goto((ROOT / 'reference' / f'labs{suffix}.html').as_uri())
    for name in ('h', 'a', 'p', 'step', 'n', 'x0', 'ea', 'eb', 'ed'):
        control = page.locator('#' + name)
        for endpoint in ('min', 'max'):
            slider(page, name, control.get_attribute(endpoint))
            require(not re.search(r'\b(?:NaN|Infinity)\b', page.locator('main').inner_text()),
                    f'{suffix} {name}/{endpoint}: nonfinite output')
            require(page.locator('svg').evaluate_all(r'''els=>els.every(svg=>
                [...svg.querySelectorAll('polyline')].every(line=>
                    line.getAttribute('points').split(/[\s,]+/).every(v=>Number.isFinite(Number(v)))) &&
                [...svg.querySelectorAll('rect')].every(rect=>
                    Number(rect.getAttribute('height'))>=0 && Number(rect.getAttribute('width'))>=0))'''),
                    f'{suffix} {name}/{endpoint}: invalid geometry')
    slider(page, 'h', .01)
    require('2.01' in page.locator('#h-out').inner_text(), 'incorrect secant slope')
    for p, head_index in [(0, 0), (1, 10)]:
        slider(page, 'p', p)
        require('1.000000' in page.locator('#p-out').inner_text(), 'binomial masses do not sum to one')
        bars = page.locator('#prob-svg rect')
        require(abs(float(bars.nth(head_index).get_attribute('height')) - 230) < 1e-8,
                'binomial endpoint must be a point mass')
    slider(page, 'p', .5)
    require('5.00' in page.locator('#p-out').inner_text()
            and '2.50' in page.locator('#p-out').inner_text(), 'incorrect binomial moments')
    slider(page, 'step', 1)
    euler = points(page, '#euler-svg polyline:last-of-type')
    require(len(euler) == 11 and abs(euler[0][1] - euler[-1][1]) < 1e-9,
            'Euler h=1 should oscillate without decay')

    # The histogram must use the same density scale as the normal, not peak matching.
    slider(page, 'n', 1)
    curve = points(page, '#clt-svg polyline')
    curve_height = 270 - min(p[1] for p in curve)
    for bar in page.locator('#clt-svg rect').all():
        count = int(re.search(r': (\d+) ', bar.locator('title').text_content()).group(1))
        ratio = float(bar.get_attribute('height')) / curve_height
        require(abs(ratio - count / 2000 * math.sqrt(.5 * math.pi)) < 1e-9,
                'CLT histogram/normal density scale mismatch')
    slider(page, 'n', 50)
    text = page.locator('#n-out').inner_text()
    numbers = re.findall(r'([0-9]+\.[0-9]+)', text)
    require(abs(float(numbers[-2]) - math.sqrt(.25 / 50)) < .008, 'sampling standard deviation is implausible')
    require(abs(float(numbers[-1]) - .5) < .01, 'sampling mean is implausible')
    snapshot = page.locator('#clt-svg').inner_html()
    summary = page.locator('#n-out').inner_text()
    slider(page, 'h', .5)
    require(page.locator('#clt-svg').inner_html() == snapshot
            and page.locator('#n-out').inner_text() == summary, 'unrelated slider resampled the experiment')
    page.locator('#resample').click()
    require(page.locator('#clt-svg').inner_html() != snapshot, 'explicit resampling did not update the experiment')

    slider(page, 'x0', 0)
    require('0.000 → 1.000 → 0.000' in page.locator('#x0-out').inner_text(), 'Newton two-cycle was lost')
    slider(page, 'x0', -2)
    require('0.000000' in page.locator('#x0-out').inner_text(), 'Newton root residual is too large')
    slider(page, 'x0', 2.5)
    curve = points(page, '#newton-svg g polyline:first-of-type')
    require(abs(curve[-1][1] - 57.890625) < 1e-8, 'Newton curve has clamped function values')
    tangent = points(page, '#newton-svg g polyline:nth-of-type(2)')
    require(tangent[0] == curve[-1], 'Newton tangent does not start on the true curve')
    require(page.locator('#newton-svg [clip-path]').count() == 1, 'Newton geometry needs viewport clipping')
    for a, b, d in [(2, 0, -1), (-1, 0, 2), (0, 1, 0), (0, 0, 0), (1, 0, 1)]:
        for name, value in [('ea', a), ('eb', b), ('ed', d)]:
            slider(page, name, value)
        axes = [points(page, f'#eigen-svg polyline:nth-of-type({i})') for i in (3, 4)]
        radius = math.hypot(a - d, 2 * b)
        expected = [abs((a + d + radius) / 2), abs((a + d - radius) / 2)]
        for line, length in zip(axes, expected):
            require(abs(math.dist(*line) / 80 - length) < 1e-8, 'incorrect eigen semiaxis length')
        for line in axes:
            dx, dy = (line[1][0] - line[0][0]) / 80, -(line[1][1] - line[0][1]) / 80
            require(abs(dx * (b * dx + d * dy) - dy * (a * dx + b * dy)) < 1e-8,
                    'axis is not an eigen-direction')


def check_concepts(page, suffix):
    key = 'math-concepts-en-v1' if suffix else 'math-concepts-v1'
    url = (ROOT / 'reference' / f'concepts{suffix}.html').as_uri()
    page.goto(url)
    data = load(f'concepts{suffix}.json')
    total = sum(len(c['items']) for v in data.values() for c in v)
    require(page.locator('.concept input').count() == total, 'checkbox count differs from concept data')
    first = page.locator('.concept input').first
    first.check()
    require(f'1 / {total}' in page.locator('#total').inner_text(), 'concept progress did not increment')
    page.reload()
    require(first.is_checked(), 'progress did not survive reload')
    with page.expect_download() as download:
        page.locator('#export').click()
    backup = Path(download.value.path()).read_bytes()
    require(len(json.loads(backup)['checked']) == 1, 'backup contains wrong progress')
    page.locator('#reset').click()
    require(f'0 / {total}' in page.locator('#total').inner_text(), 'reset did not clear progress')
    # A backup must work across languages and keep IDs stable.
    other = '' if suffix else '.en'
    page.goto((ROOT / 'reference' / f'concepts{other}.html').as_uri())
    page.locator('#import').set_input_files({'name': 'backup.json', 'mimeType': 'application/json', 'buffer': backup})
    page.wait_for_function("document.querySelector('.concept input').checked")
    require(f'1 / {total}' in page.locator('#total').inner_text(), 'cross-language import failed')
    page.locator('#import').set_input_files({'name': 'bad.json', 'mimeType': 'application/json', 'buffer': b'{"version":1,"checked":["unknown"]}'})
    page.wait_for_function("document.querySelector('#import').value === ''")
    require(page.locator('.concept input').first.is_checked(), 'invalid backup changed progress')
    page.goto(url)
    for corrupt in ('null', '[]', '42', '"text"', '{broken'):
        page.evaluate('([key,value])=>localStorage.setItem(key,value)', [key, corrupt])
        page.reload()
        require(f'0 / {total}' in page.locator('#total').inner_text(), 'corrupt storage broke progress initialization')
    page.evaluate('([key,id])=>localStorage.setItem(key,JSON.stringify({[id]:"false"}))', [key, first.get_attribute('id')])
    page.reload()
    require(not first.is_checked(), 'nonboolean stored value counted as mastery')


def check_pages(page, suffix):
    page.goto((ROOT / '06-analysis/lessons' / f'01{suffix}.html').as_uri())
    page.locator('summary').click()
    require(page.locator('details').get_attribute('open') is not None, 'solution did not open')
    page.locator('summary').click()
    page.evaluate("dispatchEvent(new Event('beforeprint'))")
    require(page.locator('details').get_attribute('open') is not None, 'printing did not expand the solution')
    page.evaluate("dispatchEvent(new Event('beforeprint'));dispatchEvent(new Event('afterprint'))")
    require(page.locator('details').get_attribute('open') is None, 'repeated printing lost folded state')
    page.locator('summary').click()
    page.evaluate("dispatchEvent(new Event('beforeprint'));dispatchEvent(new Event('afterprint'))")
    require(page.locator('details').get_attribute('open') is not None, 'printing closed an originally open solution')
    page.goto((ROOT / 'reference' / f'classification{suffix}.html').as_uri())
    audit = load('classification-audit.json')
    require(page.locator('.major').count() == audit['major'], 'classification major count differs')
    require(page.locator('.entry').count() == audit['subject_leaf'] + audit['general_leaf'], 'classification leaf count differs')
    page.locator('#search').fill('11A05')
    page.wait_for_function("document.querySelectorAll('.entry:not([hidden])').length === 1")
    require(page.locator('[id="11A05"]').is_visible(), 'exact code search failed')
    page.locator('#search').fill('zzzz-no-match')
    page.wait_for_function("document.querySelectorAll('.major:not([hidden])').length === 0")
    page.evaluate("location.hash='60G44'")
    page.wait_for_function("document.getElementById('60G44').checkVisibility()")
    require(page.locator('#search').input_value() == '', 'hash navigation did not clear conflicting filter')
    page.locator('#search').fill('')
    for module in load(f'course{suffix}.json'):
        page.goto((ROOT / module[0] / f'curriculum{suffix}.html').as_uri())
        require(page.locator('article').count() == 5, 'curriculum must contain exactly five planned levels')
    page.set_viewport_size({'width': 320, 'height': 844})
    # Check every generated page at narrow mobile width, including long equations.
    paths = sorted(ROOT.rglob(f'*{suffix}.html'))
    if not suffix:
        paths = [p for p in paths if not p.name.endswith('.en.html')]
    for path in paths:
        page.goto(path.as_uri())
        require(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),
                f'mobile overflow: {path.relative_to(ROOT)}')


def run_browser():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise SystemExit('Install browser-check dependencies: python -m pip install -r requirements.txt') from error
    with sync_playwright() as playwright:
        browser = launch(playwright)
        try:
            for suffix in ('', '.en'):
                context = browser.new_context(viewport={'width': 1280, 'height': 900})
                context.route(re.compile(r'^https?://'), lambda route: route.abort())
                # Reproducible Monte Carlo checks; production keeps the browser RNG.
                context.add_init_script('''let samplingSeed=123456789;
                    Math.random=()=>{samplingSeed=(Math.imul(1664525,samplingSeed)+1013904223)>>>0;return samplingSeed/4294967296};''')
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.on('dialog', lambda dialog: dialog.accept())
                page.goto((ROOT / f'index{suffix}.html').as_uri())
                if not suffix:
                    page.screenshot(path=str(ROOT / 'assets/home-preview.png'), full_page=True)
                check_labs(page, suffix)
                if not suffix:
                    page.screenshot(path=str(ROOT / 'assets/labs-preview.png'), full_page=True)
                check_concepts(page, suffix)
                check_pages(page, suffix)
                require(not errors, f'{suffix}: uncaught browser errors: {errors}')
                context.close()
                print(f'PASS: {suffix or "zh"} numerical labs, backups, storage corruption, print, search, mobile pages', flush=True)
            # Storage disabled by browser privacy settings must not disable the checklist.
            for suffix in ('', '.en'):
                context = browser.new_context()
                context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}})")
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.goto((ROOT / 'reference' / f'concepts{suffix}.html').as_uri())
                page.locator('.concept input').first.check()
                require('1 /' in page.locator('#total').inner_text(), 'unavailable storage disabled checklist')
                require(bool(page.locator('#storage-status').inner_text()), 'unavailable storage was hidden')
                require(not errors, f'unavailable storage: {errors}')
                context.close()
        finally:
            browser.close()
    print('PASS: offline browser verification for both editions')
