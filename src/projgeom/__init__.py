"""
projgeom - Projective Geometry in Python

This package provides classes and functions for working with projective geometry,
including points, lines, and various geometric transformations in the projective plane.
"""

import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version
else:
    from importlib_metadata import PackageNotFoundError, version

try:
    dist_name = "projgeom-py"
    __version__ = version(dist_name)
except PackageNotFoundError:
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

# Sub-modules
from . import (
    ck_plane,
    conic,
    ell_object,
    error,
    euclid_object,
    euclid_plane_measure,
    geometry,
    hyp_object,
    myck_object,
    persp_object,
    pg_object,
    pg_plane,
    proj_plane_measure,
    transform,
)

# Cayley-Klein plane functions
from .ck_plane import altitude
from .ck_plane import is_perpendicular as ck_is_perpendicular
from .ck_plane import orthocenter as ck_orthocenter
from .ck_plane import reflect
from .ck_plane import tri_altitude as ck_tri_altitude

# Conics
from .conic import Conic, ConicType
from .ell_object import EllipticLine, EllipticPoint

# Euclidean geometry
from .euclid_object import (  # type: ignore[assignment]
    EuclidLine,
    EuclidPoint,
    Ptolemy,
    archimedes,
    cqq,
    fB,
    is_parallel,
    is_perpendicular,
    midpoint,
    orthocenter,
    reflect_involution,
    tri_altitude,
    tri_midpoint,
    uc_point,
)

# Euclidean measurements
from .euclid_plane_measure import cross_s, quadrance, spread, tri_quadrance, tri_spread
from .hyp_object import HyperbolicLine, HyperbolicPoint
from .myck_object import MyCKLine, MyCKPoint
from .persp_object import PerspLine, PerspPoint

# Core projective objects
from .pg_object import PgLine, PgPoint

# Projective plane functions
from .pg_plane import (
    check_axiom,
    check_axiom2,
    check_desargue,
    check_pappus,
    coincident,
    harm_conj,
    involution,
    persp,
    tri_dual,
)

# Cross-ratio functions
from .proj_plane_measure import R0, R1, R, ratio_ratio, x_ratio

# Transforms
from .transform import (
    Transform,
    projective_transform,
    rotate_point,
    scale_point,
    translate_point,
)

__all__ = [
    # Sub-modules
    "ck_plane",
    "conic",
    "ell_object",
    "error",
    "euclid_object",
    "euclid_plane_measure",
    "geometry",
    "hyp_object",
    "myck_object",
    "persp_object",
    "pg_object",
    "pg_plane",
    "proj_plane_measure",
    "transform",
    # Core projective objects
    "PgPoint",
    "PgLine",
    "EllipticPoint",
    "EllipticLine",
    "HyperbolicPoint",
    "HyperbolicLine",
    "EuclidPoint",
    "EuclidLine",
    "MyCKPoint",
    "MyCKLine",
    "PerspPoint",
    "PerspLine",
    # Projective plane functions
    "check_axiom",
    "check_axiom2",
    "check_desargue",
    "check_pappus",
    "coincident",
    "harm_conj",
    "involution",
    "persp",
    "tri_dual",
    # Cayley-Klein plane functions
    "altitude",
    "ck_is_perpendicular",
    "ck_orthocenter",
    "reflect",
    "ck_tri_altitude",
    # Cross-ratio functions
    "R",
    "R0",
    "R1",
    "ratio_ratio",
    "x_ratio",
    # Euclidean geometry
    "Ptolemy",
    "archimedes",
    "cqq",
    "fB",
    "is_parallel",
    "is_perpendicular",
    "midpoint",
    "orthocenter",
    "reflect_involution",
    "tri_altitude",
    "tri_midpoint",
    "uc_point",
    # Euclidean measurements
    "cross_s",
    "quadrance",
    "spread",
    "tri_quadrance",
    "tri_spread",
    # Conics
    "Conic",
    "ConicType",
    # Transforms
    "Transform",
    "projective_transform",
    "rotate_point",
    "scale_point",
    "translate_point",
]
