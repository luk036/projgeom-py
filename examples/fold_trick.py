"""Fold trick-art: exact-rational two-plane anamorphosis on a foldable sheet.

Python mirror of ``examples/fold_trick.cpp``.  A viewer ``V`` looks at an object
standing in the right-angle corner between a **floor** (``z = 0``) and a **wall**
(``y = 0``) that meet along the crease (the ``x`` axis).  Every object point is
recorded on whichever plane its sight ray reaches first; the planes are then
unfolded into one flat sheet.  The plane reached first is decided by the linear
form

.. math::

    \\sigma(P) = V_z\\,P_y - V_y\\,P_z \\qquad (< 0 \\text{ wall flap},\\ > 0 \\text{ floor flap}).

Every coordinate is an exact :class:`fractions.Fraction`, and the face maps use
:func:`projgeom.projective_transform`, so the sheets are reproducible and
printable at 100%.

Usage::

    python examples/fold_trick.py [outdir]
"""

import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import List, Sequence, Tuple

from projgeom import PgPoint, projective_transform

SHEET_W = Fraction(210)
SHEET_H = Fraction(297)
PX_PER_MM = 4
MARGIN = Fraction(16)

PAPER = "#ffffff"
INK = "#111111"
CREASE = "#d21f1f"

Vec3 = Tuple[Fraction, Fraction, Fraction]
Pt2 = Tuple[Fraction, Fraction]
Face = Tuple[str, List[Vec3]]
Edge = Tuple[Vec3, Vec3]
Piece = Tuple[List[Vec3], List[Pt2]]

UNIT_SQUARE = [PgPoint([0, 0, 1]), PgPoint([1, 0, 1]), PgPoint([1, 1, 1]), PgPoint([0, 1, 1])]


@dataclass
class Scene:
    """Viewer position, planar faces, edges and title of one fold trick-art object."""

    vx: Fraction
    vy: Fraction
    vz: Fraction
    faces: List[Face]
    edges: List[Edge]
    title: str
    filename: str


@dataclass
class Fit:
    """Uniform scale and offsets that map the sheet coordinates onto A4."""

    scale: Fraction
    off_u: Fraction
    off_v: Fraction


def round_frac(value: Fraction) -> int:
    """Round a rational to the nearest integer, halves away from zero."""
    num, den = value.numerator, value.denominator
    whole, rest = divmod(num, den)
    if 2 * rest >= den:
        whole += 1
    return whole


def sigma(scene: Scene, point: Vec3) -> Fraction:
    r"""Wall/floor classifier :math:`\sigma(P) = V_z P_y - V_y P_z`."""
    return scene.vz * point[1] - scene.vy * point[2]


def project(scene: Scene, point: Vec3) -> Pt2:
    """Central projection of ``point`` onto the nearer plane, then unfolded."""
    px, py, pz = point
    if sigma(scene, point) <= 0:
        t = scene.vy / (scene.vy - py)
        return scene.vx + t * (px - scene.vx), scene.vz + t * (pz - scene.vz)
    t = scene.vz / (scene.vz - pz)
    return scene.vx + t * (px - scene.vx), -(scene.vy + t * (py - scene.vy))


def to_pg(point: Pt2) -> PgPoint:
    """Build a projgeom point from a sheet coordinate (exact rationals)."""
    return PgPoint.from_fractions([point[0], point[1], Fraction(1)])


def from_pg(point: PgPoint) -> Pt2:
    """Return the Euclidean sheet coordinate of a projgeom point."""
    x, y, z = (Fraction(c) for c in point.coord)
    return x / z, y / z


def lerp3(a: Vec3, b: Vec3, t: Fraction) -> Vec3:
    """Linear interpolation between two 3-D points."""
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), a[2] + t * (b[2] - a[2]))


def clip_half(scene: Scene, poly: Sequence[Vec3], keep: Fraction) -> List[Vec3]:
    """Sutherland-Hodgman half-plane clip of ``poly`` on :math:`\\sigma = 0`."""
    out: List[Vec3] = []
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        sa, sb = keep * sigma(scene, a), keep * sigma(scene, b)
        if sa >= 0:
            out.append(a)
        if (sa > 0 > sb) or (sa < 0 < sb):
            out.append(lerp3(a, b, sa / (sa - sb)))
    return out


