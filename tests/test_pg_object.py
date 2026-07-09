from projgeom.pg_object import PgLine, PgObject, PgPoint


def test_pg_object_invalid_coord_length() -> None:
    """PgObject rejects coordinates that are not length 3 (line 173)."""
    import pytest
    with pytest.raises(ValueError, match="three integers"):
        PgObject([1, 2])


def test_pg_object_eq_non_pgobject() -> None:
    """PgObject.__eq__ returns False for non-PgObject types (line 209)."""
    obj = PgObject([1, 2, 3])
    assert obj != "not a PgObject"
    assert obj != 42


def test_pg_object_dual_type() -> None:
    """PgObject.dual_type() returns PgLine (line 219)."""
    obj = PgObject([1, 2, 3])
    assert obj.dual_type() == PgLine


def test_pg_point_meet() -> None:
    pt_p = PgPoint([1, 2, 3])
    pt_q = PgPoint([4, 5, 6])
    ln_l = pt_p.meet(pt_q)
    assert isinstance(ln_l, PgLine)
    assert ln_l.coord == [-3, 6, -3]


def test_pg_point_dual() -> None:
    pt_p = PgPoint([1, 2, 3])
    ln_l = pt_p.aux()
    assert isinstance(ln_l, PgLine)
    assert not pt_p.incident(ln_l)


def test_pg_line_dual() -> None:
    ln_l = PgLine([1, 2, 3])
    pt_p = ln_l.aux()
    assert isinstance(pt_p, PgPoint)
    assert not ln_l.incident(pt_p)
