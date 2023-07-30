from .pg_object import PgObject


class PgPoint(PgObject["PgLine"]):
    """Projective Geometry Point

    The `PgPoint` class represents a point in projective geometry and has a method `dual()` that returns
    the dual line of the point.

    Examples:
        >>> from projgeom_py.pg_point import PgPoint, PgLine
        >>> p = PgPoint([1, 2, 3])
        >>> l = p.aux()
        >>> assert isinstance(l, PgLine)
        >>> assert not p.incident(l)
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
        >>> from projgeom_py.pg_point import PgPoint, PgLine
        >>> l = PgLine([1, 2, 3])
        >>> p = l.aux()
        >>> assert isinstance(p, PgPoint)
        >>> assert not l.incident(p)
    """

    def dual(self) -> type:
        return PgPoint
