"""
Core projective geometry objects (PgObject, PgPoint, PgLine).

Defines points and lines in homogeneous coordinates, with dot/cross
product helpers for incidence and meet operations.







"""

from typing import List, Self, Type, TypeVar, cast

from .pg_plane import ProjectivePlane, Value

Dual = TypeVar("Dual", bound="PgObject")  # type: ignore[type-arg]


def dot(v_a: List[int], v_b: List[int]) -> int:
    r"""Dot product of two homogeneous coordinate vectors.

    For projective coordinates :math:`\mathbf{a} = (a_1:a_2:a_3)` and
    :math:`\mathbf{b} = (b_1:b_2:b_3)`:

    .. math::

       \mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2 + a_3 b_3

    A point is incident with a line when their dot product is zero.

    :param v_a: First vector :math:`(a_1,a_2,a_3)`
    :param v_b: Second vector :math:`(b_1,b_2,b_3)`
    :return: The dot product

    Examples:
        >>> dot([1, 2, 3], [4, 5, 6])
        32
    """
    return v_a[0] * v_b[0] + v_a[1] * v_b[1] + v_a[2] * v_b[2]


def cross(v_a: List[int], v_b: List[int]) -> List[int]:
    r"""Cross product of two homogeneous coordinate vectors.

    For :math:`\mathbf{a} = (a_1:a_2:a_3)` and
    :math:`\mathbf{b} = (b_1:b_2:b_3)`:

    .. math::

       \mathbf{a} \times \mathbf{b} =
       \bigl(a_2 b_3 - a_3 b_2,\;
             a_3 b_1 - a_1 b_3,\;
             a_1 b_2 - a_2 b_1\bigr)

    In projective geometry the cross product gives the line through two
    points, or the intersection point of two lines.

    :param v_a: First vector :math:`(a_1,a_2,a_3)`
    :param v_b: Second vector :math:`(b_1,b_2,b_3)`
    :return: The cross product vector

    Examples:
        >>> cross([1, 2, 3], [4, 5, 6])
        [-3, 6, -3]
    """
    return [
        v_a[1] * v_b[2] - v_a[2] * v_b[1],
        v_a[2] * v_b[0] - v_a[0] * v_b[2],
        v_a[0] * v_b[1] - v_a[1] * v_b[0],
    ]


def cross0(v_a: List[int], v_b: List[int]) -> int:
    r"""Cross product 0th component (yz-plane projection).

    .. math::

        \mathrm{cross}_0(v_a,v_b) = v_{a,y} v_{b,z} - v_{b,y} v_{a,z}

    :param v_a: First vector :math:`(a_1,a_2,a_3)`.
    :param v_b: Second vector :math:`(b_1,b_2,b_3)`.
    :return: The yz-plane cross component.

    Examples:
        >>> cross0([1, 2, 3], [4, 5, 6])
        -3
    """
    return v_a[1] * v_b[2] - v_b[1] * v_a[2]


def cross1(v_a: List[int], v_b: List[int]) -> int:
    r"""Cross product 1st component (xz-plane projection).

    .. math::

        \mathrm{cross}_1(v_a,v_b) = v_{a,x} v_{b,z} - v_{b,x} v_{a,z}

    :param v_a: First vector :math:`(a_1,a_2,a_3)`.
    :param v_b: Second vector :math:`(b_1,b_2,b_3)`.
    :return: The xz-plane cross component.

    Examples:
        >>> cross1([1, 2, 3], [4, 5, 6])
        -6
    """
    return v_a[0] * v_b[2] - v_b[0] * v_a[2]


def cross2(v_a: List[int], v_b: List[int]) -> int:
    r"""Cross product (2d) — xy-plane projection.

    .. math::

        \mathrm{cross}_2(v_a, v_b) = v_{a,x} v_{b,y} - v_{a,y} v_{b,x}

    :param v_a: First vector :math:`(a_1,a_2)`.
    :param v_b: Second vector :math:`(b_1,b_2)`.
    :return: The 2d cross product.

    Examples:
        >>> cross2([1, 2], [3, 4])
        -2
    """
    return v_a[0] * v_b[1] - v_a[1] * v_b[0]


def dot1(v_a: List[int], v_b: List[int]) -> int:
    r"""Dot product of the (x,y)-components (affine part).

    .. math::

        \mathrm{dot}_1(v_a, v_b) = v_{a,x} v_{b,x} + v_{a,y} v_{b,y}

    :param v_a: First vector :math:`(a_1,a_2)`.
    :param v_b: Second vector :math:`(b_1,b_2)`.
    :return: The affine dot product.

    Examples:
        >>> dot1([1, 2], [3, 4])
        11
    """
    return v_a[0] * v_b[0] + v_a[1] * v_b[1]


