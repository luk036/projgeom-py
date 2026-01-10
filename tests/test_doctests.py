import doctest

import projgeom.pg_plane


def test_doctests() -> None:
    assert doctest.testmod(projgeom.pg_plane).failed == 0
