"""
Benchmarks for projective geometry operations.

Run with: pytest tests/bench_projgeom.py --benchmark-only --benchmark-sort=name
"""

import pytest
from fractions import Fraction

from projgeom.pg_object import PgPoint, PgLine, dot, cross, cross0, cross1, cross2, dot1, plckr
from projgeom.conic import Conic, ConicType
from projgeom.transform import Transform
from projgeom.euclid_object import EuclidPoint, EuclidLine, orthocenter, tri_altitude, midpoint
from projgeom.proj_plane_measure import R, R0, R1


def test_bench_dot_product(benchmark):
    """Benchmark dot product of two homogeneous 3-vectors."""
    a, b = [1, 2, 3], [4, 5, 6]
    result = benchmark(dot, a, b)
    assert result == 32


def test_bench_cross_product(benchmark):
    """Benchmark cross product of two homogeneous 3-vectors."""
    a, b = [1, 2, 3], [4, 5, 6]
    result = benchmark(cross, a, b)
    assert result == [-3, 6, -3]


def test_bench_cross0(benchmark):
    result = benchmark(cross0, [1, 2, 3], [4, 5, 6])
    assert result == -3


def test_bench_cross1(benchmark):
    result = benchmark(cross1, [1, 2, 3], [4, 5, 6])
    assert result == -6


def test_bench_cross2(benchmark):
    result = benchmark(cross2, [1, 2], [3, 4])
    assert result == -2


def test_bench_dot1(benchmark):
    result = benchmark(dot1, [1, 2], [3, 4])
    assert result == 11


def test_bench_plckr(benchmark):
    """Benchmark Plücker parametrization."""
    result = benchmark(plckr, 1, [1, 2, 3], 2, [4, 5, 6])
    assert result == [9, 12, 15]


def test_bench_point_creation_pg(benchmark):
    """Benchmark PgPoint creation."""
    p = benchmark(PgPoint, [1, 2, 3])
    assert p.coord == [1, 2, 3]


def test_bench_point_creation_euclid(benchmark):
    """Benchmark EuclidPoint creation."""
    p = benchmark(EuclidPoint, [1, 2, 1])
    assert p.coord == [1, 2, 1]


def test_bench_meet_points(benchmark):
    """Benchmark meet (join) of two points to form a line."""
    p1, p2 = PgPoint([1, 2, 3]), PgPoint([4, 5, 6])
    l = benchmark(p1.meet, p2)
    assert l == PgLine([-3, 6, -3])


def test_bench_meet_lines(benchmark):
    """Benchmark meet of two lines to form a point."""
    l1, l2 = PgLine([1, 0, 0]), PgLine([0, 1, 0])
    p = benchmark(l1.meet, l2)
    assert p == PgPoint([0, 0, 1])


def test_bench_incident(benchmark):
    """Benchmark incidence check."""
    p, l = PgPoint([1, 2, 3]), PgLine([4, 5, 6])
    result = benchmark(p.incident, l)
    assert not result


def test_bench_parametrize(benchmark):
    """Benchmark point parametrization."""
    p1, p2 = PgPoint([1, 2, 3]), PgPoint([4, 5, 6])
    result = benchmark(p1.parametrize, 2, p2, 3)
    assert result == PgPoint([14, 19, 24])


def test_bench_harmonic_conjugate(benchmark):
    """Benchmark harmonic conjugate via pg_plane."""
    from projgeom.pg_plane import harm_conj
    a, b, c = PgPoint([1, 0, 1]), PgPoint([0, 0, 1]), PgPoint([2, 0, 1])
    d = benchmark(harm_conj, a, b, c)
    assert d == PgPoint([2, 0, 3])


def test_bench_orthocenter(benchmark):
    """Benchmark triangle orthocenter."""
    a, b, c = EuclidPoint([0, 0, 1]), EuclidPoint([2, 0, 1]), EuclidPoint([1, 3, 1])
    h = benchmark(orthocenter, [a, b, c])
    assert h == EuclidPoint([3, 1, 3])


def test_bench_tri_altitude(benchmark):
    """Benchmark triangle altitudes."""
    a, b, c = EuclidPoint([0, 0, 1]), EuclidPoint([2, 0, 1]), EuclidPoint([1, 3, 1])
    alts = benchmark(tri_altitude, [a, b, c])
    assert len(alts) == 3


def test_bench_midpoint(benchmark):
    """Benchmark midpoint calculation."""
    a, b = EuclidPoint([0, 0, 1]), EuclidPoint([2, 4, 1])
    m = benchmark(midpoint, a, b)
    assert m == EuclidPoint([1, 2, 1])


def test_bench_cross_ratio_R(benchmark):
    """Benchmark cross-ratio R (auto-select)."""
    a, b, c, d = [PgPoint([i, 0, 1]) for i in range(4)]
    r = benchmark(R, a, b, c, d)
    assert r is not None


def test_bench_conic_contains(benchmark):
    """Benchmark conic.contains()."""
    circle = Conic.unit_circle()
    pt = PgPoint([1, 0, 1])
    result = benchmark(circle.contains, pt)
    assert result is True


def test_bench_transform_apply(benchmark):
    """Benchmark transform apply_point."""
    t = Transform.translation(5, 3)
    p = PgPoint([1, 2, 1])
    result = benchmark(t.apply_point, p)
    assert result == PgPoint([6, 5, 1])


def test_bench_transform_inverse(benchmark):
    """Benchmark transform inverse."""
    t = Transform.translation(5, 3)
    inv = benchmark(t.inverse)
    assert inv is not None
    # Verify inverse restores original
    p = PgPoint([1, 2, 1])
    restored = inv.apply_point(t.apply_point(p))
    assert restored == p
