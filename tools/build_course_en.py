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

printjs = ("<script>'use strict';let printed=[];"
           "addEventListener('beforeprint',()=>{printed=[...document.querySelectorAll('details:not([open])')];"
           "printed.forEach(d=>d.open=true)});"
           "addEventListener('afterprint',()=>{printed.forEach(d=>d.open=false);printed=[]});</script>")


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
            'working through it.</footer></main>{printjs}</body></html>')


# ---------------------------------------------------------------- lesson pages
for folder, title, subs, pre, source, lessons in data:
    d = root / folder
    (d / 'lessons').mkdir(parents=True, exist_ok=True)
    name_s, url = sources[source]
    links = ''
    for i, (name, concept, example, q, a) in enumerate(lessons, 1):
        filename = f'{i:02}.en.html'
        links += f'<li><a href="lessons/{filename}">{i:02} · {name}</a></li>'
        nav = f'<a href="../index.en.html">Back to the branch overview</a>'
        if i > 1:
            nav += f' · <a href="{i-1:02d}.en.html">Previous lesson</a>'
        if i < len(lessons):
            nav += f' · <a href="{i+1:02d}.en.html">Next lesson</a>'
        short = name.split(':')[0]
        body = (
            f'<header><p class="tag">{E(title)} / LESSON {i:02}</p><h1>{name}</h1>'
            f'<p>Goal for this lesson: explain "{short}" in your own words, then complete the '
            f'transfer exercise below on your own.</p>'
            f'<p>Prerequisites: {pre}. Try the worked example first; if the notation feels '
            f'heavy, go back to the preparation module.</p></header>'
            '<article>'
            '<h2>Intuition First, Then Symbols</h2>'
            f'<p>{concept}</p>'
            '<h2>A Derivation, Step by Step</h2>'
            f'<p class="formula">{example}</p>'
            '<h2>Pause and Try It</h2>'
            f'<p>{q}</p>'
            '<label for="answer">Write your answer and reasoning (this box is not graded and '
            'nothing is saved)</label>'
            '<textarea id="answer" placeholder="Write your reasoning before opening the '
            'solution."></textarea>'
            '<details><summary>Show the solution and self-check criteria</summary>'
            f'<p>{a}</p>'
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
            f'<p>Background: <a href="{url}">{name_s}</a>. Consult the relevant chapters by '
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
        f'<p>Prerequisites: {pre}</p>'
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
    ('Av=λv', 'Eigenvalue λ and eigenvector v: the direction is unchanged and merely scaled '
              'by λ.'),
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
    '<output id="n-out" aria-live="polite"></output>'
    '<svg id="clt-svg" viewBox="0 0 600 320" role="img" aria-label="A histogram of sample '
    'means overlaid with a normal density curve"></svg>'
    '<p>The gray dashed curve is the theoretical normal density N(0.5, 0.25/n). As n grows '
    'the means concentrate at 0.5 while the spread shrinks like 1/√n — an experimental '
    'picture of the central limit theorem.</p>'
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
    '<p>The orange dashes are the successive tangents. Starting near 0, the iteration '
    'cycles between 0 and 1; near the real root (about −1.77) it converges quickly — a good '
    'starting point is part of Newton\'s method.</p>'
    '<a href="../12-numerical/lessons/04.en.html">Back to the Newton\'s-method '
    'lesson</a></section>'
    '<section class="panel"><h2>07 · Circle to Ellipse: the Eigenvalues Are the '
    'Semi-Axes</h2><p>A symmetric matrix A=[[a,b],[b,d]] acts on the unit circle. Predict: '
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
    'orange segments are the two eigen-directions, each with length equal to the '
    'corresponding eigenvalue. Semi-axes =|λ|, directions = eigenvectors; |det| is the area '
    'scale factor. At b=0 the ellipse straightens out and its axes lie along the coordinate '
    'axes.</p>'
    '<a href="../04-linear-algebra/lessons/07.en.html">Back to the eigenvalue '
    'lesson</a></section>')
(root / 'reference/labs.en.html').write_text(
    page('Interactive Labs', labs, widgets=True, zh='labs.html'), encoding='utf-8')

