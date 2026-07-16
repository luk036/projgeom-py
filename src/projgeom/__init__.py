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
from . import ck_plane
from . import conic
from . import ell_object
from . import error
from . import euclid_object
from . import euclid_plane_measure
from . import geometry
from . import hyp_object
from . import myck_object
from . import persp_object
from . import pg_object
from . import pg_plane
from . import proj_plane_measure
from . import transform

# Core projective objects
from .pg_object import PgPoint, PgLine
from .ell_object import EllipticPoint, EllipticLine
from .hyp_object import HyperbolicPoint, HyperbolicLine
from .euclid_object import EuclidPoint, EuclidLine
from .myck_object import MyCKPoint, MyCKLine
from .persp_object import PerspPoint, PerspLine

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

# Cayley-Klein plane functions
from .ck_plane import (
    altitude,
    is_perpendicular as ck_is_perpendicular,
    orthocenter,
    reflect,
    tri_altitude as ck_tri_altitude,
)

# Cross-ratio functions
from .proj_plane_measure import R, R0, R1, ratio_ratio, x_ratio

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
from .euclid_plane_measure import (
    cross_s,
    quadrance,
    spread,
    tri_quadrance,
    tri_spread,
)

# Conics
from .conic import Conic, ConicType

# Transforms
from .transform import (
    Transform,
    projective_transform,
    rotate_point,
    scale_point,
    translate_point,
)
