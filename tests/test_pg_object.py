from projgeom.pg_object import PgLine, PgPoint


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
