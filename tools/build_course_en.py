"""English edition builder for the Mathematics Atlas (数学理解课).

Reads the hand-maintained English data
  - assets/course.en.json   (translated course data; mirrors assets/course.json)
  - RESOURCES.en.md         (translated book list)
and generates the English counterpart pages next to the Chinese ones:
  - NN-*/lessons/NN.en.html, NN-*/index.en.html
  - index.en.html
  - reference/glossary.en.html, reference/labs.en.html, reference/resources.en.html
  - assets/widgets.en.js

Shared assets (style.css, sources.json) are reused from the Chinese build.
The Chinese generators own those files; this script never rewrites them.
Run:  python tools/build_course_en.py
"""
from site_common import inline as R, PRINT_SCRIPT, script_source
from pathlib import Path
import csv
import html
import json
import re

root = Path(__file__).resolve().parents[1]
E = html.escape

data = json.loads((root / 'assets/course.en.json').read_text(encoding='utf-8'))
sources = json.loads((root / 'assets/sources.json').read_text(encoding='utf-8'))
# sources.json is written by the Chinese build and uses full-width punctuation in
# book titles; normalize for display on the English pages.
sources = {k: (v[0].replace('：', ': ').replace('（', '(').replace('）', ')'), v[1])
           for k, v in sources.items()}

# MSC major classes -> official English names (from the official CSV; no retranslation).
groups = {
    '17-history': '00 01 97', '01-foundations': '03', '08-combinatorics': '05',
    '02-algebra': '06 08 12 13 16 17 18 19 20 22', '03-number-theory': '11',
    '05-geometry': '14 51 52 53', '04-linear-algebra': '15',
    '06-analysis': '26 28 30 31 32 33 40 41 42 43 44 46 47 58',
    '11-differential-equations': '34 35 37 39 45', '13-optimization': '49 90 93',
    '07-topology': '54 55 57', '09-probability': '60', '10-statistics': '62',
    '12-numerical': '65', '14-computation': '68 94',
    '15-mathematical-physics': '70 74 76 78 80 81 82 83 85 86',
    '16-modeling': '91 92',
}
msc_names = {r['code'][:2]: r['text'] for r in csv.DictReader(
    (root / 'assets/msc2020.csv').open(encoding='latin1'), delimiter='\t')
    if r['code'].endswith('-XX')}
assert len(msc_names) == 63, 'MSC major-class count mismatch against assets/msc2020.csv'

printjs = PRINT_SCRIPT


def page(title, body, prefix='../', widgets=False, zh=None):
    """Shared page shell. zh = path of the Chinese counterpart page, if any."""
    home = f'<a href="{prefix}index.en.html">Mathematics Atlas</a>' if prefix else ''
    lang = f'<a href="{zh}">中文</a>' if zh else ''
    w = f'<script defer src="{prefix}assets/widgets.en.js"></script>' if widgets else ''
    desc = (f'{title}: an English self-study lesson of Understanding Mathematics, '
            'with intuition, a worked derivation, an exercise, and a folded solution. '
            'Works offline.')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)} · Understanding Mathematics</title>'
            f'<meta name="description" content="{E(desc)}">'
            f'<link rel="stylesheet" href="{prefix}assets/style.css">{w}</head><body><main>'
            f'<nav>{home}<a href="{prefix}reference/glossary.en.html">Notation Reference</a>'
            f'<a href="{prefix}reference/labs.en.html">Interactive Labs</a>{lang}</nav>'
            f'{body}'
            f'<footer>Each lesson takes about 15–25 minutes. Answer on your own before opening '
            'the solution; redo the lesson closed-book after 1 day, 3 days, and 7 days. When a '
            'step is unclear, send me the problem together with your reasoning and we can keep '
            f'working through it.</footer></main>{printjs}</body></html>')


