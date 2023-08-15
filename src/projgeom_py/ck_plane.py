from abc import abstractmethod
from typing import List, TypeVar

from .pg_plane import ProjectivePlane, Value, involution

# CayleyKleinPlanePrimitive = Union[HyperbolicLine, HyperbolicPoint]

# trait CayleyKleinPlanePrimitive<Line>: ProjectivePlanePrimitive<Line>:
#     def perp(self) -> Line

Dual = TypeVar("Dual", bound="CayleyKleinPlane")


# Object in Cayley–Klein Plane
class CayleyKleinPlane(ProjectivePlane[Dual, Value]):
    @abstractmethod
    def perp(self) -> Dual:
        pass


Pck = CayleyKleinPlane["Lck", Value]
Lck = CayleyKleinPlane["Pck", Value]


def is_perpendicular(m1: Lck, m2: Lck) -> bool:
    """
    The function `is_perpendicular` checks if two lines are perpendicular.

    :param m1: The parameter `m1` represents a line in Cayley–Klein geometry. It is of type `Lck`, which is likely a custom class representing a hyperbolic line
    :type m1: Lck
    :param m2: The parameter `m2` represents a line in Cayley–Klein geometry
    :type m2: Lck
    :return: a boolean value, indicating whether the two given lines are perpendicular to each other.

    Examples:
        >>> from projgeom_py.hyp_point import HyperbolicLine, HyperbolicPoint
        >>> is_perpendicular(HyperbolicLine([0, 1, 0]), HyperbolicLine([0, 0, 1]))
        True
        >>> is_perpendicular(HyperbolicLine([0, 1, 0]), HyperbolicLine([0, 0, -1]))
        True
    """
    return m1.perp().incident(m2)


def altitude(p: Pck, m: Lck) -> Lck:
    """
    The `altitude` function calculates the altitude of a point `p` with respect to a line `m` in a
    Cayley–Klein geometry.

    :param p: p is a CayleyKleinPlanePrimitive object representing a point in three-dimensional space
    :type p: Pck
    :param m: m is a CayleyKleinPlanePrimitive object representing a line in a hyperbolic plane
    :type m: Lck
    :return: The function `altitude` returns a `CayleyKleinPlanePrimitive<Line>` object.

    Examples:
        >>> from projgeom_py.hyp_point import HyperbolicLine, HyperbolicPoint
        >>> t = altitude(HyperbolicPoint([0, 1, 0]), HyperbolicLine([0, 0, 1]))
        >>> t == HyperbolicLine([1, 0, 0])
        True
    """
    return m.perp().meet(p)


def orthocenter(tri: List[Pck]):
    """
    The `orthocenter` function calculates the orthocenter of a triangle in Cayley–Klein geometry.

    :param tri: The `tri` parameter is a list of three `CayleyKleinPlanePrimitive<Point>` objects.
    :type tri: List[Pck]
    :return: The function `orthocenter` returns a `CayleyKleinPlanePrimitive<Point>` object.

    Examples:
        >>> from projgeom_py.hyp_point import HyperbolicLine, HyperbolicPoint
        >>> t = orthocenter([HyperbolicPoint([0, 1, 0]), HyperbolicPoint([0, 0, 1]), HyperbolicPoint([1, 0, 0])])
        >>> t == HyperbolicPoint([1, 1, 1])
        True
    """
    [a1, a2, a3] = tri
    t1 = altitude(a1, a2.meet(a3))
    t2 = altitude(a2, a3.meet(a1))
    return t1.meet(t2)


def tri_altitude(tri):
    """
    The function `tri_altitude` calculates the altitudes of a triangle given its side lengths.

    :param tri: The `tri` parameter is a list containing three elements. Each element represents a side of a triangle
    :return: a list of altitudes of a triangle.
    """
    [a1, a2, a3] = tri
    t1 = altitude(a1, a2.meet(a3))
    t2 = altitude(a2, a3.meet(a1))
    t3 = altitude(a3, a1.meet(a2))
    return [t1, t2, t3]


# trait CayleyKleinPlane<Line, Value: Default + Eq>: ProjectivePlane<Line, Value> + CayleyKleinPlanePrimitive<Line> {}


def reflect(mirror: CayleyKleinPlane, p: CayleyKleinPlane):
    """
    The `reflect` function performs a reflection of a plane `p` across a mirror plane `mirror`.

    :param mirror: The `mirror` parameter is of type `CayleyKleinPlane<Line>`, which represents a mirror plane. It is used to define the mirror in which the point `p` will be reflected
    :type mirror: CayleyKleinPlane
    :param p: The parameter `p` represents a CayleyKleinPlane object
    :type p: CayleyKleinPlane

    Examples:
        >>> from projgeom_py.hyp_point import HyperbolicLine, HyperbolicPoint
        >>> t = reflect(HyperbolicLine([0, 1, 0]), HyperbolicPoint([0, 0, 1]))
        >>> t == HyperbolicPoint([0, 1, 0])
        False
    """
    involution(mirror.perp(), mirror, p)
