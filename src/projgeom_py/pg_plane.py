from abc import abstractmethod
from typing import Generic, List, Sequence, TypeVar

from typing_extensions import Self

Dual = TypeVar("Dual", bound="ProjectivePlane")
Value = TypeVar("Value", bound=int)


class ProjectivePlane(Generic[Dual, Value]):
    @abstractmethod
    def dual(self) -> type:
        pass

    @abstractmethod
    def __eq__(self, rhs) -> bool:
        pass

    @abstractmethod
    def meet(self, rhs: Self) -> Dual:
        pass

    @abstractmethod
    def aux(self) -> Dual:
        pass

    @abstractmethod
    def dot(self, line: Dual) -> Value:
        pass

    @abstractmethod
    def plucker(self, lambda_: Value, q: Self, mu_: Value) -> Self:
        pass

    @abstractmethod
    def incident(self, line: Dual) -> bool:
        return self.dot(line) == 0

    def coincident(self, q: Self, r: Self) -> bool:
        """
        The `coincident` function checks if three points `p`, `q`, and `r` are collinear.

        :param q: q is an instance of the class ProjectivePlanePrimitive<Point>
        :type q: Self
        :param r: The parameter `r` is of type `ProjectivePlanePrimitive<Point>`
        :type r: Self
        :return: A boolean value is being returned.
        """
        return self.meet(q).incident(r)

    def harm_conj(self, a: Self, b: Self) -> Self:
        """
        The `harm_conj` function calculates the harmonic conjugate of two points on a projective plane.

        :param a: The parameter `a` is of type `ProjectivePlane`
        :type a: Self
        :param b: The parameter `b` is of type `ProjectivePlane`
        :type b: Self
        :return: a ProjectivePlane object.
        """
        assert self.coincident(a, b)
        ab = a.meet(b)
        lc = ab.aux().meet(self)
        return a.plucker(lc.dot(b), b, lc.dot(a))


Point = ProjectivePlane["Line", Value]
Line = ProjectivePlane["Point", Value]

# ProjectivePlanePrimitive = PgObject

# trait ProjectivePlanePrimitive<Line>: Eq {
#     def meet(self, rhs: Self) -> Line
#     def incident(self, line) -> bool
# }


def check_axiom(p: Point, q: Point, line: Line):
    """
    The function `check_axiom` checks various axioms related to a projective plane.

    :param p: p is a ProjectivePlanePrimitive object, which represents a point in a projective plane
    :type p: Point
    :param q: The parameter `q` is a ProjectivePlanePrimitive object, which represents a point or a line in a projective plane
    :type q: Point
    :param line: The `line` parameter represents a projective plane line
    :type line: Line
    """
    assert p == p
    assert (p == q) == (q == p)
    assert p.incident(line) == line.incident(p)
    assert p.meet(q) == q.meet(p)
    m = p.meet(q)
    assert m.incident(p) and m.incident(q)


def coincident(p: Point, q: Point, r: Point) -> bool:
    """
    The `coincident` function checks if three points `p`, `q`, and `r` are collinear in a projective
    plane.

    :param p: p is an object of type ProjectivePlanePrimitive<Point>. It represents a point in a projective plane
    :type p: Point
    :param q: q is a ProjectivePlanePrimitive object, which represents a point in a projective plane
    :type q: Point
    :param r: The parameter `r` represents a point in a projective plane
    :type r: Point
    :return: The function `coincident` returns a boolean value.

    Examples:
        >>> from projgeom_py.pg_point import PgLine, PgPoint
        >>> coincident(PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0]))
        False
    """
    return p.meet(q).incident(r)


def check_pappus(co1: List[Point], co2: List[Point]) -> bool:
    """
    The function `check_pappus` checks if three lines in a projective plane satisfy Pappus' theorem.

    :param co1: The parameter `co1` is a list of `ProjectivePlanePrimitive` objects
    :type co1: List[Point]
    :param co2: The parameter `co2` is a list of `ProjectivePlanePrimitive` objects
    :type co2: List[Point]
    :return: a boolean value.

    Examples:
        >>> from projgeom_py.pg_point import PgLine, PgPoint
        >>> co1 = [PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0])]
        >>> co2 = [PgPoint([0, 0, 1]), PgPoint([0, 1, 0]), PgPoint([1, 0, 0])]
        >>> check_pappus(co1, co2)
        True
    """
    [a, b, c] = co1
    [d, e, f] = co2
    g = (a.meet(e)).meet(b.meet(d))
    h = (a.meet(f)).meet(c.meet(d))
    i = (b.meet(f)).meet(c.meet(e))
    return coincident(g, h, i)


