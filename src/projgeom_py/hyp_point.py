from .pg_object import PgObject


class HypPoint(PgObject["HypLine"]):
    """
    The HypPoint class represents a point in Hyperbolic geometry and provides methods for finding its
    dual and perpendicular line.
    """

    def dual(self) -> type:
        return HypLine

    def perp(self):
        """
        The `perp` function returns a HypLine object that is perpendicular to the current HypLine
        object.
        :return: a HypLine object.
        """
        return HypLine([self.coord[0], self.coord[1], -self.coord[2]])


class HypLine(PgObject[HypPoint]):
    """
    The HypLine class represents a line in Hyperbolic geometry and provides methods for finding its
    dual and perpendicular point.
    """

    def dual(self) -> type:
        return HypPoint

    def perp(self) -> HypPoint:
        """
        The `perp` function returns a HypPoint object that represents the perpendicular point to the
        given point.
        :return: The `perp` method returns a `HypPoint` object.
        """
        return HypPoint([self.coord[0], self.coord[1], -self.coord[2]])
