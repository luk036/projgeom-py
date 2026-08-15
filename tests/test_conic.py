from fractions import Fraction

from projgeom.conic import Conic, ConicType
from projgeom.pg_object import PgLine, PgPoint


def test_conic_type_ellipse() -> None:
    assert Conic.unit_circle().conic_type() is ConicType.ELLIPSE


def test_conic_type_parabola() -> None:
    assert Conic.parabola(Fraction(1, 1)).conic_type() is ConicType.PARABOLA


def test_conic_type_hyperbola() -> None:
    """Negative discriminant yields HYPERBOLA (line 289)."""
    zero = Fraction(0, 1)
    c = Conic(
        [
            [Fraction(-1, 1), zero, zero],
            [zero, Fraction(1, 1), zero],
            [zero, zero, Fraction(1, 1)],
        ]
    )
    assert c.discriminant() < Fraction(0, 1)
    assert c.conic_type() is ConicType.HYPERBOLA


def test_conic_contains() -> None:
    c = Conic.unit_circle()
    assert c.contains(PgPoint([1, 0, 1]))
    assert not c.contains(PgPoint([2, 0, 1]))


def test_conic_polar_tangent() -> None:
    c = Conic.unit_circle()
    assert c.polar(PgPoint([1, 0, 1])) == PgLine([1, 0, -1])
    assert c.tangent(PgPoint([1, 0, 1])) == PgLine([1, 0, -1])


def test_conic_pole_intersect() -> None:
    c = Conic.unit_circle()
    pole = c.pole(PgLine([1, 0, -1]))
    assert isinstance(pole, PgPoint)
    assert c.intersect(PgLine([1, 0, 0])) == []


def test_conic_circle() -> None:
    c = Conic.circle(0, 0, 1)
    assert c.contains(PgPoint([1, 0, 1]))