def face_pieces(scene: Scene, corners: Sequence[Vec3]) -> List[Piece]:
    """Return each piece of a face with its sheet polygon, splitting at the crease."""
    if all(sigma(scene, p) <= 0 for p in corners) or all(sigma(scene, p) >= 0 for p in corners):
        dst = [to_pg(project(scene, p)) for p in corners]
        try:
            transform = projective_transform(UNIT_SQUARE, dst)
            return [(list(corners), [from_pg(transform.apply_point(q)) for q in UNIT_SQUARE])]
        except Exception:
            return [(list(corners), [project(scene, p) for p in corners])]
    pieces: List[Piece] = []
    for keep in (Fraction(1), Fraction(-1)):
        piece = clip_half(scene, corners, keep)
        if len(piece) >= 3:
            pieces.append((piece, [project(scene, p) for p in piece]))
    return pieces


def edge_segments(scene: Scene, a: Vec3, b: Vec3) -> List[Edge]:
    """Split an edge at the crease plane so it bends rather than jumping across."""
    sa, sb = sigma(scene, a), sigma(scene, b)
    if sa == 0 or sb == 0 or (sa > 0) == (sb > 0):
        return [(a, b)]
    mid = lerp3(a, b, sa / (sa - sb))
    return [(a, mid), (mid, b)]


def depth2(scene: Scene, centroid: Vec3) -> Fraction:
    """Squared Euclidean distance from the viewer (a square-root-free depth key)."""
    dx, dy, dz = centroid[0] - scene.vx, centroid[1] - scene.vy, centroid[2] - scene.vz
    return dx * dx + dy * dy + dz * dz


def centroid(poly: Sequence[Vec3]) -> Vec3:
    """Mean of the vertices of a polygon."""
    n = Fraction(len(poly))
    return (sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n, sum(p[2] for p in poly) / n)


def make_fit(points: Sequence[Pt2]) -> Fit:
    """Compute the uniform A4 fit for a set of sheet points."""
    us = [p[0] for p in points]
    vs = [p[1] for p in points]
    span_u = max(max(us) - min(us), Fraction(1))
    span_v = max(max(vs) - min(vs), Fraction(1))
    scale = min((SHEET_W - 2 * MARGIN) / span_u, (SHEET_H - 2 * MARGIN) / span_v)
    off_u = MARGIN + (SHEET_W - 2 * MARGIN - span_u * scale) / 2 - min(us) * scale
    off_v = MARGIN + (SHEET_H - 2 * MARGIN - span_v * scale) / 2 - min(vs) * scale
    return Fit(scale, off_u, off_v)


def to_px(point: Pt2, fit: Fit) -> Tuple[int, int]:
    """Map a sheet coordinate to integer SVG pixels (millimetres at 100%)."""
    u = point[0] * fit.scale + fit.off_u
    v = point[1] * fit.scale + fit.off_v
    return round_frac(u * PX_PER_MM), round_frac((SHEET_H - v) * PX_PER_MM)


def verify(scene: Scene) -> None:
    """Check the fold: every drawn sheet point and its object point share a ray."""
    vxz = PgPoint.from_fractions([scene.vx, scene.vz, Fraction(1)])
    vyz = PgPoint.from_fractions([scene.vy, scene.vz, Fraction(1)])
    for _, poly in scene.faces:
        for corner in poly:
            px, py, pz = corner
            u, v = project(scene, corner)
            fx, fy, fz = (u, Fraction(0), v) if v >= 0 else (u, -v, Fraction(0))
            pxz, fxz = PgPoint.from_fractions([px, pz, Fraction(1)]), PgPoint.from_fractions([fx, fz, Fraction(1)])
            pyz, fyz = PgPoint.from_fractions([py, pz, Fraction(1)]), PgPoint.from_fractions([fy, fz, Fraction(1)])
            if not pxz.incident(vxz.meet(fxz)) or not pyz.incident(vyz.meet(fyz)):
                raise AssertionError(f"point {corner} is not on the ray through {fx, fy, fz}")


