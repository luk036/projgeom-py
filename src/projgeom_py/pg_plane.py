from typing import List, Sequence
from typing import Generic, TypeVar
from typing_extensions import Self
from abc import abstractmethod

Dual = TypeVar("Dual", bound="ProjPlane")
V = TypeVar("V", bound=int)


class ProjPlane(Generic[Dual, V]):
    @abstractmethod
    def dual(self) -> type:
        pass

    @abstractmethod
    def __eq__(self, rhs) -> bool:
        pass

    @abstractmethod
    def circ(self, rhs: Self) -> Dual:
        pass

    @abstractmethod
    def aux(self) -> Dual:
        pass

    @abstractmethod
    def dot(self, line: Dual) -> V:
        pass

    @abstractmethod
    def plucker(self, ld: V, q: Self, mu: V) -> Self:
        pass

    @abstractmethod
    def incident(self, line: Dual) -> bool:
        return self.dot(line) == 0

    def coincident(self, q: Self, r: Self) -> bool:
        """
        The `coincident` function checks if three points `p`, `q`, and `r` are collinear.

        :param q: q is an instance of the class ProjPlanePrim<P>
        :type q: Self
        :param r: The parameter `r` is of type `ProjPlanePrim<P>`
        :type r: Self
        :return: A boolean value is being returned.
        """
        return self.circ(q).incident(r)

    def harm_conj(self, a: Self, b: Self) -> Self:
        """
        The `harm_conj` function calculates the harmonic conjugate of two points on a projective plane.

        :param a: The parameter `a` is of type `ProjPlane`
        :type a: Self
        :param b: The parameter `b` is of type `ProjPlane`
        :type b: Self
        :return: a ProjPlane object.
        """
        assert self.coincident(a, b)
        ab = a.circ(b)
        lc = ab.aux().circ(self)
        return a.plucker(lc.dot(b), b, lc.dot(a))


P = ProjPlane["L", V]
L = ProjPlane["P", V]

# ProjPlanePrim = PgObject

# trait ProjPlanePrim<L>: Eq {
#     def circ(self, rhs: Self) -> L
#     def incident(self, line) -> bool
# }


def check_axiom(p: P, q: P, line: L):
    """
    The function `check_axiom` checks various axioms related to a projective plane.

    :param p: p is a ProjPlanePrim object, which represents a point in a projective plane
    :type p: P
    :param q: The parameter `q` is a ProjPlanePrim object, which represents a point or a line in a projective plane
    :type q: P
    :param line: The `line` parameter represents a projective plane line
    :type line: L
    """
    assert p == p
    assert (p == q) == (q == p)
    assert p.incident(line) == line.incident(p)
    assert p.circ(q) == q.circ(p)
    m = p.circ(q)
    assert m.incident(p) and m.incident(q)


def coincident(p: P, q: P, r: P) -> bool:
    """
    The `coincident` function checks if three points `p`, `q`, and `r` are collinear in a projective
    plane.

    :param p: p is an object of type ProjPlanePrim<P>. It represents a point in a projective plane
    :type p: P
    :param q: q is a ProjPlanePrim object, which represents a point in a projective plane
    :type q: P
    :param r: The parameter `r` represents a point in a projective plane
    :type r: P
    :return: The function `coincident` returns a boolean value.

    Examples:
        >>> from projgeom_py.pg_point import PgLine, PgPoint
        >>> coincident(PgPoint([0, 1, 0]), PgPoint([0, 0, 1]), PgPoint([1, 0, 0]))
        False
    """
    return p.circ(q).incident(r)


def check_pappus(co1: List[P], co2: List[P]) -> bool:
    """
    The function `check_pappus` checks if three lines in a projective plane satisfy Pappus' theorem.

    :param co1: The parameter `co1` is a list of `ProjPlanePrim` objects
    :type co1: List[P]
    :param co2: The parameter `co2` is a list of `ProjPlanePrim` objects
    :type co2: List[P]
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
    g = (a.circ(e)).circ(b.circ(d))
    h = (a.circ(f)).circ(c.circ(d))
    i = (b.circ(f)).circ(c.circ(e))
    return coincident(g, h, i)


def tri_dual(tri: Sequence) -> List:
    """
    The function `tri_dual` takes a list of three `ProjPlanePrim` objects representing a triangle and
    returns a list of three `ProjPlanePrim` objects representing the circumcircles of the triangle's
    three edges.

    :param tri: The `tri` parameter is expected to be a sequence (e.g., list, tuple) of three elements. Each element should be an object of type `ProjPlanePrim`
    :type tri: Sequence
    :return: The function `tri_dual` returns a list of three `ProjPlanePrim` objects.
    """
    [a1, a2, a3] = tri
    assert not coincident(a1, a2, a3)
    return [a2.circ(a3), a1.circ(a3), a1.circ(a2)]


def persp(tri1: List[P], tri2: List[P]) -> bool:
    """
    The `persp` function checks whether two triangles are perspective.

    :param tri1: tri1 is a list of three ProjPlanePrim objects representing the vertices of the first triangle
    :type tri1: List[P]
    :param tri2: tri2 is a list of three ProjPlanePrim objects representing the vertices of the second triangle
    :type tri2: List[P]
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
    o = a.circ(d).circ(b.circ(e))
    return c.circ(f).incident(o)


def check_desargue(tri1: List[P], tri2: List[P]) -> bool:
    """
    The function `check_desargue` checks if two triangles in a projective plane satisfy the Desargue's
    theorem.

    :param tri1: tri1 is a list of ProjPlanePrim objects representing the first triangle in the Desargue's theorem
    :type tri1: List[P]
    :param tri2: The `tri2` parameter is a list of `ProjPlanePrim` objects representing the second triangle
    :type tri2: List[P]
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


# trait ProjPlane<L, V: Default + Eq>: ProjPlanePrim<L>:
#     def aux(self) -> L
#     def dot(self, line) -> V; # basic measurement
#     def plucker(ld: V, p: Self, mu: V, q: Self)
#     def incident(self, line) -> bool:
#         self.dot(line) == V::default()


def harm_conj(a: P, b: P, c: P):
    """
    The `harm_conj` function calculates the harmonic conjugate of three points on a projective plane.

    :param a: a is an object of type ProjPlane
    :type a: P
    :param b: The parameter `b` represents a point on the projective plane
    :type b: P
    :param c: The parameters `a`, `b`, and `c` are of type `ProjPlane`
    :type c: P
    :return: The function `harm_conj` returns a `ProjPlane` object.
    """
    assert coincident(a, b, c)
    ab = a.circ(b)
    lc = ab.aux().circ(c)
    # P = type(a)
    return a.plucker(lc.dot(b), b, lc.dot(a))


def involution(origin: P, mirror: P, p: P):
    """
    The function `involution` performs an involution transformation on a point `p` with respect to an
    origin point `origin` and a mirror line `mirror`.

    :param origin: The `origin` parameter represents a point in a projective plane
    :type origin: P
    :param mirror: The `mirror` parameter represents a mirror line or mirror plane in a projective plane. It is used to perform a reflection or mirror transformation on a point `p` with respect to the mirror line or plane
    :type mirror: P
    :param p: The parameter `p` represents a point in a projective plane
    :type p: P
    :return: a ProjPlane<P> object.
    """
    po = p.circ(origin)
    b = po.circ(mirror)
    return harm_conj(origin, b, p)
