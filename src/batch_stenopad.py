#!/usr/bin/env python3

from shorthand_string import String as ShorthandString
import tomli
from shorthand_waseda import tdict

def main(method="waseda", to_animate=False, speed_mm_per_s=20, to_generate_keyframe=False):
    with open('input.toml', "rb") as f:
        in_text = tomli.load(f)
    for filename in in_text:
        s = ShorthandString(in_text[filename], tdict[method])
        if to_generate_keyframe:
            svgs = s.create_key_frames(speed_mm_per_s=24)
            for n, svg in enumerate(svgs, start=1):
                with open(f"{filename}_{n:05}.svg", "w", encoding="utf8") as f:
                    f.write(svg)
        else:
            svg, _ = s.create_svg(to_animate, speed_mm_per_s)
            with open(f"{filename}.svg", "w", encoding="utf8") as f:
                f.write(svg)
            print(in_text[filename])

if __name__ == '__main__':
    main(to_animate=False, to_generate_keyframe=True)
