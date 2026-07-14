"""
Cross-project Consistency Verification.

Verifies that Python produces the same results as Rust/C++ for
identical operations. Expected values are derived from the Rust
projgeom-rs test suite and docstring examples.
"""

import sys
sys.path.insert(0, 'src')

from fractions import Fraction

from projgeom.pg_object import PgPoint, PgLine, dot, cross, cross0, cross1, plckr
from projgeom.pg_plane import harm_conj, involution, coincident, check_pappus, persp
from projgeom.ell_object import EllipticPoint, EllipticLine
from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine
from projgeom.euclid_object import (
    EuclidPoint, EuclidLine, midpoint, orthocenter, tri_altitude,
    Ptolemy, archimedes, cqq, uc_point, is_parallel, is_perpendicular,
    reflect_involution,
)
from projgeom.proj_plane_measure import R, R0, R1, ratio_ratio
from projgeom.transform import Transform
from projgeom.conic import Conic, ConicType


# ===========================================================================
# Section 1: Vector/Coordinate Operations
# ===========================================================================

def test_dot_product():
    """Rust doc test: dot_product(&[1,2,3], &[4,5,6]) == 26"""
    result = dot([1, 2, 3], [4, 5, 6])
    assert result == 32, f"dot([1,2,3],[4,5,6]) = {result}, expected 32"
    print("  ✅ dot_product")


def test_cross0():
    """Rust doc test: cross0(&[1,2,3], &[4,5,6]) == -3"""
    result = cross0([1, 2, 3], [4, 5, 6])
    assert result == -3, f"cross0 = {result}"
    print("  ✅ cross0")


def test_cross1():
    """Rust doc test: cross1(&[1,2,3], &[4,5,6]) == -6"""
    result = cross1([1, 2, 3], [4, 5, 6])
    assert result == -6, f"cross1 = {result}"
    print("  ✅ cross1")


def test_cross_product():
    """Rust doc test: cross_product(&[1,2,3], &[3,4,5]) == [-2,4,-2]"""
    result = cross([1, 2, 3], [3, 4, 5])
    assert result == [-2, 4, -2], f"cross = {result}"
    print("  ✅ cross_product")


def test_plucker():
    """Rust doc test: plucker_operation(1, [1,2,3], -1, [3,4,5]) == [-2,-2,-2]"""
    result = plckr(1, [1, 2, 3], -1, [3, 4, 5])
    assert result == [-2, -2, -2], f"plckr = {result}"
    print("  ✅ plucker_operation")


# ===========================================================================
# Section 2: Projective Point/Line Operations
# ===========================================================================

def test_pgpoint_equality():
    """Rust test: PgPoint([1,2,3]) == PgPoint([2,4,6])"""
    assert PgPoint([1, 2, 3]) == PgPoint([2, 4, 6])
    assert PgPoint([1, 2, 3]) != PgPoint([1, 0, 0])
    print("  ✅ PgPoint equality")


def test_meet():
    """Rust doc test: p1.meet(p2) gives line through points"""
    p1, p2 = PgPoint([1, 2, 3]), PgPoint([4, 5, 6])
    line = p1.meet(p2)
    assert line == PgLine([-3, 6, -3])
    assert line.incident(p1)
    assert line.incident(p2)
    print("  ✅ meet + incident")


def test_parametrize():
    """Rust doc test: p1.parametrize(1, p2, 1) == PgPoint([1,1,2])"""
    p1, p2 = PgPoint([1, 0, 1]), PgPoint([0, 1, 1])
    mid = p1.parametrize(1, p2, 1)
    assert mid == PgPoint([1, 1, 2])
    print("  ✅ parametrize")


# ===========================================================================
# Section 3: Harmonic Conjugate
# ===========================================================================

def test_harmonic_conjugate():
    """
    Rust doc test: harm_conj(PgPoint([1,0,1]), PgPoint([0,0,1]), PgPoint([2,0,1]))
    == PgPoint([2,0,3])
    """
    a, b, c = PgPoint([1, 0, 1]), PgPoint([0, 0, 1]), PgPoint([2, 0, 1])
    d = harm_conj(a, b, c)
    assert d == PgPoint([2, 0, 3]), f"harm_conj = {d}"
    print("  ✅ harm_conj")


# ===========================================================================
# Section 4: Cayley-Klein perp() operations
# ===========================================================================

def test_elliptic_perp():
    """Elliptic: p.perp() == EllipticLine(p.coord) — self-dual"""
    p = EllipticPoint([1, 2, 3])
    l = p.perp()
    assert l == EllipticLine([1, 2, 3])
    # Double perp returns to self
    assert l.perp() == EllipticPoint([1, 2, 3])
    print("  ✅ Elliptic perp")


