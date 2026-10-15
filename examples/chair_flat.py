"""Fold-a-chair trick art: a 3D chair anamorphosed onto a foldable sheet.

A chair stands in the right-angle corner between a **floor** (``z = 0``, in
front) and a **wall** (``y = 0``, rising up); they meet along the crease, the
``x`` axis.  A viewer sits at ``V`` in the room, in front of and above the
chair.  Every point ``P`` of the chair is looked at from ``V``: the sight ray
hits whichever of the two planes comes first and is recorded there.  The two
planes are then *unfolded* into one flat sheet (the wall rotates about the
crease into the floor plane).  Print that sheet, fold it back 90 degrees, and
from ``V`` each recorded point lies on the same ray as the real one, so the flat
drawing reads as the solid chair.

The sight ray through ``P`` meets the two planes at the parameters

.. math::

    t_{\\text{floor}} = \\frac{-V_z}{P_z - V_z}, \\qquad
    t_{\\text{wall}}  = \\frac{-V_y}{P_y - V_y},

so the plane reached first is decided by the *linear* form

.. math::

    \\sigma(P) = V_z\\,P_y - V_y\\,P_z .

With the viewer on the floor side (``V_y > 0``), ``\\sigma(P) < 0`` means the
wall is reached first (``P`` belongs on the wall flap) and ``\\sigma(P) > 0``
means the floor is reached first.  ``\\sigma`` is linear, so a face is split (if
at all) along the single line where it crosses ``\\sigma = 0``; every face and
edge is clipped there, and each piece is projected onto its own plane.

The crease in the picture is the line ``v = 0``, where a chair point lies on the
plane ``\\sigma = 0`` through ``V`` and the physical wall/floor corner.  Keeping
the backrest plane a little *closer* to the wall than ``y = Z_s\\,V_y/V_z``
leaves the whole backrest on the wall flap (a clean rectangle) while the crease
crosses the flat seat instead of its sharp back corner.

Unfolding maps ``(x, 0, z) -> (u, v) = (x, z)`` on the wall and
``(x, y, 0) -> (u, v) = (x, -y)`` on the floor: ``v = 0`` is the crease,
``v > 0`` the wall flap (the backrest, above) and ``v < 0`` the floor flap (the
seat, below).  The same central projection, written as a projective transform on
each face plane, maps every face onto the sheet.

The sheet is A4 portrait (210 mm x 297 mm) and the SVG is sized in millimetres
(printable at 100%).  Every coordinate is an exact :class:`fractions.Fraction`;
no floating point is used.

Usage::

    python examples/chair_flat.py
"""

from fractions import Fraction
from pathlib import Path
from typing import List, Sequence, Tuple

from projgeom import PgPoint, projective_transform

VX = Fraction(-120)
VY = Fraction(280)
VZ = Fraction(220)

WIDTH = Fraction(60)
X0, X1 = -WIDTH / 2, WIDTH / 2
SEAT_Z = Fraction(55)
SEAT_T = Fraction(10)
SEAT_Y0 = Fraction(64)
SEAT_Y1 = Fraction(104)
BACK_TOP = Fraction(103)
GREEN_BOT = Fraction(83)
STILE = Fraction(5)
LEG = Fraction(3)

PAPER = "#ffffff"
GREEN = "#3aa93a"
ORANGE = "#e2701f"
LIGHT = "#b4d9ea"
BLUE = "#1f6fd0"
INK = "#111111"
CREASE = "#d21f1f"

SHEET_W = Fraction(210)
SHEET_H = Fraction(297)
PX_PER_MM = 4
MARGIN = Fraction(16)

Vec3 = Tuple[Fraction, Fraction, Fraction]
Pt2 = Tuple[Fraction, Fraction]
Face = Tuple[str, List[Vec3]]
Edge = Tuple[Vec3, Vec3]
Fit = Tuple[Fraction, Fraction, Fraction]

UNIT_SQUARE = [PgPoint([0, 0, 1]), PgPoint([1, 0, 1]), PgPoint([1, 1, 1]), PgPoint([0, 1, 1])]


def round_frac(value: Fraction) -> int:
    num, den = value.numerator, value.denominator
    whole, rest = divmod(num, den)
    if 2 * rest >= den:
        whole += 1
    return whole


def sigma(point: Vec3) -> Fraction:
    r"""Wall/floor classifier :math:`\sigma(P) = V_z P_y - V_y P_z`."""
    return VZ * point[1] - VY * point[2]


def project(point: Vec3) -> Pt2:
    """Central projection of ``point`` onto the nearer plane, then unfolded.

    Returns flat-sheet coordinates ``(u, v)`` in millimetres, with the crease at
    ``v = 0``, the wall flap at ``v > 0`` and the floor flap at ``v < 0``.
    """
    px, py, pz = point
    if sigma(point) <= 0:
        t = VY / (VY - py)
        return VX + t * (px - VX), VZ + t * (pz - VZ)
    t = VZ / (VZ - pz)
    return VX + t * (px - VX), -(VY + t * (py - VY))


