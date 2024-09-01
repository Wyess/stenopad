import util;
import path_defs;

unitsize(1cm);
path su = path_su();

draw(point(su, 1) -- point(su, 3));
draw(point(su, 2) -- point(su, 4));
draw(path_sa(), red);
draw(su);
dot(su);

pair[] p;
label('$P_{1}$', point(su, 1), align = E);
label('$P_{2}$', point(su, 2), align = NE);
label('$P_{3}$', point(su, 3), align = NW);
label('$P_{4}$', point(su, 4), align = SE);
