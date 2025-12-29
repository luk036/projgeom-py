"""
Hypothesis tests for pg_object module
"""

from hypothesis import given, assume
from hypothesis.strategies import integers, composite

from projgeom.pg_object import PgPoint, PgLine, dot, cross, plckr


@composite
def non_zero_triplets(draw):
    """Generate non-zero triplets of integers"""
    a = draw(integers(min_value=-100, max_value=100))
    b = draw(integers(min_value=-100, max_value=100))
    c = draw(integers(min_value=-100, max_value=100))
    assume(a != 0 or b != 0 or c != 0)
    return [a, b, c]


@composite
def pg_points(draw):
    """Generate valid PgPoint objects"""
    coords = draw(non_zero_triplets())
    return PgPoint(coords)


@composite
def pg_lines(draw):
    """Generate valid PgLine objects"""
    coords = draw(non_zero_triplets())
    return PgLine(coords)


@composite
def distinct_pg_points(draw):
    """Generate two distinct PgPoint objects"""
    pt1 = draw(pg_points())
    pt2 = draw(pg_points())
    assume(pt1 != pt2)
    return pt1, pt2


@composite
def distinct_pg_lines(draw):
    """Generate two distinct PgLine objects"""
    ln1 = draw(pg_lines())
    ln2 = draw(pg_lines())
    assume(ln1 != ln2)
    return ln1, ln2


@given(non_zero_triplets(), non_zero_triplets())
def test_dot_commutativity(vec_a, vec_b):
    """Test that dot product is commutative"""
    assert dot(vec_a, vec_b) == dot(vec_b, vec_a)


@given(non_zero_triplets(), non_zero_triplets())
def test_cross_anti_commutativity(vec_a, vec_b):
    """Test that cross product is anti-commutative"""
    result_ab = cross(vec_a, vec_b)
    result_ba = cross(vec_b, vec_a)
    assert result_ab[0] == -result_ba[0]
    assert result_ab[1] == -result_ba[1]
    assert result_ab[2] == -result_ba[2]


@given(non_zero_triplets())
def test_cross_with_self_is_zero(vec):
    """Test that cross product of a vector with itself is zero"""
    result = cross(vec, vec)
    assert result == [0, 0, 0]


@given(
    integers(min_value=-10, max_value=10),
    integers(min_value=-10, max_value=10),
    non_zero_triplets(),
    non_zero_triplets(),
)
def test_plckr_linearity(lambda_val, mu_val, vec_a, vec_b):
    """Test that plckr operation is linear"""
    result = plckr(lambda_val, vec_a, mu_val, vec_b)
    expected = [
        lambda_val * vec_a[0] + mu_val * vec_b[0],
        lambda_val * vec_a[1] + mu_val * vec_b[1],
        lambda_val * vec_a[2] + mu_val * vec_b[2],
    ]
    assert result == expected


@given(pg_points(), pg_lines())
def test_incidence_symmetry(point, line):
    """Test that incidence is symmetric for points and lines"""
    assert point.incident(line) == line.incident(point)


@given(distinct_pg_points())
def test_meet_returns_line(points):
    """Test that meet of two distinct points returns a line"""
    pt_p, pt_q = points
    line = pt_p.meet(pt_q)
    assert isinstance(line, PgLine)
    assert line.incident(pt_p) and line.incident(pt_q)


@given(distinct_pg_lines())
def test_meet_returns_point(lines):
    """Test that meet of two distinct lines returns a point"""
    ln_l, ln_m = lines
    point = ln_l.meet(ln_m)
    assert isinstance(point, PgPoint)
    assert ln_l.incident(point) and ln_m.incident(point)


@given(pg_points())
def test_aux_returns_dual_type(point):
    """Test that aux returns the dual type"""
    dual = point.aux()
    assert isinstance(dual, PgLine)
    assert not point.incident(dual)


@given(pg_lines())
def test_aux_returns_dual_type_for_line(line):
    """Test that aux returns the dual type for lines"""
    dual = line.aux()
    assert isinstance(dual, PgPoint)
    assert not line.incident(dual)


@given(
    pg_points(),
    pg_points(),
    integers(min_value=-5, max_value=5),
    integers(min_value=-5, max_value=5),
)
def test_parametrize_returns_point_on_line(pt_p, pt_q, lambda_val, mu_val):
    """Test that parametrize returns a point on the line through two points"""
    assume(lambda_val != 0 or mu_val != 0)
    result = pt_p.parametrize(lambda_val, pt_q, mu_val)
    assert isinstance(result, PgPoint)

    # The result should be collinear with pt_p and pt_q
    line = pt_p.meet(pt_q)
    assert line.incident(result)


@given(
    pg_lines(),
    pg_lines(),
    integers(min_value=-5, max_value=5),
    integers(min_value=-5, max_value=5),
)
def test_parametrize_returns_line_through_point(ln_l, ln_m, lambda_val, mu_val):
    """Test that parametrize returns a line through the intersection point"""
    assume(lambda_val != 0 or mu_val != 0)
    result = ln_l.parametrize(lambda_val, ln_m, mu_val)
    assert isinstance(result, PgLine)

    # The result should pass through the intersection point
    point = ln_l.meet(ln_m)
    assert result.incident(point)


@given(pg_points(), pg_points(), pg_points())
def test_meet_associativity(pt_a, pt_b, pt_c):
    """Test associativity property of meet operation"""
    # (A ∧ B) ∧ C = A ∧ (B ∧ C) in geometric sense
    line_ab = pt_a.meet(pt_b)
    point_abc = line_ab.meet(pt_c)

    line_bc = pt_b.meet(pt_c)
    point_abc_alt = line_bc.meet(pt_a)

    # Both should represent the same geometric concept
    assert point_abc.__class__ == point_abc_alt.__class__


@given(pg_points(), pg_lines())
def test_duality_preservation(pt1, ln1):
    """Test that duality preserves incidence relations"""
    # If point is on line, then dual of line is on dual of point
    if pt1.incident(ln1):
        dual_pt1 = pt1.aux()
        dual_ln1 = ln1.aux()
        assert dual_ln1.incident(dual_pt1)
    else:
        # If point is not on line, then dual of line is not on dual of point
        dual_pt1 = pt1.aux()
        dual_ln1 = ln1.aux()
        assert not dual_ln1.incident(dual_pt1)


@given(pg_points(), pg_points())
def test_equality_up_to_scalar(pt1, pt2):
    """Test that points are equal if their coordinates are scalar multiples"""
    # Create a scaled version of pt1
    scale = 3
    scaled_coords = [scale * coord for coord in pt1.coord]
    pt1_scaled = PgPoint(scaled_coords)

    # They should be equal in projective space
    assert pt1 == pt1_scaled

    # But pt1 and pt2 should generally be different
    # (unless they happen to be scalar multiples)
    # This test mainly checks the equality logic works correctly
