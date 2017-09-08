from numbers import Complex


class Length:
    __slots__ = 'px',

    unit = NotImplemented
    _px_per_unit = NotImplemented

    def __init__(self, length):
        if isinstance(length, Length):
            self.px = length.px
        elif isinstance(length, Complex):
            # Any numerical value:
            self.px = length * self._px_per_unit
        else:
            raise TypeError(
                'Expected Length or number, got {!r}'.format(type(length)))

    def __str__(self):
        return '{}{}'.format(
            str_number(self.px / self._px_per_unit),
            self.unit)


class user(Length):
    unit = ''
    _px_per_unit = 1


class px(Length):
    unit = 'px'
    _px_per_unit = 1


class pt(Length):
    unit = 'pt'
    _px_per_unit = 1.25


class pc(Length):
    unit = 'pc'
    _px_per_unit = 15


class mm(Length):
    unit = 'mm'
    _px_per_unit = 3.543307


class cm(Length):
    unit = 'cm'
    _px_per_unit = 35.43307


class in_(Length):
    unit = 'in'
    _px_per_unit = 90


def to_length(x):
    if isinstance(x, Length):
        return x
    else:
        return user(x)


def str_number(n):
    return '{:f}'.format(n).rstrip('0').rstrip('.')
