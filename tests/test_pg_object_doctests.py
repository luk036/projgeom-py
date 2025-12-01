import doctest
import projgeom.pg_object


def test_doctests() -> None:
    assert doctest.testmod(projgeom.pg_object).failed == 0
