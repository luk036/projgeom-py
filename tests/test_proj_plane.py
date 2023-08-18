from hypothesis import given
from hypothesis.strategies import integers

from projgeom.pg_object import PgLine, PgPoint
from projgeom.pg_plane import ProjectivePlane, coincident, harm_conj


def check_pg_plane(pt_p: ProjectivePlane, pt_q: ProjectivePlane):
    ln_l = pt_p.meet(pt_q)
    assert ln_l == pt_q.meet(pt_p)
    assert ln_l.incident(pt_p)
    assert ln_l.incident(pt_q)
    pq = pt_p.parametrize(2000000000000, pt_q, 311111111111)
    assert coincident(pt_p, pt_q, pq)
    pt_h = harm_conj(pt_p, pt_q, pq)
    assert harm_conj(pt_p, pt_q, pt_h) == pq


@given(integers(), integers())
def test_pg_point(pz, qz):
    pt_p = PgPoint([133333333333, 322222222222, pz])
    pt_q = PgPoint([-244444444444, 166666666666, qz])
    check_pg_plane(pt_p, pt_q)


@given(integers(), integers())
def test_pg_line(pz, qz):
    ln_l = PgLine([133333333333, 322222222222, pz])
    ln_m = PgLine([-244444444444, 166666666666, qz])
    check_pg_plane(ln_l, ln_m)