def render(scene: Scene) -> str:
    """Return the SVG document for a scene (faces back to front, then edges)."""
    pieces: List[Tuple[Vec3, str, List[Pt2]]] = []
    for color, poly in scene.faces:
        for poly3d, poly2d in face_pieces(scene, poly):
            pieces.append((centroid(poly3d), color, poly2d))
    order = sorted(range(len(pieces)), key=lambda i: depth2(scene, pieces[i][0]), reverse=True)

    edge_list = [(project(scene, seg[0]), project(scene, seg[1])) for a, b in scene.edges for seg in edge_segments(scene, a, b)]
    all_pts = [pt for _, _, poly in pieces for pt in poly]
    for pa, pb in edge_list:
        all_pts.append(pa)
        all_pts.append(pb)
    fit = make_fit(all_pts)

    doc = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_W}mm" height="{SHEET_H}mm" viewBox="0 0 {round_frac(SHEET_W * PX_PER_MM)} {round_frac(SHEET_H * PX_PER_MM)}">',
        f"<title>{scene.title}</title>",
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
    ]
    for idx in order:
        _, color, poly = pieces[idx]
        pts = " ".join(f"{to_px(pt, fit)[0]},{to_px(pt, fit)[1]}" for pt in poly)
        doc.append(f'<polygon points="{pts}" fill="{color}" stroke="none"/>')
    for pa, pb in edge_list:
        a, b = to_px(pa, fit), to_px(pb, fit)
        doc.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="2"/>')
    crease_lo = to_px((min(pt[0] for pt in all_pts) - Fraction(14), Fraction(0)), fit)
    crease_hi = to_px((max(pt[0] for pt in all_pts) + Fraction(14), Fraction(0)), fit)
    doc.append(f'<line x1="{crease_lo[0]}" y1="{crease_lo[1]}" x2="{crease_hi[0]}" y2="{crease_hi[1]}" stroke="{CREASE}" stroke-width="2" stroke-dasharray="12 8"/>')
    doc.append(f'<text x="{crease_hi[0]}" y="{crease_hi[1] - 8}" font-size="20" fill="{CREASE}" text-anchor="end">fold here (crease)</text>')
    doc.append("</svg>")
    doc.append("")
    return "\n".join(doc)


def make_chair() -> Scene:
    """Build the chair scene (corner coordinates, viewer ``V``)."""
    x0, x1 = Fraction(-30), Fraction(30)
    z, t, y0, y1, top, gb, st, lg = Fraction(55), Fraction(10), Fraction(64), Fraction(104), Fraction(103), Fraction(83), Fraction(5), Fraction(3)
    z0 = Fraction(0)
    faces: List[Face] = [
        ("#3aa93a", [(x0 + st, y0, gb), (x1 - st, y0, gb), (x1 - st, y0, top - st), (x0 + st, y0, top - st)]),
        ("#e2701f", [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]),
        ("#b4d9ea", [(x0, y1, z - t), (x1, y1, z - t), (x1, y1, z), (x0, y1, z)]),
        ("#1f6fd0", [(x0, y0, z - t), (x0, y1, z - t), (x0, y1, z), (x0, y0, z)]),
    ]
    edges: List[Edge] = [
        ((x0, y0, z), (x0, y0, top)),
        ((x1, y0, z), (x1, y0, top)),
        ((x0, y0, top), (x1, y0, top)),
        ((x0, y0, gb), (x1, y0, gb)),
        ((x0, y0, z), (x1, y0, z)),
        ((x1, y0, z), (x1, y1, z)),
        ((x1, y1, z), (x0, y1, z)),
        ((x0, y1, z), (x0, y0, z)),
        ((x0, y1, z - t), (x1, y1, z - t)),
        ((x0, y0, z - t), (x0, y1, z - t)),
        ((x0, y1, z - t), (x0, y1, z)),
        ((x1, y1, z - t), (x1, y1, z)),
    ]
    for lx in (x0 + lg / 2, x1 - lg / 2):
        for ly in (y0 + lg / 2, y1 - lg / 2):
            edges.append(((lx, ly, z - t), (lx, ly, z0)))
            edges.append(((lx - lg / 2, ly, z0), (lx + lg / 2, ly, z0)))
    return Scene(Fraction(-120), Fraction(280), Fraction(220), faces, edges, "Fold-a-chair trick art", "chair_flat.svg")


