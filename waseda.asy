import util;
import glyph;
import path_defs;

write(mm);
// TODO: Decomposition of complex ligatures
//       - Ha-Sa as a simple example
// TODO: Streamline the process
//       - write character file in asymptote program -> DONE(20240401
//       - defalut: new file, others: append -> DONE(20240401)
//       - dict: Done (20240403)
//       - char
// DONE: Implement position-characters (20240329)

file fout = output("waseda_asy.toml");
Glyph.fout = fout;

//Dict dict = Dict.Dict("waseda_dict_asy.xml");
//CharSet cset = CharSet.CharSet("waseda_chars_asy.xml");

Glyph.Glyph(
    "Null",
    "default",
    fn_dz((5, -1.5)),
    0.0,
    path_null()
).toml();

Glyph.Glyph(
    "Newline",
    "default",
    fn_dz(),
    0.0,
    path_none()
).toml().dict("\n");

Glyph.Glyph(
    "Space",
    "default",
    fn_dz((4, 0)),
    0.0,
    path_none()
).toml().dict(" ");

Glyph.Glyph(
    "A",
    "default",
    fn_dz(),
    0.0
    ... path_a_smooth()
).toml().dict("あ")
 .group("head_el4")
 .group("tail_el");

Glyph.Glyph(
    "A",
    "$i[1]",
    fn_dz(),
    0.0,
    path_a_smooth(path_i_smooth())
).toml();

Glyph.Glyph(
    "A",
    "$head_sw[1] | $wa[1]",
    fn_dz(),
    0.0,
    path_a_smooth(scale(-1) * path_o())
).toml();

Glyph.Glyph(
    "A",
    "$head_s[1]",
    fn_dz(),
    0.0,
    path_a_smooth(scale(-1) * path_u())
).toml();

Glyph.Glyph(
    "A",
    "$head_e[1]",
    fn_dz(),
    0.0,
    path_a_smooth(scale(-1) * path_e(), tn = 1)
).toml();

Glyph.Glyph(
    "Kari",
    "default",
    fn_flick(),
    0.0,
    mask = get_line_contour(path_ka())
    //mask =  get_flick_mask(path_ka())
    ... path_ka()
).toml().dict("カリ").group('head_e');

Glyph.Glyph(
    "Nihon",
    "default",
    fn_dz(),
    1.0
    ... paths_nihon()
).toml().dict("日本").group("head_e");

Glyph.Glyph(
    "Nihon",
    "$head_e[1]",
    fn_dz(),
    1.0
    ... paths_nihon_jog()
).toml();

Glyph.Glyph(
    "Ma",
    "default",
    fn_dz(),
    0.0,
    path_ma()
).toml()
 .dict("ま")
 .group("head_er8");

Glyph.Position(
    "Pos_Aru",
    "default",
    (3, 0)
).toml();

Glyph.Glyph(
    "U",
    "default",
    fn_dz(),
    ascent = 2.0,
    path_u()
).toml().dict("う")
 .group("head_s")
 .group("tail_s");

Glyph.Glyph(
    "E",
    "default",
    fn_dz(),
    ascent = 2,
    path_e()
).toml().dict("え").group("head_se");

Glyph.Glyph(
    "E",
    "$tail_s[-1]",
    fn_dz(),
    ascent = 2,
    path_e_45()
).toml();


Glyph.Glyph(
    "O",
    "default",
    fn_dz(),
    ascent = 2,
    path_o()
).toml().dict("お").dict("を").group("head_sw");

Glyph.Glyph(
    "Masu",
    "default",
    fn_flick(),
    ascent = 0,
    clip_paths = get_line_contour(path_masu()),
    path_masu()
).toml().dict("マス").group('head_e');

Glyph.Glyph(
    "Ka",
    "default",
    fn_dz(),
    ascent = 0,
    path_ka()
).toml().dict("か").dict("カ").group('head_e');

Glyph.Glyph(
    "Ka",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    jog(path_ka())
).toml();

Glyph.Glyph(
    "Ki",
    "default",
    fn_dz(),
    ascent = 0,
    //path_ki()
    append_circle(path_ka(), path_o())
).toml().dict("き").group("head_e");

Glyph.Glyph(
    "Ki",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    path_ki_ka()
).toml();

