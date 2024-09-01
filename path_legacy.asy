include util;

path path_SWL8NEL8(pair pos = (0, 0)) {
    return shift(pos) * rotate(-30) * ((0, 0){dir(-120)} .. tension 1.5 .. {dir(-30)}(1.2, -sqrt(7.6 ^ 2 - 1.2 ^ 2)){dir(-30)} .. tension 1.5 .. {dir(120)}(2.4, 0.0));
}

path path_OSEL4(pair pos = (0, 0)) {
    return shift(pos) * ((0, 0){dir(-95)} .. tension 1.6 .. {dir(0)}rpair(3.5, -60) .. tension 1.55 .. {dir(135)}(0, 0));
}

path path_OSL4(pair pos = (0, 0)) {
    return shift(pos) * ((0, 0){dir(-135)} .. tension 2.3 .. {dir(0)}rpair(3.7, -90) .. tension 2.3 .. {dir(135)}(0, 0));
}

path path_OSWL4(pair pos = (0, 0)) {
    return shift(pos) * ((0, 0){dir(180)} .. tension 2.4 .. {dir(-55)}rpair(3.7, -128) .. tension 2.9 .. {dir(122)}(0, 0));
}

path path_CNR4(pair pos = (0,0)) {
    return shift(pos) * ((0, 0){dir(180)} .. tension 0.9 .. {dir(90)}(-1.4, 1.6) .. tension 1.2 .. {dir(0)}(0.4, 3.2) .. tension 1.1 .. {dir(-94)}(2.0, 1.5) .. tension 1.2 .. {dir(180)}(0, 0));
}

path path_SEL1() {
    path p = (0, 0){dir(-98)} .. {dir(-22)}(1.0, -1.0);
    p = shift(-arcpoint(p, 0.55)) * p;
    return p;
}

path path_P() {
    return (0, 0);
}

guide path_E4() {
    return (0, 0) -- (4, 0);
}

guide path_E8() {
    return (0, 0) -- (8, 0);
}

guide path_E16() {
    return (0, 0) -- (16, 0);
}

guide path_E20() {
    return (0, 0) -- (20, 0);
}

guide path_E24() {
    return (0, 0) -- (24, 0);
}

guide path_NE8(real a = 34) {
    return (0, 0) -- rpair(8, a);
}

guide path_NE16(real a = 40) {
    return (0, 0) -- rpair(16, a);
}

guide path_NE24(real a = 37) {
    return rotate(a) * path_E24();
}

guide path_SE24(real a = -55) {
    return rotate(a) * path_E24();
}

guide path_SW4(real a = 45 - 180) {
    return (0, 0) -- rpair(4, a);
}

guide path_SW8(real len = 8, real a = 70 - 180) {
    return (0, 0) -- rpair(len, a);
}

guide path_SW16(real a = -115) {
    return (0, 0) -- rpair(16, a);
}

guide path_SW24(real a = -105) {
    return rotate(a) * path_E24();
}

guide path_S20(real a = -90) {
    return (0, 0) -- rpair(20, a);
}

guide path_ER24() {
    return (0, 0){dir(15)} .. {dir(-30)}(24, 0);
}

guide path_EL25_4() {
    return (0, 0){dir(-30)}..tension 1.5..{dir(40)}(25.4, 0);
}

guide path_E24CR1F() {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(23.0, 0);
    pair z2 = z1 + rpair(0.9, -46);
    pair z3 = z2 + rpair(0.9, -159);
    pair z4 = z3 + rpair(2.7, 52);
    guide g = z0{dir(-4)} .. tension 1.05 .. z1{dir(4)} .. tension 0.75 .. z2{dir(-143)} .. tension 1.15 .. z3{dir(140)} .. tension 2.65 .. {dir(44)}z4;

    return g;
}

guide path_ER24CR1F() {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(23.0, 1);
    pair z2 = z1 + rpair(1.0, -70);
    pair z3 = z2 + rpair(0.7, -160);
    pair z4 = z3 + rpair(2.5, 53);
    guide g = z0{dir(16)} .. tension 1.4 .. {dir(-15)}z1 .. tension 0.8 .. z2{dir(-131)} .. tension 1.2 .. z3{dir(151)} .. tension 2.05 .. {dir(42)}z4;

    return g;
}


guide path_Ecl1(guide base) {
    base = xscale(7.5 / 8.0) * base;
    int b = 3;
    pair z2 = point(base, 1) + rpair(0.7, 45);
    return bend(base, b) .. z2; 
}

guide path_Ecl4(guide base) {
    return path_Ecl1(base);
}

guide path_SWR4(real ha = -80, real tn = 1.1, real ta = -155, real len = 4.3, real d = -113) {
    return (0, 0){dir(ha)} .. tension 1.1 .. {dir(ta)}rpair(len, d);
}

guide path_SERSWR4() {
    /*
       0.000000,0.000000
       1.545560,0.051249
       2.356550,-0.739770
       2.356550,-1.109650
       2.356550,-1.945820
       0.564880,-2.580310
       -0.114517,-2.685080
       (0.000000, 0.000000) .. controls (1.545560, 0.051249) and (2.356550, -0.739770) .. 
       (2.356550, -1.109650) .. controls (2.356550, -1.945820) and (0.564880, -2.580310) .. 
       (-0.114517, -2.685080)
     */

    //pair z0 = (0, 0);
    //pair z1 = z0 + (2.4, -1.1);
    //pair z2 = z1 + (-2.5, -1.6);
    //pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    //pair z2 = z0 + rpair(2.7, -92);
    pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    pair z1 = z0 + (2.2, -1.1);
    pair z2 = z1 + rpair(2.9, -147);
    guide g = z0{dir(2)} .. tension 0.8 and 2.05 .. {dir(-90)}z1{dir(-90)} .. tension 1.3 and 1.65 .. {dir(-171)}z2;

    return g;
}

guide path_SERSWR4_tangent(real a = -171) {
    /*
       0.000000,0.000000
       1.545560,0.051249
       2.356550,-0.739770
       2.356550,-1.109650
       2.356550,-1.945820
       0.564880,-2.580310
       -0.114517,-2.685080
       (0.000000, 0.000000) .. controls (1.545560, 0.051249) and (2.356550, -0.739770) .. 
       (2.356550, -1.109650) .. controls (2.356550, -1.945820) and (0.564880, -2.580310) .. 
       (-0.114517, -2.685080)
     */

    //pair z0 = (0, 0);
    //pair z1 = z0 + (2.4, -1.1);
    //pair z2 = z1 + (-2.5, -1.6);
    //pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    //pair z2 = z0 + rpair(2.7, -92);
    pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    pair z1 = z0 + (2.2, -1.1);
    pair z2 = z1 + rpair(2.9, -130);
    guide g = z0{dir(2)} .. tension 0.8 and 2.05 .. {dir(-90)}z1{dir(-90)} ..
        tension 1.3 .. {-dir(a)}z2;

    return g;
}

guide path_SERSWR4_up() {
    /*
       0.000000,0.000000
       1.545560,0.051249
       2.356550,-0.739770
       2.356550,-1.109650
       2.356550,-1.945820
       0.564880,-2.580310
       -0.114517,-2.685080
       (0.000000, 0.000000) .. controls (1.545560, 0.051249) and (2.356550, -0.739770) .. 
       (2.356550, -1.109650) .. controls (2.356550, -1.945820) and (0.564880, -2.580310) .. 
       (-0.114517, -2.685080)
     */

    //pair z0 = (0, 0);
    //pair z1 = z0 + (2.4, -1.1);
    //pair z2 = z1 + (-2.5, -1.6);
    //pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    //pair z2 = z0 + rpair(2.7, -92);
    pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    pair z1 = z0 + (2.2, -1.1);
    pair z2 = z1 + rpair(2.9, -160);
    guide g = z0{dir(2)} .. tension 0.8 and 2.05 .. {dir(-90)}z1{dir(-90)} ..
        tension 1.3 and 1.65 .. {dir(135)}z2;

    return g;
}
guide path_SERSWR4_seamless(real a) {
    /*
       0.000000,0.000000
       1.545560,0.051249
       2.356550,-0.739770
       2.356550,-1.109650
       2.356550,-1.945820
       0.564880,-2.580310
       -0.114517,-2.685080
       (0.000000, 0.000000) .. controls (1.545560, 0.051249) and (2.356550, -0.739770) .. 
       (2.356550, -1.109650) .. controls (2.356550, -1.945820) and (0.564880, -2.580310) .. 
       (-0.114517, -2.685080)
     */

    //pair z0 = (0, 0);
    //pair z1 = z0 + (2.4, -1.1);
    //pair z2 = z1 + (-2.5, -1.6);
    //pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    //pair z2 = z0 + rpair(2.7, -92);
    pair z0 = (0, 0);
    //pair z1 = z0 + rpair(2.6, -25);
    pair z1 = z0 + (2.2, -1.1);
    pair z2 = z1 + rpair(2.9, -147);
    guide g = z0{dir(2)} .. tension 0.8 and 2.05 .. {dir(-90)}z1{dir(-90)} ..
        tension 1.3 and 1.65 .. {dir(a)}z2;

    return g;
}
guide path_E8CL1() {
    guide base = path_Ecl1(path_E8());
    int b = -5;
    pair z3 = arcpoint(-base, 1.7);
    pair z2 = z3 - rpair(1.2, 50 + b - 180);

    return base .. bend(z2 -- z3, b); 
}

guide path_E16CL1() {
    guide base = path_Ecl1(path_E16());
    int b = -5;
    pair z3 = arcpoint(-base, 1.7);
    pair z2 = z3 - rpair(1.2, 50 + b - 180);

    return base .. bend(z2 -- z3, b); 
}

guide path_E20CL1() {
    guide base = path_Ecl1(path_E20());
    int b = -5;
    pair z3 = arcpoint(-base, 1.7);
    pair z2 = z3 - rpair(1.2, 50 + b - 180);

    return base .. bend(z2 -- z3, b); 
}


guide path_E4CL1() {
    guide base = path_Ecl1(path_E4());
    int b = -5;
    pair z3 = arcpoint(-base, 1.7);
    pair z2 = z3 - rpair(1.2, 50 + b - 180);

    return base .. bend(z2 -- z3, b); 
}


guide path_ECL1sw(guide base, real a) {
    base = path_Ecl1(base);
    int b = 5;
    pair z3 = arcpoint(-base, 1.2);
    pair z2 = z3 - rpair(0.9, a);

    return base .. {dir(a)}bend(z2 -- z3, b);
}

guide path_E4CL1sw(real a = 60 - 180) {
    return path_ECL1sw(path_E4(), a);
}
guide path_E8CL1sw(real a = 60 - 180) {
    return path_ECL1sw(path_E8(), a);
}

guide path_E16CL1sw(real a = 60 - 180) {
    return path_ECL1sw(path_E16(), a);
}

guide path_E20CL1sw(real a = 60 - 180) {
    return path_ECL1sw(path_E20(), a);
}

