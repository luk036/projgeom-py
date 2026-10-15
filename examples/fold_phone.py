"""Render a foldable-phone demo: a rotating 3-D chair shown on a 90-degree screen.

A foldable phone is folded to 90 degrees so its two halves form the corner of the
fold-anamorphosis (one half lies down as the floor plane, the other stands up as
the wall plane). The chair is projected onto the two halves from the viewpoint V,
so from V it reads as a solid chair -- and because the screen is a screen, the
chair can spin. In mode ``flat`` the screen stays unfolded, so the same content
warps wildly as the chair turns (the "before"); in mode ``folded`` the screen is
bent to 90 degrees and the same content reads as a solid rotating chair.

Usage::

    python examples/fold_phone.py [out.mp4] [flat|folded]
"""

import math
import subprocess
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon as MPolygon  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import chair_flat as cf  # noqa: E402

FPS = 24
SIZE = 1080
SPIN_SECONDS = 8.0

V = (float(cf.VX), float(cf.VY), float(cf.VZ))
SCREEN = "#fbfbfd"
BODY = "#2b3440"
INK = "#111111"

Vec3 = Tuple[float, float, float]
Pt2 = Tuple[float, float]


def sigma(p: Vec3) -> float:
    return V[2] * p[1] - V[1] * p[2]


def project(p: Vec3) -> Pt2:
    if sigma(p) <= 0.0:
        t = V[1] / (V[1] - p[1])
        return (V[0] + t * (p[0] - V[0]), V[2] + t * (p[2] - V[2]))
    t = V[2] / (V[2] - p[2])
    return (V[0] + t * (p[0] - V[0]), -(V[1] + t * (p[1] - V[1])))


def lerp3(a: Vec3, b: Vec3, t: float) -> Vec3:
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), a[2] + t * (b[2] - a[2]))


def clip(poly: Sequence[Vec3], keep: float) -> List[Vec3]:
    out: List[Vec3] = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        sa, sb = keep * sigma(a), keep * sigma(b)
        if sa >= 0.0:
            out.append(a)
        if (sa > 0.0 > sb) or (sa < 0.0 < sb):
            out.append(lerp3(a, b, sa / (sa - sb)))
    return out


def face_pieces(poly: Sequence[Vec3]) -> List[List[Vec3]]:
    if all(sigma(p) <= 0.0 for p in poly) or all(sigma(p) >= 0.0 for p in poly):
        return [list(poly)]
    pieces = []
    for keep in (1.0, -1.0):
        piece = clip(poly, keep)
        if len(piece) >= 3:
            pieces.append(piece)
    return pieces


def edge_segments(a: Vec3, b: Vec3) -> List[Tuple[Vec3, Vec3]]:
    sa, sb = sigma(a), sigma(b)
    if sa == 0.0 or sb == 0.0 or (sa > 0.0) == (sb > 0.0):
        return [(a, b)]
    mid = lerp3(a, b, sa / (sa - sb))
    return [(a, mid), (mid, b)]


def rotate(p: Vec3, theta: float, cx: float, cy: float) -> Vec3:
    x, y = p[0] - cx, p[1] - cy
    return (cx + x * math.cos(theta) - y * math.sin(theta), cy + x * math.sin(theta) + y * math.cos(theta), p[2])


