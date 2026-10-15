"""Render a short fold-anamorphosis movie: the flat sheet folds into a 3-D object.

Reuses the exact geometry from chair_flat.py / table_flat.py / house_flat.py: the
printed sheet (an anamorphic image) is folded about the crease while a camera
stays at the viewpoint V, so at 90 degrees the drawing snaps into the solid
object. Output is an H.264 MP4 (square, phone-friendly) written next to the repo.

Usage::

    python examples/fold_anim.py [chair|table|house] [out.mp4]
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

import chair_flat  # noqa: E402
import house_flat  # noqa: E402
import table_flat  # noqa: E402

OBJECTS = {"chair": chair_flat, "table": table_flat, "house": house_flat}

FPS = 24
SIZE = 1080
FOLD_SECONDS = 3.2
HOLD_SECONDS = 1.8
UNFOLD_SECONDS = 3.2

Vec3 = Tuple[float, float, float]
Pt2 = Tuple[float, float]


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(a: Vec3) -> Vec3:
    n = math.sqrt(dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


def smoothstep(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


class Camera:
    def __init__(self, eye: Vec3, target: Vec3) -> None:
        self.eye = eye
        self.fwd = unit(sub(target, eye))
        self.right = unit(cross((0.0, 0.0, 1.0), self.fwd))
        self.up = unit(cross(self.fwd, self.right))

    def project(self, p: Vec3) -> Pt2:
        w = sub(p, self.eye)
        den = dot(w, self.fwd)
        den = den if den != 0.0 else 1e-9
        return (dot(w, self.right) / den, dot(w, self.up) / den)


def fold(uv: Pt2, alpha: float) -> Vec3:
    u, v = uv
    if v >= 0.0:
        return (u, -v * math.cos(alpha), v * math.sin(alpha))
    return (u, -v, 0.0)


def sheet_point(obj: object, p3: Sequence[float]) -> Pt2:
    u, v = obj.project(tuple(p3))  # type: ignore[attr-defined]
    return (float(u), float(v))


def alpha_at(t: float) -> float:
    total_fold = FOLD_SECONDS
    if t < total_fold:
        return smoothstep(t / FOLD_SECONDS) * (math.pi / 2)
    if t < total_fold + HOLD_SECONDS:
        return math.pi / 2
    t2 = (t - total_fold - HOLD_SECONDS) / UNFOLD_SECONDS
    return (1.0 - smoothstep(t2)) * (math.pi / 2)


def drawable_pieces(obj: object) -> List[Tuple[str, List[Pt2]]]:
    pieces: List[Tuple[str, List[Pt2]]] = []
    for color, poly in obj.faces():  # type: ignore[attr-defined]
        for _piece3d, poly2d in obj.face_pieces(poly):
            pieces.append((color, [(float(u), float(v)) for u, v in poly2d]))
    return pieces


def drawable_edges(obj: object) -> List[Tuple[Pt2, Pt2]]:
    edges: List[Tuple[Pt2, Pt2]] = []
    for a, b in obj.edges():  # type: ignore[attr-defined]
        for seg in obj.edge_segments(a, b):
            edges.append((sheet_point(obj, seg[0]), sheet_point(obj, seg[1])))
    return edges


def frame_points(obj: object, cam: Camera, alpha: float) -> List[Pt2]:
    pts: List[Pt2] = []
    for _color, poly in drawable_pieces(obj):
        pts.extend(cam.project(fold(p, alpha)) for p in poly)
    for a, b in drawable_edges(obj):
        pts.append(cam.project(fold(a, alpha)))
        pts.append(cam.project(fold(b, alpha)))
    return pts


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "chair"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / f"fold_trick_{name}.mp4"
    obj = OBJECTS[name]

    eye = (float(obj.VX), float(obj.VY), float(obj.VZ))
    target = (0.0, 30.0, 34.0)
    cam = Camera(eye, target)
    pieces = drawable_pieces(obj)
    edges = drawable_edges(obj)

    upright = frame_points(obj, cam, math.pi / 2)
    xs = [p[0] for p in upright]
    ys = [p[1] for p in upright]
    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    half = max(max(xs) - min(xs), max(ys) - min(ys)) * 0.62
    xlim = (cx - half, cx + half)
    ylim = (cy - half, cy + half)

    fig = plt.figure(figsize=(SIZE / 100, SIZE / 100), dpi=100)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.set_axis_off()
    fig.patch.set_facecolor("#f7f7f5")

    total = FOLD_SECONDS + HOLD_SECONDS + UNFOLD_SECONDS
    n_frames = int(total * FPS)
    ffmpeg = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        "-movflags", "+faststart", str(out),
    ]
    proc = subprocess.Popen(ffmpeg, stdin=subprocess.PIPE)

    for i in range(n_frames):
        alpha = alpha_at(i / FPS)
        ax.clear()
        ax.set_axis_off()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")

        order = sorted(
            range(len(pieces)),
            key=lambda k: -_depth(cam, pieces[k][1], alpha),
        )
        for k in order:
            color, poly = pieces[k]
            ax.add_patch(MPolygon([cam.project(fold(p, alpha)) for p in poly], closed=True, facecolor=color, edgecolor="none"))
        for a, b in edges:
            pa, pb = cam.project(fold(a, alpha)), cam.project(fold(b, alpha))
            ax.plot([pa[0], pb[0]], [pa[1], pb[1]], color="#111111", linewidth=1.2, solid_capstyle="round")

        fig.canvas.draw()
        assert proc.stdin is not None
        fig.savefig(proc.stdin, format="png")

    assert proc.stdin is not None
    proc.stdin.close()
    proc.wait()
    print(f"wrote {out} ({n_frames} frames, {total:.1f}s)")


def _depth(cam: Camera, poly: Sequence[Pt2], alpha: float) -> float:
    folded = [fold(p, alpha) for p in poly]
    gx = sum(q[0] for q in folded) / len(folded)
    gy = sum(q[1] for q in folded) / len(folded)
    gz = sum(q[2] for q in folded) / len(folded)
    d = sub((gx, gy, gz), cam.eye)
    return dot(d, d)


if __name__ == "__main__":
    main()
