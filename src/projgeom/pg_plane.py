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
    def parametrize(self, lambda_: Value, pt_q: Self, mu_: Value) -> Self:
        pass

    @abstractmethod
    def incident(self, line: Dual) -> bool:
        return self.dot(line) == 0

    def coincident(self, pt_q: Self, pt_r: Self) -> bool:
        r"""
        The `coincident` function checks if three points `pt_p`, `pt_q`, and `pt_r` are collinear.

        :param pt_q: pt_q is an instance of the class ProjectivePlanePrimitive<Point>
        :type pt_q: Self
        :param pt_r: The parameter `pt_r` is of type `ProjectivePlanePrimitive<Point>`
        :type pt_r: Self
        :return: A boolean value is being returned.

        .. svgbob::
           :align: center

                 |  /
               \ | /       coincidence
                \|/
                 o      -----o------o---o---
                /|\           A      B   C
               / | \
              l  |  \
                 m   n
        """
        return self.meet(pt_q).incident(pt_r)

    def harm_conj(self, pt_a: Self, pt_b: Self) -> Self:
        """
        The `harm_conj` function calculates the harmonic conjugate of two points on a projective plane.

        :param pt_a: The parameter `pt_a` is of type `ProjectivePlane`
        :type pt_a: Self
        :param pt_b: The parameter `pt_b` is of type `ProjectivePlane`
        :type pt_b: Self
        :return: a ProjectivePlane object.
        """
        assert self.coincident(pt_a, pt_b)
        ab = pt_a.meet(pt_b)
        lc = ab.aux().meet(self)
        return pt_a.parametrize(lc.dot(pt_b), pt_b, lc.dot(pt_a))


Point = ProjectivePlane["Line", Value]
Line = ProjectivePlane["Point", Value]

# ProjectivePlanePrimitive = PgObject

# trait ProjectivePlanePrimitive<Line>: Eq {
#     def meet(self, rhs: Self) -> Line
#     def incident(self, line) -> bool
# }


def check_axiom(pt_p: Point, pt_q: Point, ln_l: Line):
    """
    The function `check_axiom` checks various axioms related to a projective plane.

    :param pt_p: pt_p is a ProjectivePlanePrimitive object, which represents a point in a projective plane
    :type pt_p: Point
    :param pt_q: The parameter `pt_q` is a ProjectivePlanePrimitive object, which represents a point or a line in a projective plane
    :type pt_q: Point
    :param line: The `line` parameter represents a projective plane line
    :type line: Line
    """
    assert pt_p == pt_p
    assert (pt_p == pt_q) == (pt_q == pt_p)
    assert pt_p.incident(ln_l) == ln_l.incident(pt_p)
    assert pt_p.meet(pt_q) == pt_q.meet(pt_p)
    ln_l = pt_p.meet(pt_q)
    assert ln_l.incident(pt_p) and ln_l.incident(pt_q)


def coincident(pt_p: Point, pt_q: Point, pt_r: Point) -> bool:
    """
    The `coincident` function checks if three points `pt_p`, `pt_q`, and `pt_r` are collinear in a projective
    plane.

    :param pt_p: pt_p is an object of type ProjectivePlanePrimitive<Point>. It represents a point in a projective plane
    :type pt_p: Point
    :param pt_q: pt_q is a ProjectivePlanePrimitive object, which represents a point in a projective plane
    :type pt_q: Point
    :param pt_r: The parameter `pt_r` represents a point in a projective plane
    :type pt_r: Point
    :return: The function `coincident` returns a boolean value.

    Examples:
        >>> from projgeom.pg_object import PgLine, PgPoint
        >>> coincident(PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0]))
        False
    """
    return pt_p.meet(pt_q).incident(pt_r)


def check_pappus(coline1: List[Point], coline2: List[Point]) -> bool:
    """
    The function `check_pappus` checks if three lines in a projective plane satisfy Pappus' theorem.

    :param coline1: The parameter `coline1` is a list of `ProjectivePlanePrimitive` objects
    :type coline1: List[Point]
    :param coline2: The parameter `coline2` is a list of `ProjectivePlanePrimitive` objects
    :type coline2: List[Point]
    :return: a boolean value.

    Examples:
        >>> from projgeom.pg_object import PgLine, PgPoint
        >>> coline1 = [PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0])]
        >>> coline2 = [PgPoint([0, 0, 1]), PgPoint([0, 1, 0]), PgPoint([1, 0, 0])]
        >>> check_pappus(coline1, coline2)
        True
    """
    [pt_a, pt_b, pt_c] = coline1
    [pt_d, pt_e, pt_f] = coline2
    pt_g = (pt_a.meet(pt_e)).meet(pt_b.meet(pt_d))
    pt_h = (pt_a.meet(pt_f)).meet(pt_c.meet(pt_d))
    pt_i = (pt_b.meet(pt_f)).meet(pt_c.meet(pt_e))
    return coincident(pt_g, pt_h, pt_i)


