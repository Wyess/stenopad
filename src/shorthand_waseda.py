#!/usr/bin/env python3

import pyx
#import toml
import json
from util import *
import math
from path_expression_parser import create_path_expression_parser

vdict = {
    'ta_angle': -120,
    'to_henki_angle': -115,
}

pdict = {
    "A.": "O{-30} .. tension 1.2 .. 4E",
    "Ai": "O{170} .. 3.5N .. {-170}O",
    "I.": "O{30} .. tension 1.0 .. 4E",
    "U": "O -- 4S",
    "E": "O -- 4SSE",
    "Ketsu": "O -- 8SE",
    "E(?=SW)": "O -- 4SE",
    "Shite": "O -- 3SE",
    "Sha": "O{-50} .. {-135}8S",
    "Sha.": "O{-60} .. 8S",
    "O": "O -- 4SSW",
    "O(jog)": "O -- 4SSW -- ++(45: 1)",
    "Oo": "O --- 3.5SSW .. (4SSW + 0.5ESE) .. @(-1.3, -1)",
    "Kai": "O -- 4E",
    "Ka": "O -- 8E",
    "Ki": "O --- 7.5E .. 8E + 0.5N .. {-150}@(6, -1)",
    "Ki(?=EL)": "O --- 7.5E .. 8E + 0.5N .. tension 1.1 .. @(7.5, -1) + (140: 1.3) .. ++(140: -1.3)",
    "Ku": "O --- 7.5E .. 8E + 2.0N .. {-140}@(4.5, -1)",
    "Ke": "O --- 15.5E .. 16E + 0.5N .. {-150}@(14, -1)",
    "Ko": "O -- 16E",
    "Koto": "O -- 8S",
    "Kon2": "O -- 8E -- ++4S",
    "Kokoro": "O -- 8E -- ++4SSW",
    "Kyou": "O -- ++(60: -3) -- ++(30: 2) -- ++(60:-3)",
    "Sa.": "O{30} .. tension 1.3 .. (45: 8)",
    "Satsu.": "(1.5, 0){90} .. tension 1.2 .. ++O{-60} .. ++(1.5, 0) .. tension 1.3 .. ++(45: 8)",
    "SaHenki": "O{-90} .. tension 1.2 .. {180}(-120: 8)",
    "Shi(?=EL)": "O{30} .. tension 1.3 .. {150}(60: 7) .. @(-1.8, -1) + (130: 1.8) .. ++(130: -1.8)",
    "Shin": "O{30} .. tension 1.3 .. {150}(60: 8) .. tension 1.1 .. @(-0.4, -1) + (195: 2.0) ..  @(-0.4, -2) + (30: -1.5) -- ++(30: 3.0) ",
    "Shimi": "O{90} .. tension 1.2 .. {-45}4NE .. tension 1.2 .. {-135}2ESE",
    "Su(?=EL)": "O{30} .. tension 1.3 .. {140}(60: 6.5) .. @(-2.5, -1) + (130: 2.8) .. ++(130: -2.8)",

    "Su(?=ER)": "O{30} .. tension 1.3 .. {140}(60: 6.5) .. tension 1.5 .. @(-2.5, -1) + (10: -2.5) .. ++(10: 2.5)",

    "So.": "O{34} .. tension 1.6 .. (45: 16)",
    "Shourai": "O -- 4E 2E -- ++4S",

    #"Su(?=S)": "O{30} .. tension 1.3 .. {140}(60: 8) .. @(-3.2, -1) + (9: 3.5) .. ++(90: -3.5)",
    #"Ta": "O -- (60: -8)",
    #"TaHenki": "O -- (45: 8)",
    #"Cha": "O -- (30: 8)",
    #"ChaHenki": "O -- (55: -8)",
    "Ta": "O -- (ta_angle: 8)",
    "Taxe": "O -- (ta_angle: 8) (ta_angle: 7) -- ++(-45: 0.5)",
    "Taxe.": "O -- (ta_angle: 8) (ta_angle: 7) -- ++(-45: 0.1)",
    "TaHenki": "O -- (30: 8)",
    "Cha": "O -- (22.5: 8)",
    "Che": "O -- (22.5: 7.5){22.5} .. ++(22.5-90: 0.9) .. @(-1.0, -2)",
    "ChaHenki": "O -- (45: -8)",
    "TeJoshi": "O -- (60: -4.0){100} .. {145}++(108: 1.9)",
    "TeJoshi(?=Ha)": "O --- (60: -3.0) .. (60: -4.0) + (150: 0.5) .. tension 1.1 .. (60: -4) + (80: 1.3) .. {-90}(60:-4)",
    "Terx": "O --- (60: -3.0) .. (60: -4.0) + (150: 0.3) .. tension 1.1 .. (60: -4) + (90: 1.2){-90} .. {-90}(60:-4) + S",
    "To": "O -- (40: 16)",
    "To(?=E)": "O -- (45: 16)",
    "ToHenki": "O -- (to_henki_angle: 16)",
    "ToJoshi": "O -- (60: -4.0){30} .. {0}++(30: 1.9)",
    "Tsu": "O -- 3.5S{S} .. 4S + 0.5W .. {45}@(-1.2, -2)",
    "Tsu(?=ER)": "O -- 3.5S{S} .. 4S + 1.0W .. @(-0.9, -2)",
    "Na.": "O{-20} .. tension 1.7 .. 8E",
    "Nu(?=S)": "O{-30} .. tension 1.7 .. 8E .. tension 1.3 .. {-90}@(-3.2, -1) + 1.3N .. ++1.3S",
    "NoJoshi": "O{-30} .. tension 1.7 .. 8E .. {190}++(145:4)",
    "NaiHitei": "(60: 1.5) -- +(-120: 3)",
    "NakuHitei": "(0, 1.5) -- (0, -1.5)",
    "Nihon": "O -- +4E 2S -- ++4E",
    "Ha": "O{-90} .. tension 1.0 .. {0}(-60: 8)",
    "Hi": "O{-90} .. tension 1.0 .. {20}(-60: 8) .. @(-1.2, -1) + (45: 2) .. {-135}++(45: -2)",
    "Hur": "O{-90} .. tension 1.0 .. {0}(-60: 8) .. ++(110: 3.5){150}",
    "Ho": "O{-90} .. tension 1.0 .. {0}(-60: 16)",
    "Hoku": "(45: -1.5) .. {90}O{-90} .. tension 1.0 .. {0}(-60: 16)",
    "Ho(up)": "O{-90} .. tension 1.0 .. {45}(-60: 16)",
    "Hoku(up)": "(45: -1.5) .. {90}O{-90} .. tension 1.0 .. {45}(-60: 16)",
    "Na.": "O{-30} .. tension 1.3 .. 8E",
    "Ma.": "O{30} .. tension 1.3 .. 8E",
    "MoJoshi.": "O{20} .. tension 1.7 .. 8E .. ++(45: -4)",
    "Mo.": "O{20} .. tension 1.8 .. 16E",
    "N": "O -- (45: 2) ++(45: 2) -- +0.1SW",
    "N$": "O -- (45: 2)",
    "Fu$": "O -- (30: 4)",
    "Koi": "O -- (30: 4)",
    "Futsu$": "(30: 1){-45} .. (-60: 0.8) .. {30}O -- (30: 4)",
    #"Wa": "O{-164} .. tension 1.4 .. (-124: 3){-71} .. tension 0.95 .. {19}++(-17: 2)",
    "Wa": "O{-164} .. tension 1.4 .. (-124: 3){-70} .. {20}(-80: 3)",
    "Wa.": "O{-164} .. tension 1.4 .. (-124: 3){-70} .. (-80: 3)",
    "Wa(?=EL)": "O{-190} .. (-115: 3)",
    "Wa(?=E)": "O{-164} .. tension 1.4 .. (-124: 3){-70} .. {0}(-80: 3.2)",

}
pdict.update({
    "A": pdict["A."] + "{90}",
    "I": pdict["I."] + "{-100}",
    "I(?=Ta)": pdict["I."] + "{ta_angle}",
    "Ka(jog)": pdict["Ka"] + "-- ++(-170: 1)",
    "Karu": pdict["Ka"] + "-- ++(0, -1.5)",
    "Kai(jog)": pdict["Kai"] + "-- ++(-170: 1)",
    "KiTa": "O --- 7.5E .. 8E + 1.3N .. {-120}(6.8, 0) + (60: 1.3) -- (6.8, 0)",
    "KeSaHenki": "O --- 15.5E .. 16E + 0.5N .. @(15.3, -1)+ (95: 1.5) .. ++(95: -1.5) & " + pdict["SaHenki"],
    "Ko(jog)": pdict["Ko"] + "-- ++(-170: 1)",
    "Koto(jog)": pdict["Koto"] + "-- ++(80: 1)",
    "Sa": pdict["Sa."] + "{90}",
    "Satsu": pdict["Satsu."] + "{90}",
    "Sa(bend)": pdict["Sa."] + "{120}",
    "Shi": pdict["Shi(?=EL)"] + "{-30}",
    "Shimiru": pdict["Shimi"] + " -- ++1.5S",
    "Su": pdict["Su(?=EL)"] + "{-30}",
    "So": pdict["So."] + "{90}",
    "Sore": "O{-90} .. {180}(45: -4)",
    "Se": "O{34} .. tension 1.9 .. {140}(50: 15) .. @(-1.7, -1) + (130: 2.0) .. {-60}++(130: -2.0)",
    "Sen": "O{34} .. tension 1.9 .. {140}(50: 15) .. tension 1.1 .. @(-0.4, -1) + (195: 2.0) ..  @(-0.4, -2) + (30: -1.5) -- ++(30: 3.0)",
    "Na": pdict["Na."] + "{90}",
    "Nan": pdict["Na."] + "{45}",
    "Naru": pdict["Na."] + "{80} .. {S}++1.5S",
    "Ma": pdict["Ma."] + "{-90}",
    "Ii": pdict["I."] + "{-90} .. @(-0.7, -1) + (60: -1.8) .. {60}++(60: 1.8)",
    "Ii(?=S)": pdict["I."] + "{-90} .. {90}@(-1.8, -1) ",
    "Mi": pdict["Ma."] + "{-90} .. @(-0.7, -1) + (60: -1.8) .. {60}++(60: 1.8)",
    "Me": pdict["Mo."] + "{-90} .. @(-0.7, -1) + (60: -1.8) .. {60}++(60: 1.8)",
    "Me(?=S)": pdict["Mo."] + "{-90} .. {90}@(-2.3, -1) ",
    "Fu": pdict['Fu$'] + "++(30: 2.5) -- ++0.1SW",
    "Futsu": pdict['Futsu$'] + "++(30: 2.5) -- ++0.1SW",
    "Mo": pdict["Mo."] + "{-80}",
    "MoJoshi": pdict['MoJoshi.'] + "{-180}",
    "Mono": pdict['Mo.'] + "{-90} .. {180}++(-145: 4)",
    "Nihon(jog)": pdict["Nihon"] + "-- ++(-170: 1)",
})
pdict.update({
    "Ah(?=EL)": pdict["A"] + " .. @(-0.9, -1) + (130: 1.7) .. ++(130: -1.7)",
    "Ni(?=EL)": pdict["Na"] + " .. @(-0.5, -1) + (130: 1.7) .. ++(130: -1.7)",
    "Nu": pdict["Na"] + " .. @(-4.5, -1) + (45: 1.7) .. {-135} ++(45: -1.7)",
    "Nure$": pdict["Na"] + " .. tension 1.5 .. @(-3.0, -1) + (135: 2.7) .. {-30} ++(135: -3.7)",
    "Mi(?=Na)": pdict["Ma."] + "{-120} .. @(-0.5, -1) + (180: 1.5) .. ++(180: -1.5)" + "&" + pdict['Na'],
    "Mi(?='E')": pdict["Ma."] + "{-90} .. ++(210: 1.5) .. {SSE}@(-0.0, -1) + 1.2NNE -- ++1.2SSE",
    "Me(?=Na)": "O{20} .. tension 1.8 .. 16E{-120} .. @(-0.5, -1) + (180: 1.5) .. ++(180: -1.5)" + "&" + pdict['Na'],
    "SuMa": pdict["Su(?=ER)"] + '&' + pdict['Ma'],
    "KiNa": pdict["Ki(?=EL)"] + "&" +  pdict["Na"],
    "MaNa": pdict["Ma."] + "&" + pdict["Na"],
    "TsuMo": pdict["Tsu(?=ER)"] + "&" + pdict["Mo"],
    "WaNa": pdict["Wa(?=EL)"] + "&" + pdict["Na"]
})
pdict.update({
    "Ah": pdict["Ah(?=EL)"] + "{-30}",
    "Ni": pdict["Ni(?=EL)"] + "{-30}",
    "NiNa": cat(("Ni(?=EL)", "Na"), pdict),
    "AI": cat(("A.", "I"), pdict),
    "Nure": pdict["Nure$"] + "++(-30: 2) -- ++0.1S",
})


