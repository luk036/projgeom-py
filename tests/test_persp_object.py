from projgeom.persp_object import PerspPoint, PerspLine, I_RE, I_IM, L_INF


def test_persp_point():
    pt_p = PerspPoint([1, 2, 3])
    ln_l = pt_p.dual()([4, 5, 6])
    assert isinstance(ln_l, PerspLine)
    assert pt_p.perp() == L_INF
    pt_q = PerspPoint([4, 5, 6])
    midpoint = pt_p.midpoint(pt_q)
    assert isinstance(midpoint, PerspPoint)


def test_persp_line():
    ln_l = PerspLine([1, 2, 3])
    pt_p = ln_l.dual()([4, 5, 6])
    assert isinstance(pt_p, PerspPoint)
    perp = ln_l.perp()
    assert isinstance(perp, PerspPoint)
    ln_m = PerspLine([4, 5, 6])
    assert not ln_l.is_parallel(ln_m)


def test_constants():
    assert I_RE.coord == [0, 1, 1]
    assert I_IM.coord == [1, 0, 0]
    assert L_INF.coord == [0, -1, 1]
