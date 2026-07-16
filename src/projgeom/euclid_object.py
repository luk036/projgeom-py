"""
Euclidean geometry objects (EuclidPoint, EuclidLine).

This module defines points and lines in Euclidean geometry, including
midpoint calculation, perpendicular/parallel checks, altitude,
orthocenter, reflection, and related operations.

The Cayley-Klein model of Euclidean geometry uses the absolute conic
defined by the line at infinity z = 0, so:

- The polar of any point is the line at infinity L_INF = (0:0:1).
- The pole of a line (a:b:c) is its direction vector (a:b:0).
"""

from typing import List

from .pg_object import PgObject, dot1
from .pg_plane import tri_dual


class EuclidPoint(PgObject["EuclidLine"]):
    """A point in the Euclidean plane.

    .. svgbob::
       :align: center

        (x,y)
          o
          |
          |
          o
        (0,0)
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (EuclidLine for EuclidPoint).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.euclid_object import EuclidPoint
            >>> pt = EuclidPoint([1, 2, 3])
            >>> pt.dual_type()
            <class 'projgeom.euclid_object.EuclidLine'>
        """
        return EuclidLine

    def perp(self) -> "EuclidLine":
        """Polar line of the point with respect to the Euclidean absolute conic.

        In Euclidean geometry, all points have the same polar — the line at
        infinity :math:`z = 0`, represented as (0:0:1).

        Note: This represents the polar operation, not perpendicular.

        :return: The line at infinity.

        Examples:
            >>> from projgeom.euclid_object import EuclidPoint, EuclidLine
            >>> p = EuclidPoint([1, 2, 1])
            >>> p.perp()
            EuclidLine(0 : 0 : 1)
        """
        return self.polar()

    def polar(self) -> "EuclidLine":
        r"""Polar line of the point.

        .. math::

            \operatorname{polar}(P) = \mathbf{L}_\infty \quad \forall P

        :return: The line at infinity :math:`\mathbf{L}_\infty = (0:0:1)`.

        Examples:
            >>> from projgeom.euclid_object import EuclidPoint, EuclidLine
            >>> p = EuclidPoint([1, 2, 1])
            >>> p.polar()
            EuclidLine(0 : 0 : 1)
        """
        return L_INF

    def midpoint(self, other: "EuclidPoint") -> "EuclidPoint":
        r"""Midpoint of two Euclidean points.

        .. math::

            M\bigl((x_1:y_1:z_1), (x_2:y_2:z_2)\bigr) =
            (x_1 z_2 + x_2 z_1 : y_1 z_2 + y_2 z_1 : 2 z_1 z_2)

        More compactly, using parametrize::

            M = A·(B_z) + B·(A_z)

        :param other: The other point.
        :return: The midpoint.

        Examples:
            >>> from projgeom.euclid_object import EuclidPoint
            >>> a = EuclidPoint([0, 0, 1])
            >>> b = EuclidPoint([2, 4, 1])
            >>> a.midpoint(b)
            EuclidPoint(2 : 4 : 2)
        """
        return EuclidPoint.parametrize(self, other.coord[2], other, self.coord[2])


