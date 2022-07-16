from typing import List

from .pg_object import PgObject


class MyCKPoint(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = MyCKPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return MyCKLine

    def perp(self):
        """_summary_

        Returns:
            MyCKLine: _description_
        """
        return MyCKLine([-2 * self.coord[0], self.coord[1], -2 * self.coord[2]])


class MyCKLine(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = MyCKPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return MyCKPoint

    def perp(self) -> MyCKPoint:
        """_summary_

        Returns:
            MyCKPoint: _description_
        """
        return MyCKPoint([-self.coord[0], 2 * self.coord[1], -self.coord[2]])
