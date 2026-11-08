"""English edition atlas builder: classification index, staged curriculum, concept checklist.

Generates:
  - reference/classification.en.html   (official MSC2020 data, English chrome)
  - NN-*/curriculum.en.html            (staged L0–L4 routes per module)
  - reference/curriculum.en.html       (overview)
  - reference/concepts.en.html         (self-check list, data from concepts.en.json)

Reads assets/course.en.json (titles/lesson counts) and assets/concepts.en.json.
Never touches Chinese pages. Run after tools/build_course_en.py:
  python tools/extend_atlas_en.py
"""
from pathlib import Path
import csv
import html
import json
import re

root = Path(__file__).resolve().parents[1]
E = html.escape

course = json.loads((root / 'assets/course.en.json').read_text(encoding='utf-8'))
n_lessons = sum(len(m[5]) for m in course)

rows = list(csv.DictReader((root / 'assets/msc2020.csv').open(encoding='latin1'), delimiter='\t'))
codes = [r['code'] for r in rows]
assert len(codes) == len(set(codes))
tex = (root / 'assets/msc2020.tex').read_text(encoding='utf-8')
assert set(re.findall(r'\\label\{([^}]+)\}', tex)) == set(codes)
major = [r for r in rows if re.fullmatch(r'\d{2}-XX', r['code'])]
middle = [r for r in rows if re.fullmatch(r'\d{2}[A-Z]xx', r['code'])]
general = [r for r in rows if re.fullmatch(r'\d{2}-\d{2}', r['code'])]
leaves = [r for r in rows if re.fullmatch(r'\d{2}[A-Z]\d{2}', r['code'])]
assert len(rows) == len(major) + len(middle) + len(general) + len(leaves)
count = {'total': len(rows), 'major': len(major), 'middle': len(middle),
         'subject_leaf': len(leaves), 'general_leaf': len(general)}
(root / 'assets/classification-audit.json').write_text(json.dumps(count, indent=2), encoding='utf-8')

printjs = ("<script>'use strict';let printed=[];"
           "addEventListener('beforeprint',()=>{printed=[...document.querySelectorAll('details:not([open])')];"
           "printed.forEach(d=>d.open=true)});"
           "addEventListener('afterprint',()=>{printed.forEach(d=>d.open=false);printed=[]});</script>")


def page(title, body, zh=None, module=False):
    """Page shell. module=True is for NN-*/curriculum pages (reference links get
    the ../reference/ prefix); otherwise the page lives inside reference/ itself."""
    r = '../reference/' if module else ''
    lang = f'<a href="{zh}">中文</a>' if zh else ''
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title>'
            f'<meta name="description" content="{E(title)}: a reference page (classification '
            'index, staged curriculum, or concept checklist) of Understanding Mathematics. '
            'Works offline.">'
            f'<link rel="stylesheet" href="../assets/style.css"></head><body><main>'
            f'<nav><a href="../index.en.html">Mathematics Atlas</a>'
            f'<a href="{r}classification.en.html">Classification</a>'
            f'<a href="{r}curriculum.en.html">Staged Curriculum</a>'
            f'<a href="{r}concepts.en.html">Concepts</a>{lang}</nav>'
            f'{body}</main>{printjs}</body></html>')


# --------------------------------------------------------- classification index
# Official descriptions are preserved verbatim; the chrome is translated.
index = ('<header><p class="tag">MSC2020 / FULL SOURCE INDEX</p>'
         '<h1>Index of Mathematics Research Classifications</h1>'
         '<p>This page keeps the official English classification names and descriptions as '
         'published; nothing here is retranslated.</p></header>')
