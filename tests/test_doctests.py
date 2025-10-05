import doctest
import projgeom.pg_plane

def test_doctests():
    assert doctest.testmod(projgeom.pg_plane).failed == 0
