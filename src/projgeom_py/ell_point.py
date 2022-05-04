from typing import List
from .pgobject import dot, cross, plckr
from .ell_line import EllLine


class EllPoint:
    coord: List[int]

# impl EllPoint:

    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_
        """
        self.coord = coord

# impl PartialEq for EllPoint:

    def eq(self, other) -> bool:
        """_summary_

        Args:
            other (EllPoint): _description_

        Returns:
            bool: _description_
        """
        return cross(self.coord, other.coord) == [0, 0, 0]

# impl ProjPlane<EllLine, int> for EllPoint:

    def aux(self) -> EllLine:
        """_summary_

        Returns:
            EllLine: _description_
        """
        return EllLine(self.coord.copy())

    def dot(self, line: EllLine) -> int:
        """basic measurement

        Args:
            line (EllLine): _description_

        Returns:
            int: _description_
        """
        return dot(self.coord, line.coord)

    def plucker(ld: int, p, mu: int, q):
        """_summary_

        Args:
            ld (int): _description_
            p (EllPoint): _description_
            mu (EllPoint): _description_
            q (EllPoint): _description_

        Returns:
            EllPoint: _description_
        """
        return EllPoint(plckr(ld, p.coord, mu, q.coord))

# impl ProjPlanePrim<EllLine> for EllPoint:

    def incident(self, rhs: EllLine) -> bool:
        """_summary_

        Args:
            rhs (EllLine): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs) -> EllLine:
        """_summary_

        Args:
            rhs (EllPoint): _description_

        Returns:
            EllLine: _description_
        """
        return EllLine(cross(self.coord, rhs.coord))

# impl CKPlanePrim<EllLine> for EllPoint:

    def perp(self) -> EllLine:
        """_summary_

        Returns:
            EllLine: _description_
        """
        return EllLine(self.coord)
