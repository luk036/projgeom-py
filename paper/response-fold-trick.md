# Response to Reviewer

Paper: *Fold Trick-Art: Exact Two-Plane Anamorphosis for Printable Sheets and Foldable Screens* (Wai-Shing Luk).

Reference implementations inspected: `projgeom-py` (this repository) — `examples/fold_trick.py`, the Python mirror of `examples/fold_trick.cpp`; and the C++ sibling `projgeom-cpp` — `examples/fold_trick.cpp` (branch `dev`, commit `5ca042c`), built with `xmake` + MSVC.

We thank the reviewer for a careful and largely accurate critique. Every point was re-checked against the actual source and against the compiled artefacts, and every claim that rested on a number was re-measured. Most of the critique holds. Three of the reviewer's factual premises did not survive re-measurement — the *integer budget*, the *edge counts*, and the word *independent* — and those are corrected below. The qualitative conclusions of the paper (exactness, the $\sigma$ classifier, "32-bit insufficient, 64-bit sufficient", zero pixel divergence) are unchanged. The paper (`fold-trick.md`) has been revised accordingly.

## Verdict summary

| # | Critique | Verdict | Action |
|---|----------|---------|--------|
| 1 | Unified linear form $\sigma$ | Strength, accepted | — |
| 2 | Exact rationals + zero pixel divergence | Strength, accepted; "independent" corrected | Clarified the C++ is a line-by-line port |
| 3 | Integer budget ($6.1\times10^{7}$; $\sim10^{15}$ products) | **Not reproducible** | Re-measured; table and prose replaced |
| 4 | Crease condition | Strength, accepted | — |
| 5 | Foldable-screen hardware translation | Strength, accepted | — |
| 6 | Centroid painter's occlusion | **Valid** | Conceded; failure modes named |
| 7 | Rational / planar-only restriction | Valid (already conceded) | Retained |
| 8 | Cascading bit growth | Valid (already conceded) | Retained |
| 9 | Monocular vs binocular stereopsis | Valid | Added |
| 10 | Rigid spatial coupling | Valid (already conceded) | Retained |
| 11 | No photometric / material model | Valid | Added |
| 12 | Narrow validation (3 objects; 20/20/22 edges) | Valid; counts corrected | Edge counts fixed to 20/16/21 |

## Point-by-point

### Strengths 1, 4, 5 — accepted

We agree with the reviewer's reading of the $\sigma$ formulation, the crease condition $Y_0 = Z_s V_y / V_z$, and the foldable-screen translation, and we keep them as presented. The crease condition in particular is a genuine design rule, and we have not softened it.

### 2. Exact rationals and "zero pixel divergence" — accepted, one correction

The **zero-divergence** claim is true and we re-verified it end to end. Compiling the C++ example (`xmake build fold_trick`, MSVC `/O2`) and rendering the three sheets gives files that are byte-identical to the Python output *except for line endings*:

| sheet | committed (CRLF) | C++ / Python (LF) |
|-------|------------------|-------------------|
| `chair_flat.svg` | 2617 B | 2583 B |
| `table_flat.svg` | 2454 B | 2422 B |
| `house_flat.svg` | 3086 B | 3046 B |

The byte difference is exactly the number of line breaks, so the content (and therefore "pixel-for-pixel") is identical.

However, the reviewer's word **"independent"** overstates the evidence. The C++ is a *line-by-line port* of the Python — same author, same algorithm, committed 22 s after the Python (`723eba5`, 21:18:42 vs `5ca042c`, 21:19:04) and described in both the paper and the file header as a port. The agreement is therefore a strong **translation-consistency** check, not independent corroboration by a separately derived implementation. The paper now says this explicitly, and the contribution list no longer leans on "independent".

As part of this revision the Python was also reorganised so that a single module, `examples/fold_trick.py`, mirrors `examples/fold_trick.cpp` 1:1 (a `Scene` value plus `make_chair` / `make_table` / `make_house`), with the old per-object scripts reduced to thin wrappers. The two codebases can now be maintained together; the SVGs are unchanged.

**Action.** Reworded the C++ section to state that the port is a translation rather than an independent implementation; noted the Python reorganisation; kept the verified zero-divergence statement.

### 3. Integer budget — NOT REPRODUCIBLE (the correction that changes a number)

The reviewer quoted the paper's figures — max stored value $6.1\times10^{7}$, with homography products "of order $10^{15}$ to $10^{16}$" — as a strength. We could not reproduce those numbers from either implementation, and we now believe the printed table is wrong. The measurement and its result:

- **Method.** We instrumented the exact arithmetic so that the largest numerator *or* denominator of *every* rational formed is recorded **before** each gcd reduction. This deliberately includes the internal determinant and adjugate products of the four-point homography — the quantity the paper claims to report.
- **Compiled C++ (every rational operation):** chair $9.37\times10^{7}$, table $2.03\times10^{11}$, house $9.56\times10^{10}$.
- **Python reference (four-point homography layer):** chair $2.48\times10^{7}$, table $7.34\times10^{7}$, house $2.71\times10^{7}$.

Consequently:

