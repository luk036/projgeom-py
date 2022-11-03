import pytest

# from projgeom_py.pg_plane import coincident, harm_conj
from projgeom_py.ck_plane import (
    CKPlane,
    is_perpendicular,
    orthocenter,
    tri_altitude,
    tri_dual,
)
from projgeom_py.ell_point import EllLine, EllPoint
from projgeom_py.hyp_point import HypLine, HypPoint
from projgeom_py.myck_point import MyCKLine, MyCKPoint
from projgeom_py.persp_point import PerspPoint


def check_ck_plane(a1: CKPlane, a2: CKPlane, a3: CKPlane):
    triangle = [a1, a2, a3]
    trilateral = tri_dual(triangle)
    l1 = trilateral[0]
    assert l1.incident(triangle[1])

    t1, t2, t3 = tri_altitude(triangle)
    assert is_perpendicular(t1, l1)
    o = orthocenter(triangle)
    assert o == t2.circ(t3)


def test_ell_point(a1z, a2z, a3z):
    a1 = EllPoint([13, 23, a1z])
    a2 = EllPoint([44, -3, a2z])
    a3 = EllPoint([-2, 12, a3z])
    check_ck_plane(a1, a2, a3)


def test_ell_line(a1z, a2z, a3z):
    a1 = EllLine([13, 23, a1z])
    a2 = EllLine([44, -3, a2z])
    a3 = EllLine([-2, 12, a3z])
    check_ck_plane(a1, a2, a3)


def test_hyp_point(a1z, a2z, a3z):
    a1 = HypPoint([13, 23, a1z])
    a2 = HypPoint([44, -3, a2z])
    a3 = HypPoint([-2, 12, a3z])
    check_ck_plane(a1, a2, a3)


def test_hyp_line(a1z, a2z, a3z):
    a1 = HypLine([13, 23, a1z])
    a2 = HypLine([44, -3, a2z])
    a3 = HypLine([-2, 12, a3z])
    check_ck_plane(a1, a2, a3)


def test_myck_point(a1z, a2z, a3z):
    a1 = MyCKPoint([13, 23, a1z])
    a2 = MyCKPoint([44, -3, a2z])
    a3 = MyCKPoint([-2, 12, a3z])
    check_ck_plane(a1, a2, a3)


def test_myck_line(a1z, a2z, a3z):
    a1 = MyCKLine([13, 23, a1z])
    a2 = MyCKLine([44, -3, a2z])
    a3 = MyCKLine([-2, 12, a3z])
    check_ck_plane(a1, a2, a3)


def test_persp_point(a1z, a2z, a3z):
    a1 = PerspPoint([13, 23, a1z])
    a2 = PerspPoint([44, -3, a2z])
    a3 = PerspPoint([-2, 12, a3z])
    check_ck_plane(a1, a2, a3)
