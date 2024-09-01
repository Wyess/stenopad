import util;
import glyph;
import path_defs;

unitsize(1cm);

guide sa = (0, 0){dir(30)} .. {N}dir(45) * 8;
guide base = subpath(sa, 0, 0.75);

pair ze = arcpoint(reverse(base), 1.5);
pair z2 = ze + dir(120) * 2;
real h = relpoint(sa, 1).y;
pair top = (ze.x, h);
guide su = base .. {W}top .. {dir(-60 - 10)}z2 .. {dir(-60 + 10)}ze;

draw(sa, blue);
draw(base);
draw(su);
dot(su, red + linewidth(5));
