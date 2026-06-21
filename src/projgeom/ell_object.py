"""
Elliptic geometry objects (EllipticPoint, EllipticLine).

This module defines points and lines in elliptic geometry.
"""

from .pg_object import PgObject


class EllipticPoint(PgObject["EllipticLine"]):
    """
    .. svgbob::
       :align: center

          / \\
         /   \\
        /-----\\
        \\-----/
         \\   /
          \\ /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (EllipticLine for EllipticPoint).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.ell_object import EllipticPoint
            >>> pt = EllipticPoint([1, 2, 3])
            >>> pt.dual_type()
            <class 'projgeom.ell_object.EllipticLine'>
        """
        return EllipticLine

    def perp(self) -> "EllipticLine":
        """
        The `perp` function returns an `EllipticLine` object representing the polar line of this point.
        Note: This represents the polar operation in projective geometry, not perpendicular.
        :return: The `perp` method is returning an instance of the `EllipticLine` class.

        Examples:
            >>> from projgeom.ell_object import EllipticPoint, EllipticLine
            >>> p = EllipticPoint([1, 2, 3])
            >>> p.perp()
            EllipticLine(1 : 2 : 3)
        """
        return self.polar()

    def polar(self) -> "EllipticLine":
        r"""Polar line with respect to the elliptic absolute conic.

        The elliptic polar uses the identity conic :math:`x_1^2 + x_2^2 + x_3^2 = 0`,
        so the polar of :math:`\mathbf{x}` is simply:

        .. math::

           \mathbf{p} = \mathbf{x}

        (the point and its polar have identical coordinates).

        :return: An :class:`EllipticLine` with the same coordinates.

        Examples:
            >>> from projgeom.ell_object import EllipticPoint, EllipticLine
            >>> p = EllipticPoint([1, 2, 3])
            >>> p.polar()
            EllipticLine(1 : 2 : 3)
        """
        return EllipticLine(self.coord)


class EllipticLine(PgObject[EllipticPoint]):
    """
    The `EllipticLine` class represents a line in Elliptic geometry and has a method `perp()` that returns
    the pole.

    .. svgbob::
       :align: center

          / \\
         /   \\
        /-----\\
        \\-----/
         \\   /
          \\ /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (EllipticPoint for EllipticLine).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.ell_object import EllipticLine
            >>> ln = EllipticLine([1, 2, 3])
            >>> ln.dual_type()
            <class 'projgeom.ell_object.EllipticPoint'>
        """
        return EllipticPoint

    def perp(self) -> EllipticPoint:
        """
        The `perp` function returns an `EllipticPoint` object, which represents the pole of this line.
        Note: This represents the pole operation in projective geometry, not perpendicular.
        :return: An `EllipticPoint` object is being returned.

        Examples:
            >>> from projgeom.ell_object import EllipticPoint, EllipticLine
            >>> l = EllipticLine([1, 2, 3])
            >>> l.perp()
            EllipticPoint(1 : 2 : 3)
        """
        return self.pole()

    def pole(self) -> EllipticPoint:
        r"""Pole of the line with respect to the elliptic absolute conic.

        Same as :meth:`EllipticPoint.polar` — the pole has identical
        coordinates to the line in elliptic geometry:

        .. math::

           \mathbf{p} = \mathbf{l}

        :return: An :class:`EllipticPoint` with the same coordinates.

        Examples:
            >>> from projgeom.ell_object import EllipticPoint, EllipticLine
            >>> l = EllipticLine([1, 2, 3])
            >>> l.pole()
            EllipticPoint(1 : 2 : 3)
        """
        return EllipticPoint(self.coord)
