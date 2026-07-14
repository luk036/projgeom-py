"""
Cayley-Klein Plane (ck_plane.py)

This code defines a set of classes and functions for working with Cayley-Klein
    planes, which are a type of geometric structure used in projective geometry. The
    purpose of this code is to provide tools for performing calculations and
    operations in Cayley-Klein geometry.

The main input for this code is geometric objects like points and lines in a
    Cayley-Klein plane. These are represented by the CayleyKleinPlane class and its
    subclasses PointCk and LineCk. The code doesn't take direct user input, but
    rather provides a framework for working with these geometric objects
    programmatically.

The outputs of this code are various geometric calculations and transformations.
    For example, it can determine if two lines are perpendicular, calculate the
    altitude of a point with respect to a line, find the orthocenter of a
    triangle, or reflect a point across a mirror plane.

The code achieves its purpose through a series of mathematical operations and
    geometric algorithms. It uses abstract methods and type hinting to define the
    structure of Cayley-Klein planes and their properties. The actual calculations are performed in functions like is_perpendicular,
    altitude, orthocenter, and reflect.

Some important logic flows in this code include:

1. The use of the perp() method to find polar lines or poles of points, which are essential for various geometric constructions. Note: perp() represents the polar/pole operation in projective geometry, not perpendicular.
2. The calculation of altitudes using the meet() operation between lines and points.
3. The determination of the orthocenter by finding the intersection of two altitudes of a triangle.
4. The reflection of points using an involution operation.

The code uses object-oriented programming concepts to represent geometric
    entities and their relationships. It also employs type hinting and abstract
    methods to ensure proper usage of the classes and functions. While the actual
    mathematical operations are not fully implemented in this snippet, the code
    provides a clear structure for how these geometric calculations should be
    performed in a Cayley-Klein plane.
"""

from abc import abstractmethod
from typing import Generic, List, TypeVar, cast

from .pg_plane import Point, ProjectivePlane, Value, involution

# CayleyKleinPlanePrimitive = Union[HyperbolicLine, HyperbolicPoint]

# trait CayleyKleinPlanePrimitive<Line>: ProjectivePlanePrimitive<Line>:
#     def perp(self) -> Line

Dual = TypeVar("Dual", bound="CayleyKleinPlane")  # type: ignore[type-arg]


class CayleyKleinPlane(ProjectivePlane[Dual, Value], Generic[Dual, Value]):
    """
    The class CayleyKleinPlane represents a Cayley-Klein plane in projective geometry.
    """

    @abstractmethod
    def perp(self) -> Dual:
        """Pole or Polar

        The `perp` function returns the pole or polar of an object.
        Note: This represents the polar/pole operation in projective geometry, not perpendicular.
        """
        pass


PointCk = CayleyKleinPlane["LineCk", int]
LineCk = CayleyKleinPlane["PointCk", int]


def is_perpendicular(ln_l: LineCk, ln_m: LineCk) -> bool:
    r"""Check if two lines are perpendicular in Cayley–Klein geometry.

    Two lines :math:`\ell_1, \ell_2` are perpendicular when the pole of
    one lies on the other:

    .. math::

       \ell_1 \perp \ell_2 \iff \text{pole}(\ell_1) \in \ell_2

    :param ln_l: The parameter `ln_l` represents a line in Cayley-Klein geometry. It is of type `LineCk`, which is likely a custom class representing a hyperbolic line
    :type ln_l: LineCk
    :param ln_m: The parameter `ln_m` represents a line in Cayley-Klein geometry
    :type ln_m: LineCk
    :return: a boolean value, indicating whether the two given lines are perpendicular to each other.

    .. svgbob::
       :align: center

           l perpendicular to m
          /
         /
        /_____ m
       /
      /
     l

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> is_perpendicular(HyperbolicLine([0, 1, 0]), HyperbolicLine([0, 0, 1]))
        True
        >>> is_perpendicular(HyperbolicLine([0, 1, 0]), HyperbolicLine([0, 0, -1]))
        True
    """
    return ln_l.perp().incident(ln_m)


