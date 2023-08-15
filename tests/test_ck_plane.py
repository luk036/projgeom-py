from hypothesis import given
from hypothesis.strategies import integers

from projgeom_py.ck_plane import (
    CayleyKleinPlane,
    is_perpendicular,
    orthocenter,
    tri_altitude,
)
from projgeom_py.ell_point import EllipticLine, EllipticPoint
from projgeom_py.hyp_point import HyperbolicLine, HyperbolicPoint
from projgeom_py.myck_point import MyCKLine, MyCKPoint
from projgeom_py.persp_point import PerspPoint

# from projgeom_py.pg_plane import coincident, harm_conj
from projgeom_py.pg_plane import tri_dual


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
    a_1 = EllipticPoint([13, 23, a1z])
    a_2 = EllipticPoint([44, -3, a2z])
    a_3 = EllipticPoint([-2, a3y, 12])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_ell_line(a1z, a2z, a3y):
    a_1 = EllipticLine([13, 23, a1z])
    a_2 = EllipticLine([44, -3, a2z])
    a_3 = EllipticLine([-2, a3y, 12])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_hyp_point(a1z, a2z, a3y):
    a_1 = HyperbolicPoint([13, 23, a1z])
    a_2 = HyperbolicPoint([44, -3, a2z])
    a_3 = HyperbolicPoint([-2, a3y, 12])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_hyp_line(a1z, a2z, a3y):
    a_1 = HyperbolicLine([13, 23, a1z])
    a_2 = HyperbolicLine([44, -3, a2z])
    a_3 = HyperbolicLine([-2, a3y, 12])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_myck_point(a1z, a2z, a3y):
    a_1 = MyCKPoint([13, 23, a1z])
    a_2 = MyCKPoint([44, -3, a2z])
    a_3 = MyCKPoint([-2, a3y, 12])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_myck_line(a1z, a2z, a3y):
    a_1 = MyCKLine([13, 23, a1z])
    a_2 = MyCKLine([44, -3, a2z])
    a_3 = MyCKLine([-2, a3y, 12])
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_persp_point(a1z, a2z, a3y):
    a_1 = PerspPoint([13, 23, a1z])
    a_2 = PerspPoint([44, -3, a2z])
    a_3 = PerspPoint([-2, a3y, 12])
    check_ck_plane(a_1, a_2, a_3)
