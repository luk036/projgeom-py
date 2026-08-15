from fractions import Fraction

from projgeom.pg_object import PgLine, PgPoint
from projgeom.proj_plane_measure import R0, R1, R, ratio_ratio, x_ratio


def test_ratio_ratio() -> None:
    assert ratio_ratio(1, 2, 3, 4) == Fraction(2, 3)


def test_x_ratio() -> None:
    a = PgPoint([1, 0, 1])
    b = PgPoint([0, 1, 1])
    l1 = PgLine([1, 2, -3])
    l2 = PgLine([3, 4, -5])
    r = x_ratio(a, b, l1, l2)
    assert abs(r) > 0


def test_R0() -> None:
    a = PgPoint([0, 0, 1])
    b = PgPoint([1, 1, 1])
    c = PgPoint([2, 2, 1])
    d = PgPoint([3, 3, 1])
    assert R0(a, b, c, d) is not None


def test_R1() -> None:
    a = PgPoint([0, 0, 1])
    b = PgPoint([1, 1, 1])
    c = PgPoint([2, 2, 1])
    d = PgPoint([3, 3, 1])
    assert R1(a, b, c, d) is not None


def test_R_fallback_to_r1() -> None:
    """R() falls back to R1 when cross0(pt_a, pt_b) == 0 (line 173)."""
    a = PgPoint([1, 1, 1])
    b = PgPoint([2, 1, 1])
    c = PgPoint([3, 1, 1])
    d = PgPoint([4, 1, 1])
    assert R(a, b, c, d) == Fraction(4, 3)