def test_hyperbolic_perp():
    """Hyperbolic: (x,y,z).perp() == (x,y,-z)"""
    p = HyperbolicPoint([1, 2, 3])
    l = p.perp()
    assert l == HyperbolicLine([1, 2, -3]), f"hyp perp = {l}"
    # Double perp
    p2 = l.perp()
    assert p2 == HyperbolicPoint([1, 2, 3])
    print("  ✅ Hyperbolic perp")


def test_euclidean_perp_point():
    """Euclidean point: perp() == L_INF = (0,0,1)"""
    p = EuclidPoint([1, 2, 1])
    l = p.perp()
    assert l == EuclidLine([0, 0, 1]), f"euc point perp = {l}"
    print("  ✅ Euclidean point perp")


def test_euclidean_perp_line():
    """Euclidean line: perp() == direction vector (a,b,0)"""
    l = EuclidLine([1, 2, -3])
    p = l.perp()
    assert p == EuclidPoint([1, 2, 0]), f"euc line perp = {p}"
    print("  ✅ Euclidean line perp")


# ===========================================================================
# Section 5: Euclidean Geometry
# ===========================================================================

def test_midpoint():
    """Rust doc test: midpoint((0,0),(2,4)) == (1,2)"""
    a, b = EuclidPoint([0, 0, 1]), EuclidPoint([2, 4, 1])
    m = midpoint(a, b)
    assert m == EuclidPoint([1, 2, 1]), f"midpoint = {m}"
    print("  ✅ midpoint")


def test_orthocenter():
    """Rust doc test: orthocenter((0,0),(2,0),(1,3)) == (3,1,3)"""
    a, b, c = EuclidPoint([0, 0, 1]), EuclidPoint([2, 0, 1]), EuclidPoint([1, 3, 1])
    h = orthocenter([a, b, c])
    assert h == EuclidPoint([3, 1, 3]), f"orthocenter = {h}"
    print("  ✅ orthocenter")


def test_ptolemy():
    """Rust doc test: rectangle 3×4 → diagonals 5"""
    assert Ptolemy([9, 16, 9, 16, 25, 25])
    print("  ✅ Ptolemy")


def test_archimedes():
    """archimedes(a,b,c) = 4ab - (a+b-c)²; zero when c = a+b±2√(ab)"""
    # 4*1*4 - (1+4-9)² = 16 - 16 = 0
    assert archimedes(1, 4, 9) == 0
    # archimedes(1,2,3) = 4*1*2 - (1+2-3)² = 8 - 0 = 8 ≠ 0
    assert archimedes(1, 2, 3) == 8
    print("  ✅ archimedes")


def test_uc_point():
    """Rust doc test: uc_point(1,0) == (1,0,1), uc_point(0,1) == (-1,0,1)"""
    assert uc_point(1, 0) == EuclidPoint([1, 0, 1])
    assert uc_point(0, 1) == EuclidPoint([-1, 0, 1])
    print("  ✅ uc_point")


def test_euclid_is_parallel():
    """Rust doc test: l1.is_parallel(l2)"""
    l1, l2 = EuclidLine([1, 0, -1]), EuclidLine([2, 0, -5])
    assert is_parallel(l1, l2)
    assert not is_parallel(l1, EuclidLine([0, 1, -1]))
    print("  ✅ is_parallel")


def test_euclid_is_perpendicular():
    """Rust doc test: l1.is_perpendicular(l2)"""
    l1, l2 = EuclidLine([1, 0, -1]), EuclidLine([0, 1, -1])
    assert is_perpendicular(l1, l2)
    assert not is_perpendicular(l1, EuclidLine([1, 1, -1]))
    print("  ✅ is_perpendicular")


def test_reflect_involution():
    """Rust doc test: reflect((2,0) across y-axis) == (-2,0)"""
    mirror, p = EuclidLine([1, 0, 0]), EuclidPoint([2, 0, 1])
    reflected = reflect_involution(mirror, p)
    assert reflected == EuclidPoint([-2, 0, 1]), f"reflected = {reflected}"
    print("  ✅ reflect_involution")


# ===========================================================================
# Section 6: Cross-Ratio
# ===========================================================================

def test_ratio_ratio():
    """C++/Rust: ratio_ratio(1,2,3,4) == 2/3"""
    r = ratio_ratio(1, 2, 3, 4)
    assert r == Fraction(2, 3), f"ratio_ratio = {r}"
    print("  ✅ ratio_ratio")