def tri_dual(tri: Sequence) -> List:
    """
    The function `tri_dual` takes a list of three `ProjectivePlanePrimitive` objects representing a triangle and
    returns a list of three `ProjectivePlanePrimitive` objects representing the circumcircles of the triangle's
    three edges.

    :param tri: The `tri` parameter is expected to be a sequence (e.g., list, tuple) of three elements. Each element should be an object of type `ProjectivePlanePrimitive`
    :type tri: Sequence
    :return: The function `tri_dual` returns a list of three `ProjectivePlanePrimitive` objects.
    """
    [a1, a2, a3] = tri
    assert not coincident(a1, a2, a3)
    return [a2.meet(a3), a1.meet(a3), a1.meet(a2)]


def persp(tri1: List[Point], tri2: List[Point]) -> bool:
    """
    The `persp` function checks whether two triangles are perspective.

    :param tri1: tri1 is a list of three ProjectivePlanePrimitive objects representing the vertices of the first triangle
    :type tri1: List[Point]
    :param tri2: tri2 is a list of three ProjectivePlanePrimitive objects representing the vertices of the second triangle
    :type tri2: List[Point]
    :return: a boolean value.

    Examples:
        >>> from projgeom_py.pg_point import PgLine, PgPoint
        >>> tri1 = [PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0])]
        >>> tri2 = [PgPoint([0, 0, 1]), PgPoint([0, 1, 0]), PgPoint([1, 0, 0])]
        >>> persp(tri1, tri2)
        True
    """
    [a, b, c] = tri1
    [d, e, f] = tri2
    o = a.meet(d).meet(b.meet(e))
    return c.meet(f).incident(o)


def check_desargue(tri1: List[Point], tri2: List[Point]) -> bool:
    """
    The function `check_desargue` checks if two triangles in a projective plane satisfy the Desargue's
    theorem.

    :param tri1: tri1 is a list of ProjectivePlanePrimitive objects representing the first triangle in the Desargue's theorem
    :type tri1: List[Point]
    :param tri2: The `tri2` parameter is a list of `ProjectivePlanePrimitive` objects representing the second triangle
    :type tri2: List[Point]
    :return: a boolean value.

    Examples:
        >>> from projgeom_py.pg_point import PgLine, PgPoint
        >>> tri1 = [PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0])]
        >>> tri2 = [PgPoint([0, 0, 1]), PgPoint([0, 1, 0]), PgPoint([1, 0, 0])]
        >>> check_desargue(tri1, tri2)
        True
    """
    trid1 = tri_dual(tri1)
    trid2 = tri_dual(tri2)
    b1 = persp(tri1, tri2)
    b2 = persp(trid1, trid2)
    return (b1 and b2) or (not b1 and not b2)


# trait ProjectivePlane<Line, Value: Default + Eq>: ProjectivePlanePrimitive<Line>:
#     def aux(self) -> Line
#     def dot(self, line) -> Value; # basic measurement
#     def plucker(lambda_: Value, p: Self, mu_: Value, q: Self)
#     def incident(self, line) -> bool:
#         self.dot(line) == Value::default()


def harm_conj(a: Point, b: Point, c: Point):
    """
    The `harm_conj` function calculates the harmonic conjugate of three points on a projective plane.

    :param a: a is an object of type ProjectivePlane
    :type a: Point
    :param b: The parameter `b` represents a point on the projective plane
    :type b: Point
    :param c: The parameters `a`, `b`, and `c` are of type `ProjectivePlane`
    :type c: Point
    :return: The function `harm_conj` returns a `ProjectivePlane` object.
    """
    assert coincident(a, b, c)
    ab = a.meet(b)
    lc = ab.aux().meet(c)
    # Point = type(a)
    return a.plucker(lc.dot(b), b, lc.dot(a))


def involution(origin: Point, mirror: Point, p: Point):
    """
    The function `involution` performs an involution transformation on a point `p` with respect to an
    origin point `origin` and a mirror line `mirror`.

    :param origin: The `origin` parameter represents a point in a projective plane
    :type origin: Point
    :param mirror: The `mirror` parameter represents a mirror line or mirror plane in a projective plane. It is used to perform a reflection or mirror transformation on a point `p` with respect to the mirror line or plane
    :type mirror: Point
    :param p: The parameter `p` represents a point in a projective plane
    :type p: Point
    :return: a ProjectivePlane<Point> object.
    """
    po = p.meet(origin)
    b = po.meet(mirror)
    return harm_conj(origin, b, p)
