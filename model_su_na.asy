import util;
import path_defs;

unitsize(1cm);
path su = path_su_na();
path na = shift(relpoint(su, 1)) * path_na();

real r = radius(na, 0);
pair c = dir(na, 0) * I * r + point(na, 0);

draw(shift(c) * scale(r) * unitcircle, red);
draw(c -- point(na, 0));
draw(c -- point(su, 3));
dot(c);

draw(point(su, 1) -- point(su, 3));
draw(point(su, 2) -- point(su, 4));
draw(su);
draw(na);
dot(su);
dot(na);
label("C", c, W);
