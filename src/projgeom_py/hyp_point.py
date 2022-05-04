from typing import List
from .pgobject import dot, cross, plckr
from .hyp_line import HypLine


class HypPoint:
    coord: List[int]

# impl HypPoint:

    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_
        """
        self.coord = coord

# impl PartialEq for HypPoint:

    def eq(self, other) -> bool:
        """_summary_

        Args:
            other (HypPoint): _description_

        Returns:
            bool: _description_
        """
        return cross(self.coord, other.coord) == [0, 0, 0]

# impl ProjPlane<HypLine, int> for HypPoint:

    def aux(self) -> HypLine:
        """_summary_

        Returns:
            HypLine: _description_
        """
        return HypLine(self.coord.copy())

    def dot(self, line: HypLine) -> int:
        """basic measurement

        Args:
            line (HypLine): _description_

        Returns:
            int: _description_
        """
        return dot(self.coord, line.coord)

    def plucker(ld: int, p, mu: int, q):
        """_summary_

        Args:
            ld (int): _description_
            p (HypPoint): _description_
            mu (HypPoint): _description_
            q (HypPoint): _description_

        Returns:
            HypPoint: _description_
        """
        return HypPoint(plckr(ld, p.coord, mu, q.coord))

# impl ProjPlanePrim<HypLine> for HypPoint:

    def incident(self, rhs: HypLine) -> bool:
        """_summary_

        Args:
            rhs (HypLine): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs) -> HypLine:
        """_summary_

        Args:
            rhs (HypPoint): _description_

        Returns:
            HypLine: _description_
        """
        return HypLine(cross(self.coord, rhs.coord))

# impl CKPlanePrim<HypLine> for HypPoint:

    def perp(self) -> HypLine:
        """_summary_

        Returns:
            HypLine: _description_
        """
        return HypLine([self.coord[0], self.coord[1], -self.coord[2]])
