"""Fold-a-ladder trick art generated with projgeom.

A ladder leans in the 90-degree corner between a floor (z = 0) and a wall
(y = 0), with its left rail on the viewing axis and its right rail to the side,
so the right rail swings out to a chevron where it crosses the horizon.  A
viewer at V sees the ladder; each visible point is projected along the ray
V -> point onto whichever plane the ray meets first, and the two planes are then
unfolded into one flat sheet.  That sheet is the printable drawing: fold it 90
degrees along the horizon and, viewed from V, the flat chevron ladder stands up
as a real 3D ladder.

The map from the ladder's ``(side, v)`` plane onto the floor and onto the wall is
a projectivity, built exactly with :func:`projective_transform`.  All coordinates
are exact :class:`fractions.Fraction` values, so no floating point is used.

Usage::

    python examples/fold_ladder.py
"""

from fractions import Fraction
from pathlib import Path
from typing import List, Sequence, Tuple

from projgeom import PgPoint, projective_transform

VX, VY, VZ = Fraction(0), Fraction(-300), Fraction(300)
XC, W = Fraction(60), Fraction(60)
FOOT_DEPTH, TOP_HEIGHT = Fraction(100), Fraction(100)
RUNGS = 11

FLAT_W, FLAT_H = 560, 780
VIEW_W, VIEW_H = 440, 780
VIEW_PLANE_Y = Fraction(-150)

INK = "#333333"
FOLD = "#4d90c8"
PAPER = "#fbfbf7"

Flat = Tuple[Fraction, Fraction]


def round_frac(value: Fraction) -> int:
    num, den = value.numerator, value.denominator
    whole, rest = divmod(num, den)
    if 2 * rest >= den:
        whole += 1
    return whole


def ladder_point(side: Fraction, v: Fraction) -> Tuple[Fraction, Fraction, Fraction]:
    return XC + side * W, -FOOT_DEPTH * (Fraction(1) - v), TOP_HEIGHT * v


def ray_hit(px: Fraction, py: Fraction, pz: Fraction) -> Flat:
    best_t = Fraction(-1)
    result: Flat = (Fraction(0), Fraction(0))

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


def crossover() -> Fraction:
    ratio = VZ / VY
    return -ratio * FOOT_DEPTH / (TOP_HEIGHT - ratio * FOOT_DEPTH)


def homogeneous(side: Fraction, v: Fraction) -> PgPoint:
    return PgPoint.from_fractions([side, v, Fraction(1)])


def as_flat(pt: PgPoint) -> Flat:
    x, y, z = pt.coord
    return Fraction(x, z), Fraction(y, z)


def projectivity(corners: Sequence[Tuple[Fraction, Fraction]]):
    src = [homogeneous(side, v) for side, v in corners]
    dst = [
        PgPoint.from_fractions([*ray_hit(*ladder_point(side, v)), Fraction(1)])
        for side, v in corners
    ]
    return projective_transform(src, dst)


def sample(low: Fraction, high: Fraction, count: int) -> List[Fraction]:
    return [low + (high - low) * Fraction(k, count) for k in range(count + 1)]


def scene():
    v_star = crossover()
    eps = Fraction(1, 10**6)
    floor_map = projectivity(
        [
            (Fraction(-1), Fraction(0)),
            (Fraction(1), Fraction(0)),
            (Fraction(1), v_star - eps),
            (Fraction(-1), v_star - eps),
        ]
    )
    wall_map = projectivity(
        [
            (Fraction(-1), v_star + eps),
            (Fraction(1), v_star + eps),
            (Fraction(1), Fraction(1)),
            (Fraction(-1), Fraction(1)),
        ]
    )

    def map_point(side: Fraction, v: Fraction) -> Flat:
        transform = floor_map if v < v_star else wall_map
        return as_flat(transform.apply_point(homogeneous(side, v)))

    rails = [
        [map_point(Fraction(side), v) for v in sample(Fraction(0), Fraction(1), 120)]
        for side in (-1, 1)
    ]
    rungs = [
        (map_point(Fraction(-1), Fraction(k, RUNGS)), map_point(Fraction(1), Fraction(k, RUNGS)))
        for k in range(1, RUNGS)
    ]
    return rails, rungs


def render(
    width: int,
    height: int,
    rails: List[List[Flat]],
    rungs: List[Tuple[Flat, Flat]],
    horizon: bool,
    footnote: str,
) -> str:
    pts = [p for rail in rails for p in rail] + [p for a, b in rungs for p in (a, b)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    scale = min(
        Fraction(width - 90, 1) / (max_x - min_x),
        Fraction(height - 120, 1) / (max_y - min_y),
    )
    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2

    def px(p: Flat) -> Tuple[int, int]:
        return (
            round_frac((p[0] - cx) * scale + Fraction(width, 2)),
            round_frac(-(p[1] - cy) * scale + Fraction(height, 2)),
        )

    doc = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<title>Fold-a-ladder trick art</title>",
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
    ]
    for rail in rails:
        coords = " ".join(f"{x},{y}" for x, y in (px(p) for p in rail))
        doc.append(f'<polyline points="{coords}" fill="none" stroke="{INK}" stroke-width="4"/>')
    for a_flat, b_flat in rungs:
        a, b = px(a_flat), px(b_flat)
        doc.append(
            f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="3"/>'
        )
    if horizon:
        a, b = px((min_x - 1, Fraction(0))), px((max_x + 1, Fraction(0)))
        doc.append(
            f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" '
            f'stroke="{FOLD}" stroke-width="2" stroke-dasharray="12,8"/>'
        )
    doc.append(
        f'<text x="22" y="{height - 22}" font-family="sans-serif" font-size="15" fill="#555555">{footnote}</text>'
    )
    doc.append("</svg>")
    doc.append("")
    return "\n".join(doc)


def build_view() -> str:
    def vhit(side: Fraction, v: Fraction) -> Flat:
        px, py, pz = ladder_point(side, v)
        t = (VIEW_PLANE_Y - VY) / (py - VY)
        return VX + t * (px - VX), VZ + t * (pz - VZ)

    rails = [
        [vhit(Fraction(side), v) for v in sample(Fraction(0), Fraction(1), 40)]
        for side in (-1, 1)
    ]
    rungs = [
        (vhit(Fraction(-1), Fraction(k, RUNGS)), vhit(Fraction(1), Fraction(k, RUNGS)))
        for k in range(1, RUNGS)
    ]
    return render(
        VIEW_W,
        VIEW_H,
        rails,
        rungs,
        False,
        "The same sheet seen from the viewpoint once folded.",
    )


def main() -> None:
    out = Path(__file__).resolve().parent
    rails, rungs = scene()
    documents = {
        "fold_ladder.svg": render(
            FLAT_W,
            FLAT_H,
            rails,
            rungs,
            True,
            "Fold 90 degrees along the dashed horizon, then view from V.",
        ),
        "fold_ladder_view.svg": build_view(),
    }
    for name, document in documents.items():
        (out / name).write_text(document, encoding="utf-8")
        print(f"wrote {name} ({len(document)} bytes)")


if __name__ == "__main__":
    main()
