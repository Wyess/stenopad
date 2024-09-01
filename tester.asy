import util;
import glyph;
import path_defs;


real ori = get_rot_dir(path_na());
write(ori);
write(get_head_dir_diff(path_na()));
write(get_head_dir_diff(path_ma()));
write(get_head_dir_diff(path_ka()));
write(get_head_dir_diff(path_ya()));
write(get_head_dir_diff(path_sa()));

draw(append_circle(path_ma(), path_ka()));

void drawdetail(path p) {
    draw(p);
    currentpen += red;
    dot(p);
}

unitsize(1cm);
currentpen = 2mm + black;

pair[] p = {(0, 0)};
p[1] = p[0] + 2 * dir(250);
p[2] = p[1] + 2 * dir(0);
guide g = p[0]{dir(45 + 180)} .. p[1] .. p[2];
g = append_circle(path_ka(), path_o());
//p[1] = p[0] + 8 * dir(15);
//p[2] = p[1] + 1 * dir(45);
//p[3] = p[1];
//p[4] = p[1] + 8 * dir(255);
//int[] d = {0, 30, 30, 135, 135, 240, 240, -90};
//
//guide g = make_guide(p, d);

//draw(g);

currentpen = 1.0mm + blue;
for (int i = 1; i <= length(g); ++i) {
    //draw(point(g, i - 1) -- point(g, i));
}
//drawdetail(g);
//currentpen = 1.7mm + red;
//dot(g);
//
//draw((0, 0) -- E*8);
