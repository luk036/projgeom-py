from abc import abstractmethod
from typing import List, TypeVar

from .pg_plane import ProjPlane, V, involution

# CKPlanePrim = Union[HypLine, HypPoint]

# trait CKPlanePrim<L>: ProjPlanePrim<L>:
#     def perp(self) -> L

Dual = TypeVar("Dual", bound="CKPlane")


# Object in Cayley–Klein Plane
class CKPlane(ProjPlane[Dual, V]):
    @abstractmethod
    def perp(self) -> Dual:
        pass


Pck = CKPlane["Lck", V]
Lck = CKPlane["Pck", V]


def is_perpendicular(m1: Lck, m2: Lck) -> bool:
    """
    The function `is_perpendicular` checks if two lines are perpendicular.

    :param m1: The parameter `m1` represents a line in Cayley–Klein geometry. It is of type `Lck`, which is likely a custom class representing a hyperbolic line
    :type m1: Lck
    :param m2: The parameter `m2` represents a line in Cayley–Klein geometry
    :type m2: Lck
    :return: a boolean value, indicating whether the two given lines are perpendicular to each other.

    Examples:
        >>> from projgeom_py.hyp_point import HypLine, HypPoint
        >>> is_perpendicular(HypLine([0, 1, 0]), HypLine([0, 0, 1]))
        True
        >>> is_perpendicular(HypLine([0, 1, 0]), HypLine([0, 0, -1]))
        True
    """
    return m1.perp().incident(m2)


def altitude(p: Pck, m: Lck) -> Lck:
    """
    The `altitude` function calculates the altitude of a point `p` with respect to a line `m` in a
    Cayley–Klein geometry.

    :param p: p is a CKPlanePrim object representing a point in three-dimensional space
    :type p: Pck
    :param m: m is a CKPlanePrim object representing a line in a hyperbolic plane
    :type m: Lck
    :return: The function `altitude` returns a `CKPlanePrim<L>` object.

    Examples:
        >>> from projgeom_py.hyp_point import HypLine, HypPoint
        >>> t = altitude(HypPoint([0, 1, 0]), HypLine([0, 0, 1]))
        >>> t == HypLine([1, 0, 0])
        True
    """
    return m.perp().circ(p)


def orthocenter(tri: List[Pck]):
    """
    The `orthocenter` function calculates the orthocenter of a triangle in Cayley–Klein geometry.

    :param tri: The `tri` parameter is a list of three `CKPlanePrim<P>` objects.
    :type tri: List[Pck]
    :return: The function `orthocenter` returns a `CKPlanePrim<P>` object.

    Examples:
        >>> from projgeom_py.hyp_point import HypLine, HypPoint
        >>> t = orthocenter([HypPoint([0, 1, 0]), HypPoint([0, 0, 1]), HypPoint([1, 0, 0])])
        >>> t == HypPoint([1, 1, 1])
        True
    """
    [a1, a2, a3] = tri
    t1 = altitude(a1, a2.circ(a3))
    t2 = altitude(a2, a3.circ(a1))
    return t1.circ(t2)


def tri_altitude(tri):
    """
    The function `tri_altitude` calculates the altitudes of a triangle given its side lengths.

    :param tri: The `tri` parameter is a list containing three elements. Each element represents a side of a triangle
    :return: a list of altitudes of a triangle.
    """
    [a1, a2, a3] = tri
    t1 = altitude(a1, a2.circ(a3))
    t2 = altitude(a2, a3.circ(a1))
    t3 = altitude(a3, a1.circ(a2))
    return [t1, t2, t3]


# trait CKPlane<L, V: Default + Eq>: ProjPlane<L, V> + CKPlanePrim<L> {}


def reflect(mirror: CKPlane, p: CKPlane):
    """
    The `reflect` function performs a reflection of a plane `p` across a mirror plane `mirror`.

    :param mirror: The `mirror` parameter is of type `CKPlane<L>`, which represents a mirror plane. It is used to define the mirror in which the point `p` will be reflected
    :type mirror: CKPlane
    :param p: The parameter `p` represents a CKPlane object
    :type p: CKPlane

    Examples:
        >>> from projgeom_py.hyp_point import HypLine, HypPoint
        >>> t = reflect(HypLine([0, 1, 0]), HypPoint([0, 0, 1]))
        >>> t == HypPoint([0, 1, 0])
        False
    """
    involution(mirror.perp(), mirror, p)