# ---------------------------------------------------------------- lesson pages
for folder, title, subs, pre, source, lessons in data:
    d = root / folder
    (d / 'lessons').mkdir(parents=True, exist_ok=True)
    name_s, url = sources[source]
    links = ''
    for i, (name, concept, example, q, a) in enumerate(lessons, 1):
        filename = f'{i:02}.en.html'
        links += f'<li><a href="lessons/{filename}">{i:02} · {R(name)}</a></li>'
        nav = f'<a href="../index.en.html">Back to the branch overview</a>'
        if i > 1:
            nav += f' · <a href="{i-1:02d}.en.html">Previous lesson</a>'
        if i < len(lessons):
            nav += f' · <a href="{i+1:02d}.en.html">Next lesson</a>'
        short = name.split(':')[0]
        body = (
            f'<header><p class="tag">{E(title)} / LESSON {i:02}</p><h1>{R(name)}</h1>'
            f'<p>Goal for this lesson: explain "{R(short)}" in your own words, then complete the '
            f'transfer exercise below on your own.</p>'
            f'<p>Prerequisites: {R(pre)}. Try the worked example first; if the notation feels '
            f'heavy, go back to the preparation module.</p></header>'
            '<article>'
            '<h2>Intuition First, Then Symbols</h2>'
            f'<p>{R(concept)}</p>'
            '<h2>A Derivation, Step by Step</h2>'
            f'<p class="formula">{R(example)}</p>'
            '<h2>Pause and Try It</h2>'
            f'<p>{R(q)}</p>'
            '<label for="answer">Write your answer and reasoning (this box is not graded and '
            'nothing is saved)</label>'
            '<textarea id="answer" placeholder="Write your reasoning before opening the '
            'solution."></textarea>'
            '<details><summary>Show the solution and self-check criteria</summary>'
            f'<p>{R(a)}</p>'
            '<p>Self-check: Is the conclusion correct? Are the conditions stated? Can you '
            'explain the key steps without looking at the example? If you only recalled the '
            'answer, redo the lesson.</p></details>'
            '<h2>Closed-Book Recall</h2>'
            '<p>Close the solution: write down one definition from this lesson, the key step '
            'of the worked example, and the conditions the conclusion needs. Then change one '
            'number in the example and recompute.</p>'
            '<p><a href="../../reference/labs.en.html">Explore the related figures in the '
            'Interactive Labs</a> — turn what you observe into a conjecture, then verify it '
            'against the definitions.</p>'
            '<h2>Further Reading</h2>'
            f'<p>Background: <a href="{url}">{R(name_s)}</a>. Consult the relevant chapters by '
            'topic rather than page by page; these open textbooks serve to double-check '
            'definitions. This lesson is an independent exposition, not a translation of any '
            'textbook. The branch page lists directions that follow.</p></article>'
            f'<p>{nav}</p>')
        (d / 'lessons' / filename).write_text(
            page(name, body, '../../', zh=f'{i:02}.html'), encoding='utf-8')

    # ------------------------------------------------------------- branch page
    plans = ''
    for topic in [t.strip() for t in subs.split(';')]:
        plans += (f'<li><b>{E(topic)}</b>: first master the definitions and worked examples '
                  f'of this branch\'s {len(lessons)} introductory lessons; full developments '
                  'of each subfield follow the staged route.</li>')
    msc_section = ''
    if folder in groups:
        msc_list = ''.join(
            f'<li>{code} · {E(msc_names[code])}</li>'
            for code in sorted(msc_names) if code in groups[folder].split())
        msc_section = (
            '<section class="panel"><h2>Supplementary Index of Research Directions</h2>'
            '<p>The MSC major classes grouped under this folder are listed below as the scope '
            'for future course development; cross-branch topics may also live in other '
            f'folders.</p><ul>{msc_list}</ul></section>')
    body = (
        f'<header><p class="tag">BRANCH {folder[:2]} / INTRODUCTORY UNIT</p><h1>{E(title)}</h1>'
        f'<p>Prerequisites: {R(pre)}</p>'
        f'<p>This branch has {len(lessons)} introductory lessons ready to study; the subfields '
        'listed below are later routes, not yet expanded into full treatments.</p>'
        '<p class="curriculum-link"><a href="curriculum.en.html">See the staged route from '
        'first lessons to research training →</a></p></header>'
        f'<h2>Start Learning</h2><ol>{links}</ol>'
        '<h2>Subfield Routes (a suggested order, from earlier to later)</h2>'
        f'<ol>{plans}</ol>'
        f'{msc_section}'
        '<h2>How Far to Go Before Moving On</h2>'
        '<p>Finish the exercises of two lessons, state the conditions of each result, and give '
        'an example or counterexample of your own. Advanced subfields often require crossed '
        'prerequisites — don\'t march through them in name order.</p>'
        '<p><a href="../reference/labs.en.html">Interactive Labs</a> · '
        '<a href="../reference/resources.en.html">Books &amp; branch sources</a></p>')
    (d / 'index.en.html').write_text(
        page(title, body, zh='index.html'), encoding='utf-8')