Glyph.Glyph(
    "Ki",
    "$head_el8[1]",
    fn_dz(),
    ascent = 0,
    //path_ki_na()
    append_circle(path_ka(), path_na())
).toml();

Glyph.Glyph(
    "Ku",
    "default",
    fn_dz(),
    ascent = 0,
    path_ku()
).toml().dict("く")
 .group("head_e");

//Glyph.Glyph(
//    "Ku",
//    "$head_e[1]",
//    fn_dz(),
//    ascent = 0,
//    path_ku_ka()
//).toml();

Glyph.Glyph(
    "Ku",
    "$head_el8[1]",
    fn_dz(),
    ascent = 0,
    path_ku_na()
).toml();

Glyph.Glyph(
    "Ku",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    //append_circle(path_ka(), path_ka(), 0.93, 0, r34 = 2.0, r24 = 2.5, 135)
    path_ku_ka()
).toml();

Glyph.Glyph(
    "Ku",
    "$head_er8[1]",
    fn_dz(),
    ascent = 0,
    path_ku_ma()
).toml();

Glyph.Glyph(
    "Ke",
    "default",
    fn_dz(),
    ascent = 0,
    //path_ke()
    append_circle(path_ko(), path_o())
).toml().dict("け")
 .group("head_e");

Glyph.Glyph(
    "Ke",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    path_ke_e()
).toml();

Glyph.Glyph(
    "Ke",
    "$head_el8[1]",
    fn_dz(),
    ascent = 0,
    path_ke_na()
).toml();

Glyph.Glyph(
    "Kei",
    "default",
    fn_dz(),
    ascent = 0,
    append_circle((0, 0) -- E * 4, path_o())
).toml().dict("ケー")
 .group("head_e");

Glyph.Glyph(
    "Kei",
    "$head_el8[1]",
    fn_dz(),
    ascent = 0,
    append_circle((0, 0) -- E * 4, path_na())
).toml();

Glyph.Glyph(
    "Ko",
    "default",
    fn_dz(),
    ascent = 0,
    path_ko()
).toml().dict("こ").group("head_e");

Glyph.Glyph(
    "Ko",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    jog(path_ko())
).toml();

Glyph.Glyph(
    "Sa",
    "default",
    fn_dz(),
    ascent = -3,
    path_sa()
).toml().dict("さ");

Glyph.Glyph(
    "Sa",
    "$head_e[1]",
    fn_dz(),
    ascent = -3,
    path_sa_bend()
).toml();

Glyph.Glyph(
    "Su",
    "default",
    fn_dz(),
    ascent = -3,
    path_su()
).toml().dict("す");

Glyph.Glyph(
    "Su",
    "$head_e[1]",
    fn_dz(),
    ascent = -3,
    path_su_ka()
).toml();

Glyph.Glyph(
    "Su",
    "$head_er8[1]",
    fn_dz(),
    ascent = -3,
    path_su_ma()
).toml();

Glyph.Glyph(
    "Su",
    "$head_el8[1]",
    fn_dz(),
    ascent = -3,
    path_su_na()
).toml();

Glyph.Glyph(
    "Su",
    "$head_ne[1]",
    fn_dz(),
    ascent = -3,
    path_su_cha()
).toml();

Glyph.Glyph(
    "Su",
    "$head_s[1]",
    fn_dz(),
    ascent = -3,
    path_su_u()
).toml();

Glyph.Glyph(
    "Su",
    "$head_se[1]",
    fn_dz(),
    ascent = -3,
    path_su_e()
).toml();

Glyph.Glyph(
    "Na",
    "default",
    fn_dz(),
    ascent = 0,
    path_na()
).toml().dict("な")
 .group("tail_el")
 .group("head_el")
 .group("head_el8");

Glyph.Glyph(
    "Na",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    path_na_up()
).toml();

Glyph.Glyph(
    "No",
    "default",
    fn_dz(),
    ascent = 0,
    path_no()
).toml().dict("の")
 .group("tail_el")
 .group("head_el16");

Glyph.Glyph(
    "Ni",
    "default",
    fn_dz(),
    ascent = 0,
    path_ni()
).toml().dict("に")
 .group("head_el8");

Glyph.Glyph(
    "Ni",
    "$o[1]",
    fn_dz(),
    ascent = 0,
    path_x_ni_o()
).toml();

