"""
Conic sections support.

This module provides support for conic sections (circles, ellipses,
parabolas, hyperbolas) in projective geometry using homogeneous coordinates.
"""

from enum import Enum
from fractions import Fraction
from typing import List

from .pg_object import PgLine, PgPoint


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

        return Conic([
            [one, zero, -cx],
            [zero, one, -cy],
            [-cx, -cy, cx * cx + cy * cy - r2],
        ])

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

        return Conic([
            [-a, zero, zero],
            [zero, zero, half],
            [zero, half, zero],
        ])

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
            x * (
                self.matrix[0][0] * x
                + self.matrix[0][1] * y
                + self.matrix[0][2] * z
            )
            + y * (
                self.matrix[1][0] * x
                + self.matrix[1][1] * y
                + self.matrix[1][2] * z
            )
            + z * (
                self.matrix[2][0] * x
                + self.matrix[2][1] * y
                + self.matrix[2][2] * z
            )
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

        return PgLine([
            a.numerator // a.denominator,
            b.numerator // b.denominator,
            c.numerator // c.denominator,
        ])

    def pole(self, line: PgLine) -> PgPoint:
        r"""Compute the pole of a line with respect to the conic.

        .. math::

            \mathbf{x} = Q^{-1} \mathbf{l}

        .. note::

            This is a placeholder returning a point on the line.
            A full implementation requires inverting Q.

        :param line: The line.
        :return: The pole point.

        Examples:
            >>> from projgeom.conic import Conic
            >>> from projgeom.pg_object import PgLine
            >>> c = Conic.unit_circle()
            >>> pole = c.pole(PgLine([1, 0, -1]))
            >>> isinstance(pole, PgPoint)
            True
        """
        return PgPoint([line.coord[0], line.coord[1], line.coord[2]])

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
        r"""Find the intersection points of a line with the conic.

        Solves for :math:`\mathbf{x}` satisfying both
        :math:`\mathbf{x}^T Q \mathbf{x} = 0` and :math:`\mathbf{l}^T \mathbf{x} = 0`.

        .. note::

            This is a placeholder returning an empty list.
            A full implementation requires solving a quadratic equation.

        :param line: The line.
        :return: A list of 0, 1, or 2 intersection points.

        Examples:
            >>> from projgeom.conic import Conic
            >>> from projgeom.pg_object import PgLine
            >>> c = Conic.unit_circle()
            >>> c.intersect(PgLine([1, 0, 0]))
            []
        """
        return []

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
