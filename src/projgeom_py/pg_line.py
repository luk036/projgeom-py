from typing import List
from .pg_object import dot, cross, plckr
from .pg_point import PgPoint


class PgLine:
    coord: List[int]

# impl PgLine:

    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_
        """
        self.coord = coord

# impl PartialEq for PgLine:

    def eq(self, other) -> bool:
        """_summary_

        Args:
            other (PgLine): _description_

        Returns:
            bool: _description_
        """
        return cross(self.coord, other.coord) == [0, 0, 0]

# impl ProjPlane<PgPoint, int> for PgLine:

    def aux(self) -> PgPoint:
        """_summary_

        Returns:
            PgPoint: _description_
        """
        return PgPoint(self.coord.copy())

    def dot(self, point: PgPoint) -> int:
        """_summary_

        Args:
            point (PgPoint): _description_

        Returns:
            int: _description_
        """
        return dot(self.coord, point.coord)
        # basic measurement

    def plucker(ld: int, p, mu: int, q):
        """_summary_

        Args:
            ld (int): _description_
            p (PgLine): _description_
            mu (int): _description_
            q (PgLine): _description_

        Returns:
            PgLine: _description_
        """
        return PgLine(plckr(ld, p.coord, mu, q.coord))

# impl ProjPlanePrim<PgPoint> for PgLine:

    def incident(self, rhs: PgPoint) -> bool:
        """_summary_

        Args:
            rhs (PgPoint): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs) -> PgPoint:
        """_summary_

        Args:
            rhs (_type_): _description_

        Returns:
            PgPoint: _description_
        """
        return PgPoint(cross(self.coord, rhs.coord))

# impl CKPlanePrim<PgPoint> for PgLine:

    def perp(self) -> PgPoint:
        """_summary_

        Returns:
            PgPoint: _description_
        """
        return PgPoint([self.coord[0], self.coord[1], -self.coord[2]])
