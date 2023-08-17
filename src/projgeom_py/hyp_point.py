from .pg_object import PgObject


class HyperbolicPoint(PgObject["HyperbolicLine"]):
    """
    The HyperbolicPoint class represents a point in Hyperbolic geometry and provides methods for finding its
    dual and perpendicular line.
    """

    def dual(self) -> type:
        return HyperbolicLine

    def perp(self):
        """Polar line of the point.

        :return: a HyperbolicLine object.
        """
        return HyperbolicLine([self.coord[0], self.coord[1], -self.coord[2]])


class HyperbolicLine(PgObject[HyperbolicPoint]):
    """
    The HyperbolicLine class represents a line in Hyperbolic geometry and provides methods for finding its
    dual and perpendicular point.
    """

    def dual(self) -> type:
        return HyperbolicPoint

    def perp(self) -> HyperbolicPoint:
        """
        The `perp` function returns a HyperbolicPoint object that represents the perpendicular point to the
        given point.
        :return: The `perp` method returns a `HyperbolicPoint` object.
        """
        return HyperbolicPoint([self.coord[0], self.coord[1], -self.coord[2]])
