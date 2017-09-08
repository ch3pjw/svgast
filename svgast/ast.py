import sys
from collections import namedtuple, OrderedDict
from functools import partial, wraps

from lxml import etree
from pyrsistent import PClass, field
from pyrsistent._pclass import PClassMeta

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


class OrderedPClassMeta(PClassMeta):
    def __init__(cls, name, bases, cls_dict):
        super().__init__(name, bases, cls_dict)

    def __prepare__(name, bases, **kwargs):
        return OrderedDict()


class ArgsPClass(PClass, metaclass=OrderedPClassMeta):
    def __new__(cls, *args, **kwargs):
        kwargs.update(zip(cls._fields(), args))
        return super().__new__(cls, **kwargs)

    @classmethod
    def _fields(cls):
        return cls.__slots__[1:]


class PathInstruction(ArgsPClass):
    rel = field(mandatory=True)
    _letter = None

    @classmethod
    def _fields(cls):
        print(cls.__slots__)
        return cls.__slots__[2:]  # Exlude 'rel' from *args

    @property
    def letter(self):
        return self._letter.lower() if self.rel else self._letter.upper()

    @property
    def _args(self):
        return tuple(getattr(self, f) for f in self._fields())

    def __str__(self):
        arg_string = ' '.join(map(str_number, self._args))
        if arg_string:
            return '{} {}'.format(self.letter, arg_string)
        else:
            return self.letter


class MoveTo(PathInstruction):
    _letter = 'm'
    x = field(mandatory=True)
    y = field(mandatory=True)


class LineTo(PathInstruction):
    _letter = 'l'
    x = field(mandatory=True)
    y = field(mandatory=True)


class HorizontalLineTo(PathInstruction):
    _letter = 'h'
    x = field(mandatory=True)


class VerticalLineTo(PathInstruction):
    _letter = 'v'
    y = field(mandatory=True)


class ArcTo(PathInstruction):
    _letter = 'a'
    rx = field(mandatory=True)
    ry = field(mandatory=True)
    x_axis_rotation = field(mandatory=True)
    large = field(mandatory=True)
    sweep = field(mandatory=True)
    x = field(mandatory=True)
    y = field(mandatory=True)


class ClosePath(PathInstruction):
    _letter = 'z'


for instruction in (
        MoveTo, LineTo, HorizontalLineTo, VerticalLineTo, ArcTo, ClosePath):
    for rel, str_f in ((True, str.lower), (False, str.upper)):
        setattr(
            _module,
            str_f(instruction._letter),
            wraps(instruction)(partial(instruction, rel=rel)))


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
