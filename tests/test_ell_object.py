from projgeom.ell_object import EllipticLine, EllipticPoint


def test_elliptic_point():
    pt_p = EllipticPoint([1, 2, 3])
    ln_l = pt_p.dual_type()([4, 5, 6])
    assert isinstance(ln_l, EllipticLine)
    assert pt_p.perp().coord == [1, 2, 3]


def test_elliptic_line():
    ln_l = EllipticLine([1, 2, 3])
    pt_p = ln_l.dual_type()([4, 5, 6])
    assert isinstance(pt_p, EllipticPoint)
    assert ln_l.perp().coord == [1, 2, 3]
