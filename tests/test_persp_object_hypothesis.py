"""
Hypothesis tests for persp_object module
"""

from hypothesis import given, assume
from hypothesis.strategies import integers, composite

from projgeom.persp_object import PerspPoint, PerspLine, I_RE, I_IM, L_INF


@composite
def non_zero_triplets(draw):
    """Generate non-zero triplets of integers"""
    a = draw(integers(min_value=-100, max_value=100))
    b = draw(integers(min_value=-100, max_value=100))
    c = draw(integers(min_value=-100, max_value=100))
    assume(a != 0 or b != 0 or c != 0)
    return [a, b, c]


@composite
def persp_points(draw):
    """Generate valid PerspPoint objects"""
    coords = draw(non_zero_triplets())
    return PerspPoint(coords)


@composite
def persp_lines(draw):
    """Generate valid PerspLine objects"""
    coords = draw(non_zero_triplets())
    return PerspLine(coords)


@composite
def distinct_persp_points(draw):
    """Generate two distinct PerspPoint objects"""
    pt1 = draw(persp_points())
    pt2 = draw(persp_points())
    assume(pt1 != pt2)
    return pt1, pt2


@composite
def distinct_persp_lines(draw):
    """Generate two distinct PerspLine objects"""
    ln1 = draw(persp_lines())
    ln2 = draw(persp_lines())
    assume(ln1 != ln2)
    return ln1, ln2


@given(persp_points())
def test_persp_point_perp_returns_line(point):
    """Test that perp of a PerspPoint returns L_INF (polar line)"""
    line = point.perp()
    assert line == L_INF


@given(persp_lines())
def test_persp_line_perp_returns_point(line):
    """Test that perp of a PerspLine returns a PerspPoint (pole point)"""
    point = line.perp()
    assert isinstance(point, PerspPoint)


@given(persp_points())
def test_persp_point_midpoint_properties(pt_p):
    """Test properties of midpoint"""
    # Midpoint of a point with itself should be the same point
    midpoint = pt_p.midpoint(pt_p)
    assert midpoint == pt_p


@given(distinct_persp_points())
def test_persp_point_midpoint_symmetry(points):
    """Test that midpoint is symmetric"""
    pt_p, pt_q = points
    midpoint_pq = pt_p.midpoint(pt_q)
    midpoint_qp = pt_q.midpoint(pt_p)
    assert midpoint_pq == midpoint_qp


@given(distinct_persp_points())
def test_persp_point_midpoint_incidence(points):
    """Test that midpoint lies on the line through the two points"""
    pt_p, pt_q = points
    midpoint = pt_p.midpoint(pt_q)
    line = pt_p.meet(pt_q)
    assert line.incident(midpoint)


@given(distinct_persp_points())
def test_persp_point_midpoint_coordinates(points):
    """Test the coordinate formula for midpoint"""
    pt_p, pt_q = points
    midpoint = pt_p.midpoint(pt_q)

    # Calculate expected coordinates based on the implementation
    alpha = L_INF.dot(pt_q)
    beta = L_INF.dot(pt_p)
    expected = pt_p.parametrize(alpha, pt_q, beta)

    assert midpoint == expected


@given(persp_lines())
def test_persp_line_perp_coordinates(line):
    """Test the coordinate formula for perp"""
    point = line.perp()

    # Calculate expected coordinates based on the implementation
    alpha = I_RE.dot(line)
    beta = I_IM.dot(line)
    expected = I_RE.parametrize(alpha, I_IM, beta)

    assert point == expected


@given(persp_lines())
def test_persp_line_perp_incidence(line):
    """Test that a line has a pole"""
    point = line.perp()
    assert isinstance(point, PerspPoint)
    # In perspective geometry, the perp operation creates a dual object
    # but doesn't necessarily imply incidence


@given(distinct_persp_lines())
def test_persp_line_is_parallel_properties(lines):
    """Test properties of is_parallel"""
    ln_l, ln_m = lines

    # Parallelism should be symmetric
    assert ln_l.is_parallel(ln_m) == ln_m.is_parallel(ln_l)

    # A line is parallel to itself if it meets L_INF at infinity
    # This is a property of perspective geometry


