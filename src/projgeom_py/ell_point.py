from .pg_object import PgObject


class EllPoint(PgObject["EllLine"]):
    """
    The `EllPoint` class represents a point in elliptic geometry and provides methods for finding its
    dual and perpendicular line.
    """

    def dual(self) -> type:
        return EllLine

    def perp(self) -> "EllLine":
        """
        The `perp` function returns an `EllLine` object.
        :return: The `perp` method is returning an instance of the `EllLine` class.
        """
        return EllLine(self.coord)


class EllLine(PgObject[EllPoint]):
    """
    The `EllLine` class represents a line in Elliptic geometry and has a method `perp()` that returns
    the perpendicular point.
    """

    def dual(self) -> type:
        return EllPoint

    def perp(self) -> EllPoint:
        """
        The `perp` function returns an `EllPoint` object.
        :return: An EllPoint object is being returned.
        """
        return EllPoint(self.coord)
