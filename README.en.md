# Understanding Mathematics

Goal: build mathematical literacy — understand why concepts are defined the way they are and why results hold, and be able to use them to explain problems.

Double-click to open the [HTML study homepage](index.en.html). All explanations, graphics, and interactions work offline with nothing to install; external textbooks require an internet connection. A modern Chrome, Edge, or Firefox is recommended. The right end of every page's navigation switches between English and Chinese; the Chinese edition entry is [index.html](index.html).

## How Mathematics Is Divided

There is no single, universally accepted, non-overlapping list of "all main branches" of mathematics. This course uses **17 study directions + 1 preparation module**, covering foundations, pure mathematics, computation, and applications, and groups neighboring research areas. Cross-cutting fields such as algebraic geometry or stochastic analysis may belong to several directions; the history of mathematics and mathematics education stand as separate literacy directions. The Mathematics Atlas references the research classification of [MSC2020](https://msc2020.org/), but its study grouping is not the official MSC hierarchy.

## Branches and Subfields

| Branch / Course Entry | Main Subfields | Introductory Prerequisites |
|---|---|---|
| [Arithmetic, Functions, and Preparation](00-preparation/index.en.html) | Numbers and operations; fractions and proportions; powers and logarithms; equations and inequalities; functions; trigonometric functions | The four arithmetic operations; if these are unfamiliar, start here |
| [Mathematical Foundations and Proof](01-foundations/index.en.html) | Integers, fractions, and ratios; sets and mappings; propositional logic; proof methods; set theory, axioms, and computability | The four arithmetic operations |
| [Algebra and Structure](02-algebra/index.en.html) | Elementary algebra; polynomials; group theory; ring theory; field theory; commutative algebra; representation theory; category theory and homological algebra | Fractions, equations, and basic proofs |
| [Number Theory](03-number-theory/index.en.html) | Divisibility and congruences; prime numbers; Diophantine equations; analytic number theory; algebraic number theory; arithmetic geometry | Integers, algebra, and proof |
| [Linear Algebra](04-linear-algebra/index.en.html) | Systems of linear equations; vector spaces; linear maps; matrices; eigenvalues; inner products and spectral decomposition; multilinear algebra | Elementary algebra, the coordinate plane |
| [Geometry](05-geometry/index.en.html) | Euclidean geometry; analytic geometry; projective geometry; differential geometry; Riemannian geometry; algebraic geometry; convex geometry | Algebra, coordinates, and basic proofs |
| [Calculus and Mathematical Analysis](06-analysis/index.en.html) | Functions and limits; differentiation; integration; real analysis; complex analysis; measure theory; harmonic analysis; functional analysis; nonstandard analysis | Functions, algebra, coordinates |
| [Topology](07-topology/index.en.html) | Point-set topology; continuity and homeomorphisms; compactness; connectedness; algebraic topology; differential topology; geometric topology | Sets, mappings; advanced topics need analysis and algebra |
| [Combinatorics and Graph Theory](08-combinatorics/index.en.html) | Counting; recurrences; generating functions; graph theory; extremal combinatorics; design theory; discrete geometry | Integers and basic proofs |
| [Probability Theory](09-probability/index.en.html) | Probability spaces; conditional probability; random variables; distributions; law of large numbers; limit theorems; stochastic processes; stochastic analysis | Fractions, sets; advanced topics need analysis |
| [Statistics](10-statistics/index.en.html) | Descriptive statistics; sampling; parameter estimation; hypothesis testing; regression; Bayesian statistics; experimental design; multivariate and nonparametric statistics | Probability, algebra; for binomial coefficients see 08 |
| [Differential Equations and Dynamical Systems](11-differential-equations/index.en.html) | Ordinary differential equations; partial differential equations; integral equations; difference equations; stability; bifurcations; chaos; ergodic theory | Derivatives, integrals; Lesson 7's phase plane needs linear algebra (eigenvalues: see 04, Lesson 07) |
| [Numerical Analysis and Scientific Computing](12-numerical/index.en.html) | Errors; interpolation and approximation; numerical linear algebra; numerical integration (quadrature); root-finding; numerical solution of differential equations; computational reliability | Algebra, calculus |
| [Optimization, Operations Research, and Control](13-optimization/index.en.html) | Convex optimization; linear programming; integer programming; calculus of variations; optimal control; game theory; scheduling and decision-making | Algebra; advanced topics need calculus and linear algebra |
| [Theoretical Computer Science and Information Mathematics](14-computation/index.en.html) | Algorithms and complexity; automata; computability; information theory; coding theory; cryptography | Logic, combinatorics, probability |
| [Mathematical Physics](15-mathematical-physics/index.en.html) | Classical mechanics; fluids and continua; electromagnetism and optics; heat and statistical physics; the mathematics of quantum theory; relativity and field theory | Calculus, linear algebra, differential equations |
| [Mathematical Modeling and Interdisciplinary Applications](16-modeling/index.en.html) | Models and validation; mathematical biology; economics and financial mathematics; networks and social systems; systems science; data modeling | Algebra; needs derivatives from 06 and differential-equation basics from 11 |
| [History, Philosophy, and Mathematical Literacy](17-history/index.en.html) | Number systems and their extensions; conceptions of proof; the axiomatic method; infinity; philosophy of mathematics; mathematics education and communication | Curiosity, basic algebra |

## Recommended Study Paths

1. If fractions, percentages, or functions are not yet familiar, start with 00; otherwise take the diagnostic questions on the homepage first.
2. First main line: 00 Preparation → 01 Foundations and Proof → 02 Elementary Algebra → 04 Linear Algebra, 05 Geometry → 06 Calculus.
3. Discrete branch: 01 → 03 Number Theory, 08 Combinatorics and Graph Theory → 14 Computation and Information.
4. Uncertainty branch: 00, 01 → 09 Probability → 10 Statistics; advanced probability needs measure theory from 06.
5. Continuous and applied branch: 04, 06 → 11 Differential Equations → 12 Numerical, 13 Optimization → 15 Mathematical Physics, 16 Modeling.
6. Abstract direction: 01, 02, 06 → 07 Topology; then move on to algebraic geometry, functional analysis, and the like. 17 History and Philosophy can be read alongside at any time.

Prerequisites here refer to the introductory lessons; research-level subfields require longer preparation. For example, algebraic geometry requires abstract algebra and topology, and stochastic analysis requires measure-theoretic probability and real analysis.

## How to Work Through a Lesson

Work through a lesson in 15–25 minutes: read the intuition → work the example by hand → write the exercise on your own → read the solution → restate the idea in your own words. Redo it without looking at the answers the next day, after 3 days, and after 7 days; when reviewing, mix in problems from an earlier branch. A good rhythm is 3 study sessions and 1 review session per week, and the pace that matters is the one at which you can explain the material.

The [Interactive Labs](reference/labs.en.html) offer seven experiments — secants approaching the tangent, areas under linear transformations, the binomial distribution, step-size stability, sampling distributions, Newton's method, and eigenvalue ellipses; each lab has prediction questions and explanations. Use the [Notation Reference](reference/glossary.en.html) for review at any time; after finishing a lesson, check off each item in the [core concept checklist](reference/concepts.en.html) as a self-assessment.

## Current Content and Boundaries

The current version has 18 modules and 139 short introductory lessons in Chinese, each containing concepts, a worked example with derivation, an exercise, and a folded solution-and-analysis. Every module has a subfield route. It is a panoramic introductory course you can start right away — **not a complete textbook for every subfield**; the advanced topics along the routes are not yet developed. Learning records start empty: nothing is assumed about what you have already mastered. Exercise input is not saved, and proofs are not automatically judged for correctness.

## Course Design and Maintenance

The [teach skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md) was retrieved and read in full first, informing the design of short lessons, feedback, spaced retrieval, and learning records. As requested by the user, the course lives in the branch directories. The skill was used only for that one read; it is not installed globally.

- [Learning mission](MISSION.en.md), [teaching preferences](NOTES.en.md), [sources](RESOURCES.en.md), [maintenance checklist](CHECKLIST.en.md).
- `learning-records/` holds the real learning feedback you submit later.
- `assets/` holds shared styles, scripts, and course data.
- After editing `tools/build_course.py`, run `python tools/build_course.py` to rebuild the course; do not also hand-edit the generated lesson pages.

## MSC2020: All 63 Two-Digit Major Classes

To avoid omissions, all two-digit major classes of the research classification are listed below, mapped to the folders of this course. **The mapping indicates route coverage, not that each of these research areas already has a complete course.** For example, K-theory, Lie groups, special functions, and astrophysics are all directions awaiting expansion. 00 is a general class, not a single research branch. Field names here are the official MSC2020 English titles; the Chinese README carries simplified Chinese renderings for study purposes.

| MSC | Field | Mapped Folder |
|---|---|---|
| 00 | General and overarching topics; collections | [History, Philosophy, and Mathematical Literacy](17-history/index.en.html) |
| 01 | History and biography | [History, Philosophy, and Mathematical Literacy](17-history/index.en.html) |
| 03 | Mathematical logic and foundations | [Mathematical Foundations and Proof](01-foundations/index.en.html) |
| 05 | Combinatorics | [Combinatorics and Graph Theory](08-combinatorics/index.en.html) |
| 06 | Order, lattices, ordered algebraic structures | [Algebra and Structure](02-algebra/index.en.html) |
| 08 | General algebraic systems | [Algebra and Structure](02-algebra/index.en.html) |
| 11 | Number theory | [Number Theory](03-number-theory/index.en.html) |
| 12 | Field theory and polynomials | [Algebra and Structure](02-algebra/index.en.html) |
| 13 | Commutative algebra | [Algebra and Structure](02-algebra/index.en.html) |
| 14 | Algebraic geometry | [Geometry](05-geometry/index.en.html) |
| 15 | Linear and multilinear algebra; matrix theory | [Linear Algebra](04-linear-algebra/index.en.html) |
| 16 | Associative rings and algebras | [Algebra and Structure](02-algebra/index.en.html) |
| 17 | Nonassociative rings and algebras | [Algebra and Structure](02-algebra/index.en.html) |
| 18 | Category theory; homological algebra | [Algebra and Structure](02-algebra/index.en.html) |
| 19 | K-theory | [Algebra and Structure](02-algebra/index.en.html) |
| 20 | Group theory and generalizations | [Algebra and Structure](02-algebra/index.en.html) |
| 22 | Topological groups, Lie groups | [Algebra and Structure](02-algebra/index.en.html) |
| 26 | Real functions | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 28 | Measure and integration | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 30 | Functions of a complex variable | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 31 | Potential theory | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 32 | Several complex variables and analytic spaces | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 33 | Special functions | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 34 | Ordinary differential equations | [Differential Equations and Dynamical Systems](11-differential-equations/index.en.html) |
| 35 | Partial differential equations | [Differential Equations and Dynamical Systems](11-differential-equations/index.en.html) |
| 37 | Dynamical systems and ergodic theory | [Differential Equations and Dynamical Systems](11-differential-equations/index.en.html) |
| 39 | Difference and functional equations | [Differential Equations and Dynamical Systems](11-differential-equations/index.en.html) |
| 40 | Sequences, series, summability | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 41 | Approximations and expansions | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 42 | Harmonic analysis on Euclidean spaces | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 43 | Abstract harmonic analysis | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 44 | Integral transforms, operational calculus | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 45 | Integral equations | [Differential Equations and Dynamical Systems](11-differential-equations/index.en.html) |
| 46 | Functional analysis | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 47 | Operator theory | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 49 | Calculus of variations and optimal control; optimization | [Optimization, Operations Research, and Control](13-optimization/index.en.html) |
| 51 | Geometry | [Geometry](05-geometry/index.en.html) |
| 52 | Convex and discrete geometry | [Geometry](05-geometry/index.en.html) |
| 53 | Differential geometry | [Geometry](05-geometry/index.en.html) |
| 54 | General topology | [Topology](07-topology/index.en.html) |
| 55 | Algebraic topology | [Topology](07-topology/index.en.html) |
| 57 | Manifolds and cell complexes | [Topology](07-topology/index.en.html) |
| 58 | Global analysis, analysis on manifolds | [Calculus and Mathematical Analysis](06-analysis/index.en.html) |
| 60 | Probability theory and stochastic processes | [Probability Theory](09-probability/index.en.html) |
| 62 | Statistics | [Statistics](10-statistics/index.en.html) |
| 65 | Numerical analysis | [Numerical Analysis and Scientific Computing](12-numerical/index.en.html) |
| 68 | Computer science | [Theoretical Computer Science and Information Mathematics](14-computation/index.en.html) |
| 70 | Mechanics of particles and systems | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 74 | Mechanics of deformable solids | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 76 | Fluid mechanics | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 78 | Optics, electromagnetic theory | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 80 | Classical thermodynamics, heat transfer | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 81 | Quantum theory | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 82 | Statistical mechanics, structure of matter | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 83 | Relativity and gravitational theory | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 85 | Astronomy and astrophysics | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 86 | Geophysics | [Mathematical Physics](15-mathematical-physics/index.en.html) |
| 90 | Operations research, mathematical programming | [Optimization, Operations Research, and Control](13-optimization/index.en.html) |
| 91 | Game theory, economics, finance, and other social and behavioral sciences | [Mathematical Modeling and Interdisciplinary Applications](16-modeling/index.en.html) |
| 92 | Biology and other natural sciences | [Mathematical Modeling and Interdisciplinary Applications](16-modeling/index.en.html) |
| 93 | Systems theory; control | [Optimization, Operations Research, and Control](13-optimization/index.en.html) |
| 94 | Information and communication theory, circuits | [Theoretical Computer Science and Information Mathematics](14-computation/index.en.html) |
| 97 | Mathematics education | [History, Philosophy, and Mathematical Literacy](17-history/index.en.html) |


## Full Classification and Course Planning from Foundations to Research

- [Complete MSC2020 classification index](reference/classification.en.html): includes all **6,603 code records** from the CSV downloaded from the official site — 63 major classes, 534 middle classes, 5,503 subject leaf entries, and 503 general leaf entries; verified against the full set of labels in the official TeX. English technical names are retained, and codes or keywords can be searched offline. Full inclusion of classification names does not mean the corresponding lessons exist.
- **A note on counts**: the [official site](https://msc2020.org/) states 63 major classes, 529 middle classes, and 6,022 leaf classes; the currently downloaded file counts differently. This project reports the counts measured from the source file and has not invented classifications of its own. The audit results are in `assets/classification-audit.json`.
- [Staged curriculum overview](reference/curriculum.en.html): every module has goals and acceptance criteria for L0 introductory, L1 undergraduate core, L2 advanced with proofs, L3 graduate topics, and L4 research training. This is **teaching planning yet to be developed**; the current body of text is still 139 lessons.
- [Core concept checklist](reference/concepts.en.html): item-by-item "can explain / can derive / can transfer" self-assessment for all 139 lessons; progress is stored in your browser (localStorage) by default, with JSON export/import for backups and transfer across browsers or editions. Storage failures are reported.
- Research training means reading papers in a specific direction, reproducing proofs or algorithms, posing questions, and receiving feedback. There is no "master graduation line" covering all of mathematics, and finishing the materials does not by itself guarantee the ability to do original research.

Rebuild both editions with `python tools/build_all.py`. For dependency-free static checks, run `python tools/verify_course.py --static-only`. For full verification, first run `python -m pip install -r requirements.txt` and `python -m playwright install chromium`, then `python -m unittest discover -s tests` and `python tools/verify_course.py`. The browser checks cover both editions. See [CHECKLIST.en.md](CHECKLIST.en.md) for source ownership and [REVIEW.en.md](REVIEW.en.md) for review findings and fixes.