wdict = {
    'SEPARATOR': '・',
    ' ': 'Space',
    '　': 'Space',
    '\n': 'Newline',
    'あ': 'A',
    'あい': 'Ai',
    '雨': ['A', 'PosAme', 'E'],
    'ある（点）': 'Aru(dot)',
    'い': 'I',
    'いい': 'Ii',
    'いる': ['PosIru', 'I'],
    'う': 'U',
    'うち（交差）': ['PosUchi', 'U'],
    'たい': 'Tai',
    'っ': 'SmallTsu',
    'え': 'E',
    'お': 'O',
    'か': 'Ka',
    '傘': ['Ka', 'Sa'],
    'か（点）': 'DotKa',
    'かた（点）': 'DotKata',
    'が': ['Ka', 'Dakuten'],
    'かい': 'Kai',
    'かる': 'Karu',
    'き': 'Ki',
    '君': 'Ki',
    'きょう': 'Kyou',
    'く': 'Ku',
    'け': 'Ke',
    'けつ': 'Ketsu',
    'べつ': 'Ketsu',
    'こ': 'Ko',
    'こい': 'Koi',
    'こえ': 'Koi',
    'こく': 'Koi',
    '心': 'Kokoro',
    '事': 'Koto',
    'コン': 'Kon2',
    'さ': 'Sa',
    'さつ（交差）': ['PosTsuKousa', 'Sa'],
    'し': 'Shi',
    'しゃ': 'Sha',
    'して': 'Shite',
    '将来': 'Shourai',
    'しみ': 'Shimi',
    'しみる': 'Shimiru',
    'しめ': 'Shimi',
    'しめる': 'Shimiru',
    'しん': 'Shin',
    '新聞': 'Sen',
    'す': 'Su',
    'せ': 'Se',
    'せん': 'Sen',
    'そ': 'So',
    'それ': 'Sore',
    '其': 'Sore',
    'する（点）': 'DotSuru',
    'た': 'Ta',
    '誰': 'Taxe',
    'た（え略）': 'Taxe',
    'だけ': ['PosDake', 'Ta'],
    'つ': 'Tsu',
    'て（助詞）': 'TeJoshi',
    'テｒ': 'Terx',
    'と': 'To',
    'と（助詞）': 'ToJoshi',
    'ちゃ': 'Cha',
    'ちぇ': 'Che',
    'てｒ': 'Che',
    'な': 'Na',
    'なか（点）': 'DotNaka',
    'なる': 'Naru',
    'なん': 'Nan',
    '何': 'Nan',
    '日本': 'Nihon',
    'ない（否定）': 'NaiHitei',
    'なく（否定）': ['PosNaku', 'NakuHitei'],
    'に': 'Ni',
    'ぬ': 'Nu',
    'ぬれ': 'Nure',
    'の（助詞）': 'NoJoshi',
    'は': 'Ha',
    'ひ': 'Hi',
    'フ': 'Fu',
    'ふつ': 'Futsu',
    'ふｒ': 'Hur',
    '問題': 'Futsu',
    'ほ': 'Ho',
    'ほく': 'Hoku',
    'ま': 'Ma',
    'まつ（交差）': ['PosTsuKousa', 'Ma'],
    'み': 'Mi',
    'め': 'Me',
    'も': 'Mo',
    'も（助詞）': 'MoJoshi',
    '物': 'Mono',
    '者': 'Mono',
    'もの': 'Mono',
    'られ': ['PosRare', 'Wa'],
    'ろう': ['PosRou', 'A'],
    'わ': 'Wa',
    'わが国': ['Wagaku', 'Ni'],
    'を': 'O',
    'ん': 'N',
}

