"""Fold-a-house trick art: thin wrapper over :mod:`fold_trick`.

Backwards-compatible entry point: ``python examples/house_flat.py`` still writes
``house_flat.svg``, and :mod:`fold_anim` keeps importing the same module-level
names.  The geometry and the exact-rational pipeline live in :mod:`fold_trick`,
the Python mirror of ``examples/fold_trick.cpp``.
"""

from pathlib import Path
from typing import List, Sequence, Tuple

import fold_trick as _ft
from fold_trick import Edge, Face, Pt2, Vec3

SCENE = _ft.make_house()
VX, VY, VZ = SCENE.vx, SCENE.vy, SCENE.vz


def faces() -> List[Face]:
    """Return the house faces (colour, corner polygon)."""
    return SCENE.faces


def edges() -> List[Edge]:
    """Return the house edges (segment endpoint pairs)."""
    return SCENE.edges


def project(point: Vec3) -> Pt2:
    """Project a house point onto the nearer plane, unfolded."""
    return _ft.project(SCENE, point)


def face_pieces(corners: Sequence[Vec3]) -> List[Tuple[List[Vec3], List[Pt2]]]:
    """Split a house face at the crease and project each piece."""
    return _ft.face_pieces(SCENE, corners)


def edge_segments(a: Vec3, b: Vec3) -> List[Edge]:
    """Split a house edge at the crease."""
    return _ft.edge_segments(SCENE, a, b)


def verify() -> None:
    """Check that the drawn sheet points share a ray with the house points."""
    _ft.verify(SCENE)


def render(out: Path) -> None:
    """Write the house sheet SVG to ``out``."""
    out.write_text(_ft.render(SCENE), encoding="utf-8")


def main() -> None:
    """Render ``house_flat.svg`` at the repository root."""
    verify()
    root = Path(__file__).resolve().parent.parent
    render(root / "house_flat.svg")
    print("wrote house_flat.svg")


if __name__ == "__main__":
    main()