index += (f'<section class="panel"><h2>Scope and Verification</h2>'
          f'<p>All {len(rows):,} records from the officially downloaded CSV are included, and '
          f'the TeX label set was verified to match exactly: {len(major)} major classes, '
          f'{len(middle)} middle classes, {len(leaves):,} subject leaf entries, and '
          f'{len(general)} general leaf entries. The general entries cover surveys, history, '
          'textbooks, software, and the like; they are not separate branches of knowledge.</p>'
          '<p>The official landing page states 63 / 529 / 6,022; the currently downloaded file '
          'counts differently. This page reports the counts of the downloaded file. "Complete" '
          'here means full code-level coverage of the downloaded CSV and TeX — not a claim '
          'that mathematics admits one permanently complete classification.</p>'
          f'<p>A classification index is not a list of finished lessons. The authored lessons '
          f'remain at {n_lessons}; most research topics are unwritten.</p></section>')
index += ('<section class="panel"><label for="search"><b>Filter by code or English '
          'keyword</b></label><input id="search" type="search" placeholder="e.g. 11A / prime '
          '/ topology" style="display:block;width:100%;padding:12px;font:inherit">'
          '<output id="search-count" aria-live="polite">Type a keyword to search all '
          'entries</output><p>Searching expands the matching entries. Clear the box to browse '
          'level by level, major class by middle class. When using the browser\'s find, '
          'expand the relevant major class first.</p></section><div id="tree">')
for m in major:
    prefix = m['code'][:2]
    index += (f'<details class="major panel" id="{m["code"]}"><summary><b>{m["code"]} · '
              f'{E(m["text"])}</b></summary>')
    g = [r for r in general if r['code'].startswith(prefix)]
    index += '<details class="minor"><summary>General entries: textbooks, surveys, history, software, etc.</summary>'
    for r in g:
        index += f'<p class="entry" id="{r["code"]}"><b>{r["code"]}</b> {E(r["description"])}</p>'
    index += '</details>'
    for sub in [r for r in middle if r['code'].startswith(prefix)]:
        index += (f'<details class="minor" id="{sub["code"]}"><summary><b>{sub["code"]} · '
                  f'{E(sub["text"])}</b></summary>')
        for r in leaves:
            if r['code'].startswith(sub['code'][:3]):
                index += (f'<p class="entry" id="{r["code"]}"><b>{r["code"]}</b> '
                          f'{E(r["description"])}</p>')
        index += '</details>'
    index += '</details>'
index += r'''</div><footer><p>Sources: <a href="https://msc2020.org/">MSC2020</a>, by Mathematical Reviews and zbMATH. <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>. This page rearranges the CSV into a tree index; the original English content is preserved, with usage notes and a count audit added. Source files: <a href="../assets/msc2020.csv">CSV</a>, <a href="../assets/msc2020.tex">TeX</a>.</p></footer>
<script>
'use strict';const input=document.getElementById('search');let timer;
// Pre-index lowercased text once at startup to avoid re-reading textContent per keystroke (6600+ entries).
const majors=[...document.querySelectorAll('.major')].map(m=>({el:m,txt:m.querySelector('summary').textContent.toLowerCase(),subs:[...m.querySelectorAll('.minor')].map(s=>({el:s,txt:s.querySelector('summary').textContent.toLowerCase(),leaves:[...s.querySelectorAll('.entry')].map(e=>({el:e,txt:e.textContent.toLowerCase()}))}))}));
function filter(){const q=input.value.toLowerCase().trim();const exact=/^\d{2}[a-z]\d{2}$|^\d{2}-\d{2}$/.test(q);let matched=0;
for(const major of majors){
 const majorMatch=q&&major.txt.includes(q);let majorVisible=false;
 for(const sub of major.subs){
 const subMatch=q&&sub.txt.includes(q);let visible=false;
 for(const leaf of sub.leaves){const hit=exact?leaf.el.id.toLowerCase()===q:(!q||majorMatch||subMatch||leaf.txt.includes(q));leaf.el.hidden=!hit;if(hit){visible=true;matched++;}}
 sub.el.hidden=!visible;sub.el.open=!!q&&visible;majorVisible=majorVisible||visible;}
 major.el.hidden=!majorVisible;major.el.open=!!q&&majorVisible;}
 document.getElementById('search-count').textContent=q?`Matched ${matched} leaf entries (including matches on parent class names)`:'All classes shown; expand level by level';}
input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(filter,120)});
function revealHash(){if(!location.hash)return;let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)))}catch(e){return}if(target){for(let p=target.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;if(target.tagName==='DETAILS')target.open=true;requestAnimationFrame(()=>target.scrollIntoView());}}
window.addEventListener('hashchange',revealHash);revealHash();
</script>'''
(root / 'reference/classification.en.html').write_text(
    page('MSC2020 Full Classification Index · Understanding Mathematics', index,
         zh='classification.html'), encoding='utf-8')

