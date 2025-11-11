"""
PgObject.py

This code defines a set of classes and functions for working with projective
    geometry objects in a 2D plane. The main purpose is to represent and manipulate
    points and lines in projective space, which is a way of thinking about geometry
    that includes points at infinity.

    The code takes inputs in the form of coordinates, typically represented as
    lists of three integers. These coordinates define the position of points
    or the equation of lines in the projective plane. The outputs are various
    geometric objects (points and lines) and the results of operations
    performed on them, such as checking if a point lies on a line or
    finding the intersection of two lines.
The main class, PgObject, serves as a base for both points (PgPoint) and
    lines (PgLine). It provides common functionality like equality checking, string
    representation, and basic geometric operations. The PgPoint and PgLine classes
    are specialized versions of PgObject that represent points and lines
    respectively.

The code achieves its purpose through several key functions:

1. dot: Calculates the dot product of two vectors, which is used to check if points lie on lines.
2. cross: Computes the cross product of two vectors, used to find intersections of lines.
3. plckr: Performs a linear combination of two vectors, useful for parametrizing points and lines.

The main logic flow involves creating PgPoint and PgLine objects, then
    using their methods to perform geometric operations. For example, you can
    check if a point is incident to a line, find the intersection of two
    lines, or create a line passing through two points.

An important concept in this code is duality, where points and lines can be interchanged.
    This is represented by the 'aux' method, which returns the dual object (a line for a point, or a point for a line).

The code uses abstract methods and type hinting to ensure proper implementation
    and usage of the geometric objects. It also includes docstrings and examples to
    help users understand how to use the classes and functions.

Overall, this code provides a foundation for working with projective geometry,
    allowing users to create and manipulate geometric objects in a way that's
    consistent with the mathematical principles of projective spaces.
"""

from abc import abstractmethod
from typing import List, TypeVar, cast, Self

from .pg_plane import ProjectivePlane, Value

Dual = TypeVar("Dual", bound="PgObject")


def dot(vec_a: List[int], vec_b: List[int]) -> int:
    """
    The `dot` function calculates the dot product of two lists of integers.

    :param vec_a: a is a list of integers
    :type vec_a: List[int]
    :param vec_b: The parameter `vec_b` is a list of integers
    :type vec_b: List[int]
    :return: The function `dot` returns the dot product of two lists of integers.

    .. svgbob::
       :align: center

        a . b = |a| |b| cos(theta)

    Examples:
        >>> dot([1, 2, 3], [4, 5, 6])
        32
        >>> dot([1, 2, 3], [4, 5, 6]) == 32
        True
    """
    return vec_a[0] * vec_b[0] + vec_a[1] * vec_b[1] + vec_a[2] * vec_b[2]


def cross(vec_a: List[int], vec_b: List[int]) -> List[int]:
    """
    The `cross` function calculates the cross product of two vectors.

    :param vec_a: a is a list of integers
    :type vec_a: List[int]
    :param vec_b: The parameter `vec_b` is a list of integers
    :type vec_b: List[int]
    :return: The function `cross` returns a list of three integers.

    .. svgbob::
       :align: center

          a x b
          ^
          |
          |  /
          | /
          |/
          +------> b
         /
        /
       a

    Examples:
        >>> cross([1, 2, 3], [4, 5, 6])
        [-3, 6, -3]
        >>> cross([1, 2, 3], [4, 5, 6]) == [-3, 6, -3]
        True
    """
    return [
        vec_a[1] * vec_b[2] - vec_a[2] * vec_b[1],
        vec_a[2] * vec_b[0] - vec_a[0] * vec_b[2],
        vec_a[0] * vec_b[1] - vec_a[1] * vec_b[0],
    ]


