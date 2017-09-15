from collections import namedtuple
from numbers import Complex


class Axis:
    __slots__ = 'n',

    def __init__(self, n):
        self.n = n

    def _guard_axis(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                "Can't mix axis types - expected {} got {}".format(
                    type(self).__name__, type(other).__name__))

    def __add__(self, other):
        self._guard_axis(other)
        return type(self)(self.n + other.n)

    def __sub__(self, other):
        self._guard_axis(other)
        return type(self)(self.n - other.n)

    def _guard_scalar(self, other):
        if not isinstance(other, Complex):
            raise TypeError('Need regular number')

    def __mult__(self, other):
        self._guard_scalar(other)
        return type(self)(self.n * other)

    def __rmult__(self, other):
        self._guard_scalar(other)
        return type(self)(other * self.n)

    def __div__(self, other):
        self._guard_scalar(other)
        return type(self)(self.n / other)

    def __rdiv__(self, other):
        self._guard_scalar(other)
        return type(self)(other / self.n)


class Horizontal(Axis):
    pass


class Vertical(Axis):
    pass


class BoundingBox(namedtuple('BoundingBox', ('l', 't', 'w', 'h'))):
    def __new__(cls, l, t, w, h):
        return super().__new__(
            cls,
            Horizontal(l),
            Vertical(t),
            Horizontal(w),
            Vertical(h))

    @property
    def r(self):
        return self.l + self.w

    @property
    def b(self):
        return self.t + self.h

    @property
    def hm(self):
        '''
        Horizontal midpoint
        '''
        return self.hf(0.5)

    @property
    def vm(self):
        '''
        Vertical midpoint
        '''
        return self.vf(0.5)

    def hpc(self, percentage):
        '''
        Horizontal coord as percentage of bounding box
        '''
        return self.hf(percentage / 100)

    def vpc(self, percentage):
        '''
        Vertical coord as percentage of bounding box
        '''
        return self.vf(percentage / 100)

    def hf(self, fraction):
        '''
        Horizontal coord as fraction of bounding box
        '''
        return self.l + (self.w * fraction)

    def vf(self, fraction):
        '''
        Vertical coord as fraction of bounding box
        '''
        return self.t + (self.h * fraction)
