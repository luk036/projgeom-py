"""Fold-a-ladder trick art on an A4 sheet, following the "3D ladder" illusion.

The sheet is A4 landscape (297 mm x 210 mm).  Folded in half it has a vertical
crease down the middle.  Two parallel lines near the bottom are the shadow; from
their ends straight lines run up to the crease, giving a symmetric chevron whose
apex sits on the crease, and vertical lines join the chevron's rails (the rungs).
Matching rungs are drawn on the shadow.

Because the apex lies on the crease, folding 90 degrees puts the two arms in two
perpendicular planes; viewed along the fold's bisector they are exactly
collinear, so the flat chevron reads as a straight 3D ladder.

The SVG is sized in millimetres (printable at 100%), vertices are projgeom
:class:`PgPoint` objects, and every coordinate is an exact
:class:`fractions.Fraction` in millimetres -- no floating point is used.

Usage::

    python examples/fold_ladder.py
"""

from fractions import Fraction
from pathlib import Path
from typing import List, Tuple

from projgeom import PgPoint

SHEET_W = Fraction(297)
SHEET_H = Fraction(210)
PX_PER_MM = 4

CREASE_X = SHEET_W / 2
HALF_WIDTH = Fraction(237, 2)
SHADOW_LOW = Fraction(30)
SHADOW_HIGH = Fraction(38)
APEX_HEIGHT = Fraction(182)
RUNGS = 11

INK = "#26356b"
LIGHT = "#a9a9a9"
FOLD = "#4d90c8"
PAPER = "#fdfcf8"

Pt = Tuple[Fraction, Fraction]
Vec3 = Tuple[Fraction, Fraction, Fraction]


def round_frac(value: Fraction) -> int:
    num, den = value.numerator, value.denominator
    whole, rest = divmod(num, den)
    if 2 * rest >= den:
        whole += 1
    return whole


def clean(x: Fraction, y: Fraction) -> Pt:
    px, py, pz = PgPoint.from_fractions([x, y, Fraction(1)]).coord
    return Fraction(px, pz), Fraction(py, pz)


def rail_y(base: Fraction, x: Fraction) -> Fraction:
    return base + (APEX_HEIGHT - SHADOW_LOW) * (HALF_WIDTH - abs(x - CREASE_X)) / HALF_WIDTH


def columns() -> List[Fraction]:
    return [
        CREASE_X + Fraction(k, RUNGS) * HALF_WIDTH
        for k in range(-RUNGS, RUNGS + 1)
    ]


def fold3(point: Pt) -> Vec3:
    x, y = point
    if x <= CREASE_X:
        return x, y, Fraction(0)
    return CREASE_X, y, x - CREASE_X


def view_xy(point: Vec3) -> Pt:
    x, y, z = point
    return x - z, y


def flat_spans() -> List[Tuple[Pt, Pt, str]]:
    spans: List[Tuple[Pt, Pt, str]] = []
    cols = columns()

    for base, color in ((SHADOW_LOW, INK), (SHADOW_HIGH, INK)):
        for i in range(len(cols) - 1):
            spans.append(
                (
                    clean(cols[i], rail_y(base, cols[i])),
                    clean(cols[i + 1], rail_y(base, cols[i + 1])),
                    color,
                )
            )

    for x in cols:
        spans.append((clean(x, rail_y(SHADOW_LOW, x)), clean(x, rail_y(SHADOW_HIGH, x)), INK))
        spans.append((clean(x, SHADOW_LOW), clean(x, SHADOW_HIGH), LIGHT))

    spans.append((clean(CREASE_X - HALF_WIDTH, SHADOW_LOW), clean(CREASE_X + HALF_WIDTH, SHADOW_LOW), LIGHT))
    spans.append((clean(CREASE_X - HALF_WIDTH, SHADOW_HIGH), clean(CREASE_X + HALF_WIDTH, SHADOW_HIGH), LIGHT))

    spans.append(
        (
            clean(CREASE_X, Fraction(2)),
            clean(CREASE_X, APEX_HEIGHT + Fraction(18)),
            FOLD,
        )
    )
    return spans


def view_spans() -> List[Tuple[Pt, Pt, str]]:
    return [
        (view_xy(fold3(a)), view_xy(fold3(b)), color)
        for a, b, color in flat_spans()
    ]


def render(spans: List[Tuple[Pt, Pt, str]], spans_for_fit: List[Tuple[Pt, Pt, str]]) -> str:
    pts = [p for a, b, _ in spans_for_fit for p in (a, b)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(max_x - min_x, Fraction(1))
    span_y = max(max_y - min_y, Fraction(1))
    margin = Fraction(8)
    scale = min(
        (SHEET_W - 2 * margin) / span_x,
        (SHEET_H - 2 * margin) / span_y,
    )
    off_x = margin + (SHEET_W - 2 * margin - span_x * scale) / 2 - min_x * scale
    off_y = margin + (SHEET_H - 2 * margin - span_y * scale) / 2 - min_y * scale

    def px(point: Pt) -> Tuple[int, int]:
        mx = point[0] * scale + off_x
        my = point[1] * scale + off_y
        return round_frac(mx * PX_PER_MM), round_frac((SHEET_H - my) * PX_PER_MM)

    doc = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_W}mm" height="{SHEET_H}mm" '
        f'viewBox="0 0 {round_frac(SHEET_W * PX_PER_MM)} {round_frac(SHEET_H * PX_PER_MM)}">',
        "<title>Fold-a-ladder trick art</title>",
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
    ]
    for a, b, color in spans:
        pa, pb = px(a), px(b)
        doc.append(
            f'<line x1="{pa[0]}" y1="{pa[1]}" x2="{pb[0]}" y2="{pb[1]}" '
            f'stroke="{color}" stroke-width="1.2"/>'
        )
    doc.append("</svg>")
    doc.append("")
    return "\n".join(doc)


def main() -> None:
    out = Path(__file__).resolve().parent
    flat = flat_spans()
    (out / "fold_ladder.svg").write_text(render(flat, flat), encoding="utf-8")
    print("wrote fold_ladder.svg")
    view = view_spans()
    (out / "fold_ladder_view.svg").write_text(render(view, view), encoding="utf-8")
    print("wrote fold_ladder_view.svg")


if __name__ == "__main__":
    main()
