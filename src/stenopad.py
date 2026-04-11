#!/usr/bin/env python3

from shorthand_string import String as ShorthandString
from shorthand_waseda import tdict
import argparse
import os
import subprocess


def gen_svg(input_, output, method, to_animate=False, speed=20):
    with open(input_, "r", encoding="utf8") as f:
        in_text = f.read()

    s = ShorthandString(in_text, tdict[method])
    svg, _ = s.create_svg(to_animate=to_animate, speed_mm_per_s=speed)
    with open(f"{output}", "w", encoding="utf8") as f:
        f.write(svg)

def gen_png(input_, output, method):
    with open(input_, "r", encoding="utf8") as f:
        in_text = f.read()
    s = ShorthandString(in_text, tdict[method])
    svg, _ = s.create_svg()
    with open("tmp.svg", "w", encoding="utf8") as f:
        f.write(svg)

    cmd = ["rsvg-convert", "-o", output, "tmp.svg"]
    subprocess.run(cmd)
    os.remove("tmp.svg")

def gen_mp4(input_, output, method, fps, speed):
    base, ext = os.path.splitext(input_)
    keyframe_pattern = f"{base}_%05d.svg"
    with open(input_, "r", encoding="utf8") as f:
        in_text = f.read()
    s = ShorthandString(in_text, tdict[method])
    svgs = s.create_key_frames(speed_mm_per_s=speed)

    frame_files = [keyframe_pattern % n for n in range(1, len(svgs))]
    for frame_file, svg in zip(frame_files, svgs):
        with open(frame_file, "w", encoding="utf8") as f:
            f.write(svg)
    cmd = ["ffmpeg", "-y", "-r", str(fps), "-i", keyframe_pattern, "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p", output]
    subprocess.run(cmd)
    for frame_file in frame_files:
        os.remove(frame_file)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output", nargs="?")
    parser.add_argument("-m", "--method", type=str, default="waseda", choices=["waseda"], help="frames per second")
    parser.add_argument("-r", "--fps", type=float, default=24.0, help="frames per second")
    parser.add_argument("-s", "--speed", type=float, default=24.0, help="drawing speed")
    parser.add_argument("-f", "--format", choices=["svg", "smil", "png", "mp4"], default="svg", help="output format")

    args = parser.parse_args()
    base, _ = os.path.splitext(args.input)
    to_animate = args.format == "smil"
    if args.output is None:
        if args.format == "smil":
            args.output = f"{base}_animated.svg"
        else:
            args.output = f"{base}.{args.format}"
    print(f"{args.input} => {args.output}")
    return args

def main():
    args = parse_args()
    if args.format == "svg":
        gen_svg(args.input, args.output, args.method)
    elif args.format == "smil":
        gen_svg(args.input, args.output, args.method, to_animate=True, speed=args.speed)
    elif args.format == "png":
        gen_png(args.input, args.output, args.method)
    elif args.format == "mp4":
        gen_mp4(args.input, args.output, args.method, args.fps, args.speed)
    else:
        pass

if __name__ == "__main__":
    main()