# ----------------------------------------------------------------- root index
cards = ''.join(
    f'<a class="card" href="{folder}/index.en.html"><span class="tag">{folder[:2]}</span>'
    f'<h2>{E(title)}</h2><p>{E(subs)}</p></a>'
    for folder, title, subs, pre, source, lessons in data)
n_lessons = sum(len(m[5]) for m in data)
body = (
    '<header><p class="tag">THE MATHEMATICS ATLAS</p>'
    '<h1>From reading formulas to understanding mathematics.</h1>'
    f'<p>{len(data)} modules · {n_lessons} introductory lessons · 7 interactive labs</p>'
    '<p>Build intuition first, then make the conditions explicit, and test understanding '
    'with derivations and exercises.</p></header>'
    '<section class="panel"><h2>Where to Start?</h2>'
    '<p>Answer these with the page closed: ① 100 rises 20% and then falls 20% — what is it '
    'now? ② Which real numbers solve x²=x? ③ A fair die is known to show an even number; '
    'what is the probability that it shows more than 3?</p>'
    '<details><summary>Check answers and pick a starting point</summary>'
    '<p>① 96 — if this surprised you, start with 00. ② 0 and 1 — if unsure, start with 02 '
    '(and 01 for proofs). ③ 2/3 — if unsure, start with 09. These three questions only '
    'locate a starting point; they cannot certify mastery of a branch.</p></details>'
    '<p><a href="00-preparation/index.en.html">Start with the preparation module →</a>'
    ' · <a href="reference/labs.en.html">Open the Interactive Labs →</a></p>'
    '<p>Suggested route: preparation → proof → algebra → linear algebra / geometry → '
    'calculus, then probability, discrete mathematics, topology, or the applied branches, '
    'by interest.</p></section>'
    '<section class="panel" id="extended-atlas"><h2>Full classification and long-term '
    'routes</h2><p><a href="reference/classification.en.html">Open the complete MSC2020 '
    'source classification index</a> · <a href="reference/curriculum.en.html">See each '
    'branch\'s staged overview, from foundations to research training</a></p>'
    '<p>The classification index searches by code or English keyword. The staged routes are '
    'a plan; the advanced lessons are not yet written.</p></section>'
    '<h2>The Branch Map of Mathematics</h2>'
    f'<div class="grid">{cards}</div>')
(root / 'index.en.html').write_text(
    page('The Branch Map of Mathematics', body, '', zh='index.html'), encoding='utf-8')

