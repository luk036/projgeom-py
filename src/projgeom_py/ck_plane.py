from .pg_plane import involution, tri_dual
from .pg_object import PgObject
from typing import List

CKPlanePrim = PgObject

# trait CKPlanePrim<L>: ProjPlanePrim<L>:
#     def perp(self) -> L


def is_perpendicular(m1: CKPlanePrim, m2: CKPlanePrim) -> bool:
    """_summary_

    Args:
        m1 (CKPlanePrim): _description_
        m2 (CKPlanePrim): _description_

    Returns:
        bool: _description_
    """
    return m1.perp().incident(m2)


def altitude(p: CKPlanePrim, m: CKPlanePrim):
    """_summary_

    Args:
        p (CKPlanePrim<P>): _description_
        m (CKPlanePrim<L>): _description_

    Returns:
        CKPlanePrim<L>: _description_
    """
    return m.perp().circ(p)


def orthcenter(tri: List[CKPlanePrim]):
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


def tri_altitude(tri: List[CKPlanePrim]) -> List[CKPlanePrim]:
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

CKPlane = PgObject


def reflect(mirror: CKPlane, p: CKPlane):
    """_summary_

    Args:
        mirror (CKPlane<L>): _description_
        p (CKPlane<P>): _description_
    """
    involution(mirror.perp(), mirror, p)
