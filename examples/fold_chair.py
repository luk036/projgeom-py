"""Fold-a-chair trick art: a 3D chair projected onto the floor and the wall.

The chair is built in 3D in the corner between a floor (z = 0, in front) and a
wall (y = 0, rising up), which meet along the crease y = z = 0.  Every edge is
projected along the ray from a viewpoint V onto whichever of the two planes the
ray meets first; the planes are then unfolded about the crease into a flat sheet,
one on each side of the crease (drawn green).  Fold the sheet 90 degrees along
the crease and, seen from V, the drawing is the 3D chair standing at the wall.

The sheet is A4 portrait (210 mm x 297 mm) and the SVG is sized in millimetres
(printable at 100%); every coordinate is an exact :class:`fractions.Fraction`, so
no floating point is used.

Usage::

    python examples/fold_chair.py
"""

from fractions import Fraction
from pathlib import Path
from typing import List, Tuple

SHEET_W = Fraction(210)
SHEET_H = Fraction(297)
PX_PER_MM = 4

VX, VY, VZ = Fraction(41), Fraction(-230), Fraction(74)

X0, X1 = Fraction(20), Fraction(62)
YF = Fraction(-48)
ZS, ZT = Fraction(46), Fraction(92)
ZA, ZB = Fraction(34), Fraction(14)
ZS1, ZS2 = Fraction(64), Fraction(80)

EDGE = "#6f4318"
CREASE = "#1faa1f"
PAPER = "#fdfcf8"

Vec3 = Tuple[Fraction, Fraction, Fraction]
Pt = Tuple[Fraction, Fraction]
Span = Tuple[Pt, Pt, str]


def round_frac(value: Fraction) -> int:
    num, den = value.numerator, value.denominator
    whole, rest = divmod(num, den)
    if 2 * rest >= den:
        whole += 1
    return whole


def chair_edges() -> List[Tuple[Vec3, Vec3]]:
    z0 = Fraction(0)
    return [
        ((X0, z0, z0), (X0, z0, ZS)),
        ((X1, z0, z0), (X1, z0, ZS)),
        ((X0, YF, z0), (X0, YF, ZS)),
        ((X1, YF, z0), (X1, YF, ZS)),
        ((X0, z0, ZS), (X1, z0, ZS)),
        ((X0, YF, ZS), (X1, YF, ZS)),
        ((X0, z0, ZS), (X0, YF, ZS)),
        ((X1, z0, ZS), (X1, YF, ZS)),
        ((X0, z0, ZA), (X0, YF, ZA)),
        ((X1, z0, ZA), (X1, YF, ZA)),
        ((X0, YF, ZA), (X1, YF, ZA)),
        ((X0, z0, ZA), (X1, z0, ZA)),
        ((X0, z0, ZS), (X0, z0, ZT)),
        ((X1, z0, ZS), (X1, z0, ZT)),
        ((X0, z0, ZT), (X1, z0, ZT)),
        ((X0, z0, ZS1), (X1, z0, ZS1)),
        ((X0, z0, ZS2), (X1, z0, ZS2)),
        ((X0, YF, ZB), (X1, YF, ZB)),
        ((X0, z0, ZB), (X1, z0, ZB)),
        ((X0, YF, ZB), (X0, z0, ZB)),
        ((X1, YF, ZB), (X1, z0, ZB)),
    ]


def plane_hit(point: Vec3) -> Pt:
    px, py, pz = point
    best_t = Fraction(-1)
    result: Pt = (Fraction(0), Fraction(0))
    if pz != VZ:
        t = -VZ / (pz - VZ)
        if t > 0:
            qy = VY + t * (py - VY)
            if qy <= 0 and (best_t < 0 or t < best_t):
                best_t, result = t, (VX + t * (px - VX), qy)
    if py != VY:
        t = -VY / (py - VY)
        if t > 0:
            qz = VZ + t * (pz - VZ)
            if qz >= 0 and (best_t < 0 or t < best_t):
                best_t, result = t, (VX + t * (px - VX), qz)
    return result


def project(a: Vec3, b: Vec3) -> List[List[Pt]]:
    runs: List[List[Pt]] = []
    run: List[Pt] = []
    for k in range(61):
        t = Fraction(k, 60)
        p = (
            a[0] + t * (b[0] - a[0]),
            a[1] + t * (b[1] - a[1]),
            a[2] + t * (b[2] - a[2]),
        )
        q = plane_hit(p)
        if run and (run[-1][1] <= 0) != (q[1] <= 0):
            run.append(q)
            runs.append(run)
            run = []
        run.append(q)
    if len(run) >= 2:
        runs.append(run)
    return runs


def build() -> List[Span]:
    spans: List[Span] = []
    for a, b in chair_edges():
        for run in project(a, b):
            for i in range(len(run) - 1):
                spans.append((run[i], run[i + 1], EDGE))
    xs = [p[0] for a, b, _ in spans for p in (a, b)]
    spans.append(((min(xs), Fraction(0)), (max(xs), Fraction(0)), CREASE))
    return spans


def render(spans: List[Span], out: Path) -> None:
    pts = [p for a, b, _ in spans for p in (a, b)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    margin = Fraction(16)
    scale = min(
        (SHEET_W - 2 * margin) / max(max_x - min_x, Fraction(1)),
        (SHEET_H - 2 * margin) / max(max_y - min_y, Fraction(1)),
    )
    off_x = margin + (SHEET_W - 2 * margin - (max_x - min_x) * scale) / 2 - min_x * scale
    off_y = margin + (SHEET_H - 2 * margin - (max_y - min_y) * scale) / 2 - min_y * scale

    def px(point: Pt) -> Tuple[int, int]:
        mx = point[0] * scale + off_x
        my = point[1] * scale + off_y
        return round_frac(mx * PX_PER_MM), round_frac((SHEET_H - my) * PX_PER_MM)

    doc = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_W}mm" height="{SHEET_H}mm" '
        f'viewBox="0 0 {round_frac(SHEET_W * PX_PER_MM)} {round_frac(SHEET_H * PX_PER_MM)}">',
        "<title>Fold-a-chair trick art</title>",
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
    ]
    for a, b, color in spans:
        pa, pb = px(a), px(b)
        width = "2.6" if color == CREASE else "1.6"
        doc.append(
            f'<line x1="{pa[0]}" y1="{pa[1]}" x2="{pb[0]}" y2="{pb[1]}" '
            f'stroke="{color}" stroke-width="{width}"/>'
        )
    (out / "fold_chair.svg").write_text("\n".join(doc + ["</svg>", ""]), encoding="utf-8")
    print("wrote fold_chair.svg")


def main() -> None:
    out = Path(__file__).resolve().parent
    render(build(), out)


if __name__ == "__main__":
    main()
