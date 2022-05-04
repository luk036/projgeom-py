from typing import List

from .pg_object import PgObject


class HypPoint(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = HypPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return HypLine

    def perp(self):
        """_summary_

        Returns:
            HypLine: _description_
        """
        return HypLine([self.coord[0], self.coord[1], -self.coord[2]])


class HypLine(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = HypPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return HypPoint

    def perp(self) -> HypPoint:
        """_summary_

        Returns:
            HypPoint: _description_
        """
        return HypPoint([self.coord[0], self.coord[1], -self.coord[2]])