# ---------------------------------------------------------- staged curriculum
paths = {
 '00-preparation': [
  'Integers, rational numbers, the four operations, and orders of magnitude; checking results with units and estimation',
  'Fractions, ratios, percentages, powers, radicals, and logarithms; explaining when each rule of exponents applies',
  'Linear and quadratic equations, inequalities, domains, graphs, and composition; setting up equations from word problems',
  'Trigonometric functions, radian measure, identities, exponential and logarithmic functions; moving fluently among symbols, graphs, and language',
  'Capstone transition: dimensions, an intuition for limits, and vectors; complete the placement diagnostics for analysis and linear algebra and enter the main tracks'],
 '01-foundations': [
  'Sets, maps, propositions, quantifiers, and counterexamples; distinguishing converse, inverse, and contrapositive',
  'Direct proof, contradiction, induction, recursion, equivalence relations, and quotient sets; writing complete proofs',
  'Naive set theory, cardinality, countability, relations, and first-order languages; separating syntax from semantics',
  'Axiomatic set theory, model theory, computability, and formal proof; examining the hypotheses of the completeness and incompleteness theorems',
  'A seminar topic in logic: reconstruct a theorem\'s proof, compare models and methods, and pose a small question under advisor feedback'],
 '02-algebra': [
  'Manipulating equations, polynomials, factorization, and complex numbers; checking the solution set after every step',
  'Groups, subgroups, homomorphisms, quotient groups; rings, ideals, quotient rings; a first look at field extensions',
  'Group actions, Sylow theory, modules, finite fields, and Galois theory; connecting equations with symmetry',
  'Commutative algebra, representation theory, categories and homological algebra; add Noetherian conditions, chain complexes, and derived functors by track',
  'Choose representation theory, commutative algebra, or another algebraic track and reproduce the core lemmas of a survey paper; K-theory and similar topics form separate long-term routes'],
 '03-number-theory': [
  'Divisibility, gcd, the Euclidean algorithm, congruences, and primes; giving elementary arguments',
  'The Chinese Remainder Theorem, the theorems of Fermat and Euler, multiplicative order, quadratic residues, and simple Diophantine equations',
  'Quadratic reciprocity, continued fractions, and arithmetic functions; branch into analytic or algebraic tracks after analysis and abstract algebra',
  'Analytic track: Dirichlet series and the distribution of primes; algebraic track: number fields, rings of integers, ideals, and local fields',
  'Pick a small topic in analytic or algebraic number theory and re-derive known results; arithmetic geometry additionally requires algebraic geometry'],
 '04-linear-algebra': [
  'Vectors, linear combinations, systems of equations, elimination, and matrices; explaining the geometry',
  'Vector spaces, bases, dimension, kernels and images, rank–nullity; proving in the language of maps',
  'Determinants, eigenvalues, diagonalization, inner products, orthogonal projection, and least squares',
  'The spectral theorem, singular value decomposition, Jordan form, tensors and multilinear algebra; separating exact algebra from numerical conditioning',
  'Choose a topic in spectral theory, matrix analysis, or tensors; reproduce results and build edge-case counterexamples, linking to functional or numerical analysis'],
 '05-geometry': [
  'Euclidean axioms, similarity, congruence, circles, and coordinates; moving from pictures to proofs',
  'Analytic geometry, affine and projective viewpoints, convexity; understanding invariants under different transformations',
  'Curves and surfaces, curvature, manifolds and tangent spaces; adding multivariable calculus and topology',
  'By track: Riemannian geometry and connections, algebraic geometry and varieties/schemes, or convex geometry; the specialized tracks need not be sequential',
  'Choose a geometry topic: rebuild a local-to-global proof or one concrete example; read a modern paper and state its dependencies'],
 '06-analysis': [
  'Functions, limits, continuity, derivatives, and integrals; building intuition from graphs and numbers',
  'Completeness of the reals, sequences and series, rigorous limits, and the theorems of calculus; writing ε-δ proofs',
  'Multivariable calculus, metric spaces, uniform convergence, Lebesgue measure and integration, complex analysis',
  'Functional analysis, operator theory, Fourier and harmonic analysis; extending into special functions, potential theory, or several complex variables by topic',
  'Choose a small analysis topic and check the hypotheses of every limit interchange; reproduce one nontrivial theorem together with a counterexample'],
 '07-topology': [
  'Open and closed sets, continuity, homeomorphisms, and connectedness; making examples in concrete spaces',
  'Metric spaces, topological spaces, compactness, products and quotients, separation; going beyond rubber-sheet intuition',
  'The fundamental group, covering spaces, homotopy, and homology; learning to separate spaces by algebraic invariants',
  'Cohomology, manifolds, differential and geometric topology; adding algebra or differential geometry by track',
  'Select a topic such as low-dimensional topology or homotopy theory; carry out computations in concrete spaces and present a proof from a paper'],
 '08-combinatorics': [
  'The multiplication and addition principles, permutations and combinations, inclusion–exclusion, the pigeonhole principle, and basic graph theory',
  'Recurrences, generating functions, trees, connectivity, matchings, planar graphs, and basic graph algorithms',
  'Extremal methods, the probabilistic method, Ramsey ideas, and combinatorial designs; practicing both constructions and counting proofs',
  'Specialize by track in algebraic combinatorics, spectral graph theory, additive combinatorics, or extremal graph theory; add the matching algebra and probability',
  'Rebuild an extremal bound or construction and analyze its optimality; explore small cases computationally and write a rigorous proof'],
 '09-probability': [
  'Sample spaces, events, conditional probability, independence, and Bayes\' rule; from model to computation',
  'Random variables, distributions, expectation, variance, joint distributions, intuition for conditional expectation, and the basic limit theorems',
  'Measure-theoretic probability, modes of convergence, proofs of the law of large numbers and the central limit theorem; stating integrability conditions',
  'Martingales, Markov processes, Brownian motion, stochastic integrals; by track, large deviations or stochastic differential equations',
  'Study one stochastic model: prove bounds, simulate, and check against theory; explain why empirical results cannot replace proofs'],
 '10-statistics': [
  'Describing distributions, sampling, bias, correlation and causation; reading and questioning statistical claims',
  'Estimation, confidence intervals, hypothesis testing, linear regression, experimental design; explaining uncertainty',
  'Likelihood, sufficiency, asymptotic theory, generalized linear models, Bayes and decision theory',
  'Specialize by track in nonparametrics, high dimensions, causal inference, time series, or computational statistics; checking identifiability and model assumptions',
  'Reproduce a methodological study: theoretical conditions, simulations, and validation on real data; analyze coverage, bias, and failure modes'],
 '11-differential-equations': [
  'Differential equations, initial values, exponential growth, direction fields, equilibria, and simple numerical solutions',
  'First- and second-order linear ODEs, separable equations, systems, existence and uniqueness, phase planes, stability, and a first look at difference equations',
  'The heat/wave/Laplace equations, boundary and initial conditions, Fourier methods, and a first look at variational and weak solutions',
  'By track: nonlinear PDE, dynamical systems, bifurcations and chaos, ergodic theory, integral or difference equations',
  'Choose one concrete equation and prove a result on existence, estimates, or long-time behavior; check the solution space and boundary conditions'],
 '12-numerical': [
  'Rounding, truncation, errors and residuals, bisection and Euler\'s method; testing whether a computation is trustworthy',
  'Interpolation, quadrature, solving linear systems, iterative methods, condition numbers and stability',
  'Numerical ODEs/PDEs, sparse matrices, eigenvalue algorithms, error estimates and rates of convergence',
  'Specialize by track in finite elements, finite volumes, spectral methods, adaptive algorithms, or high-performance computing',
  'Reproduce an algorithms paper: derive error bounds and design reproducible benchmarks; report failures, complexity, and implementation gaps'],
 '13-optimization': [
  'Objectives, variables, constraints, feasible regions, local vs. global optima; simple gradient iterations',
  'Convex sets and functions, linear programming, duality, optimality conditions, and when KKT applies',
  'Integer programming, combinatorial optimization, nonlinear optimization, dynamic programming; basics of variational methods and control; games and interactive decision-making',
  'By track: convex analysis, stochastic optimization, optimal control, robust control, or scheduling and operations research',
  'Prove convergence or control properties under explicit assumptions; compare performance and failure ranges on benchmark problems'],
 '14-computation': [
  'Algorithms, complexity, and information; preparing the tools of logic, combinatorics, and probability',
  'Automata, formal languages, computability, reductions, P/NP, and basic algorithm design',
  'By track: complexity theory, entropy and mutual information, channel coding, error-correcting codes, and modern security definitions',
  'Specialize in randomized algorithms, complexity, coding, or cryptography; the cryptography track also needs number theory and probabilistic security reductions',
  'Reproduce an algorithmic bound, a coding construction, or a security proof; distinguish experimental speedups from asymptotic gains, and empirical security from proofs'],
 '15-mathematical-physics': [
  'Dimensions, Newton\'s equations, oscillations, and conservation; separating mathematical variables from physical interpretation',
  'Analytical mechanics, continua, and the basic field equations; adding vector calculus and ODEs/PDEs',
  'By track: Hamiltonian systems, fluids/elasticity, heat and electromagnetism, or the mathematical foundations of quantum theory or relativity',
  'Choose tools from spectral methods, differential geometry, statistical mechanics, or nonlinear PDE; each physics track has its own prerequisites',
  'Reproduce a mathematical result within one explicit model and state its physical limits; astrophysics and geophysics require extra domain knowledge'],
 '16-modeling': [
  'Problem definition, variables, units, assumptions, validation, and sensitivity; building simple, checkable models',
  'Nondimensionalization, parameter estimation, growth/network/stochastic models; separating fitting from extrapolation',
  'By track: biological systems, economics and games, financial stochastic models, networks, or social systems',
  'Identifiability, uncertainty quantification, model comparison, and mechanism testing; adding the matching domain knowledge and causal methods',
  'Complete a project on open data or a mechanism model; external validation, failure analysis, reproducible code, and independent review are all required'],
 '17-history': [
  'Number systems, axioms, definitions, proofs, and counterexamples; respecting different spaces and hypotheses',
  'The conceptual development of classical geometry, algebra, and calculus; distinguishing modern restatements from historical intent',
  'Infinity, rigorization, formalization, and the foundational crises; reading original sources and reliable historical scholarship',
  'By track: philosophy of mathematics, historiography, concept learning, and research design in mathematics education',
  'Pose a narrow question from primary sources or educational data; publish the evidence chain, counter-interpretations, and the limits of the method'],
}
levels = ['L0 · First Contact and Intuition', 'L1 · Undergraduate Core',
          'L2 · Advanced Undergraduate and Proof Training', 'L3 · Graduate Topics',
          'L4 · Research Training']
