"""
MyCKPoint and MyCKLine Classes

This code defines two classes, MyCKPoint and MyCKLine, which are used to
represent points and lines in Cayley-Klein geometry, a type of projective
geometry. These classes are designed to work together and provide methods for
geometric operations.

The purpose of this code is to create a framework for working with points and
    lines in Cayley-Klein geometry. It allows users to create point and line
    objects and perform operations on them, such as finding the perpendicular (or
    polar) line to a point, or the pole of a line.

Both classes inherit from a PgObject class, which likely provides some common
functionality for projective geometry objects. The classes don't explicitly
take any inputs when created, but they are designed to work with coordinate
data, which is assumed to be stored in a 'coord' attribute.

The perp() method in each class produces a new object of the opposite type - a
    MyCKLine for a point, or a MyCKPoint for a line.

The code achieves its purpose by implementing two key methods for each class:

1.  dual(): This method returns the type of the dual object. For a point, the
    dual is a line, and vice versa.

2.  perp(): This method calculates the perpendicular (or polar) object. For a
    point, it calculates the polar line, and for a line, it calculates the pole
    point.

The perp() methods contain the core logic of the classes. They perform
    coordinate transformations to convert between points and lines. For
    MyCKPoint, the perpendicular line is calculated by doubling the first and
    third coordinates and negating the first and third. For MyCKLine, the pole
    point is calculated by doubling the second coordinate and negating the first
    and third.

These transformations represent important geometric relationships in
    Cayley-Klein geometry. They allow users to easily switch between dual
    representations of geometric objects, which is a fundamental concept in
    projective geometry.

Overall, this code provides a simple but powerful tool for working with
Cayley-Klein geometry, allowing users to create and manipulate geometric
objects with ease.
"""

from .pg_object import PgObject


class MyCKPoint(PgObject["MyCKLine"]):
    """
    A customized point class for Cayley-Klein geometry.

    .. svgbob::
       :align: center

          / \
         / _ \
        | / \ |
        | \_/ |
         \ _ /
          \ /
    """

    def dual_type(self) -> type:
        return MyCKLine

    def perp(self):
        """
        The perp function returns an instance of the MyCKLine class that represents a polar line.
        :return: an instance of the MyCKLine class.

        Examples:
            >>> from projgeom.myck_object import MyCKPoint, MyCKLine
            >>> p = MyCKPoint([1, 2, 3])
            >>> p.perp()
            MyCKLine(-2 : 2 : -6)
        """
        coord = self.coord
        return MyCKLine([-2 * coord[0], coord[1], -2 * coord[2]])


class MyCKLine(PgObject[MyCKPoint]):
    """
    A customized line class for Cayley-Klein geometry.

    .. svgbob::
       :align: center

          / \
         / _ \
        | / \ |
        | \_/ |
         \ _ /
          \ /
    """

    def dual_type(self) -> type:
        return MyCKPoint

    def perp(self) -> MyCKPoint:
        """Pole of the line.
        :return: The `perp` method returns a `MyCKPoint` object.

        Examples:
            >>> from projgeom.myck_object import MyCKPoint, MyCKLine
            >>> l = MyCKLine([1, 2, 3])
            >>> l.perp()
            MyCKPoint(-1 : 4 : -3)
        """
        coord = self.coord
        return MyCKPoint([-coord[0], 2 * coord[1], -coord[2]])
