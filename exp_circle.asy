unitsize(1cm);

real orient(path p, real t0 = 0, real t1 = 0.5, real t2 = 1) {
    if (straight(subpath(p, t0, t1), 0)) {
        return 0;
    } else {
        return orient(point(p, t0), point(p, t1), point(p, t2));
    }
}

guide append_circle(
    guide base_path,
    guide next_path,
    real cut_time,
    real end_length,
    real r34,
    real r24,
    int cross_angle = 90
) {
    pair z1, z2, z3, z4;
    guide g = subpath(base_path, 0, cut_time);
    real ori = orient(g);
    real ori_next = orient(next_path);

    z1 = relpoint(g, 1);
    z4 = arcpoint(reverse(g), end_length);

    if (ori > 0) {
        if (ori_next > 0) {
            // Left to left
            z3 = z4 - scale(r34) * rotate(-10) * dir(next_path, 0);
            z2 = z4 - scale(r24) * rotate(cross_angle) * dir(z3 - z1);
            g = g .. z2 .. {rotate(-20) * dir(next_path, 0)}z3 .. shift(z4) * next_path;
        } else if (ori_next < 0) {
            // Left to right
        } else {
            // Left to straight
            z3 = z4 - scale(r34) * dir(next_path, 0);
            z2 = z4 - scale(r24) * rotate(cross_angle) * dir(z3 - z1);
            g = g .. z2 .. {dir(next_path, 0)}z3 -- shift(z4) * next_path;
        }
    } else if (ori < 0) {
        if (ori_next > 0) {
            // Right to left
        } else if (ori_next < 0) {
            // Right to right
        } else {
            // Right to straight
        }
    } else {
        if (ori_next > 0) {
            // Straight to left
        } else if (ori_next < 0) {
            // Straight to right
        } else {
            // Straight to straight
        }
    }


    //g = g .. z2 .. {rotate(-10) * dir(next_path, 0)}z3 .. shift(z4) * next_path;
    return subpath(g, 0, length(g) - length(next_path));
}

guide sa = (0, 0){dir(30)} .. {dir(90)}(dir(45) * 8);

guide sa_next = (0, 0){dir(-45)} .. {dir(45)}(2, 0);
guide su = append_circle(sa, sa_next, 0.85, 2, r34 = 2, r24 = 3, 90);

guide ka = (0, 0) -- 8E;
guide x_su_ka = append_circle(sa, ka, 0.93, 2, r34 = 1.5, r24 = 2.3, 90);

guide u = (0, 0) -- 4S;
guide x_su_u = append_circle(sa, u, 0.8, 3, r34 = 3, r24 = 4, 90);

draw(su);
dot(su);

draw(x_su_ka);
dot(x_su_ka);

draw(x_su_u);
dot(x_su_u);

draw(sa, red);
//draw(point(su, 1) -- point(su, 3));
//draw(point(su, 2) -- point(su, 4));
unitsize(1cm);

real orient(path p, real t0 = 0, real t1 = 0.5, real t2 = 1) {
    if (straight(subpath(p, t0, t1), 0)) {
        return 0;
    } else {
        return orient(point(p, t0), point(p, t1), point(p, t2));
    }
}

guide path_with_tail_circle(
    guide base_path,
    real cut_time,
    real end_length,
    real r34,
    real r24,
    int cross_angle = 90,
    guide next_path
) {
    guide g = subpath(base_path, 0, cut_time);

    pair z1 = relpoint(g, 1);
    pair z4 = arcpoint(reverse(g), end_length);
    pair z3 = z4 - scale(r34) * dir(-45);
    pair z2 = z4 - scale(r24) * rotate(cross_angle) * dir(z3 - z1);

    real ori = orient(g);
    real ori_next = orient(next_path);

    if (ori > 0) {
    } else if (ori < 0) {
    } else {
    }

    g = g .. z2 .. {dir(-45 -10)}z3 .. {dir(-45)}z4;
    return g;
}

guide sa = (0, 0){dir(30)} .. {dir(90)}(dir(45) * 8);
pair d0 = dir(sa, 0);
pair d1 = dir(sa, 0.1);
real a = atan2(cross(d1, d0), dot(d1, d0));
//write(a);
write(orient(sa));
write(orient(reverse(sa)));
write(orient((0, 0) -- NNE));
//draw(g);
//dot(g);
//draw(point(g, 1) -- point(g, 3));
//draw(point(g, 2) -- point(g, 4));
//draw(base_orig, red);


