# Session Report — Fold Trick-Art on projgeom-py

## 1. Objective

Produce **printable "fold trick-art" sheets** — the optical-illusion craft where a flat drawing, when folded 90° along a crease, reads as a 3D object from the right viewing angle. Constraints carried through the whole session: **use projgeom's functions**, **no floating-point arithmetic**, **printable on A4**.

Two objects were attempted: a **ladder** (reached an acceptable state) and a **chair** (unfinished).

## 2. Work timeline

### Task A — Reverse-perspective art — reverted

- Read the muminthemadhouse reverse-perspective page; built `examples/reverse_perspective.py` plus three SVGs (corridor, room, underwater) using `Transform`, `projective_transform` and `uc_point`, all-Fraction.
- Feedback: "Not quite correct. Revert all the changes." — the `examples/` directory was deleted and the working tree left clean.

### Task B — Fold-a-ladder — committed

Sources: the rainfrancescreations "3D ladder" tutorial, then a clearer reference (Singapore NLB PDF, "Eye-mazing Optical Illusions", page 1 — "The 3D Ladder").

Iterations and feedback:

1. Central-projection **anamorphosis** (viewer `V` projects each point onto the floor/wall, then unfold). Feedback: "It looks 3D only when viewing from certain angle", "Not correct. Read again the diagrams."
2. Added a cast **shadow** from a light `L`. Feedback: "It does not look like the drawing."
3. Rewrote to the **PDF's actual method**: fold a sheet in half to make a crease; draw two parallel "shadow" lines near the bottom; from their **ends** draw lines **up to the crease** (a chevron); add **vertical rungs**; fold 90°.
   - **Why it works (proved):** the chevron apex lies on the crease, so folding puts the arms in two perpendicular planes. Arms `(±A, −B)` become `(−A, −B, 0)` and `(0, −B, A)`; projected along the bisector `(1, 0, 1)` both give `(−A/2, −B, A/2)` — exactly collinear.
   - Feedback: "Much better now. But the aspect ratio is not correct." — retuned to a wide, shallow chevron.
   - Then: "Assume draw on A4 paper…" plus "avoid using floating-point numbers" — rebuilt with millimetre `Fraction` coordinates and an SVG sized `297mm × 210mm`.
- **Verification:** 41/41 mirrored arm pairs land on the same folded screen point; no float literals; valid XML; `flake8` clean.
- **Committed** and pushed to `origin/dev`:
  - `2997cd1  feat: add anamorphic fold-a-ladder trick-art generator`
  - `3893b29  docs: add fold-a-ladder printable and viewpoint SVGs`

### Task C — Fold-a-chair — unfinished (surrendered)

Request: "Draw a simple chair against a wall with shadow."

Clarified spec (user answers): the two planes are the **floor + wall at 90°**; the two images sit **side by side, clipped on the fold line**; use **`projective_transform`**; projection type "you find out"; and the **purpose** was confirmed (printable fold-anamorphosis → fold 90° → a 3D chair with a shadow from the matching viewpoint).

Attempts, each rejected:

- a mirrored copy of the chair — "It is a chair! not ladder!"
- `projective_transform` on both halves — stretched
- 3D chair ray-projected onto floor + wall — messy
- "Use perspective transformation on both parts" — done, still wrong
- green crease plus a fuller brown profile — "Not correct."
- a plain front view — "3/4 view you fool!"
- a clean **3/4 view** (filled seat/back, thick outline, hidden edges removed) — "Yes to all"
- shadow removed, then the projection step — **"completely wrong" (×2)**
- **Result: I said "surrender."**

## 3. Artifacts / repo state

- **Committed** (`origin/dev` @ `3893b29`): `examples/fold_ladder.py`, `examples/fold_ladder.svg`, `examples/fold_ladder_view.svg`.
- **Uncommitted** (working tree):
  - `M examples/fold_ladder.py`, `M examples/fold_ladder.svg`, `M examples/fold_ladder_view.svg`
  - `?? examples/fold_chair.py`, `?? examples/fold_chair.svg`
- Branch `dev`, in sync with `origin/dev`.

## 4. Technical findings

- projgeom toolbox used: `projective_transform` (four-point homography), `PgPoint`/`PgLine`, `meet`, `Transform`, exact `Fraction`.
- **No-float discipline:** all geometry as `Fraction`/`int`; pixels via exact integer rounding; SVG in millimetres (printable at 100%).
- **Ladder geometry:** the "folding makes the arms collinear from the bisector" identity above.
- **Known trade-off** (derived): chevron sharpness scales as `t* = VZ / (VZ − z*)`, so a sharp chevron needs a close viewer, which makes the folded view foreshortened.
- **Chair projection:** ray-plane "first hit" from `V` onto floor/wall, then unfold, does reproduce the object from `V` — but I could not shape it into a recognisable chair.

## 5. What went wrong

- Long analysis loops and repeated re-approaches without pinning the geometry up front.
- For the chair there was **no reference for the intended flat image**, so every guess missed.

## 6. Recommendation / next step

- **Ladder:** done and committed — re-tune the aspect if desired, then re-commit the working-tree changes.
- **Chair:** the fastest unblock is **one reference image** (or link) of the intended **flat sheet plus folded result**. With that the geometry can be matched exactly instead of guessed.
