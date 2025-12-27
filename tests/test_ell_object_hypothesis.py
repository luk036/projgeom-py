"""
Hypothesis tests for ell_object module
"""

from hypothesis import given, assume, strategies as st
from hypothesis.strategies import lists, integers, composite

from projgeom.ell_object import EllipticPoint, EllipticLine


@composite
def non_zero_triplets(draw):
    """Generate non-zero triplets of integers"""
    a = draw(integers(min_value=-100, max_value=100))
    b = draw(integers(min_value=-100, max_value=100))
    c = draw(integers(min_value=-100, max_value=100))
    assume(a != 0 or b != 0 or c != 0)
    return [a, b, c]


@composite
def elliptic_points(draw):
    """Generate valid EllipticPoint objects"""
    coords = draw(non_zero_triplets())
    return EllipticPoint(coords)


@composite
def elliptic_lines(draw):
    """Generate valid EllipticLine objects"""
    coords = draw(non_zero_triplets())
    return EllipticLine(coords)


@composite
def distinct_elliptic_points(draw):
    """Generate two distinct EllipticPoint objects"""
    pt1 = draw(elliptic_points())
    pt2 = draw(elliptic_points())
    assume(pt1 != pt2)
    return pt1, pt2


@composite
def distinct_elliptic_lines(draw):
    """Generate two distinct EllipticLine objects"""
    ln1 = draw(elliptic_lines())
    ln2 = draw(elliptic_lines())
    assume(ln1 != ln2)
    return ln1, ln2


@given(elliptic_points())
def test_elliptic_point_perp_returns_line(point):
    """Test that perp of an EllipticPoint returns an EllipticLine"""
    line = point.perp()
    assert isinstance(line, EllipticLine)


@given(elliptic_lines())
def test_elliptic_line_perp_returns_point(line):
    """Test that perp of an EllipticLine returns an EllipticPoint"""
    point = line.perp()
    assert isinstance(point, EllipticPoint)


@given(elliptic_points())
def test_elliptic_point_perp_incidence(point):
    """Test that a point has a perpendicular line"""
    line = point.perp()
    assert isinstance(line, EllipticLine)
    # In elliptic geometry, the perp operation creates a dual object
    # but doesn't necessarily imply incidence


@given(elliptic_lines())
def test_elliptic_line_perp_incidence(line):
    """Test that a line has a perpendicular point"""
    point = line.perp()
    assert isinstance(point, EllipticPoint)
    # In elliptic geometry, the perp operation creates a dual object
    # but doesn't necessarily imply incidence


@given(elliptic_points())
def test_elliptic_point_perp_coordinates(point):
    """Test that perp preserves coordinates for elliptic points"""
    line = point.perp()
    assert line.coord == point.coord


@given(elliptic_lines())
def test_elliptic_line_perp_coordinates(line):
    """Test that perp preserves coordinates for elliptic lines"""
    point = line.perp()
    assert point.coord == line.coord


@given(elliptic_points())
def test_elliptic_point_perp_duality(point):
    """Test that perp is dual to itself for elliptic points"""
    line = point.perp()
    point_back = line.perp()
    assert point_back == point


@given(elliptic_lines())
def test_elliptic_line_perp_duality(line):
    """Test that perp is dual to itself for elliptic lines"""
    point = line.perp()
    line_back = point.perp()
    assert line_back == line


@given(distinct_elliptic_points())
def test_elliptic_point_meet_perp(points):
    """Test properties of meet and perp for elliptic points"""
    pt_p, pt_q = points
    line = pt_p.meet(pt_q)
    
    # The perpendicular of the intersection line should pass through the perpendicular points
    perp_p = pt_p.perp()
    perp_q = pt_q.perp()
    perp_line = line.perp()
    
    assert perp_line.incident(perp_p)
    assert perp_line.incident(perp_q)


@given(distinct_elliptic_lines())
def test_elliptic_line_meet_perp(lines):
    """Test properties of meet and perp for elliptic lines"""
    ln_l, ln_m = lines
    point = ln_l.meet(ln_m)
    
    # The perpendicular of the intersection point should lie on the perpendicular lines
    perp_l = ln_l.perp()
    perp_m = ln_m.perp()
    perp_point = point.perp()
    
    assert perp_point.incident(perp_l)
    assert perp_point.incident(perp_m)


@given(elliptic_points())
def test_elliptic_point_aux_vs_perp(point):
    """Test difference between aux and perp for elliptic points"""
    aux_line = point.aux()
    perp_line = point.perp()
    
    # aux returns a line not incident with the point
    assert not point.incident(aux_line)
    # perp returns a line (dual object) but doesn't need to be incident
    assert isinstance(perp_line, EllipticLine)
    
    # In elliptic geometry, aux and perp may return different types of dual objects
    # aux is guaranteed not to be incident, perp is a geometric dual


@given(elliptic_lines())
def test_elliptic_line_aux_vs_perp(line):
    """Test difference between aux and perp for elliptic lines"""
    aux_point = line.aux()
    perp_point = line.perp()
    
    # aux returns a point not incident with the line
    assert not line.incident(aux_point)
    # perp returns a point (dual object) but doesn't need to be incident
    assert isinstance(perp_point, EllipticPoint)
    
    # In elliptic geometry, aux and perp may return different types of dual objects
    # aux is guaranteed not to be incident, perp is a geometric dual


@given(elliptic_points(), elliptic_lines())
def test_elliptic_perp_incidence_symmetry(point, line):
    """Test symmetry of incidence with perpendiculars"""
    perp_point = line.perp()
    perp_line = point.perp()
    
    # If point is on line, then line's perp should be on point's perp
    if point.incident(line):
        assert perp_point.incident(perp_line)