from typing import List

from .pgobject import cross, dot, plckr


class EllPoint:
    coord: List[int]

    # impl EllPoint:

    def __init__(self, coord: List[int]):
        self.coord = coord

    # impl PartialEq for EllPoint:
    def eq(self, other) -> bool:
        return cross(self.coord, other.coord) == [0, 0, 0]

    # impl ProjPlane<EllLine, int> for EllPoint:

    def aux(self):
        return EllLine(self.coord.copy())

    def dot(self, line) -> int:
        return dot(self.coord, line.coord)
        # basic measurement

    def plucker(ld: int, p, mu: int, q):
        return EllPoint(plckr(ld, p.coord, mu, q.coord))

    # impl ProjPlanePrim<EllLine> for EllPoint:

    def incident(self, rhs) -> bool:
        dot(self.coord, rhs.coord) == 0

    def circ(self, rhs):
        EllLine(cross(self.coord, rhs.coord))

    # impl CKPlanePrim<EllLine> for EllPoint:

    def perp(self):
        EllLine([self.coord[0], self.coord[1], -self.coord[2]])


class EllLine:
    coord: List[int]

    # impl EllLine:

    def __init__(self, coord: List[int]):
        self.coord = coord

    # impl PartialEq for EllLine:

    def eq(self, other) -> bool:
        return cross(self.coord, other.coord) == [0, 0, 0]

    # impl ProjPlane<EllPoint, int> for EllLine:

    def aux(self) -> EllPoint:
        return EllPoint(self.coord.copy())

    def dot(self, point: EllPoint) -> int:
        return dot(self.coord, point.coord)
        # basic measurement

    def plucker(ld: int, p, mu: int, q):
        return EllLine(plckr(ld, p.coord, mu, q.coord))

    # impl ProjPlanePrim<EllPoint> for EllLine:

    def incident(self, rhs: EllPoint) -> bool:
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs) -> EllPoint:
        return EllPoint(cross(self.coord, rhs.coord))

    # impl CKPlanePrim<EllPoint> for EllLine:

    def perp(self) -> EllPoint:
        EllPoint([self.coord[0], self.coord[1], -self.coord[2]])
