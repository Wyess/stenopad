#!/usr/bin/env python3

from decimal import Decimal, ROUND_HALF_UP
import sys
from svgpathtools import parse_path
import textwrap

def main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            try:
                print(parse_path_d(arg, format="toml"))
            except:
                pass
    else:
        #lines = [line.rstrip() for line in sys.stdin.readlines()]
        line = sys.stdin.readline().rstrip()
        try:
            print(parse_path_d(line, format="toml"))
        except:
            pass

def dround(val, fmt='0.001'):
    return Decimal(val).quantize(Decimal(fmt), rounding=ROUND_HALF_UP)

def parse_path_d(d, format="json"):
    path = parse_path(d)

    length = dround(path.length())

    startX = dround(path.start.real)
    startY = dround(path.start.imag)

    endX = dround(path.end.real)
    endY = dround(path.end.imag)

    bbox = path.bbox()
    minX = dround(bbox[0])
    maxX = dround(bbox[1])
    minY = dround(bbox[2])
    maxY = dround(bbox[3])

    if format == "json":
        return f'{{"d": "{d}", "length": {length}, "startX": {startX}, "startY": {startY}, "endX": {endX}, "endY": {endY}, "minX": {minX}, "maxX": {maxX}, "minY": {minY}, "maxY": {maxY}}}'
    elif format == "toml":
        return textwrap.dedent(f"""
            [[]]
            name = ""
            key = "default"
            left = {minX}
            right = {maxX}
            top = {minY}
            bottom = {maxY}
            dx = {endX}
            dy = {endY}
            length = {length}
            ascent = {dround((minY - maxY) / 2)}
            path = "{d}"
            """)[1:-1]
    else:
        return {"d": d, "length": length, "startX": startX, "startY": startY, "endX": endX, "endY": endY, "minX": minX, "maxX": maxX, "minY": minY, "maxY": maxY}

if __name__ == "__main__":
    main()
