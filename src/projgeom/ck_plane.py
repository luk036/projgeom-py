from abc import abstractmethod
from typing import List, TypeVar

from .pg_plane import ProjectivePlane, Value, involution

# CayleyKleinPlanePrimitive = Union[HyperbolicLine, HyperbolicPoint]

# trait CayleyKleinPlanePrimitive<Line>: ProjectivePlanePrimitive<Line>:
#     def perp(self) -> Line

Dual = TypeVar("Dual", bound="CayleyKleinPlane")


class CayleyKleinPlane(ProjectivePlane[Dual, Value]):
    """
    The class CayleyKleinPlane represents a Cayley-Klein plane in projective geometry.
    """

    @abstractmethod
    def perp(self) -> Dual:
        """Pole or Polar

        The `perp` function returns the pole or polar of an object.
        """
        pass


PointCk = CayleyKleinPlane["LineCk", Value]
LineCk = CayleyKleinPlane["PointCk", Value]


def is_perpendicular(l_1: LineCk, l_2: LineCk) -> bool:
    """
    The function `is_perpendicular` checks if two lines are perpendicular.

    :param l_1: The parameter `l_1` represents a line in Cayley-Klein geometry. It is of type `LineCk`, which is likely a custom class representing a hyperbolic line
    :type l_1: LineCk
    :param l_2: The parameter `l_2` represents a line in Cayley-Klein geometry
    :type l_2: LineCk
    :return: a boolean value, indicating whether the two given lines are perpendicular to each other.

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> is_perpendicular(HyperbolicLine([0, 1, 0]), HyperbolicLine([0, 0, 1]))
        True
        >>> is_perpendicular(HyperbolicLine([0, 1, 0]), HyperbolicLine([0, 0, -1]))
        True
    """
    return l_1.perp().incident(l_2)


def altitude(pt_p: PointCk, ln_l: LineCk) -> LineCk:
    """
    The `altitude` function calculates the altitude of a point `pt_p` with respect to a line `ln_l` in a
    Cayley-Klein geometry.

    :param pt_p: pt_p is a CayleyKleinPlanePrimitive object representing a point in three-dimensional space
    :type pt_p: PointCk
    :param ln_l: ln_l is a CayleyKleinPlanePrimitive object representing a line in a hyperbolic plane
    :type ln_l: LineCk
    :return: The function `altitude` returns a `CayleyKleinPlanePrimitive<Line>` object.

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> t = altitude(HyperbolicPoint([0, 1, 0]), HyperbolicLine([0, 0, 1]))
        >>> t == HyperbolicLine([1, 0, 0])
        True
    """
    return ln_l.perp().meet(pt_p)


def orthocenter(triangle: List[PointCk]):
    """
    The `orthocenter` function calculates the orthocenter of a triangle in Cayley-Klein geometry.

    :param triangle: The `triangle` parameter is a list of three `CayleyKleinPlanePrimitive<Point>` objects.
    :type triangle: List[PointCk]
    :return: The function `orthocenter` returns a `CayleyKleinPlanePrimitive<Point>` object.

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> t = orthocenter([HyperbolicPoint([0, 1, 0]), HyperbolicPoint([0, 0, 1]), HyperbolicPoint([1, 0, 0])])
        >>> t == HyperbolicPoint([1, 1, 1])
        True
    """
    [a_1, a_2, a_3] = triangle
    t_1 = altitude(a_1, a_2.meet(a_3))
    t_2 = altitude(a_2, a_3.meet(a_1))
    return t_1.meet(t_2)


def tri_altitude(triangle):
    """
    The function `tri_altitude` calculates the altitudes of a triangle.

    :param triangle: The `triangle` parameter is a list containing three elements. Each element represents a side of a triangle
    :return: a list of altitudes of a triangle.
    """
    [a_1, a_2, a_3] = triangle
    t_1 = altitude(a_1, a_2.meet(a_3))
    t_2 = altitude(a_2, a_3.meet(a_1))
    t_3 = altitude(a_3, a_1.meet(a_2))
    return [t_1, t_2, t_3]


# trait CayleyKleinPlane<Line, Value: Default + Eq>: ProjectivePlane<Line, Value> + CayleyKleinPlanePrimitive<Line> {}


def reflect(mirror: CayleyKleinPlane, pt_p: CayleyKleinPlane):
    """
    The `reflect` function performs a reflection of a plane `pt_p` across a mirror plane `mirror`.

    :param mirror: The `mirror` parameter is of type `CayleyKleinPlane<Line>`, which represents a mirror plane. It is used to define the mirror in which the point `pt_p` will be reflected
    :type mirror: CayleyKleinPlane
    :param pt_p: The parameter `pt_p` represents a CayleyKleinPlane object
    :type pt_p: CayleyKleinPlane

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> t = reflect(HyperbolicLine([0, 1, 0]), HyperbolicPoint([0, 0, 1]))
        >>> t == HyperbolicPoint([0, 1, 0])
        False
    """
    involution(mirror.perp(), mirror, pt_p)
