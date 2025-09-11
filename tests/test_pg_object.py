import pytest

from projgeom.pg_object import PgLine, PgObject, PgPoint, cross, dot, plckr


def test_dot():
    assert dot([1, 2, 3], [4, 5, 6]) == 32
    assert dot([1, 2, 3], [4, 5, 6]) == dot([4, 5, 6], [1, 2, 3])

    assert dot([1, 0, 0], [0, 1, 0]) == 0


def test_cross():
    assert cross([1, 0, 0], [0, 1, 0]) == [0, 0, 1]
    assert cross([1, 2, 3], [4, 5, 6]) == [-3, 6, -3]
    assert cross([4, 5, 6], [1, 2, 3]) == [3, -6, 3]


def test_plckr():
    assert plckr(1, [1, 2, 3], 2, [4, 5, 6]) == [9, 12, 15]
    assert plckr(2, [1, 2, 3], 1, [4, 5, 6]) == [6, 9, 12]


def test_pg_object_constructor():
    pt_p = PgObject([3, 4, 5])
    assert pt_p.coord == [3, 4, 5]


def test_pg_object_repr():
    pt_p = PgObject([3, 4, 5])
    assert repr(pt_p) == "PgObject(3 : 4 : 5)"


def test_pg_object_str():
    pt_p = PgObject([3, 4, 5])
    assert str(pt_p) == "(3 : 4 : 5)"


def test_pg_object_eq():
    pt_p = PgObject([3, 4, 5])
    pt_q = PgObject([30, 40, 50])
    pt_r = PgObject([1, 2, 3])
    assert pt_p == pt_q
    assert pt_p != pt_r


def test_pg_object_dot():
    pt_p = PgObject([3, 4, 5])
    ln_l = PgObject([30, 40, 50])
    assert pt_p.dot(ln_l) == 500


def test_pg_object_parametrize():
    pt_p = PgObject([1, 2, 3])
    pt_q = PgObject([4, 5, 6])
    assert pt_p.parametrize(1, pt_q, 2) == PgObject([9, 12, 15])


def test_pg_object_incident():
    pt_p = PgObject([1, 2, 3])
    ln_l = PgObject([-3, 6, -3])
    assert pt_p.incident(ln_l)


def test_pg_object_meet():
    pt_p = PgPoint([1, 2, 3])
    pt_q = PgPoint([4, 5, 6])
    ln_l = pt_p.meet(pt_q)
    assert isinstance(ln_l, PgLine)
    assert ln_l.coord == [-3, 6, -3]


def test_pg_point_dual():
    pt_p = PgPoint([1, 2, 3])
    ln_l = pt_p.aux()
    assert isinstance(ln_l, PgLine)
    assert not pt_p.incident(ln_l)


def test_pg_line_dual():
    ln_l = PgLine([1, 2, 3])
    pt_p = ln_l.aux()
    assert isinstance(pt_p, PgPoint)
    assert not ln_l.incident(pt_p)


def test_pg_object_invalid_coord():
    with pytest.raises(ValueError):
        PgObject([1, 2])
