"""
Conic sections support.

This module provides support for conic sections (circles, ellipses,
parabolas, hyperbolas) in projective geometry using homogeneous coordinates.
"""

from enum import Enum
from fractions import Fraction
from math import isqrt
from typing import List, Optional

from ._linalg import adjugate3, determinant3
from .error import DivisionByZeroError
from .pg_object import PgLine, PgPoint, rationalize


def _cross3(v_a: List[Fraction], v_b: List[Fraction]) -> List[Fraction]:
    return [
        v_a[1] * v_b[2] - v_a[2] * v_b[1],
        v_a[2] * v_b[0] - v_a[0] * v_b[2],
        v_a[0] * v_b[1] - v_a[1] * v_b[0],
    ]


def _quadratic_form(matrix: List[List[Fraction]], x: List[Fraction]) -> Fraction:
    return (
        x[0] * (matrix[0][0] * x[0] + matrix[0][1] * x[1] + matrix[0][2] * x[2])
        + x[1] * (matrix[1][0] * x[0] + matrix[1][1] * x[1] + matrix[1][2] * x[2])
        + x[2] * (matrix[2][0] * x[0] + matrix[2][1] * x[1] + matrix[2][2] * x[2])
    )


def _bilinear_form(
    matrix: List[List[Fraction]], x: List[Fraction], y: List[Fraction]
) -> Fraction:
    qy = [
        matrix[i][0] * y[0] + matrix[i][1] * y[1] + matrix[i][2] * y[2]
        for i in range(3)
    ]
    return x[0] * qy[0] + x[1] * qy[1] + x[2] * qy[2]


def _rational_sqrt(value: Fraction) -> Optional[Fraction]:
    if value < 0:
        return None
    num = isqrt(value.numerator)
    den = isqrt(value.denominator)
    if num * num == value.numerator and den * den == value.denominator:
        return Fraction(num, den)
    return None


class ConicType(Enum):
    """Types of conic sections based on discriminant."""

    ELLIPSE = "ellipse"
    PARABOLA = "parabola"
    HYPERBOLA = "hyperbola"