def _pg(point: Pt2) -> PgPoint:
    return PgPoint.from_fractions([point[0], point[1], Fraction(1)])


def _xy(point: PgPoint) -> Pt2:
    x, y, z = (Fraction(c) for c in point.coord)
    return x / z, y / z


def _lerp3(a: Vec3, b: Vec3, t: Fraction) -> Vec3:
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), a[2] + t * (b[2] - a[2]))


def _clip(poly: Sequence[Vec3], keep: Fraction) -> List[Vec3]:
    out: List[Vec3] = []
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        sa, sb = keep * sigma(a), keep * sigma(b)
        if sa >= 0:
            out.append(a)
        if (sa > 0 > sb) or (sa < 0 < sb):
            out.append(_lerp3(a, b, sa / (sa - sb)))
    return out


def face_pieces(corners: Sequence[Vec3]) -> List[Tuple[List[Vec3], List[Pt2]]]:
    """Return each piece of a face with its sheet polygon, splitting at the crease."""
    if all(sigma(p) <= 0 for p in corners) or all(sigma(p) >= 0 for p in corners):
        dst = [_pg(project(p)) for p in corners]
        try:
            transform = projective_transform(UNIT_SQUARE, dst)
            return [(list(corners), [_xy(transform.apply_point(q)) for q in UNIT_SQUARE])]
        except Exception:
            return [(list(corners), [project(p) for p in corners])]
    pieces = []
    for keep in (Fraction(1), Fraction(-1)):
        piece = _clip(corners, keep)
        if len(piece) >= 3:
            pieces.append((piece, [project(p) for p in piece]))
    return pieces


def edge_segments(a: Vec3, b: Vec3) -> List[Edge]:
    """Split an edge at the crease plane so it bends rather than jumping across."""
    sa, sb = sigma(a), sigma(b)
    if sa == 0 or sb == 0 or (sa > 0) == (sb > 0):
        return [(a, b)]
    mid = _lerp3(a, b, sa / (sa - sb))
    return [(a, mid), (mid, b)]


def depth2(point: Vec3) -> Fraction:
    dx, dy, dz = point[0] - VX, point[1] - VY, point[2] - VZ
    return dx * dx + dy * dy + dz * dz


def _centroid(poly: Sequence[Vec3]) -> Vec3:
    n = Fraction(len(poly))
    return (
        sum(p[0] for p in poly) / n,
        sum(p[1] for p in poly) / n,
        sum(p[2] for p in poly) / n,
    )


def faces() -> List[Face]:
    yb, zl, zt = SEAT_Y0, SEAT_Z - SEAT_T, SEAT_Z
    return [
        (
            GREEN,
            [
                (X0 + STILE, yb, GREEN_BOT),
                (X1 - STILE, yb, GREEN_BOT),
                (X1 - STILE, yb, BACK_TOP - STILE),
                (X0 + STILE, yb, BACK_TOP - STILE),
            ],
        ),
        (
            ORANGE,
            [(X0, SEAT_Y0, zt), (X1, SEAT_Y0, zt), (X1, SEAT_Y1, zt), (X0, SEAT_Y1, zt)],
        ),
        (
            LIGHT,
            [(X0, SEAT_Y1, zl), (X1, SEAT_Y1, zl), (X1, SEAT_Y1, zt), (X0, SEAT_Y1, zt)],
        ),
        (
            BLUE,
            [(X0, SEAT_Y0, zl), (X0, SEAT_Y1, zl), (X0, SEAT_Y1, zt), (X0, SEAT_Y0, zt)],
        ),
    ]


def edges() -> List[Edge]:
    yb, z0, zl = SEAT_Y0, Fraction(0), SEAT_Z - SEAT_T
    segs: List[Edge] = [
        ((X0, yb, SEAT_Z), (X0, yb, BACK_TOP)),
        ((X1, yb, SEAT_Z), (X1, yb, BACK_TOP)),
        ((X0, yb, BACK_TOP), (X1, yb, BACK_TOP)),
        ((X0, yb, GREEN_BOT), (X1, yb, GREEN_BOT)),
        ((X0, SEAT_Y0, SEAT_Z), (X1, SEAT_Y0, SEAT_Z)),
        ((X1, SEAT_Y0, SEAT_Z), (X1, SEAT_Y1, SEAT_Z)),
        ((X1, SEAT_Y1, SEAT_Z), (X0, SEAT_Y1, SEAT_Z)),
        ((X0, SEAT_Y1, SEAT_Z), (X0, SEAT_Y0, SEAT_Z)),
        ((X0, SEAT_Y1, zl), (X1, SEAT_Y1, zl)),
        ((X0, SEAT_Y0, zl), (X0, SEAT_Y1, zl)),
        ((X0, SEAT_Y1, zl), (X0, SEAT_Y1, SEAT_Z)),
        ((X1, SEAT_Y1, zl), (X1, SEAT_Y1, SEAT_Z)),
    ]
    for lx in (X0 + LEG / 2, X1 - LEG / 2):
        for ly in (SEAT_Y0 + LEG / 2, SEAT_Y1 - LEG / 2):
            segs.append(((lx, ly, zl), (lx, ly, z0)))
            segs.append(((lx - LEG / 2, ly, z0), (lx + LEG / 2, ly, z0)))
    return segs


