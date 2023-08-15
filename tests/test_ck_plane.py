from hypothesis import given
from hypothesis.strategies import integers

from projgeom_py.ck_plane import CayleyKleinPlane, is_perpendicular, orthocenter, tri_altitude
from projgeom_py.ell_point import EllLine, EllPoint
from projgeom_py.hyp_point import HypLine, HypPoint
from projgeom_py.myck_point import MyCKLine, MyCKPoint
from projgeom_py.persp_point import PerspPoint

# from projgeom_py.pg_plane import coincident, harm_conj
from projgeom_py.pg_plane import tri_dual


def check_ck_plane(a1: CayleyKleinPlane, a2: CayleyKleinPlane, a3: CayleyKleinPlane):
    triangle = [a1, a2, a3]
    trilateral = tri_dual(triangle)
    l1 = trilateral[0]
    assert l1.incident(triangle[1])

    t1, t2, t3 = tri_altitude(triangle)
    assert is_perpendicular(t1, l1)
    o = orthocenter(triangle)
    assert o == t2.meet(t3)


@given(integers(), integers(), integers())
def test_ell_point(a1z, a2z, a3y):
    a1 = EllPoint([13, 23, a1z])
    a2 = EllPoint([44, -3, a2z])
    a3 = EllPoint([-2, a3y, 12])
    check_ck_plane(a1, a2, a3)


@given(integers(), integers(), integers())
def test_ell_line(a1z, a2z, a3y):
    a1 = EllLine([13, 23, a1z])
    a2 = EllLine([44, -3, a2z])
    a3 = EllLine([-2, a3y, 12])
    check_ck_plane(a1, a2, a3)


@given(integers(), integers(), integers())
def test_hyp_point(a1z, a2z, a3y):
    a1 = HypPoint([13, 23, a1z])
    a2 = HypPoint([44, -3, a2z])
    a3 = HypPoint([-2, a3y, 12])
    check_ck_plane(a1, a2, a3)


@given(integers(), integers(), integers())
def test_hyp_line(a1z, a2z, a3y):
    a1 = HypLine([13, 23, a1z])
    a2 = HypLine([44, -3, a2z])
    a3 = HypLine([-2, a3y, 12])
    check_ck_plane(a1, a2, a3)


@given(integers(), integers(), integers())
def test_myck_point(a1z, a2z, a3y):
    a1 = MyCKPoint([13, 23, a1z])
    a2 = MyCKPoint([44, -3, a2z])
    a3 = MyCKPoint([-2, a3y, 12])
    check_ck_plane(a1, a2, a3)


@given(integers(), integers(), integers())
def test_myck_line(a1z, a2z, a3y):
    a1 = MyCKLine([13, 23, a1z])
    a2 = MyCKLine([44, -3, a2z])
    a3 = MyCKLine([-2, a3y, 12])
    check_ck_plane(a1, a2, a3)


@given(integers(), integers(), integers())
def test_persp_point(a1z, a2z, a3y):
    a1 = PerspPoint([13, 23, a1z])
    a2 = PerspPoint([44, -3, a2z])
    a3 = PerspPoint([-2, a3y, 12])
    check_ck_plane(a1, a2, a3)
