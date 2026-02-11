from typing import Any

from hypothesis import given
from hypothesis.strategies import integers

from projgeom.ck_plane import (
    LineCk,
    PointCk,
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


def check_ck_plane(a_1: PointCk, a_2: PointCk, a_3: PointCk) -> None:
    triangle = [a_1, a_2, a_3]
    trilateral: list[LineCk] = tri_dual(triangle)  # type: ignore[assignment,arg-type]
    l_1: LineCk = trilateral[0]
    assert l_1.incident(triangle[1])

    t_1, t_2, t_3 = tri_altitude(triangle)
    assert is_perpendicular(t_1, l_1)
    pt_o = orthocenter(triangle)
    assert pt_o == t_2.meet(t_3)


@given(integers(), integers(), integers())
def test_ell_point(a1z: int, a2z: int, a3y: int) -> None:
    a_1: PointCk = EllipticPoint([13333333333, 2333333333, a1z])  # type: ignore[assignment]
    a_2: PointCk = EllipticPoint([44444444444, -333333333, a2z])  # type: ignore[assignment]
    a_3: PointCk = EllipticPoint([-2333333333, a3y, 1222222222])  # type: ignore[assignment]
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_ell_line(a1z: int, a2z: int, a3y: int) -> None:
    a_1: PointCk = EllipticLine([1333333333, 2333333333, a1z])  # type: ignore[assignment]
    a_2: PointCk = EllipticLine([4444444444, -333333333, a2z])  # type: ignore[assignment]
    a_3: PointCk = EllipticLine([-233333333, a3y, 1222222222])  # type: ignore[assignment]
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_hyp_point(a1z: int, a2z: int, a3y: int) -> None:
    a_1: PointCk = HyperbolicPoint([1333333333, 2333333333, a1z])  # type: ignore[assignment]
    a_2: PointCk = HyperbolicPoint([4444444444, -333333333, a2z])  # type: ignore[assignment]
    a_3: PointCk = HyperbolicPoint([-233333333, a3y, 1222222222])  # type: ignore[assignment]
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_hyp_line(a1z: int, a2z: int, a3y: int) -> None:
    a_1: PointCk = HyperbolicLine([1333333333, 2333333333, a1z])  # type: ignore[assignment]
    a_2: PointCk = HyperbolicLine([4444444444, -333333333, a2z])  # type: ignore[assignment]
    a_3: PointCk = HyperbolicLine([-233333333, a3y, 1222222222])  # type: ignore[assignment]
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_myck_point(a1z: int, a2z: int, a3y: int) -> None:
    a_1: PointCk = MyCKPoint([1333333333, 2333333333, a1z])  # type: ignore[assignment]
    a_2: PointCk = MyCKPoint([4444444444, -333333333, a2z])  # type: ignore[assignment]
    a_3: PointCk = MyCKPoint([-233333333, a3y, 1222222222])  # type: ignore[assignment]
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_myck_line(a1z: int, a2z: int, a3y: int) -> None:
    a_1: PointCk = MyCKLine([1333333333, 2333333333, a1z])  # type: ignore[assignment]
    a_2: PointCk = MyCKLine([4444444444, -333333333, a2z])  # type: ignore[assignment]
    a_3: PointCk = MyCKLine([-233333333, a3y, 1222222222])  # type: ignore[assignment]
    check_ck_plane(a_1, a_2, a_3)


@given(integers(), integers(), integers())
def test_persp_point(a1z: int, a2z: int, a3y: int) -> None:
    a_1: PointCk = PerspPoint([1333333333, 2333333333, a1z])  # type: ignore[assignment]
    a_2: PointCk = PerspPoint([4444444444, -333333333, a2z])  # type: ignore[assignment]
    a_3: PointCk = PerspPoint([-233333333, a3y, 1222222222])  # type: ignore[assignment]
    check_ck_plane(a_1, a_2, a_3)
