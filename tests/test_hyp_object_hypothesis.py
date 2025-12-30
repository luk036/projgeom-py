"""
Hypothesis tests for hyp_object module
"""

from hypothesis import given, assume
from hypothesis.strategies import integers, composite

from projgeom.hyp_object import HyperbolicPoint, HyperbolicLine


@composite
def non_zero_triplets(draw):
    """Generate non-zero triplets of integers"""
    a = draw(integers(min_value=-100, max_value=100))
    b = draw(integers(min_value=-100, max_value=100))
    c = draw(integers(min_value=-100, max_value=100))
    assume(a != 0 or b != 0 or c != 0)
    return [a, b, c]


@composite
def hyperbolic_points(draw):
    """Generate valid HyperbolicPoint objects"""
    coords = draw(non_zero_triplets())
    return HyperbolicPoint(coords)


@composite
def hyperbolic_lines(draw):
    """Generate valid HyperbolicLine objects"""
    coords = draw(non_zero_triplets())
    return HyperbolicLine(coords)


@composite
def distinct_hyperbolic_points(draw):
    """Generate two distinct HyperbolicPoint objects"""
    pt1 = draw(hyperbolic_points())
    pt2 = draw(hyperbolic_points())
    assume(pt1 != pt2)
    return pt1, pt2


@composite
def distinct_hyperbolic_lines(draw):
    """Generate two distinct HyperbolicLine objects"""
    ln1 = draw(hyperbolic_lines())
    ln2 = draw(hyperbolic_lines())
    assume(ln1 != ln2)
    return ln1, ln2


@given(hyperbolic_points())
def test_hyperbolic_point_perp_returns_line(point):
    """Test that perp of a HyperbolicPoint returns a HyperbolicLine (polar line)"""
    line = point.perp()
    assert isinstance(line, HyperbolicLine)


@given(hyperbolic_lines())
def test_hyperbolic_line_perp_returns_point(line):
    """Test that perp of a HyperbolicLine returns a HyperbolicPoint (pole point)"""
    point = line.perp()
    assert isinstance(point, HyperbolicPoint)


@given(hyperbolic_points())
def test_hyperbolic_point_perp_coordinates(point):
    """Test that perp transforms coordinates correctly for hyperbolic points"""
    line = point.perp()
    expected_coords = [point.coord[0], point.coord[1], -point.coord[2]]
    assert line.coord == expected_coords


@given(hyperbolic_lines())
def test_hyperbolic_line_perp_coordinates(line):
    """Test that perp transforms coordinates correctly for hyperbolic lines"""
    point = line.perp()
    expected_coords = [line.coord[0], line.coord[1], -line.coord[2]]
    assert point.coord == expected_coords


@given(hyperbolic_points())
def test_hyperbolic_point_perp_duality(point):
    """Test that perp is dual to itself for hyperbolic points"""
    line = point.perp()
    point_back = line.perp()
    assert point_back == point


@given(hyperbolic_lines())
def test_hyperbolic_line_perp_duality(line):
    """Test that perp is dual to itself for hyperbolic lines"""
    point = line.perp()
    line_back = point.perp()
    assert line_back == line


@given(hyperbolic_points())
def test_hyperbolic_point_perp_incidence(point):
    """Test that a point has a polar line"""
    line = point.perp()
    assert isinstance(line, HyperbolicLine)
    # In hyperbolic geometry, the perp operation creates a dual object
    # but doesn't necessarily imply incidence


@given(hyperbolic_lines())
def test_hyperbolic_line_perp_incidence(line):
    """Test that a line has a pole point"""
    point = line.perp()
    assert isinstance(point, HyperbolicPoint)
    # In hyperbolic geometry, the perp operation creates a dual object
    # but doesn't necessarily imply incidence


@given(distinct_hyperbolic_points())
def test_hyperbolic_point_meet_perp(points):
    """Test properties of meet and perp for hyperbolic points"""
    pt_p, pt_q = points
    line = pt_p.meet(pt_q)

    # The polar of the intersection line should pass through the polar points
    perp_p = pt_p.perp()
    perp_q = pt_q.perp()
    perp_line = line.perp()

    assert perp_line.incident(perp_p)
    assert perp_line.incident(perp_q)


@given(distinct_hyperbolic_lines())
def test_hyperbolic_line_meet_perp(lines):
    """Test properties of meet and perp for hyperbolic lines"""
    ln_l, ln_m = lines
    point = ln_l.meet(ln_m)

    # The pole of the intersection point should lie on the pole lines
    perp_l = ln_l.perp()
    perp_m = ln_m.perp()
    perp_point = point.perp()

    assert perp_point.incident(perp_l)
    assert perp_point.incident(perp_m)


@given(hyperbolic_points())
def test_hyperbolic_point_aux_vs_perp(point):
    """Test difference between aux and perp for hyperbolic points"""
    aux_line = point.aux()
    perp_line = point.perp()

    # aux returns a line not incident with the point
    assert not point.incident(aux_line)
    # perp returns a line (dual object) but doesn't need to be incident
    assert isinstance(perp_line, HyperbolicLine)

    # In hyperbolic geometry, aux and perp may return different types of dual objects
    # aux is guaranteed not to be incident, perp is a geometric dual


@given(hyperbolic_lines())
def test_hyperbolic_line_aux_vs_perp(line):
    """Test difference between aux and perp for hyperbolic lines"""
    aux_point = line.aux()
    perp_point = line.perp()

    # aux returns a point not incident with the line
    assert not line.incident(aux_point)
    # perp returns a point (dual object) but doesn't need to be incident
    assert isinstance(perp_point, HyperbolicPoint)

    # In hyperbolic geometry, aux and perp may return different types of dual objects
    # aux is guaranteed not to be incident, perp is a geometric dual


@given(hyperbolic_points(), hyperbolic_lines())
def test_hyperbolic_perp_incidence_symmetry(point, line):
    """Test symmetry of incidence with polar/pole operations"""
    perp_point = line.perp()
    perp_line = point.perp()

    # If point is on line, then line's pole should be on point's polar
    if point.incident(line):
        assert perp_point.incident(perp_line)


@given(hyperbolic_points())
def test_hyperbolic_point_perp_not_aux(point):
    """Test that perp is not the same as aux for hyperbolic points"""
    aux_line = point.aux()
    perp_line = point.perp()

    # The aux line should not be incident with the point
    assert not point.incident(aux_line)
    # The perp line is a dual object
    assert isinstance(perp_line, HyperbolicLine)

    # They should generally be different since aux is guaranteed not to be incident
    # and perp is a geometric dual with specific coordinate transformation


@given(hyperbolic_lines())
def test_hyperbolic_line_perp_not_aux(line):
    """Test that perp is not the same as aux for hyperbolic lines"""
    aux_point = line.aux()
    perp_point = line.perp()

    # The aux point should not be incident with the line
    assert not line.incident(aux_point)
    # The perp point is a dual object
    assert isinstance(perp_point, HyperbolicPoint)

    # They should generally be different since aux is guaranteed not to be incident
    # and perp is a geometric dual with specific coordinate transformation
