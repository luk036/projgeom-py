from typing import List

from .pg_object import PgObject


class PerspPoint(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = PerspPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return PerspLine

    def perp(self):
        """_summary_

        Returns:
            PerspLine: _description_
        """
        return L_INF

    def midpoint(self, other):
        """_summary_

        Returns:
            PerspPoint: _description_
        """
        alpha = L_INF.dot(other)
        beta = L_INF.dot(self)
        return PerspPoint.plucker(alpha, self, beta, other)


class PerspLine(PgObject):
    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = PerspPoint([3, 4, 5])
        """
        PgObject.__init__(self, coord)

    def dual(self):
        return PerspPoint

    def perp(self) -> PerspPoint:
        """_summary_

        Returns:
            PerspPoint: _description_
        """
        alpha = I_RE.dot(self)
        beta = I_IM.dot(self)
        return PerspPoint.plucker(alpha, I_RE, beta, I_IM)

    def is_parallel(self, other) -> bool:
        return L_INF.dot(self.circ(other)) == 0


I_RE = PerspPoint([0, 1, 1])
I_IM = PerspPoint([1, 0, 0])
L_INF = PerspLine([0, -1, 1])