def create_dot_glyph(x, y, w=0.1, h=0, key='default'):
    return {
        'key': key,
        'path': [{'d': f'm{x} {-y}l{w} {h}', 'length': math.hypot(w, h)}],
        'dx': x + w,
        'dy': -(y + h),
        'ascent': 0,
        'top': -(y + h),
        'bottom': -(y + h),
        'left': x + w,
        'right': x + w,
    }

def create_pos_glyph(x, y, key='default'):
    return {
        'key': key,
        'path': [{'d': f'M0 0', 'length': 0}],
        'dx': x,
        'dy': -y,
        'ascent': 0,
        'top': y,
        'bottom': y,
        'left': x,
        'right': x,
    }

parser = create_path_expression_parser(vdict)
set_path_expression_parser(parser)

kdict = {
    'sp_or_eos': 'eos[1]|space[1]|newline[1]',
}

cdict = {
    'Null': {
        'tag': {},
        'default_glyph': {
            'key': 'default',
            'path': [{'d': 'M2 -2v4h4v-4h-4l4 4', 'length': 0}],
            'dx': 8,
            'dy': 0,
            'ascent': 0,
            'top': 0,
            'bottom': 0,
            'left': 0,
            'right': 8,
        },
        'glyphs': [],
    },
    'Space': {
        'tag': {
            'space',
        },
        'default_glyph': {
            'key': 'default',
            'path': [],
            'dx': 4,
            'dy': 0,
            'ascent': 0,
            'top': 0,
            'bottom': 0,
            'left': 0,
            'right': 0,
        },
        'glyphs': [],
    },
    'Newline': {
        'tag': {
            'newline',
        },
        'default_glyph': {
            'key': 'default',
            'path': [],
            'dx': 0,
            'dy': 0,
            'ascent': 0,
            'top': 0,
            'bottom': 0,
            'left': 0,
            'right': 0,
        },
        'glyphs': [],
    },
    'Aru(dot)': {
        'tag': {
            'aru_dot',
            '@dot',
        },
        'default_glyph': create_dot_glyph(2.5, 0),
        'glyphs': [],
    },
    'Dakuten': {
        'tag': {
            'dakuten',
            'mark',
        },
        'default_glyph': create_dot_glyph(4, -1.5),
        'glyphs': [
        ],
    },
    'A': {
        'tag': {
            'a',
            'el4',
        },
        'default_glyph': create_glyph(pdict['A']),
        'glyphs': [
            create_glyph(pdict['AI'], key='i[1]')
        ],
    },
    'Ai': {
        'tag': {
            'ai',
            'cr4',
        },
        'default_glyph': create_glyph(pdict['Ai'], ascent=-2),
        'glyphs': [
        ],
    },
    'I': {
        'tag': {
            'i',
            'er4',
        },
        'default_glyph': create_glyph(pdict['I']),
        'glyphs': [
            create_glyph(pdict['I(?=Ta)'], key='ta[1]'),
        ],
    },
    'Ii': {
        'tag': {
            'ii',
            '@head_er',
            '@head_er4',
            'er4cr1',
        },
        'default_glyph': create_glyph(pdict['Ii']),
        'glyphs': [
             create_glyph(pdict['Ii(?=S)']),
        ],
    },
    'U': {
        'tag': {
            'u',
            's4',
        },
        'default_glyph': create_glyph(pdict['U']),
        'glyphs': [
        ],
    },
    'Tai': {
        'tag': {
            'tai',
            's4',
            '@head_s',
        },
        'default_glyph': create_glyph(pdict['U']),
        'glyphs': [
        ],
    },
    'Shourai': {
        'tag': {
            'shourai',
            'e4-s4',
        },
        'default_glyph': create_glyph(pdict['Shourai']),
        'glyphs': [
        ],
    },
    'E': {
        'tag': {
            'e',
            'se4',
            '@head_se4',
            '@head_se',
        },
        'default_glyph': create_glyph(pdict['E']),
        'glyphs': [
            create_glyph(pdict['E(?=SW)'], key='@head_sw[1]'),
        ],
    },
    'Shite': {
        'tag': {
            'shite',
            'se3',
        },
        'default_glyph': create_glyph(pdict['Shite']),
        'glyphs': [
        ],
    },
    'O': {
        'tag': {
            'o',
            'sw4',
            '@head_sw',
            '@tail_sw',
        },
        'default_glyph': create_glyph(pdict['O']),
        'glyphs': [
            create_glyph(pdict['O(jog)'], key='@head_sw[1]'),
        ],
    },
    'Oo': {
        'tag': {
            'oo',
            'sw4cl1',
            '@head_sw',
        },
        'default_glyph': create_glyph(pdict['Oo'], name='Oo'),
        'glyphs': [
            create_glyph(pdict['Oo'], name='Oo'),
        ],
    },
    'Ka': {
        'tag': {
            'ka',
            'e8',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Ka']),
        'glyphs': [
            create_glyph(pdict['Ka(jog)'], key='@head_e[1]'),
        ],
    },
    'Kai': {
        'tag': {
            'kai',
            'e4',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Kai']),
        'glyphs': [
            create_glyph(pdict['Kai(jog)'], key='@head_e[1]'),
        ],
    },
    'Karu': {
        'tag': {
            'karu',
            'e8s1f',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Karu'], post_offset=(0, -2.5)),
        'glyphs': [
        ],
    },
    'Ki': {
        'tag': {
            'ki',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Ki']),
        'glyphs': [
            create_glyph(pdict['KiTa'], key='ta[1]'),
            create_glyph(pdict['KiNa'], key='@head_el8[1]'),
        ],
    },
    'Kyou': {
        'tag': {
            'kyou',
        },
        'default_glyph': create_glyph(pdict['Kyou'], ascent=2),
        'glyphs': [
        ],
    },
    'Ku': {
        'tag': {
            'ku',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Ku']),
        'glyphs': [
        ],
    },
    'Ke': { 
        'tag': {
            'ke',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Ke']),
        'glyphs': [
            create_glyph(pdict["KeSaHenki"], key="sa_henki[1]"),
        ],
    },
    'Ketsu': { 
        'tag': {
            'ketsu',
            '@head_se',
            '@head_se8',
            '@tail_se',
            '@tail_se8',
        },
        'default_glyph': create_glyph(pdict['Ketsu']),
        'glyphs': [
        ],
    },
    'Ko': {
        'tag': {
            'ko',
            'e16',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Ko']),
        'glyphs': [
            create_glyph(pdict['Ko(jog)'], key='@head_e[1]'),
        ],
    },
    'Koi': {
        'tag': {
            'koi',
            'ne4',
            '@head_ne',
        },
        'default_glyph': create_glyph(pdict['Koi']),
        'glyphs': [
            #create_glyph(pdict['Ko(jog)'], key='@head_e[1]'),
        ],
    },
    'Koto': {
        'tag': {
            'koto',
            's8',
            '@head_s',
            '@tail_s',
        },
        'default_glyph': create_glyph(pdict['Koto']),
        'glyphs': [
            create_glyph(pdict['Koto(jog)'], key='@head_s[1]'),
        ],
    },
    'Kon2': {
        'tag': {
            'kon',
            'e8s4f',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Kon2'], post_offset=(0, -3)),
        'glyphs': [
        ],
    },
    'Kokoro': {
        'tag': {
            'kokoro',
            'e8sw4f',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Kokoro'], post_offset=polar(-2.5, 60)),
        'glyphs': [
        ],
    },
    'Sa': {
        'tag': {
            'sa',
            '@head_nel',
        },
        'default_glyph': create_glyph(pdict['Sa'], ascent=-1.5),
        'glyphs': [
            create_glyph(pdict['SaHenki'], key="@head_e[-1]", name='SaHenki'),
        ],
    },
    'Satsu': {
        'tag': {
            'satsu',
        },
        'default_glyph': create_glyph(pdict['Satsu'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'SaHenki': {
        'tag': {
            'sa_henki',
            '@head_swr',
        },
        'default_glyph': create_glyph(pdict['SaHenki'], name='SaHenki'),
        'glyphs': [
        ],
    },
    'Shi': {
        'tag': {
            'shi',
            '@head_nel',
        },
        'default_glyph': create_glyph(pdict['Shi'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'Shin': {
        'tag': {
            'shin',
            '@head_nel',
        },
        'default_glyph': create_glyph(pdict['Shin'], ascent=-1.5, post_offset=polar(3, 30)),
        'glyphs': [
        ],
    },
    'Sha': {
        'tag': {
            'sha',
            '@head_sr',
        },
        'default_glyph': create_glyph(pdict['Sha'], ascent=4),
        'glyphs': [
        ],
    },
    'Shimi': {
        'tag': {
            'shimi',
            '@head_ner',
        },
        'default_glyph': create_glyph(pdict['Shimi'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'Shimiru': {
        'tag': {
            'shimiru',
            '@head_ner',
        },
        'default_glyph': create_glyph(pdict['Shimiru'], ascent=-1.5, post_offset=(0, -2.5)),
        'glyphs': [
        ],
    },
    'Su': {
        'tag': {
            'su',
            '@head_nel',
        },
        'default_glyph': create_glyph(pdict['Su'], ascent=-1.5),
        'glyphs': [
            create_glyph(pdict['SuMa'], key='@head_er8[1]', ascent=-1.5),
        ],
    },
    'Se': {
        'tag': {
            'se',
            '@head_nel',
        },
        'default_glyph': create_glyph(pdict['Se'], ascent=-8.0),
        'glyphs': [
        ],
    },
    'Sen': {
        'tag': {
            'sen',
            '@head_nel',
        },
        'default_glyph': create_glyph(pdict['Sen'], ascent=-8.0, post_offset=polar(3, 30)),
        'glyphs': [
        ],
    },
    'So': {
        'tag': {
            'so',
            '@head_nel',
        },
        'default_glyph': create_glyph(pdict['So'], ascent=-8.0),
        'glyphs': [
        ],
    },
    'Sore': {
        'tag': {
            'sore',
            '@head_swr',
        },
        'default_glyph': create_glyph(pdict['Sore'], ascent=2.0, post_offset=(-2, -0.5)),
        'glyphs': [
        ],
    },
    'DotSuru': {
        'tag': {
            'dot_suru',
        },
        'default_glyph': create_dot_glyph(2, -2),
        'glyphs': [
        ],
    },
    'Ta': {
        'tag': {
            'ta',
            '@head_sw',
        },
        'default_glyph': create_glyph(pdict['Ta'], ascent=1.5),
        'glyphs': [
            create_glyph(pdict['TaHenki'], key='(ta[-1]|@tail_s[-1])|(ta[-2].pos_dake[-1])', ascent=1.5, name='TaHenki'),
        ],
    },
    'Taxe': {
        'tag': {
            'taxe',
            '@head_sw',
        },
        'default_glyph': create_glyph(pdict['Taxe'], ascent=1.5),
        'glyphs': [
            create_glyph(pdict['Taxe.'], ascent=1.5, key='!@head_sw[1].!' + kdict['sp_or_eos']),
        ],
    },
    'ChaHenki': {
        'tag': {
            'cha_henki',
            '@head_sw',
        },
        'default_glyph': create_glyph(pdict['ChaHenki'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'TaHenki': {
        'tag': {
            'ta_henki',
            '@head_ne',
        },
        'default_glyph': create_glyph(pdict['TaHenki'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'Cha': {
        'tag': {
            'cha',
            '@head_ne',
        },
        'default_glyph': create_glyph(pdict['Cha'], ascent=-1),
        'glyphs': [
            create_glyph(pdict['ChaHenki'], key='ta_henki[-1]|cha[-1]', ascent=-1, name='ChaHenki'),
        ],
    },
    'Che': {
        'tag': {
            'che',
            '@head_ne',
        },
        'default_glyph': create_glyph(pdict['Che'], ascent=-1),
        'glyphs': [
        ],
    },
    'Tsu': {
        'tag': {
            'tsu',
            '@head_s',
        },
        'default_glyph': create_glyph(pdict['Tsu'], ascent=2),
        'glyphs': [
            create_glyph(pdict['TsuMo'], ascent=2, key='@head_er16[1]'),
        ],
    },
    'SmallTsu': {
        'tag': {
            'small_tsu',
        },
        'default_glyph': create_pos_glyph(0, -2),
        'glyphs': [
            create_pos_glyph(-2, 4, key='@tail_se8[-1].@head_sw4[1]'),
        ],
    },
    'TeJoshi': {
        'tag': {
            'te_joshi',
            '@head_sw',
        },
        'default_glyph': create_glyph(pdict['TeJoshi'], ascent=-1),
        'glyphs': [
            create_glyph(pdict['TeJoshi(?=Ha)'], ascent=-1, key='ha[1]'),
        ],
    },
    'Terx': {
        'tag': {
            'terx',
            '@head_sw',
            '@head_sw4',
        },
        'default_glyph': create_glyph(pdict['Terx'], ascent=1, post_offset=(0, -0.5)),
        'glyphs': [
        ],
    },
    'To': {
        'tag': {
            'to',
            '@head_ne',
        },
        'default_glyph': create_glyph(pdict['To'], ascent=-2.5),
        'glyphs': [
            create_glyph(pdict['To(?=E)'], key='@head_e[1]', ascent=-2.5),
            create_glyph(pdict['ToHenki'], key='@head_ne[-1]', ascent=2.5, name='ToHenki'),
        ],
    },
    'ToHenki': {
        'tag': {
            'to_henki',
            '@head_sw',
        },
        'default_glyph': create_glyph(pdict['ToHenki'], ascent=-2.5, name='ToHenki'),
        'glyphs': [
            create_glyph(pdict['ToHenki'], key='@head_e[1]', ascent=-2.5),
        ],
    },
    'ToJoshi': {
        'tag': {
            'to_joshi',
            '@head_sw',
        },
        'default_glyph': create_glyph(pdict['ToJoshi'], ascent=-1.5),
        'glyphs': [
            create_glyph(pdict['Oo'], key='!'+kdict['sp_or_eos'], name='Oo')
        ],
    },
    'Na': {
        'tag': {
            'na',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pdict['Na']),
        'glyphs': [
        ],
    },
    'Naru': {
        'tag': {
            'naru',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pdict['Naru'], post_offset=(0, -2)),
        'glyphs': [
        ],
    },
    'Nan': {
        'tag': {
            'nan',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pdict['Nan'], post_offset=polar(2.5, 45)),
        'glyphs': [
        ],
    },
    'NaiHitei': {
        'tag': {
            'nai_hitei',
        },
        'default_glyph': create_glyph("1.5W + " + pdict['NaiHitei']),
        'glyphs': [
        ],
    },
    'PosNaku': {
        'tag': {
            'pos_naku',
        },
        'default_glyph': create_pos_glyph(-1.5, 0),
        'glyphs': [
            create_pos_glyph(-0.7, -0.5, key='wa[-1]'),
            create_pos_glyph(-0.5, 0.5, key='e[-1]'),
        ],
    },
    'NakuHitei': {
        'tag': {
            'naku_hitei',
        },
        'default_glyph': create_glyph(pdict['NakuHitei']),
        'glyphs': [
        ],
    },
    'Ni': {
        'tag': {
            'ni',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pdict['Ni']),
        'glyphs': [
        ],
    },
    'Nu': {
        'tag': {
            'nu',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pdict['Nu']),
        'glyphs': [
            create_glyph(pdict['Nu(?=S)'], key='@head_s[1]'),

        ],
    },
    'Nure': {
        'tag': {
            'nure'
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pdict['Nure']),
        'glyphs': [
            create_glyph(pdict['Nure$'], key=kdict['sp_or_eos']),
        ],
    },
    'Nihon': {
        'tag': {
            'nihon',
            '@head_e',
        },
        'default_glyph': create_glyph(pdict['Nihon']),
        'glyphs': [
            create_glyph(pdict['Nihon(jog)'], key='@head_e[1]'),
        ],
    },
    'NoJoshi': {
        'tag': {
            'no_joshi',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pdict['NoJoshi']),
        'glyphs': [
            create_glyph(pdict['Nu(?=S)'], key='@head_s[1]'),
        ],
    },
    'Ha': {
        'tag': {
            'ha',
            '@head_sel',
        },
        'default_glyph': create_glyph(pdict['Ha']),
        'glyphs': [
        ],
    },
    'Hi': {
        'tag': {
            'hi',
            '@head_sel',
        },
        'default_glyph': create_glyph(pdict['Hi']),
        'glyphs': [
        ],
    },
    'Hur': {
        'tag': {
            'hur',
            '@head_sel',
        },
        'default_glyph': create_glyph(pdict['Hur'], ascent=4),
        'glyphs': [
        ],
    },
    'Ho': {
        'tag': {
            'ho',
            '@head_sel',
        },
        'default_glyph': create_glyph(pdict['Ho'], ascent=6),
        'glyphs': [
            create_glyph(pdict['Ho(up)'], ascent=6, key="@head_e[1]|@head_el[1]")
        ],
    },
    'Hoku': {
        'tag': {
            'hoku',
            '@head_sel',
        },
        'default_glyph': create_glyph(pdict['Hoku'], ascent=6),
        'glyphs': [
            create_glyph(pdict['Hoku(up)'], ascent=6, key="@head_e[1]|@head_el[1]")
        ],
    },
    'N': {
        'tag': {
            'n',
        },
        'default_glyph': create_glyph(pdict['N']),
        'glyphs': [
            create_glyph(pdict['N$'], key=kdict['sp_or_eos']),
        ],
    },
    'Fu': {
        'tag': {
            'fu',
        },
        'default_glyph': create_glyph(pdict['Fu']),
        'glyphs': [
            create_glyph(pdict['Fu$'], key=kdict['sp_or_eos']),
        ],
    },
    'Futsu': {
        'tag': {
            'futsu',
        },
        'default_glyph': create_glyph(pdict['Futsu$'], post_offset=polar(2.5, 30)),
        'glyphs': [
        ],
    },
    'Ma': {
        'tag': {
            'ma',
            '@head_er',
            '@head_er8',
        },
        'default_glyph': create_glyph(pdict['Ma']),
        'glyphs': [
            create_glyph(pdict['MaNa'], key='@head_el8[1]'),
        ],
    },
    'Mi': {
        'tag': {
            'mi',
            '@head_er',
            '@head_er8',
        },
        'default_glyph': create_glyph(pdict['Mi']),
        'glyphs': [
            create_glyph(pdict['Mi(?=Na)'], key='@head_el8[1]'),
            create_glyph(pdict["Mi(?='E')"], key='@head_se[1]'),
        ],
    },
    'Me': {
        'tag': {
            'me',
            '@head_er',
            '@head_er16',
        },
        'default_glyph': create_glyph(pdict['Me']),
        'glyphs': [
            create_glyph(pdict["Me(?=Na)"], key='@head_el8[1]'),
            create_glyph(pdict["Me(?=S)"], key='@head_s[1]|@head_sw[1]'),
        ],
    },
    'Mo': {
        'tag': {
            'mo',
            '@head_er',
            '@head_er16',
        },
        'default_glyph': create_glyph(pdict['Mo']),
        'glyphs': [
        ],
    },
    'MoJoshi': {
        'tag': {
            'mo_joshi',
            '@head_er',
        },
        'default_glyph': create_glyph(pdict['MoJoshi']),
        'glyphs': [
        ],
    },
    'Mono': {
        'tag': {
            'mono',
        },
        'default_glyph': create_glyph(pdict['Mono']),
        'glyphs': [
        ],
    },
    'Wa': {
        'tag': {
            'wa',
        },
        'default_glyph': create_glyph(pdict['Wa'], ascent=1.0),
        'glyphs': [
            create_glyph(pdict['Wa(?=E)'], ascent=1.0, key='@head_e[1]'),
        ],
    },
    'Wagaku': {
        'tag': {
            'wagaku',
        },
        'default_glyph': create_glyph(pdict['WaNa'], ascent=1.0),
        'glyphs': [
        ],
    },
    'PosTsuKousa': {
        'tag': {
            'pos_tsu_kousa',
        },
        'default_glyph': create_pos_glyph(0, 0),
        'glyphs': [
            create_pos_glyph(-1.5, -1, key='shi[-1]'),
            create_pos_glyph(1.5, -1.5, key='no_joshi[-1].@head_er[1]'),
        ],
    },
    'PosAme': {
        'tag': {
            'pos_ame',
        },
        'default_glyph': create_pos_glyph(*polar(1.3, 120)),
        'glyphs': [
        ],
    },
    'PosIru': {
        'tag': {
            'pos_iru',
        },
        'default_glyph': create_pos_glyph(3, 0),
        'glyphs': [
            create_pos_glyph(3, -1, key='te_joshi[-1]')
        ],
    },
    'PosDake': {
        'tag': {
            'pos_dake',
        },
        'default_glyph': create_pos_glyph(-2, 1),
        'glyphs': [
            create_pos_glyph(-0.8, 1.5, key='ta[-1]')
        ],
    },
    'DotKa': {
        'tag': {
            'dot_ka',
        },
        'default_glyph': create_dot_glyph(-4, -1.5),
        'glyphs': [
            create_dot_glyph(-1, -2.0, key='wa[-1]')
        ],
    },
    'DotKata': {
        'tag': {
            'dot_kata',
        },
        'default_glyph': create_dot_glyph(*polar(3, 45)),
        'glyphs': [
            create_dot_glyph(5, 0.5, key='no_joshi[-1]')
        ],
    },
    'PosRare': {
        'tag': {
            'pos_rare',
        },
        'default_glyph': create_pos_glyph(*polar(2.3, -45)),
        'glyphs': [
        ],
    },
    'PosRou': {
        'tag': {
            'pos_rou',
        },
        'default_glyph': create_pos_glyph(-2.6, 0.8),
        'glyphs': [
        ],
    },
    'PosUchi': {
        'tag': {
            'pos_uchi',
        },
        'default_glyph': create_pos_glyph(1.5, -1.5),
        'glyphs': [
        ],
    },
    'DotNaka': {
        'tag': {
            'dot_naka',
        },
        'default_glyph': create_dot_glyph(0, -1.5),
        'glyphs': [
        ],
    },
}

tdict = {
    'waseda': {
        'dictionary': wdict,
        'character': cdict,
    },
}



if __name__ == '__main__':
    def default(obj):
        if isinstance(obj, set):
            return {key: None for key in obj}
        raise TypeError(f'Cannot serialize object of {type(obj)}')
    with open('waseda.json', 'w', encoding='utf8') as f:
        json.dump(tdict, f, ensure_ascii=False, default=default)