def fold(uv: Pt2, alpha: float) -> Vec3:
    u, v = uv
    if v >= 0.0:
        return (u, -v * math.cos(alpha), v * math.sin(alpha))
    return (u, -v, 0.0)


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(a: Vec3) -> Vec3:
    n = math.sqrt(dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


FWD = unit(sub((0.0, 30.0, 34.0), V))
RIGHT = unit(cross((0.0, 0.0, 1.0), FWD))
UP = unit(cross(FWD, RIGHT))


def screen(p: Vec3) -> Pt2:
    w = sub(p, V)
    den = dot(w, FWD) or 1e-9
    return (dot(w, RIGHT) / den, dot(w, UP) / den)


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "fold-phone.mp4"
    mode = sys.argv[2] if len(sys.argv) > 2 else "folded"
    alpha = 0.0 if mode == "flat" else math.pi / 2

    chair_faces = [(color, [(float(p[0]), float(p[1]), float(p[2])) for p in poly]) for color, poly in cf.faces()]
    chair_edges = [((float(a[0]), float(a[1]), float(a[2])), (float(b[0]), float(b[1]), float(b[2]))) for a, b in cf.edges()]
    xs = [p[0] for _c, poly in chair_faces for p in poly]
    ys = [p[1] for _c, poly in chair_faces for p in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

    def sheet_bbox() -> Tuple[float, float, float, float]:
        us: List[float] = []
        vs: List[float] = []
        for theta in [k * math.pi / 6 for k in range(12)]:
            for _c, poly in chair_faces:
                for piece in face_pieces([rotate(p, theta, cx, cy) for p in poly]):
                    for p in piece:
                        u, v = project(p)
                        us.append(u)
                        vs.append(v)
            for a, b in chair_edges:
                for seg in edge_segments(rotate(a, theta, cx, cy), rotate(b, theta, cx, cy)):
                    for p in seg:
                        u, v = project(p)
                        us.append(u)
                        vs.append(v)
        return min(us), max(us), min(vs), max(vs)

    umin, umax, vmin, vmax = sheet_bbox()
    margin = 4.0
    pad = 3.0
    depth = max(-vmin, vmax) + margin
    x0, x1 = umin - pad, umax + pad
    b = 6.0
    floor_sheet = [(x0, -depth), (x1, -depth), (x1, 0.0), (x0, 0.0)]
    wall_sheet = [(x0, 0.0), (x1, 0.0), (x1, depth), (x0, depth)]
    floor_body = [(x0 - b, -depth - b), (x1 + b, -depth - b), (x1 + b, 0.0), (x0 - b, 0.0)]
    wall_body = [(x0 - b, 0.0), (x1 + b, 0.0), (x1 + b, depth + b), (x0 - b, depth + b)]

    pts = [screen(fold(project(p), alpha)) for _c, poly in chair_faces for p in poly]
    for rect in (floor_sheet, wall_sheet, floor_body, wall_body):
        pts.extend(screen(fold(p, alpha)) for p in rect)
    allx = [p[0] for p in pts]
    ally = [p[1] for p in pts]
    scx, scy = (min(allx) + max(allx)) / 2, (min(ally) + max(ally)) / 2
    half = max(max(allx) - min(allx), max(ally) - min(ally)) * 0.62
    xlim, ylim = (scx - half, scx + half), (scy - half, scy + half)

    fig = plt.figure(figsize=(SIZE / 100, SIZE / 100), dpi=100)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.set_axis_off()
    fig.patch.set_facecolor("#eef1f4")

    total = SPIN_SECONDS
    n_frames = int(total * FPS)
    ffmpeg = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        "-movflags", "+faststart", str(out),
    ]
    proc = subprocess.Popen(ffmpeg, stdin=subprocess.PIPE)

    for i in range(n_frames):
        t = i / FPS
        theta = t / SPIN_SECONDS * 2.0 * math.pi

        ax.clear()
        ax.set_axis_off()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")

        ax.add_patch(MPolygon([screen(fold(p, alpha)) for p in floor_body], closed=True, facecolor=BODY, edgecolor="none", zorder=1))
        ax.add_patch(MPolygon([screen(fold(p, alpha)) for p in wall_body], closed=True, facecolor=BODY, edgecolor="none", zorder=1))
        ax.add_patch(MPolygon([screen(fold(p, alpha)) for p in floor_sheet], closed=True, facecolor=SCREEN, edgecolor="#d7dde4", linewidth=1.0, zorder=2))
        ax.add_patch(MPolygon([screen(fold(p, alpha)) for p in wall_sheet], closed=True, facecolor=SCREEN, edgecolor="#d7dde4", linewidth=1.0, zorder=2))

        rotating = [(color, [rotate(p, theta, cx, cy) for p in poly]) for color, poly in chair_faces]
        pieces = []
        for color, poly in rotating:
            for piece in face_pieces(poly):
                pieces.append((color, piece))
        order = sorted(range(len(pieces)), key=lambda k: -_depth(pieces[k][1]))
        for k in order:
            color, piece = pieces[k]
            ax.add_patch(MPolygon([screen(fold(project(p), alpha)) for p in piece], closed=True, facecolor=color, edgecolor="none", zorder=3))
        for a, b in chair_edges:
            for seg in edge_segments(rotate(a, theta, cx, cy), rotate(b, theta, cx, cy)):
                pa, pb = screen(fold(project(seg[0]), alpha)), screen(fold(project(seg[1]), alpha))
                ax.plot([pa[0], pb[0]], [pa[1], pb[1]], color=INK, linewidth=1.1, solid_capstyle="round", zorder=4)

        fig.canvas.draw()
        assert proc.stdin is not None
        fig.savefig(proc.stdin, format="png")

    assert proc.stdin is not None
    proc.stdin.close()
    proc.wait()
    print(f"wrote {out} ({n_frames} frames, {total:.1f}s)")


def _depth(poly: Sequence[Vec3]) -> float:
    gx = sum(p[0] for p in poly) / len(poly)
    gy = sum(p[1] for p in poly) / len(poly)
    gz = sum(p[2] for p in poly) / len(poly)
    d = sub((gx, gy, gz), V)
    return dot(d, d)


if __name__ == "__main__":
    main()
