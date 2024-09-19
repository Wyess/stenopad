import util;

guide append_circle(guide base, guide next) {
    int tail_angle = (int)degrees(dir(next, 0));
    int point_num = ceil((angle(dir(base)) - tail_angle) / 90) - 1;
    int base_angle = (int)degrees(dir(base)); 
    int curve_angle = (int)get_head_dir_diff(base);
    string base_model = estimate_model(base);
    string next_model = estimate_model(next);

    if (base_model == "E") {
        if (next_model == "EL") {
            //guide base = (0, 0) -- (7.5, 0);
            pair z0 = arcpoint(-base, 0);
            pair z1 = z0 + 0.8 * dir(30);
            pair z2 = z0 + 1.2 * dir(140);
            //guide na = (0, 0){dir(-18)} .. tension 1.7 .. {dir(80)}(8, 0);
            guide g = base{dir(0)} .. z1 .. tension 1.3 .. z2 .. shift(z0) * next;
            real diff = max(subpath(g, 0, length(g) - length(next))).x - z0.x;

            return (0, 0) -- shift(-diff, 0) * subpath(g, 1, length(g) - length(next));
        } else {
        //if (next_model == "SW") {
            real c0 = 1.2;
            real c1 = 1.0;
            pair z0 = relpoint(base, 0);
            pair z1 = relpoint(base, 1);
            pair z2 = z1 - E;
            pair z12 = z1 + c0 * dir(80);
            pair z21 = z2 + c1 * -dir(next);

            guide g = base{E} .. tension 1 .. z12 .. z21{dir(next)} .. shift(z2) * next;
            real xdiff = arclength(base) > 4 ? max(g).x - z1.x : 0;
            return (0, 0) -- shift(-xdiff, 0) * subpath(g, 1, length(g) - length(next));
        }
    } else if (base_model == "EL") {
    } else if (base_model == "ER") {
    } else if (base_model == "S") {
        guide g = append_circle(rotate(90) * base, rotate(90) * next);
        return rotate(-90) * g;
    }

    // ka + circle
    if (base_angle == 0) {
        if (curve_angle == 0) {
            if (tail_angle == 240) {
                real c0 = 1.2;
                real c1 = 1.0;
                pair z0 = relpoint(base, 0);
                pair z1 = relpoint(base, 1);
                pair z2 = z1 - E;
                pair z12 = z1 + c0 * dir(80);
                pair z21 = z2 + c1 * -dir(next);

                guide g = base{E} .. tension 1 .. z12 .. z21{dir(next)} .. shift(z2) * next;
                real xdiff = arclength(base) > 4 ? max(g).x - z1.x : 0;
                return (0, 0) -- shift(-xdiff, 0) * subpath(g, 1, length(g) - length(next));
            } else if (tail_angle > 360 - 45) {
                //guide base = (0, 0) -- (7.5, 0);
                pair z0 = arcpoint(-base, 0);
                pair z1 = z0 + 0.8 * dir(30);
                pair z2 = z0 + 1.2 * dir(140);
                //guide na = (0, 0){dir(-18)} .. tension 1.7 .. {dir(80)}(8, 0);
                guide g = base{dir(0)} .. z1 .. tension 1.3 .. z2 .. shift(z0) * next;
                real diff = max(subpath(g, 0, length(g) - length(next))).x - z0.x;

                return (0, 0) -- shift(diff, 0) * subpath(g, 1, length(g) - length(next));
            }
        } else if (curve_angle < 0) {
        } else {
        }
    }
    return base{dir(base_angle)} .. {dir(tail_angle)}arcpoint(reverse(base), 0.5);
    //return (0, 0) -- (1, 0);
}

guide path_null_necr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_necr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_secr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_scr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcr_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_necl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ecl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_secl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_scl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nercl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_ercl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_sercl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_srcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swrcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_nelcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_elcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_selcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_slcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_ne() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_e() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_se() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_s() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_sw() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_ner() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_er() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_ser() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_sr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_swr() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_nel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_el() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_sel() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_sl() {
    return (0, 0) -- (1, 0);
}

guide path_null_swlcl_swl() {
    return (0, 0) -- (1, 0);
}

