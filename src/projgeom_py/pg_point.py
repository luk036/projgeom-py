from typing import List

from .pg_line import PgLine
from .pgobject import cross, dot, plckr


class PgPoint:
    coord: List[int]

    # impl PgPoint:

    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_
        """
        self.coord = coord

    # impl PartialEq for PgPoint:

    def eq(self, other) -> bool:
        """_summary_

        Args:
            other (PgPoint): _description_

        Returns:
            bool: _description_
        """
        return cross(self.coord, other.coord) == [0, 0, 0]

    # impl ProjPlane<PgLine, int> for PgPoint:

    def aux(self) -> PgLine:
        """_summary_

        Returns:
            PgLine: _description_
        """
        return PgLine(self.coord.copy())

    def dot(self, line: PgLine) -> int:
        """basic measurement

        Args:
            line (PgLine): _description_

        Returns:
            int: _description_
        """
        return dot(self.coord, line.coord)

    def plucker(ld: int, p, mu: int, q):
        """_summary_

        Args:
            ld (int): _description_
            p (PgPoint): _description_
            mu (PgPoint): _description_
            q (PgPoint): _description_

        Returns:
            PgPoint: _description_
        """
        return PgPoint(plckr(ld, p.coord, mu, q.coord))

    # impl ProjPlanePrim<PgLine> for PgPoint:

    def incident(self, rhs: PgLine) -> bool:
        """_summary_

        Args:
            rhs (PgLine): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs) -> PgLine:
        """_summary_

        Args:
            rhs (PgPoint): _description_

        Returns:
            PgLine: _description_
        """
        return PgLine(cross(self.coord, rhs.coord))
