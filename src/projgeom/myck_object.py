"""
MyCKPoint and MyCKLine classes for a custom Cayley-Klein geometry.

Defines points and lines in the Cayley-Klein plane with the absolute
conic 2*x_1^2 - x_2^2 + 2*x_3^2 = 0.
"""

from .pg_object import PgObject


class MyCKPoint(PgObject["MyCKLine"]):
    """
    A customized point class for Cayley-Klein geometry.

    .. svgbob::
       :align: center

          / \\
         / _ \\
        | / \\ |
        | \\_/ |
         \\ _ /
          \\ /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (MyCKLine for MyCKPoint).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.myck_object import MyCKPoint
            >>> pt = MyCKPoint([1, 2, 3])
            >>> pt.dual_type()
            <class 'projgeom.myck_object.MyCKLine'>
        """
        return MyCKLine

    def perp(self) -> "MyCKLine":
        """
        The perp function returns an instance of the MyCKLine class that represents a polar line.
        Note: This represents the polar operation in projective geometry, not perpendicular.
        :return: an instance of the MyCKLine class.

        Examples:
            >>> from projgeom.myck_object import MyCKPoint, MyCKLine
            >>> p = MyCKPoint([1, 2, 3])
            >>> p.perp()
            MyCKLine(-2 : 2 : -6)
        """
        return self.polar()

    def polar(self) -> "MyCKLine":
        r"""Polar line with respect to a custom conic :math:`2x_1^2 - x_2^2 + 2x_3^2 = 0`.

        The polar of :math:`\mathbf{x} = (x_1:x_2:x_3)` is:

        .. math::

           \mathbf{p} = (-2x_1,\; x_2,\; -2x_3)

        :return: An :class:`MyCKLine` instance.

        Examples:
            >>> from projgeom.myck_object import MyCKPoint, MyCKLine
            >>> p = MyCKPoint([1, 2, 3])
            >>> p.polar()
            MyCKLine(-2 : 2 : -6)
        """
        coord = self.coord
        return MyCKLine([-2 * coord[0], coord[1], -2 * coord[2]])


class MyCKLine(PgObject[MyCKPoint]):
    """
    A customized line class for Cayley-Klein geometry.

    .. svgbob::
       :align: center

          / \\
         / _ \\
        | / \\ |
        | \\_/ |
         \\ _ /
          \\ /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (MyCKPoint for MyCKLine).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.myck_object import MyCKLine
            >>> ln = MyCKLine([1, 2, 3])
            >>> ln.dual_type()
            <class 'projgeom.myck_object.MyCKPoint'>
        """
        return MyCKPoint

    def perp(self) -> MyCKPoint:
        """Pole of the line.
        Note: This represents the pole operation in projective geometry, not perpendicular.
        :return: The `perp` method returns a `MyCKPoint` object.

        Examples:
            >>> from projgeom.myck_object import MyCKPoint, MyCKLine
            >>> l = MyCKLine([1, 2, 3])
            >>> l.perp()
            MyCKPoint(-1 : 4 : -3)
        """
        return self.pole()

    def pole(self) -> MyCKPoint:
        r"""Pole with respect to the custom conic :math:`2x_1^2 - x_2^2 + 2x_3^2 = 0`.

        The pole of :math:`\mathbf{l} = (l_1:l_2:l_3)` is:

        .. math::

           \mathbf{p} = (-l_1,\; 2l_2,\; -l_3)

        :return: A :class:`MyCKPoint` object.

        Examples:
            >>> from projgeom.myck_object import MyCKPoint, MyCKLine
            >>> l = MyCKLine([1, 2, 3])
            >>> l.pole()
            MyCKPoint(-1 : 4 : -3)
        """
        coord = self.coord
        return MyCKPoint([-coord[0], 2 * coord[1], -coord[2]])