guide path_a_smooth(path p = (0, 0)--dir(90), real tn = 1.2) {
    guide g = (0, 0){dir(-30)} .. tension tn .. shift(4, 0) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_i_smooth(path p = (0, 0)--dir(-90), real tn = 1.2) {
    guide g = (0, 0){dir(30)} .. tension tn .. shift(4, 0) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_u(path p = (0, 0)--dir(-90)) {
    return (0, 0) -- 4 * dir(p);
}

guide path_e(path p = (0, 0)--dir(-60)) {
    return (0, 0) -- 4 * dir(p);
}

guide path_e_45() {
    return path_e((0, 0)--dir(-45));
}

guide path_o(path p = (0, 0)--dir(-120)) {
    return (0, 0) -- 4 * dir(p);
}

guide path_ecl1(real len) {
    pair[] z;
    z[0] = (len - 0.5, 0);
    z[1] = z[0] + 1 * dir(45);
    z[2] = (len - 1.5, 0);
    return (0, 0) --  z[0] .. z[1] .. {dir(-135)}z[2]; 
}

guide path_ka(path p = (0, 0)--dir(0)) {
    return (0, 0) -- 8 * dir(p);
}

//guide path_ki(path p = (0, 0) .. dir(-135)) {
//    return path_ecl1(8);
//}

guide path_ki(path p = (0, 0) -- -dir(60), path base = path_ka()) {
    real c0 = 1;
    real c1 = 1;
    pair z0 = relpoint(base, 0);
    pair z1 = relpoint(base, 1);
    pair z2 = arcpoint(reverse(base), 1);
    pair z12 = z1 + c0 * dir(80);
    pair z21 = z2 + c1 * -dir(p);

    guide g = base .. tension 1.5 .. z12 .. z21{dir(p)} .. shift(z2) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_ECL1el(guide base, real a = 90, real r = 1) {
    int b = -10;
    pair z3 = rarcpoint(base, 0);
    pair z2 = z3 + r * dir(90);

    return base .. {dir(180)}z2 :: {dir(a)}z3;
}

guide path_ki_ka(real a = 0) {
    return path_ECL1el(path_ka(), a);
}

guide path_ko(path p = (0, 0) -- dir(0)) {
    return (0, 0) -- 16 * dir(0);
}

//guide path_ke(path p = (0, 0) .. dir(-135)) {
//    return path_ecl1(16);
//}

guide path_ke(path p = (0, 0) -- -dir(60)) {
    return path_ki(base = path_ko());
}

guide path_ke_e(real a = 0) {
    return path_ECL1el(path_ko(), a);
}

//guide path_sa(real ha = 30, real tn = 1.2, real ta = 90, real d = 40, pair dz = (0, 0)) {
//    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(shift(dz) * dir(d) * 8);
//}

//guide path_sa() {
guide path_sa(real ha = 30, real tn = 1.2, real ta = 90, real d = 40, pair dz = (0, 0)) {
    pair[] z;
    z[0] = (0, 0);
    z[1] = dir(45) * 8;

    return z[0]{dir(30)} .. {dir(90)}z[1];
}


guide path_sa_bend() {
    return path_sa(ta = 110);
}

guide path_su() {
    guide sa = path_sa();
    guide base = subpath(sa, 0, 0.85);

    real top = point(sa, 1).y;
    pair d = dir(-45);

    pair z1 = relpoint(base, 1);
    pair z4 = arcpoint(reverse(base), 1.8);
    pair z3 = z4 - d * 2.0;
    pair z2 = z4 + dir(z1 - z3) * I * 2.8;
    guide g = base .. z2 .. {rotate(-10) * d}z3 .. z4;

    return subpath(g, 0, length(g));
}

guide _path_su() {
    guide sa = (0, 0){dir(30)} .. {N}dir(45) * 8;
    guide base = subpath(sa, 0, 0.75);

    pair ze = arcpoint(reverse(base), 1.5);
    pair z2 = ze + dir(120) * 2;
    real h = relpoint(sa, 1).y;
    pair top = (ze.x, h);
    guide su = base .. {W}top .. {dir(-60 - 10)}z2 .. {dir(-60 + 10)}ze;
    return su;
    //return (0, 0) .. controls (2.0288, 1.1246) and (5.7144, 2.6743) .. (5.7144, 4.9674) .. controls (0, 2.1677) and (-2.4742, 1.8055) .. (-2.2707, 0.6511) .. controls (0.169, -0.9584) and (0.5711, -1.8606) .. (1.1708, -2.627);
}

guide path_su_ka_orig() {
    guide sa = (0, 0){dir(30)} .. {N}dir(45) * 8;
    guide base = subpath(sa, 0, 0.8);

    pair ze = arcpoint(reverse(base), 2.5);
    pair z2 = ze + dir(180) * 2;
    real h = relpoint(sa, 1).y;
    pair z3 = relpoint(base, 1) + dir(160) * 2;
    //guide su = base .. {W}top .. {dir(-60 - 10)}z2 .. {dir(-60 + 10)}ze;
    guide su = base .. z3 .. {E}z2 .. {E}ze;
    return su;
}

guide path_su_ka() {
    return  add_circle_14(
        path_sa(),
        path_ka(),
        l1 = 0.7,
        l4 = 3,
        l24 = 2.5,
        l34 = 2,
        direction = CCW
    );
}



//guide path_ku(path p = (0, 0)--dir(-135)) {
//    guide base = xscale(0.9) * path_ka();
//
//    pair z0 = relpoint(base, 1);
//    pair z3 = point(base, 0.6);
//    pair z2 = z3 + dir(35) * 4.5;
//
//    guide g = base{dir(0)} .. tension 1.5 .. z2 .. tension 1.0 .. shift(z3) * p;
//
//    return subpath(g, 0, length(g) - length(p));
//}

guide path_ku(path p = (0, 0) -- -dir(60)) {
    real c0 = 3;
    real c1 = 2;
    guide base = xscale(0.9) * path_ka();
    pair z0 = relpoint(base, 0);
    pair z1 = relpoint(base, 1);
    pair z2 = z0 + (5, 0);
    pair z12 = z1 + c0 * dir(80);
    pair z21 = z2 + c1 * -dir(p);

    guide g = base .. tension 1.5 .. z12 .. z21{dir(p)} .. shift(z2) * p;
    return subpath(g, 0, length(g) - length(p));
}

//guide path_ku_ka(guide g) {
//    guide ka = path_ka();
//    guide base = subarc(ka, 0, -0.5);
//    pair d = dir(base);
//    pair z1, z2, z3, z4, z5;
//    real w = 2.5;
//    real h = 2;
//
//    z1 = arcpoint(reverse(base), 0);
//    z4 = arcpoint(reverse(base), w / 2);
//    z3 = arcpoint(reverse(base), w);
//    z2 = z4 + h * d * I;
//    z5 = z1;
//
//    return base .. z2 .. {E}z3 -- z4 -- z5;
//}

guide path_ku_ka() {
    return add_circle_between_lines_of_same_dir(
        path_ka(),
        l1 = 0.5,
        w = 2.5,
        h = 2,
        direction = CCW
    );
}

guide[] paths_nihon() {
    guide[] g;
    g[0] = (0, 0) -- (4, 0);
    g[1] = shift(0, -2) * g[0];
    return g;
}

guide[] paths_nihon_jog() {
    return jogs(paths_nihon());
}


guide path_ma(path p = (0, 0)--dir(-90)) {
    guide g = (0, 0){dir(23)} .. tension 1.5 .. shift(8, 0) * p;
    return subpath(g, 0, length(g) - length(p));
}

//guide _path_su_ma() {
//    guide sa = path_sa();
//    guide ma = path_ma();
//    guide base = subpath(sa, 0, 0.92);
//
//    pair ze = arcpoint(reverse(base), 2);
//    real t = arctime(ma, 2);
//    pair z2 = ze - point(ma, t);
//    real h = relpoint(sa, 1).y;
//    pair z3 = ze + dir(relpoint(base, 1) - z2) * I * 2.5;
//    guide su = base .. z3 .. {dir(ma, t)}z2 .. shift(ze) * ma;
//    return subpath(su, 0, 4);
//}

guide path_su_ma(guide next = path_ma()) {
    //guide base = subpath(path_sa(), 0, 0.89);
    guide base = subarc(path_sa(), 0, -0.8);

    pair z1 = relpoint(base, 1);
    pair z4 = arcpoint(reverse(base), 2);
    guide arc34 = prearc(shift(z4) * next, 2);
    pair z3 = point(arc34, 0);
    pair z2 = z4 + dir(z1 - z3) * I * 2.4;

    return base .. z2 .. arc34;
}

guide[] paths_hasa() {
    pair[] z;
    z[0] = (0, 0);
    z[1] = (4.5, -sqrt(8**2 - 4.5**2));
    z[2] = (9, 0);

    guide g = z[0]{dir(-90)} .. tension 1.5 .. {dir(0)}z[1]{dir(0)} .. tension 1.5 .. {dir(90)}z[2];
    return new guide[] {subpath(g, 0, 1), subpath(g, 1, 2)};
}

guide path_null() {
    return shift(5, -1.5) * ((0, 0) -- (3, 0) -- (3, 3) -- (0, 3) -- (0, 0) -- (3, 3));
}

guide path_none() {
    return (0, 0);
}

guide path_ta(real len = 8, real a = 180 + 70) {
    return (0, 0) -- len * dir(a);
}

guide path_ha(real ha = -90, real tn = 0.8, real ta = 0, real d = -55, real len = 8, pair dz = (0, 0)) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(dz + len * dir(d));
}

guide path_ya(pair hd = dir(70), real tn = 1.1, pair td = dir(0), real d = 40, pair dz = (0, 0)) {
    return (0, 0){hd} .. tension tn .. {td}(8 * dir(d) + dz);
}

guide path_ra(real ha = -35, real tn = 1.2, real ta = -120, real d = -60, pair dz = (0, 0)) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(8 * dir(d) + dz);
}

guide path_wa(real ha = -164, real a0 = 40, real ta = 19) {
    pair z0 = (0, 0);
    pair z1 = z0 + 3.0 * dir(ha + a0);
    pair z2 = z1 + 2.0 * dir(-17);
    guide g = z0{dir(ha)} .. tension 1.4 .. z1{dir(-71)} .. tension 0.95 .. {dir(ta)}z2;

    return g;
}

guide path_wa_open(real ha = -164, real ta = 19) {
    return path_wa(ha = -180 + 25);
}

guide path_wa_up(real ha = -164, real ta = 45) {
    pair z0 = (0, 0);
    pair z1 = z0 + 3.0 * dir(ha + 40);
    pair z2 = z1 + 2.5 * dir(-10);
    guide g = z0{dir(ha)} .. tension 1.4 .. z1{dir(-71)} .. tension 0.95 .. {dir(ta)}z2;

    return g;
}

guide path_na(path p = (0, 0)-- dir(80), real ha = -18, real tn = 1.7, real ta = 80) {
    guide g = (0, 0){dir(ha)} .. tension tn .. shift(8, 0) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_shi_na(guide next = path_na()) {
    return add_circle_14(
        path_sa(),
        next,
        l1 = 2.1 / 1.8,
        l4 = 1.2 / 1.8,
        l24 = 3.0 / 1.8,
        l34 = 1.5 / 1.8,
        direction = CCW
    );
}

guide path_su_na(guide next = path_na(), bool round = true) {
    if (round) {
        return add_circle_14(
            path_sa(),
            next,
            l1 = 2.1,
            l4 = 1.2,
            l24 = 3.0,
            l34 = 1.5,
            direction = CCW
        );
    } else {
         return add_circle_14(
            path_sa(),
            next,
            l1 = 0.5,
            l4 = 3,
            l24 = 2.6,
            l34 = 2.0,
            direction = CCW
        );
    }
}

guide path_ki_na(real a = 0, path p = path_na()) {
    guide base = (0, 0) -- (7.5, 0);
    pair z0 = arcpoint(-base, 0);
    pair z1 = z0 + 0.8 * dir(30);
    pair z2 = z0 + 1.2 * dir(140);
    //guide na = (0, 0){dir(-18)} .. tension 1.7 .. {dir(80)}(8, 0);
    guide g = base{dir(0)} .. z1 .. tension 1.3 .. z2 .. shift(z0) * p;

    return subpath(g, 0, length(g) - length(p));
}

guide path_ke_na(real a = 0, path p = path_na()) {
    guide base = (0, 0) -- (15.5, 0);
    pair z0 = arcpoint(-base, 0);
    pair z1 = z0 + 0.8 * dir(30);
    pair z2 = z0 + 1.2 * dir(140);
    //guide na = (0, 0){dir(-18)} .. tension 1.7 .. {dir(80)}(8, 0);
    guide g = base{dir(0)} .. z1 .. tension 1.3 .. z2 .. shift(z0) * p;

    return subpath(g, 0, length(g) - length(p));
}

guide path_ku_na(path p = path_na()) {
    guide base = (0, 0) -- (7, 0);
    pair z0 = arcpoint(reverse(base), 0);
    //pair z1 = z0 + 2.1 * dir(30);
    //pair z2 = z0 + 3.1 * dir(140);
    //guide na = (0, 0){dir(-18)} .. tension 1.7 .. {dir(80)}(8, 0);
    pair z1 = z0 + 3.5 * dir(110);
    pair z2 = z0 + 4.5 * dir(130);
    guide g = base{dir(0)} .. z1 .. tension 1.3 .. z2 .. shift(z0) * p;

    return subpath(g, 0, length(g) - length(p));
}

guide path_ku_ma(guide next = path_ma()) {
    guide ka = path_ka();
    guide base = subarc(ka, 0, -0.5);

    pair z1 = arcpoint(reverse(base), 0);
    pair z4 = arcpoint(reverse(base), 2.5);
    pair z2 = extension(z4, z4 + dir(15), z1 + (0.5, 0), z1 + (0.5, 1));
    pair z5 = z2;
    pair z3 = interp(z4, z1, 0.2) + (0, 2);

    guide ku = base .. z2 .. z3 .. {E}z4 .. shift(z5) * next;
    return subpath(ku, 0, length(ku) - length(next));
}

guide path_no(path p = (0, 0) -- dir(90), real ha = -13, real tn = 2.5, real ta = 90) {
    guide g = (0, 0){dir(ha)} .. tension tn .. shift(16, 0) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_na_up() {
    return path_na(tn = 1.5, ta = 100);
}

guide path_ni(guide base = path_na(ta = 90)) {
    real b = 5;
    pair z3 = rarcpoint(base, 0.7);
    pair z2 = z3 - 1.4 * dir(-60 + b);

    return base .. tension 1.2 .. bend(z2 -- z3, -b);
}

real ni_wa_angle() {
    return -180 + 35;
}

guide path_x_ni_wa(path base = path_na()) {
    path wa = path_wa(ha = ni_wa_angle(), a0 = 30);
    real b = 5;
    pair z3 = arcpoint(-base, 2.5);
    pair z2 = z3 - 1.4 * dir(-60 + b);

    guide p = base :: shift(z3) * wa;
    return subpath(p, 0, length(p) - length(wa));
}

guide path_ne(guide base = path_no(ta = 90)) {
    real b = 5;
    pair z3 = rarcpoint(base, 0.6);
    pair z2 = z3 - 1.4 * dir(-60 + b);

    return base .. tension 1.2 .. bend(z2 -- z3, -b);
}

guide path_ne_ka(guide base = path_no(ta = 90), guide ka = path_ka()) {
    pair z3 = arcpoint(reverse(base), 0.4);
    pair z2 = z3 + 1 * dir(180);

    guide g = base .. tension 1.5 .. z2{dir(0)} .. shift(z3) * ka;
    return subpath(g, 0, length(g) - length(ka));
}

guide path_ne_o(guide base = path_no(ta = 90), guide o = path_o()) {
    pair z3 = xpoint(base, xpart(max(base)) - 1.5);
    pair z2 = relpoint(base, 1);
    pair z1 = z3 - 1.5 * dir(o, 0);

    guide g = base .. tension 1.5 .. z1 -- (shift(z3) * o);
    return subpath(g, 0, length(g) - length(o));
}

guide path_x_ni_o(guide base = path_na(ta = 90), real a = -120) {
    pair z3 = rarcpoint(base, 1.8);
    pair z2 = z3 - 1.3 * dir(a);

    return base .. {dir(a)}z2 -- z3; 
}

guide path_x_ni_na(guide base = path_na(ta = 90), real a = -20) {
    real b = -10;

    pair z1 = relpoint(base, 1);
    pair z3 = rarcpoint(base, 0.5);
    pair z2 = z1 + 1.4 * dir(160);

    //return base .. bend(z2 -- z3, b);
    guide g = base .. tension 1.2 .. z2 .. shift(z3) * base;
    return subpath(g, 0, length(g) - length(base));
}

guide path_x_ni_ka(guide base = path_na(ta = 90), real a = 0) {
    real b = 3;

    pair z1 = relpoint(base, 1);
    pair z3 = rarcpoint(base, 0.3);
    pair z2 = z3 - 0.8 * dir(a + b);

    return base .. {dir(a)}bend(z2 -- z3, b);
}

guide path_nu(path p = (0, 0) -- dir(40 + 180)) {
    guide base = path_na();
    pair z3 = arcpoint(base, 4);
    guide g = base .. tension 1.1 .. shift(z3) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_nu_ma(guide base = path_na(), guide p = path_ma()) {
    real ra = degrees(dir(p, 0)) + 180;
    real cx1 = 2.8;
    real cx2 = 1;
    real cy = 1.2;

    pair z1 = relpoint(base, 1);
    real t3 = arctime(base, 5);
    pair z3 = point(base, t3);
    pair z4 = arcpoint(base, 6);
    pair z2 = z4 + dir(z3 - z1) * -I * 2.2;
    guide g = base .. z2 .. {dir(base, t3)}z3 .. shift(z1) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_x_nu_ka(path p = (0, 0) -- dir(0)) {
    path base = path_na();
    pair z1 = relpoint(base, 1);
    pair z0 = arcpoint(reverse(base), 0.5);
    
    pair z2 = z0 + 4 * dir(160);
    pair z3 = z0 + 4 * dir(180);
    guide g = base .. z2 .. {dir(0)}z3 .. shift(z0) * p;
    //guide g = base .. z1 .. {dir(0)}z2 .. shift(z3) * p;
    return subpath(g, 0, length(g) - length(p));
}

guide path_souiu() {
    int a = 60;
    pair[] p;
    p[0] = (0, 0);
    p[1] = p[0] + 8 * dir(a + 180);
    p[2] = p[1] + 8 * dir(90 - a);

    int[] d = {-90, 45 + 180, 45, 0};

    return make_guide(p, d);
}

guide path_sahya() {
    int a = 30;
    pair[] p = {(0, 0)};
    p[1] = p[0] + 8 * dir(a);
    p[2] = p[1] + 8 * dir(-90 - a);
    int[] d = {0, 45, 225, -90};

    return make_guide(p, d);
}

guide path_masu() {
    return (0, 0) -- 24E;
}

guide path_cha(int a = 30) {
    return (0, 0) -- dir(a) * 8;
}

guide path_su_cha() {
    return  add_circle_14(
        path_sa(),
        path_cha(),
        l1 = 0.7,
        l4 = 2,
        l24 = 2.4,
        l34 = 2,
        direction = CCW
    );
}

guide path_su_u(guide next = path_u()) {
    guide base = subpath(path_sa(), 0, 0.80);
    guide base = subpath(path_sa(), 0, 0.80);

    pair d = dir(next, 0);

    pair z1 = relpoint(base, 1);
    pair z4 = arcpoint(reverse(base), 2.8);
    pair z3 = z4 - d * 3.0;
    pair z2 = z4 + dir(z1 - z3) * I * 3.7;
    guide g = base .. z2 .. {d}z3 .. shift(z4) * next;

    return subpath(g, 0, length(g) - length(next));

    pair d = dir(next, 0);

    pair z1 = relpoint(base, 1);
    pair z4 = arcpoint(reverse(base), 2.8);
    pair z3 = z4 - d * 3.0;
    pair z2 = z4 + dir(z1 - z3) * I * 3.7;
    guide g = base .. z2 .. {d}z3 .. shift(z4) * next;

    return subpath(g, 0, length(g) - length(next));
}
