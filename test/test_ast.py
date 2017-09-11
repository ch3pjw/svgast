from pytest import raises, fixture

from lxml import etree

from svgast.ast import Element, to_etree, ViewBox, Svg, Rect, Text
from svgast.units import mm


class MyElement(Element):
    pass


# Ultimately, whilst easy, as lot of these are just testing Python APIs


def test_attributes():
    e = MyElement(fooBar=3, gant='chart', viewBox=(1, 2, 3, 4))
    assert e.fooBar == 3
    assert e.gant == 'chart'
    assert isinstance(e.viewBox, ViewBox)
    with raises(AttributeError):
        e.bad


def test_children():
    c = MyElement(child='childy')
    children = c, 'non-element child'
    e = MyElement(*children, child='nope')
    assert tuple(e) == children
    assert e[0] is c


@fixture
def svg():
    class Tosh(Element):
        pass

    return Svg(
        Rect(
            x=0, y=0, width=mm(10), height=mm(10), fill='#bada55',
            cls='square'),
        Text('hello', Tosh(), 'world', x=0, y=mm(5)),
        viewBox=(0, 0, mm(10), mm(10)))


def test_serialisation(svg):
    string = (
        b'<svg version="1.1" viewBox="0 0 10mm 10mm" '
        b'xmlns="http://www.w3.org/2000/svg">\n'
        b'  <rect class="square" fill="#bada55" height="10mm" width="10mm" '
        b'x="0" y="0"/>\n'
        b'  <text x="0" y="5mm">hello<tosh/>world</text>\n'
        b'</svg>\n'
    )
    assert etree.tostring(to_etree(svg), pretty_print=True) == string
