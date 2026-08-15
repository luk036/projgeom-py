from fractions import Fraction

import pytest

from projgeom.pg_object import PgPoint
from projgeom.transform import (
    Transform,
    projective_transform,
    rotate_point,
    scale_point,
    translate_point,
)


def test_identity() -> None:
    t = Transform.identity()
    p = PgPoint([1, 2, 3])
    assert t.apply_point(p) == p
    assert t.matrix[0][0] == Fraction(1, 1)


def test_translation() -> None:
    t = Transform.translation(5, 3)
    assert t.apply_point(PgPoint([1, 2, 1])) == PgPoint([6, 5, 1])


def test_rotation() -> None:
    t = Transform.rotation(Fraction(0, 1), Fraction(1, 1))
    assert t.apply_point(PgPoint([1, 0, 1])) == PgPoint([0, 1, 1])


def test_scaling() -> None:
    t = Transform.scaling(Fraction(2, 1), Fraction(3, 1))
    assert t.apply_point(PgPoint([1, 1, 1])) == PgPoint([2, 3, 1])


def test_shear() -> None:
    t = Transform.shear(Fraction(1, 1), Fraction(0, 1))
    assert t.apply_point(PgPoint([1, 1, 1])) == PgPoint([2, 1, 1])


def test_compose() -> None:
    t1 = Transform.translation(1, 0)
    t2 = Transform.translation(0, 2)
    assert t1.apply_point(t2.apply_point(PgPoint([1, 1, 1]))) == PgPoint([2, 3, 1])


def test_inverse() -> None:
    t = Transform.translation(5, 3)
    inv = t.inverse()
    p = PgPoint([1, 2, 1])
    assert inv.apply_point(t.apply_point(p)) == p


def test_inverse_singular_raises() -> None:
    """Inverting a singular matrix raises ZeroDivisionError (line 312)."""
    zero = Fraction(0, 1)
    singular = Transform([[zero, zero, zero], [zero, zero, zero], [zero, zero, zero]])
    with pytest.raises(ZeroDivisionError):
        singular.inverse()


def test_eq() -> None:
    assert Transform.identity() == Transform.identity()
    assert Transform.identity() != Transform.translation(1, 0)


def test_eq_non_transform() -> None:
    """__eq__ with a non-Transform returns NotImplemented (line 338)."""
    assert (Transform.identity() == "not a transform") is False


def test_rotate_point() -> None:
    p = rotate_point(PgPoint([1, 0, 1]), Fraction(0, 1), Fraction(1, 1))
    assert p == PgPoint([0, 1, 1])


def test_translate_point() -> None:
    assert translate_point(PgPoint([1, 2, 1]), 3, 4) == PgPoint([4, 6, 1])


def test_scale_point() -> None:
    assert scale_point(PgPoint([2, 3, 1]), Fraction(2, 1), Fraction(3, 1)) == PgPoint(
        [4, 9, 1]
    )


def test_projective_transform() -> None:
    src = [
        PgPoint([0, 0, 1]),
        PgPoint([1, 0, 1]),
        PgPoint([0, 1, 1]),
        PgPoint([1, 1, 1]),
    ]
    dst = [
        PgPoint([0, 0, 1]),
        PgPoint([2, 0, 1]),
        PgPoint([0, 2, 1]),
        PgPoint([2, 2, 1]),
    ]
    t = projective_transform(src, dst)
    assert t == Transform.identity()