guide path_ECL1swr(guide base, real a) {
    base = path_Ecl1(base);
    int b = 5;
    pair z3 = arcpoint(-base, 1.0);
    pair z2 = z3 - rpair(0.7, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1swr(real a = -90) {
    return path_ECL1swr(path_E4(), a);
}
guide path_E8CL1swr(real a = -90) {
    return path_ECL1swr(path_E8(), a);
}
guide path_E16CL1swr(real a = -90) {
    return path_ECL1swr(path_E16(), a);
}

guide path_E20CL1swr(real a = -90) {
    return path_ECL1swr(path_E20(), a);
}

guide path_ECL1sel(guide base, real a = -90) {
    base = path_Ecl1(base);
    int b = -8;
    pair z3 = arcpoint(-base, 1.1);
    pair z2 = z3 - rpair(1, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1sel(real a = -90) {
    return path_ECL1sel(path_E4(), a);
}

guide path_E8CL1sel(real a = -90) {
    return path_ECL1sel(path_E8(), a);
}

guide path_E16CL1sel(real a = -90) {
    return path_ECL1sel(path_E16(), a);
}

guide path_E20CL1sel(real a = -90) {
    return path_ECL1sel(path_E20(), a);
}

guide path_ECL1sl(guide base, real a = -120) {
    base = path_Ecl1(base);
    int b = -10;
    pair z3 = arcpoint(-base, 1.5);
    pair z2 = z3 - rpair(1.3, a + b);

    return base .. bend(z2 -- z3, b, 0.8);
}

guide path_E4CL1sl(real a = -120) {
    return path_ECL1sl(path_E4(), a);
}

guide path_E8CL1sl(real a = -120) {
    return path_ECL1sl(path_E8(), a);
}

guide path_E16CL1sl(real a = -120) {
    return path_ECL1sl(path_E16(), a);
}

guide path_E20CL1sl(real a = -120) {
    return path_ECL1sl(path_E20(), a);
}

guide path_ECL1swl(guide base, real a = -120) {
    base = path_Ecl1(base);
    int b = -10;
    pair z3 = arcpoint(-base, 1.5);
    pair z2 = z3 - rpair(1.2, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1swl(real a = -120) {
    return path_ECL1swl(path_E4(), a);
}

guide path_E8CL1swl(real a = -120) {
    return path_ECL1swl(path_E8(), a);
}

guide path_E16CL1swl(real a = -120) {
    return path_ECL1swl(path_E16(), a);
}

guide path_E20CL1swl(real a = -120) {
    return path_ECL1swl(path_E20(), a);
}

guide path_ECL1ne(guide base, real a = -120) {
    base = path_Ecl1(base);
    pair z3 = arcpoint(-base, 1.8);
    pair z2 = z3 - rpair(0.9, a - 180);

    return base .. {-dir(a)}z2 -- z3;
}

guide path_E4CL1ne(real a = -120) {
    return path_ECL1ne(path_E4(), a);
}

guide path_E8CL1ne(real a = -120) {
    return path_ECL1ne(path_E8(), a);
}

guide path_E16CL1ne(real a = -120) {
    return path_ECL1ne(path_E16(), a);
}

guide path_E20CL1ne(real a = -120) {
    return path_ECL1ne(path_E20(), a);
}

guide path_ECL1s(guide base, real a = -90) {
    base = path_Ecl1(base);
    pair z3 = arcpoint(-base, 1.0);
    pair z2 = z3 - rpair(0.8, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_E4CL1s(real a = -90) {
    return path_ECL1s(path_E4(), a);
}

guide path_E8CL1s(real a = -90) {
    return path_ECL1s(path_E8(), a);
}

guide path_E16CL1s(real a = -90) {
    return path_ECL1s(path_E16(), a);
}

guide path_E20CL1s(real a = -90) {
    return path_ECL1s(path_E20(), a);
}


guide path_ECL1se(guide base, real a = -60) {
    base = path_Ecl1(base);
    pair z3 = arcpoint(-base, 0.7);
    pair z2 = z3 - rpair(1.0, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_E4CL1se(real a = -60) {
    return path_ECL1se(path_E4(), a);
}

guide path_E8CL1se(real a = -60) {
    return path_ECL1se(path_E8(), a);
}

guide path_E16CL1se(real a = -60) {
    return path_ECL1se(path_E16(), a);
}

guide path_E20CL1se(real a = -60) {
    return path_ECL1se(path_E20(), a);
}

guide path_ECL1ser(guide base, real a = -60) {
    base = path_Ecl1(base);
    int b = 5;
    pair z3 = arcpoint(-base, 0.5);
    pair z2 = z3 - rpair(1.1, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1ser(real a = -60) {
    return path_ECL1ser(path_E4(), a);
}

guide path_E8CL1ser(real a = -60) {
    return path_ECL1ser(path_E8(), a);
}

guide path_E16CL1ser(real a = -60) {
    return path_ECL1se(path_E16(), a);
}

guide path_E20CL1ser(real a = -60) {
    return path_ECL1se(path_E20(), a);
}


guide path_ECL1sr(guide base, real a = -60) {
    base = path_Ecl1(base);
    int b = 5;
    pair z3 = arcpoint(-base, 0.6);
    pair z2 = z3 - rpair(1.1, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1sr(real a = -60) {
    return path_ECL1sr(path_E4(), a);
}

guide path_E8CL1sr(real a = -60) {
    return path_ECL1sr(path_E8(), a);
}

guide path_E16CL1sr(real a = -60) {
    return path_ECL1sr(path_E16(), a);
}

guide path_E20CL1sr(real a = -60) {
    return path_ECL1sr(path_E20(), a);
}

guide path_ECL1ner(guide base, real a = 90) {
    base = path_Ecl1(base);
    int b = -15;
    pair z3 = arcpoint(-base, 1.5);
    pair z2 = z3 - rpair(1.0, a + b + 180);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1ner(real a = 90) {
    return path_ECL1ner(path_E4(), a);
}

guide path_E8CL1ner(real a = 90) {
    return path_ECL1ner(path_E8(), a);
}

guide path_E16CL1ner(real a = 90) {
    return path_ECL1ner(path_E16(), a);
}

guide path_E20CL1ner(real a = 90) {
    return path_ECL1ner(path_E20(), a);
}



guide path_ECL1el(guide base, real a = 90) {
    base = path_Ecl1(base);
    int b = -10;
    pair z3 = arcpoint(-base, 0.4);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1el(real a = 90) {
    return path_ECL1el(path_E4(), a);
}

guide path_E8CL1el(real a = 90) {
    return path_ECL1el(path_E8(), a);
}

guide path_E16CL1el(real a = 90) {
    return path_ECL1el(path_E16(), a);
}

guide path_E20CL1el(real a = 90) {
    return path_ECL1el(path_E20(), a);
}


guide path_ECL1e(guide base, real a = 0) {
    int b = 0;
    base = bend(base, b);
    pair z1 = lastpoint(base) + (0, 0.1);
    pair z2 = z1 + rpair(0.8, 125);
    pair z3 = z1 + rpair(1.0, 180);

    return base .. {dir(180)}z2 .. {dir(a)}z3 .. z1;
}

guide path_E4CL1e(real a = 0) {
    return path_ECL1e(path_E4(), a);
}

guide path_E8CL1e(real a = 0) {
    return path_ECL1e(path_E8(), a);
}

guide path_E16CL1e(real a = 0) {
    return path_ECL1e(path_E16(), a);
}

guide path_E20CL1e(real a = 0) {
    return path_ECL1e(path_E20(), a);
}


guide path_ECL1_xe(guide base, real a = 0) {
    int b = 2;
    base = bend(base, b);
    pair z1 = lastpoint(base) + (0, 0.1);
    pair z2 = z1 + rpair(0.8, 125);
    pair z3 = z1 + rpair(1.1, 180);
    pair z4 = z1 + (0.2, 0); 

    return base .. {dir(180)}z2 .. {dir(a)}z3 -- z4;
}

guide path_E4CL1xe(real a = 0) {
    return path_ECL1_xe(path_E4(), a);
}

guide path_E8CL1xe(real a = 0) {
    return path_ECL1_xe(path_E8(), a);
}

guide path_E16CL1xe(real a = 0) {
    return path_ECL1_xe(path_E16(), a);
}

guide path_E20CL1xe(real a = 0) {
    return path_ECL1_xe(path_E20(), a);
}


guide path_ECL1er(guide base, real a = 0) {
    int b = 2;
    base = bend(base, b);
    pair z1 = lastpoint(base) + (0, 0.3);
    pair z2 = z1 + rpair(0.8, 125);
    pair z3 = z1 + rpair(1.0, 180);

    return base .. {dir(180)}z2 .. z3 ..{dir(a)}z1;
}

guide path_E4CL1er(real a = 0) {
    return path_ECL1er(path_E4(), a);
}

guide path_E8CL1er(real a = 0) {
    return path_ECL1er(path_E8(), a);
}

guide path_E16CL1er(real a = 0) {
    return path_ECL1er(path_E16(), a);
}

guide path_E20CL1er(real a = 0) {
    return path_ECL1er(path_E20(), a);
}



guide path_ECL1nel(guide base, real a = 0) {
    int b = 2;
    base = bend(base, b);
    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(0.8, 125);
    pair z3 = z1 + rpair(1.5, 180);

    return base .. {dir(180)}z2 .. z3 ..{dir(a)}z1;
}

guide path_E4CL1nel(real a = 0) {
    return path_ECL1nel(path_E4(), a);
}

guide path_E8CL1nel(real a = 0) {
    return path_ECL1nel(path_E8(), a);
}

guide path_E16CL1nel(real a = 0) {
    return path_ECL1nel(path_E16(), a);
}

guide path_E20CL1nel(real a = 0) {
    return path_ECL1nel(path_E20(), a);
}



guide path_ECL1ner(guide base, real a = 90) {
    base = path_Ecl1(base);
    int b = -15;
    pair z3 = arcpoint(-base, 1.5);
    pair z2 = z3 - rpair(1.0, a + b + 180);

    return base .. bend(z2 -- z3, b);
}

guide path_E4CL1ner(real a = 90) {
    return path_ECL1ner(path_E4(), a);
}

guide path_E8CL1ner(real a = 90) {
    return path_ECL1ner(path_E8(), a);
}

guide path_E16CL1ner(real a = 90) {
    return path_ECL1ner(path_E16(), a);
}

guide path_E20CL1ner(real a = 90) {
    return path_ECL1ner(path_E20(), a);
}

guide path_SE4NE4(real a = -60, real a1 = -a) {
    int b = 3;
    pair z0 = (0, 0);
    pair z1 = rpair(3.5, a);
    pair z2 = z1 + rpair(3.5, a1);


    return bend(z0 -- z1, b) & bend(z1 -- z2, b);
}


guide path_SEL8NEL8() {
    // hasa
    return
        (0, 0){dir(-90)}
    .. tension 1.5
        .. {dir(0)}(4.5, -sqrt(7.6**2 - 4.5**2))
        .. tension 1.5
        .. {dir(90)}(9, 0);
}
guide path_SEL8nel() {
    return subpath(path_SEL8NEL8(), 0, 1);
}

guide path_SEL8(real ha = -90, real tn = 0.8, real ta = 0, real d = -55, real len = 7.3, pair dz = (0, 0)) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(dz + rpair(len, d));
}

guide path_SEL8_up() {
    return path_SEL8(ta = 60, dz = (0, 1.4));
}

guide path_SEL8F() {
    return path_SEL8(ta = 30, dz = (0, 0.4));
}

guide path_SEL8_smooth(real ta = 0) {
    return path_SEL8(ta = ta);
}


guide path_SEL4NEL4(real ha = -96, real ta = 0, real d = -50) {
    // haisa
    write("TODO");
    return (0.0, 0.0){dir(ha)} .. tension 0.9 and 1.3 .. {dir(ta)}rpair(3.5, d);
}
guide path_SEL4nel() {
    return subpath(path_SEL4NEL4(), 0, 1);
}

guide path_SEL4(real ha = -90, real tn = 0.9, real ta = 0, real d = -50, real
len = 4.0, pair dz = (0, 0)) {
    write("TODO");
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(dz + rpair(len, d));
}

guide path_SEL4_up() {
    write("TODO");
    return path_SEL4(ta = 60, dz = (0, 1.4));
}

guide path_SEL4F() {
    write("TODO");
    return path_SEL4(ta = 30, dz = (0, 0.4));
}

guide path_SEL4_smooth(real ta = 0) {
    write("TODO");
    return path_SEL4(ta = ta);
}

guide path_SE0_3() {
    return (0, 0) -- rpair(0.3, -45);
}

guide path_SE1() {
    return (0, 0) -- rpair(1, -45);
}

guide path_NE1_5(real a = 30) {
    // n
    return (0, 0) -- rpair(1.5, a);
}

guide path_NE2_4(real a = 30) {
    // nen
    return (0, 0) -- rpair(2.4, a);
}

guide path_NE3_3(real a = 33) {
    // fu
    return (0, 0) -- rpair(3.3, a);
}

guide path_NE4(real a = 35) {
    return (0, 0) -- rpair(4, a);
}

guide path_NE7_8(real a = 38) {
    return (0, 0) -- rpair(7.8, a);
}

guide path_ENW4(guide base, real a = 125.7) {
    return base -- (lastpoint(base) + rpair(4, a));
}

guide path_ENW1(guide base, real a = 125.7) {
    return base -- (lastpoint(base) + rpair(1, a));
}

guide path_E8NW4(real a = 125.7) {
    // ken
    return path_ENW4(path_E8(), a); 
}

guide path_SEL16NEL16() {
    return (0.0, 0.0){dir(-90)}              .. tension 1.5 ..
    {dir(0)}(8.0, -sqrt(16 ** 2 - 8.0 ** 2)) .. tension 1.5 ..
    {dir(90)}(16.0, 0.0);
}

guide path_SEL16(real ha = -90, real tn = 0.88, real ta = 0, real d = -60, pair dz = (0, 0)) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(rpair(16, d) + dz);
}

guide path_SEL16_up() {
    return path_SEL16(ta = 60, dz = (0, 2.7));
}

guide path_SEL16F() {
    return path_SEL16(ta = 30, dz = (0, 0.4));
}

guide path_SEL16nel() {
    return subpath(path_SEL16NEL16(), 0, 1);
}

guide path_SEL16_smooth(real ta = 60) {
    return path_SEL16(ta = ta);
}

guide path_SEL16NW4(guide base = path_SEL16(), real a = 125.7) {
    return base -- (lastpoint(base) + rpair(4, a));
}

guide path_E4NW1(real a = 125.7) {
    // keizai
    return path_ENW1(path_E4(), a); 
}

guide path_E16NW4(real a = 125.7) {
    // kerx
    return path_ENW4(path_E16(), a); 
}


guide path_S1() {
    return (0, 0) -- (0, -1);
}

guide path_S2() {
    return (0, 0) -- (0, -2);
}


guide path_S4() {
    return (0, 0) -- (0, -4);
}

guide path_S8() {
    return (0, 0) -- (0, -8);
}

guide path_SE1(real a = -60) {
    return (0, 0) -- rpair(1, a);
}

guide path_SE2(real a = -60) {
    return (0, 0) -- rpair(2, a);
}
guide path_SE3_4(real a = -42.6) {
    return (0, 0) -- rpair(3.4, a);
}

guide path_SE4(real a = -60) {
    return (0, 0) -- rpair(4, a);
}

guide path_SE8(real a = -60) {
    return (0, 0) -- rpair(8, a);
}

guide path_SE8NE1(real a = -60) {
    return path_SE8() ++ rpair(1.5, 45);
}

guide path_SE16(real a = -60) {
    return (0, 0) -- rpair(16, a);
}

guide path_SE20(real a = -55) {
    return (0, 0) -- rpair(20, a);
}

guide path_EN4(guide base, real a = 90) {
    return base -- (lastpoint(base) + rpair(4, a));
}

guide path_E8N4(real a = 90) {
    return path_EN4(path_E8(), a);
}

guide path_E16N4(real a = 90) {
    return path_EN4(path_E16(), a);
}

guide path_SWLSEL4(real ha = -164, real ta = 19) {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(3.0, -124);
    pair z2 = z1 + rpair(2.0, -17);
    guide g = z0{dir(ha)} .. tension 1.4 .. z1{dir(-71)} .. tension 0.95 .. {dir(ta)}z2;

    return g;
}



guide path_E8CL4() {
    real a = -135;
    real b0 = 2;
    real b1 = -5;
    guide base = bend(scale(0.8) * path_E8(), b0);

    pair z0 = lastpoint(base);
    pair z3 = point(base, 0.7);
    pair z2 = z3 - rpair(2.5, a + b1);

    return base .. bend(z2 -- z3, b1);
}

guide path_E8CL4er(real a) {
    real b = 5;
    guide base = bend(path_E8(), b);

    pair z1 = lastpoint(base) + (0, 0.6);
    pair z2 = z1 + rpair(2, 125);
    pair z3 = z1 + rpair(3, 175);

    return base .. {dir(180)}z2 .. z3 .. {dir(a)}z1;
}

guide path_E8CL4e(real a) {
    real b = 2;
    guide base = bend(path_E8(), b);

    pair z1 = lastpoint(base) + (0, 0.2);
    pair z2 = z1 + rpair(2.4, 125);
    pair z3 = z1 + rpair(2.8, 180);

    return base .. {dir(180)}z2 .. {dir(0)}z3 -- z1;
}

guide path_E8CL4el(real a) {
    real b = -1;
    guide base = path_Ecl4(path_E8());

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1);
    pair z2 = z3 - rpair(2, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E8CL4swr(real a) {
    real b = 10;
    guide base = path_Ecl4(path_E8());

    pair z1 = lastpoint(base);
    pair z3 = point(base, 2.0/3);
    pair z2 = z3 - rpair(1.8, a + b);

    return base .. tension 1.5 .. bend(z2 -- z3, b);
}

guide path_E8CL4ne(real a) {
    real b = -5;
    guide base = bend(scale(0.9) * path_E8(), 0);

    pair z0 = lastpoint(base);
    pair z2 = point(base, 2.0/3);
    pair z1 = z2 - rpair(3.5, a + b - 180);

    return base .. bend(z1 -- z2, b);
}

guide path_E8CL4sw(real a = -130) {
    real b = 2;
    guide base = bend(scale(0.8) * path_E8(), b);

    pair z1 = lastpoint(base);
    pair z3 = point(base, 0.7);
    pair z2 = z3 - rpair(2, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_E8CL4s(real a = -90) {
    real b = 5;
    guide base = path_Ecl4(path_E8());

    pair z1 = lastpoint(base);
    pair z3 = point(base, 2.0/3);
    pair z2 = z3 - rpair(1.8, a + b);

    return base .. tension 1.5 .. {dir(a)}bend(z2 -- z3, b);
}

guide path_E8CL4se(real a = -90) {
    real b = 5;
    guide base = path_Ecl4(path_E8());

    pair z1 = lastpoint(base);
    pair z3 = point(base, 2.0/3);
    pair z2 = z3 - rpair(1.5, a);

    return base .. tension 1.5 .. {dir(a)}z2 -- z3;
}


guide path_E8CL4nel(real a) {
    real b = 2;
    guide base = bend(path_E8(), b);

    pair z1 = lastpoint(base) + (0, 0.6);
    pair z2 = z1 + rpair(2.5, 125);
    pair z3 = z1 - rpair(3, 180);

    return base .. {dir(180)}z2 .. z3 .. {dir(a)}z1;
}

guide path_E8CL4ser(real a) {
    real b = 5;
    guide base = path_Ecl4(path_E8());

    pair z1 = lastpoint(base);
    pair z3 = point(base, 0.65);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. tension 1.5 .. bend(z2 -- z3, b);
}

guide path_E8CL4sel(real a) {
    real b = -20;
    guide base = path_Ecl4(path_E8());

    pair z1 = lastpoint(base);
    pair z3 = point(base, 2.0/3);
    pair z2 = z3 - rpair(2, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E8CL4sr(real a) {
    real b = 5;
    guide base = path_Ecl4(path_E8());

    pair z1 = lastpoint(base);
    pair z3 = point(base, 0.7);
    pair z2 = z3 - rpair(1.5, a + b);

    return base .. tension 1.5 .. bend(z2 -- z3, b);
}

guide path_E8CL4sl(real a) {
    real b = -5;
    guide base = bend(scale(0.8) * path_E8(), 2);

    pair z1 = lastpoint(base);
    pair z3 = point(base, 2.0/3);
    pair z2 = z3 - rpair(2.5, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_E8CL4swl(real a) {
    real b = -5;
    guide base = bend(scale(0.8) * path_E8(), 2);

    pair z1 = lastpoint(base);
    pair z3 = point(base, 2.0/3);
    pair z2 = z3 - rpair(2.5, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_CL1E(real len = 8) {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(0.9, 134);
    pair z2 = z1 + rpair(0.8, -146);
    pair z3 = z2 + rpair(0.7, -24);
    guide c = z0{dir(90)} .. tension 0.85 .. z1{dir(180)} .. tension 1.15 .. z2{dir(-90)} .. tension 1.05 .. z3{dir(1)};
    pair z4 = (xpart(min(c)), 0) + rpair(len, 0);

    guide g = c .. {dir(0)}z4;

    return shift(-xpart(min(g)), 0) * g;
}
/*
   guide path_EL8(real ha = -18, real tn = 1.7, real ta = 80) {
   return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(8, 0);
   }

   guide path_EL8CL1(guide base = path_EL8()) {
   real b = 5;
   pair z1 = lastpoint(base);
   pair z3 = arcpoint(-base, 0.7);
   pair z2 = z3 - rpair(1.2, -60 + b);

   return base .. tension 1.2 .. bend(z2 -- z3, -b); 
   }

 */

guide path_ER16cr1() {
    return (0, 0){dir(23)} .. tension 2.05 .. {dir(-90)}rpair(16, 4);
}

guide path_ER8(real ha = 23, real tn = 1.5, real ta = -90) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(8, 0);
}

guide path_ER8_smooth(real ta = -90) {
    return path_ER8(ta = ta, tn = 1.0);
}

guide path_ER8swr(real ta = 35, real tn = 1.3) {
    return path_ER8(ta = ta, tn = tn);
}

guide path_ER8_down(real ta = -110) {
    return path_ER8(ta = ta);
}

guide path_ER8cr1() {
    return (0, 0){dir(26)} .. tension 2.05 .. {dir(-90)}rpair(8.0, 4);
}


guide path_ERCR1(guide base = path_ER8cr1()) {
    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(1.2, -144);
    pair z3 = z2 + rpair(0.7, 75);
    pair z4 = z3 + rpair(0.7, 46);

    pair end = dirpoint(base, 67-90);

    guide g = base .. tension 0.75 and 2.05 .. {dir(180)}z2 .. tension 0.75 and 0.95 .. z3{dir(44)} .. tension 1 .. {dir(67)}end;

    return g;
}

guide path_ER4(real ha = 30, real tn = 1.2, real ta = -90) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(4, 0);
}

guide path_ER4_smooth(real ta = -90) {
    return path_ER4(ta = ta, tn = 1.0);
}

guide path_ER4_down(real ta = -110) {
    return path_ER4(ta = ta);
}

guide path_ER4cr1(real ha = 28, real tn1 = 1.75, real tn2 = 1.1, real ta = -90) {
    return (0, 0){dir(ha)} .. tension tn1 and tn2 .. {dir(ta)}rpair(4, 4);
}

guide path_ER8CR1() {
    return path_ERCR1();
}

guide path_ER16CR1() {
    return path_ERCR1(base = path_ER16cr1());
}


guide path_ERCR1er(guide base = path_ER8cr1(), real a) {
    real b = 5;
    pair z1 = lastpoint(base);
    //pair z3 = dirpoint(base, a - 80);
    pair z3 = xpoint(base, xpart(z1) - 0.2);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1er(real a) {
    return path_ERCR1er(a = a);
}

guide path_ER16CR1er(real a) {
    return path_ERCR1er(base = path_ER16cr1(), a);
}


guide path_ERCR1nel(guide base = path_ER8cr1(), real a) {
    real b = -7;

    pair z1 = lastpoint(base);
    //pair z3 = dirpoint(base, a - 80);
    pair z3 = ypoint(base, ypart(z1) + 0.4, 1);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1nel(real a = 15) {
    return path_ERCR1nel(a = a);
}

guide path_ER16CR1nel(guide base = path_ER16cr1(), real a) {
    real b = -7;

    pair z1 = lastpoint(base);
    pair z3 = dirpoint(base, a - 85);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. bend(z2 -- z3, b);
}
/*
   guide path_ER16CR1nel(real a = 15) {
   return path_ERCR1nel(base = path_ER16cr1(), a = a);
   }
 */

guide path_ERCR1el(guide base = path_ER8cr1(), real a) {
    real b = -3;

    pair z0 = lastpoint(base);
    pair z1 = z0 + rpair(0.8, -150);
    base = base .. {dir(180)}z1;
    pair z3 = arcpoint(-base, 0.9);
    pair z2 = z3 - rpair(1, a + b);

    return base .. bend(z2 -- z3, b); 
}

guide path_ER8CR1el(real a) {
    return path_ERCR1el(a = a);
}

guide path_ER16CR1el(guide base = path_ER16cr1(), real a) {
    real b = -3;

    pair z0 = lastpoint(base);
    pair z1 = z0 + rpair(0.8, -150);
    base = base .. {dir(180)}z1;
    pair z3 = arcpoint(-base, 1.0);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. bend(z2 -- z3, b);
}

/*
   guide path_ER16CR1el(real a) {
   return path_ERCR1el(base = path_ER16cr1(), a = a);
   }
 */

guide path_ERCR1e(guide base = path_ER8cr1(), real a) {
    real b = 3;
    pair z0 = lastpoint(base);
    pair z1 = z0 + rpair(1.0, -150);
    base = base .. {dir(180)}z1;
    //pair z3 = arcpoint(-base, 1.3);
    pair z3 = ypoint(base, ypart(z1) + 0.8, 1);
    pair z2 = z3 - rpair(1.2, a + b);

    return base .. bend(z2 -- z3, b); 
}

guide path_ER8CR1e(real a) {
    return path_ERCR1e(a = a);
}

guide path_ER16CR1e(real a) {
    return path_ERCR1e(base = path_ER16cr1(), a = a);
}

guide path_ERCR1s(guide base = path_ER8cr1(), real a) {
    real b = 5;
    pair z1 = lastpoint(base);
    //pair z3 = arcpoint(-base, 1.2);
    pair z3 = xpoint(base, xpart(z1) - 1);
    pair z2 = z3 - rpair(0.7, 90 + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1s(real a) {
    return path_ERCR1s(a = a);
}

guide path_ER16CR1s(real a) {
    return path_ERCR1s(base = path_ER16cr1(), a = a);
}

guide path_ERCR1sel(guide base = path_ER8cr1()) {
    real b = 5;

    pair z1 = lastpoint(base);
    //pair z3 = arcpoint(-base, 1.3);
    pair z3 = xpoint(base, xpart(z1) - 1);
    pair z2 = z3 - rpair(0.7, 90 + b);

    return base .. bend(z2 -- z3, b);
}


guide path_ER8CR1sel() {
    return path_ERCR1sel();
}

guide path_ER16CR1sel() {
    return path_ERCR1sel(base = path_ER16cr1());
}

guide path_ERCR1sl(guide base = path_ER8cr1()) {
    real b = 5;

    pair z1 = lastpoint(base);
    //pair z3 = arcpoint(-base, 1.3);
    pair z3 = xpoint(base, xpart(z1) - 1.3);
    pair z2 = z3 - rpair(0.7, 90 + b);

    return base .. bend(z2 -- z3,b,1);
}

guide path_ER8CR1sl() {
    return path_ERCR1sl();
}

guide path_ER16CR1sl() {
    return path_ERCR1sl(base = path_ER16cr1());
}

guide path_ERCR1swl(guide base = path_ER8cr1()) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.5);
    pair z2 = z3 - rpair(0.7, 90 + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1swl() {
    return path_ERCR1sel();
}

guide path_ER16CR1swl() {
    return path_ERCR1sel(base = path_ER16cr1());
}

guide path_ERCR1sw(guide base = path_ER8cr1()) {
    real b = 5;

    pair z1 = lastpoint(base);
    //pair z3 = arcpoint(-base, 1.3);
    pair z3 = xpoint(base, xpart(z1) - 1);
    pair z2 = z3 - rpair(0.7, 90 + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1sw() {
    return path_ERCR1sw();
}

guide path_ER16CR1sw() {
    return path_ERCR1sw(base = path_ER16cr1());
}

guide path_ERCR1ne(guide base = path_ER8cr1(), real a) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.7);
    pair z2 = z3 - rpair(0.9, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1ne(real a) {
    return path_ERCR1ne(a);
}

guide path_ER16CR1ne(real a) {
    return path_ERCR1ne(base = path_ER16cr1(), a = a);
}

guide path_ERCR1F(guide base = path_ER8CR1ne(45)) {
    real a = 45;

    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(1.5, a);

    return base .. z2;
}

guide path_ER8CR1F() {
    return path_ERCR1F();
}

guide path_ER16CR1F() {
    return path_ERCR1F(base = path_ER16cr1());
}

guide path_ERCR1ner(guide base = path_ER8cr1(), real a) {
    real b = 8;

    pair z1 = lastpoint(base);
    //pair z3 = arcpoint(-base, 1.1);
    pair z3 = xpoint(base, xpart(z1) - 0.9);
    pair z2 = z3 - rpair(0.8, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1ner(real a) {
    return path_ERCR1ner(a);
}

guide path_ER16CR1ner(real a) {
    return path_ERCR1ner(base = path_ER16cr1(), a = a);
}

guide path_ERCR1swr(guide base = path_ER8cr1()) {
    real b = 5;

    pair z1 = lastpoint(base);
    //pair z3 = arcpoint(-base, 1.5);
    pair z3 = xpoint(base, xpart(z1) - 1.2);
    pair z2 = z3 - rpair(0.7, 90 + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1swr() {
    return path_ERCR1swr();
}

guide path_ER16CR1swr() {
    return path_ERCR1swr(base = path_ER16cr1());
}

guide path_ERCR1se(guide base = path_ER8cr1(), real a) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z4 = z1 + rpair(1.0, -150);
    base = base .. {dir(180)}z4;
    pair z3 = arcpoint(-base, 0.7);
    pair z2 = z3 - rpair(0.8, a);

    return base .. {dir(a)}z2--z3;
}

guide path_ER8CR1se(real a) {
    return path_ERCR1se(a);
}

guide path_ER16CR1se(real a) {
    return path_ERCR1se(base = path_ER16cr1(), a = a);
}

guide path_ERCR1ser(guide base = path_ER8cr1(), real a) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z4 = z1 + rpair(0.9, -150);
    base = base .. {dir(180)}z4;
    pair z3 = arcpoint(-base, 0.9);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1ser(real a) {
    return path_ERCR1ser(a);
}

guide path_ER16CR1ser(real a) {
    return path_ERCR1ser(base = path_ER16cr1(), a = a);
}

guide path_ERCR1sr( guide base = path_ER8cr1(), real a) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z4 = z1 + rpair(1.0, -150);
    base = base .. {dir(180)}z4;
    pair z3 = arcpoint(-base, 0.8);
    pair z2 = z3 - rpair(0.9, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_ER8CR1sr(real a) {
    return path_ERCR1sr(a);
}

guide path_ER16CR1sr(real a) {
    return path_ERCR1sr(base = path_ER16cr1(), a = a);
}

guide path_ER8CR4() {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(5.2, 15);
    pair z2 = z0 + rpair(7.8, -2);
    pair z3 = z2 + rpair(2.6, -180);
    guide base = z0{dir(23)} .. tension 0.8 and 1.3 .. z1{dir(0)} .. tension 1.25 and 0.95 .. z2{dir(-90)} .. tension 0.9 and 1.9 .. {dir(145)}z3;
    pair z4 = point(base, 0.7);

    return  base .. z4;
}


guide path_ER8SWR4(guide base = path_ER8(), real ta = -160, pair dz = (0, 0)) {
    pair z2 = lastpoint(base) + rpair(4, -135);

    return base .. {dir(ta)}(z2 + dz);
}

guide path_ER8SWR4_up() {
    return path_ER8SWR4(ta = 145, dz = (-1.0,0.6));
}

guide path_ER8SWR4er(real ta = 160) {
    return path_ER8SWR4(ta = ta + 180, dz = (-2.0, 0.6));
}


guide path_ER8SWR4ner(real ta = -160) {
    return path_ER8SWR4(ta = ta + 160, dz = (0.8, -0.8));
}

guide path_ER8SWR4ne(real ta = -160) {
    return path_ER8SWR4(ta = ta + 180, dz = (0.8, -0.8));
}

guide path_ER8SWR4nel(real ta = -160) {
    return path_ER8SWR4(ta = ta + 180, dz = (0.0, -0.5));
}

guide path_N4(real a = 90) {
    return (0, 0) -- rpair(4, a);
}

guide path_serN4(guide ser) {
    pair z0 = lastpoint(ser);
    pair z1 = z0 + rpair(3.6, 89);
    return ser -- z1;
}

guide path_CL1SEL8NW4(real a = 120) {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(1.0, 60);
    pair z2 = z1 + rpair(0.7, 137);
    pair z3 = z2 + rpair(0.7, -107);
    pair z4 = z3 + rpair(3.7, -66);
    pair z5 = z4 + rpair(4.7, -14);
    pair z6 = z5 + rpair(2.8, a);
    guide g = z0{dir(30)} .. z1{dir(109)} .. tension 1.1 and 0.75 .. z2{dir(-170)} .. tension 0.75 and 1.05 .. z3{dir(-80)} .. tension 1.1 and 2 .. z4{dir(-48)} .. tension 0.85 and 2 .. {dir(43)}z5{dir(a)} .. tension 1.1 .. {dir(a)}z6;

    return g;
}

guide path_EL4(real ha = -28, real tn = 1.2, real ta = 80) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(4, 0);
}

guide path_EL4_tangent(real ha = -28, real tn = 1.2, real ta = 80) {
    return path_EL4(ha, tn, ta + 180); 
}

guide path_EL4_flat(real ha = -28, real tn = 1.2, real ta = 60) {
    return path_EL4(ha, tn, ta); 
}

guide path_EL4_up(real ha = -28, real tn = 1.2, real ta = 90) {
    return path_EL4(ha, tn, ta); 
}

guide path_EL8(real ha = -18, real tn = 1.7, real ta = 80) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(8, 0);
}

guide path_EL8_smooth(real tn =  0.75, real ta = 80) {
    return path_EL8(tn = tn, ta = ta);
}

guide path_EL8_tangent(real ta = 80) {
    return path_EL8(ta = ta + 180);
}

guide path_EL8_up(real ta = 90) {
    return path_EL8(ta = ta);
}

guide path_EL8_flat(real ta = 60) {
    return path_EL8(ta = ta);
}

guide path_EL8S1(real len = 1.5) {
    return path_EL8() ++ (0, -len);
}


guide path_EL8CL1(guide base = path_EL8(ta = 90)) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.7);
    pair z2 = z3 - rpair(1.4, -60 + b);

    return base .. tension 1.2 .. bend(z2 -- z3, -b);
}

guide path_EL8CL1sw(guide base = path_EL8(ta = 90), real a = -120) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.5);
    pair z2 = z3 - rpair(1.3, a);

    return base .. {dir(a)}z2 -- z3; 
}

guide path_EL8CL1s(guide base = path_EL8(ta = 90), real a = -90) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.2);
    pair z2 = z3 - rpair(1.2, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_EL8CL1se(guide base = path_EL8(ta = 90), real a = -60) {
    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.8);
    pair z2 = z3 - rpair(1.2, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_EL8CL1e(guide base = path_EL8(ta = 90), real a = 0) {
    real b = 3;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.2);
    pair z2 = z3 - rpair(0.8, a + b);

    return base .. {dir(a)}bend(z2 -- z3, b);
}

guide path_EL8CL1ne(guide base = path_EL8(ta = 90), real a = 60) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 2.3);
    pair z2 = z3 - rpair(1.3, (a + 180));

    return base .. {-dir(a)}z2 -- z3; 
}

guide path_EL8CL1swl(guide base = path_EL8(ta = 90), real a = -120) {
    real b = -5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 2.0);
    pair z2 = z3 - rpair(0.7, a + b);

    return base .. bend(z2 -- z3, b); 
}

guide path_EL8CL1sl(guide base = path_EL8(ta = 90), real a = -120) {
    real b = -5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 2.0);
    pair z2 = z3 - rpair(0.7, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_EL8CL1sel(guide base = path_EL8(ta = 90), real a = -90) {
    real b = -8;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.3);
    pair z2 = z3 - rpair(1.3, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_EL8CL1el(guide base = path_EL8(ta = 90), real a = -20) {
    real b = -10;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.3);
    pair z2 = z3 - rpair(1.2, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_EL8CL1nel(guide base = path_EL8(ta = 90), real a = 30) {
    real b = -5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.1);
    pair z2 = z3 - rpair(0.6, a + b);

    return base .. bend(z2 -- z3, b);  
}

guide path_EL8CL1swr(guide base = path_EL8(ta = 90), real a = -90) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.1);
    pair z2 = z3 - rpair(1.3, a + b);

    return base .. bend(z2 -- z3, b);  
}

guide path_EL8CL1sr(guide base = path_EL8(ta = 90), real a = -60) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.8);
    pair z2 = z3 - rpair(1.2, a);

    return base .. {dir(a)}z2--z3;
}

guide path_EL8CL1ser(guide base = path_EL8(ta = 90), real a = -30) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.5);
    pair z2 = z3 - rpair(1.0, a + b);

    return base .. bend(z2 -- z3, b);
}

guide path_EL8CL1er(guide base = path_EL8(ta = 60), real a = 30) {
    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(0.8, 135);
    pair z3 = z2 + rpair(0.9, -140);
    pair z4 = arcpoint(-base, 0);
    guide g = base .. z2{dir(180)} .. tension 1.3 .. z3{dir(-90)} .. tension 0.75 .. {dir(a)}z4;

    return g;
}

guide path_EL8CL1ner(guide base = path_EL8(ta = 90), real a = 60) {
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.8);
    pair z2 = z3 - rpair(0.7, (a + 170));

    return base .. {dir (a + 180)}z2 -- z3; 
}

guide path_SL8(real ha = -120, real tn = 1.4, real ta = -30, pair dz = (0, 0)) {
    return (0, 0){dir(ha)} ..tension tn .. {dir(ta)}((0, -8) + dz);
}

guide path_SL8cl1(guide base = rotate(-5) * path_SL8()) {
    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(1.2, 30);

    return base .. z2;
}

guide path_SL8CL1(guide base = path_SL8cl1()) {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(7.5, -97);
    pair z2 = z1 + rpair(1.2, 28);
    pair z3 = z2 + rpair(1.1, -141);
    guide g = z0{dir(-113)} .. tension 1.1 and 1.55 .. {dir(-57)}z1{dir(-57)} .. tension 1.15 and 1.2 .. {dir(109)}z2{dir(109)} .. tension 1.45 and 1.3 .. {dir(-127)}z3;

    return g;
}


guide path_SWCL4() {
    // kotaeru, okonau
    guide g = (0.0, 0.0){dir(-168)}    .. tension 1.6 and 1.4   ..
    {dir(-126)}(-3.2, -2.6){dir(-127)} .. tension 1.0 and 1.4   ..
    {dir(-74)}(-3.6, -3.5){dir(-59)}   .. tension 1.2 and 1.0   ..
    {dir(23)}(-2.9, -3.5){dir(27)}     .. tension 1.2 and 1.3   ..
    {dir(61)}(-0.2, -0.6){dir(63)}     .. tension 1.1 and 1.7   .. 
    {dir(135)}(0.0, 0.0);

    return g;
}

guide path_SESW4(real a = 166) {
    pair z0 = (0, 0);
    pair z1 = z0 + rpair(2.6, -48);
    pair z2 = z1 + rpair(2.3, -151);
    guide g = z0{dir(-25)} .. tension 1.05 and 0.9 .. {dir(-90)}z1
        .. tension 0.9 and 1.1 .. {dir(a)}z2;

    return g;
}

/*
   guide path_SR8CR1e() {
// shu_ka
guide g = (0.0, 0.0){dir(-59)}     .. tension 1.4 and 1.8 .. 
{dir(-126)}(1.6, -11.0){dir(-121)} .. tension 1.4 and 1.0 .. 
{dir(141)}(0.0, -11.9){dir(157)}   .. tension 1.2 and 1.0 .. 
{dir(28)}(-0.2, -10.7){dir(29)}    .. tension 1.0 and 1.0 ..
{dir(0)}(0.9, -10.6){dir(0)}       .. tension 0.8 and 1.6 .. 
{dir(0)}(1.8, -10.6);

return g;
}

guide path_SR8CR1er(real a = 24) {
// shu_ma
guide g = (0.0, 0.0){dir(-51)}   .. tension 1.5 and 2.6 .. 
{dir(-153)}(0.8,-9.4){dir(-152)} .. tension 1.2 and 0.8 .. 
{dir(45)}(-0.1, -8.8){dir(42)}   .. tension 1.1 and 0.9 .. 
{dir(a)}(1.3, -7.9);

return g;
}

guide path_SR8CR1el(real a = -23) {
// shu_na
guide g = (0.0, 0.0){dir(-44)}    .. tension 1.1 and 1.3 .. 
{dir(-141)}(0.9, -7.3){dir(-141)} .. tension 1.1 and 1.0 .. 
{dir(101)}(-0.3, -7.1){dir(101)}  .. tension 1.5 and 0.8 .. 
{dir(-34)}(0.1, -6.7){dir(-34)}   .. tension 1.0 and 1.0 .. 
{dir(-23)}(1.0, -7.2);

return g;
}
 */

guide path_SR8CR1ne(real a = 45) {
    // shu_cha
    return (0.0, 0.0){dir(-61)}       .. tension 1.2 and 1.3 
        .. {dir(-149)}(-0.5,-9.4){dir(-146)} .. tension 1.1 and 0.8 
        .. {dir(49)}(-0.4, -8.5){dir(46)}    .. tension 1.0 and 1.0 
        .. {dir(a)}(0.9, -7.3);
}

/*
   guide path_SR8CR1nel(real a = 34) {
// shu_sa
guide g = (0.0, 0.0){dir(-53)}     .. tension 1.1 and 1.2 .. 
{dir(-121)}(1.5, -10.4){dir(-124)} .. tension 1.1 and 1.1 .. 
{dir(180)}(0.6, -11.1){dir(180)}   .. tension 1.2 and 1.2 .. 
{dir(82)}(-0.2, -10.3){dir(82)}    .. tension 1.1 and 1.1 .. 
{dir(27)}(0.5, -10.0){dir(24)}     .. tension 1.0 and 0.9 .. 
{dir(a)}(2.0, -9.1);

return g;
}
 */

guide path_SR8(real a0 = -56, real tn = 1.2, real a1 = -142, pair dz = (0, 0)) {
    guide g = (0.0, 0.0){dir(a0)} .. tension tn .. {dir(a1)}(shift(dz) * (0.0, -8.0));
    return g;
}

guide path_SR8_up() {
    return path_SR8(a1 = 120, dz = (-1.0, -0.8));
}

guide path_SR8_tangent(real a = -142) {
    return path_SR8(a1 = a + 180);
}

guide path_SR8cr1(guide base = path_SR8()) {
    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(0.6, 135);

    return base .. z2;
}

guide path_SR8CR1(guide base = path_SR8cr1()) {
    real a = 45;
    int b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(reverse(base), 2.5);
    pair z2 = z3 - rpair(1, a + b);

    return base .. {dir(a)}z3;
}


/*
   vardef base_shu=
   clearxy; save base; path base;
   save a; a = 45;
   save b; b = 5;

   base = subbase_shu;

   z1 = lastpoint of base;
   z3 = arcpoint -2.5mm of base;
   z3 - z2 = polar(1.0mm, a+b);

   base..{dir a}z3

   enddef;
 */

guide path_SR8CR1er(guide base = path_SR8cr1(), real a = 30) {
    int b = 5;

    pair z3 = arcpoint(reverse(base), 2.5);

    return base .. {dir(a)}z3;
}

/*
   vardef base_shu_ma(expr _a)=
   clearxy; save base; path base;
   save a; a = _a;
   save b; b = 5;

   base = subbase_shu;

   z1 = lastpoint of base;
   z3 = arcpoint -2.5mm of base;
   z3 - z2 = polar(1.0mm, a+b);

   base..{dir a}z3

   enddef;
 */

guide path_SR8CR1e(guide base = path_SR8cr1(), real a = 0, int b = 5) {
    pair z3 = arcpoint(reverse(base), 1.3);
    pair z2 = z3 - rpair(1, a + b);

    return base .. bend(z2 -- z3, b, 1);
}

/*
   vardef base_shu_ka(expr _a)=
   clearxy; save base; path base;
   save a; a = _a;
   save b; b = 5;

   base = base_sha;

   z1 = lastpoint of base;
   z3 = arcpoint -1.3mm of base;
   z3 - z2 = polar(1.0mm, a+b);

   base..bend(z2--z3, b, 1)

   enddef;

 */

guide path_SR8CR1el(guide base = path_SR8cr1(), real a = 0, int b = -5) {
    pair z3 = arcpoint(reverse(base), 0.6);
    pair z2 = z3 - rpair(0.8, a + b);

    return base .. bend(z2 -- z3, b, 1);
}

/*
   vardef base_shu_na(expr _a)=
   clearxy; save base; path base;
   save a; a = _a;
   save b; b = -5;

   base = base_sha;

   z1 = lastpoint of base;
   z3 = arcpoint -0.6mm of base;
   z3 - z2 = polar(0.8mm, a+b);

   base..bend(z2--z3, b, 1)

   enddef;
 */


//vardef base_shu_ya(expr _a)=
//clearxy; save base; path base;
//save a; a = _a-20;
//save b; b = 1;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -2.6mm of base;
//z3 - z2 = polar(1.3mm, a+b);
//
//base..{dir a}z3
//
//enddef;
//
//vardef base_shu_koi(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 5;
//
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -2.1mm of base;
//z3 - z2 = polar(1.9mm, a+b);
//
//base..bend(z2--z3, b, 1)
//
//enddef;
//
//
//vardef base_shu_sa(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = -5;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -1.6mm of base;
//z3 - z2 = polar(1.9mm, a+b);
//
//base..bend(z2--z3, b, 1)
//
//enddef;
//
//
//vardef base_shu_node(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 5;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.3mm of base;
//z3 - z2 = polar(0.2mm, a+b);
//
//base..bend(z2--z3, b, 1)
//
//enddef;
//vardef base_shu_o(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 10;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.5mm of base;
//z3 - z2 = polar(0.8mm, a+b);
//z4 - z1 =polar(0.6mm, 135);
//
//base..z4..bend(z2--z3, b, 1)
//
//enddef;
//
//
//
//vardef base_shu_hya(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 10;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.5mm of base;
//z3 - z2 = polar(0.8mm, a+b);
//z4 - z1 =polar(0.6mm, 135);
//
//base..z4..bend(z2--z3, b, 1)
//
//enddef;
//
//vardef base_shu_sha(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 10;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.2mm of base;
//z3 - z2 = polar(0.8mm, a+b);
//z4 - z1 =polar(1.0mm, 175);
//
//base..z4..bend(z2--z3, b, 1)
//
//enddef;
//
//vardef base_shu_e(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 4;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.4mm of base;
//z3 - z2 = polar(0.6mm, a+b);
//z4 - z1 =polar(1.0mm, 175);
//
//base..bend(z2--z3, b, 1)
//
//enddef;
//
//vardef base_shu_u(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 0;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.1mm of base;
//z3 - z2 = polar(0.5mm, a+b);
//z4 - z1 =polar(1.0mm, 175);
//
//base..bend(z2--z3, b, 1)
//
//enddef;
//
//vardef base_shu_ra(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = 4;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.7mm of base;
//z3 - z2 = polar(0.7mm, a+b);
//z4 - z1 =polar(1.0mm, 175);
//
//base..bend(z2--z3, b, 1)
//
//enddef;
//
//vardef base_shu_ha(expr _a)=
//clearxy; save base; path base;
//save a; a = _a;
//save b; b = -5;
//
//base = base_sha;
//
//z1 = lastpoint of base;
//z3 = arcpoint -0.2mm of base;
//z3 - z2 = polar(1.0mm, a+b);
//z4 - z1 =polar(0.8mm, 140);
//
//base..z4..bend(z2--z3, b, 1)
//
//enddef;


guide path_E8CR1NE1F() {
    // keredomo, kankei, kamo, kakin
    return (0.0, 0.0){dir(-10)}       .. tension 2.2 and 2.4 ..
    {dir(15)}(8.2, 0.2){dir(15)}      .. tension 0.9 and 1.1 ..
    {dir(8)}(9.0, 0.4){dir(0)}        .. tension 1.4 and 0.8 ..
    {dir(-136)}(9.1, -0.5){dir(-135)} .. tension 0.8 and 1.9 ..
    {dir(135)}(8.1, -0.8){dir(127)}   .. tension 1.3 and 1.2 ..
    {dir(53)}(8.3, -0.3){dir(49)}     .. tension 1.1 and 0.8 ..
    {dir(54)}(10.0, 1.7);
}


guide path_EL8NWL4(guide base = path_EL8(), real a = 180) {
    // joshi_no
    pair z1 = shift(-3.0, 1.5) * lastpoint(base);

    return base .. {dir(a)}z1;
}

guide path_EL8NWL4_down(guide base = path_EL8(), real a = -150) {
    // joshi_no_yurisage
    return path_EL8NWL4(base, a);
}

guide path_EL8NWL4_tangent(guide base = path_EL8(), real a = 180) {
    // joshi_no_zenkin
    return path_EL8NWL4(base, a + 180);

}

guide path_EL8NCL4sel(real a = -83) {
    // joshi_noha
    return (0.0, 0.0){dir(-29)}    .. tension 1.5 and 1.1 ..
    {dir(57)}(8.9, 0.0){dir(56)}   .. tension 1.4 and 1.3 ..
    {dir(178)}(7.7, 2.6){dir(179)} .. tension 1.1 and 1.3 ..
    {dir(-83)}(5.6, -1.4);
}

guide path_EL8NCL4sw(real a = -102) {
    // nu_o, joshi_no_o
    return (0.0, 0.0){dir(-29)}      .. tension 1.7 and 1.1 ..
    {dir(92)}(9.1, 0.7){dir(92)}     .. tension 1.2 and 0.8 ..
    {dir(-132)}(6.8, 2.2){dir(-132)} .. tension 1.4 and 1.2 ..
    {dir(a)}(5.5, -1.3);
}

guide path_EL8NCL4sr(real a = -60) {
    // nu_sha
    return (0.0, 0.0){dir(-26)}      .. tension 1.9 and 1.1 ..
    {dir(83)}(9.1, 0.4){dir(84)}     .. tension 1.0 and 1.8 ..
    {dir(-135)}(4.2, 1.4){dir(-135)} .. tension 1.1 and 1.3 ..
    {dir(a)}(4.9, -1.2);
}

guide path_EL8NCL4se(real a = -60) {
    // nu_e, joshi_no_e
    return (0.0, 0.0){dir(-18)}    .. tension 1.7 and 1.7 ..
    {dir(90)}(9.9, 0.0){dir(90)}   .. tension 1.5 and 1.5 ..
    {dir(-54)}(5.8, 0.8){dir(-55)} .. tension 1.0 and 1.0 ..
    {dir(-60)}(7.2, -1.3);
}

guide path_EL8NCL4ser(real a = -60) {
    // nu_ra
    return (0.0, 0.0){dir(-18)}    .. tension 1.7 and 1.7 ..
    {dir(90)}(9.8, 0.0){dir(90)}   .. tension 2.0 and 2.0 ..
    {dir(-50)}(5.3, 1.2){dir(-49)} .. tension 1.0 and 1.0 ..
    {dir(a)}(7.1, -1.3);
}


guide path_EL8NCL4s(real a = -90) {
    // nu_u
    return (0.0, 0.0){dir(-18)}    .. tension 1.7 and 1.7 ..
    {dir(90)}(9.8, 0.0){dir(90)}   .. tension 1.0 and 1.0 ..
    {dir(-89)}(5.9, 1.0){dir(-90)} .. tension 1.0 and 1.0 ..
    {dir(a)}(6.0, -1.2);
}


guide path_EL8NCL4swl(real a = -123) {
    // nu_hya
    return (0.0, 0.0){dir(-26)}      .. tension 1.7 and 1.1 ..
    {dir(90)}(9.8, 0.0){dir(90)}     .. tension 0.8 and 1.0 ..
    {dir(-158)}(8.6, 0.5){dir(-159)} .. tension 1.1 and 0.9 ..
    {dir(a)}(5.9, -1.8);
}

guide path_EL8NCL4sl(real a = -123) {
    // nu_kya
    return (0.0, 0.0){dir(-26)}      .. tension 1.7 and 1.1 ..
    {dir(90)}(9.8, 0.0){dir(90)}     .. tension 0.8 and 1.0 ..
    {dir(-158)}(8.6, 0.5){dir(-159)} .. tension 1.1 and 0.9 ..
    {dir(a)}(5.9, -1.8);
}

guide path_EL8NCL4swr(real a = -90) {
    // nu_node
    return (0.0, 0.0){dir(-15)}    .. tension 1.7 and 2.2 ..
    {dir(90)}(10.0, 0.0){dir(90)}  .. tension 2.0 and 2.0 ..
    {dir(-64)}(5.6, 0.9){dir(-66)} .. tension 1.0 and 1.0 ..
    {dir(a)}(6.0, -1.0);
}

guide[] path_E3_E3() {
    // nihon
    return (0.0, 0.0) .. (3.0, 0) ^^ (0.0, -1.0) .. (3.0, -1.0);
}


guide path_1() {
    return (0.0, 0.0){dir(-116)} .. tension 1.0 and 1.0 ..
    {dir(-116)}rpair(14, -117);
}

guide path_2() {
    return
        (0.0, 0.0)   .. controls (1.4, -1.0) and (-0.0, -1.3) ..
        (-1.1, -1.9) .. controls (-0.5, -1.9) and (0.1, -1.9) ..
        (0.7, -1.9);
}

guide path_3() {
    return scale(2) * (
        (0.0, 0.0){dir(-45)} .. tension 0.9 and 0.8 .. 
        {dir(157)}(-0.1, -0.3){dir(-58)} .. tension 0.8 and 0.8 .. 
        {dir(122)}(-0.3, -0.5)
    );
    
    //return
    //    (0.0, 0.0)   .. controls (0.5, -0.5) and (0.5, -1.2)  ..
    //    (-0.2, -0.9) .. controls (0.8, -2.5) and (-0.6, -2.4) ..
    //    (-1.1, -1.6);
}

guide[] path_4() {
    return (0.0,  0.0) .. controls (-0.9, -1.0) and ( 0.4, -1.7) .. ( 1.3, -1.5) 
        ^^ (1.0, -0.7) .. controls ( 0.2, -0.9) and (-0.2, -1.9) .. (-0.5, -2.5);
}

guide[] path_5(int type = 0) {
    if (type == 0) {
        return (0.0, 0.0)
            .. controls (-0.5, -0.4)
            and (-0.9, -1.1)
            .. (-0.6, -1.6)
            .. controls (-0.1, -2.3)
            and (-0.8, -2.6)
            .. (-1.2, -2.1)
            ^^ (-0.3, -0.4)
            .. controls (0.4, -0.3)
            and (1.0, -0.5)
            .. (1.6, -0.7);
    } else {  
        return (0.0, 0.0)
            .. controls (-0.1, -1.2)
            and (-0.3, -2.0)
            .. (-0.4, -3.1)
            .. controls (-0.7, -2.8)
            and (-0.9, -2.5)
            .. (-1.2, -2.1) 
            ^^ (-0.1, -1.0)
            .. controls (0.5, -0.9)
            and (1.1, -0.8)
            .. (1.7, -0.8);
    }
}

guide path_6() {
    return (0.0, 0.0)
        .. controls (-0.8, -0.8)
        and (-1.8, -2.1)
        .. (-1.0, -2.3)
        .. controls (-0.6, -2.5)
        and (0.2, -2.0)
        .. (0.3, -1.8)
        .. controls (0.3, -1.3)
        and (-0.7, -1.5)
        .. (-1.2, -1.6);
}

guide[] path_7(int type = 0) {
    if (type == 0) {
        return (0.0, 0.0)
            .. controls (-0.2, -0.3)
            and (-0.5, -0.5)
            .. (-0.7, -0.8)
            .. controls (-0.1, -0.0)
            and (1.0, 0.0)
            .. (0.8, -0.7)
            .. controls (0.5, -1.4)
            and (0.1, -2.1)
            .. (-0.4, -2.7);
    } else {
        return (0.0, 0.0)
            .. controls (0.4, -0.2)
            and (1.0, -0.3)
            .. (1.5, -0.1)
            .. controls (1.0, -1.2)
            and (0.4, -2.3)
            .. (-0.0, -3.3);
    }
}

guide path_8() {
    return (0.0, 0.0)
        .. controls (0.2, 0.5)
        and (-0.3, 1.3)
        .. (-0.5, 1.3)
        .. controls (-1.2, 1.4)
        and (-0.8, -0.9)
        .. (-1.2, -0.9)
        .. controls (-1.6, -1.0)
        and (-1.9, -0.6)
        .. (-1.8, -0.2)
        .. controls (-1.8, 0.1)
        and (-1.0, 0.1)
        .. (-0.5, 0.2);
}

guide path_9(int type = 0) {
    if (type == 0) { 
        return (0.0, 0.0)
            .. controls (0.4, 0.3)
            and (0.4, 0.9)
            .. (0.0, 1.1)
            .. controls (-0.3, 1.2)
            and (-1.3, 0.2)
            .. (-1.1, -0.1)
            .. controls (-0.8, -0.3)
            and (-0.4, -0.1)
            .. (0.1, 0.0)
            .. controls (0.0, -0.5)
            and (-0.9, -1.6)
            .. (-1.2, -2.4);
    } else {
        return (0.0, 0.0)
            .. controls (0.5, -0.2)
            and (1.1, 0.0)
            .. (1.1, 0.5)
            .. controls (1.0, 0.7)
            and (0.8, 1.3)
            .. (0.5, 1.1)
            .. controls (0.3, 1.0)
            and (-0.3, -0.9)
            .. (-0.9, -1.7);
    }
}

guide path_0() {
    return (0.0, 0.0)
        .. controls (-0.7, 0.2)
        and (-1.5, -0.8)
        .. (-1.0, -1.2)
        .. controls (-0.7, -1.4)
        and (1.0, -0.4)
        .. (0.1, -0.0);
}

guide path_E8S3_8() {
    return (0, 0) -- (8, 0) ++ (0, -3.8);
}


guide[] path_SW4_SE4(real a = -126) {
    // kumi
    return
        (0.0, 0.0){dir(a)} .. {dir(a)}rpair(4, a)
        ^^
        shift(Cos(a) * 4, 0.0) * ((0, 0){dir(-a - 180)} .. {dir(-a - 180)}rpair(4, -a - 180));
}


guide path_SW4NW1() {
    // te_joshi
    //return (0, 0) -- rpair(-4.0, 60){dir(100)} .. {dir(145)}(-2.6, -1.7);
    return (0, 0) -- rpair(-4.0, 60){dir(100)} .. {dir(145)}rnr(1.9, 108);
}

guide path_SW4NW1er(real a = 18) {
    // te_joshi_ma
    return
        (0.0, 0.0){dir(-125)}              .. tension 1.0 and 1.0 ..
        {dir(-115)}(-1.8, -3.0){dir(-115)} .. tension 1.0 and 1.0 ..
    {dir(a)}(-2.3, -2.3){dir(a)}       .. tension 0.9 and 1.0 ..
    {dir(a)}(-1.1, -1.8);
}

guide path_SW4NW1e(real a = 0) {
    // te_joshi_ka
    return
        (0.0, 0.0){dir(-125)}              .. tension 1.0 and 1.0 ..
        {dir(-115)}(-1.8, -3.0){dir(-115)} .. tension 1.0 and 1.0 ..
    {dir(11)}(-2.8, -2.7){dir(11)}   .. tension 0.75 ..
    {dir(a)}(-1.6, -2.6);
}

guide path_SW4NW1el(real a) {
    // te_joshi_na
    return 
        (0.0, 0.0){dir(-115)}   .. tension 1.0 and 1.0 ..
        {dir(-105)}(-1.2, -3.3) .. tension 1.0 and 1.0 ..
    {dir(-18)}(-2.2, -3.0)  .. tension 1.0 and 1.0 ..
    {dir(a)}(-1.7, -3.1);
}

guide path_SW4NW1ner(real a) {
    // TODO: te_joshi_ya
    return 
        rotate(15) *((0.0, 0.0){dir(-125)} ..
                {dir(-115)}rpair(-3.5, 60) ..
                (-2.3, -2.8) ---
                {dir(a)}(-1.3, -2.2));
}

guide path_SW4NW1ne() {
    // TODO: te_joshi_koi
    return (0, 0);
}

guide path_SW4NW1nel() {
    // TODO: te_joshi_sa
    return (0, 0);
}

guide path_SW4NW1swr() {
    // TODO: te_joshi_node
    return (0, 0);
}

guide path_SW4NW1sw() {
    // TODO: te_joshi_o
    return (0, 0);
}

guide path_SW4NW1swl() {
    // TODO: te_joshi_pu
    return (0, 0);
}

guide path_SW4NW1sr() {
    // TODO: te_joshi_sha
    return (0, 0);
}

guide path_SW4NW1s() {
    // TODO: te_joshi_kya
    return (0, 0);
}

guide path_SW4NW1sl() {
    // TODO: te_joshi_u
    return (0, 0);
}

guide path_SW4NW1ser() {
    // TODO: te_joshi_ra
    return (0, 0);
}

guide path_SW4NW1se() {
    // TODO: te_joshi_e
    return (0, 0);
}

guide path_SW4NW1sel() {
    // TODO: te_joshi_ha
    return (0, 0);
}
// SW4NW1


guide path_SER4SWR4CR1() {
    // TODO: sei
    return 
        (0.0, 0.0){dir(-12)} .. tension 0.8 and 1.1 .. 
        {dir(-88)}(1.7, -2.0){dir(-87)} .. tension 1.1 and 1.1 .. 
    {dir(-164)}(0.6, -3.5){dir(-160)} .. tension 1.6 and 0.8 .. 
    {dir(68)}(-0.4, -2.9){dir(68)} .. tension 1.4 and 1.0 .. 
    {dir(-35)}(0.8, -3.4);
}

guide path_SER4SWR4CR1er() {
    // TODO: sei_ma
    return (0, 0);
}

guide path_SER4SWR4CR1e() {
    // TODO: sei_ka
    return (0, 0);
}

guide path_SER4SWR4CR1el() {
    // TODO: sei_na
    return (0, 0);
}

guide path_SER4SWR4CR1ner() {
    // TODO: sei_ya
    return (0, 0);
}

guide path_SER4SWR4CR1ne() {
    // TODO: sei_koi
    return (0, 0);
}

guide path_SER4SWR4CR1nel() {
    // TODO: sei_sa
    return (0, 0);
}

guide path_SER4SWR4CR1swr() {
    // TODO: sei_node
    return (0, 0);
}

guide path_SER4SWR4CR1sw() {
    // TODO: sei_o
    return (0, 0);
}

guide path_SER4SWR4CR1swl() {
    // TODO: sei_pu
    return (0, 0);
}

guide path_SER4SWR4CR1sr() {
    // TODO: sei_sha
    return (0, 0);
}

guide path_SER4SWR4CR1s() {
    // TODO: sei_kya
    return (0, 0);
}

guide path_SER4SWR4CR1sl() {
    // TODO: sei_u
    return (0, 0);
}

guide path_SER4SWR4CR1ser() {
    // TODO: sei_ra
    return (0, 0);
}

guide path_SER4SWR4CR1se() {
    // TODO: sei_e
    return (0, 0);
}

guide path_SER4SWR4CR1sel() {
    // TODO: sei_ha
    return (0, 0);
}

guide path_SL8ONEL4() {
    // kyo
    write("TODO: kyo");
    return
        (0.0, 0.0){dir(-129)}           .. tension 2.1 and 1.0 ..
        {dir(3)}(-0.1, -7.6){dir(4)}    .. tension 1.5 and 1.3 ..
    {dir(114)}(3.3, -5.1){dir(114)} .. tension 1.7 and 1.6 ..
    {dir(-127)}(-0.3, -7.6);

    //(0.0, 0.0){dir(-129)} .. tension 2.1 and 1.0 .. 
    //{dir(3)}(-0.2, -8.4){dir(4)} .. tension 1.5 and 1.3 .. 
    //{dir(114)}(3.5, -5.6){dir(114)} .. tension 1.7 and 1.6 .. 
    //{dir(-127)}(-0.4, -8.4);

    //(0.0, 0.0){dir(-129)} .. tension 2.1 and 1.0 .. 
    //{dir(3)}(-0.2, -9.6){dir(4)} .. tension 1.5 and 1.3 .. 
    //{dir(114)}(4.1, -6.4){dir(114)} .. tension 1.7 and 1.6 .. 
    //{dir(-127)}(-0.4, -9.6);
}

guide path_SL8ONEL4er() {
    // kyo_ma
    write("TODO: kyo_ma");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4e() {
    // kyo_ka
    write("TODO: kyo_ka");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4el() {
    // kyo_na
    write("TODO: kyo_na");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4ner() {
    // kyo_ya
    write("TODO: kyo_ya");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4ne() {
    // kyo_koi
    write("TODO: kyo_koi");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4nel() {
    // kyo_sa
    write("TODO: kyo_sa");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4swr() {
    // kyo_node
    write("TODO: kyo_node");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4sw() {
    // kyo_o
    write("TODO: kyo_o");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4swl() {
    // kyo_pu
    write("TODO: kyo_pu");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4sr() {
    // kyo_sha
    write("TODO: kyo_sha");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4s() {
    // kyo_kya
    write("TODO: kyo_kya");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4sl() {
    // kyo_u
    write("TODO: kyo_u");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4ser() {
    // kyo_ra
    write("TODO: kyo_ra");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4se() {
    // kyo_e
    write("TODO: kyo_e");
    return path_SL8ONEL4();
}

guide path_SL8ONEL4sel() {
    // kyo_ha
    write("TODO: kyo_ha");
    return path_SL8ONEL4();
}

guide path_SWL4NEL4(real ha = -147, real ta = 73) {
    // hou
    return (0.0, 0.0){dir(ha)}       .. tension 1.2 and 1.3 ..
    {dir(-35)}(-1.5, -2.8){dir(-35)} .. tension 1.1 and 1.8 ..
    {dir(ta)}(1.5, -0.4);
}

guide path_SWL4NEL4er() {
    // hou_ma
    write("TODO: hou_ma");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4e() {
    // hou_ka
    write("TODO: hou_ka");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4el() {
    // hou_na
    write("TODO: hou_na");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4ner() {
    // hou_ya
    write("TODO: hou_ya");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4ne() {
    // hou_koi
    write("TODO: hou_koi");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4nel(real ta = 90) {
    // hou_sa
    write("TODO: hou_sa");
    return path_SWL4NEL4(ta = ta);
}

guide path_SWL4NEL4swr() {
    // hou_node
    write("TODO: hou_node");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4sw() {
    // hou_o
    write("TODO: hou_o");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4swl() {
    // hou_pu
    write("TODO: hou_pu");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4sr() {
    // hou_sha
    write("TODO: hou_sha");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4s() {
    // hou_kya
    write("TODO: hou_kya");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4sl() {
    // hou_u
    write("TODO: hou_u");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4ser() {
    // hou_ra
    write("TODO: hou_ra");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4se() {
    // hou_e
    write("TODO: hou_e");
    return path_SWL4NEL4();
}

guide path_SWL4NEL4sel() {
    // hou_ha
    write("TODO: hou_ha");
    return path_SWL4NEL4();
}

guide path_SW4NE1() {
    // to_joshi
    guide base = bend((0, 0) -- rpair(-4.0, 60), 5, 1);
    real a = 25;
    real b = 10;

    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(1.8, a + b);

    return base .. bend(z1 -- z2, b, 1);
}

guide path_SW4NE1er() {
    // to_joshi_ma
    write("TODO: to_joshi_ma");
    return path_SW4NE1();
}

guide path_SW4NE1e() {
    // to_joshi_ka
    write("TODO: to_joshi_ka");
    return path_SW4NE1();
}

guide path_SW4NE1el() {
    // to_joshi_na
    write("TODO: to_joshi_na");
    return path_SW4NE1();
}

guide path_SW4NE1ner() {
    // to_joshi_ya
    write("TODO: to_joshi_ya");
    return path_SW4NE1();
}

guide path_SW4NE1ne() {
    // to_joshi_koi
    write("TODO: to_joshi_koi");
    return path_SW4NE1();
}

guide path_SW4NE1nel() {
    // to_joshi_sa
    write("TODO: to_joshi_sa");
    return path_SW4NE1();
}

guide path_SW4NE1swr() {
    // to_joshi_node
    write("TODO: to_joshi_node");
    return path_SW4NE1();
}

guide path_SW4NE1sw() {
    // to_joshi_o
    write("TODO: to_joshi_o");
    return path_SW4NE1();
}

guide path_SW4NE1swl() {
    // to_joshi_pu
    write("TODO: to_joshi_pu");
    return path_SW4NE1();
}

guide path_SW4NE1sr() {
    // to_joshi_sha
    write("TODO: to_joshi_sha");
    return path_SW4NE1();
}

guide path_SW4NE1s() {
    // to_joshi_kya
    write("TODO: to_joshi_kya");
    return path_SW4NE1();
}

guide path_SW4NE1sl() {
    // to_joshi_u
    write("TODO: to_joshi_u");
    return path_SW4NE1();
}

guide path_SW4NE1ser() {
    // to_joshi_ra
    write("TODO: to_joshi_ra");
    return path_SW4NE1();
}

guide path_SW4NE1se() {
    // to_joshi_e
    write("TODO: to_joshi_e");
    return path_SW4NE1();
}

guide path_SW4NE1sel() {
    // to_joshi_ha
    write("TODO: to_joshi_ha");
    return path_SW4NE1();
}

guide[] path_E4P(real len = 1) {
    // kou
    return (0, 0) -- (4, 0.1) ^^ (2.3, 0) -- (2.3, -len);
}

guide[] path_E4P_without_point() {
    // kou
    return path_E4P(len = 0);
}



guide path_SER4F() {
    // kara
    write("TODO: kara");
    return (0.0, 0.0){dir(-42)} .. tension 1.3 and 0.8 .. {dir(-139)}(1.2, -3.1);
}

guide path_SER4Fer() {
    // kara_ma
    write("TODO: kara_ma");
    return path_SER4F();
}

guide path_SER4Fe() {
    // kara_ka
    write("TODO: kara_ka");
    return path_SER4F();
}

guide path_SER4Fel() {
    // kara_na
    write("TODO: kara_na");
    return path_SER4F();
}

guide path_SER4Fner() {
    // kara_ya
    write("TODO: kara_ya");
    return path_SER4F();
}

guide path_SER4Fne() {
    // kara_koi
    write("TODO: kara_koi");
    return path_SER4F();
}

guide path_SER4Fnel() {
    // kara_sa
    write("TODO: kara_sa");
    return path_SER4F();
}

guide path_SER4Fswr() {
    // kara_node
    write("TODO: kara_node");
    return path_SER4F();
}

guide path_SER4Fsw() {
    // kara_o
    write("TODO: kara_o");
    return path_SER4F();
}

guide path_SER4Fswl() {
    // kara_pu
    write("TODO: kara_pu");
    return path_SER4F();
}

guide path_SER4Fsr() {
    // kara_sha
    write("TODO: kara_sha");
    return path_SER4F();
}

guide path_SER4Fs() {
    // kara_kya
    write("TODO: kara_kya");
    return path_SER4F();
}

guide path_SER4Fsl() {
    // kara_u
    write("TODO: kara_u");
    return path_SER4F();
}

guide path_SER4Fser() {
    // kara_ra
    write("TODO: kara_ra");
    return path_SER4F();
}

guide path_SER4Fse() {
    // kara_e
    write("TODO: kara_e");
    return path_SER4F();
}

guide path_SER4Fsel() {
    // kara_ha
    write("TODO: kara_ha");
    return path_SER4F();
}

guide path_KE8() {
    // kaku
    return kagi(path_E8());
}

guide path_KE8er() {
    // kaku_ma
    write("TODO: kaku_ma");
    return path_KE8();
}

guide path_KE8e() {
    // kaku_ka
    write("TODO: kaku_ka");
    return path_KE8();
}

guide path_KE8el() {
    // kaku_na
    write("TODO: kaku_na");
    return path_KE8();
}

guide path_KE8ner() {
    // kaku_ya
    write("TODO: kaku_ya");
    return path_KE8();
}

guide path_KE8ne() {
    // kaku_koi
    write("TODO: kaku_koi");
    return path_KE8();
}

guide path_KE8nel() {
    // kaku_sa
    write("TODO: kaku_sa");
    return path_KE8();
}

guide path_KE8swr() {
    // kaku_node
    write("TODO: kaku_node");
    return path_KE8();
}

guide path_KE8sw() {
    // kaku_o
    write("TODO: kaku_o");
    return path_KE8();
}

guide path_KE8swl() {
    // kaku_pu
    write("TODO: kaku_pu");
    return path_KE8();
}

guide path_KE8sr() {
    // kaku_sha
    write("TODO: kaku_sha");
    return path_KE8();
}

guide path_KE8s() {
    // kaku_kya
    write("TODO: kaku_kya");
    return path_KE8();
}

guide path_KE8sl() {
    // kaku_u
    write("TODO: kaku_u");
    return path_KE8();
}

guide path_KE8ser() {
    // kaku_ra
    write("TODO: kaku_ra");
    return path_KE8();
}

guide path_KE8se() {
    // kaku_e
    write("TODO: kaku_e");
    return path_KE8();
}

guide path_KE8sel() {
    // kaku_ha
    write("TODO: kaku_ha");
    return path_KE8();
}

guide path_E8S1(real len = 1.0) {
    return path_E8() ++ (0, -len);
}

guide path_relative_test_curve() {
    write((0, 0) :: (1, 0) :: (0, 1) :: (1, 0) :: (0, -1));
    return (0, 0) :: (1, 0) :: (0, 1) :: (1, 0) :: (0, -1);
}

guide path_relative_test_line() {
    return (0, 0) ++ (1, 0) ++ (0, 1) ++ (1, 0) ++ (0, -1);
}




guide path_SW3NE2SW3(real ha = -125, real ta = -125) {
    // kyou
    write("TODO: kyou");
    return 
        (0.0, 0.0) 
        ++ rpair(3.5, ha)
        ++ rpair(2, 16)
        ++ rpair(3.5, ta);
}

guide node_test() {
    //return (0, 0){dir(-30)} .. nr(10, 10, predir = dir(90), postdir = dir(-90)) 
    //                        .. nr(10, 10, predir = dir(90));
    return (0, 0){dir(-30)} .. nr(10, 10) .. tension 1
        and 1 .. (100, 100);
}


//guide path_SR8CR1() {
//    // shu
//    write("TODO: shu");
//    return (0, 0);
//}

//guide path_SR8CR1er() {
//    // shu_ma
//    write("TODO: shu_ma");
//    return path_SR8CR1();
//}

//guide path_SR8CR1e() {
//    // shu_ka
//    write("TODO: shu_ka");
//    return path_SR8CR1();
//}
//
//guide path_SR8CR1el() {
//    // shu_na
//    write("TODO: shu_na");
//    return path_SR8CR1();
//}

guide path_SR8CR1ner() {
    // shu_ya
    write("TODO: shu_ya");
    return path_SR8CR1();
}

guide path_SR8CR1ne() {
    // shu_koi
    write("TODO: shu_koi");
    return path_SR8CR1();
}

guide path_SR8CR1nel() {
    // shu_sa
    write("TODO: shu_sa");
    return path_SR8CR1();
}

guide path_SR8CR1swr() {
    // shu_node
    write("TODO: shu_node");
    return path_SR8CR1();
}

guide path_SR8CR1sw() {
    // shu_o
    write("TODO: shu_o");
    return path_SR8CR1();
}

guide path_SR8CR1swl() {
    // shu_pu
    write("TODO: shu_pu");
    return path_SR8CR1();
}

guide path_SR8CR1sr() {
    // shu_sha
    write("TODO: shu_sha");
    return path_SR8CR1();
}

guide path_SR8CR1s() {
    // shu_kya
    write("TODO: shu_kya");
    return path_SR8CR1();
}

guide path_SR8CR1sl() {
    // shu_u
    write("TODO: shu_u");
    return path_SR8CR1();
}

guide path_SR8CR1ser() {
    // shu_ra
    write("TODO: shu_ra");
    return path_SR8CR1();
}

guide path_SR8CR1se() {
    // shu_e
    write("TODO: shu_e");
    return path_SR8CR1();
}

guide path_SR8CR1sel() {
    // shu_ha
    write("TODO: shu_ha");
    return path_SR8CR1();
}

guide path_E8NW4S1() {
    // kenri
    return path_E8NW4() ++ path_S1();
}

guide path_SEL8cl1(guide base = path_SEL8()) {
    base = xscale(0.8) * base;
    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(1.5, 30);

    return base..{dir(90)}z2;
}

guide path_SEL8CL1(guide base = path_SEL8()) {
    // hi
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(reverse(base), 1.0);
    pair z2 = z3 - rpair(-1.2, 30 + b);

    return base .. bend(z2 -- z3, -b, 1);
}

guide path_SEL8CL1er() {
    // hi_ma
    write("TODO: hi_ma");
    return path_SEL8CL1();
}

guide path_SEL8CL1e() {
    // hi_ka
    write("TODO: hi_ka");
    return path_SEL8CL1();
}

guide path_SEL8CL1el() {
    // hi_na
    write("TODO: hi_na");
    return path_SEL8CL1();
}

guide path_SEL8CL1ner() {
    // hi_ya
    write("TODO: hi_ya");
    return path_SEL8CL1();
}

guide path_SEL8CL1ne() {
    // hi_koi
    write("TODO: hi_koi");
    return path_SEL8CL1();
}

guide path_SEL8CL1nel() {
    // hi_sa
    write("TODO: hi_sa");
    return path_SEL8CL1();
}

guide path_SEL8CL1swr() {
    // hi_node
    write("TODO: hi_node");
    return path_SEL8CL1();
}

guide path_SEL8CL1sw(real a = -120, guide base = path_SEL8cl1()) {
    // hi_o
    real b = -3;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.4);
    pair z2 = z3 - rpair(1.4, a);

     return base .. {dir(a)}z2 -- z3;
}

guide path_SEL8CL1SW1(real a = -120, guide base = path_SEL8cl1()) {
    // hiro
    return path_SEL8CL1sw() ++ rpair(1.5, a);
}

guide path_SEL8CL1swl() {
    // hi_pu
    write("TODO: hi_pu");
    return path_SEL8CL1();
}

guide path_SEL8CL1sr() {
    // hi_sha
    write("TODO: hi_sha");
    return path_SEL8CL1();
}

guide path_SEL8CL1s() {
    // hi_kya
    write("TODO: hi_kya");
    return path_SEL8CL1();
}

guide path_SEL8CL1sl() {
    // hi_u
    write("TODO: hi_u");
    return path_SEL8CL1();
}

guide path_SEL8CL1ser() {
    // hi_ra
    write("TODO: hi_ra");
    return path_SEL8CL1();
}

guide path_SEL8CL1se() {
    // hi_e
    write("TODO: hi_e");
    return path_SEL8CL1();
}

guide path_SEL8CL1sel() {
    // hi_ha
    write("TODO: hi_ha");
    return path_SEL8CL1();
}

guide path_S4cr1() {
    return scale(0.9) * path_S4();
}

guide path_S4CR1(guide base = path_S4cr1()) {
    // tsu
    pair z3 = arcpoint(-base, 1.0);
    pair z2 = z3 - rpair(1.8, 60);

    return base .. z2 .. {dir(60)}z3;
}

guide path_S4CR1er(real a = 18, guide base = path_S4cr1()) {
    // tsu_ma
    write("TODO: tsu_ma");
    real b= 5;
    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.5);
    pair z2 = z3 - rpair(0.9, a + b);

    return base .. bend(z2 -- z3, b, 1);
}

guide path_S4CR1e(real a = 0, guide base = path_S4cr1()) {
    // tsu_ka
    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.3);
    pair z2 = z3 - rpair(0.6, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_S4CR1el(real ta = -18, guide base = path_S4cr1()) {
    // tsu_na
    real b= -3;

    pair z1 = lastpoint(base);
    pair z4 = z1 + rpair(0.8, 170);
    pair z3 = arcpoint(-base, 0.4);
    pair z2 = z3 - rpair(0.7, ta + b);

    return base .. z4 .. bend(z2 -- z3, b, 1);
}

guide path_S4CR1ner() {
    // tsu_ya
    write("TODO: tsu_ya");
    return path_S4CR1();
}

guide path_S4CR1ne() {
    // tsu_koi
    write("TODO: tsu_koi");
    return path_S4CR1();
}

guide path_S4CR1nel() {
    // tsu_sa
    write("TODO: tsu_sa");
    return path_S4CR1();
}

guide path_S4CR1swr() {
    // tsu_node
    write("TODO: tsu_node");
    return path_S4CR1();
}

guide path_S4CR1sw() {
    // tsu_o
    write("TODO: tsu_o");
    return path_S4CR1();
}

guide path_S4CR1swl() {
    // tsu_pu
    write("TODO: tsu_pu");
    return path_S4CR1();
}

guide path_S4CR1sr() {
    // tsu_sha
    write("TODO: tsu_sha");
    return path_S4CR1();
}

guide path_S4CR1sl() {
    // tsu_kya
    write("TODO: tsu_kya");
    return path_S4CR1();
}

guide path_S4CR1s(real a = -90, guide base = path_S4cr1()) {
    // tsu_u
    write("TODO: tsu_u");

    pair z1 = lastpoint(base);
    pair z4 = z1 + rpair(0.8, 150);
    pair z3 = arcpoint(-base,  -0.5);
    pair z2 = z3 - rpair(0.7, a);

    return base .. z4 .. {dir(a)}z2 -- z3;
}

guide path_S4CR1S1(real len = 1.5, guide base = path_S4cr1()) {
    // tsu_u
    write("TODO: tsu_u");
    return path_S4CR1s(base) .. {dir(-90)}nr(0, -len);
}

guide path_S4CR1ser() {
    // tsu_ra
    write("TODO: tsu_ra");
    return path_S4CR1();
}

guide path_S4CR1se() {
    // tsu_e
    write("TODO: tsu_e");
    return path_S4CR1();
}

guide path_S4CR1sel() {
    // tsu_ha
    write("TODO: tsu_ha");
    return path_S4CR1();
}



guide path_EL16(real ha = -13, real tn = 2.5, real ta = 90) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(16.0, 0.0);
}

guide path_EL16_smooth(real ta = 90) {
    return path_EL16(tn = 1.0, ta = ta);
}

guide path_EL16_tangent(real ta = 90) {
    return path_EL16(ta = ta + 180);
}

guide path_EL16_up() {
    return path_EL16(ta = 110);
}

guide path_EL16F() {
    return path_EL16(ta = 60);
}

guide path_EL16CL1() {
    // ne
    return path_EL8CL1(base = path_EL16(ta = 90));
}

guide path_EL16CL1er() {
    // ne_ma
    write("TODO: ne_ma");
    return path_EL16CL1();
}

guide path_EL16CL1e() {
    // ne_ka
    write("TODO: ne_ka");
    return path_EL16CL1();
}

guide path_EL16CL1el() {
    // ne_na
    write("TODO: ne_na");
    return path_EL16CL1();
}

guide path_EL16CL1ner() {
    // ne_ya
    write("TODO: ne_ya");
    return path_EL16CL1();
}

guide path_EL16CL1ne() {
    // ne_koi
    write("TODO: ne_koi");
    return path_EL16CL1();
}

guide path_EL16CL1nel() {
    // ne_sa
    write("TODO: ne_sa");
    return path_EL16CL1();
}

guide path_EL16CL1swr() {
    // ne_node
    write("TODO: ne_node");
    return path_EL16CL1();
}

guide path_EL16CL1sw() {
    // ne_o
    write("TODO: ne_o");
    return path_EL16CL1();
}

guide path_EL16CL1swl() {
    // ne_pu
    write("TODO: ne_pu");
    return path_EL16CL1();
}

guide path_EL16CL1sr() {
    // ne_sha
    write("TODO: ne_sha");
    return path_EL16CL1();
}

guide path_EL16CL1s() {
    // ne_kya
    write("TODO: ne_kya");
    return path_EL16CL1();
}

guide path_EL16CL1sl() {
    // ne_u
    write("TODO: ne_u");
    return path_EL16CL1();
}

guide path_EL16CL1ser() {
    // ne_ra
    write("TODO: ne_ra");
    return path_EL16CL1();
}

guide path_EL16CL1se() {
    // ne_e
    write("TODO: ne_e");
    return path_EL16CL1();
}

guide path_EL16CL1sel() {
    // ne_ha
    write("TODO: ne_ha");
    return path_EL16CL1();
}

guide path_number_3() {
    // 3
    return path_3();
}

guide path_number_3er(real a = 18) {
    // 3_ma
    return scale(2) * (
        (0.0, 0.0){dir(-45)} .. tension 0.9 and 0.8 .. 
        {dir(157)}(-0.2, -0.9){dir(-58)} .. tension 0.8 and 0.8 .. 
        {dir(a + 180)}(-1.1, -2.3)
    );
}

guide path_number_3e() {
    // 3_ka
    write("TODO: 3_ka");
    return path_number_3();
}

guide path_number_3el() {
    // 3_na
    write("TODO: 3_na");
    return path_number_3();
}

guide path_number_3ner() {
    // 3_ya
    write("TODO: 3_ya");
    return path_number_3();
}

guide path_number_3ne() {
    // 3_koi
    write("TODO: 3_koi");
    return path_number_3();
}

guide path_number_3nel() {
    // 3_sa
    write("TODO: 3_sa");
    return path_number_3();
}

guide path_number_3swr() {
    // 3_node
    write("TODO: 3_node");
    return path_number_3();
}

guide path_number_3sw() {
    // 3_o
    write("TODO: 3_o");
    return path_number_3();
}

guide path_number_3swl() {
    // 3_pu
    write("TODO: 3_pu");
    return path_number_3();
}

guide path_number_3sr() {
    // 3_sha
    write("TODO: 3_sha");
    return path_number_3();
}

guide path_number_3s() {
    // 3_kya
    write("TODO: 3_kya");
    return path_number_3();
}

guide path_number_3sl() {
    // 3_u
    write("TODO: 3_u");
    return path_number_3();
}

guide path_number_3ser() {
    // 3_ra
    write("TODO: 3_ra");
    return path_number_3();
}

guide path_number_3se() {
    // 3_e
    write("TODO: 3_e");
    return path_number_3();
}

guide path_number_3sel() {
    // 3_ha
    write("TODO: 3_ha");
    return path_number_3();
}

guide[] path_SW3_SEL4() {
    // hijou
    write("TODO: hijou");
    guide g1 = (0.0, 0.0){dir(-133)} .. tension 1.0 and 1.2 .. {dir(-138)}(-1.9, -2.2);
    guide g2 = (0.0, 0.0){dir(-79)} .. tension 1.1 and 0.8 .. {dir(0)}(3.7, -3.7);
    g2 = shift(lastpoint(g1) - arcpoint(g2, 1.8)) * g2;
    
    return g1 ^^ g2; 
}

guide[] path_SW3_SEL4er() {
    // hijou_ma
    write("TODO: hijou_ma");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4e() {
    // hijou_ka
    write("TODO: hijou_ka");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4el() {
    // hijou_na
    write("TODO: hijou_na");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4ner() {
    // hijou_ya
    write("TODO: hijou_ya");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4ne() {
    // hijou_koi
    write("TODO: hijou_koi");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4nel() {
    // hijou_sa
    write("TODO: hijou_sa");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4swr() {
    // hijou_node
    write("TODO: hijou_node");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4sw() {
    // hijou_o
    write("TODO: hijou_o");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4swl() {
    // hijou_pu
    write("TODO: hijou_pu");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4sr() {
    // hijou_sha
    write("TODO: hijou_sha");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4s() {
    // hijou_u
    write("TODO: hijou_u");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4sl() {
    // hijou_kya
    write("TODO: hijou_kya");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4ser() {
    // hijou_ra
    write("TODO: hijou_ra");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4se() {
    // hijou_e
    write("TODO: hijou_e");
    return path_SW3_SEL4();
}

guide[] path_SW3_SEL4sel() {
    // hijou_ha
    write("TODO: hijou_ha");
    return path_SW3_SEL4();
}


guide[] path_SW3_el(guide base = path_EL8()) {
    guide g1 = (0.0, 0.0){dir(-133)} .. tension 1.0 and 1.2 .. {dir(-138)}(-1.9, -2.2);
    base = shift(lastpoint(g1) - arcpoint(base, 2.0)) * base;

    return g1 ^^ base;
}

guide path_NEL16(real ha = 34, real tn = 1.6, real ta = 90, real d = 45, pair dz = (0, 0)) {
    // so
    write("TODO: so");
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(shift(dz) * rpair(16, d)) ;
}

guide path_NEL16_tangent(real ha = 34, real d = 45, real ta = 90) {
    // so
    write("TODO: so");
    return path_NEL16(ha = ha, d = d, ta = ta + 180);
}

guide path_NEL16_bend(real ha = 34, real d = 45) {
    // so
    write("TODO: so");
    return path_NEL16(ha = ha, d = d, ta = 120);
}

guide path_NEL16er() {
    // so_ma
    write("TODO: so_ma");
    return path_NEL16_bend();
}

guide path_NEL16e() {
    // so_ka
    write("TODO: so_ka");
    return path_NEL16_bend();
}

guide path_NEL16el() {
    // so_na
    write("TODO: so_na");
    return path_NEL16();
}

guide path_NEL16ner() {
    // so_ya
    write("TODO: so_ya");
    return path_NEL16();
}

guide path_NEL16ne() {
    // so_koi
    write("TODO: so_koi");
    return path_NEL16();
}

guide path_NEL16nel() {
    // so_sa
    write("TODO: so_sa");
    return path_NEL16();
}

guide path_NEL16swr() {
    // so_node
    write("TODO: so_node");
    return path_NEL16();
}

guide path_NEL16sw(real a = -120) {
    // so_o
    write("TODO: so_o");
    return path_NEL16(ha = a);
}

guide path_NEL16swl() {
    // so_pu
    write("TODO: so_pu");
    return path_NEL16();
}

guide path_NEL16sr() {
    // so_sha
    write("TODO: so_sha");
    return path_NEL16();
}

guide path_NEL16s() {
    // so_u
    write("TODO: so_u");
    return path_NEL16();
}

guide path_NEL16sl() {
    // so_kya
    write("TODO: so_kya");
    return path_NEL16();
}

guide path_NEL16ser() {
    // so_ra
    write("TODO: so_ra");
    return path_NEL16();
}

guide path_NEL16se() {
    // so_e
    write("TODO: so_e");
    return path_NEL16();
}

guide path_NEL16sel() {
    // so_ha
    write("TODO: so_ha");
    return path_NEL16();
}

guide path_NEL8(real ha = 30, real tn = 1.2, real ta = 90, real d = 42, pair dz = (0, 0)) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(shift(dz) * rpair(7.6, d));
}

guide path_NEL8CL1(real a = -60, guide base = path_NEL8()) {
    // shi

    //base = scale(0.9) * base;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.0);
    pair z2 = z3 - rpair(1.5, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_elNEL8CL1er() {
    return (0, 0);
}

guide path_elNEL8CL1e() {
    return (0, 0);
}

guide path_elNEL8CL1el() {
    return (0, 0);
}

guide path_elNEL8CL1ne() {
    return (0, 0);
}

guide path_elNEL8CL1nel() {
    return (0, 0);
}

guide path_elNEL8CL1sw() {
    return (0, 0);
}

guide path_elNEL8CL1swl() {
    return (0, 0);
}

guide path_elNEL8CL1s() {
    return (0, 0);
}

guide path_elNEL8CL1sl() {
    return (0, 0);
}

guide path_swlNEL8CL1er() {
    return (0, 0);
}

guide path_swlNEL8CL1e() {
    return (0, 0);
}

guide path_swlNEL8CL1el() {
    return (0, 0);
}

guide path_swlNEL8CL1ne() {
    return (0, 0);
}

guide path_swlNEL8CL1nel() {
    return (0, 0);
}

guide path_swlNEL8CL1sw() {
    return (0, 0);
}

guide path_swlNEL8CL1swl() {
    return (0, 0);
}

guide path_swlNEL8CL1s() {
    return (0, 0);
}

guide path_swlNEL8CL1sl() {
    return (0, 0);
}

guide path_slNEL8CL1er() {
    return (0, 0);
}

guide path_slNEL8CL1e() {
    return (0, 0);
}

guide path_slNEL8CL1el() {
    return (0, 0);
}

guide path_slNEL8CL1ne() {
    return (0, 0);
}

guide path_slNEL8CL1nel() {
    return (0, 0);
}

guide path_slNEL8CL1sw() {
    return (0, 0);
}

guide path_slNEL8CL1swl() {
    return (0, 0);
}

guide path_slNEL8CL1s() {
    return (0, 0);
}

guide path_slNEL8CL1sl() {
    return (0, 0);
}

guide path_selNEL8CL1er() {
    return (0, 0);
}

guide path_selNEL8CL1e() {
    return (0, 0);
}

guide path_selNEL8CL1el() {
    return (0, 0);
}

guide path_selNEL8CL1ne() {
    return (0, 0);
}

guide path_selNEL8CL1nel() {
    return (0, 0);
}

guide path_selNEL8CL1sw() {
    return (0, 0);
}

guide path_selNEL8CL1swl() {
    return (0, 0);
}

guide path_selNEL8CL1s() {
    return (0, 0);
}

guide path_selNEL8CL1sl() {
    return (0, 0);
}

guide path_elNEL8CL1() {
    return (0, 0);
}

guide path_swlNEL8CL1() {
    return (0, 0);
}

guide path_slNEL8CL1() {
    return (0, 0);
}

guide path_selNEL8CL1() {
    return (0, 0);
}

guide path_NEL8CL1er() {
    return (0, 0);
}

guide path_NEL8CL1e(real a = 0, guide base = path_NEL8()) {
    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 0.4);
    pair z2 = z3 - rpair(1.2, a);

    return base .. tension 1.5 .. {dir(a)}z2 -- z3;
}

guide path_NEL8CL1el() {
    return (0, 0);
}

guide path_NEL8CL1ne() {
    return (0, 0);
}

guide path_NEL8CL1nel() {
    return (0, 0);
}

guide path_NEL8CL1sw(real a = -135, guide base = path_NEL8()) {
    base = scale(1.2, 0.9) * base;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 2.5);
    pair z2 = z3 - rpair(1.0, a);

    return base .. {dir(a)}z2 -- z3;
}

guide path_NEL8CL1swl() {
    return (0, 0);
}

guide path_NEL8CL1s() {
    return (0, 0);
}

guide path_NEL8CL1sl() {
    return (0, 0);
}


guide path_SEL16NEL16() {
    return 
    (0, 0){dir(-90)} .. tension 1.5 .. 
    {dir(0)}rnr(16, -60) .. tension 1.5 .. 
    {dir(90)}rnr(16, 60);
}

guide path_SEL16nel() {
    return subpath(path_SEL16NEL16(), 0, 1);
}

guide path_selNEL16() {
    guide g = path_SEL16NEL16();
    return shift(-point(g, 1)) * subpath(g, 1, 2);
}

guide path_SWR8(real ha = -90, real tn = 1.2, real ta = 180, pair dz = (0, 0), real d = -120) {
    return (0.0, 0.0){dir(ha)} .. tension tn .. {dir(ta)}(shift(dz) * rpair(8.0, d));
}

guide path_SWR8CR1(guide base = path_SWR8()) {
    real a = -30;
    real b = 5;

    pair z1 = lastpoint(base);
    pair z3 = arcpoint(-base, 1.0);
    pair z2 = z3 - rpair(1.5, a + b);

    return base .. bend(z2 -- z3, b, 1);
}

guide path_erSWR8CR1er() {
    return (0, 0);
}

guide path_erSWR8CR1e() {
    return (0, 0);
}

guide path_erSWR8CR1ner() {
    return (0, 0);
}

guide path_erSWR8CR1ne() {
    return (0, 0);
}

guide path_erSWR8CR1nel() {
    return (0, 0);
}

guide path_erSWR8CR1sw() {
    return (0, 0);
}

guide path_nerSWR8CR1er() {
    return (0, 0);
}

guide path_nerSWR8CR1e() {
    return (0, 0);
}

guide path_nerSWR8CR1ner() {
    return (0, 0);
}

guide path_nerSWR8CR1ne() {
    return (0, 0);
}

guide path_nerSWR8CR1nel() {
    return (0, 0);
}

guide path_nerSWR8CR1sw() {
    return (0, 0);
}

guide path_erSWR8CR1() {
    return (0, 0);
}

guide path_nerSWR8CR1() {
    return (0, 0);
}

guide path_SWR8CR1er() {
    return (0, 0);
}

guide path_SWR8CR1e() {
    return (0, 0);
}

guide path_SWR8CR1ner() {
    return (0, 0);
}

guide path_SWR8CR1ne() {
    return (0, 0);
}

guide path_SWR8CR1nel() {
    return (0, 0);
}

guide path_SWR8CR1sw() {
    return (0, 0);
}





/*
guide path_NEL16() {
    return (0, 0);
}
*/

guide path_elNEL16er() {
    return path_NEL16();
}
guide path_elNEL16e() {
    return path_NEL16();
}
guide path_elNEL16el() {
    return path_NEL16();
}
guide path_elNEL16ne() {
    return path_NEL16();
}
guide path_elNEL16nel() {
    return path_NEL16();
}
guide path_elNEL16sw() {
    return path_NEL16();
}
guide path_elNEL16swl() {
    return path_NEL16();
}
guide path_elNEL16s() {
    return path_NEL16();
}
guide path_elNEL16sl() {
    return path_NEL16();
}
guide path_swlNEL16er() {
    return path_NEL16();
}
guide path_swlNEL16e() {
    return path_NEL16();
}
guide path_swlNEL16el() {
    return path_NEL16();
}
guide path_swlNEL16ne() {
    return path_NEL16();
}
guide path_swlNEL16nel() {
    return path_NEL16();
}
guide path_swlNEL16sw() {
    return path_NEL16();
}
guide path_swlNEL16swl() {
    return path_NEL16();
}
guide path_swlNEL16s() {
    return path_NEL16();
}
guide path_swlNEL16sl() {
    return path_NEL16();
}
guide path_slNEL16er() {
    return path_NEL16();
}
guide path_slNEL16e() {
    return path_NEL16();
}
guide path_slNEL16el() {
    return path_NEL16();
}
guide path_slNEL16ne() {
    return path_NEL16();
}
guide path_slNEL16nel() {
    return path_NEL16();
}
guide path_slNEL16sw() {
    return path_NEL16();
}
guide path_slNEL16swl() {
    return path_NEL16();
}
guide path_slNEL16s() {
    return path_NEL16();
}
guide path_slNEL16sl() {
    return path_NEL16();
}
guide path_selNEL16er() {
    return path_NEL16();
}
guide path_selNEL16e() {
    return path_NEL16();
}
guide path_selNEL16el() {
    return path_NEL16();
}
guide path_selNEL16ne() {
    return path_NEL16();
}
guide path_selNEL16nel() {
    return path_NEL16();
}
guide path_selNEL16sw() {
    return path_NEL16();
}
guide path_selNEL16swl() {
    return path_NEL16();
}
guide path_selNEL16s() {
    return path_NEL16();
}
guide path_selNEL16sl() {
    return path_NEL16();
}
guide path_elNEL16() {
    return path_NEL16();
}
guide path_swlNEL16() {
    return path_NEL16();
}
guide path_slNEL16() {
    return path_NEL16();
}
guide path_selNEL16() {
    return path_NEL16();
}
guide path_NEL16er() {
    return path_NEL16();
}
guide path_NEL16e() {
    return path_NEL16();
}
guide path_NEL16el() {
    return path_NEL16();
}
guide path_NEL16ne() {
    return path_NEL16();
}
guide path_NEL16nel() {
    return path_NEL16();
}
guide path_NEL16sw() {
    return path_NEL16();
}
guide path_NEL16swl() {
    return path_NEL16();
}
guide path_NEL16s() {
    return path_NEL16();
}
guide path_NEL16sl() {
    return path_NEL16();
}



guide path_SWL8(real ha = -155, real tn = 1.5, real ta = -75, real d = -130, pair dz = (0, 0)) {
    return (0.0, 0.0){dir(ha)} ..tension tn .. {dir(ta)}(shift(dz) * rpair(8.0, d));
}

guide path_eSWL8el() {
    return path_SWL8();
}
guide path_eSWL8sw() {
    return path_SWL8();
}
guide path_eSWL8swl() {
    return path_SWL8();
}
guide path_eSWL8sr() {
    return path_SWL8();
}
guide path_eSWL8s() {
    return path_SWL8();
}
guide path_eSWL8sl() {
    return path_SWL8();
}
guide path_eSWL8nel() {
    return path_SWL8();
}
guide path_elSWL8el() {
    return path_SWL8();
}
guide path_elSWL8sw() {
    return path_SWL8();
}
guide path_elSWL8swl() {
    return path_SWL8();
}
guide path_elSWL8sr() {
    return path_SWL8();
}
guide path_elSWL8s() {
    return path_SWL8();
}
guide path_elSWL8sl() {
    return path_SWL8();
}
guide path_elSWL8nel() {
    return path_SWL8();
}
guide path_nerSWL8el() {
    return path_SWL8();
}
guide path_nerSWL8sw() {
    return path_SWL8();
}
guide path_nerSWL8swl() {
    return path_SWL8();
}
guide path_nerSWL8sr() {
    return path_SWL8();
}
guide path_nerSWL8s() {
    return path_SWL8();
}
guide path_nerSWL8sl() {
    return path_SWL8();
}
guide path_nerSWL8nel() {
    return path_SWL8();
}
guide path_neSWL8el() {
    return path_SWL8();
}
guide path_neSWL8sw() {
    return path_SWL8();
}
guide path_neSWL8swl() {
    return path_SWL8();
}
guide path_neSWL8sr() {
    return path_SWL8();
}
guide path_neSWL8s() {
    return path_SWL8();
}
guide path_neSWL8sl() {
    return path_SWL8();
}
guide path_neSWL8nel() {
    return path_SWL8();
}
guide path_nelSWL8el() {
    return path_SWL8();
}
guide path_nelSWL8sw() {
    return path_SWL8();
}
guide path_nelSWL8swl() {
    return path_SWL8();
}
guide path_nelSWL8sr() {
    return path_SWL8();
}
guide path_nelSWL8s() {
    return path_SWL8();
}
guide path_nelSWL8sl() {
    return path_SWL8();
}
guide path_nelSWL8nel() {
    return path_SWL8();
}
guide path_swrSWL8el() {
    return path_SWL8();
}
guide path_swrSWL8sw() {
    return path_SWL8();
}
guide path_swrSWL8swl() {
    return path_SWL8();
}
guide path_swrSWL8sr() {
    return path_SWL8();
}
guide path_swrSWL8s() {
    return path_SWL8();
}
guide path_swrSWL8sl() {
    return path_SWL8();
}
guide path_swrSWL8nel() {
    return path_SWL8();
}
guide path_swlSWL8el() {
    return path_SWL8();
}
guide path_swlSWL8sw() {
    return path_SWL8();
}
guide path_swlSWL8swl() {
    return path_SWL8();
}
guide path_swlSWL8sr() {
    return path_SWL8();
}
guide path_swlSWL8s() {
    return path_SWL8();
}
guide path_swlSWL8sl() {
    return path_SWL8();
}
guide path_swlSWL8nel() {
    return path_SWL8();
}
guide path_srSWL8el() {
    return path_SWL8();
}
guide path_srSWL8sw() {
    return path_SWL8();
}
guide path_srSWL8swl() {
    return path_SWL8();
}
guide path_srSWL8sr() {
    return path_SWL8();
}
guide path_srSWL8s() {
    return path_SWL8();
}
guide path_srSWL8sl() {
    return path_SWL8();
}
guide path_srSWL8nel() {
    return path_SWL8();
}
guide path_slSWL8el() {
    return path_SWL8();
}
guide path_slSWL8sw() {
    return path_SWL8();
}
guide path_slSWL8swl() {
    return path_SWL8();
}
guide path_slSWL8sr() {
    return path_SWL8();
}
guide path_slSWL8s() {
    return path_SWL8();
}
guide path_slSWL8sl() {
    return path_SWL8();
}
guide path_slSWL8nel() {
    return path_SWL8();
}
guide path_selSWL8el() {
    return path_SWL8();
}
guide path_selSWL8sw() {
    return path_SWL8();
}
guide path_selSWL8swl() {
    return path_SWL8();
}
guide path_selSWL8sr() {
    return path_SWL8();
}
guide path_selSWL8s() {
    return path_SWL8();
}
guide path_selSWL8sl() {
    return path_SWL8();
}
guide path_selSWL8nel() {
    return path_SWL8();
}
guide path_ecl1SWL8el() {
    return path_SWL8();
}
guide path_ecl1SWL8sw() {
    return path_SWL8();
}
guide path_ecl1SWL8swl() {
    return path_SWL8();
}
guide path_ecl1SWL8sr() {
    return path_SWL8();
}
guide path_ecl1SWL8s() {
    return path_SWL8();
}
guide path_ecl1SWL8sl() {
    return path_SWL8();
}
guide path_ecl1SWL8nel() {
    return path_SWL8();
}
guide path_ecl4SWL8el() {
    return path_SWL8();
}
guide path_ecl4SWL8sw() {
    return path_SWL8();
}
guide path_ecl4SWL8swl() {
    return path_SWL8();
}
guide path_ecl4SWL8sr() {
    return path_SWL8();
}
guide path_ecl4SWL8s() {
    return path_SWL8();
}
guide path_ecl4SWL8sl() {
    return path_SWL8();
}
guide path_ecl4SWL8nel() {
    return path_SWL8();
}
guide path_elcl1SWL8el() {
    return path_SWL8();
}
guide path_elcl1SWL8sw() {
    return path_SWL8();
}
guide path_elcl1SWL8swl() {
    return path_SWL8();
}
guide path_elcl1SWL8sr() {
    return path_SWL8();
}
guide path_elcl1SWL8s() {
    return path_SWL8();
}
guide path_elcl1SWL8sl() {
    return path_SWL8();
}
guide path_elcl1SWL8nel() {
    return path_SWL8();
}
guide path_eSWL8() {
    return path_SWL8();
}
guide path_elSWL8() {
    return path_SWL8(ha = -120, d = -110);
}
guide path_nerSWL8() {
    return path_SWL8();
}
guide path_neSWL8() {
    return path_SWL8();
}
guide path_nelSWL8() {
    return path_SWL8();
}
guide path_swrSWL8() {
    return path_SWL8();
}
guide path_swlSWL8() {
    return path_SWL8();
}
guide path_srSWL8() {
    return path_SWL8();
}
guide path_slSWL8() {
    return path_SWL8();
}
guide path_selSWL8() {
    return path_SWL8();
}
guide path_ecl1SWL8() {
    return path_SWL8();
}
guide path_ecl4SWL8() {
    return path_SWL8();
}
guide path_elcl1SWL8() {
    return path_SWL8();
}
guide path_SWL8el() {
    return path_SWL8();
}
guide path_SWL8sw() {
    return path_SWL8();
}
guide path_SWL8swl() {
    return path_SWL8();
}
guide path_SWL8sr() {
    return path_SWL8();
}
guide path_SWL8s() {
    return path_SWL8();
}
guide path_SWL8sl() {
    return path_SWL8();
}
guide path_SWL8nel() {
    return subpath(path_SWL8NEL8(), 0, 1);
}

guide path_NE8owl4() {
    return bend((0, 0) -- rpair(7.0, 51), 5, 1);
}

guide path_NE8OWL4(guide base = path_NE8owl4()) {
    // cho
    real a = -175;
    real b = 1;

    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(2.3, 170);
    pair z3 = z1 + rpair(3.5, a + b);

    write("TODO: cho");
    return base .. {dir(-170)}z2 .. bend(z3 -- z1, b, 1);
}

guide path_NE8OWL4er() {
    // cho_ma
    write("TODO: cho_ma");
    return path_NE8OWL4();
}

guide path_NE8OWL4e() {
    // cho_ka
    write("TODO: cho_ka");
    return path_NE8OWL4();
}

guide path_NE8OWL4el() {
    // cho_na
    write("TODO: cho_na");
    return path_NE8OWL4();
}

guide path_NE8OWL4ner() {
    // cho_ya
    write("TODO: cho_ya");
    return path_NE8OWL4();
}

guide path_NE8OWL4ne() {
    // cho_koi
    write("TODO: cho_koi");
    return path_NE8OWL4();
}

guide path_NE8OWL4nel() {
    // cho_sa
    write("TODO: cho_sa");
    return path_NE8OWL4();
}

guide path_NE8OWL4swr() {
    // cho_node
    write("TODO: cho_node");
    return path_NE8OWL4();
}

guide path_NE8OWL4sw() {
    // cho_o
    write("TODO: cho_o");
    return path_NE8OWL4();
}

guide path_NE8OWL4swl() {
    // cho_pu
    write("TODO: cho_pu");
    return path_NE8OWL4();
}

guide path_NE8OWL4sr() {
    // cho_sha
    write("TODO: cho_sha");
    return path_NE8OWL4();
}

guide path_NE8OWL4s() {
    // cho_u
    write("TODO: cho_u");
    return path_NE8OWL4();
}

guide path_NE8OWL4sl() {
    // cho_kya
    write("TODO: cho_kya");
    return path_NE8OWL4();
}

guide path_NE8OWL4ser() {
    // cho_ra
    write("TODO: cho_ra");
    return path_NE8OWL4();
}

guide path_NE8OWL4se() {
    // cho_e
    write("TODO: cho_e");
    return path_NE8OWL4();
}

guide path_NE8OWL4sel() {
    // cho_ha
    write("TODO: cho_ha");
    return path_NE8OWL4();
}

guide path_SW8owr4() {
    return bend((0.0, 0.0) -- rpair(-7.0, 65), -5, 1);
}

guide path_SW8OWR4(guide base = path_SW8owr4()) {
    real a = -10;
    real b = 5;

    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(2.3, -170);
    pair z3 = z1 + rpair(-3.5, a + b);

    return base .. {dir(170)}z2 .. bend(z3 -- z1, b, 1);
}

guide path_SW8OWR4er() {
    return path_SW8OWR4();
}
guide path_SW8OWR4e(real a = 0, guide base = path_SW8owr4()) {
    real b = 0;

    pair z1 = lastpoint(base);
    pair z2 = z1 + rpair(2.5, -170);
    pair z3 = z1 + rpair(-3.5, a + b);
    pair z4 = arcpoint(-base, 0.2);

    return base .. {dir(170)}z2 .. bend(z3 -- z4, b, 1);
}
guide path_SW8OWR4el() {
    return path_SW8OWR4();
}
guide path_SW8OWR4ner() {
    return path_SW8OWR4();
}
guide path_SW8OWR4ne() {
    return path_SW8OWR4();
}
guide path_SW8OWR4nel() {
    return path_SW8OWR4();
}
guide path_SW8OWR4swr() {
    return path_SW8OWR4();
}
guide path_SW8OWR4sw() {
    return path_SW8OWR4();
}
guide path_SW8OWR4swl() {
    return path_SW8OWR4();
}
guide path_SW8OWR4sr() {
    return path_SW8OWR4();
}
guide path_SW8OWR4s() {
    return path_SW8OWR4();
}
guide path_SW8OWR4sl() {
    return path_SW8OWR4();
}
guide path_SW8OWR4ser() {
    return path_SW8OWR4();
}
guide path_SW8OWR4se() {
    return path_SW8OWR4();
}
guide path_SW8OWR4sel() {
    return path_SW8OWR4();
}

guide path_NER8SER8() {
    return (0.0, 0.0){dir(90)}
    ..tension 1.5
    ..{dir(0)}rnr(8, 60)
    ..tension 1.5
    ..{dir(-90)}rnr(8, -60);
}

guide NER8ser() {
    return subpath(path_NER8SER8(), 0, 1);
}

guide path_SER8(real ha = -35, real tn = 1.2, real ta = -120, real d = -60, pair dz = (0, 0)) {
    return (0, 0){dir(ha)} .. tension tn .. {dir(ta)}(rpair(8, d) + dz);
}

guide path_nerSER8() {
    return shift(-point(path_NER8SER8(), 1)) * subpath(path_NER8SER8(), 1, 2);
}

guide path_nerSER8swr() {
    return path_nerSER8();
    //return path_SER8(ha = 0, tn = 1.1, d = -40, dz = (-2.2, -0.2));
}
guide path_nerSER8s() {
    return path_SER8(ha = 0, tn = 1.1, d = -40, dz = (-2.2, -0.2));
}
guide path_nerSER8sr() {
    return path_SER8(ha = 0, tn = 1.1, d = -40, dz = (-2.2, -0.2));
}
guide path_nerSER8sw() {
    return path_SER8(ha = 0, tn = 1.1, d = -40, dz = (-2.2, -0.2));
}
guide path_nerSER8sel() {
    return path_SER8(ha = 0, tn = 1.1, d = -40, dz = (-2.2, -0.2));
}
guide path_SER8swr() {
    return path_SER8();
}
guide path_SER8s() {
    return path_SER8();
}
guide path_SER8sr() {
    return path_SER8();
}
guide path_SER8sw() {
    return path_SER8();
}
guide path_SER8sel() {
    return path_SER8();
}

