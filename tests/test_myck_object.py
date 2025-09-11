from projgeom.myck_object import MyCKLine, MyCKPoint


def test_myck_point():
    pt_p = MyCKPoint([1, 2, 3])
    ln_l = pt_p.dual()([4, 5, 6])
    assert isinstance(ln_l, MyCKLine)
    assert pt_p.perp().coord == [-2, 2, -6]


def test_myck_line():
    ln_l = MyCKLine([1, 2, 3])
    pt_p = ln_l.dual()([4, 5, 6])
    assert isinstance(pt_p, MyCKPoint)
    assert ln_l.perp().coord == [-1, 4, -3]