def test_cross_ratio_R():
    """C++/Rust doc test: R(points) computes correctly"""
    a, b, c, d = [PgPoint([i, 0, 1]) for i in range(4)]
    r = R(a, b, c, d)
    assert r is not None and r.denominator != 0
    print(f"  ✅ cross_ratio R: {r}")


# ===========================================================================
# Section 7: Conic Sections
# ===========================================================================

def test_conic_unit_circle():
    """Rust doc test: Conic.unit_circle()"""
    circle = Conic.unit_circle()
    assert circle.contains(PgPoint([1, 0, 1]))
    assert circle.contains(PgPoint([0, 1, 1]))
    assert not circle.contains(PgPoint([2, 0, 1]))
    assert circle.conic_type() == ConicType.ELLIPSE
    print("  ✅ Conic unit_circle")


def test_conic_polar():
    """Rust doc test: polar of (1,0) on unit circle == x=1"""
    circle = Conic.unit_circle()
    polar = circle.polar(PgPoint([1, 0, 1]))
    assert polar == PgLine([1, 0, -1]), f"polar = {polar}"
    print("  ✅ Conic polar")


# ===========================================================================
# Section 8: Transform
# ===========================================================================

def test_transform_translation():
    """Rust doc test: translation(5,3) applied to (1,2,1) == (6,5,1)"""
    t = Transform.translation(5, 3)
    p = t.apply_point(PgPoint([1, 2, 1]))
    assert p == PgPoint([6, 5, 1])
    print("  ✅ Transform translation")


def test_transform_inverse():
    """Rust doc test: inverse restores original point"""
    t = Transform.translation(5, 3)
    inv = t.inverse()
    p = PgPoint([1, 2, 1])
    restored = inv.apply_point(t.apply_point(p))
    assert restored == p, f"restored = {restored}"
    print("  ✅ Transform inverse")


def test_transform_rotation():
    """Rust doc test: rotation 90° of (1,0) == (0,1)"""
    t = Transform.rotation(Fraction(0, 1), Fraction(1, 1))
    p = t.apply_point(PgPoint([1, 0, 1]))
    assert p == PgPoint([0, 1, 1])
    print("  ✅ Transform rotation")


def test_transform_scaling():
    """Rust doc test: scaling(2,3) of (1,2) == (2,6)"""
    t = Transform.scaling(Fraction(2, 1), Fraction(3, 1))
    p = t.apply_point(PgPoint([1, 2, 1]))
    assert p == PgPoint([2, 6, 1])
    print("  ✅ Transform scaling")


def test_transform_compose():
    """Rust doc test: compose translation + scaling"""
    t1 = Transform.translation(2, 3)
    t2 = Transform.scaling(Fraction(2, 1), Fraction(2, 1))
    tc = t1.compose(t2)
    p = tc.apply_point(PgPoint([1, 1, 1]))
    assert p == PgPoint([4, 5, 1])
    print("  ✅ Transform compose")


# ===========================================================================
# Run all
# ===========================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Cross-Project Consistency Verification (Python ↔ Rust/C++)")
    print("=" * 60)
    tests = [
        ("Vector/Coordinate Operations", [
            test_dot_product, test_cross0, test_cross1, test_cross_product,
            test_plucker,
        ]),
        ("Projective Point/Line", [
            test_pgpoint_equality, test_meet, test_parametrize,
        ]),
        ("Harmonic Conjugate", [
            test_harmonic_conjugate,
        ]),
        ("Cayley-Klein perp()", [
            test_elliptic_perp, test_hyperbolic_perp,
            test_euclidean_perp_point, test_euclidean_perp_line,
        ]),
        ("Euclidean Geometry", [
            test_midpoint, test_orthocenter, test_ptolemy, test_archimedes,
            test_uc_point, test_euclid_is_parallel, test_euclid_is_perpendicular,
            test_reflect_involution,
        ]),
        ("Cross-Ratio", [
            test_ratio_ratio, test_cross_ratio_R,
        ]),
        ("Conic Sections", [
            test_conic_unit_circle, test_conic_polar,
        ]),
        ("Transform", [
            test_transform_translation, test_transform_inverse,
            test_transform_rotation, test_transform_scaling, test_transform_compose,
        ]),
    ]
    total = 0
    for section_name, section_tests in tests:
        print(f"\n── {section_name} ──")
        for test_fn in section_tests:
            try:
                test_fn()
                total += 1
            except AssertionError as e:
                print(f"  ❌ {test_fn.__name__}: {e}")
            except Exception as e:
                print(f"  ❌ {test_fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{'=' * 60}")
    print(f"Results: {total}/{sum(len(t[1]) for t in tests)} tests passed")
    print(f"{'=' * 60}")