checks = [
 'Can explain the key terms, carry out the computations independently, and give examples and counterexamples.',
 'Can choose a method without hints, check the hypotheses, and write complete solutions.',
 'Can reconstruct the proofs of the key theorems, see where a hypothesis cannot be dropped, and handle synthesis problems.',
 'Can read textbooks or survey notes, fill in the omitted steps, and produce a verifiable topic report.',
 'Can read papers in a chosen direction, reproduce known results, and accept peer feedback; whether original results emerge is decided by real research.']
assert set(paths) == {m[0] for m in course}, 'curriculum paths and course modules disagree'

overview = (f'<header><h1>From Foundations to Research Training: Curriculum Overview</h1>'
            '<p>This is course design, not a claim that "all lessons are written". The '
            f'{n_lessons} introductory lessons are ready to read; the advanced units on this '
            'page are not yet written. The 6,000-plus records in the classification index are '
            'not 6,000 unrelated courses either.</p></header>')
overview += ('<section class="panel"><h2>How "Mastery" Is Understood Here</h2>'
             '<p>There is no recognized "graduation line for masters of mathematics". This '
             'project sets the checkable upper bound at research preparation and initial '
             'research training in one direction: reading papers, filling in proofs, '
             'reproducing results, posing small questions, and accepting feedback. The '
             'branches of mathematics span widely; one usually builds a broad foundation and '
             'then goes deep in a few directions.</p>'
             '<p>Promotion is based on evidence from work and problem-solving, not on browsing '
             'progress. Finishing a lesson does not automatically mean mastery, and finishing '
             'this overview does not mean finishing a textbook.</p>'
             '<h2>Completion Criteria for Authored Lessons</h2>'
             '<p>Each topic should have: explicit prerequisites and goals, conceptual '
             'intuition, precise definitions, theorem hypotheses, the necessary proofs, at '
             'least one fully worked example, basic and transfer exercises, hints and complete '
             'solutions, common mistakes, and credible sources. Topics that suit '
             'visualization additionally get manipulable figures, with a note that figures do '
             'not replace proofs.</p></section>'
             '<h2>Staged Routes by Direction</h2><div class="grid">')
