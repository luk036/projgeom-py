from typing import List
from .pg_object import dot, cross, plckr
from .hyp_point import HypPoint


class HypLine:
    coord: List[int]

# impl HypLine:

    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_
        """
        self.coord = coord

# impl PartialEq for HypLine:

    def eq(self, other) -> bool:
        """_summary_

        Args:
            other (HypLine): _description_

        Returns:
            bool: _description_
        """
        return cross(self.coord, other.coord) == [0, 0, 0]

# impl ProjPlane<HypPoint, int> for HypLine:

    def aux(self) -> HypPoint:
        """_summary_

        Returns:
            HypPoint: _description_
        """
        return HypPoint(self.coord.copy())

    def dot(self, point: HypPoint) -> int:
        """_summary_

        Args:
            point (HypPoint): _description_

        Returns:
            int: _description_
        """
        return dot(self.coord, point.coord)
        # basic measurement

    def plucker(ld: int, p, mu: int, q):
        """_summary_

        Args:
            ld (int): _description_
            p (HypLine): _description_
            mu (int): _description_
            q (HypLine): _description_

        Returns:
            HypLine: _description_
        """
        return HypLine(plckr(ld, p.coord, mu, q.coord))

# impl ProjPlanePrim<HypPoint> for HypLine:

    def incident(self, rhs: HypPoint) -> bool:
        """_summary_

        Args:
            rhs (HypPoint): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs) -> HypPoint:
        """_summary_

        Args:
            rhs (_type_): _description_

        Returns:
            HypPoint: _description_
        """
        return HypPoint(cross(self.coord, rhs.coord))

# impl CKPlanePrim<HypPoint> for HypLine:

    def perp(self) -> HypPoint:
        """_summary_

        Returns:
            HypPoint: _description_
        """
        return HypPoint([self.coord[0], self.coord[1], -self.coord[2]])
