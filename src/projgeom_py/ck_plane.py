from .pg_plane import involution, tri_dual
from .pg_plane import ProjPlane, V

from typing import List
from typing import TypeVar
from abc import abstractmethod

# CKPlanePrim = Union[HypLine, HypPoint]

# trait CKPlanePrim<L>: ProjPlanePrim<L>:
#     def perp(self) -> L

Dual = TypeVar("Dual", bound="CKPlane")


class CKPlane(ProjPlane[Dual, V]):
    @abstractmethod
    def perp(self) -> Dual:
        pass


Pck = CKPlane["Lck", V]
Lck = CKPlane["Pck", V]


def is_perpendicular(m1: Lck, m2: Lck) -> bool:
    return m1.perp().incident(m2)


def altitude(p: Pck, m: Lck) -> Pck:
    """_summary_

    Args:
        p (CKPlanePrim<P>): _description_
        m (CKPlanePrim<L>): _description_

    Returns:
        CKPlanePrim<L>: _description_
    """
    return m.perp().circ(p)


def orthocenter(tri: List[Pck]):
    """_summary_

    Args:
        tri (List[CKPlanePrim<P>]): _description_

    Returns:
        CKPlanePrim<P>: _description_
    """
    [a1, a2, a3] = tri
    t1 = altitude(a1, a2.circ(a3))
    t2 = altitude(a2, a3.circ(a1))
    return t1.circ(t2)


def tri_altitude(tri):
    """_summary_

    Args:
        tri (list): _description_

    Returns:
        list: _description_
    """
    [l1, l2, l3] = tri_dual(tri)
    [a1, a2, a3] = tri
    t1 = altitude(a1, l1)
    t2 = altitude(a2, l2)
    t3 = altitude(a3, l3)
    return [t1, t2, t3]


# trait CKPlane<L, V: Default + Eq>: ProjPlane<L, V> + CKPlanePrim<L> {}


def reflect(mirror: CKPlane, p: CKPlane):
    """_summary_

    Args:
        mirror (CKPlane<L>): _description_
        p (CKPlane<P>): _description_
    """
    involution(mirror.perp(), mirror, p)
