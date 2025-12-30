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
        return HyperbolicLine

    def perp(self):
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

    def polar(self):
        """Polar line of the point.

        :return: a HyperbolicLine object.

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
        """
        The `pole` function returns a HyperbolicPoint object that represents the pole to the given line.
        :return: The `pole` method returns a `HyperbolicPoint` object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
            >>> l = HyperbolicLine([1, 2, 3])
            >>> l.pole()
            HyperbolicPoint(1 : 2 : -3)
        """
        return HyperbolicPoint([self.coord[0], self.coord[1], -self.coord[2]])
