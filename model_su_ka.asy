import util;
import path_defs;

unitsize(1cm);

guide sa = path_sa();
guide su = path_su_ka();
draw(sa, blue);
draw(su);
dot(su, red);
draw(point(su, 1) -- point(su, 3));
draw(point(su, 2) -- point(su, 4));
