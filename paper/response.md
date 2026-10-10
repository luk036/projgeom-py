# Response to Reviewer

Paper: *Projective Geometry as a Unified Framework for Exact Computational Geometry* (Wai-Shing Luk).
Reference implementation inspected: `projgeom-py` (this repository), `src/projgeom/`.

We thank the reviewer for a careful and largely accurate critique. Every point was
re-checked against the actual source. Below, each item is given a verdict with
file-and-line evidence, followed by the action taken in the revision. The paper
(`projgeom.md`) has been revised; the PDF was rebuilt (now 10 pages, no unresolved
cross-references, no overfull boxes).

## Verdict summary

| # | Critique | Verdict | Action |
|---|----------|---------|--------|
| 1 | Mathematical elegance / unification | Strength, accepted | -- |
| 2 | Axiomatic four-layer architecture | Strength, accepted | -- |
| 3 | Exact-arithmetic focus removes robustness bugs | Strength, refined | Clarified as exactness *over the rationals* |
| 4 | Breakdown at irrationality (2A) | **Valid, and understated** | Rewrote the limitation; removed an incorrect claim |
| 5 | Rational-trig trade-offs: non-additivity, interoperability (2B) | **Partly valid** (additivity yes, interoperability overstated) | Broadened the discussion, with a defense |
| 6 | Confinement to 2D / P^2 (2C) | **Valid** | Added an explicit limitation |
| 7 | Coordinate bit-width explosion (3A) | **Valid, previously unaddressed** | Added a coordinate-growth analysis |
| 8 | Artificial microbenchmarks; no real workloads or CGAL/Shewchuk comparison (3B) | **Partly valid**; the "~30 unit tests" figure is inaccurate | Corrected the test inventory; conceded the benchmark gap |
| 9 | Limited scope for general applications (3C) | **Valid, already conceded** | Retained |

## Point-by-point

### Strengths (1-3) -- accepted

We agree with the reviewer's reading of the mathematical unification and the
four-layer architecture, and we have kept them as presented. One refinement: the
"exact-arithmetic removes robustness bugs" claim is now stated precisely as
exactness **over the integers and the rationals**, since point 4 shows there is no
escape hatch when the result leaves that field.

### 4. Breakdown at irrationality (2A) -- VALID, and understated

The reviewer is correct, and the situation is in fact starker than the critique
states. We verified by inspection of `src/projgeom/`:

- The source contains **no** `sqrt`, `arcsin`/trigonometric function, `float`,
  `complex`, `cmath`, `numpy`, `math` or `decimal` usage (a repo-wide scan of
  `src/projgeom/*.py` returns no matches).
- `sympy` is **declared but unused**: it appears only in `requirements/extras.txt`
  and is never imported.
- The exact operations that would produce irrationals are either stubs or require
  the caller to pre-supply rationals:
  - `Conic.intersect` is a placeholder that unconditionally returns the empty
    list (`src/projgeom/conic.py:229`, `:250`); its docstring says a full version
    "requires solving a quadratic equation". `Conic.pole` (`:186`) is likewise a
    stub.
  - `Transform.rotation(angle_cos, angle_sin)` takes pre-computed rational
    cosine and sine (`src/projgeom/transform.py:90`), so a 45-degree rotation is
    representable only through a caller-supplied rational approximation.
  - `projective_transform(...)` returns `Transform.identity()`
    (`src/projgeom/transform.py:411`, `:436`).
  - Where a `Fraction` result is produced, it is **truncated back to an int** by
    floor division (`transform.py:239-241`, `:273-275`; `conic.py:180-182`).

Consequently the paper's original sentence -- "the library either keeps an exact
algebraic representation, when one is available, or falls back to floating point"
-- was **not true of the code**: there is neither a symbolic nor a floating-point
fallback.

**Action.** We replaced the "Irrational situations" limitation with a precise
statement, retitled *"Exactness stops at the rationals."* It now says the
guarantee is a *scope boundary fixed at the field of computation*, names the
concrete stubs (conic-line intersection, rotation-from-rationals, general
projective transform), and states explicitly that no symbolic or floating-point
fallback exists. The abstract and conclusion were updated to match.

### 5. Rational-trigonometry trade-offs (2B) -- PARTLY VALID

Two distinct claims were made.

*Non-additivity (valid).* Quadrance and spread are quadratic forms and are not
additive along a line or about a point; compositions require the polynomial
identities (triple quad / triple spread / cross law). This is a genuine cost and
we now state it.

*Loss of interoperability (overstated).* The framework does not disconnect from
mainstream geometry. Distances and angles are recovered from quadrance and spread
by a single square root or arcsine at the boundary when requested, and the
transformation groups are exactly the conventional Lie groups: the projective
group `PGL(3)` in the plane (`src/projgeom/transform.py:416`) and the Möbius
group `PGL(2)` on the projective line. Rational trigonometry is a measurement
representation that keeps the arithmetic exact for as long as possible; it is not
a replacement for vector calculus or Lie theory.

**Action.** Added the discussion *"Non-additivity and interoperability,"* which
concedes the additivity cost and rebuts the disconnection claim with the recovery
of distance/angle and the identification of the transformation groups.

