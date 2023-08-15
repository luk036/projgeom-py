from .pg_object import PgObject


class MyCKPoint(PgObject["MyCKLine"]):
    """
    A customized point class for Cayley-Klein geometry.
    """

    def dual(self) -> type:
        return MyCKLine

    def perp(self):
        """
        The `perp` function returns a `MyCKLine` object that is perpendicular to the current line.
        :return: an instance of the MyCKLine class.
        """
        coord = self.coord
        return MyCKLine([-2 * coord[0], coord[1], -2 * coord[2]])


class MyCKLine(PgObject[MyCKPoint]):
    """
    A customized line class for Cayley-Klein geometry.
    """

    def dual(self) -> type:
        return MyCKPoint

    def perp(self) -> MyCKPoint:
        """
        The `perp` function returns a new `MyCKPoint` object with the coordinates of the original object
        negated along the x-axis and z-axis, and doubled along the y-axis.
        :return: The `perp` method returns a `MyCKPoint` object.
        """
        coord = self.coord
        return MyCKPoint([-coord[0], 2 * coord[1], -coord[2]])
