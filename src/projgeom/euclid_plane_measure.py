"""
Euclidean plane measurement functions.

This module provides quadrance, spread, and cross-spread computations
for Euclidean geometry.
"""

from fractions import Fraction
from typing import List

from .euclid_object import EuclidPoint
from .pg_object import cross2, dot1, sq


def quad1(x1: int, z1: int, x2: int, z2: int) -> Fraction:
    r"""Compute the squared difference of two ratios.

    .. math::

        Q_1 = \left(\frac{x_1}{z_1} - \frac{x_2}{z_2}\right)^2

    :param x1: First numerator.
    :param z1: First denominator.
    :param x2: Second numerator.
    :param z2: Second denominator.
    :return: The squared difference.

    Examples:
        >>> from projgeom.euclid_plane_measure import quad1
        >>> quad1(0, 1, 3, 1)
        Fraction(9, 1)
    """
    diff = Fraction(x1, z1) - Fraction(x2, z2)
    return diff * diff


def quadrance(a: EuclidPoint, b: EuclidPoint) -> Fraction:
    r"""Compute the quadrance (squared distance) between two Euclidean points.

    .. math::

        Q(A,B) =
        \left(\frac{A_x}{A_z} - \frac{B_x}{B_z}\right)^2
        + \left(\frac{A_y}{A_z} - \frac{B_y}{B_z}\right)^2

    :param a: First point.
    :param b: Second point.
    :return: The quadrance.

    Examples:
        >>> from projgeom.euclid_plane_measure import quadrance
        >>> from projgeom.euclid_object import EuclidPoint
        >>> a = EuclidPoint([0, 0, 1])
        >>> b = EuclidPoint([3, 4, 1])
        >>> quadrance(a, b)
        Fraction(25, 1)
    """
    return quad1(a.coord[0], a.coord[2], b.coord[0], b.coord[2]) + quad1(
        a.coord[1], a.coord[2], b.coord[1], b.coord[2]
    )


def sbase(
    l1: EuclidPoint, l2: EuclidPoint, d: int
) -> Fraction:
    r"""Base function for spread and cross-spread calculations.

    .. math::

        \text{sbase}(l_1, l_2, d) =
        \frac{d^2}{\text{dot}_1(l_1,l_1)\,\text{dot}_1(l_2,l_2)}

    :param l1: First line (as dual point).
    :param l2: Second line (as dual point).
    :param d: The cross or dot product value.
    :return: The spread or cross-spread base value.

    Examples:
        >>> from projgeom.euclid_plane_measure import sbase
        >>> from projgeom.euclid_object import EuclidPoint
        >>> l1 = EuclidPoint([1, 0, 0])
        >>> l2 = EuclidPoint([0, 1, 0])
        >>> sbase(l1, l2, 1)
        Fraction(1, 1)
    """
    d_sq = d * d
    denom = dot1(l1.coord, l1.coord) * dot1(l2.coord, l2.coord)
    return Fraction(d_sq, denom)


def spread(l1: EuclidPoint, l2: EuclidPoint) -> Fraction:
    r"""Compute the spread (squared sine) between two lines.

    .. math::

        s(\theta) = \sin^2\theta = \frac{(l_1 \times l_2)^2}
                                         {(l_1 \cdot l_1)(l_2 \cdot l_2)}

    :param l1: First line direction (as dual point).
    :param l2: Second line direction (as dual point).
    :return: The spread.

    Examples:
        >>> from projgeom.euclid_plane_measure import spread
        >>> from projgeom.euclid_object import EuclidPoint
        >>> l1 = EuclidPoint([1, 0, 0])
        >>> l2 = EuclidPoint([0, 1, 0])
        >>> spread(l1, l2)
        Fraction(1, 1)
        >>> l3 = EuclidPoint([2, 0, 0])
        >>> spread(l1, l3)
        Fraction(0, 1)
    """
    d = cross2(l1.coord, l2.coord)
    return sbase(l1, l2, d)


def cross_s(l1: EuclidPoint, l2: EuclidPoint) -> Fraction:
    r"""Compute the cross-spread (squared cosine) between two lines.

    .. math::

        \text{cs}(\theta) = \cos^2\theta = \frac{(l_1 \cdot l_2)^2}
                                                {(l_1 \cdot l_1)(l_2 \cdot l_2)}

    :param l1: First line direction (as dual point).
    :param l2: Second line direction (as dual point).
    :return: The cross-spread.

    Examples:
        >>> from projgeom.euclid_plane_measure import cross_s
        >>> from projgeom.euclid_object import EuclidPoint
        >>> l1 = EuclidPoint([1, 0, 0])
        >>> l2 = EuclidPoint([0, 1, 0])
        >>> cross_s(l1, l2)
        Fraction(0, 1)
    """
    d = dot1(l1.coord, l2.coord)
    return sbase(l1, l2, d)


def tri_quadrance(triangle: List[EuclidPoint]) -> List[Fraction]:
    r"""Compute the quadrances of all three sides of a triangle.

    Returns ``[Q(BC), Q(AC), Q(AB)]``.

    :param triangle: Three vertices of the triangle.
    :return: Three quadrance values.

    Examples:
        >>> from projgeom.euclid_plane_measure import tri_quadrance
        >>> from projgeom.euclid_object import EuclidPoint
        >>> a = EuclidPoint([0, 0, 1])
        >>> b = EuclidPoint([3, 0, 1])
        >>> c = EuclidPoint([0, 4, 1])
        >>> tri_quadrance([a, b, c])
        [Fraction(25, 1), Fraction(16, 1), Fraction(9, 1)]
    """
    a1, a2, a3 = triangle
    return [quadrance(a2, a3), quadrance(a1, a3), quadrance(a1, a2)]


def tri_spread(trilateral: List[EuclidPoint]) -> List[Fraction]:
    r"""Compute the spreads of all three angles of a triangle.

    Returns ``[spread(side2, side3), spread(side1, side3), spread(side1, side2)]``.

    :param trilateral: Three lines of the triangle (the sides, as dual points).
    :return: Three spread values.

    Examples:
        >>> from projgeom.euclid_plane_measure import tri_spread
        >>> from projgeom.euclid_object import EuclidPoint
        >>> l1 = EuclidPoint([1, 0, 0])
        >>> l2 = EuclidPoint([0, 1, 0])
        >>> l3 = EuclidPoint([1, -1, 0])
        >>> len(tri_spread([l1, l2, l3]))
        3
    """
    l1, l2, l3 = trilateral
    return [spread(l2, l3), spread(l1, l3), spread(l1, l2)]
