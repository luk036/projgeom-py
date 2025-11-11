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

        :return: a HyperbolicLine object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
            >>> p = HyperbolicPoint([1, 2, 3])
            >>> p.perp()
            HyperbolicLine(1 : 2 : -3)
        """
        return HyperbolicLine([self.coord[0], self.coord[1], -self.coord[2]])


class HyperbolicLine(PgObject[HyperbolicPoint]):
    """
    The HyperbolicLine class represents a line in Hyperbolic geometry and provides methods for finding its
    dual and perpendicular point.

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
        The `perp` function returns a HyperbolicPoint object that represents the perpendicular point to the
        given point.
        :return: The `perp` method returns a `HyperbolicPoint` object.

        Examples:
            >>> from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
            >>> l = HyperbolicLine([1, 2, 3])
            >>> l.perp()
            HyperbolicPoint(1 : 2 : -3)
        """
        return HyperbolicPoint([self.coord[0], self.coord[1], -self.coord[2]])
