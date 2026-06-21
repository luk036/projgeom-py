"""
Hyperbolic geometry objects (HyperbolicPoint, HyperbolicLine).

This module defines points and lines in hyperbolic geometry using the
Cayley-Klein model of the hyperbolic plane.
"""

from .pg_object import PgObject


class HyperbolicPoint(PgObject["HyperbolicLine"]):
    """
    .. svgbob::
       :align: center

        \\  |  /
         \\ | /
          \\|/
      -----o-----
          /|\\
         / | \\
        /  |  \\
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (HyperbolicLine for HyperbolicPoint).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint
            >>> pt = HyperbolicPoint([1, 2, 3])
            >>> pt.dual_type()
            <class 'projgeom.hyp_object.HyperbolicLine'>
        """
        return HyperbolicLine

    def perp(self) -> "HyperbolicLine":
        """Polar line of the point.

        Note: This represents the polar operation in projective geometry, not perpendicular.

        :return: a HyperbolicLine object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
            >>> p = HyperbolicPoint([1, 2, 3])
            >>> p.perp()
            HyperbolicLine(1 : 2 : -3)
        """
        return self.polar()

    def polar(self) -> "HyperbolicLine":
        r"""Polar line of the point in the Cayley–Klein model.

        The polar of :math:`\mathbf{x} = (x_1:x_2:x_3)` with respect to
        the absolute conic :math:`x_1^2 + x_2^2 - x_3^2 = 0` is given by:

        .. math::

           \mathbf{p} = (x_1,\; x_2,\; -x_3)

        :return: A HyperbolicLine object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
            >>> p = HyperbolicPoint([1, 2, 3])
            >>> p.polar()
            HyperbolicLine(1 : 2 : -3)
        """
        return HyperbolicLine([self.coord[0], self.coord[1], -self.coord[2]])


class HyperbolicLine(PgObject[HyperbolicPoint]):
    """
    The HyperbolicLine class represents a line in Hyperbolic geometry and provides methods for finding its
    pole.

    .. svgbob::
       :align: center

        \\  |  /
         \\ | /
          \\|/
      -----o-----
          /|\\
         / | \\
        /  |  \\
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (HyperbolicPoint for HyperbolicLine).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicLine
            >>> ln = HyperbolicLine([1, 2, 3])
            >>> ln.dual_type()
            <class 'projgeom.hyp_object.HyperbolicPoint'>
        """
        return HyperbolicPoint

    def perp(self) -> HyperbolicPoint:
        """
        The `perp` function returns a HyperbolicPoint object that represents the pole to the given line.
        Note: This represents the pole operation in projective geometry, not perpendicular.
        :return: The `perp` method returns a `HyperbolicPoint` object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
            >>> l = HyperbolicLine([1, 2, 3])
            >>> l.perp()
            HyperbolicPoint(1 : 2 : -3)
        """
        return self.pole()

    def pole(self) -> HyperbolicPoint:
        r"""Pole of the line with respect to the absolute conic.

        The pole of :math:`\mathbf{l} = (l_1:l_2:l_3)` is:

        .. math::

           \mathbf{p} = (l_1,\; l_2,\; -l_3)

        (same transformation as :meth:`HyperbolicPoint.polar` due to
        the symmetry of the absolute conic).

        :return: A :class:`HyperbolicPoint` object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
            >>> l = HyperbolicLine([1, 2, 3])
            >>> l.pole()
            HyperbolicPoint(1 : 2 : -3)
        """
        return HyperbolicPoint([self.coord[0], self.coord[1], -self.coord[2]])