# ------------------------------------------------------------------- widgets
js = '''"use strict";
const $=id=>document.getElementById(id);
function path(points,color,dash=''){return `<polyline points="${points.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="3" stroke-dasharray="${dash}"/>`;}
const axes=(x=65,y=270)=>`<path d="M25 ${y}H580M${x} 15V290" stroke="#5f7470" fill="none"/><text x="565" y="300">x</text>`;
function render(){
 if(!$('h'))return;
 let h=+$('h').value, pts=[];const xy=(x,y)=>[65+x*200,270-y*55];
 for(let x=0;x<=2.21;x+=.03)pts.push(xy(x,x*x));
 $('derivative-svg').innerHTML=axes()+path(pts,'#086a67')+path([xy(0,-1),xy(2.3,3.6)],'#697c78','6 5')+path([xy(.5,1-(2+h)*.5),xy(2,1+(2+h))],'#bd6029')+[xy(1,1),xy(1+h,(1+h)**2)].map(p=>`<circle cx="${p[0]}" cy="${p[1]}" r="5" fill="#bd6029"/>`).join('')+'<text x="280" y="220">Fixed point (1,1)</text>';
 $('h-out').textContent=`h=${h.toFixed(2)}; secant slope=${(2+h).toFixed(2)}; tangent slope=2`;
 let a=+$('a').value, x=300, y=250,s=90;
 $('linear-svg').innerHTML=axes(x,y)+`<rect x="300" y="160" width="90" height="90" fill="none" stroke="#677c77" stroke-dasharray="6 4"/><rect x="${Math.min(x,x+a*s)}" y="160" width="${Math.abs(a*s)}" height="90" fill="#147d7866" stroke="#086a67"/><text x="30" y="35">One unit corresponds to 90 pixels</text>`;
 $('a-out').textContent=`a=${a.toFixed(1)}; det(A)=${a.toFixed(1)}; area=${Math.abs(a).toFixed(1)}`;
 let p=+$('p').value, bars='',sum=0;function choose(n,k){let c=1;for(let j=1;j<=k;j++)c=c*(n-j+1)/j;return c;}
 for(let k=0;k<=10;k++){let v=choose(10,k)*p**k*(1-p)**(10-k);sum+=v;bars+=`<rect x="${40+k*48}" y="${270-v*230}" width="32" height="${v*230}" fill="#086a67"><title>k=${k}, probability=${v.toFixed(5)}</title></rect><text x="${45+k*48}" y="295">${k}</text>`;}
 $('prob-svg').innerHTML='<path d="M25 270H580" stroke="#5f7470" fill="none"/>'+bars+'<text x="30" y="25">Probability (axis 0–1); horizontal axis: number of heads k</text>';
 $('p-out').textContent=`p=${p.toFixed(2)}; mean=${(10*p).toFixed(2)}; variance=${(10*p*(1-p)).toFixed(2)}; total probability=${sum.toFixed(6)}`;
 let step=+$('step').value;if(!(step>0))step=0.1;let arr=[[0,1]],v=1;for(let j=1;j*step<=10+1e-9;j++){v*=1-2*step;arr.push([j*step,v]);}
 const scale=Math.max(1,...arr.map(x=>Math.abs(x[1]))),pos=(t,v)=>[45+t*52,155-v/scale*120];let exact=[];for(let t=0;t<=10;t+=.05)exact.push(pos(t,Math.exp(-2*t)));
 $('euler-svg').innerHTML=axes(45,155)+path(exact,'#086a67')+path(arr.map(([t,v])=>pos(t,v)),'#bd6029')+`<text x="40" y="25">Vertical range about ±${scale.toFixed(2)}; horizontal axis t=0…10</text>`;
 $('step-out').textContent=`h=${step.toFixed(1)}; one-step factor=${(1-2*step).toFixed(2)}; last step t=${arr.at(-1)[0].toFixed(1)}, y≈${v.toFixed(5)}`;
 if($('n')){const nn=+$('n').value,groups=2000,means=[];for(let g=0;g<groups;g++){let s=0;for(let i=0;i<nn;i++)s+=Math.random()<.5?0:1;means.push(s/nn);}
  const bins=40,hist=new Array(bins).fill(0);for(const m of means)hist[Math.min(bins-1,Math.floor(m*bins))]++;
  const mx=Math.max(...hist),bw=540/bins,sd=Math.sqrt(.25/nn);let bars='';hist.forEach((h,i)=>{bars+=`<rect x="${30+i*bw}" y="${270-h/mx*230}" width="${bw-2}" height="${h/mx*230}" fill="#086a67"><title>bin ${(i/bins).toFixed(2)}–${((i+1)/bins).toFixed(2)}: ${h} groups</title></rect>`});
  const pk=groups*(1/bins)/(sd*Math.sqrt(2*Math.PI)),curve=[];for(let i=0;i<=120;i++){const x=i/120,d=groups*(1/bins)/(sd*Math.sqrt(2*Math.PI))*Math.exp(-((x-.5)**2)/(2*sd*sd));curve.push([30+x*540,270-d/pk*230]);}
  $('clt-svg').innerHTML=axes(30,270)+path(curve,'#5f7470','6 5')+bars+'<text x="30" y="25">Histogram of heads proportions (2000 groups) with the theoretical normal density (dashed)</text>';
  const mo=means.reduce((a,b)=>a+b,0)/groups,ms=Math.sqrt(means.reduce((a,b)=>a+(b-mo)**2,0)/groups);
  $('n-out').textContent=`n=${nn}; theoretical σ=√(0.25/n)=${sd.toFixed(4)}; sample σ=${ms.toFixed(4)}; sample mean≈${mo.toFixed(3)}`;}
 if($('x0')){const f=x=>x**3-2*x+2,fp=x=>3*x*x-2,px=v=>30+(v+2.5)/5*540,py=v=>270-(Math.max(-0.9,Math.min(8,v))/8)*230;
  let x=+$('x0').value,lines='',dots='',list=[x];for(let i=0;i<8&&Math.abs(x)<=3;i++){const y=f(x),d=fp(x);if(Math.abs(d)<1e-6)break;const xn=x-y/d;lines+=path([[px(x),py(y)],[px(xn),270]],'#bd6029','4 4');dots+=`<circle cx="${px(x)}" cy="${py(y)}" r="5" fill="#bd6029"/>`;x=xn;list.push(x);}
  const curve=[];for(let t=-2.5;t<=2.51;t+=.05)curve.push([px(t),py(f(t))]);
  $('newton-svg').innerHTML=axes(300,270)+path(curve,'#086a67')+lines+dots+'<text x="30" y="25">Newton iteration for f(x)=x³−2x+2: each tangent\'s zero is the next iterate</text>';
  const tail=list.slice(0,5).map(v=>v.toFixed(3)).join(' → '),y4=list.length>4?f(list[4]):f(list[list.length-1]);
  $('x0-out').textContent=`iterates: ${tail}${list.length>5?' → …':''}; f(x₄)=${y4.toFixed(4)}`;}
 if($('ea')){const aa=+$('ea').value,bb=+$('eb').value,dd=+$('ed').value,T=aa+dd,R=Math.sqrt((aa-dd)**2+4*bb*bb),l1=(T+R)/2,l2=(T-R)/2;
  const cx=170,cy=160,s=42,pX=(x,y)=>[cx+x*s,cy-y*s];
  let v1=[bb,l1-aa];if(Math.hypot(v1[0],v1[1])<1e-9)v1=[1,0];const n1=Math.hypot(v1[0],v1[1]),u1=[v1[0]/n1,v1[1]/n1],u2=[-u1[1],u1[0]];
  const circle=[],ellipse=[];for(let i=0;i<=60;i++){const t=i/60*2*Math.PI,x=Math.cos(t),y=Math.sin(t);circle.push(pX(x,y));ellipse.push(pX(aa*x+bb*y,bb*x+dd*y));}
  $('eigen-svg').innerHTML=path(circle,'#5f7470','6 5')+path(ellipse,'#086a67')+path([pX(-l1*u1[0],-l1*u1[1]),pX(l1*u1[0],l1*u1[1])],'#bd6029')+path([pX(-l2*u2[0],-l2*u2[1]),pX(l2*u2[0],l2*u2[1])],'#bd6029','4 4')+'<text x="30" y="25">Gray dashed: unit circle; green solid: its image (ellipse); orange: eigen-directions, length=λ</text>';
  $('e-out').textContent=`A=[[${aa.toFixed(1)},${bb.toFixed(1)}],[${bb.toFixed(1)},${dd.toFixed(1)}]]; λ₁=${l1.toFixed(3)}, λ₂=${l2.toFixed(3)}; det=${(aa*dd-bb*bb).toFixed(3)}=λ₁λ₂; area scale=|det|=${Math.abs(aa*dd-bb*bb).toFixed(3)}`;}
}
for(const el of document.querySelectorAll('input[type=range]'))el.addEventListener('input',render);render();
// Print expand/restore logic is inlined in every page template; this file only renders the labs.
'''
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
