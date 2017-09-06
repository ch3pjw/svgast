import sys
from collections import namedtuple
from functools import wraps

from lxml import etree

from .units import to_length, str_number

_module = sys.modules[__name__]


class Element:
    def __init__(self, *children, **attributes):
        self._children = children
        self._attributes = attributes
        view_box = attributes.get('viewBox')
        if view_box:
            attributes['viewBox'] = ViewBox(*view_box)

    def __len__(self):
        return len(self._children)

    def __iter__(self):
        return iter(self._children)

    def __getitem__(self, idx):
        return self._children[idx]

    def __getattr__(self, name):
        return self._attributes[name]

    @property
    def _tag(self):
        n = type(self).__name__
        return n[0].lower() + n[1:]

    @property
    def _etree(self):
        attributes = dict(self._attributes)
        cls = attributes.pop('cls', None)
        if cls:
            attributes['class'] = cls
        e = etree.Element(
            self._tag, attrib={
                k.replace('_', '-'): str(v) for k, v in attributes.items()
            }
        )
        last_child_etree_elem = None
        for c in self._children:
            if isinstance(c, str):
                if last_child_etree_elem is None:
                    e.text = c
                else:
                    last_child_etree_elem.tail = c
            else:
                last_child_etree_elem = c._etree
                e.append(last_child_etree_elem)
        return e


def to_etree(element):
    return element._etree


def write(svg_element, file_or_path):
    if not isinstance(svg_element, Svg):
        raise TypeError(
            'Must use an Svg element as document root, got {!r}'.format(
                type(svg_element)))
    do_write = lambda f: etree.ElementTree(to_etree(svg_element)).write(
        f, pretty_print=True, xml_declaration=True, encoding='utf-8')
    if isinstance(file_or_path, str):
        with open(file_or_path, 'wb') as f:
            do_write(f)
    else:
        do_write(file_or_path)


class Circle(Element):
    pass


class Defs(Element):
    pass


class G(Element):
    pass


class Path(Element):
    def __init__(self, *children, d, **attributes):
        super().__init__(*children, d=PathD(*d), **attributes)


class Rect(Element):
    pass


class Style(Element):
    pass


class Svg(Element):
    def __init__(self, *children, **attributes):
        super().__init__(
            *children,
            xmlns='http://www.w3.org/2000/svg',
            version='1.1',
            **attributes)


class Symbol(Element):
    pass


class Text(Element):
    def __init__(self, *children, dx=None, **attributes):
        if dx:
            attributes['dx'] = Kern(*dx)
        super().__init__(*children, **attributes)


class Use(Element):
    pass


class _PathInstructionMeta(type):
    def __new__(metacls, name, bases, cls_dict):
        cls = super().__new__(
            metacls, name,
            (
                namedtuple(name, cls_dict.get('_fields', ()) + ('rel',)),
            ) + bases,
            cls_dict)
        if cls._letter:
            setattr(
                _module,
                cls._letter.lower(),
                wraps(cls)(lambda *a: cls(*a, rel=True)))
            setattr(
                _module,
                cls._letter.upper(),
                wraps(cls)(lambda *a: cls(*a, rel=False)))
        return cls


class PathInstruction(metaclass=_PathInstructionMeta):
    _letter = None
    _fields = ()

    @property
    def letter(self):
        return self._letter.lower() if self.rel else self._letter.upper()

    @property
    def args(self):
        return self[:-1]

    @property
    def rel(self):
        return self[-1]

    def __str__(self):
        return '{} {}'.format(
            self.letter,
            ' '.join(map(str_number, self.args)))

    def __repr__(self):
        return '{}({})'.format(
            self.letter,
            ', '.join(map(str_number, self.args)))


class MoveTo(PathInstruction):
    '''
    FIXME: docstring
    '''
    _letter = 'm'
    _fields = 'x', 'y'


class LineTo(PathInstruction):
    '''
    FIXME: docstring
    '''
    _letter = 'l'
    _fields = 'x', 'y'


class HorizontalLineTo(PathInstruction):
    '''
    FIXME: docstring
    '''
    _letter = 'h'
    _fields = 'x',


class VerticalLineTo(PathInstruction):
    '''
    FIXME: docstring
    '''
    _letter = 'v'
    _fields = 'y',


class ArcTo(PathInstruction):
    '''
    FIXME: docstring
    '''
    _letter = 'a'
    _fields = 'rx', 'ry', 'x_axis_rotate', 'large', 'sweep', 'x', 'y'


class ClosePath(PathInstruction):
    _letter = 'z'

    def __str__(self):
        return self.letter


class PathD(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __str__(self):
        return '  '.join(map(str, self))


class ViewBox(namedtuple('ViewBox', ('ox', 'oy', 'width', 'height'))):
    def __new__(cls, *args):
        return super().__new__(cls, *map(to_length, args))

    def __str__(self):
        return ' '.join(map(str, self))


class Kern(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, *map(to_length, args))

    def __str__(self):
        return ' '.join(map(str, self))
