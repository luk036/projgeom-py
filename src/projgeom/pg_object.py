from abc import abstractmethod
from typing import List, TypeVar

from typing_extensions import Self

from .pg_plane import ProjectivePlane

Dual = TypeVar("Dual", bound="PgObject")


def dot(vec_a: List[int], vec_b: List[int]) -> int:
    """
    The `dot` function calculates the dot product of two lists of integers.

    :param vec_a: a is a list of integers
    :type vec_a: List[int]
    :param vec_b: The parameter `vec_b` is a list of integers
    :type vec_b: List[int]
    :return: The function `dot` returns the dot product of two lists of integers.

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

    :param lambda_: lambda_ is an integer representing the scalar coefficient for the first vector vec_a in the Plucker operation
    :type lambda_: int
    :param vec_a: The parameter `vec_a` is a list of three integers
    :type vec_a: List[int]
    :param mu_: The `mu_` parameter represents a scalar value that is used in the Plucker operation.
    :type mu_: int
    :param vec_b: The parameter `vec_b` is a list of integers
    :type vec_b: List[int]
    :return: The `plckr` function returns a list of three integers.

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
        self.coord = coord

    # impl PartialEq for PgObject:

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
    def dual(self) -> type:
        pass

    def aux(self) -> Dual:
        """
        The `aux` function returns a `Dual` object with a copy of the `coord` attribute.
        :return: The `aux` function is returning a `Dual` object.
        """
        # Line = self.dual()
        return self.dual()(self.coord.copy())

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

    def parametrize(self, lambda_: int, pt_q: Self, mu_: int) -> Self:
        """Homogeneous parametrization of point or line

        :param lambda_: The parameter `lambda_` represents the index of the coordinate to be used in the parametrize operation
        :type lambda_: int
        :param pt_q: The parameter `pt_q` is an instance of the `PgObject` class
        :type pt_q: Self
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
        return Point(plckr(lambda_, self.coord, mu_, pt_q.coord))

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
        :type rhs: Self
        :return: a Dual object.
        """
        return self.dual()(cross(self.coord, rhs.coord))


class PgPoint(PgObject["PgLine"]):
    """Projective Geometry Point

    The `PgPoint` class represents a point in projective geometry and has a method `dual()` that returns
    the dual line of the point.

    Examples:
        >>> from projgeom.pg_object import PgPoint, PgLine
        >>> pt_p = PgPoint([1, 2, 3])
        >>> ln_l = pt_p.aux()
        >>> assert isinstance(ln_l, PgLine)
        >>> assert not pt_p.incident(ln_l)
    """

    def dual(self) -> type:
        """
        The `dual` function returns the type `PgLine`.
        :return: The `dual` method is returning the type `PgLine`.
        """
        return PgLine


class PgLine(PgObject[PgPoint]):
    """Projective Geometry Line

    The `PgLine` class represents a projective geometry line and has a method `dual()` that returns the
    dual object, which is a `PgPoint`.

    Examples:
        >>> from projgeom.pg_object import PgPoint, PgLine
        >>> ln_l = PgLine([1, 2, 3])
        >>> pt_p = ln_l.aux()
        >>> assert isinstance(pt_p, PgPoint)
        >>> assert not ln_l.incident(pt_p)
    """

    def dual(self) -> type:
        return PgPoint