def plckr(lambda_: int, vec_a: List[int], mu_: int, vec_b: List[int]) -> List[int]:
    """Homogeneous parametrization of point or line

    :param lambda_: lambda_ is an integer representing the scalar coefficient for
    the first vector vec_a in the Plucker operation
    :type lambda_: int
    :param vec_a: The parameter `vec_a` is a list of three integers
    :type vec_a: List[int]
    :param mu_: The `mu_` parameter represents a scalar value that is used in the
    Plucker operation
    :type mu_: int
    :param vec_b: The parameter `vec_b` is a list of integers
    :type vec_b: List[int]
    :return: The `plckr` function returns a list of three integers.

    .. svgbob::
       :align: center

          a * lambda + b * mu

    Examples:
        >>> plckr(1, [1, 2, 3], 2, [4, 5, 6])
        [9, 12, 15]
        >>> plckr(1, [1, 2, 3], 2, [4, 5, 6]) == [9, 12, 15]
        True
    """
    return [
        lambda_ * vec_a[0] + mu_ * vec_b[0],
        lambda_ * vec_a[1] + mu_ * vec_b[1],
        lambda_ * vec_a[2] + mu_ * vec_b[2],
    ]


# The `PgObject` class represents a geometric object in a projective plane with integer coordinates.
class PgObject(ProjectivePlane[Dual, int]):
    """
    The `PgObject` class represents a geometric object in a projective plane with integer coordinates.

    :param coord: The `coord` parameter represents a list of three integers that represent the
        coordinates of the geometric object.
    :type coord: List[int]
    :raises ValueError: The `coord` parameter must be a list of three integers.

    Examples:
        >>> pt_p = PgObject([3, 4, 5])
        >>> pt_p.coord
        [3, 4, 5]
    """

    coord: List[int]

    # impl PgObject:

    def __init__(self, coord: List[int]) -> None:
        """
        The function initializes an object with a given coordinate.

        :param coord: The `coord` parameter is a list of integers that represents the coordinates of a
            point in a three-dimensional space
        :type coord: List[int]

        Examples:
            >>> pt_p = PgObject([3, 4, 5])
            >>> pt_p.coord
            [3, 4, 5]
        """
        if len(coord) != 3:
            raise ValueError("coord must be a list of three integers")
        self.coord = coord

    # impl PartialEq for PgObject:

    def __repr__(self):
        """repr(self)"""
        return f"{self.__class__.__name__}({self.coord[0]} : {self.coord[1]} : {self.coord[2]})"

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> pt_p = PgObject([3, 4, 5])
            >>> print(pt_p)
            (3 : 4 : 5)
        """
        return f"({self.coord[0]} : {self.coord[1]} : {self.coord[2]})"

    def __eq__(self, other) -> bool:
        """
        The function checks if two PgObject instances are equal by comparing their coordinates.

        :param other: The `other` parameter is of type `PgObject`
        :return: The `__eq__` method is returning a boolean value. It returns `True` if the `coord`
            attribute of `self` and `other` are equal, and `False` otherwise.

        Examples:
           >>> pt_p = PgObject([3, 4, 5])
           >>> pt_q = PgObject([30, 40, 50])
           >>> pt_p == pt_q
           True
        """
        if type(self) is not type(other):
            return False
        return cross(self.coord, other.coord) == [0, 0, 0]

    # impl ProjectivePlane<PgLine, int> for PgObject:

    @abstractmethod
    def dual_type(self) -> type:
        pass

    def aux(self) -> Dual:
        """
        The `aux` function returns a `Dual` object with a copy of the `coord` attribute.
        :return: The `aux` function is returning a `Dual` object.
        """
        # Line = self.dual_type()
        return self.dual_type()(self.coord.copy())

    def dot(self, line) -> int:
        """
        The `dot` function calculates the dot product between two vectors.

        :param line: The `line` parameter is of type `PgLine`
        :return: The dot method is returning an integer value.

        Examples:
            >>> pt_p = PgObject([3, 4, 5])
            >>> ln_l = PgObject([30, 40, 50])
            >>> pt_p.dot(ln_l)
            500
        """
        return dot(self.coord, line.coord)

    def parametrize(self, lambda_: Value, pt_q: Self, mu_: Value) -> Self:
        """Homogeneous parametrization of point or line

        :param lambda_: The parameter `lambda_` represents the index of the coordinate to be used in the parametrize operation
        :type lambda_: int
        :param pt_q: The parameter `pt_q` is an instance of the `PgObject` class
        :type pt_q: "PgObject[Dual]"
        :param mu_: The parameter `mu_` is an integer that represents the scalar multiplier for the `pt_q` object in the parametrize operation
        :type mu_: int
        :return: The parametrize method returns an instance of the PgObject class.

        Examples:
            >>> pt_p = PgObject([1, 2, 3])
            >>> pt_q = PgObject([4, 5, 6])
            >>> pt_p.parametrize(1, pt_q, 2) == PgObject([9, 12, 15])
            True
        """
        Point = type(self)
        # Cast pt_q to PgObject[Dual] to access .coord
        pg_q = cast("PgObject[Dual]", pt_q)
        return Point(plckr(lambda_, self.coord, mu_, pg_q.coord))

    # impl ProjectivePlanePrimitive<PgLine> for PgObject:

    def incident(self, rhs: Dual) -> bool:
        """
        The function checks if two objects have a zero dot product.

        :param rhs: The parameter `rhs` is of type `Dual` and represents the right-hand side of the equation
        :type rhs: Dual
        :return: a boolean value.

        Examples:
            >>> pt_p = PgObject([1, 2, 3])
            >>> ln_l = PgObject([4, 5, 6])
            >>> pt_p.incident(ln_l)
            False
        """
        return dot(self.coord, rhs.coord) == 0

    def meet(self, rhs: Self) -> Dual:
        """
        The `meet` function performs a join or meet operation on two `PgObject` objects and returns a
        `Dual` object.

        :param rhs: The parameter `rhs` stands for "right-hand side" and it represents another `PgObject` object that is being passed as an argument to the `meet` method
        :type rhs: "PgObject[Dual]"
        :return: a Dual object.

        Examples:
            >>> from projgeom.pg_object import PgPoint, PgLine
            >>> p1 = PgPoint([1, 2, 3])
            >>> p2 = PgPoint([4, 5, 6])
            >>> p1.meet(p2)
            PgLine(-3 : 6 : -3)
        """
        # Cast rhs to PgObject[Dual] to access .coord
        pg_rhs = cast("PgObject[Dual]", rhs)
        return self.dual_type()(cross(self.coord, pg_rhs.coord))


class PgPoint(PgObject["PgLine"]):
    """Projective Geometry Point

    The `PgPoint` class represents a point in projective geometry and has a method `dual()` that returns
    the dual line of the point.

    .. svgbob::
       :align: center

          / \
         / _ \
        | / \ |
        | \_/ |
         \ _ /
          \ /

    Examples:
        >>> from projgeom.pg_object import PgPoint, PgLine
        >>> pt_p = PgPoint([1, 2, 3])
        >>> ln_l = pt_p.aux()
        >>> assert isinstance(ln_l, PgLine)
        >>> assert not pt_p.incident(ln_l)
    """

    def dual_type(self) -> type:
        """
        The `dual` function returns the type `PgLine`.
        :return: The `dual` method is returning the type `PgLine`.
        """
        return PgLine


class PgLine(PgObject[PgPoint]):
    """Projective Geometry Line

    The `PgLine` class represents a projective geometry line and has a method `dual()` that returns the
    dual object, which is a `PgPoint`.

    .. svgbob::
       :align: center

          / \
         / _ \
        | / \ |
        | \_/ |
         \ _ /
          \ /

    Examples:
        >>> from projgeom.pg_object import PgPoint, PgLine
        >>> ln_l = PgLine([1, 2, 3])
        >>> pt_p = ln_l.aux()
        >>> assert isinstance(pt_p, PgPoint)
        >>> assert not ln_l.incident(pt_p)
    """

    def dual_type(self) -> type:
        return PgPoint
