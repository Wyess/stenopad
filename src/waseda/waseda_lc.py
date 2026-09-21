#!/usr/bin/env python3

from metasteno import Point as z, Path, Point

def path_lc(
    len_,
    circle_start=0.5,
    initial_up=0.5,
    tail_angle=-135,
    end_at=-1.5,
    scale_x=1,
    scale_y=1,
    angle=0,
):
    #(
    #    z[0]
    #    --- z[len_ - 0.5]
    #    >> +z[0.5, 0.5]
    #    >> {-150}@z[0]@(-1.5, -2)
    #)
    if tail_angle is not None:
        tail_angle += angle
    p = (
        z[0]
        --- z[len_ - circle_start]
        >> z[len_, initial_up]
        >> {tail_angle}@z[0]@(end_at, -2)
    )
    return p * (scale_x, scale_y, angle)

def path_lc_l_0(
    len_,
    circle_start=0.5,
    circle_size=1.0,
    scale_x=1,
    scale_y=1,
    angle=0
):
    #TODO
    #(
    #    z[0] 
    #    --- z[len_ - 0.5] 
    #    >> z[len_, 0.5]
    #    >> {180}@z[len_ - 0.5, 1.0]
    #    >> {0}@z[len_ - 1.0]
    #    >> z[len_]
    #)
    path = (
        z[0] 
        --- z[len_ - circle_start] 
        >> {90}@z[len_, circle_start]
        >> {180}@z[len_ - circle_start, circle_size]
        >> {0}@z[len_ - circle_size]
        >> z[len_]
    )
    return path * (scale_x, scale_y, angle)

def waseda_lc(builder):
    from stenobuilder import vref, pref
    builder = (
        builder.root()
        .word("けい", "Kei")
        .word("き", "Ki")
        .word("く", "Ku")
        .word("け", "Ke")
        .word("百万", "Hyakuman")
        .word("まする", "Hyakuman")
    )

    ecl1_len = {
        "Kei": 4.5,
        "Ki": 8,
        "Ku": 8,
        "Ke": 16,
        "Hyakuman": 25
    }
    for name, len_ in ecl1_len.items():
        builder = (
            builder.root()
            .path(
                f"{name.lower()}~",
                path_lc(
                    len_=len_,
                    circle_start=0.5,
                    initial_up=2 if name == 'Ku' else 0.5,
                    tail_angle=None,
                    end_at=-3.5 if name == 'Ku' else -1.5
                )
            )
            .path(
                name.lower(),
                pref(f"{name.lower()}~")@{-135},
            )
            .path(
                f"{name.lower()}(?=@head_e)",
                 path_lc_l_0(
                     len_=len_,
                     circle_start=0.5,
                     circle_size=1.0,
                )
            )
            .char(name)
                .model(f"e{len_}cl{4 if name == 'Ku' else 1}")
                .glyph()
                    .path(name.lower())
                .glyph("@head_e[1]")
                    .path(f"{name.lower()}(?=@head_e)")
        )
    return builder

