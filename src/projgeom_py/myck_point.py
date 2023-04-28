from .pg_object import PgObject


class MyCKPoint(PgObject["MyCKLine"]):
    def dual(self) -> type:
        return MyCKLine

    def perp(self):
        """_summary_

        Returns:
            MyCKLine: _description_
        """
        coord = self.coord
        return MyCKLine([-2 * coord[0], coord[1], -2 * coord[2]])


class MyCKLine(PgObject[MyCKPoint]):
    def dual(self) -> type:
        return MyCKPoint

    def perp(self) -> MyCKPoint:
        """_summary_

        Returns:
            MyCKPoint: _description_
        """
        coord = self.coord
        return MyCKPoint([-coord[0], 2 * coord[1], -coord[2]])