class EuclidLine(PgObject[EuclidPoint]):
    """A line in the Euclidean plane.

    A Euclidean line is represented by homogeneous coordinates (a:b:c)
    corresponding to the equation :math:`a x + b y + c z = 0`.
    In affine coordinates (z = 1) this is :math:`a x + b y + c = 0`.

    .. svgbob::
       :align: center

           /
          /
         /_____
        /
       /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (EuclidPoint for EuclidLine).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.euclid_object import EuclidLine
            >>> ln = EuclidLine([1, 2, 3])
            >>> ln.dual_type()
            <class 'projgeom.euclid_object.EuclidPoint'>
        """
        return EuclidPoint

    def perp(self) -> EuclidPoint:
        r"""Pole of the line (direction vector).

        The pole of a line :math:`(a:b:c)` in Euclidean geometry is its
        direction vector :math:`(a:b:0)` — the point at infinity orthogonal
        to the line's normal.

        Note: This represents the pole operation, not perpendicular.

        :return: The direction vector as a Euclidean point with :math:`z=0`.

        Examples:
            >>> from projgeom.euclid_object import EuclidLine, EuclidPoint
            >>> l = EuclidLine([1, 2, -3])
            >>> l.perp()
            EuclidPoint(1 : 2 : 0)
        """
        return self.pole()

    def pole(self) -> EuclidPoint:
        r"""Pole of the line in the Euclidean plane.

        .. math::

            \operatorname{pole}((a:b:c)) = (a : b : 0)

        :return: An :class:`EuclidPoint` with coordinates :math:`(a:b:0)`.

        Examples:
            >>> from projgeom.euclid_object import EuclidLine, EuclidPoint
            >>> l = EuclidLine([1, 2, -3])
            >>> l.pole()
            EuclidPoint(1 : 2 : 0)
        """
        return EuclidPoint([self.coord[0], self.coord[1], 0])

    def altitude(self, pt_a: EuclidPoint) -> "EuclidLine":
        r"""Altitude from a point to this line.

        The altitude is the line through point :math:`A` that is perpendicular
        to this line:

        .. math::

            \text{altitude}(l, A) = l^\perp \wedge A

        where :math:`l^\perp` is the pole of the line.

        :param pt_a: The point through which the altitude passes.
        :return: The altitude line.

        Examples:
            >>> from projgeom.euclid_object import EuclidPoint, EuclidLine
            >>> p = EuclidPoint([1, 2, 1])
            >>> l = EuclidLine([1, 0, -1])  # x = 1
            >>> l.altitude(p)
            EuclidLine(0 : -1 : 2)
        """
        return self.perp().meet(pt_a)

    def is_parallel(self, other: "EuclidLine") -> bool:
        r"""Check if two Euclidean lines are parallel.

        Two lines :math:`(a_1:b_1:c_1)` and :math:`(a_2:b_2:c_2)` are parallel
        when their normal vectors are proportional:

        .. math::

            a_1 b_2 - a_2 b_1 = 0

        :param other: The other line.
        :return: ``True`` if the lines are parallel.

        Examples:
            >>> from projgeom.euclid_object import EuclidLine
            >>> l1 = EuclidLine([1, 0, -1])  # x = 1
            >>> l2 = EuclidLine([2, 0, -5])  # x = 2.5
            >>> l1.is_parallel(l2)
            True
            >>> l3 = EuclidLine([0, 1, -1])  # y = 1
            >>> l1.is_parallel(l3)
            False
        """
        return self.coord[0] * other.coord[1] == self.coord[1] * other.coord[0]

    def is_perpendicular(self, other: "EuclidLine") -> bool:
        r"""Check if two Euclidean lines are perpendicular.

        Two lines are perpendicular when the dot product of their normals
        is zero:

        .. math::

            a_1 a_2 + b_1 b_2 = 0

        :param other: The other line.
        :return: ``True`` if the lines are perpendicular.

        Examples:
            >>> from projgeom.euclid_object import EuclidLine
            >>> l1 = EuclidLine([1, 0, -1])  # x = 1
            >>> l2 = EuclidLine([0, 1, -1])  # y = 1
            >>> l1.is_perpendicular(l2)
            True
            >>> l3 = EuclidLine([1, 1, -1])  # x + y = 1
            >>> l1.is_perpendicular(l3)
            False
        """
        return dot1(self.coord, other.coord) == 0


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

L_INF: EuclidLine = EuclidLine([0, 0, 1])
"""The line at infinity in Euclidean geometry (0:0:1)."""


# ---------------------------------------------------------------------------
# Free functions
# ---------------------------------------------------------------------------


def fB(line_l: EuclidLine) -> EuclidPoint:
    r"""Convert a line to its direction vector in the affine plane.

    Extracts the first two coordinates and sets :math:`z = 0`.

    :param line_l: The line to extract the direction from.
    :return: A point representing the direction vector :math:`(a:b:0)`.

    Examples:
        >>> from projgeom.euclid_object import EuclidLine, EuclidPoint, fB
        >>> l = EuclidLine([1, 2, -3])
        >>> fB(l)
        EuclidPoint(1 : 2 : 0)
    """
    return EuclidPoint([line_l.coord[0], line_l.coord[1], 0])


def midpoint(a: EuclidPoint, b: EuclidPoint) -> EuclidPoint:
    """Compute the midpoint of two Euclidean points.

    :param a: First point.
    :param b: Second point.
    :return: The midpoint.

    Examples:
        >>> from projgeom.euclid_object import EuclidPoint, midpoint
        >>> midpoint(EuclidPoint([0, 0, 1]), EuclidPoint([2, 4, 1]))
        EuclidPoint(2 : 4 : 2)
    """
    return a.midpoint(b)


