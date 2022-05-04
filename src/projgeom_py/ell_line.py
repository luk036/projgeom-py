from typing import List

from .ell_point import EllPoint
from .pg_object import cross, dot, plckr


class EllLine:
    coord: List[int]

    # impl EllLine:

    def __init__(self, coord: List[int]):
        """_summary_

        Args:
            coord (List[int]): _description_
        """
        self.coord = coord

    # impl PartialEq for EllLine:

    def eq(self, other) -> bool:
        """_summary_

        Args:
            other (EllLine): _description_

        Returns:
            bool: _description_
        """
        return cross(self.coord, other.coord) == [0, 0, 0]

    # impl ProjPlane<EllPoint, int> for EllLine:

    def aux(self) -> EllPoint:
        """_summary_

        Returns:
            EllPoint: _description_
        """
        return EllPoint(self.coord.copy())

    def dot(self, point: EllPoint) -> int:
        """_summary_

        Args:
            point (EllPoint): _description_

        Returns:
            int: _description_
        """
        return dot(self.coord, point.coord)
        # basic measurement

    def plucker(ld: int, p, mu: int, q):
        """_summary_

        Args:
            ld (int): _description_
            p (EllLine): _description_
            mu (int): _description_
            q (EllLine): _description_

        Returns:
            EllLine: _description_
        """
        return EllLine(plckr(ld, p.coord, mu, q.coord))

    # impl ProjPlanePrim<EllPoint> for EllLine:

    def incident(self, rhs: EllPoint) -> bool:
        """_summary_

        Args:
            rhs (EllPoint): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs) -> EllPoint:
        """_summary_

        Args:
            rhs (_type_): _description_

        Returns:
            EllPoint: _description_
        """
        return EllPoint(cross(self.coord, rhs.coord))

    # impl CKPlanePrim<EllPoint> for EllLine:

    def perp(self) -> EllPoint:
        """_summary_

        Returns:
            EllPoint: _description_
        """
        return EllPoint([self.coord[0], self.coord[1], -self.coord[2]])