def _fit(points: Sequence[Pt2]) -> Fit:
    us = [p[0] for p in points]
    vs = [p[1] for p in points]
    span_u = max(max(us) - min(us), Fraction(1))
    span_v = max(max(vs) - min(vs), Fraction(1))
    scale = min((SHEET_W - 2 * MARGIN) / span_u, (SHEET_H - 2 * MARGIN) / span_v)
    off_u = MARGIN + (SHEET_W - 2 * MARGIN - span_u * scale) / 2 - min(us) * scale
    off_v = MARGIN + (SHEET_H - 2 * MARGIN - span_v * scale) / 2 - min(vs) * scale
    return scale, off_u, off_v


def _to_px(point: Pt2, fit: Fit) -> Tuple[int, int]:
    scale, off_u, off_v = fit
    u = point[0] * scale + off_u
    v = point[1] * scale + off_v
    return round_frac(u * PX_PER_MM), round_frac((SHEET_H - v) * PX_PER_MM)


def verify() -> None:
    """Check the fold: the drawn sheet point and the chair point share a ray."""
    vxz = PgPoint.from_fractions([VX, VZ, Fraction(1)])
    vyz = PgPoint.from_fractions([VY, VZ, Fraction(1)])
    for _, poly in faces():
        for corner in poly:
            px, py, pz = corner
            u, v = project(corner)
            fx, fy, fz = (u, Fraction(0), v) if v >= 0 else (u, -v, Fraction(0))
            pxz, fxz = PgPoint.from_fractions([px, pz, Fraction(1)]), PgPoint.from_fractions([fx, fz, Fraction(1)])
            pyz, fyz = PgPoint.from_fractions([py, pz, Fraction(1)]), PgPoint.from_fractions([fy, fz, Fraction(1)])
            if not pxz.incident(vxz.meet(fxz)) or not pyz.incident(vyz.meet(fyz)):
                raise AssertionError(f"point {corner} is not on the ray through {fx, fy, fz}")


def render(out: Path) -> None:
    pieces = []
    for color, poly in faces():
        for poly3d, poly2d in face_pieces(poly):
            pieces.append((_centroid(poly3d), color, poly2d))
    order = sorted(range(len(pieces)), key=lambda i: depth2(pieces[i][0]), reverse=True)

    edge_list = [
        (project(seg[0]), project(seg[1]))
        for a, b in edges()
        for seg in edge_segments(a, b)
    ]
    all_pts = [pt for _, _, poly in pieces for pt in poly]
    for pa, pb in edge_list:
        all_pts.append(pa)
        all_pts.append(pb)
    fit = _fit(all_pts)

    doc = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_W}mm" height="{SHEET_H}mm" '
        f'viewBox="0 0 {round_frac(SHEET_W * PX_PER_MM)} {round_frac(SHEET_H * PX_PER_MM)}">',
        "<title>Fold-a-chair trick art</title>",
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
    ]
    for idx in order:
        _, color, poly = pieces[idx]
        pts = " ".join(f"{_to_px(pt, fit)[0]},{_to_px(pt, fit)[1]}" for pt in poly)
        doc.append(f'<polygon points="{pts}" fill="{color}" stroke="none"/>')
    for pa, pb in edge_list:
        a, b = _to_px(pa, fit), _to_px(pb, fit)
        doc.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="2"/>')
    crease_lo = _to_px((min(pt[0] for pt in all_pts) - Fraction(14), Fraction(0)), fit)
    crease_hi = _to_px((max(pt[0] for pt in all_pts) + Fraction(14), Fraction(0)), fit)
    doc.append(f'<line x1="{crease_lo[0]}" y1="{crease_lo[1]}" x2="{crease_hi[0]}" y2="{crease_hi[1]}" stroke="{CREASE}" stroke-width="2" stroke-dasharray="12 8"/>')
    doc.append(f'<text x="{crease_hi[0]}" y="{crease_hi[1] - 8}" font-size="20" fill="{CREASE}" text-anchor="end">fold here (crease)</text>')
    doc.append("</svg>")
    doc.append("")
    out.write_text("\n".join(doc), encoding="utf-8")


def main() -> None:
    verify()
    root = Path(__file__).resolve().parent.parent
    render(root / "chair_flat.svg")
    print("wrote chair_flat.svg")


if __name__ == "__main__":
    main()
