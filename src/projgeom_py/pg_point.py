from typing import List

from .pg_object import PgObject


class PgPoint(PgObject):
    # def __init__(self, coord: List[int]):
    #     """_summary_
    #
    #     Args:
    #         coord (List[int]): _description_
    #
    #     Examples:
    #        >>> p = PgPoint([3, 4, 5])
    #     """
    #     PgObject.__init__(self, coord)
    #
    def dual(self):
        return PgLine


class PgLine(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> l = PgLine([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return PgPoint