for folder, title, subs, pre, source, lessons in course:
    text = (f'<header><h1>{E(title)}: Staged Course Route</h1>'
            f'<p>This branch currently has {len(lessons)} introductory lessons. Each level '
            'below bundles several topics awaiting development; two finished lessons do not '
            'mean L0 or L1 is complete.</p>'
            f'<p>Entry prerequisites: {E(pre)}</p>'
            '<a href="index.en.html">Read the current lesson texts</a></header>')
    for i, topic in enumerate(paths[folder]):
        text += (f'<article><p class="tag">Planned / not counted toward finished '
                 f'lessons</p><h2>{levels[i]}</h2><p>{E(topic)}</p>'
                 f'<h3>Stage Assessment</h3><p>{checks[i]}</p>')
        if i > 0:
            text += ('<p>Before entering: pass the previous level\'s independent '
                     'problem-solving or report assessment; when crossing into another '
                     'direction, also add the corresponding analysis, algebra, probability, '
                     'or domain knowledge.</p>')
        text += '</article>'
    text += ('<footer><p>Do not skip levels blindly by checklist. After each study session, '
             'record which problems you can solve unaided and which proofs still need hints, '
             'then choose the next lesson. In the research stage, join a reading group or '
             'seek professional guidance.</p></footer>')
    (root / folder / 'curriculum.en.html').write_text(
        page(f'{title}: Staged Curriculum · Understanding Mathematics', text,
             zh='curriculum.html', module=True), encoding='utf-8')
    overview += (f'<a class="card" href="../{folder}/curriculum.en.html"><h3>{E(title)}</h3>'
                 '<p>L0 Introduction → L1 Core → L2 Proofs → L3 Topics → L4 Research '
                 'Training</p></a>')
