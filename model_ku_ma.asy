import util;
import path_defs;

unitsize(1cm);

guide ka = path_ka();
guide base = subpath(ka, 0, arctime(ka, arclength(ka) - 0.5));
guide ma = path_ma();
pair z1, z2, z3, z4, z5;

z1 = arcpoint(reverse(base), 0);
z4 = arcpoint(reverse(base), 2);
z3 = z1 + 2 * dir(135);
z2 = z4 - 2.2 * dir(z3 - z1) * I;

guide ku = base .. z3 .. z4;
z5 = arcpoint(ku, 8.0);
ku = ku{E} .. {dir(ma, 0)}z5;

draw(ku);
draw(shift(relpoint(ku, 1)) * ma);
draw(ka, red);
dot(ku);
