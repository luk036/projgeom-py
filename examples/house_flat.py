"""Fold-a-house trick art: a 3D house anamorphosed onto a foldable sheet.

Companion to ``chair_flat.py`` / ``table_flat.py``.  A little house stands in the
right-angle corner between a **floor** (``z = 0``) and a **wall** (``y = 0``)
meeting along the crease (the ``x`` axis).  A viewer at ``V`` sees each point of
the house recorded on whichever plane its sight ray reaches first; the two
planes are then unfolded into one flat sheet.  Print the sheet, fold it 90
degrees and, from ``V``, the flat drawing reads as the solid house.

The plane reached first is decided by the linear form

.. math::

    \\sigma(P) = V_z\\,P_y - V_y\\,P_z,

(``\\sigma < 0`` -> wall flap, ``\\sigma > 0`` -> floor flap).  Faces and edges
that straddle ``\\sigma = 0`` are clipped there and each piece projected onto its
own plane, so the sloped roof and the triangular gable come out correctly.
Unfolding is ``(x, 0, z) -> (x, z)`` on the wall and ``(x, y, 0) -> (x, -y)``
on the floor, so ``v = 0`` is the crease.

The sheet is A4 portrait (210 mm x 297 mm), sized in millimetres and exact in
:class:`fractions.Fraction` -- no floating point.

Usage::

    python examples/house_flat.py
"""

from fractions import Fraction
from pathlib import Path
from typing import List, Sequence, Tuple

from projgeom import PgPoint, projective_transform

VX = Fraction(-150)
VY = Fraction(280)
VZ = Fraction(240)

HW = Fraction(40)
X0, X1 = -HW, HW
HY0 = Fraction(38)
HY1 = Fraction(100)
MID_Y = (HY0 + HY1) / 2
WALL_Z = Fraction(80)
RIDGE_Z = Fraction(116)
DOOR_W = Fraction(11)
DOOR_H = Fraction(42)
WIN_X0, WIN_X1 = Fraction(13), Fraction(31)
WIN_Z0, WIN_Z1 = Fraction(52), Fraction(66)
EPS = Fraction(1, 2)

PAPER = "#ffffff"
WALL = "#ece5d6"
SIDE = "#cec4ab"
ROOF = "#b5523a"
DOOR = "#7a4a2b"
WIN = "#8fd0e8"
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
    """Central projection of ``point`` onto the nearer plane, then unfolded."""
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
    yf, yb, z0 = HY1, HY0, Fraction(0)
    return [
        (WALL, [(X0, yf, z0), (X1, yf, z0), (X1, yf, WALL_Z), (X0, yf, WALL_Z)]),
        (SIDE, [(X0, yb, z0), (X0, yf, z0), (X0, yf, WALL_Z), (X0, yb, WALL_Z)]),
        (SIDE, [(X0, yb, WALL_Z), (X0, yf, WALL_Z), (X0, MID_Y, RIDGE_Z)]),
        (ROOF, [(X0, yf, WALL_Z), (X1, yf, WALL_Z), (X1, MID_Y, RIDGE_Z), (X0, MID_Y, RIDGE_Z)]),
        (DOOR, [(-DOOR_W, yf + EPS, z0), (DOOR_W, yf + EPS, z0), (DOOR_W, yf + EPS, DOOR_H), (-DOOR_W, yf + EPS, DOOR_H)]),
        (WIN, [(WIN_X0, yf + EPS, WIN_Z0), (WIN_X1, yf + EPS, WIN_Z0), (WIN_X1, yf + EPS, WIN_Z1), (WIN_X0, yf + EPS, WIN_Z1)]),
    ]


def edges() -> List[Edge]:
    yf, yb, z0 = HY1, HY0, Fraction(0)
    segs: List[Edge] = [
        ((X0, yb, z0), (X1, yb, z0)),
        ((X1, yb, z0), (X1, yf, z0)),
        ((X1, yf, z0), (X0, yf, z0)),
        ((X0, yf, z0), (X0, yb, z0)),
        ((X0, yf, z0), (X0, yf, WALL_Z)),
        ((X1, yf, z0), (X1, yf, WALL_Z)),
        ((X0, yb, z0), (X0, yb, WALL_Z)),
        ((X0, yb, WALL_Z), (X0, yf, WALL_Z)),
        ((X0, yf, WALL_Z), (X1, yf, WALL_Z)),
        ((X0, yb, WALL_Z), (X0, MID_Y, RIDGE_Z)),
        ((X0, MID_Y, RIDGE_Z), (X0, yf, WALL_Z)),
        ((X0, MID_Y, RIDGE_Z), (X1, MID_Y, RIDGE_Z)),
        ((X1, MID_Y, RIDGE_Z), (X1, yf, WALL_Z)),
        ((-DOOR_W, yf, z0), (DOOR_W, yf, z0)),
        ((-DOOR_W, yf, z0), (-DOOR_W, yf, DOOR_H)),
        ((DOOR_W, yf, z0), (DOOR_W, yf, DOOR_H)),
        ((-DOOR_W, yf, DOOR_H), (DOOR_W, yf, DOOR_H)),
        ((WIN_X0, yf, WIN_Z0), (WIN_X1, yf, WIN_Z0)),
        ((WIN_X0, yf, WIN_Z1), (WIN_X1, yf, WIN_Z1)),
        ((WIN_X0, yf, WIN_Z0), (WIN_X0, yf, WIN_Z1)),
        ((WIN_X1, yf, WIN_Z0), (WIN_X1, yf, WIN_Z1)),
    ]
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
    """Check the fold: every drawn sheet point and its house point share a ray."""
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
        "<title>Fold-a-house trick art</title>",
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
    render(root / "house_flat.svg")
    print("wrote house_flat.svg")


if __name__ == "__main__":
    main()