overview += ('</div><footer><p>These are pedagogical stages, not a unified university '
             'standard; the concrete order will shift with the direction and with your study '
             'feedback.</p></footer>')
(root / 'reference/curriculum.en.html').write_text(
    page('Staged Curriculum Overview · Understanding Mathematics', overview,
         zh='curriculum.html'), encoding='utf-8')

# ------------------------------------------------------------ concept checklist
concepts = json.loads((root / 'assets/concepts.en.json').read_text(encoding='utf-8'))
assert set(concepts) == {m[0] for m in course}, 'concepts.en.json module keys disagree with the course data'
cp = (f'<header><p class="tag">CONCEPT CHECKLIST</p><h1>Core Concept Self-Check List</h1>'
      f'<p>One group of items for each of the {n_lessons} lessons, self-checked in the sense '
      'of can explain / can derive / can transfer: answer closed-book first, tick only once '
      'you can do it, and revisit after 1 day, 3 days, and 7 days to redo. Ticks are stored '
      'only in this browser (localStorage); nothing is uploaded or written to the '
      'repository.</p><p id="total" aria-live="polite"></p>'
      '<button id="reset" type="button">Clear all check marks</button></header>')
for folder, title, subs, pre, source, lessons in course:
    n = concepts[folder]
    assert len(n) == len(lessons), f'{folder}: concept entry count disagrees with lesson count'
    cp += (f'<section class="panel" data-module="{folder}"><h2>{E(title)} '
           f'<span class="muted" data-count></span></h2>'
           f'<p><a href="../{folder}/index.en.html">Branch page</a> · '
           f'<a href="../{folder}/curriculum.en.html">Staged route</a></p>')
    for lesson, c in zip(lessons, n):
        items = ''.join(
            f'<li><label><input type="checkbox" id="{folder}-{c["file"]}-{i}"> {E(t)}'
            f'</label></li>' for i, t in enumerate(c['items'], 1))
        cp += (f'<div class="concept"><h3><a href="../{folder}/lessons/{c["file"]}.en.html">'
               f'{int(c["file"]):02d} · {E(lesson[0])}</a> '
               f'<span class="muted" data-count></span></h3><ul>{items}</ul></div>')
    cp += '</section>'
