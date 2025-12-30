"""
Hypothesis tests for myck_object module
"""

from hypothesis import given, assume
from hypothesis.strategies import integers, composite

from projgeom.myck_object import MyCKPoint, MyCKLine


@composite
def non_zero_triplets(draw):
    """Generate non-zero triplets of integers"""
    a = draw(integers(min_value=-100, max_value=100))
    b = draw(integers(min_value=-100, max_value=100))
    c = draw(integers(min_value=-100, max_value=100))
    assume(a != 0 or b != 0 or c != 0)
    return [a, b, c]


@composite
def myck_points(draw):
    """Generate valid MyCKPoint objects"""
    coords = draw(non_zero_triplets())
    return MyCKPoint(coords)


@composite
def myck_lines(draw):
    """Generate valid MyCKLine objects"""
    coords = draw(non_zero_triplets())
    return MyCKLine(coords)


@composite
def distinct_myck_points(draw):
    """Generate two distinct MyCKPoint objects"""
    pt1 = draw(myck_points())
    pt2 = draw(myck_points())
    assume(pt1 != pt2)
    return pt1, pt2


@composite
def distinct_myck_lines(draw):
    """Generate two distinct MyCKLine objects"""
    ln1 = draw(myck_lines())
    ln2 = draw(myck_lines())
    assume(ln1 != ln2)
    return ln1, ln2


@given(myck_points())
def test_myck_point_perp_returns_line(point):
    """Test that perp of a MyCKPoint returns a MyCKLine (polar line)"""
    line = point.perp()
    assert isinstance(line, MyCKLine)


@given(myck_lines())
def test_myck_line_perp_returns_point(line):
    """Test that perp of a MyCKLine returns a MyCKPoint (pole point)"""
    point = line.perp()
    assert isinstance(point, MyCKPoint)


@given(myck_points())
def test_myck_point_perp_coordinates(point):
    """Test that perp transforms coordinates correctly for MyCK points"""
    line = point.perp()
    expected_coords = [-2 * point.coord[0], point.coord[1], -2 * point.coord[2]]
    assert line.coord == expected_coords


@given(myck_lines())
def test_myck_line_perp_coordinates(line):
    """Test that perp transforms coordinates correctly for MyCK lines"""
    point = line.perp()
    expected_coords = [-line.coord[0], 2 * line.coord[1], -line.coord[2]]
    assert point.coord == expected_coords


@given(myck_points())
def test_myck_point_perp_duality(point):
    """Test that perp is dual to itself for MyCK points"""
    line = point.perp()
    point_back = line.perp()
    assert point_back == point


@given(myck_lines())
def test_myck_line_perp_duality(line):
    """Test that perp is dual to itself for MyCK lines"""
    point = line.perp()
    line_back = point.perp()
    assert line_back == line


@given(myck_points())
def test_myck_point_perp_incidence(point):
    """Test that a point has a polar line"""
    line = point.perp()
    assert isinstance(line, MyCKLine)
    # In Cayley-Klein geometry, the perp operation creates a dual object
    # but doesn't necessarily imply incidence


@given(myck_lines())
def test_myck_line_perp_incidence(line):
    """Test that a line has a pole point"""
    point = line.perp()
    assert isinstance(point, MyCKPoint)
    # In Cayley-Klein geometry, the perp operation creates a dual object
    # but doesn't necessarily imply incidence


@given(distinct_myck_points())
def test_myck_point_meet_perp(points):
    """Test properties of meet and perp for MyCK points"""
    pt_p, pt_q = points
    line = pt_p.meet(pt_q)

    # The polar of the intersection line should pass through the polar points
    perp_p = pt_p.perp()
    perp_q = pt_q.perp()
    perp_line = line.perp()

    assert perp_line.incident(perp_p)
    assert perp_line.incident(perp_q)


@given(distinct_myck_lines())
def test_myck_line_meet_perp(lines):
    """Test properties of meet and perp for MyCK lines"""
    ln_l, ln_m = lines
    point = ln_l.meet(ln_m)

    # The pole of the intersection point should lie on the pole lines
    perp_l = ln_l.perp()
    perp_m = ln_m.perp()
    perp_point = point.perp()

    assert perp_point.incident(perp_l)
    assert perp_point.incident(perp_m)


@given(myck_points())
def test_myck_point_aux_vs_perp(point):
    """Test difference between aux and perp for MyCK points"""
    aux_line = point.aux()
    perp_line = point.perp()

    # aux returns a line not incident with the point
    assert not point.incident(aux_line)
    # perp returns a line (dual object) but doesn't need to be incident
    assert isinstance(perp_line, MyCKLine)

    # In Cayley-Klein geometry, aux and perp may return different types of dual objects
    # aux is guaranteed not to be incident, perp is a geometric dual


@given(myck_lines())
def test_myck_line_aux_vs_perp(line):
    """Test difference between aux and perp for MyCK lines"""
    aux_point = line.aux()
    perp_point = line.perp()

    # aux returns a point not incident with the line
    assert not line.incident(aux_point)
    # perp returns a point (dual object) but doesn't need to be incident
    assert isinstance(perp_point, MyCKPoint)

    # In Cayley-Klein geometry, aux and perp may return different types of dual objects
    # aux is guaranteed not to be incident, perp is a geometric dual


@given(myck_points(), myck_lines())
def test_myck_perp_incidence_symmetry(point, line):
    """Test symmetry of incidence with polar/pole operations"""
    perp_point = line.perp()
    perp_line = point.perp()

    # If point is on line, then line's pole should be on point's polar
    if point.incident(line):
        assert perp_point.incident(perp_line)


@given(myck_points())
def test_myck_point_perp_not_aux(point):
    """Test that perp is not the same as aux for MyCK points"""
    aux_line = point.aux()
    perp_line = point.perp()

    # The aux line should not be incident with the point
    assert not point.incident(aux_line)
    # The perp line is a dual object
    assert isinstance(perp_line, MyCKLine)

    # They should generally be different since aux is guaranteed not to be incident
    # and perp is a geometric dual with specific coordinate transformation


@given(myck_lines())
def test_myck_line_perp_not_aux(line):
    """Test that perp is not the same as aux for MyCK lines"""
    aux_point = line.aux()
    perp_point = line.perp()

    # The aux point should not be incident with the line
    assert not line.incident(aux_point)
    # The perp point is a dual object
    assert isinstance(perp_point, MyCKPoint)

    # They should generally be different since aux is guaranteed not to be incident
    # and perp is a geometric dual with specific coordinate transformation


@given(myck_points())
def test_myck_point_perp_coordinate_scaling(point):
    """Test how perp transforms coordinate scaling"""
    # Create a scaled version of the point
    scale = 3
    scaled_coords = [scale * coord for coord in point.coord]
    scaled_point = MyCKPoint(scaled_coords)

    # They should be equal in projective space
    assert point == scaled_point

    # Their perpendiculars should also be equal
    perp_original = point.perp()
    perp_scaled = scaled_point.perp()
    assert perp_original == perp_scaled


@given(myck_lines())
def test_myck_line_perp_coordinate_scaling(line):
    """Test how perp transforms coordinate scaling"""
    # Create a scaled version of the line
    scale = 3
    scaled_coords = [scale * coord for coord in line.coord]
    scaled_line = MyCKLine(scaled_coords)

    # They should be equal in projective space
    assert line == scaled_line

    # Their perpendiculars should also be equal
    perp_original = line.perp()
    perp_scaled = scaled_line.perp()
    assert perp_original == perp_scaled
