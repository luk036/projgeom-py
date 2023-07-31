from .pg_object import PgObject
from typing_extensions import Self


# The PerspPoint class represents a point in a perspective plane and provides methods for calculating
# the dual, perpendicular line, and midpoint of the point.
class PerspPoint(PgObject["PerspLine"]):
    """A point in a perspective plane.

    The PerspPoint class represents a point in a perspective plane and provides methods for calculating
    the dual, perpendicular line, and midpoint of the point.
    """

    def dual(self) -> type:
        return PerspLine

    def perp(self) -> "PerspLine":
        """
        The `perp` function returns a `PerspLine` object.
        :return: The code is returning the value of the variable `L_INF`.
        """
        return L_INF

    def midpoint(self, other: Self) -> Self:
        """
        The `midpoint` function calculates the midpoint between two PerspPoint objects.

        :param other: The `other` parameter is an instance of the same class as `self`. It represents another point that you want to find the midpoint with
        :type other: Self
        :return: The `midpoint` method returns an instance of the `PerspPoint` class.
        """
        alpha = L_INF.dot(other)
        beta = L_INF.dot(self)
        return self.plucker(alpha, other, beta)


class PerspLine(PgObject[PerspPoint]):
    """A line in a perspective plane.

    The PerspLine class represents a line in a perspective plane and provides methods for calculating
    the dual and perpendicular point, as well as checking if two lines are parallel.
    """

    def dual(self) -> type:
        return PerspPoint

    def perp(self) -> PerspPoint:
        """
        The `perp` function returns a `PerspPoint` object that is obtained by taking the dot product of
        `self` with `I_RE` and `I_IM`, and then using the results to create a new `PerspPoint` object
        using the `plucker` method of `I_RE`.
        :return: a PerspPoint object.
        """
        alpha = I_RE.dot(self)
        beta = I_IM.dot(self)
        return I_RE.plucker(alpha, I_IM, beta)

    def is_parallel(self, other: Self) -> bool:
        """
        The function checks if two lines are parallel by calculating the dot product of their direction
        vectors.

        :param other: The "other" parameter is an object of the same class as the current object. It represents another instance of the class that we want to check for parallelism with the current object
        :type other: Self
        :return: a boolean value, indicating whether the two objects are parallel or not.
        """
        return L_INF.dot(self.circ(other)) == 0


I_RE = PerspPoint([0, 1, 1])
I_IM = PerspPoint([1, 0, 0])
L_INF = PerspLine([0, -1, 1])
