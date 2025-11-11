from .pg_object import PgObject


class EllipticPoint(PgObject["EllipticLine"]):
    """
    The `EllipticPoint` class represents a point in elliptic geometry and provides methods for finding its
    dual and perpendicular line.

    .. svgbob::
       :align: center

          / \
         /   \
        /-----\
        \-----/
         \   /
          \ /
    """

    def dual_type(self) -> type:
        return EllipticLine

    def perp(self) -> "EllipticLine":
        """
        The `perp` function returns an `EllipticLine` object representing the polar line of this point.
        :return: The `perp` method is returning an instance of the `EllipticLine` class.

        Examples:
            >>> from projgeom.ell_object import EllipticPoint, EllipticLine
            >>> p = EllipticPoint([1, 2, 3])
            >>> p.perp()
            EllipticLine(1 : 2 : 3)
        """
        return EllipticLine(self.coord)


class EllipticLine(PgObject[EllipticPoint]):
    """
    The `EllipticLine` class represents a line in Elliptic geometry and has a method `perp()` that returns
    the perpendicular point.

    .. svgbob::
       :align: center

          / \
         /   \
        /-----\
        \-----/
         \   /
          \ /
    """

    def dual_type(self) -> type:
        return EllipticPoint

    def perp(self) -> EllipticPoint:
        """
        The `perp` function returns an `EllipticPoint` object, which represents the pole of this line.
        :return: An `EllipticPoint` object is being returned.

        Examples:
            >>> from projgeom.ell_object import EllipticPoint, EllipticLine
            >>> l = EllipticLine([1, 2, 3])
            >>> l.perp()
            EllipticPoint(1 : 2 : 3)
        """
        return EllipticPoint(self.coord)
