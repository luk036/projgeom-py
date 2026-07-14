"""
Projective plane measurement functions.

This module provides cross-ratio computations for projective geometry.
"""

from fractions import Fraction
from typing import List

from .pg_object import PgObject, cross0, cross1
from .pg_plane import ProjectivePlane


def ratio_ratio(a: int, b: int, c: int, d: int) -> Fraction:
    r"""Compute the ratio of two ratios.

    .. math::

        \frac{a/b}{c/d} = \frac{ad}{bc}

    :param a: First numerator.
    :param b: First denominator.
    :param c: Second numerator.
    :param d: Second denominator.
    :return: The ratio of ratios as a :class:`Fraction`.

    Examples:
        >>> from projgeom.proj_plane_measure import ratio_ratio
        >>> ratio_ratio(1, 2, 3, 4)
        Fraction(2, 3)
    """
    return Fraction(a, b) / Fraction(c, d)


def x_ratio(
    pt_a: ProjectivePlane,
    pt_b: ProjectivePlane,
    line_l: ProjectivePlane,
    line_m: ProjectivePlane,
) -> Fraction:
    r"""Cross ratio of four collinear points with respect to two lines.

    .. math::

        R(A, B; l, m) = \frac{A \cdot l}{A \cdot m} \Big/ \frac{B \cdot l}{B \cdot m}

    :param pt_a: First point :math:`A`.
    :param pt_b: Second point :math:`B`.
    :param line_l: First line :math:`\ell`.
    :param line_m: Second line :math:`m`.
    :return: The cross ratio.

    Examples:
        >>> from projgeom.proj_plane_measure import x_ratio
        >>> from projgeom.pg_object import PgPoint, PgLine
        >>> a = PgPoint([1, 0, 1])
        >>> b = PgPoint([0, 1, 1])
        >>> l1 = PgLine([1, 1, -1])
        >>> l2 = PgLine([1, -1, 0])
        >>> r = x_ratio(a, b, l1, l2)
        >>> abs(r) > 0
        True
    """
    return ratio_ratio(
        pt_a.dot(line_l), pt_a.dot(line_m), pt_b.dot(line_l), pt_b.dot(line_m)
    )


def R0(
    pt_a: "PgObject", pt_b: "PgObject", pt_c: "PgObject", pt_d: "PgObject"
) -> Fraction:
    r"""Cross ratio using yz-plane projection (cross0-based).

    .. math::

        R_0(A,B;C,D) = \frac{\mathrm{cross}_0(A,C)}{\mathrm{cross}_0(A,D)}
                     \Big/ \frac{\mathrm{cross}_0(B,C)}{\mathrm{cross}_0(B,D)}

    :param pt_a: First point.
    :param pt_b: Second point.
    :param pt_c: Third point.
    :param pt_d: Fourth point.
    :return: The cross ratio.

    Examples:
        >>> from projgeom.proj_plane_measure import R0
        >>> from projgeom.pg_object import PgPoint
        >>> a = PgPoint([0, 0, 1])
        >>> b = PgPoint([1, 0, 1])
        >>> c = PgPoint([2, 0, 1])
        >>> d = PgPoint([3, 0, 1])
        >>> r = R0(a, b, c, d)
        >>> r is not None
        True
    """
    return ratio_ratio(
        cross0(pt_a.coord, pt_c.coord),
        cross0(pt_a.coord, pt_d.coord),
        cross0(pt_b.coord, pt_c.coord),
        cross0(pt_b.coord, pt_d.coord),
    )


def R1(
    pt_a: "PgObject", pt_b: "PgObject", pt_c: "PgObject", pt_d: "PgObject"
) -> Fraction:
    r"""Cross ratio using xz-plane projection (cross1-based).

    .. math::

        R_1(A,B;C,D) = \frac{\mathrm{cross}_1(A,C)}{\mathrm{cross}_1(A,D)}
                     \Big/ \frac{\mathrm{cross}_1(B,C)}{\mathrm{cross}_1(B,D)}

    :param pt_a: First point.
    :param pt_b: Second point.
    :param pt_c: Third point.
    :param pt_d: Fourth point.
    :return: The cross ratio.

    Examples:
        >>> from projgeom.proj_plane_measure import R1
        >>> from projgeom.pg_object import PgPoint
        >>> a = PgPoint([0, 1, 1])
        >>> b = PgPoint([1, 0, 1])
        >>> c = PgPoint([1, 1, 1])
        >>> d = PgPoint([2, 1, 1])
        >>> r = R1(a, b, c, d)
        >>> r is not None
        True
    """
    return ratio_ratio(
        cross1(pt_a.coord, pt_c.coord),
        cross1(pt_a.coord, pt_d.coord),
        cross1(pt_b.coord, pt_c.coord),
        cross1(pt_b.coord, pt_d.coord),
    )


def R(
    pt_a: "PgObject", pt_b: "PgObject", pt_c: "PgObject", pt_d: "PgObject"
) -> Fraction:
    r"""Cross ratio of four collinear points (auto-select projection).

    Automatically chooses the best coordinate projection (yz-plane or xz-plane)
    based on the points:

    .. math::

        R(A,B;C,D) =
        \begin{cases}
            R_0(A,B;C,D) & \text{if } \mathrm{cross}_0(A,B) \neq 0 \\
            R_1(A,B;C,D) & \text{otherwise}
        \end{cases}

    :param pt_a: First point.
    :param pt_b: Second point.
    :param pt_c: Third point.
    :param pt_d: Fourth point.
    :return: The cross ratio.

    Examples:
        >>> from projgeom.proj_plane_measure import R
        >>> from projgeom.pg_object import PgPoint
        >>> a = PgPoint([1, 0, 1])
        >>> b = PgPoint([0, 1, 1])
        >>> c = PgPoint([1, 1, 1])
        >>> d = PgPoint([2, 1, 1])
        >>> r = R(a, b, c, d)
        >>> r is not None
        True
    """
    if cross0(pt_a.coord, pt_b.coord) != 0:
        return R0(pt_a, pt_b, pt_c, pt_d)
    return R1(pt_a, pt_b, pt_c, pt_d)