def altitude(pt_p: PointCk, ln_l: LineCk) -> LineCk:
    r"""Altitude of a point with respect to a line.

    The altitude is the line through :math:`P` that is perpendicular to
    :math:`\ell`. In Cayley–Klein geometry, perpendicularity is defined
    via the pole–polar relationship:

    .. math::

       \text{altitude}(P, \ell) = \text{polar}(\ell) \wedge P

    where :math:`\text{polar}(\ell)` is the pole of :math:`\ell` and
    :math:`\wedge` denotes the meet (intersection) operation.

    :param pt_p: Point :math:`P`
    :param ln_l: Line :math:`\ell`
    :return: The altitude line through :math:`P` perpendicular to :math:`\ell`

    .. svgbob::
       :align: center

             P
             |
             |
       l ----*-----------
             Q

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> t = altitude(HyperbolicPoint([0, 1, 0]), HyperbolicLine([0, 0, 1]))
        >>> t == HyperbolicLine([1, 0, 0])
        True
    """
    return ln_l.perp().meet(pt_p)


def orthocenter(triangle: List[PointCk]) -> PointCk:
    r"""Orthocenter of a triangle in Cayley–Klein geometry.

    The orthocenter :math:`H` is the intersection of two altitudes:

    .. math::

       H = \text{altitude}(A, BC) \wedge \text{altitude}(B, CA)

    where :math:`\text{altitude}(P, \ell)` is the line through :math:`P`
    perpendicular to :math:`\ell`.

    :param triangle: Triangle vertices :math:`[A, B, C]`
    :return: The orthocenter :math:`H`

    .. svgbob::
       :align: center

           A
           |\\
           | \\
          /   \\
         /_____\\
        B       C

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


def tri_altitude(triangle: List[PointCk]) -> List[LineCk]:
    """
    The function `tri_altitude` calculates the altitudes of a triangle.

    :param triangle: The `triangle` parameter is a list containing three elements. Each element represents a side of a triangle
    :return: a list of altitudes of a triangle.

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> triangle = [HyperbolicPoint([0, 1, 0]), HyperbolicPoint([0, 0, 1]), HyperbolicPoint([1, 0, 0])]
        >>> altitudes = tri_altitude(triangle)
        >>> len(altitudes)
        3
    """
    [a_1, a_2, a_3] = triangle
    t_1 = altitude(a_1, a_2.meet(a_3))
    t_2 = altitude(a_2, a_3.meet(a_1))
    t_3 = altitude(a_3, a_1.meet(a_2))
    return [t_1, t_2, t_3]


# trait CayleyKleinPlane<Line, Value: Default + Eq>: ProjectivePlane<Line, Value> + CayleyKleinPlanePrimitive<Line> {}


def reflect(mirror: LineCk, pt_p: PointCk) -> PointCk:
    """
    The `reflect` function performs a reflection of a point `pt_p` across a mirror line `mirror`.

    :param mirror: The `mirror` parameter is of type `CayleyKleinPlane<Line>`, which represents a mirror plane. It is used to define the mirror in which the point `pt_p` will be reflected
    :type mirror: CayleyKleinPlane
    :param pt_p: The parameter `pt_p` represents a CayleyKleinPlane object
    :type pt_p: CayleyKleinPlane

    .. svgbob::
       :align: center

        P'          P
         \\         /
          \\       /
           ._____.
              |
              |
            mirror

    Examples:
        >>> from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
        >>> t = reflect(HyperbolicLine([0, 1, 0]), HyperbolicPoint([0, 0, 1]))
        >>> t == HyperbolicPoint([0, 1, 0])
        False
    """
    return cast(
        PointCk,
        involution(
            cast(Point, mirror.perp()),
            mirror,
            cast(Point, pt_p),
        ),
    )