### 6. Confinement to 2D / P^2 (2C) -- VALID

Confirmed against the code. Coordinates are length-3 homogeneous triples, enforced
at runtime (`src/projgeom/pg_object.py:228`, `if len(coord) != 3`). Join and meet
are both the three-vector cross product (`pg_object.py:45`, `:328`), the core
types are integer-only (`def dot(...) -> int`, `pg_object.py:22`; `Value =
TypeVar("Value", bound=int)`, `pg_plane.py:16`), and `Conic`/`Transform` are
`3 x 3`. There is no `P^3`, hyperplane, exterior-algebra, wedge or Grassmann
construct anywhere in the repository.

We also flag a naming trap the reviewer could have cited: `plckr`
(`pg_object.py:161`) and its test `test_plucker`
(`tests/verify_consistency.py`) are named after Plücker but implement the
two-term linear combination `lambda*a + mu*b` of the parameterization, **not**
Plücker (exterior-algebra) coordinates. They are therefore not a hidden
higher-dimensional feature.

**Action.** Added the limitation *"Confinement to the projective plane,"* which
explains why `P^3`/`P^n` requires Grassmann-Cayley algebra (lines as 2-blades /
Plücker coordinates) rather than a larger cross product, and notes the misleading
`plckr` naming.

### 7. Coordinate bit-width explosion (3A) -- VALID (previously unaddressed)

The reviewer is right that the paper never analyzed coordinate growth. Join and
meet are bilinear, so each construction doubles the degree of the coordinates in
the primitive inputs; a chain of `d` constructions yields degree growth by a
factor of two per step. GCD normalization keeps coordinates coprime but does not
bound the degree, and the fixed-width integer cores (Rust `wrapping_mul`; C++ raw
arithmetic) can overflow before a long chain finishes. Python's arbitrary-precision
integers avoid the overflow but not the growth.

**Action.** Added the analysis *"Coordinate growth,"* together with the standard
mitigations we do **not** implement -- arbitrary precision, modular /
evaluation-interpolation arithmetic, and filtered predicates
[@yap2000fundamental; @shewchuk1997adaptive] -- and named bounding that growth as
the clearest direction for future work.

### 8. Artificial microbenchmarks; no real workloads or robust-predicate comparison (3B) -- PARTLY VALID

The benchmark criticism is fair and is now conceded explicitly:

- There is exactly one benchmark file, `tests/bench_projgeom.py`, with 21 atomic
  `test_bench_*` functions; the paper reports only five of them.
- The benchmark module does **not** match pytest's `test_*.py` collection pattern,
  so it is **not run in CI** (CI runs `pytest tests/ --doctest-modules src/`).
- There are **no** workload-level benchmarks (no convex hull, Voronoi,
  triangulation, mesh or CAD) and **no** comparison against CGAL or Shewchuk's
  adaptive-precision predicates; both are cited as *background*, not baselines.

However, the reviewer's incidental figure of "~30 unit tests" **understates** the
actual test surface by roughly fivefold. Static count of the current tree:

- **157** pytest-collected test functions across 21 `test_*.py` files;
  - **91** property-based (Hypothesis `@given`) tests across 6
    `test_*_hypothesis.py` files, asserting algebraic invariants (duality
    idempotence, reflection involution, collinearity) for the Euclidean,
    Cayley-Klein, elliptic, hyperbolic, perspective and multi-CK models;
  - **66** conventional tests;
  - plus **2** doctest harnesses and source-level doctests.
- The figure the reviewer likely saw ("30") is the count of cross-language
  reference cases in `tests/verify_consistency.py`, which is run as a script and
  is **not** part of the pytest suite.

**Action.** The experiments section now reports the full inventory (157 tests, 91
property-based, 30 cross-language cases) and states plainly that the performance
evidence is atomic and that no workload-level benchmark or adaptive-predicate
comparison is offered; the contribution is a design and a reference
implementation, not a performance claim.

### 9. Limited scope for general applications (3C) -- VALID (already conceded)

The paper already states that a special-purpose implementation will be faster and
simpler when a single fixed geometry suffices and floating point is adequate. We
keep that concession and have reinforced it (together with point 7) by noting the
gcd/overflow cost of exact arithmetic.

## Changes to the manuscript

- Front matter: abstract now reports the 157-test property-based suite and lists
  the corrected limitations (rational-only exactness, 2D confinement, coordinate
  growth, non-additivity).
- "Cross-Language Verification and Benchmarks": added the test-surface inventory
  and the explicit concession of the benchmark scope.
- "Rational Trigonometry": clarified that the Ptolemy identity is confirmed by an
  *external* symbolic algebra system (the library performs no symbolic
  computation).
- "Discussion and Limitations": rewrote the irrationality limitation and added
  three new limitations -- confinement to the projective plane, coordinate
  growth, and non-additivity and interoperability. Remaining limitations
  (irrational/complex arithmetic, overflow) were retained.
- "Conclusion": updated the limitations sentence to match.

## Artifact

`projgeom.pdf` rebuilt from the revised `projgeom.md`: 10 pages, 0 unresolved
`??` cross-references, 0 overfull boxes, builds offline with a vendored CSL.
