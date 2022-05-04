from typing import List

from .pg_object import PgObject


class EllPoint(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = EllPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return EllLine

    def perp(self):
        """_summary_

        Returns:
            EllLine: _description_
        """
        return EllLine(self.coord)


class EllLine(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = EllPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return EllPoint

    def perp(self) -> EllPoint:
        """_summary_

        Returns:
            EllPoint: _description_
        """
        return EllPoint(self.coord)