def tri_dual(triangle: Sequence) -> List:
    r"""
    The function `tri_dual` takes a list of three `ProjectivePlanePrimitive` objects representing a triangle and
    returns a list of three `ProjectivePlanePrimitive` objects representing the circumcircles of the triangle's
    three edges.

    :param triangle: The `triangle` parameter is expected to be a sequence (pt_e.pt_g., list, tuple) of three elements. Each element should be an object of type `ProjectivePlanePrimitive`
    :type triangle: Sequence
    :return: The function `tri_dual` returns a list of three `ProjectivePlanePrimitive` objects.

    .. svgbob::
       :align: center

                          a
               \         /
                \ A     /
         c ------o-----o--------
                  \   / B
                   \ /
                  C o    triangle,
                   / \     trilateral
                  /   \
                       b
    """
    [a_1, a_2, a_3] = triangle
    assert not coincident(a_1, a_2, a_3)
    return [a_2.meet(a_3), a_1.meet(a_3), a_1.meet(a_2)]


def persp(tri_1: List[Point], tri_2: List[Point]) -> bool:
    """
    The `persp` function checks whether two triangles are perspective.

    :param tri_1: tri_1 is a list of three ProjectivePlanePrimitive objects representing the vertices of the first triangle
    :type tri_1: List[Point]
    :param tri_2: tri_2 is a list of three ProjectivePlanePrimitive objects representing the vertices of the second triangle
    :type tri_2: List[Point]
    :return: a boolean value.

    Examples:
        >>> from projgeom.pg_object import PgLine, PgPoint
        >>> tri_1 = [PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0])]
        >>> tri_2 = [PgPoint([0, 0, 1]), PgPoint([0, 1, 0]), PgPoint([1, 0, 0])]
        >>> persp(tri_1, tri_2)
        True
    """
    [pt_a, pt_b, pt_c] = tri_1
    [pt_d, pt_e, pt_f] = tri_2
    pt_o = pt_a.meet(pt_d).meet(pt_b.meet(pt_e))
    return pt_c.meet(pt_f).incident(pt_o)


def check_desargue(tri_1: List[Point], tri_2: List[Point]) -> bool:
    """
    The function `check_desargue` checks if two triangles in a projective plane satisfy the Desargue's
    theorem.

    :param tri_1: tri_1 is a list of ProjectivePlanePrimitive objects representing the first triangle in the Desargue's theorem
    :type tri_1: List[Point]
    :param tri_2: The `tri_2` parameter is a list of `ProjectivePlanePrimitive` objects representing the second triangle
    :type tri_2: List[Point]
    :return: a boolean value.

    Examples:
        >>> from projgeom.pg_object import PgLine, PgPoint
        >>> tri_1 = [PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0])]
        >>> tri_2 = [PgPoint([0, 0, 1]), PgPoint([0, 1, 0]), PgPoint([1, 0, 0])]
        >>> check_desargue(tri_1, tri_2)
        True
    """
    trid_1 = tri_dual(tri_1)
    trid_2 = tri_dual(tri_2)
    bool_1 = persp(tri_1, tri_2)
    bool_2 = persp(trid_1, trid_2)
    return (bool_1 and bool_2) or (not bool_1 and not bool_2)


# trait ProjectivePlane<Line, Value: Default + Eq>: ProjectivePlanePrimitive<Line>:
#     def aux(self) -> Line
#     def dot(self, line) -> Value; # basic measurement
#     def parametrize(lambda_: Value, pt_p: Self, mu_: Value, pt_q: Self)
#     def incident(self, line) -> bool:
#         self.dot(line) == Value::default()


def harm_conj(pt_a: Point, pt_b: Point, pt_c: Point):
    """
    The `harm_conj` function calculates the harmonic conjugate of three points on a projective plane.

    :param pt_a: a is an object of type ProjectivePlane
    :type pt_a: Point
    :param pt_b: The parameter `pt_b` represents a point on the projective plane
    :type pt_b: Point
    :param pt_c: The parameters `pt_a`, `pt_b`, and `pt_c` are of type `ProjectivePlane`
    :type pt_c: Point
    :return: The function `harm_conj` returns a `ProjectivePlane` object.
    """
    assert coincident(pt_a, pt_b, pt_c)
    ab = pt_a.meet(pt_b)
    lc = ab.aux().meet(pt_c)
    # Point = type(pt_a)
    return pt_a.parametrize(lc.dot(pt_b), pt_b, lc.dot(pt_a))


def involution(origin: Point, mirror: Point, pt_p: Point):
    """
    The function `involution` performs an involution transformation on a point `pt_p` with respect to an
    origin point `origin` and a mirror line `mirror`.

    :param origin: The `origin` parameter represents a point in a projective plane
    :type origin: Point
    :param mirror: The `mirror` parameter represents a mirror line or mirror plane in a projective plane. It is used to perform a reflection or mirror transformation on a point `pt_p` with respect to the mirror line or plane
    :type mirror: Point
    :param pt_p: The parameter `pt_p` represents a point in a projective plane
    :type pt_p: Point
    :return: a ProjectivePlane<Point> object.
    """
    ln_x = pt_p.meet(origin)
    pt_b = ln_x.meet(mirror)
    return harm_conj(origin, pt_b, pt_p)
