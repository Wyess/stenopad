import graph;

string format_pair(pair z) {
    return format('%f', z.x) + " " + format('%f', z.y);
}

string path2svgpath(path p, pair sz = (1, 1)) {
    p = scale(sz.x, sz.y) * p;

    string s = "M" + format_pair(point(p, 0));
    for (int i = 0; i < length(p); ++i) {
        s += "C" + format_pair(postcontrol(p, i));
        s += " " + format_pair(precontrol(p, i + 1));
        s += " " + format_pair(point(p, i + 1));
    }
    return s;
}

string create_glyph_element(path p, string id, real ascent = 0.0, pair sz = (1, -1)) {
    p = scale(sz.x, sz.y) * p;
    pair bbox_min = min(p);
    pair bbox_max = max(p);

    string svg_path = path2svgpath(p);
    real path_length = arclength(p);
    pair dz = relpoint(p, 1);

    string glyph = "";
    glyph += '<glyph key="' + id + '"\n';
    glyph += '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n';
    glyph += '  xmlns:xi="http://www.w3.org/2001/XInclude"\n';
    glyph += '  xsi:noNamespaceSchemaLocation="glyph.xsd">\n';
    glyph += '  <bbox>\n';
    glyph += '    <left>' + format('%f', bbox_min.x) + '</left>\n';
    glyph += '    <right>' + format('%f', bbox_max.x) + '</right>\n';
    glyph += '    <top>' + string(bbox_min.y) + '</top>\n';
    glyph += '    <bottom>' + string(bbox_max.y) + '</bottom>\n';
    glyph += '  </bbox>\n';
    glyph += '  <dx>' + format('%f', dz.x) + '</dx>\n';
    glyph += '  <dy>' + format('%f', dz.y) + '</dy>\n';
    glyph += '  <ascent>' + string(ascent) + '</ascent>\n';

    glyph += '  <path d="' + svg_path + '" pathLength="' + string(path_length) + '" />\n';

    glyph += '</glyph>\n';

    return glyph;
}

void export_glyph_element(string filename, path p, string id, real ascent = 0.0, pair sz = (1, -1)) {
    string glyph = create_glyph_element(p, id, ascent, sz);
    file fout = output(filename);
    write(fout, glyph);
}

guide jog(path base, real deg = 20, real len = 0.5) {
    real d = degrees(dir(base), warn = false);
    if (d > 180) d -= 360;

    pair z0 = relpoint(base, 1);
    pair z1 = z0 - len * dir((d <= -90) ? d - deg : d + deg);

    return base -- z1; 
}

guide[] jogs(path[] bases, real deg = 20, real len = 0.5) {
    bases.cyclic = true;
    real d = degrees(dir(bases[-1]), warn = false);
    if (d > 180) d -= 360;

    pair z0 = relpoint(bases[-1], 1);
    pair z1 = z0 - len * dir((d <= -90) ? d - deg : d + deg);

    bases[-1] = bases[-1] -- z1;
    return bases;
}

typedef pair tailfunc(path[]);

tailfunc fn_dz(pair offset = (0, 0)) {
    return new pair(path[] p) {
        p.cyclic = true;
        return relpoint(p[-1], 1) + offset;
    };
}

tailfunc fn_flick(real len = 3, pair offset = (0, 0)) {
    return new pair(path[] p) {
        p.cyclic = true;
        pair lp = relpoint(p[-1], 1);
        return lp + dir(p[-1]) * len + offset;
    };
}

guide bend(guide g, real a1 = 10, real a2 = a1, real tn = 1.0) {
    return point(g, 0){rotate(a1) * dir(g, 0)}
    .. tension tn
        .. {rotate(-a2) * dir(g, intMax)}point(g, intMax);
}

pair rarcpoint(guide g, real len) {
    return arcpoint(reverse(g), len);
}

guide operator -(guide g) {
    return reverse(g);
}

guide operator -(path p) {
    return reverse(p);
}

pair xpoint(path p, real x, int idx = 0) {
    return (x, ypart(point(p, times(p, x)[idx])));
}

pair ypoint(path p, real y, int idx = 0) {
    return (xpart(point(p, times(p, (0, y))[idx])), y);
}

guide make_guide(pair[] p, int[] d) {
    guide g = p[0];
    for (int i = 1, j = 0; i < size(p); i += 1, j += 2) {
        g = g{dir(d[j])} .. {dir(d[j + 1])}p[i];
    }
    return g;
}

real orient(guide g) {
    if (straight(g, 0)) {
        return 0.0;
    } else {
        return orient(point(g, 0), postcontrol(g, 0), point(g, 1));
    }
}

