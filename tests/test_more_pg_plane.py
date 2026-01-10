from projgeom.pg_object import PgLine, PgPoint
from projgeom.pg_plane import (
    check_axiom,
    check_axiom2,
    check_desargue,
    check_pappus,
    coincident,
    involution,
    persp,
    tri_dual,
)


def test_check_axiom() -> None:
    pt_p = PgPoint([1, 2, 3])
    pt_q = PgPoint([4, 5, 6])
    ln_l = PgLine([7, 8, 9])
    check_axiom(pt_p, pt_q, ln_l)


def test_check_axiom2() -> None:
    pt_p = PgPoint([1, 2, 3])
    pt_q = PgPoint([4, 5, 6])
    ln_l = PgLine([7, 8, 9])
    alpha = 2
    beta = 3
    check_axiom2(pt_p, pt_q, ln_l, alpha, beta)


def test_coincident() -> None:
    pt_a = PgPoint([1, 0, 0])
    pt_b = PgPoint([0, 1, 0])
    pt_c = PgPoint([1, 1, 0])
    assert coincident(pt_a, pt_b, pt_c)

    pt_d = PgPoint([1, 1, 1])
    assert not coincident(pt_a, pt_b, pt_d)


def test_check_pappus() -> None:
    pt_a = PgPoint([1, 0, 0])
    pt_b = PgPoint([0, 1, 0])
    pt_c = PgPoint([1, 1, 0])
    coline1 = [pt_a, pt_b, pt_c]

    pt_d = PgPoint([1, 0, 1])
    pt_e = PgPoint([0, 1, 1])
    pt_f = PgPoint([1, 1, 1])
    coline2 = [pt_d, pt_e, pt_f]

    assert not check_pappus(coline1, coline2)


def test_tri_dual() -> None:
    pt_a = PgPoint([1, 0, 0])
    pt_b = PgPoint([0, 1, 0])
    pt_c = PgPoint([0, 0, 1])
    triangle = [pt_a, pt_b, pt_c]
    duals = tri_dual(triangle)
    assert len(duals) == 3
    assert isinstance(duals[0], PgLine)


def test_persp() -> None:
    tri_1 = [PgPoint([1, 0, 0]), PgPoint([0, 1, 0]), PgPoint([0, 0, 1])]
    tri_2 = [PgPoint([1, 1, 1]), PgPoint([1, 2, 1]), PgPoint([2, 1, 1])]
    assert not persp(tri_1, tri_2)

    tri_3 = [PgPoint([2, 0, 0]), PgPoint([0, 2, 0]), PgPoint([0, 0, 2])]
    assert persp(tri_1, tri_3)


def test_check_desargue() -> None:
    tri_1 = [PgPoint([1, 0, 0]), PgPoint([0, 1, 0]), PgPoint([0, 0, 1])]
    tri_2 = [PgPoint([1, 1, 1]), PgPoint([1, 2, 1]), PgPoint([2, 1, 1])]
    assert check_desargue(tri_1, tri_2)

    tri_3 = [PgPoint([2, 0, 0]), PgPoint([0, 2, 0]), PgPoint([0, 0, 2])]
    assert check_desargue(tri_1, tri_3)


def test_involution() -> None:
    origin = PgPoint([0, 0, 1])
    mirror = PgLine([0, 1, 0])
    pt_p = PgPoint([1, 2, 1])
    pt_q = involution(origin, mirror, pt_p)
    assert involution(origin, mirror, pt_q) == pt_p
