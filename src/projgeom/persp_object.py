from .pg_object import PgObject, plckr


# The PerspPoint class represents a point in a perspective plane and provides methods for calculating
# the dual, perpendicular line, and midpoint of the point.
class PerspPoint(PgObject["PerspLine"]):
    """A point in a perspective plane.

    The PerspPoint class represents a point in a perspective plane and provides methods for calculating
    the dual, perpendicular line, and midpoint of the point.

    .. svgbob::
       :align: center

          / \\
         /   \\
        /-----\\
        \\-----/
         \\   /
          \\ /
    """

    def dual_type(self) -> type:
        return PerspLine

    def perp(self) -> "PerspLine":
        """Polar line

        The function returns the polar line.
        :return: The code is returning the value "L_INF".
        """
        return L_INF

    def midpoint(self, other: "PerspPoint") -> "PerspPoint":
        """
        The `midpoint` function calculates the midpoint between two PerspPoint objects.

        :param other: The `other` parameter is an instance of the same class as `self`. It represents another point that you want to find the midpoint with
        :type other: "PerspPoint"
        :return: The `midpoint` method returns an instance of the `PerspPoint` class.

        Examples:
            >>> from projgeom.persp_object import PerspPoint
            >>> p1 = PerspPoint([1, 2, 3])
            >>> p2 = PerspPoint([4, 5, 6])
            >>> p1.midpoint(p2)
            PerspPoint(5 : 7 : 9)
        """
        alpha = L_INF.dot(other)
        beta = L_INF.dot(self)
        return self.parametrize(alpha, other, beta)


class PerspLine(PgObject[PerspPoint]):
    """A line in a perspective plane.

    The PerspLine class represents a line in a perspective plane and provides methods for calculating
    the dual and perpendicular point, as well as checking if two lines are parallel.

    .. svgbob::
       :align: center

          / \\
         /   \\
        /-----\\
        \\-----/
         \\   /
          \\ /
    """

    def dual_type(self) -> type:
        return PerspPoint

    def perp(self) -> PerspPoint:
        """Pole

        The `perp` function returns a `PerspPoint` object that is obtained by taking the dot product of
        `self` with `I_RE` and `I_IM`, and then using the results to create a new `PerspPoint` object
        using the `parametrize` method of `I_RE`.
        :return: a PerspPoint object.
        """
        alpha = I_RE.dot(self)
        beta = I_IM.dot(self)
        return I_RE.parametrize(alpha, I_IM, beta)

    def is_parallel(self, other: "PerspLine") -> bool:
        """
        The function checks if two lines are parallel by calculating the dot product of their direction
        vectors.

        :param other: The "other" parameter is an object of the same class as the current object. It represents another instance of the class that we want to check for parallelism with the current object
        :type other: "PerspPoint"
        :return: a boolean value, indicating whether the two objects are parallel or not.

        Examples:
            >>> from projgeom.persp_object import PerspLine
            >>> l1 = PerspLine([1, 2, 3])
            >>> l2 = PerspLine([1, 2, 4])
            >>> l1.is_parallel(l2)
            False
        """
        return L_INF.dot(self.meet(other)) == 0


I_RE = PerspPoint([0, 1, 1])
I_IM = PerspPoint([1, 0, 0])
L_INF = PerspLine([0, -1, 1])
