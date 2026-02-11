from projgeom.pg_object import PgLine, PgPoint
from projgeom.pg_plane import (
    Line,
    Point,
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
    pt_p: Point = PgPoint([1, 2, 3])  # type: ignore[assignment]
    pt_q: Point = PgPoint([4, 5, 6])  # type: ignore[assignment]
    ln_l: Line = PgLine([7, 8, 9])  # type: ignore[assignment]
    check_axiom(pt_p, pt_q, ln_l)


def test_check_axiom2() -> None:
    pt_p: Point = PgPoint([1, 2, 3])  # type: ignore[assignment]
    pt_q: Point = PgPoint([4, 5, 6])  # type: ignore[assignment]
    ln_l: Line = PgLine([7, 8, 9])  # type: ignore[assignment]
    alpha = 2
    beta = 3
    check_axiom2(pt_p, pt_q, ln_l, alpha, beta)


def test_coincident() -> None:
    pt_a: Point = PgPoint([1, 0, 0])  # type: ignore[assignment]
    pt_b: Point = PgPoint([0, 1, 0])  # type: ignore[assignment]
    pt_c: Point = PgPoint([1, 1, 0])  # type: ignore[assignment]
    assert coincident(pt_a, pt_b, pt_c)

    pt_d: Point = PgPoint([1, 1, 1])  # type: ignore[assignment]
    assert not coincident(pt_a, pt_b, pt_d)


def test_check_pappus() -> None:
    pt_a: Point = PgPoint([1, 0, 0])  # type: ignore[assignment]
    pt_b: Point = PgPoint([0, 1, 0])  # type: ignore[assignment]
    pt_c: Point = PgPoint([1, 1, 0])  # type: ignore[assignment]
    coline1: list[Point] = [pt_a, pt_b, pt_c]

    pt_d: Point = PgPoint([1, 0, 1])  # type: ignore[assignment]
    pt_e: Point = PgPoint([0, 1, 1])  # type: ignore[assignment]
    pt_f: Point = PgPoint([1, 1, 1])  # type: ignore[assignment]
    coline2: list[Point] = [pt_d, pt_e, pt_f]

    assert not check_pappus(coline1, coline2)


def test_tri_dual() -> None:
    pt_a: Point = PgPoint([1, 0, 0])  # type: ignore[assignment]
    pt_b: Point = PgPoint([0, 1, 0])  # type: ignore[assignment]
    pt_c: Point = PgPoint([0, 0, 1])  # type: ignore[assignment]
    triangle: list[Point] = [pt_a, pt_b, pt_c]
    duals = tri_dual(triangle)
    assert len(duals) == 3
    assert isinstance(duals[0], PgLine)


def test_persp() -> None:
    tri_1: list[Point] = [PgPoint([1, 0, 0]), PgPoint([0, 1, 0]), PgPoint([0, 0, 1])]  # type: ignore[list-item]
    tri_2: list[Point] = [PgPoint([1, 1, 1]), PgPoint([1, 2, 1]), PgPoint([2, 1, 1])]  # type: ignore[list-item]
    assert not persp(tri_1, tri_2)

    tri_3: list[Point] = [PgPoint([2, 0, 0]), PgPoint([0, 2, 0]), PgPoint([0, 0, 2])]  # type: ignore[list-item]
    assert persp(tri_1, tri_3)


def test_check_desargue() -> None:
    tri_1: list[Point] = [PgPoint([1, 0, 0]), PgPoint([0, 1, 0]), PgPoint([0, 0, 1])]  # type: ignore[list-item]
    tri_2: list[Point] = [PgPoint([1, 1, 1]), PgPoint([1, 2, 1]), PgPoint([2, 1, 1])]  # type: ignore[list-item]
    assert check_desargue(tri_1, tri_2)

    tri_3: list[Point] = [PgPoint([2, 0, 0]), PgPoint([0, 2, 0]), PgPoint([0, 0, 2])]  # type: ignore[list-item]
    assert check_desargue(tri_1, tri_3)


def test_involution() -> None:
    origin: Point = PgPoint([0, 0, 1])  # type: ignore[assignment]
    mirror: Point = PgLine([0, 1, 0])  # type: ignore[assignment]
    pt_p: Point = PgPoint([1, 2, 1])  # type: ignore[assignment]
    pt_q = involution(origin, mirror, pt_p)
    assert involution(origin, mirror, pt_q) == pt_p