class Conic:
    r"""A conic section represented by a symmetric 3x3 matrix in homogeneous coordinates.

    A point :math:`\mathbf{x} = (x:y:z)` lies on the conic if:

    .. math::

        \mathbf{x}^T Q \mathbf{x} = 0

    Examples:
        >>> from projgeom.conic import Conic, ConicType
        >>> c = Conic.unit_circle()
        >>> c.conic_type()
        <ConicType.ELLIPSE: 'ellipse'>
    """

    def __init__(self, matrix: List[List[Fraction]]):
        """Initialise a conic from its symmetric 3x3 matrix.

        :param matrix: A 3x3 symmetric matrix of :class:`Fraction` values.
        """
        self.matrix = matrix

    @staticmethod
    def circle(center_x: int, center_y: int, radius_sq: int) -> "Conic":
        r"""Create a circle with given centre and squared radius.

        .. math::

            (x - c_x)^2 + (y - c_y)^2 = r^2

        :param center_x: X coordinate of the centre.
        :param center_y: Y coordinate of the centre.
        :param radius_sq: Squared radius.
        :return: The circle conic.

        Examples:
            >>> from projgeom.conic import Conic
            >>> c = Conic.circle(0, 0, 1)
            >>> c.contains(PgPoint([1, 0, 1]))
            True
        """
        cx = Fraction(center_x, 1)
        cy = Fraction(center_y, 1)
        r2 = Fraction(radius_sq, 1)
        zero = Fraction(0, 1)
        one = Fraction(1, 1)

        return Conic(
            [
                [one, zero, -cx],
                [zero, one, -cy],
                [-cx, -cy, cx * cx + cy * cy - r2],
            ]
        )

    @staticmethod
    def unit_circle() -> "Conic":
        r"""Create a unit circle centred at the origin.

        .. math::

            x^2 + y^2 = 1

        :return: The unit circle conic.

        Examples:
            >>> from projgeom.conic import Conic
            >>> c = Conic.unit_circle()
            >>> c.contains(PgPoint([1, 0, 1]))
            True
            >>> c.contains(PgPoint([2, 0, 1]))
            False
        """
        return Conic.circle(0, 0, 1)

    @staticmethod
    def parabola(a: Fraction) -> "Conic":
        r"""Create a parabola :math:`y = a x^2`.

        :param a: The coefficient in :math:`y = a x^2`.
        :return: The parabola conic.

        Examples:
            >>> from fractions import Fraction
            >>> from projgeom.conic import Conic
            >>> p = Conic.parabola(Fraction(1, 1))
            >>> p.conic_type()
            <ConicType.PARABOLA: 'parabola'>
        """
        zero = Fraction(0, 1)
        half = Fraction(1, 2)

        return Conic(
            [
                [-a, zero, zero],
                [zero, zero, half],
                [zero, half, zero],
            ]
        )

    def contains(self, point: PgPoint) -> bool:
        r"""Check if a point lies on the conic.

        .. math::

            \mathbf{x}^T Q \mathbf{x} = 0

        :param point: The point to test.
        :return: ``True`` if the point lies on the conic.

        Examples:
            >>> from projgeom.conic import Conic
            >>> c = Conic.unit_circle()
            >>> c.contains(PgPoint([1, 0, 1]))
            True
        """
        x = Fraction(point.coord[0], 1)
        y = Fraction(point.coord[1], 1)
        z = Fraction(point.coord[2], 1)

        result = (
            x * (self.matrix[0][0] * x + self.matrix[0][1] * y + self.matrix[0][2] * z)
            + y
            * (self.matrix[1][0] * x + self.matrix[1][1] * y + self.matrix[1][2] * z)
            + z
            * (self.matrix[2][0] * x + self.matrix[2][1] * y + self.matrix[2][2] * z)
        )
        return result == Fraction(0, 1)

    def polar(self, point: PgPoint) -> PgLine:
        r"""Compute the polar line of a point with respect to the conic.

        .. math::

            \mathbf{l} = Q \mathbf{x}

        :param point: The point.
        :return: The polar line.

        Examples:
            >>> from projgeom.conic import Conic
            >>> c = Conic.unit_circle()
            >>> polar = c.polar(PgPoint([1, 0, 1]))
            >>> polar
            PgLine(1 : 0 : -1)
        """
        x = Fraction(point.coord[0], 1)
        y = Fraction(point.coord[1], 1)
        z = Fraction(point.coord[2], 1)

        a = self.matrix[0][0] * x + self.matrix[0][1] * y + self.matrix[0][2] * z
        b = self.matrix[1][0] * x + self.matrix[1][1] * y + self.matrix[1][2] * z
        c = self.matrix[2][0] * x + self.matrix[2][1] * y + self.matrix[2][2] * z

        return PgLine(rationalize([a, b, c]))

    def pole(self, line: PgLine) -> PgPoint:
        r"""Compute the pole of a line with respect to the conic.

        .. math::

            \mathbf{x} = Q^{-1} \mathbf{l}
            = \frac{\operatorname{adj}(Q)\, \mathbf{l}}{\det Q}

        The scalar :math:`1/\det Q` is dropped because the result is a
        homogeneous point, so the computation stays exact over the rationals.

        :param line: The line.
        :return: The pole point.
        :raises DivisionByZeroError: If the conic is degenerate (``det Q == 0``).

        Examples:
            >>> from projgeom.conic import Conic
            >>> from projgeom.pg_object import PgLine
            >>> c = Conic.unit_circle()
            >>> c.pole(PgLine([1, 0, -1]))
            PgPoint(1 : 0 : 1)
        """
        if determinant3(self.matrix) == 0:
            raise DivisionByZeroError("Cannot compute the pole of a degenerate conic")
        adj = adjugate3(self.matrix)
        line_coord = line.coord
        return PgPoint(
            rationalize(
                [
                    adj[0][0] * line_coord[0]
                    + adj[0][1] * line_coord[1]
                    + adj[0][2] * line_coord[2],
                    adj[1][0] * line_coord[0]
                    + adj[1][1] * line_coord[1]
                    + adj[1][2] * line_coord[2],
                    adj[2][0] * line_coord[0]
                    + adj[2][1] * line_coord[1]
                    + adj[2][2] * line_coord[2],
                ]
            )
        )

    def tangent(self, point: PgPoint) -> PgLine:
        r"""Compute the tangent line at a point on the conic.

        At a point :math:`\mathbf{p}` on the conic, the tangent is the polar:
        :math:`\mathbf{t} = Q \mathbf{p}`.

        :param point: A point on the conic.
        :return: The tangent line at that point.

        Examples:
            >>> from projgeom.conic import Conic
            >>> c = Conic.unit_circle()
            >>> t = c.tangent(PgPoint([1, 0, 1]))
            >>> t
            PgLine(1 : 0 : -1)
        """
        return self.polar(point)

    def intersect(self, line: PgLine) -> List[PgPoint]:
        r"""Find the real intersection points of a line with the conic.

        The line is parametrized as :math:`\mathbf{x}(t) = u + t\,v` and
        substituted into :math:`\mathbf{x}^T Q \mathbf{x} = 0`, giving a
        quadratic in :math:`t`. When its discriminant is a perfect square the
        roots are rational and the intersection points are returned exactly.

        :param line: The line.
        :return: The list of intersection points.
        :raises NotImplementedError: If the intersection is irrational or
            complex, or the line lies on the conic; those cases require a
            quadratic field extension that this module does not provide.

        Examples:
            >>> from projgeom.conic import Conic
            >>> from projgeom.pg_object import PgLine
            >>> c = Conic.unit_circle()
            >>> points = c.intersect(PgLine([1, 0, 0]))
            >>> len(points)
            2
            >>> all(c.contains(p) for p in points)
            True
        """
        line_coord = [Fraction(value, 1) for value in line.coord]
        vectors: List[List[Fraction]] = []
        for j in range(3):
            axis = [Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
            axis[j] = Fraction(1, 1)
            candidate = _cross3(line_coord, axis)
            if candidate != [0, 0, 0]:
                vectors.append(candidate)
        origin = vectors[0]
        direction = next(v for v in vectors[1:] if _cross3(origin, v) != [0, 0, 0])

        quad = _quadratic_form(self.matrix, direction)
        lin = 2 * _bilinear_form(self.matrix, origin, direction)
        const = _quadratic_form(self.matrix, origin)

        def point_at(t: Fraction) -> PgPoint:
            return PgPoint(
                rationalize([origin[i] + t * direction[i] for i in range(3)])
            )

        if quad == 0:
            if lin == 0:
                raise NotImplementedError("line lies on the conic")
            return [point_at(-const / lin)]

        disc = lin * lin - 4 * quad * const
        if disc < 0:
            raise NotImplementedError("line does not meet the conic in real points")
        root = _rational_sqrt(disc)
        if root is None:
            raise NotImplementedError("intersection requires a quadratic surd")
        if root == 0:
            return [point_at(-lin / (2 * quad))]
        return [
            point_at((-lin + root) / (2 * quad)),
            point_at((-lin - root) / (2 * quad)),
        ]

    def discriminant(self) -> Fraction:
        r"""Compute the discriminant of the conic (determinant of the 2x2 upper-left submatrix).

        .. math::

            \Delta = a e - b d

        :return: The discriminant.
            Positive = ellipse, zero = parabola, negative = hyperbola.

        Examples:
            >>> from projgeom.conic import Conic
            >>> Conic.unit_circle().discriminant() > Fraction(0, 1)
            True
        """
        a = self.matrix[0][0]
        b = self.matrix[0][1]
        d = self.matrix[1][0]
        e = self.matrix[1][1]
        return a * e - b * d

    def conic_type(self) -> ConicType:
        """Determine the type of conic based on its discriminant.

        :return: The :class:`ConicType` (ELLIPSE, PARABOLA, or HYPERBOLA).

        Examples:
            >>> from projgeom.conic import Conic, ConicType
            >>> Conic.unit_circle().conic_type()
            <ConicType.ELLIPSE: 'ellipse'>
        """
        disc = self.discriminant()
        if disc > Fraction(0, 1):
            return ConicType.ELLIPSE
        elif disc == Fraction(0, 1):
            return ConicType.PARABOLA
        else:
            return ConicType.HYPERBOLA
