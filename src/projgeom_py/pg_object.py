from typing import List
from typing import TypeVar
from typing_extensions import Self
from abc import abstractmethod
from .pg_plane import ProjPlane

Dual = TypeVar("Dual", bound="PgObject")


def dot(a: List[int], b: List[int]) -> int:
    """
    The `dot` function calculates the dot product of two lists of integers.
    
    :param a: a is a list of integers
    :type a: List[int]
    :param b: The parameter `b` is a list of integers
    :type b: List[int]
    :return: The function `dot` returns the dot product of two lists of integers.

    Examples:
        >>> dot([1, 2, 3], [4, 5, 6])
        32
        >>> dot([1, 2, 3], [4, 5, 6]) == 32
        True
    """
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: List[int], b: List[int]) -> List[int]:
    """
    The `cross` function calculates the cross product of two vectors.
    
    :param a: a is a list of integers
    :type a: List[int]
    :param b: The parameter `b` is a list of integers
    :type b: List[int]
    :return: The function `cross` returns a list of three integers.

    Examples:
        >>> cross([1, 2, 3], [4, 5, 6])
        [-3, 6, -3]
        >>> cross([1, 2, 3], [4, 5, 6]) == [-3, 6, -3]
        True
    """
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def plckr(ld: int, p: List[int], mu: int, q: List[int]) -> List[int]:
    """
    The `plckr` function calculates the Plucker operation by multiplying each element of `p` by `ld` and
    each element of `q` by `mu`, and then adding the corresponding elements together.
    
    :param ld: ld is an integer representing the scalar coefficient for the first vector p in the
    Plucker operation
    :type ld: int
    :param p: The parameter `p` is a list of three integers
    :type p: List[int]
    :param mu: The `mu` parameter represents a scalar value that is used in the Plucker operation. It is
    multiplied with the corresponding elements of the `q` list to calculate the result
    :type mu: int
    :param q: The parameter `q` is a list of integers
    :type q: List[int]
    :return: The `plckr` function returns a list of three integers.

    Examples:
        >>> plckr(1, [1, 2, 3], 2, [4, 5, 6])
        [9, 12, 15]
        >>> plckr(1, [1, 2, 3], 2, [4, 5, 6]) == [9, 12, 15]
        True
    """
    return [
        ld * p[0] + mu * q[0],
        ld * p[1] + mu * q[1],
        ld * p[2] + mu * q[2],
    ]


# The `PgObject` class represents a geometric object in a projective plane with integer coordinates.
class PgObject(ProjPlane[Dual, int]):
    """
    The `PgObject` class represents a geometric object in a projective plane with integer coordinates.

    :param coord: The `coord` parameter represents a list of three integers that represent the
    coordinates of the geometric object.
    :type coord: List[int]
    :raises ValueError: The `coord` parameter must be a list of three integers.

    Examples:
        >>> p = PgObject([3, 4, 5])
        >>> p.coord
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
           >>> p = PgObject([3, 4, 5])
           >>> p.coord
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
           >>> p = PgObject([3, 4, 5])
           >>> q = PgObject([30, 40, 50])
           >>> p == q
           True
        """
        if type(self) != type(other):
            return False
        return cross(self.coord, other.coord) == [0, 0, 0]

    # impl ProjPlane<PgLine, int> for PgObject:

    @abstractmethod
    def dual(self) -> type:
        pass

    def aux(self) -> Dual:
        """
        The `aux` function returns a `Dual` object with a copy of the `coord` attribute.
        :return: The `aux` function is returning a `Dual` object.
        """
        # L = self.dual()
        return self.dual()(self.coord.copy())

    def dot(self, line) -> int:
        """basic measurement

        Args:
            line (PgLine): _description_

        Returns:
            int: _description_

        Examples:
            >>> p = PgObject([3, 4, 5])
            >>> q = PgObject([30, 40, 50])
            >>> p.dot(q)
            500
        """
        return dot(self.coord, line.coord)

    def plucker(self, ld: int, q: Self, mu: int) -> Self:
        """_summary_

        Args:
            ld (int): _description_
            p (PgObject): _description_
            mu (int): _description_
            q (PgObject): _description_

        Returns:
            PgObject: _description_

        Examples:
            >>> p = PgObject([1, 2, 3])
            >>> q = PgObject([4, 5, 6])
            >>> p.plucker(1, q, 2) == PgObject([9, 12, 15])
            True
        """
        P = type(self)
        return P(plckr(ld, self.coord, mu, q.coord))

    # impl ProjPlanePrim<PgLine> for PgObject:

    def incident(self, rhs: Dual) -> bool:
        """_summary_

        Args:
            rhs (PgLine): _description_

        Returns:
            bool: _description_
        """
        return dot(self.coord, rhs.coord) == 0

    def circ(self, rhs: Self) -> Dual:
        """_summary_

        Args:
            rhs (PgObject): _description_

        Returns:
            Dual: _description_
        """
        return self.dual()(cross(self.coord, rhs.coord))
