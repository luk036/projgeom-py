from projgeom_py.pg_point import PgPoint, PgLine
from projgeom_py.pg_plane import ProjPlane, coincident, harm_conj
import pytest


def check_pg_plane(p: ProjPlane, q: ProjPlane):
    m = p.circ(q)
    assert m == q.circ(p)
    assert m.incident(p)
    assert m.incident(q)
    P = type(p)
    pq = P.plucker(2, p, 3, q)
    assert coincident(p, q, pq)
    h = harm_conj(p, q, pq)
    assert harm_conj(p, q, h) == pq


@pytest.mark.randomize(pz=int, qz=int, ncalls=5)
def test_pg_point(pz, qz):
    p = PgPoint([1, 3, pz])
    q = PgPoint([-2, 1, qz])
    check_pg_plane(p, q)


@pytest.mark.randomize(pz=int, qz=int, ncalls=5)
def test_pg_line(pz, qz):
    p = PgLine([1, 3, pz])
    q = PgLine([-2, 1, qz])
    check_pg_plane(p, q)
