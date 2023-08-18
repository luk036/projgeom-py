from hypothesis import given
from hypothesis.strategies import integers

from projgeom.ck_plane import (
    CayleyKleinPlane,
    is_perpendicular,
    orthocenter,
    tri_altitude,
)
from projgeom.ell_object import EllipticLine, EllipticPoint
from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint
from projgeom.myck_object import MyCKLine, MyCKPoint
from projgeom.persp_object import PerspPoint

# from projgeom.pg_plane import coincident, harm_conj
from projgeom.pg_plane import tri_dual


def check_ck_plane(a_1: CayleyKleinPlane, a_2: CayleyKleinPlane, a_3: CayleyKleinPlane):
    triangle = [a_1, a_2, a_3]
    trilateral = tri_dual(triangle)
    l_1 = trilateral[0]
    assert l_1.incident(triangle[1])

    t_1, t_2, t_3 = tri_altitude(triangle)
    assert is_perpendicular(t_1, l_1)
    pt_o = orthocenter(triangle)
    assert pt_o == t_2.meet(t_3)


@given(integers(), integers(), integers())
def test_ell_point(a1z, a2z, a3y):
    a_1 = EllipticPoint([13333333333, 2333333333, a1z])
    a_2 = EllipticPoint([44444444444, -333333333, a2z])
    a_3 = EllipticPoint([-2333333333, a3y, 1222222222])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_ell_line(a1z, a2z, a3y):
    a_1 = EllipticLine([1333333333, 2333333333, a1z])
    a_2 = EllipticLine([4444444444, -333333333, a2z])
    a_3 = EllipticLine([-233333333, a3y, 1222222222])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_hyp_point(a1z, a2z, a3y):
    a_1 = HyperbolicPoint([1333333333, 2333333333, a1z])
    a_2 = HyperbolicPoint([4444444444, -333333333, a2z])
    a_3 = HyperbolicPoint([-233333333, a3y, 1222222222])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_hyp_line(a1z, a2z, a3y):
    a_1 = HyperbolicLine([1333333333, 2333333333, a1z])
    a_2 = HyperbolicLine([4444444444, -333333333, a2z])
    a_3 = HyperbolicLine([-233333333, a3y, 1222222222])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_myck_point(a1z, a2z, a3y):
    a_1 = MyCKPoint([1333333333, 2333333333, a1z])
    a_2 = MyCKPoint([4444444444, -333333333, a2z])
    a_3 = MyCKPoint([-233333333, a3y, 1222222222])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_myck_line(a1z, a2z, a3y):
    a_1 = MyCKLine([1333333333, 2333333333, a1z])
    a_2 = MyCKLine([4444444444, -333333333, a2z])
    a_3 = MyCKLine([-233333333, a3y, 1222222222])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_persp_point(a1z, a2z, a3y):
    a_1 = PerspPoint([1333333333, 2333333333, a1z])
    a_2 = PerspPoint([4444444444, -333333333, a2z])
    a_3 = PerspPoint([-233333333, a3y, 1222222222])
    check_ck_plane(a_1, a_2, a_3)