real get_head_dir_diff(guide g) {
    pair p0 = point(g, 0);
    pair p1 = point(g, 1);
    pair c0 = postcontrol(g, 0);
    pair p = p1 - p0;
    pair c = c0 - p0;
    return degrees(atan2(cross(p, c), dot(p, c)));
}

string estimate_model(guide g) {
    string model = "";
    string[] dir_name = {"E", "NE", "N", "NW", "W", "SW", "S", "SE"};
    int d = (int)degrees(point(g, 1) - point(g, 0));

    if (d % 90 == 0) {
        int n = d # 90;
        model = dir_name[n];
    } else {
        int n = (d # 90) * 2 + 1;
        model = dir_name[n];
    }

    real diff = get_head_dir_diff(g);
    if (diff > 0) {
        model += "R";
    } else if (diff < 0) {
        model += "L";
    }

    return model;
}

typedef pair offset_func(real);
typedef real thickness_func(real t);

real th1(real t) {
    //return 0.25 - 0.25t;
    //return 0.425197 / 2 * min(1, (1 - t) / (1 - 0.8));
    real s = 0.5;
    if (t < s) {
        return 1.0;
    } else {
        //return -(t - 1) * (t - 2s + 1) / ((s - 1) ^ 2);
        return -(t - 1) * (t - 2s + 1) / ((s - 1) ^ 2);
        //return 0.425197 / 2 / 2 * (Cos(180 * (t - s)/ (1 - s)) + 1);
    }
    //return 0.425197 / 2 * min(1, (1 - t) / (1 - 0.8));
    //return min(1, (1 - t) / (1 - 0.2));
    //return  min(1, (1 - t) / (1 - 0.2));
    //return min(1, (1 - t) / (1 - 0.2));
    //return Sin(360 * 4 * t) * 0.2 + 1;
}

real th2(real t) {
    return -th1(t);
}
guide[] bak_get_line_contour(guide g, thickness_func d1 = th1, thickness_func d2 = th2, real w = 0.425197) {
    g = g .. relpoint(g, 1) + dir(g) * w / 2;
    //pair min_xy = min(g) - (w, w);
    //pair diff = max(g) + (w, w) - min_xy;

    //guide bbox = min_xy -- min_xy + (diff.x, 0) -- min_xy + diff -- min_xy + (0, diff.y) -- min_xy;

    offset_func offset_point(guide g, thickness_func d) {
        return new pair(real l) {
            real t = reltime(g, l);
            return point(g, t) + d(l) * w / 1.5 * I * dir(g, t);
        };
    }

    guide p1 = graph(offset_point(g, d1), 0, 1, operator .., n = 10);
    guide p2 = graph(offset_point(g, d2), 1, 0, operator .., n = 10);
    pair p0 = point(g, 0) - dir(g, 0) * w / 2;
    guide con = p1 .. p2 .. p0 .. cycle;
    return new guide[]{
        //bbox,
        con
    };
}

guide[] get_line_contour(guide g, real l = 0.7, real w = 0.425197) {
    g = g .. relpoint(g, 1) + dir(g) * 2w;
    pair min_xy = min(g) - (2w, 2w);
    pair diff = max(g) + (2w, 2w) - min_xy;

    guide bbox = min_xy -- min_xy + (diff.x, 0) -- min_xy + diff -- min_xy + (0, diff.y) -- min_xy -- cycle;

    real t = reltime(g, l);
    pair p0 = point(g, t);
    pair d0 = dir(g, t);
    pair n0 = p0 + d0 * 1.1 * I / 2 * w;
    pair n1 = p0 - d0 * 1.1 * I / 2 * w;
    pair p1 = relpoint(g, 1);
    pair d1 = dir(g);
    pair n2 = p1 + d1 * I * 1.5 / 2 * w;
    pair n3 = p1 - d1 * I * 1.5 / 2 * w;
    guide mask = n0{d0} .. {d1}p1{-d1} .. {-d0}n1{d0} .. {d1}n3 .. p1 .. {-d1}n2 .. {-d0}cycle;

    return new guide[]{
        bbox,
        mask
    };
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

guide[] _get_line_contour(guide g, real w = 0.425197) {
    int n = 50;

    guide gg;
    for (int j = 0; j <= n; ++j) {
        real r = j / n;
        //real t = arctime(g, arclength(g) * j / n);
        real t = reltime(g, r);
        pair d = dir(g, t);
        real w = 1.1 * 0.425197 / 2 * min(1, (1 - r) / (1 - 0.7));
        pair p = point(g, t) + w * I * d;
        gg = gg .. p;
    }

    for (int j = 0; j <= n; ++j) {
        real r = (n - j) / n;
        //real t = arctime(g, arclength(g) * (n - j) / n);
        real t = reltime(g, r);
        pair d = dir(g, t);
        //real w = 0.425197 / 2 * min(1, (n - j) / n);
        real w = 1.1 * 0.425197 / 2 * min(1, (1 - r) / (1 - 0.7));
        pair p = point(g, t) - w * I * d;
        //gg = gg .. {-d}p;
        gg = gg .. p;
    }

    gg = gg .. cycle;

    //guide p1 = graph(offset_point(g, d1), 0, length(g), operator ..);
    //guide p2 = graph(offset_point(g, d2), length(g), 0, operator ..);
    //guide con = p1 .. p2 .. cycle;
    return new guide[]{gg};
}

guide[] svg2asys(string svg_path, real scale_factor = 1 / 3.42155, bool start_from_origin = true) {
    pair pen_pos = (0, 0);
    bool start = true;
    guide[] g = new guide[];

    string[] tokens = split(svg_path, " ");
    for (int i = 0; i < tokens.length; i += 1) {
        if (find(tokens[i], "M") == 0) {
            string[] xy = split(tokens[i + 1], "");
            pen_pos = ((real)xy[0], (real)xy[1]);
            if (start) {
                g.push(((real)xy[0], (real)xy[1]));
            } else {
                g.push(((real)xy[0], (real)xy[1]));
            }
            i += 1;
        } else if (find(tokens[i], "m") == 0) {
            string[] xy = split(tokens[i + 1], ",");
            if (start) {
                if (start_from_origin) {
                    //pen_pos += ((real)xy[0], (real)xy[1]);
                    g.push((0, 0));
                } else {
                    pen_pos += ((real)xy[0], (real)xy[1]);
                    g.push(pen_pos);
                }
                start = false;
            } else {
                g.push(pen_pos);
            }
            i += 1;
        } else if (find(tokens[i], "c") == 0) {
            do {
                pair[] cp = new pair[2];
                pair p;
                string[] xy;

                xy = split(tokens[i + 1], ",");
                cp[0] = ((real)xy[0] + pen_pos.x, (real)xy[1] + pen_pos.y);

                xy = split(tokens[i + 2], ",");
                cp[1] = ((real)xy[0] + pen_pos.x, (real)xy[1] + pen_pos.y);

                xy = split(tokens[i + 3], ",");
                p = ((real)xy[0] + pen_pos.x, (real)xy[1] + pen_pos.y);

                g[g.length - 1] = g[g.length - 1] .. controls cp[0] and cp[1] .. p;

                pen_pos = p;
                i += 3;
            } while (tokens.length > (i + 1) && (find(tokens[i + 1], "c") != 0 || find(tokens[i + 1], "C") != 0 || find(tokens[i + 1], "m") != 0 || find(tokens[i + 1], "M") != 0));
        }

    }

    for (int i = 0; i < g.length; i += 1) {
        g[i] = scale(scale_factor, -scale_factor) * g[i];
    }
    return g;
}

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
    pair r34,
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
            z3 = z4 - scale(r34.x) * rotate(-10) * dir(next_path, 0);
            z2 = z4 - scale(r24) * rotate(cross_angle) * dir(z3 - z1);
            g = g .. z2 .. {rotate(-20) * dir(next_path, 0)}z3 .. shift(z4) * next_path;
        } else if (ori_next < 0) {
            // Left to right
        } else {
            // Left to straight
            z3 = z4 - scale(r34.x) * dir(next_path, 0);
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
            z3 = z4 - scale(r34.x) * dir(next_path, 0);
            z2 = z4 - scale(r24) * rotate(cross_angle) * dir(z3 - z1);
            g = g .. z2 .. {dir(next_path, 0)}z3 .. shift(z4) * next_path;
        }
    }


    //g = g .. z2 .. {rotate(-10) * dir(next_path, 0)}z3 .. shift(z4) * next_path;
    return subpath(g, 0, length(g) - length(next_path));
}

guide prearc(guide g, real l) {
    pair z0 = point(g, 0);
    pair d0 = dir(g, 0);
    real ori = orient(g);

    if (ori == 0.0) {
        pair z1 = z0 - d0 * l;
        return z1-- z0;
    } else {
        real r = radius(g, 0);
        pair n = (ori > 0 ? I : -I) * d0;
        real a = (ori > 0 ? 1 : -1) * degrees(l / r);
        pair z1 = z0 + r * (rotate(a) * n - n);
        pair d1 = rotate(a) * d0;
        return subpath(z1{d1} .. g, 0, 1);
    }
}

guide subarc(guide g, real a, real b) {
    real l = arclength(g);
    if (a < 0) a += l;
    if (b < 0) b += l;

    return subpath(g, arctime(g, a), arctime(g, b));
}
