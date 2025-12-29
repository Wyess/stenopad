class Point():
    def __init__(self, x, y, is_relative=False, to_update_pos=True):
        self._x = x
        self._y = y
        self._is_relative = is_relative
        self._to_update_pos = to_update_pos 

    def __iter__(self):
        yield self._x
        yield self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def is_relative(self):
        return self._is_relative

    @property
    def to_update_pos(self):
        return self._to_update_pos

    def __add__(self, other):
        if isinstance(other, tuple):
            assert(len(other) == 2)
            return Point(self._x + other[0], self._y + other[1])
        elif isinstance(other, complex):
            return Point(self._x + other.real, self._y + other.imag)
        elif isinstance(other, Point):
            return Point(self._x + other.x, self._y + other.y, to_update_pos=self._to_update_pos and other.to_update_pos)

    def __sub__(self, other):
        if isinstance(other, tuple):
            assert(len(other) == 2)
            return Point(self._x - other[0], self._y - other[1])
        elif isinstance(other, complex):
            return Point(self._x - other.real, self._y - other.imag)
        elif isinstance(other, Point):
            return Point(self._x - other.x, self._y - other.y)

    def __mul__(self, other):
        if type(other) in (int, float):
            return Point(self._x * other, self._y * other)

    def __truediv__(self, other):
        if type(other) in (int, float):
            assert(other != 0)
            return Point(self._x / other, self._y / other)

    def __complex__(self):
        return self._x + self._y * 1j

    def __pos__(self):
        return Point(self._x, self._y, is_relative=True)

    def __neg__(self):
        return Point(-self._x, -self._y)

    def __str__(self):
        return "%s(%g, %g)" % ("+" if self._is_relative else "", self._x, self._y)

    def __repr__(self):
        return "%sPoint(%g, %g)" % ("+" if self._is_relative else "", self._x, self._y)
