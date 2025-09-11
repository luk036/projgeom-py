from projgeom.hyp_object import HyperbolicLine, HyperbolicPoint


def test_hyperbolic_point():
    pt_p = HyperbolicPoint([1, 2, 3])
    ln_l = pt_p.dual()([4, 5, 6])
    assert isinstance(ln_l, HyperbolicLine)
    assert pt_p.perp().coord == [1, 2, -3]


def test_hyperbolic_line():
    ln_l = HyperbolicLine([1, 2, 3])
    pt_p = ln_l.dual()([4, 5, 6])
    assert isinstance(pt_p, HyperbolicPoint)
    assert ln_l.perp().coord == [1, 2, -3]