def tri_midpoint(triangle: List[EuclidPoint]) -> List[EuclidPoint]:
    """Compute the midpoints of all three sides of a triangle.

    Returns ``[midpoint(A,B), midpoint(B,C), midpoint(A,C)]``.

    :param triangle: Three vertices of the triangle.
    :return: Three midpoints.

    Examples:
        >>> from projgeom.euclid_object import EuclidPoint, tri_midpoint
        >>> a = EuclidPoint([0, 0, 1])
        >>> b = EuclidPoint([2, 0, 1])
        >>> c = EuclidPoint([0, 2, 1])
        >>> mids = tri_midpoint([a, b, c])
        >>> mids[0]
        EuclidPoint(2 : 0 : 2)
        >>> mids[1]
        EuclidPoint(2 : 2 : 2)
        >>> mids[2]
        EuclidPoint(0 : 2 : 2)
    """
    a1, a2, a3 = triangle
    return [midpoint(a1, a2), midpoint(a2, a3), midpoint(a1, a3)]


def tri_altitude(triangle: List[EuclidPoint]) -> List[EuclidLine]:
    """Compute the three altitudes of a triangle.

    Each altitude is the line through a vertex perpendicular to the
    opposite side.

    :param triangle: Three vertices of the triangle.
    :return: Three altitude lines [alt(A), alt(B), alt(C)].

    Examples:
        >>> from projgeom.euclid_object import EuclidPoint, EuclidLine, tri_altitude
        >>> a = EuclidPoint([0, 0, 1])
        >>> b = EuclidPoint([2, 0, 1])
        >>> c = EuclidPoint([1, 3, 1])
        >>> alts = tri_altitude([a, b, c])
        >>> alts[0].incident(a)
        True
        >>> alts[1].incident(b)
        True
        >>> alts[2].incident(c)
        True
    """
    sides = tri_dual(triangle)  # type: ignore[arg-type]
    a1, a2, a3 = triangle
    l1, l2, l3 = sides
    return [l1.altitude(a1), l2.altitude(a2), l3.altitude(a3)]  # type: ignore[attr-defined]


def orthocenter(triangle: List[EuclidPoint]) -> EuclidPoint:
    r"""Orthocenter of a triangle.

    The orthocenter is the intersection of two altitudes:

    .. math::

        H = \text{altitude}(A, BC) \cap \text{altitude}(B, CA)

    :param triangle: Three vertices of the triangle.
    :return: The orthocenter.

    Examples:
        >>> from projgeom.euclid_object import EuclidPoint, orthocenter
        >>> a = EuclidPoint([0, 0, 1])
        >>> b = EuclidPoint([2, 0, 1])
        >>> c = EuclidPoint([1, 3, 1])
        >>> orthocenter([a, b, c])
        EuclidPoint(6 : 2 : 6)
    """
    a1, a2, a3 = triangle
    t1 = a2.meet(a3).altitude(a1)
    t2 = a3.meet(a1).altitude(a2)
    return t1.meet(t2)


def is_perpendicular(line_l: EuclidLine, line_m: EuclidLine) -> bool:
    """Check if two Euclidean lines are perpendicular (free function).

    :param line_l: First line.
    :param line_m: Second line.
    :return: ``True`` if the lines are perpendicular.

    Examples:
        >>> from projgeom.euclid_object import EuclidLine, is_perpendicular
        >>> is_perpendicular(EuclidLine([1, 0, -1]), EuclidLine([0, 1, -1]))
        True
    """
    return line_l.is_perpendicular(line_m)


def is_parallel(line_l: EuclidLine, line_m: EuclidLine) -> bool:
    """Check if two Euclidean lines are parallel (free function).

    :param line_l: First line.
    :param line_m: Second line.
    :return: ``True`` if the lines are parallel.

    Examples:
        >>> from projgeom.euclid_object import EuclidLine, is_parallel
        >>> is_parallel(EuclidLine([1, 0, -1]), EuclidLine([2, 0, -5]))
        True
    """
    return line_l.is_parallel(line_m)


