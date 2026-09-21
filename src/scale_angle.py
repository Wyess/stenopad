#!/usr/bin/env python3

from math import radians, degrees
from cmath import rect, phase

def scale_angle(sx, sy, a):
    dv = rect(1, radians(a))
    z = complex(dv.real * sx, dv.imag * sy)
    return degrees(phase(z))

if __name__ == '__main__':
    assert scale_angle(1, -1, -135) == 135