Glyph.Glyph(
    "Ni",
    "$head_el8[1]",
    fn_dz(),
    ascent = 0,
    path_x_ni_na()
).toml();

Glyph.Glyph(
    "Ni",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    path_x_ni_ka()
).toml();

Glyph.Glyph(
    "Ni",
    "$wa[1]",
    fn_dz(),
    ascent = 0,
    path_x_ni_wa()
).toml();

Glyph.Glyph(
    "Ne",
    "default",
    fn_dz(),
    ascent = 0,
    path_ne()
).toml().dict("ね")
 .group("head_el16");

Glyph.Glyph(
    "Ne",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    path_ne_ka()
).toml();

Glyph.Glyph(
    "Ne",
    "$o[1]",
    fn_dz(),
    ascent = 0,
    path_ne_o()
).toml();

Glyph.Glyph(
    "Nu",
    "default",
    fn_dz(),
    ascent = 0,
    path_nu()
).toml().dict("ぬ");

Glyph.Glyph(
    "Nu",
    "$head_er8[1]",
    fn_dz(),
    ascent = 0,
    path_nu_ma()
).toml();

Glyph.Glyph(
    "Nu",
    "$head_e[1]",
    fn_dz(),
    ascent = 0,
    path_x_nu_ka()
).toml();

Glyph.Glyph(
    "I",
    "default",
    fn_dz(),
    0.0
    ... path_i_smooth()
).toml().dict("い").group('head_er4');

Glyph.Glyph(
    "I",
    "$head_el4[1]",
    fn_dz(),
    0.0
    ... path_i_smooth(path_a_smooth())
).toml();

Glyph.Glyph(
    "I",
    "$head_el8[1]",
    fn_dz(),
    0.0
    ... path_i_smooth(path_na())
).toml();

Glyph.Glyph(
    "I",
    "$head_se[1] | $head_e[1]",
    fn_dz(),
    0.0
    ... path_i_smooth(path_o(), tn = 0.8)
).toml();

Glyph.Glyph(
    "Ta",
    "default",
    fn_dz(),
    2.0,
    path_ta()
).toml().dict("た").group("head_sw");

Glyph.Glyph(
    "Cha",
    "default",
    fn_dz(),
    -2.0,
    path_cha()
).toml().dict("ちゃ").group("head_ne");

Glyph.Glyph(
    "Ha",
    "default",
    fn_dz(),
    2.0,
    path_ha()
).toml().dict("は").group("head_sel");

Glyph.Glyph(
    "Ya",
    "default",
    fn_dz(),
    -2.0,
    path_ya()
).toml().dict("や");

Glyph.Glyph(
    "Yan",
    "default",
    fn_flick(),
    -2.0,
    mask = get_line_contour(path_ya()),
    path_ya()
).toml().dict("やん");

Glyph.Glyph(
    "Ra",
    "default",
    fn_dz(),
    3.0,
    path_ra()
).toml().dict("ら");

Glyph.Glyph(
    "Wa",
    "default",
    fn_dz(),
    1.0,
    path_wa()
).toml().dict("わ");

Glyph.Glyph(
    "Wa",
    "$tail_el[-1]",
    fn_dz(),
    1.0,
    //path_wa_open()
    path_wa_open()
).toml();

Glyph.Glyph(
    "Wa",
    "$ni[-1]",
    fn_dz(),
    1.0,
    //path_wa_open()
    path_wa(ha = ni_wa_angle(), a0 = 30)
).toml();

Glyph.Glyph(
    "Wa",
    "$head_e[1]",
    fn_dz(),
    1.0,
    path_wa(ta = 0)
).toml();

Glyph.Glyph(
    "Wa",
    "$head_el[1]",
    fn_dz(),
    1.0,
    path_wa_up()
).toml();

Glyph.Glyph(
    "Shou",
    "default",
    fn_flick(),
    2.0,
    path_ta()
).toml()
 .dict("ショー")
 .dict("タラ")
 .dict("タリ");

Glyph.Glyph(
    "Souiu",
    "default",
    fn_dz(),
    3,
    path_souiu()
).toml()
 .dict("ソウイウ")
 .dict("ソーユー");

Glyph.Glyph(
    "Uu",
    "default",
    fn_dz(),
    2,
    append_circle(path_u(), path_na())
).toml()
 .dict("ウー")
 .dict("ウウ");