def make_table() -> Scene:
    """Build the table scene."""
    x0, x1 = Fraction(-50), Fraction(50)
    top, t, y0, y1, lg = Fraction(74), Fraction(8), Fraction(30), Fraction(90), Fraction(7)
    z0 = Fraction(0)
    zt, zb = top, top - t
    faces: List[Face] = [
        ("#cf7b32", [(x0, y0, zt), (x1, y0, zt), (x1, y1, zt), (x0, y1, zt)]),
        ("#e0a96d", [(x0, y1, zb), (x1, y1, zb), (x1, y1, zt), (x0, y1, zt)]),
        ("#9c5a22", [(x0, y0, zb), (x0, y1, zb), (x0, y1, zt), (x0, y0, zt)]),
    ]
    edges: List[Edge] = [
        ((x0, y0, zt), (x1, y0, zt)),
        ((x1, y0, zt), (x1, y1, zt)),
        ((x1, y1, zt), (x0, y1, zt)),
        ((x0, y1, zt), (x0, y0, zt)),
        ((x0, y1, zb), (x1, y1, zb)),
        ((x0, y0, zb), (x0, y1, zb)),
        ((x0, y1, zb), (x0, y1, zt)),
        ((x1, y1, zb), (x1, y1, zt)),
    ]
    for lx in (x0 + lg / 2, x1 - lg / 2):
        for ly in (y0 + lg / 2, y1 - lg / 2):
            edges.append(((lx, ly, zb), (lx, ly, z0)))
            edges.append(((lx - lg / 2, ly, z0), (lx + lg / 2, ly, z0)))
    return Scene(Fraction(-130), Fraction(280), Fraction(230), faces, edges, "Fold-a-table trick art", "table_flat.svg")


def make_house() -> Scene:
    """Build the house scene (walls, gable and sloped roof exercise the split faces)."""
    x0, x1 = Fraction(-40), Fraction(40)
    yb, yf = Fraction(38), Fraction(100)
    mid = (yb + yf) / 2
    wz, rz = Fraction(80), Fraction(116)
    dw, dh = Fraction(11), Fraction(42)
    wx0, wx1, wz0, wz1 = Fraction(13), Fraction(31), Fraction(52), Fraction(66)
    eps = Fraction(1, 2)
    z0 = Fraction(0)
    faces: List[Face] = [
        ("#ece5d6", [(x0, yf, z0), (x1, yf, z0), (x1, yf, wz), (x0, yf, wz)]),
        ("#cec4ab", [(x0, yb, z0), (x0, yf, z0), (x0, yf, wz), (x0, yb, wz)]),
        ("#cec4ab", [(x0, yb, wz), (x0, yf, wz), (x0, mid, rz)]),
        ("#b5523a", [(x0, yf, wz), (x1, yf, wz), (x1, mid, rz), (x0, mid, rz)]),
        ("#7a4a2b", [(-dw, yf + eps, z0), (dw, yf + eps, z0), (dw, yf + eps, dh), (-dw, yf + eps, dh)]),
        ("#8fd0e8", [(wx0, yf + eps, wz0), (wx1, yf + eps, wz0), (wx1, yf + eps, wz1), (wx0, yf + eps, wz1)]),
    ]
    edges: List[Edge] = [
        ((x0, yb, z0), (x1, yb, z0)),
        ((x1, yb, z0), (x1, yf, z0)),
        ((x1, yf, z0), (x0, yf, z0)),
        ((x0, yf, z0), (x0, yb, z0)),
        ((x0, yf, z0), (x0, yf, wz)),
        ((x1, yf, z0), (x1, yf, wz)),
        ((x0, yb, z0), (x0, yb, wz)),
        ((x0, yb, wz), (x0, yf, wz)),
        ((x0, yf, wz), (x1, yf, wz)),
        ((x0, yb, wz), (x0, mid, rz)),
        ((x0, mid, rz), (x0, yf, wz)),
        ((x0, mid, rz), (x1, mid, rz)),
        ((x1, mid, rz), (x1, yf, wz)),
        ((-dw, yf, z0), (dw, yf, z0)),
        ((-dw, yf, z0), (-dw, yf, dh)),
        ((dw, yf, z0), (dw, yf, dh)),
        ((-dw, yf, dh), (dw, yf, dh)),
        ((wx0, yf, wz0), (wx1, yf, wz0)),
        ((wx0, yf, wz1), (wx1, yf, wz1)),
        ((wx0, yf, wz0), (wx0, yf, wz1)),
        ((wx1, yf, wz0), (wx1, yf, wz1)),
    ]
    return Scene(Fraction(-150), Fraction(280), Fraction(240), faces, edges, "Fold-a-house trick art", "house_flat.svg")


def main() -> None:
    """Render all three sheets into ``argv[1]`` (default: the repository root)."""
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    out.mkdir(parents=True, exist_ok=True)
    for scene in (make_chair(), make_table(), make_house()):
        verify(scene)
        (out / scene.filename).write_text(render(scene), encoding="utf-8")
        print(f"wrote {scene.filename}")


if __name__ == "__main__":
    main()