cp += r'''<footer><p>The list covers the __N__ authored lessons; the higher goals of L1–L4 are in the <a href="curriculum.en.html">staged curriculum overview</a>. A tick is a self-assessment snapshot, not mastery: the standard is whether you can redo the item closed-book, state its conditions, and give an example of your own.</p></footer>
<script>
'use strict';
const KEY='math-concepts-en-v1';let state={};
try{state=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}};
function refresh(){let total=0,done=0;
for(const sec of document.querySelectorAll('[data-module]')){let sd=0,st=0;
for(const d of sec.querySelectorAll('.concept')){let ld=0,lt=0;
for(const b of d.querySelectorAll('input')){b.checked=!!state[b.id];total++;st++;lt++;if(b.checked){done++;sd++;ld++}}
d.querySelector('[data-count]').textContent=ld+'/'+lt}
sec.querySelector('[data-count]').textContent=sd+'/'+st}
document.getElementById('total').textContent='Total progress: '+done+' / '+total+' items'}
for(const b of document.querySelectorAll('.concept input'))b.addEventListener('change',()=>{state[b.id]=b.checked;save();refresh()});
document.getElementById('reset').addEventListener('click',()=>{if(confirm('Clear all check marks?')){state={};save();refresh()}});
refresh();
</script>'''
cp = cp.replace('__N__', str(n_lessons))
(root / 'reference/concepts.en.html').write_text(
    page('Core Concept Self-Check List · Understanding Mathematics', cp, zh='concepts.html'),
    encoding='utf-8')

print('English atlas built: classification', count, '| staged routes:', len(paths),
      '| lessons:', n_lessons)