def uc_point(lambda_val: int, mu_val: int) -> EuclidPoint:
    r"""Compute a point on the unit circle from rational parameters.

    Using the rational parametrisation of the circle:

    .. math::

        \bigl(\lambda^2 - \mu^2,\; 2\lambda\mu,\; \lambda^2 + \mu^2\bigr)

    :param lambda_val: The first parameter.
    :param mu_val: The second parameter.
    :return: A point on the unit circle.

    Examples:
        >>> from projgeom.euclid_object import EuclidPoint, uc_point
        >>> uc_point(1, 0)
        EuclidPoint(1 : 0 : 1)
        >>> uc_point(0, 1)
        EuclidPoint(-1 : 0 : 1)
    """
    lambda_sq = lambda_val * lambda_val
    mu_sq = mu_val * mu_val
    return EuclidPoint([lambda_sq - mu_sq, 2 * lambda_val * mu_val, lambda_sq + mu_sq])


def archimedes(a: int, b: int, c: int) -> int:
    r"""Archimedes' function.

    .. math::

        \text{archimedes}(a, b, c) = 4ab - (a + b - c)^2

    :param a: First value.
    :param b: Second value.
    :param c: Third value.
    :return: The computed value.

    Examples:
        >>> from projgeom.euclid_object import archimedes
        >>> archimedes(1, 2, 3)
        8
    """
    return 4 * a * b - (a + b - c) * (a + b - c)


def cqq(a: int, b: int, c: int, d: int) -> List[int]:
    r"""Cyclic quadrilateral quadrea theorem coefficients.

    Returns the two coefficients of the quadratic equation whose root
    is the quadrea of a cyclic quadrilateral with opposite side pairs
    (a,b) and (c,d):

    .. math::

        m &= 4ab + 4cd - (a + b - c - d)^2 \\
        p &= m^2 - 4(4ab)(4cd)

    :param a: First side quadrea.
    :param b: Opposite side quadrea to a.
    :param c: Third side quadrea.
    :param d: Opposite side quadrea to c.
    :return: ``[line_m, point_p]`` — the two coefficients.

    Examples:
        >>> from projgeom.euclid_object import cqq
        >>> cqq(3, 4, 3, 4)
        [96, 0]
    """
    t1 = 4 * a * b
    t2 = 4 * c * d
    line_m = (t1 + t2) - (a + b - c - d) * (a + b - c - d)
    point_p = line_m * line_m - 4 * t1 * t2
    return [line_m, point_p]


def Ptolemy(quad: List[int]) -> bool:
    r"""Check Ptolemy's theorem for a cyclic quadrilateral.

    Ptolemy's theorem states that for a cyclic quadrilateral, the product
    of the diagonals equals the sum of the products of opposite sides:

    .. math::

        Q_{13} Q_{24} = Q_{12} Q_{34} + Q_{23} Q_{14}

    Equivalently, :math:`\text{archimedes}(Q_{12}Q_{34},\; Q_{23}Q_{14},\; Q_{13}Q_{24}) = 0`.

    :param quad: Six quadrances ``[Q12, Q23, Q34, Q14, Q13, Q24]``.
    :return: ``True`` if Ptolemy's theorem holds.

    Examples:
        >>> from projgeom.euclid_object import Ptolemy
        >>> Ptolemy([9, 16, 9, 16, 25, 25])
        True
    """
    q12, q23, q34, q14, q13, q24 = quad
    return archimedes(q12 * q34, q23 * q14, q13 * q24) == 0


def reflect_involution(mirror: EuclidLine, pt_p: EuclidPoint) -> EuclidPoint:
    r"""Reflect a point across a line using an involution.

    Creates an involution from the mirror line's direction vector and
    applies it to the point:

    .. math::

        P' = \text{Involution}(\bar{m}, m)(P)

    where :math:`\bar{m}` is the direction vector of the mirror line.

    :param mirror: The mirror line.
    :param pt_p: The point to reflect.
    :return: The reflected point.

    Examples:
        >>> from projgeom.euclid_object import EuclidPoint, EuclidLine, reflect_involution
        >>> mirror = EuclidLine([1, 0, 0])  # y-axis
        >>> p = EuclidPoint([2, 0, 1])
        >>> reflect_involution(mirror, p)
        EuclidPoint(-2 : 0 : 1)
    """
    dir_pt = fB(mirror)
    c = mirror.dot(dir_pt)
    return pt_p.parametrize(c, dir_pt, -2 * pt_p.dot(mirror))
