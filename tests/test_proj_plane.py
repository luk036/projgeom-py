from hypothesis import given
from hypothesis.strategies import integers

from projgeom_py.pg_plane import ProjectivePlane, coincident, harm_conj
from projgeom_py.pg_point import PgLine, PgPoint


def check_pg_plane(p: ProjectivePlane, q: ProjectivePlane):
    m = p.meet(q)
    assert m == q.meet(p)
    assert m.incident(p)
    assert m.incident(q)
    pq = p.plucker(2, q, 3)
    assert coincident(p, q, pq)
    h = harm_conj(p, q, pq)
    assert harm_conj(p, q, h) == pq


@given(integers(), integers())
def test_pg_point(pz, qz):
    p = PgPoint([1, 3, pz])
    q = PgPoint([-2, 1, qz])
    check_pg_plane(p, q)


@given(integers(), integers())
def test_pg_line(pz, qz):
    p = PgLine([1, 3, pz])
    q = PgLine([-2, 1, qz])
    check_pg_plane(p, q)
