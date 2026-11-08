# Knowledge-Completeness Review (2026-11-07)

> **Fix log (completed the same day, 2026-11-07)**: A1–A13 all fixed (erroneous text, missing conditions, lesson order, and prerequisite declarations); **31 new lessons** (96→127), covering all 8 repository-wide gaps of B1 and the entry-level gaps of B2 for each module; every B3 prerequisite break resolved with a new lesson or an in-text pointer; all 14 cross-links of section C landed; the Notation Reference went from 9 to 37 entries; two new lab experiments, "Sampling Distributions (CLT)" and "Newton Iteration" (4→6); RESOURCES gained advanced-reading lists for five directions (every link verified); verify_course.py's count assertions now read values dynamically; branch-page subfield copy corrected. `python tools/build_course.py && python tools/extend_atlas.py && python tools/verify_course.py` all green.
>
> **Second pass (same day, "did everything, including the optional items")**: **12 more lessons** (127→139), landing every direction the review had marked "optional/downgrade/deferred" — quadratic residues (03-07), a first look at tensors (04-09), parallel projection and the cross-ratio (05-09), the fundamental group (07-06), Brownian motion intuition (09-09), bifurcations/discrete chaos/ergodic theory (11-08/09/10), game theory (13-06), continua (15-10), feedback loops (16-07), reading theorems and writing proofs (17-06); a 7th experiment added, "Circle to Ellipse: the Eigenvalues Are the Semiaxes", plus a baseline axis for the binomial chart; `<meta name="description">` added site-wide; RESOURCES now also generates an HTML version (`reference/resources.html`) for branch pages to link; `widgets.js` now loads only on lab pages, with the print/expand logic inlined on each page. At this point everything the review listed (including the optional items and the actionable CHECKLIST leftovers) is done; the only holdout is the TeX literals of official source data inside classification (deliberately left as-is).
>
> **Additional fixes (2026-11-08, surfaced while translating the English edition; both language versions updated in sync)**: ① 00-06 worked-example typo 8^(2/3)=(8^(1/3))²=3²=4 corrected to 2²=4; ② 05-09 a one-character typo in the Chinese term for "projective" corrected, so the cross-ratio is now properly called the "projective fingerprint" of a quadruple; ③ 11-08: the bifurcation of the logistic x′=rx−x² at r=0 renamed from "supercritical" to **transcritical** (the two equilibria exchange stability; the negative equilibrium r still exists and is unstable for r<0, so the solution's "only 0 exists" was corrected as well), with `assets/concepts.json` updated to match; ④ 12-03's checklist item now ties the one-step factor (1−2h) to y′=−2y (the earlier wording conflated it with the lesson's y′=y example, whose factor is 1+h); ⑤ 14-05 "21≡1 mod 20" normalized to "(mod 20)" notation; ⑥ 14-06 the repetition code's "efficiency 1/3" unified to "code rate", matching the Hamming-code wording; ⑦ 15-07 "fundamental frequency πc" now marked as an angular frequency (πc is an angular frequency, not cycles per unit time). Also: A6's "o=0" was re-checked and is correct — o is precisely the increment symbol in the fluxion argument of 17-03; left as-is.

Review method: all 96 lessons across the 18 modules checked one by one (with `assets/course.json` as the source of truth); every worked example and solution value recomputed; both generators (`tools/build_course.py`, `tools/extend_atlas.py`), the five reference-layer pages, the hand-written docs (README/RESOURCES/CHECKLIST/MISSION/NOTES), and the verification scripts all read through. My own re-check plus cross-validation against three independent review passes.

## Overall Assessment

- **Correctness is at a high level**: recomputing the worked examples and exercise answers of all 96 lessons surfaced only a handful of genuine errors (see section A), with no widespread computational mistakes; the mathematics of the four lab experiments (secant slope 2+h, Binomial(10,p), Euler factor 1−2h) is all correct.
- **The framing is honest**: the staged curriculum route states up front that planned items "are not counted among completed lessons"; the MSC counts report the measured values; claims that run ahead of the content carry disclaimers.
- **The core problem is knowledge completeness**, on four levels:
  1. repository-wide knowledge gaps (partial derivatives, the normal distribution, eigenvalues, and so on, silently used in many lessons but never taught anywhere);
  2. module-level gaps between "promised subfields vs. actual lessons" (worst in 04/09/11/14/15);
  3. the stale "36 lessons" count leaking into 4 generated pages and contradicting the "96 lessons" figure on the very same pages;
  4. a reference layer that is far too thin (the Notation Reference has only 9 entries).

---

## A. Correctness Issues That Must Be Fixed

Severity: **High** = factual error or self-contradiction, user-visible; **Medium** = flawed condition or argument that will mislead a careful reader; **Low** = wording or lesson-order issues.

### High

- **A1 Stale "36 lessons" count**: hard-coded in 4 places in `tools/extend_atlas.py` (L27, L178, L198, L207) plus 1 README paragraph (L236). Generated output: `reference/classification.html` "the current tutorial body still has 36 lessons", `reference/curriculum.html` "the 36-lesson introductory body is already readable", `reference/concepts.html` "corresponding to 36 lessons" plus the footer "the checklist covers the current 36 body lessons", README.md L140 "36 lessons item by item" — while L139 of the same document says "the current body still has 96 lessons" (dynamically generated), **two numbers contradicting each other on the same page**. concepts.json in fact covers all 96 lessons. Fix: generate all of these dynamically with `sum(len(m[-1]) for m in course)` (L235 already sets the precedent).
- **A2 06-05 worked example contradicts itself on the geometric-series partial sums** (course.json L339): "the partial sums of Σ(1/2)ⁿ are 1−(1/2)ⁿ, which tend to 2". If the sum starts at n=0 (consistent with this lesson's statement that the sum is 1/(1−r)), the partial sums should be 2−(1/2)ⁿ; and 1−(1/2)ⁿ tends to 1. Pick one or the other.
- **A3 11-02 worked example argues invalidly** (L566): "if two solution curves intersected, the intersection point would be assigned two slopes, contradicting 'the slope is uniquely determined at each point'". At an intersection point the two solution curves have **the same** slope f(t₀,y₀) — there are no "two slopes"; two distinct curves can perfectly well be tangent at the same point (e.g. y=t² and y=t³ at t=0). Correct argument: two solution curves both passing through (t₀,y₀) are two solutions of the same initial value problem, so by existence and uniqueness they must be the same curve.

### Medium

- **A4 09-03 retest exercise assumes conditional independence without declaring it** (L472–473): "independent retests" and "multiplying independent evidence" actually require **the two tests to be independent given the disease status**; without conditional independence the second test carries no new information, and the posterior could not rise from 1/6 to 0.8. The arithmetic 0.0098/(0.0098+0.0025)≈0.8 is itself correct.
- **A5 10-04 confidence interval lacks conditions + s is disconnected from its definition** (L528, L531): (1) "when σ is known, X̄±1.96σ/√n is a 95% confidence interval" also needs "a normal population, or n large enough (CLT)"; (2) the solution swaps in the "sample standard deviation s" at the t quantile, but the only variance defined anywhere in the course is the population variance with division by n (10-02) — computing s that way systematically underestimates, which is exactly the reason for dividing by n−1, and the text never mentions it.
- **A6 17-03's restatement of the epsilon–delta definition drops the punctured condition** (L824): it says "|f(x)−L|<ε can be controlled by |x−a|<δ", missing the 0<|x−a|; read literally, no function with f(a)≠L would have a limit, and the lesson's own topic (the difference quotient is undefined at o=0) depends precisely on puncturing. The original statement in 06-01 (L10) has 0<|x−a|<δ; it was dropped when 17-03 restated it.
- **A7 06-05 solution states the 1/n² grouping bound in the wrong direction** (L341): "each group has at most 2ᵏ terms **no smaller than** 1/4ᵏ, so the group sum is at most 1/2ᵏ" — for n∈[2ᵏ,2ᵏ⁺¹−1] each term 1/n² ≤ 1/4ᵏ, so it should read "**no larger than**"; a lower bound yields no upper bound.
- **A8 Partial-derivative notation used without ever being defined**: 11-02 (L565) "∂f/∂y is continuous"; 15-05 (from L748 on) uses ∂²u/∂t², ∂²u/∂x², and the two-variable chain rule throughout — no lesson anywhere in the repository introduces functions of two variables or partial derivatives (see B1-1). Cheapest fix: a footnote; the real cure is the P1 lesson.
- **A9 Untaught operations used inside "verify" steps**: 11-01 (L559) "verify by differentiating to get 10e^(0.1t)" — the differentiation rule for the exponential is never taught in 06; 15-03 (L735) E′=mx′x″+kxx′ uses the chain rule (d(x′²)/dt=2x′x″), not taught in 06; the 11-04 solution (L582) uses integration by parts, and 06 teaches no integration techniques at all. Symptoms of B1-4; at minimum the text should note "this step uses …, developed further in …".
- **A10 Module 16's prerequisite declaration does not match its content** (L759): it declares "algebra, probability; advanced parts require differential equations", yet Lesson 01 (L765) already uses N′=rN and 4 of the 5 lessons substantially depend on 06+11; the declared "probability" goes unused in all 5 lessons. Should read "algebra; requires derivatives (06) and differential equations (11)".

### Low

- **A11 05-04 conic-section definition conditions** (L287): the ellipse is missing "2a>distance between the foci" (otherwise it degenerates into a segment or the empty set); the hyperbola should be "the **absolute value of the difference** is constant, with 0<2a<distance between the foci" (a constant difference yields only one branch); "eccentricity e=c/a" is undefined for the parabola (c does not exist) — give the unified focus/directrix definition first.
- **A12 Tools used silently**: the 03-05 solution (L200, L202) solves 3t≡1 and 2t≡1 (mod m) outright — when a modular inverse exists is taught nowhere in the repository (add Bézout: gcd(a,m)=1); the 03-04 proof idea (L192) "repeated self-multiplication returns to the identity after the group order" is Lagrange's theorem, untaught in 02; 02-05 (L149) and 04-02 (L225) use determinants before determinants are formally defined (04-04) (04-02 is a lesson-ordering issue within the same module; suggest rewording to "the two lines have different slopes").
- **A13 Minor wording/lesson-order items**: 09-06's CLT omits the "finite variance" condition; 10-02's "about 68%" is only a rough rule of thumb for unimodal symmetric data (exact only for the normal); 10-05 is a one-sided p-value without saying so; 11-02's "family of solutions e⁻²ᵗ" drops the arbitrary constant C (should be y=Ce⁻²ᵗ); 11-05's complex-root general solution leans on Euler's formula without giving a source; the 15-04 solution's E=½v²+x⁴/4 silently takes m=1 (every other lesson in the module keeps m explicit); 16-04's nondimensionalization takes v₀ as the velocity scale, which requires v₀≠0; 16-05's "a perfect fit always occurs when the number of points equals the number of parameters" is too strong (the independent variables must also be distinct); 17-01's "the rationals accommodate division of nonzero numbers" should be "accommodate division by a nonzero divisor"; 17-04's use of the sphere as a model of "changing only the parallel postulate" is not rigorous (two great circles meet in two points, violating the other axioms; the rigorous model is elliptic geometry with antipodal points identified) — a note is advisable; 17-04 (L830) "the geometry course's spherical triangles" is a confusing reference — spherical triangles live in 17-02 (this module); 05-Geometry has no such content; 13-02's lesson title is "gradient descent" but the lesson is entirely one-dimensional (f′ rather than ∇f) — suggest renaming it "steepest descent" or stating in the text that the one-dimensional case comes first.

---

## B. Knowledge-Completeness Gaps (Main Focus)

### B1 Repository-Wide Knowledge Gaps (ordered by impact)

| # | Gap | Where used silently | Suggestion |
|---|---|---|---|
| 1 | **Functions of two variables, partial derivatives, gradient** | 11-02 (∂f/∂y), 15-05 (the wave equation throughout), 13-02 (lesson title), 16 (extension directions) | add to 06 a lesson "A First Look at Partial Derivatives and the Gradient" (the shortest path from one variable to two) |
| 2 | **Important distributions (binomial/geometric/Poisson/uniform/exponential/normal)** | 09-02/09-06 coin tossing, the CLT lesson's "tends to the normal", 10-04's 1.96, 10-05's C(20,18), Interactive Lab 3 in labs | add to 09 a "Common Distributions" lesson; the binomial distribution has still never been named in the body, and the normal has never been defined |
| 3 | **Eigenvalues, inner products/orthogonality** | 08-04 "characteristic equation", 11-05 "characteristic equation", 13-02 multidimensional overshoot, 15-02 oscillation ±2i | add two lessons to 04 (see B2) |
| 4 | **Differentiation rules (product/chain), derivatives of exponential/logarithm, integration techniques (substitution/by parts), Mean Value Theorem** | 11-01, 11-04, 15-03 (see A9) | add two lessons to 06 |
| 5 | **Law of sines/law of cosines** | implicitly needed by 05's triangle solving and 15's vector decomposition alike; 00 stops at the unit-circle definitions | add in 00-07 or 05 |
| 6 | **Parametric equations and polar coordinates** | 06's curve discussions; 15's natural language for circular motion | add one lesson in 05/06 |
| 7 | **Binomial theorem** | C(n,k) is taught but (a+b)ⁿ is never expanded; 10-05 uses it directly (and 10's prerequisites do not list 08) | add one lesson to 08 |
| 8 | **Countability/diagonal argument** | 14-04's halting problem uses the diagonal argument while 01's promised "set theory" direction goes untaught; 17's "infinity" is only half taught | add one lesson to 01 (Cantor), serving 14/17 as well |

### B2 Module-Level "Promised vs. Delivered" Gaps

The README branch table's "main subfields" checked against the actual lessons. Advanced topics already covered by a disclaimer are not repeated; only gaps that **belong in the entry layer** are listed:

| Module | Promised subfields with zero lessons | Priority entry-layer additions |
|---|---|---|
| 00 Preparation | **Equations and inequalities** (explicitly listed as a subfield, no lesson; yet homepage diagnostic question ② is already testing equation solving) | add a "Linear Equations and Inequalities" lesson |
| 01 Foundations | Propositional logic (only the universal-proposition lesson touches it); the set theory/countability direction | truth tables and connectives can fold into an existing lesson; one lesson on Cantor's diagonal argument |
| 02 Algebra | Field theory and beyond (already disclaimed) | polynomial division and the Remainder Theorem; group actions/Lagrange (03-04 is waiting) |
| 03 Number Theory | **Diophantine equations** (explicitly listed, no lesson) | one lesson, "Linear Diophantine Equations with Bézout/modular inverses" |
| 04 Linear Algebra | **Eigenvalues; inner products and spectral decomposition; multilinear algebra** (3 of 7 items missing) | two lessons, "Eigenvalues and Diagonalization" + "Inner Products, Projections, and Least Squares" (multilinear can be marked deferred) |
| 05 Geometry | Projective geometry (may be marked deferred) | inscribed angles, solving triangles, parametric equations/polar coordinates |
| 06 Analysis | Real analysis and beyond (already disclaimed) | the two B1-4 lessons; continuous functions can be folded in |
| 07 Topology | Algebraic/differential/geometric topology (already disclaimed) | optional: one lesson on fundamental-group intuition |
| 08 Combinatorics | Extremal combinatorics/design theory/discrete geometry (may be deferred) | binomial theorem; graph coloring/Eulerian circuits |
| 09 Probability | **Stochastic processes; stochastic analysis** | "Common Distributions" + "Random Walks and Markov Chain Intuition"; downgrade stochastic analysis to an outlook |
| 10 Statistics | **Bayesian statistics; experimental design; multivariate and nonparametric statistics** | a Bayesian statistics lesson is easiest (09-03 already has the formulas); fold power/sample size into the testing lesson |
| 11 Differential Equations | 6 of 7 promised items missing (only stability partially delivered) | "Separable Equations" (the largest gap: 11-01/11-03 are both separable yet jump straight to integrating factors) + "Phase Planes and Two-Dimensional Linear Systems" (to make good the "systems need linear algebra" declaration); integral equations/ergodic theory suggested as downgraded to an outlook |
| 12 Numerical | **Interpolation and approximation; numerical linear algebra** | one lesson on interpolation; one on condition numbers and numerical linear algebra |
| 13 Optimization | Integer programming/calculus of variations/optimal control/game theory/scheduling | an introduction to duality and KKT, or a game theory lesson; mark the rest deferred |
| 14 Computation | **Coding theory; cryptography** | an "RSA" lesson (everything from 03's Fermat/Euler is in place; only the multiplicativity of φ is missing) + an "error-correcting codes" lesson (picking up from entropy) |
| 15 Mathematical Physics | **Electromagnetism and optics; heat and statistical physics; the mathematics of quantum theory; relativity and field theory** (4 of 6 missing), with fluids only grazing the wave equation | at least one lesson per direction (Newton's law of cooling = 11's integrating factor; standing waves and discrete frequencies; Coulomb/geometric optics; Galilean transformations need only a 2×2 matrix), or state the deferral explicitly |
| 16 Modeling | **Networks and social systems; systems science** | one lesson on network spread (08's handshaking lemma/trees are in place); one qualitative lesson on feedback loops |
| 17 History & Philosophy | **Philosophy of mathematics; mathematics education and communication**; infinity only half taught | the three schools + incompleteness intuition; a Cantor infinity lesson |

### B3 Summary of Prerequisite-Chain Breaks

(→ the left side is where something is used; the right side is what the repository teaches)

- 11-02 ∂f/∂y → nothing
- 15-05 partial derivatives, two-variable chain rule → nothing
- 11-01 differentiating e^(kt) → 06 never teaches the derivative of the exponential
- 11-04 integration by parts → 06 teaches no integration techniques
- 15-03 chain rule d(x′²)/dt → not taught in 06
- 09-06/10-04/10-05 normal distribution, 1.96 → 09 never defines the normal
- 10-05 C(20,18) → taught in 08, but 10's prerequisites do not list 08
- 03-05 modular inverse → not taught in 03 (Bézout missing)
- 03-04 Lagrange → not taught in 02
- 02-05 det, 04-02 det → only defined in 04-04 (lesson order)
- 16 module prerequisite declaration mismatched (see A10)
- 05-03 the curvature concept sentence uses "rate of change/tangent direction" language (the worked example limits itself to circles and hedges with "general curves require calculus"; low-cost fix: change the defining sentence to κ=central angle/arc length=1/R and point back to 00's definition of radians)

---

## C. Missing Cross-Links (small effort, large payoff)

Current state: the lesson pages have **no cross-module lesson links at all** (the template links only to the previous/next lesson within the module, to labs, and to the glossary); every natural connection is left for the reader to find. Build these first:

1. **03-04 ↔ 14 RSA**: the Fermat/Euler theorems are the entire number-theoretic foundation of RSA, and 14-04 already says "some cryptographic constructions rely precisely on this", yet the two are not linked (resolved once 14 gains its cryptography lessons).
2. **01 ↔ 14-04**: the diagonal argument of the halting problem ↔ 01's set theory direction (the loop closes once the Cantor lesson is added).
3. **01-05 ↔ 03-03**: congruence classes = equivalence classes, Z/m = a quotient set — the text never names it.
4. **02 ↔ 03 ↔ 04**: 03-04 already uses group language and 03-05 already writes a ring isomorphism, both of which should point back to 02; the determinant examples of 02-05 and 04-04 should reference each other; 04-03 and 05-05 use the same shear matrix [[1,1],[0,1]] and neither names the coincidence.
5. **04 ↔ 10-06**: least squares = projection onto the column space (to be established once the inner-product lesson exists).
6. **08-01 ↔ 09-02**: "two heads being counted twice" is inclusion–exclusion.
7. **09-06 ↔ 10-04/10-05**: where 1.96 and σ/√n come from.
8. **09-05 ↔ 10-03/10-06**: r=Cov/(σₓσᵧ) and b=Cov/Var(x) share one source.
9. **11-02 ↔ 12-03**: the direction field is exactly the geometry of Euler stepping.
10. **11-03 ↔ 16-02**: the same logistic equation appears in both places, with no cross-reference.
11. **15-02 ↔ 11-05**: already says "consistent with the simple harmonic oscillator lesson"; could name the characteristic roots ±2i.
12. **16-05 ↔ 10-06**: least squares regression is the only in-body counterpart to fitting/overfitting, and the recommended route never passes through 10 — link it explicitly.
13. **17-03 ↔ 06-01**: link the epsilon–delta history lesson with the formal-definition lesson.
14. Interactive Lab 3 currently links to 09-02 (the independence lesson); re-point it once the "Common Distributions" lesson is added.

---

## D. Reference-Layer Completeness

- **The glossary has only 9 entries**, badly mismatched with its "Notation Reference" role and the volume of 96 lessons. Suggest expanding to 30–50 entries, prioritizing: ℕ/ℤ/ℚ/ℝ/ℂ, ∅, ∪/∩/∖, ≅, ∼ (equivalence/homotopy), ⌊x⌋, mod/≡, ker/im, det/tr/rank, Aᵀ, O(·)/o(·), ∂/∇, ∑/∏, ∫/∮, sup/inf/max/min, argmax, E[X]/Var/Cov, P(A|B), H(X), H₀/p-value/confidence interval/R², ε-δ, s.t./iff, ⊕/⊗, ⊥, ‖·‖, ⟨·,·⟩. The data can live in a hand-maintained `assets/glossary.json` (same pattern as concepts.json).
- **labs has only 4 experiments**, and additions are possible across the board: a CLT sampling simulation (pairing with 09), animated Newton iteration (pairing with 12), a visualization of composing linear maps/eigenvector directions (pairing with the new 04 lessons).
- **RESOURCES.md advanced-book gaps**: the 06 (real analysis/measure theory), 05 (differential geometry), 08 (combinatorics), 09 (probability theory), and 10 (statistical theory) directions have no advanced books at all (13/14/16/17 already declare that "dedicated follow-up bibliographies are still needed"; these five directions lack even the declaration). Add 1–2 open textbooks to each (e.g., Abbott's *Understanding Analysis*, Blitzstein's probability lecture notes; availability must be verified the same way).
- **Per-lesson "further reading" fit**: each module is pinned to a single book; 13 (convex optimization → OpenStax calculus), 17 (history & philosophy → Levin's discrete mathematics), 16 (modeling → 18.03 ODE), and 05 (geometry → Precalculus) are clearly weak fits — at minimum, state in the text that "only some chapters are relevant".
- concepts.json: full coverage of all 96 lessons, a uniform rubric (can explain/can derive/can transfer), good quality; the only defect is README's "36 lessons" count error (A1).

---

## E. Engineering/Consistency

- `verify_course.py` hard-codes `.concept input == 295` and `.entry == 6006`: CHECKLIST already warns to keep these in sync, but the sturdier approach is to read the expected values from `concepts.json` and `classification-audit.json`.
- The branch-page "subfield route" copy (build_course.py L143): the first item always reads "first master this branch's N introductory lessons", which assigns every lesson to the first subfield (e.g., 02's "elementary algebra" swallows the group/ring lessons) — misleading. Either add a "lesson↔subfield" mapping to the data structure, or drop this specializing sentence.
- README's "17 learning directions + 1 preparation module" agrees with the table; the MSC 63-category mapping is complete and assertion-guarded; the classification page's audit JSON matches the measured counts — all well done.
- Leftovers already recorded in CHECKLIST (meta description, the labs binomial chart lacking a baseline, etc.) are not repeated here.

---

## F. Suggested Priorities

**P0 fix the errors (within half a day)**: all of A1–A7; a footnote for A8 for now; the one-line-fixable items in A13 (the one-sided p-value, the solution-family constant C, m=1, the "geometry course" reference, etc.).

**P1 add the 6 most painful lessons (each still in the 15–25 minute format, via the CHECKLIST "add one lesson" workflow)**:
1. 06 "A First Look at Partial Derivatives and the Gradient" (also cures half of A8/A9)
2. 04 "Eigenvalues and Diagonalization" (the 2×2 characteristic polynomial needs only 02's quadratic formula; complex eigenvalues tie in neatly with 02's complex numbers and 11's complex roots)
3. 09 "Common Distributions: Binomial, Geometric, and Normal"
4. 06 "Differentiation Rules and Integration Techniques" (chain/substitution/by parts; cures the other half of A9)
5. 11 "Separable Equations" (the explicit logistic solution, bridging to 16)
6. 04 "Inner Products, Projections, and Least Squares" (the bridge to 10-06)

**P2 honor the promises / shrink the gaps (about 10–12 lessons)**: 00 equations and inequalities; 03 Diophantine equations and modular inverses; 05 solving triangles + parametric equations/polar coordinates; 08 binomial theorem; 09 random walks; 10 Bayesian statistics; 11 phase planes and systems; 12 interpolation + condition numbers; 14 RSA; 14 error-correcting codes; 16 network spread; 17 Cantor's infinity/philosophy of mathematics; 15 one lesson per direction, or state the deferral scope on the module page.

**P3 reference layer and cross-links**: glossary expansion (the section D list); labs additions; the 14 cross-links of section C; RESOURCES books for the five directions; branch-page subfield copy (section E).

**Workflow reminder**: all course-content changes go into the data tuple of `tools/build_course.py` plus matching entries in `assets/concepts.json` (extend_atlas asserts the entry counts agree); A1 is fixed in extend_atlas.py; afterward follow the fixed CHECKLIST process (build → extend → verify → spot-check in the browser → commit). Remember to sync verify's 295/6006 assertions.
