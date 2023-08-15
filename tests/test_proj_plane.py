from hypothesis import given
from hypothesis.strategies import integers

from projgeom_py.pg_plane import ProjectivePlane, coincident, harm_conj
from projgeom_py.pg_point import PgLine, PgPoint


def check_pg_plane(pt_p: ProjectivePlane, pt_q: ProjectivePlane):
    ln_l = pt_p.meet(pt_q)
    assert ln_l == pt_q.meet(pt_p)
    assert ln_l.incident(pt_p)
    assert ln_l.incident(pt_q)
    pq = pt_p.plucker(2, pt_q, 3)
    assert coincident(pt_p, pt_q, pq)
    pt_h = harm_conj(pt_p, pt_q, pq)
    assert harm_conj(pt_p, pt_q, pt_h) == pq


@given(integers(), integers())
def test_pg_point(pz, qz):
    pt_p = PgPoint([1, 3, pz])
    pt_q = PgPoint([-2, 1, qz])
    check_pg_plane(pt_p, pt_q)


@given(integers(), integers())
def test_pg_line(pz, qz):
    pt_p = PgLine([1, 3, pz])
    pt_q = PgLine([-2, 1, qz])
    check_pg_plane(pt_p, pt_q)
