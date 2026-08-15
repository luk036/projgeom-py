from projgeom.pg_object import PgPoint


def test_geometry_name() -> None:
    """Geometry.geometry_name() abstract body executes (geometry.py line 27)."""
    assert PgPoint([1, 2, 3]).geometry_name() is None
