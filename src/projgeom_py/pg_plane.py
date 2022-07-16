from typing import List

from .pg_object import PgObject

ProjPlanePrim = PgObject

# trait ProjPlanePrim<L>: Eq {
#     def circ(self, rhs: Self) -> L
#     def incident(self, line) -> bool
# }


def check_axiom(p: ProjPlanePrim, q: ProjPlanePrim, line: ProjPlanePrim):
    """_summary_

    Args:
        p (ProjPlanePrim<L>): _description_
        q (ProjPlanePrim<L>): _description_
        line (ProjPlanePrim<P>): _description_
    """
    assert p == p
    assert (p == q) == (q == p)
    assert p.incident(line) == line.incident(p)
    assert p.circ(q) == q.circ(p)
    m = p.circ(q)
    assert m.incident(p) and m.incident(q)


def coincident(p: ProjPlanePrim, q: ProjPlanePrim, r: ProjPlanePrim) -> bool:
    """_summary_

    Args:
        p (ProjPlanePrim<P>): _description_
        q (ProjPlanePrim<P>): _description_
        r (ProjPlanePrim<P>): _description_

    Returns:
        bool: _description_
    """
    return p.circ(q).incident(r)


def check_pappus(co1: List[ProjPlanePrim], co2: List[ProjPlanePrim]) -> bool:
    """Check Pappus Theorem

    Args:
        co1 (List[ProjPlanePrim]): _description_
        co2 (List[ProjPlanePrim]): _description_

    Returns:
        bool: _description_
    """
    [a, b, c] = co1
    [d, e, f] = co2
    g = (a.circ(e)).circ(b.circ(d))
    h = (a.circ(f)).circ(c.circ(d))
    i = (b.circ(f)).circ(c.circ(e))
    return coincident(g, h, i)


def tri_dual(tri: List[ProjPlanePrim]):
    """_summary_

    Args:
        tri (List[ProjPlanePrim]): _description_

    Returns:
        List[ProjPlanePrim]: _description_
    """
    [a1, a2, a3] = tri
    assert not coincident(a1, a2, a3)
    return [a2.circ(a3), a1.circ(a3), a1.circ(a2)]


def persp(tri1: List[ProjPlanePrim], tri2: List[ProjPlanePrim]) -> bool:
    """Check whether two triangles are perspective

    Args:
        tri1 (List[ProjPlanePrim]): _description_
        tri2 (List[ProjPlanePrim]): _description_

    Returns:
        bool: _description_
    """
    [a, b, c] = tri1
    [d, e, f] = tri2
    o = a.circ(d).circ(b.circ(e))
    return c.circ(f).incident(o)


def check_desargue(tri1: List[ProjPlanePrim], tri2: List[ProjPlanePrim]) -> bool:
    """_summary_

    Args:
        tri1 (List[ProjPlanePrim]): _description_
        tri2 (List[ProjPlanePrim]): _description_

    Returns:
        bool: _description_
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

ProjPlane = PgObject


def harm_conj(a: ProjPlane, b: ProjPlane, c: ProjPlane):
    """harmonic conjugate

    Args:
        a (ProjPlane): _description_
        b (ProjPlane): _description_
        c (ProjPlane): _description_

    Returns:
        ProjPlane: _description_
    """
    assert coincident(a, b, c)
    ab = a.circ(b)
    lc = ab.aux().circ(c)
    P = type(a)
    return P.plucker(lc.dot(b), a, lc.dot(a), b)


def involution(origin: ProjPlane, mirror: ProjPlane, p: ProjPlane) -> ProjPlane:
    """_summary_

    Args:
        origin (ProjPlane<P>): _description_
        mirror (ProjPlane<L>): _description_
        p (ProjPlane<P>): _description_

    Returns:
        ProjPlane<P>: _description_
    """
    po = p.circ(origin)
    b = po.circ(mirror)
    return harm_conj(origin, b, p)