- The largest value is about $2.0\times10^{11}$ (the table), not $6.1\times10^{7}$ — a factor of $\sim 3300$.
- There is **no** intermediate of order $10^{15}$: the largest value ever formed is $2.0\times10^{11}$.
- 32-bit signed integers (limit $2.1\times10^{9}$) overflow by a factor of about $10^{2}$, not "ten orders of magnitude".
- 64-bit integers (limit $9.2\times10^{18}$) *still* suffice, with about **seven** orders of magnitude of headroom, not eleven.

The qualitative conclusion is unchanged — **32-bit integers are not sufficient; 64-bit integers are** — which is what matters for the library's choice of a 64-bit rational, so this is a correction of magnitudes, not of the paper's thesis.

**Action.** Replaced Table `tab:budget` with the measured values; rewrote the surrounding analysis to state the correct headroom and to drop the unsupported "$10^{15}$ products" remark; updated the abstract and the contribution list to match.

### 6. Centroid painter's algorithm — VALID

The reviewer is right, and this was already conceded in the paper ("the non-interpenetrating faces used here"). A centroid sort is correct only for front-to-back separable, individually convex faces. It fails for cyclic overlaps, interpenetrating or self-occluding meshes, and faces of very different aspect ratio; a general scene needs a BSP tree or an exact topological visibility algorithm.

**Action.** Named the failure modes in the occlusion paragraph of Section `sec:render` and promoted the point to a named limitation, *"Occlusion is approximate."*

### 7. Rational and planar-only restriction — VALID (already conceded)

Retained. The black construction is exact for rational inputs; coordinates involving roots of non-squares need a number field or a symbolic type, and only planar faces are supported. The limitation *"Exactness stops at the rationals"* is unchanged.

### 8. Cascading bit-length growth — VALID (already conceded)

Retained. The measured budget is modest only because the construction is shallow; chained homographies and iterative clipping would grow the rationals and would eventually need wider or arbitrary-precision integers. The limitation *"Coordinate growth"* is unchanged.

### 9. Monocular rigidity vs binocular stereopsis — VALID

Added. The illusion is strictly monocular and single-viewpoint: binocular disparity exposes the physical corner, and the effect degrades continuously away from $V$.

### 10. Rigid spatial coupling — VALID (already conceded)

Retained. Scale invariance along sight rays means the sheet depends only on the *relative* geometry of viewer and object, so one cannot move the object without moving the viewer.

### 11. Absence of photometric realism and material models — VALID

Added. The renderer is purely geometric — flat shading and outlines, no lighting, shadows or reflectance — whereas in the physical craft the shadows cast across the crease are themselves strong depth cues.

**Action for 9–11.** Folded into a new limitation, *"Monocular, single-viewpoint, and unlit."*

### 12. Narrow empirical validation — VALID; counts corrected

The reviewer's "$20/20/22$ edges" is the figure printed in the paper's Table `tab:params`, and **two of the three are wrong**. The generator code defines:

| | chair | table | house |
|---|---|---|---|
| faces | 4 | 3 | 6 |
| **edges (paper)** | 20 | 20 | 22 |
| **edges (code)** | 20 | **16** | **21** |

(After the crease split the drawn segment counts are 22 / 21 / 25 respectively.) The face counts were already correct.

**Action.** Corrected the edge counts in Table `tab:params`; conceded the narrow validation by adding a limitation, *"Narrow validation,"* noting that the reported budget is a measurement for this family rather than a general bound.

### Reviewer's closing suggestions

Both are good directions and we record them as future work: relaxing $\sigma$ to a non-right (general dihedral) fold, and a study of integer growth specifically through homography *inversions* (our instrumentation already covers the inverse and its determinant products, and it is a natural place for the growth to concentrate).

## Changes to the manuscript

- **Abstract:** budget sentence corrected to the measured $2.0\times10^{11}$ and "about seven orders of magnitude"; "exact integer budget" → "measured exact-integer budget".
- **Contributions:** item 4 reworded ("measured … suffice") and no longer implies "more than sufficient".
- **"A C++ Realization and the Integer Budget":** stated that the port is a translation, not an independent implementation; restated the instrumentation protocol (every numerator/denominator, before reduction); replaced Table `tab:budget` with the measured values; rewrote the analysis (32-bit overflow ~$10^{2}$; 64-bit headroom ~seven orders); removed the $10^{15}$-product claim.
- **Table `tab:params`:** edge counts corrected to 20 / 16 / 21.
- **"Rendering the Sheet" (occlusion):** noted the painter's algorithm is not a general visibility method.
- **"Discussion and Limitations":** added *"Occlusion is approximate,"* *"Monocular, single-viewpoint, and unlit,"* and *"Narrow validation."* Kept the rational-only, scale-invariance and coordinate-growth items.
- **Conclusion:** "comfortable 64-bit integer budget" → "measured 64-bit integer budget".

## Artifact

`fold-trick.pdf` rebuilt from the revised `fold-trick.md` (same pipeline as `projgeom.pdf`: `pandoc` + `pandoc-crossref` + `--citeproc` + `pdflatex` via `make fold-trick`).