# ------------------------------------------------------------------- glossary
terms = [
    ('∀ / ∃', 'For all / there exists; swapping the order of the quantifiers can change the '
              'proposition.'),
    ('⇒ / ⇔', 'Implies / is equivalent to; the converse of an implication does not hold '
              'automatically.'),
    ('∈ / ⊆', 'An element belongs to a set / one set is contained in another.'),
    ('∅', 'The empty set; it contains no elements and is a subset of every set.'),
    ('∪ / ∩ / ∖', 'Union, intersection, difference; counting a union requires subtracting '
                  'the overlap (inclusion–exclusion).'),
    ('f: A → B', 'A function with domain A and codomain B; the values actually taken form '
                 'the image.'),
    ('lim / f′ / ∫', 'Limit / derivative / integral; check the existence conditions before '
                     'using them.'),
    ('ε-δ', 'The precise language of limits: for every ε>0 there is a δ>0; ε comes first, '
            'then δ.'),
    ('dy/dx vs y″', 'Derivative notation: dy/dx stresses the "limit of difference '
                    'quotients"; y″ is the second derivative (the derivative of the '
                    'derivative).'),
    ('∂ / ∇', 'Partial derivative (freeze the other variables and differentiate one) / '
              'gradient (the vector of partial derivatives, pointing in the direction of '
              'steepest ascent).'),
    ('Σ / Π', 'Sum / product; watch the starting index — Σ from n=0 and Σ from n=1 are '
              'different sums.'),
    ('∞', 'Infinity; "tends to ∞" is shorthand for "grows beyond every bound" — ∞ is not a '
          'real number.'),
    ('ℕ / ℤ / ℚ / ℝ / ℂ', 'The sets of natural numbers / integers / rationals / reals / '
                          'complex numbers; before saying "no solution", ask in which set.'),
    ('≡ (mod m)', 'Congruence: m divides the difference of the two numbers; the standard '
                  'example of an equivalence relation and a quotient set.'),
    ('⌊x⌋ / ⌈x⌉', 'Floor / ceiling; workhorse tools for step counting and divisibility '
                  'counting.'),
    ('|x|', 'Absolute value; distance on the number line, and a signal to argue by cases.'),
    ('ker / im', 'The kernel (inputs mapped to zero) and the image (all outputs) of a linear '
                 'map; the rank–nullity theorem relates the two.'),
    ('det / tr', 'Determinant (the area/volume scaling factor) / trace (the sum of the '
                 'diagonal entries, equal to the sum of the eigenvalues).'),
    ('Aᵀ', 'Transpose; the inner product can be written uᵀv, and the least-squares normal '
           'equations are AᵀAx=Aᵀb.'),
    ('Av=λv', 'Eigenvalue λ and nonzero eigenvector v: the spanned line is preserved; '
              'negative λ reverses direction and λ=0 maps v to zero.'),
    ('‖u‖ / u·v', 'Norm (length √(u·u)) / inner product; a zero inner product means '
                  'perpendicular.'),
    ('O(·)', 'Asymptotic upper bound; when the input doubles, watch by what factor the '
             'leading term grows.'),
    ('sup / inf', 'Supremum / infimum; the core statement of the completeness of the real '
                  'numbers.'),
    ('max / min / argmax', 'Maximum and minimum values / the input position at which the '
                           'maximum is attained.'),
    ('E[X] / Var / Cov', 'Expectation (a probability-weighted average) / variance / '
                         'covariance; linearity of expectation requires no independence.'),
    ('P(A|B)', 'The probability of A given that B occurred; requires P(B)>0.'),
    ('X ~ N(μ,σ²)', 'The random variable X follows a normal distribution with parameters μ '
                    'and σ²; read "~" as "is distributed as".'),
    ('H(X)', 'Entropy: the average number of bits of uncertainty in a random variable.'),
    ('H₀ / p-value', 'Null hypothesis / the probability, if H₀ is true, of data at least '
                     'this extreme; a p-value is not the probability that H₀ is true.'),
    ('R²', 'Coefficient of determination: the share of the variance explained by a '
           'regression; a high R² does not imply causation.'),
    ('κ(A)', 'Condition number: the worst-case amplification from relative input error to '
             'relative output error.'),
    ('χ(G)', 'Chromatic number of a graph: the fewest colors needed so that adjacent '
             'vertices get different colors.'),
    ('φ(n)', 'Euler\'s totient function: the count of integers in 1..n coprime to n; a key '
             'parameter of RSA.'),
    ('⊕ / ⊗', 'Direct sum / tensor product: ways to "put spaces together" or "multiply '
               'spaces".'),
    ('Vector / matrix', 'A vector records data or a direction; a matrix represents a linear '
                        'map in given bases.'),
    ('Definition / theorem / conjecture', 'A convention fixing what a term means / a result '
                                          'proven from assumptions / a judgment awaiting '
                                          'proof or refutation.'),
    ('Example / counterexample', 'Examples build understanding; a counterexample can refute '
                                 'a universal statement, and finitely many confirming '
                                 'examples usually cannot prove one.'),
]
(root / 'reference/glossary.en.html').write_text(
    page('Notation and Methods: Quick Reference',
         '<h1>Notation and Methods: Quick Reference</h1>'
         + ''.join(f'<article><h2>{a}</h2><p>{b}</p></article>' for a, b in terms),
         zh='glossary.html'),
    encoding='utf-8')

