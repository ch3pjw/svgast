from pytest import raises

from svgast.units import mm, cm, in_, px, pt, pc, user, to_length


def test_bad_type():
    with raises(TypeError):
        mm('hello')


def test_str():
    assert str(mm(42)) == '42mm'
    assert str(user(42)) == '42'


def test_eq():
    assert in_(1) == 90
    assert px(42) == user(42)
    assert mm(10) == cm(1)


def test_neq():
    assert mm(10) != px(10)


def test_abs():
    assert abs(pc(1)) == 15


def test_add_same_type():
    result = mm(23) + mm(19)
    assert result == mm(42)
    assert isinstance(result, mm)


def test_add_different_type():
    result = in_(2) + px(-138)
    assert result == px(42)
    assert isinstance(result, user)


def test_add_unitless():
    result = in_(2) + 90
    assert result == in_(3)
    assert isinstance(result, user)


def test_radd_unitless():
    result = 90 + in_(2)
    assert result == in_(3)
    assert isinstance(result, user)


def test_sub_same_type():
    result = in_(84) - in_(42)
    assert result == in_(42)
    assert isinstance(result, in_)


def test_sub_different_type():
    result = in_(1) - px(48)
    assert result == user(42)
    assert isinstance(result, user)


def test_sub_unitless():
    result = pc(3) - 3
    assert result == 42
    assert isinstance(result, user)


def test_rsub_unitless():
    result = 222 - in_(2)
    assert result == 42
    assert isinstance(result, user)


def test_mul():
    for a, b in [(1.5, mm(30)), (mm(30), 1.5)]:
        result = a * b
        assert result == mm(45)
        assert isinstance(result, mm)
    with raises(TypeError):
        mm(30) * mm(12)
    with raises(TypeError):
        'hello' * mm(30)


def test_div():
    result = pt(8) / 2
    assert result == px(5)
    assert isinstance(result, pt)
    result = mm(30) / cm(3)
    assert result == 1
    assert isinstance(result, user)
    with raises(TypeError):
        3 / mm(30)


def test_neg():
    assert -mm(30) == mm(-30)


def test_to_length():
    l = mm(30)
    assert to_length(l) is l
    l = to_length(90)
    assert l == in_(1)
    assert isinstance(l, user)
