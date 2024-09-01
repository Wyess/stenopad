import graph;
unitsize(1cm);

typedef pair offset_func(real);
typedef real thickness_func(real t);

guide get_line_contour(guide g, thickness_func d1, thickness_func d2) {
    offset_func offset_point(guide g, thickness_func d) {
        return new pair(real t) {
            return point(g, t) + d(t) * I * dir(g, t);
        };
    }

    guide p1 = graph(offset_point(g, d1), 0, 1, operator ..);
    guide p2 = graph(offset_point(g, d2), 1, 0, operator ..);
    guide con = p1 .. p2 .. cycle;
    return con;
};

guide g = (0, 0) .. {E}8E;

real th1(real t) {
    //return 0.25 - 0.25t;
    //return 0.5 * min(1, (1 - t) / (1 - 0.7));
    t = reltime(g, t);
    real s = 0.8;
    if (t < s) {
        return 0.425197;
    } else {
        return 0.425197 * -1 / ((1 - s) ^ 2) * (t - 1) * (t - (2s - 1));
    }
    //return Sin(360 * 4 * t) * 0.2 + 1;
}

real th2(real t) {
    return -th1(t);
}

guide get_flick_mask(guide g, real s = 0.75, int da0 = -30, int da1 = 30) {
    real t = 0.75;
    pair p0 = point(g, t);
    pair d0 = dir(g, t);
    pair n0 = p0 + d0 * I / 2;
    pair n1 = p0 - d0 * I / 2;
    pair p1 = point(g, 1);
    pair d1 = dir(g, 1);
    pair n2 = p1 + d1 * I * 1.1 / 2;
    pair n3 = p1 - d1 * I * 1.1 / 2;
    guide mask = n0{d0} .. {rotate(da0) * d1}p1{rotate(da1) * -d1} .. {-d0}n1{d0} .. {d1}n3 .. (p1 + d1 / 2) .. {-d1}n2 .. {-d0}cycle;

    return mask;
}

//guide c = get_line_contour(g, th1, th2);
//guide c = n0{d0} .. {rotate(-30) * d1}p1{rotate(30) * -d1} .. tension 2 .. {-d0}n1{d0} .. {d1}n3 .. (p1 + d1 / 2) .. {-d1}n2 .. n0 .. cycle;
guide c = get_flick_mask(g);
draw(g, currentpen + red + 1cm);
draw(c);
fill(c, currentpen + white);