# ----------------------------------------------------------------------- labs
labs = (
    '<header><p class="tag">EXPLORE → CONJECTURE → PROVE</p>'
    '<h1>Put the Concepts in Motion</h1>'
    '<p>Predict first, then drag the slider. Figures are for discovering patterns; '
    'derivations explain why the patterns hold.</p></header>'
    '<section class="panel" id="derivative"><h2>01 · How a Secant Approaches the '
    'Tangent</h2><p>The curve y=x², the fixed point (1,1), and a second point '
    '(1+h,(1+h)²). Predict: as h approaches 0, what does the secant slope approach?</p>'
    '<label for="h">Increment h (0.01–1)</label>'
    '<input id="h" type="range" min="0.01" max="1" step="0.01" value="0.7">'
    '<output id="h-out" aria-live="polite"></output>'
    '<svg id="derivative-svg" viewBox="0 0 600 320" role="img" aria-label="A parabola '
    'with a secant line through two of its points"></svg>'
    '<p>The difference quotient is 2+h, so the limit is 2. The slider cannot reach 0, '
    'because the difference quotient is undefined at h=0 — the derivative is a limit. '
    'Blue is the curve, orange the secant, and the dashed line the tangent.</p>'
    '<a href="../06-analysis/lessons/02.en.html">Back to the derivative lesson</a></section>'
    '<section class="panel"><h2>02 · How the Determinant Scales Area</h2>'
    '<p>The map A=diag(a,1). Predict: what happens when a=0, or when a is negative?</p>'
    '<label for="a">Horizontal scale factor a (−2–2)</label>'
    '<input id="a" type="range" min="-2" max="2" step="0.1" value="1.5">'
    '<output id="a-out" aria-live="polite"></output>'
    '<svg id="linear-svg" viewBox="0 0 600 320" role="img" aria-label="A unit square and '
    'the rectangle it maps to under a linear transformation"></svg>'
    '<p>The dashed outline is the original square. The shaded rectangle has area |a| and '
    'oriented area a. At a=0 the square collapses onto a line; a negative a flips it to the '
    'other side. This demo shows a diagonal matrix only — general matrices do more than '
    'scale.</p>'
    '<a href="../04-linear-algebra/lessons/04.en.html">Back to the determinant '
    'lesson</a></section>'
    '<section class="panel"><h2>03 · How the Binomial Distribution Changes Shape</h2>'
    '<p>Ten independent coin flips, each landing heads with probability p. The bars show '
    'the theoretical probability of exactly k heads — not one random sample. Predict: as p '
    'moves from 0.5 to 0.9, which way does the peak shift?</p>'
    '<label for="p">Heads probability p (0–1)</label>'
    '<input id="p" type="range" min="0" max="1" step="0.01" value="0.5">'
    '<output id="p-out" aria-live="polite"></output>'
    '<svg id="prob-svg" viewBox="0 0 600 320" role="img" aria-label="The probability '
    'distribution of the number of heads in ten independent flips"></svg>'
    '<p>P(X=k)=C(10,k)pᵏ(1−p)¹⁰⁻ᵏ. Expectation =10p, variance =10p(1−p). Equal expectations '
    'do not mean equal spread. At p=0 and p=1 the distribution concentrates on a single '
    'outcome.</p>'
    '<a href="../09-probability/lessons/05.en.html">Back to the common-distributions '
    'lesson</a></section>'
    '<section class="panel"><h2>04 · The Step Size Can Change the System\'s Behavior</h2>'
    '<p>For y′=−2y, y(0)=1, run Euler\'s method up to t=10: the next value is (1−2h)y. '
    'Predict: at h=1, does the numerical solution still decay?</p>'
    '<label for="step">Step size h (0.1–1.2)</label>'
    '<input id="step" type="range" min="0.1" max="1.2" step="0.1" value="0.5">'
    '<output id="step-out" aria-live="polite"></output>'
    '<svg id="euler-svg" viewBox="0 0 600 320" role="img" aria-label="Euler\'s numerical '
    'solution compared with the exact exponentially decaying one"></svg>'
    '<p>Blue is the exact solution, orange the numerical one. For 0&lt;h&lt;1 the amplitude '
    'decays; at h=1 it oscillates without decay; for h&gt;1 it diverges. The vertical axis '
    'auto-scales with the data, so read the numbers above as well.</p>'
    '<a href="../12-numerical/lessons/03.en.html">Back to the numerical-methods '
    'lesson</a></section>'
    '<section class="panel"><h2>05 · How Sample Means Become Normal</h2>'
    '<p>Each group flips a fair coin n times and records the proportion of heads; repeat '
    'for 2000 groups and draw a histogram of the means. Predict: how do the shapes for n=1 '
    'and n=50 differ?</p>'
    '<label for="n">Flips per group n (1–50)</label>'
    '<input id="n" type="range" min="1" max="50" step="1" value="1">'
    '<button id="resample" type="button">Resample 2000 groups</button><output id="n-out" aria-live="polite"></output>'
    '<svg id="clt-svg" viewBox="0 0 600 320" role="img" aria-label="A histogram of sample '
    'means overlaid with a normal density curve"></svg>'
    '<p>The dashed curve is the normal density N(0.5, 0.25/n). Bar heights are frequency '
    'divided by bin width, sharing the curve\'s vertical scale; bar areas sum to 1. '
    'For small n the distribution is discrete and the normal approximation is poor. '
    'As n grows the means concentrate at 0.5, with standard deviation shrinking like '
    '1/√n. Other experiments do not resample these data.</p>'
    '<a href="../09-probability/lessons/07.en.html">Back to the limit-theorems '
    'lesson</a></section>'
    '<section class="panel"><h2>06 · Newton\'s Method Depends on the Initial Guess</h2>'
    '<p>Solve f(x)=x³−2x+2=0: from x₀ draw the tangent; its zero becomes the next iterate. '
    'Predict: what happens at x₀=0? And at x₀=−2?</p>'
    '<label for="x0">Initial value x₀ (−2.5–2.5)</label>'
    '<input id="x0" type="range" min="-2.5" max="2.5" step="0.1" value="-2">'
    '<output id="x0-out" aria-live="polite"></output>'
    '<svg id="newton-svg" viewBox="0 0 600 320" role="img" aria-label="Newton-iteration '
    'tangents and iterates on a cubic curve"></svg>'
    '<p>The orange dashes are the successive tangents. Starting at 0 or 1 gives an exact '
    'two-cycle; nearby points may be attracted to that cycle. Near the real root '
    '(about −1.77) it converges quickly — a good '
    'starting point is part of Newton\'s method.</p>'
    '<a href="../12-numerical/lessons/04.en.html">Back to the Newton\'s-method '
    'lesson</a></section>'
    '<section class="panel"><h2>07 · Circle to Ellipse: Semiaxis Lengths Are '
    '|λ|</h2><p>A symmetric matrix A=[[a,b],[b,d]] acts on the unit circle. Predict: '
    'what shape is the image? What determines the semi-axis directions? What happens when '
    'b=0?</p>'
    '<label for="ea">Diagonal entry a (−2–2)</label>'
    '<input id="ea" type="range" min="-2" max="2" step="0.1" value="1.5">'
    '<label for="eb">Off-diagonal entry b (−2–2)</label>'
    '<input id="eb" type="range" min="-2" max="2" step="0.1" value="0.5">'
    '<label for="ed">Diagonal entry d (−2–2)</label>'
    '<input id="ed" type="range" min="-2" max="2" step="0.1" value="-1">'
    '<output id="e-out" aria-live="polite"></output>'
    '<svg id="eigen-svg" viewBox="0 0 600 320" role="img" aria-label="The unit circle '
    'mapped by a symmetric matrix onto an ellipse, with eigen-directions drawn as orange '
    'segments"></svg>'
    '<p>The gray dashed circle is the unit circle; the green ellipse is its image; the '
    'orange segments show the principal axes. Semiaxis lengths are |λ|, directions '
    'are eigenvectors; the sign of λ records reversal, not length. Singular matrices '
    'collapse the image to a segment or a point. |det| is the area scale factor. '
    'At b=0 the axes lie along the coordinate '
    'axes.</p>'
    '<a href="../04-linear-algebra/lessons/07.en.html">Back to the eigenvalue '
    'lesson</a></section>')
