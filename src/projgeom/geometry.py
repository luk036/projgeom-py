"""
Geometry type identification.

This module provides a unified interface for identifying geometry types.
"""

from abc import abstractmethod
from typing import List


class Geometry:
    """Abstract interface for identifying geometry types.

    Examples:
        >>> from projgeom.pg_object import PgPoint
        >>> from projgeom.geometry import Geometry
        >>> p = PgPoint([1, 2, 3])
        >>> isinstance(p, Geometry)
        True
    """

    @abstractmethod
    def geometry_name(self) -> str:
        """Return the name of the geometry type.

        :return: A string like ``"Projective"``, ``"Elliptic"``, ``"Hyperbolic"``, or ``"Euclidean"``.
        """
        ...


# Geometry names for each point/line type are assigned via their
# geometry_name property.  The convention is:
#   PgPoint / PgLine           -> "Projective"
#   EllipticPoint / EllipticLine   -> "Elliptic"
#   HyperbolicPoint / HyperbolicLine -> "Hyperbolic"
#   EuclidPoint / EuclidLine    -> "Euclidean"
#   MyCKPoint / MyCKLine        -> "CustomCK"
#   PerspPoint / PerspLine      -> "Perspective"