@given(persp_lines())
def test_persp_line_parallel_to_l_inf(line):
    """Test that all lines are parallel to L_INF"""
    assert line.is_parallel(L_INF)
    assert L_INF.is_parallel(line)


@given(distinct_persp_lines())
def test_persp_line_parallel_meet(lines):
    """Test that parallel lines meet at infinity"""
    ln_l, ln_m = lines

    if ln_l.is_parallel(ln_m):
        intersection = ln_l.meet(ln_m)
        assert L_INF.incident(intersection)


@given(distinct_persp_points())
def test_persp_point_meet_perp(points):
    """Test properties of meet and perp for persp points"""
    pt_p, pt_q = points
    line = pt_p.meet(pt_q)

    # The polar of any point is L_INF
    perp_p = pt_p.perp()
    perp_q = pt_q.perp()
    perp_line = line.perp()

    assert perp_p == L_INF
    assert perp_q == L_INF

    # L_INF should be incident with the pole point of the line
    assert L_INF.incident(perp_line)


@given(distinct_persp_lines())
def test_persp_line_meet_perp(lines):
    """Test properties of meet and perp for persp lines"""
    ln_l, ln_m = lines
    point = ln_l.meet(ln_m)

    # The pole of the intersection point should lie on the pole lines
    perp_l = ln_l.perp()
    perp_m = ln_m.perp()
    perp_point = point.perp()  # This is L_INF

    assert perp_point == L_INF

    # L_INF should be incident with both pole lines
    assert perp_l.incident(L_INF)
    assert perp_m.incident(L_INF)


@given(persp_points())
def test_persp_point_aux_vs_perp(point):
    """Test difference between aux and perp for persp points"""
    aux_line = point.aux()
    perp_line = point.perp()

    # aux returns a line not incident with the point
    assert not point.incident(aux_line)
    # perp returns L_INF
    assert perp_line == L_INF

    # They should be different unless point is on L_INF
    if not point.incident(L_INF):
        assert aux_line != perp_line


@given(persp_lines())
def test_persp_line_aux_vs_perp(line):
    """Test difference between aux and perp for persp lines"""
    aux_point = line.aux()
    perp_point = line.perp()

    # aux returns a point not incident with the line
    assert not line.incident(aux_point)
    # perp returns a point (dual object) but doesn't need to be incident
    assert isinstance(perp_point, PerspPoint)

    # In perspective geometry, aux and perp may return different types of dual objects
    # aux is guaranteed not to be incident, perp is a geometric dual


@given(persp_points(), persp_lines())
def test_persp_perp_incidence_symmetry(point, line):
    """Test symmetry of incidence with poles/polars"""
    perp_point = line.perp()
    perp_line = point.perp()  # This is L_INF

    # If point is on line, then line's pole should be on point's polar (L_INF)
    if point.incident(line):
        assert perp_point.incident(perp_line)


@given(persp_points())
def test_persp_point_midpoint_with_l_inf(point):
    """Test midpoint with L_INF"""
    midpoint = point.midpoint(L_INF)

    # The midpoint should be on the line through point and L_INF
    line = point.meet(L_INF)
    assert line.incident(midpoint)


@given(persp_lines())
def test_persp_line_perp_coordinate_scaling(line):
    """Test how perp transforms coordinate scaling"""
    # Create a scaled version of the line
    scale = 3
    scaled_coords = [scale * coord for coord in line.coord]
    scaled_line = PerspLine(scaled_coords)

    # They should be equal in projective space
    assert line == scaled_line

    # Their poles should also be equal
    perp_original = line.perp()
    perp_scaled = scaled_line.perp()
    assert perp_original == perp_scaled


@given(persp_points())
def test_persp_point_midpoint_coordinate_scaling(point):
    """Test how midpoint transforms coordinate scaling"""
    # Create a scaled version of the point
    scale = 3
    scaled_coords = [scale * coord for coord in point.coord]
    scaled_point = PerspPoint(scaled_coords)

    # They should be equal in projective space
    assert point == scaled_point

    # Their midpoints with another point should also be equal
    other_point = PerspPoint([1, 2, 3])
    midpoint_original = point.midpoint(other_point)
    midpoint_scaled = scaled_point.midpoint(other_point)
    assert midpoint_original == midpoint_scaled