(root / 'reference/labs.en.html').write_text(
    page('Interactive Labs', labs, widgets=True, zh='labs.html'), encoding='utf-8')

# ------------------------------------------------------------------- widgets
js = script_source('widgets', 'en')
(root / 'assets/widgets.en.js').write_text(js, encoding='utf-8')

# ------------------------------------------------- resources.en.md -> HTML
def _inline(s):
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s


_rout = ['<header><p class="tag">SOURCES</p><h1>Textbook Sources and How to Use '
         'Them</h1></header><section class="panel">']
_inlist = False
for _line in (root / 'RESOURCES.en.md').read_text(encoding='utf-8').splitlines():
    _l = _line.strip()
    if not _l or _l.startswith('# '):
        continue
    if _l.startswith('## '):
        if _inlist:
            _rout.append('</ul>')
            _inlist = False
        _rout.append(f'<h2>{_inline(_l[3:])}</h2>')
    elif _l.startswith('- '):
        if not _inlist:
            _rout.append('<ul>')
            _inlist = True
        _rout.append(f'<li>{_inline(_l[2:])}</li>')
    else:
        if _inlist:
            _rout.append('</ul>')
            _inlist = False
        _rout.append(f'<p>{_inline(_l)}</p>')
if _inlist:
    _rout.append('</ul>')
_rout.append('</section>')
(root / 'reference/resources.en.html').write_text(
    page('Textbook Sources', ''.join(_rout), zh='resources.html'), encoding='utf-8')

print(f'Built English edition: {len(data)} modules, '
      f'{sum(len(m[5]) for m in data)} lessons')
