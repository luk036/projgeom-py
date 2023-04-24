from abc import abstractmethod
from typing import List


def dot(a: List[int], b: List[int]) -> int:
    """_summary_

    Args:
        a (List[int]): _description_
        b (List[int]): _description_

    Returns:
        int: _description_
    """
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: List[int], b: List[int]) -> List[int]:
    """_summary_

    Args:
        a (List[int]): _description_
        b (List[int]): _description_

    Returns:
        List[int]: _description_
    """
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def plckr(ld: int, p: List[int], mu: int, q: List[int]) -> List[int]:
    """_summary_

    Args:
        ld (int): _description_
        p (List[int]): _description_
        mu (int): _description_
        q (List[int]): _description_

    Returns:
        List[int]: _description_
    """
    return [
        ld * p[0] + mu * q[0],
        ld * p[1] + mu * q[1],
        ld * p[2] + mu * q[2],
    ]


class PgObject:
    coord: List[int]

    # impl PgObject:

    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_

        Examples:
           >>> p = PgObject([3, 4, 5])
        """
        self.coord = coord

    # impl PartialEq for PgObject:

    def __eq__(self, other) -> bool:
        """_summary_

        Args:
            other (PgObject): _description_

        Returns:
            bool: _description_

        Examples:
           >>> p = PgObject([3, 4, 5])
           >>> q = PgObject([30, 40, 50])
           >>> p == q
           True
        """
        if type(self) != type(other):
            return False
        return cross(self.coord, other.coord) == [0, 0, 0]

    # impl ProjPlane<PgLine, int> for PgObject:

    @abstractmethod
    def dual(self):
        pass

    def aux(self):
        """_summary_

        Returns:
            PgLine: _description_
        """
        # L = self.dual()
        return self.dual()(self.coord.copy())

    def dot(self, line) -> int:
        """basic measurement

        Args:
            line (PgLine): _description_

        Returns:
            int: _description_
        """
        return dot(self.coord, line.coord)

    @staticmethod
    def plucker(ld: int, p, mu: int, q):
        """_summary_

        Args:
            ld (int): _description_
            p (PgObject): _description_
            mu (int): _description_
            q (PgObject): _description_

        Returns:
            PgObject: _description_
        """
        P = type(p)
        return P(plckr(ld, p.coord, mu, q.coord))

    # impl ProjPlanePrim<PgLine> for PgObject:

    def incident(self, rhs) -> bool:
        """_summary_

        Args:
            rhs (PgLine): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs):
        """_summary_

        Args:
            rhs (PgObject): _description_

        Returns:
            PgLine: _description_
        """
        return self.dual()(cross(self.coord, rhs.coord))