def sq(val: int) -> int:
    r"""Square function.

    :param val: The value to square.
    :return: ``val * val``.

    Examples:
        >>> sq(5)
        25
    """
    return val * val


def plckr(lambda_val: int, v_a: List[int], mu_val: int, v_b: List[int]) -> List[int]:
    r"""Linear combination (Plücker parametrisation) of two coordinates.

    Computes the linear combination:

    .. math::

       \lambda \mathbf{a} + \mu \mathbf{b} =
       (\lambda a_1 + \mu b_1,\;
        \lambda a_2 + \mu b_2,\;
        \lambda a_3 + \mu b_3)

    This gives a point on the line through :math:`\mathbf{a}` and
    :math:`\mathbf{b}` (or a line through their meet).

    :param lambda_val: Scalar :math:`\lambda`
    :param v_a: First vector :math:`(a_1,a_2,a_3)`
    :param mu_val: Scalar :math:`\mu`
    :param v_b: Second vector :math:`(b_1,b_2,b_3)`
    :return: The linear combination :math:`\lambda\mathbf{a} + \mu\mathbf{b}`

    Examples:
        >>> plckr(1, [1, 2, 3], 2, [4, 5, 6])
        [9, 12, 15]
        >>> plckr(1, [1, 2, 3], 2, [4, 5, 6]) == [9, 12, 15]
        True
    """
    return [
        lambda_val * v_a[0] + mu_val * v_b[0],
        lambda_val * v_a[1] + mu_val * v_b[1],
        lambda_val * v_a[2] + mu_val * v_b[2],
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.coord[0]} : {self.coord[1]} : {self.coord[2]})"

    def __str__(self) -> str:
        """String representation of the projective object.

        :return: A string in the form (x : y : z).

        Examples:
            >>> pt_p = PgObject([3, 4, 5])
            >>> print(pt_p)
            (3 : 4 : 5)
        """
        return f"({self.coord[0]} : {self.coord[1]} : {self.coord[2]})"

    def __eq__(self, other: object) -> bool:
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
        if not isinstance(other, PgObject):
            return False
        return cross(self.coord, other.coord) == [0, 0, 0]

    def dual_type(self) -> Type[Dual]:
        """Returns the type of the dual object.

        :return: The type of the dual geometric object.
        """
        return PgLine  # type: ignore[return-value]

    def aux(self) -> Dual:
        """Returns a dual object not incident with this object.

        :return: A Dual object with a copy of the coordinates.
        """
        return self.dual_type()(self.coord.copy())

    def dot(self, line: Dual) -> int:
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

    def parametrize(self, lambda_val: Value, pt_q: Self, mu_val: Value) -> Self:
        r"""Homogeneous parametrization of point or line

        :param lambda_val: Scalar coefficient :math:`\lambda` for self
        :param pt_q: The other point/line
        :param mu_val: Scalar coefficient :math:`\mu` for pt_q
        :return: The parametrized point/line

        Examples:
            >>> pt_p = PgObject([1, 2, 3])
            >>> pt_q = PgObject([4, 5, 6])
            >>> pt_p.parametrize(1, pt_q, 2) == PgObject([9, 12, 15])
            True
        """
        Point = type(self)
        pg_q = cast("PgObject[Dual]", pt_q)
        return Point(plckr(lambda_val, self.coord, mu_val, pg_q.coord))

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

    The `PgPoint` class represents a point in projective geometry and has a method `dual_type()` that returns
    the type of the dual object (a line).

    .. svgbob::
       :align: center

          / \\
         / _ \\
        | / \\ |
        | \\_/ |
         \\ _ /
          \\ /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (PgLine for PgPoint).

        :return: The type of the dual geometric object.
        """
        return PgLine


class PgLine(PgObject[PgPoint]):
    """Projective Geometry Line

    The `PgLine` class represents a projective geometry line and has a method `dual_type()` that returns
    the type of the dual object, which is a `PgPoint`.

    .. svgbob::
       :align: center

          / \\
         / _ \\
        | / \\ |
        | \\_/ |
         \\ _ /
          \\ /

    Examples:
        >>> from projgeom.pg_object import PgPoint, PgLine
        >>> ln_l = PgLine([1, 2, 3])
        >>> pt_p = ln_l.aux()
        >>> assert isinstance(pt_p, PgPoint)
        >>> assert not ln_l.incident(pt_p)
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (PgPoint for PgLine).

        :return: The type of the dual geometric object.
        """
        return PgPoint
