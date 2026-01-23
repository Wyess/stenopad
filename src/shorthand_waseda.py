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

pd = {}
pd["A."] = "O{-30} .. tension 1.2 .. 4E"
pd["A"] = pd["A."] + "{90}"
pd["Ah(?=EL)"] = pd["A"] + " .. @(-0.9, -1) + (130: 1.7) .. ++(130: -1.7)"
pd["Ah"] = pd["Ah(?=EL)"] + "{-30}"
pd["Ai"] = "O{170} .. 3.5N .. {-170}O"
pd["I."] = "O{30} .. tension 1.0 .. 4E"
pd["I"] = pd["I."] + "{-100}"
pd["I(?=Ta)"] = pd["I."] + "{ta_angle}"
pd["U"] = "O -- 4S"
pd["E"] = "O -- 4SSE"
pd["Ketsu"] = "O -- 8SE"
pd["E(?=SW)"] = "O -- 4SE"
pd["Shite"] = "O -- 3SE"
pd["Sha."] = "O{-60} .. 8S"
pd["Sha"] = pd["Sha."] + "{-135}"
pd["O"] = "O -- 4SSW"
pd["O(jog)"] = "O -- 4SSW -- ++(45: 1)"
pd["Oo"] = "O --- 3.5SSW .. (4SSW + 0.5ESE) .. @(-1.3, -1)"
pd["Kai"] = "O -- 4E"
pd["Kai(jog)"] = pd["Kai"] + "-- ++(-170: 1)"
pd["Ka"] = "O -- 8E"
pd["Ka(jog)"] = pd["Ka"] + "-- ++(-170: 1)"
pd["Karu"] = pd["Ka"] + "-- ++(0, -1.5)"
pd["Ki"] = "O --- 7.5E .. 8E + 0.5N .. {-150}@(6, -1)"
pd["Ki(?=EL)"] = "O --- 7.5E .. 8E + 0.5N .. tension 1.1 .. @(7.5, -1) + (140: 1.3) .. ++(140: -1.3)"
pd["Ku"] = "O --- 7.5E .. 8E + 2.0N .. {-140}@(4.5, -1)"
pd["Ke"] = "O --- 15.5E .. 16E + 0.5N .. {-150}@(14, -1)"
pd["Ker"] = "O -- 16E -- ++4NW"
pd["Ko"] = "O -- 16E"
pd["Ko(jog)"] = pd["Ko"] + "-- ++(-170: 1)"
pd["Koto"] = "O -- 8S"
pd["Koto(jog)"] = pd["Koto"] + "-- ++(80: 1)"
pd["Kon2"] = "O -- 8E -- ++4S"
pd["Kokoro"] = "O -- 8E -- ++4SSW"
pd["Kyou"] = "O -- ++(60: -3) -- ++(30: 2) -- ++(60:-3)"
pd["Sa."] = "O{30} .. tension 1.3 .. (45: 8)"
pd["Sa"] = pd["Sa."] + "{90}"
pd["Sa(bend)"] = pd["Sa."] + "{120}"
pd["Satsu."] = "(1.5, 0){90} .. tension 1.2 .. ++O{-60} .. ++(1.5, 0) .. tension 1.3 .. ++(45: 8)"
pd["Satsu"] = pd["Satsu."] + "{90}"
pd["SaHenki"] = "O{-90} .. tension 1.2 .. {180}(-120: 8)"
pd["Shi(?=EL)"] = "O{30} .. tension 1.3 .. {150}(60: 7) .. @(-1.8, -1) + (130: 1.8) .. ++(130: -1.8)"
pd["Shin"] = "O{30} .. tension 1.3 .. {150}(60: 8) .. tension 1.1 .. @(-0.4, -1) + (195: 2.0) ..  @(-0.4, -2) + (30: -1.5) -- ++(30: 3.0) "
pd["Shimi"] = "O{90} .. tension 1.2 .. {-45}4NE .. tension 1.2 .. {-135}2ESE"
pd["Su(?=EL)"] = "O{30} .. tension 1.3 .. {140}(60: 6.5) .. @(-2.5, -1) + (130: 2.8) .. ++(130: -2.8)"
pd["Su"] = pd["Su(?=EL)"] + "{-30}"
pd["Su(?=ER)"] = "O{30} .. tension 1.3 .. {140}(60: 6.5) .. tension 1.5 .. @(-2.5, -1) + (10: -2.5) .. ++(10: 2.5)"
pd["So."] = "O{34} .. tension 1.6 .. (45: 16)"
pd["So"] = pd["So."] + "{90}"
pd["Shourai"] = "O -- 4E 2E -- ++4S"
pd["Ta"] = "O -- (ta_angle: 8)"
pd["Taxe."] = "O -- (ta_angle: 8) (ta_angle: 7) -- ++(-45: 0.1)"
pd["Taxe"] = "O -- (ta_angle: 8) (ta_angle: 7) -- ++(-45: 0.5)"
pd["TaHenki"] = "O -- (30: 8)"
pd["Tajuon"] = "O -- 30E"
pd["Cha"] = "O -- (22.5: 8)"
pd["Che"] = "O -- (22.5: 7.5){22.5} .. ++(22.5-90: 0.9) .. @(-1.0, -2)"
pd["ChaHenki"] = "O -- (45: -8)"
pd["TeJoshi"] = "O -- (60: -4.0){100} .. {145}++(108: 1.9)"
pd["TeJoshi(?=Ha)"] = "O --- (60: -3.0) .. (60: -4.0) + (150: 0.5) .. tension 1.1 .. (60: -4) + (80: 1.3) .. {-90}(60:-4)"
pd["Terx"] = "O --- (60: -3.0) .. (60: -4.0) + (150: 0.3) .. tension 1.1 .. (60: -4) + (90: 1.2){-90} .. {-90}(60:-4) + S"
pd["To"] = "O -- (40: 16)"
pd["To(?=E)"] = "O -- (45: 16)"
pd["ToHenki"] = "O -- (to_henki_angle: 16)"
pd["ToJoshi"] = "O -- (60: -4.0){30} .. {0}++(30: 1.9)"
pd["Tsu"] = "O -- 3.5S{S} .. 4S + 0.5W .. {45}@(-1.2, -2)"
pd["Tsu(?=ER)"] = "O -- 3.5S{S} .. 4S + 1.0W .. @(-0.9, -2)"
pd["Nu(?=S)"] = "O{-30} .. tension 1.7 .. 8E .. tension 1.3 .. {-90}@(-3.2, -1) + 1.3N .. ++1.3S"
pd["NoJoshi"] = "O{-30} .. tension 1.7 .. 8E .. {190}++(145:4)"
pd["NaiHitei"] = "(60: 1.5) -- +(-120: 3)"
pd["NakuHitei"] = "(0, 1.5) -- (0, -1.5)"
pd["Nihon"] = "O -- +4E 2S -- ++4E"
pd["Ha"] = "O{-90} .. tension 1.0 .. {0}(-60: 8)"
pd["Hi"] = "O{-90} .. tension 1.0 .. {20}(-60: 8) .. @(-1.2, -1) + (45: 2) .. {-135}++(45: -2)"
pd["Hu"] = "O{-90} .. tension 1.0 .. {0}(-60: 8) .. @(-5, -1){180}"
pd["Hure"] = "O{-90} .. tension 1.0 .. {0}(-60: 8) .. ++(90: 2.5) .. {-60}@(-0.5: -2) + (115: 2) -- @(-0.5, -3) + (-60: 1.0)"
pd["Hur"] = "O{-90} .. tension 1.0 .. {0}(-60: 8) .. ++(110: 3.5){150}"
pd["Ho"] = "O{-90} .. tension 1.0 .. {0}(-60: 16)"
pd["Hoku"] = "(45: -1.5) .. {90}O{-90} .. tension 1.0 .. {0}(-60: 16)"
pd["Ho(up)"] = "O{-90} .. tension 1.0 .. {45}(-60: 16)"
pd["Hoku(up)"] = "(45: -1.5) .. {90}O{-90} .. tension 1.0 .. {45}(-60: 16)"
pd["Ma."] = "O{30} .. tension 1.3 .. 8E"
pd["MoJoshi."] = "O{30} .. tension 1.7 .. 8E .. ++(45: -4)"
pd["Mo."] = "O{20} .. tension 1.8 .. 16E"
pd["N"] = "O -- (45: 2)"
pd["Fu"] = "O -- (30: 4)"
pd["Koi"] = "O -- (30: 4)"
pd["Futsu"] = "(30: 1){-45} .. (-60: 0.8) .. {30}O -- (30: 4)"
pd["Wa"] = "O{-164} .. tension 1.4 .. (-124: 3){-70} .. {20}(-80: 3)"
pd["Wa."] = "O{-164} .. tension 1.4 .. (-124: 3){-70} .. (-80: 3)"
pd["Wa(?=EL)"] = "O{-190} .. (-115: 3)"
pd["Wa(?=E)"] = "O{-164} .. tension 1.4 .. (-124: 3){-70} .. {0}(-80: 3.2)"

pd["KiTa"] = "O --- 7.5E .. 8E + 1.3N .. {-120}(6.8, 0) + (60: 1.3) -- (6.8, 0)"
pd["KeSaHenki"] = "O --- 15.5E .. 16E + 0.5N .. @(15.3, -1)+ (95: 1.5) .. ++(95: -1.5) & " + pd["SaHenki"]
pd["Shi"] = pd["Shi(?=EL)"] + "{-30}"
pd["Shimiru"] = pd["Shimi"] + " -- ++1.5S"
pd["Sore"] = "O{-90} .. {180}(45: -4)"
pd["Se"] = "O{34} .. tension 1.9 .. {140}(50: 15) .. @(-1.7, -1) + (130: 2.0) .. {-60}++(130: -2.0)"
pd["Sen"] = "O{34} .. tension 1.9 .. {140}(50: 15) .. tension 1.1 .. @(-0.4, -1) + (195: 2.0) ..  @(-0.4, -2) + (30: -1.5) -- ++(30: 3.0)"
pd["Na."] = "O{-30} .. tension 1.3 .. 8E"
pd["Na"] = pd["Na."] + "{90}"
pd["Nan"] = pd["Na."] + "{45}"
pd["Naru"] = pd["Na."] + "{80} .. {S}++1.5S"
pd["Ma"] = pd["Ma."] + "{-90}"
pd["Ii"] = pd["I."] + "{-90} .. @(-0.7, -1) + (60: -1.8) .. {60}++(60: 1.8)"
pd["Ii(?=S)"] = pd["I."] + "{-90} .. {90}@(-1.8, -1) "
pd["Mi"] = pd["Ma."] + "{-90} .. @(-0.7, -1) + (60: -1.8) .. {60}++(60: 1.8)"
pd["Me"] = pd["Mo."] + "{-90} .. @(-0.7, -1) + (60: -1.8) .. {60}++(60: 1.8)"
pd["Me(?=S)"] = pd["Mo."] + "{-90} .. {90}@(-2.3, -1) "
pd["Mo"] = pd["Mo."] + "{-80}"
pd["MoJoshi"] = pd['MoJoshi.'] + "{-180}"
pd["Mono"] = pd['Mo.'] + "{-90} .. {180}++(-145: 4)"
pd["Nihon(jog)"] = pd["Nihon"] + "-- ++(-170: 1)"

pd["Ni(?=EL)"] = pd["Na"] + " .. @(-0.5, -1) + (130: 1.7) .. ++(130: -1.7)"
pd["Ni"] = pd["Ni(?=EL)"] + "{-30}"
pd["NiNa"] = cat(("Ni(?=EL)", "Na"), pd)
pd["Nu"] = pd["Na"] + " .. @(-4.5, -1) + (45: 1.7) .. {-135} ++(45: -1.7)"
pd["Nure"] = pd["Na"] + " .. tension 1.5 .. @(-3.0, -1) + (135: 2.7) .. {-30} ++(135: -3.7)"
pd["Mi(?=Na)"] = pd["Ma."] + "{-120} .. @(-0.5, -1) + (180: 1.5) .. ++(180: -1.5)" + "&" + pd['Na']
pd["Mi(?='E')"] = pd["Ma."] + "{-90} .. ++(210: 1.5) .. {SSE}@(-0.0, -1) + 1.2NNE -- ++1.2SSE"
pd["Me(?=Na)"] = "O{20} .. tension 1.8 .. 16E{-120} .. @(-0.5, -1) + (180: 1.5) .. ++(180: -1.5)" + "&" + pd['Na']
pd["SuMa"] = pd["Su(?=ER)"] + '&' + pd['Ma']
pd["KiNa"] = pd["Ki(?=EL)"] + "&" +  pd["Na"]
pd["MaNa"] = pd["Ma."] + "&" + pd["Na"]
pd["TsuMo"] = pd["Tsu(?=ER)"] + "&" + pd["Mo"]
pd["WaNa"] = pd["Wa(?=EL)"] + "&" + pd["Na"]

pd["AI"] = cat(("A.", "I"), pd)


wdict = {
    'SEPARATOR': '・',
    ' ': 'Space',
    '　': 'Space',
    '\n': 'Newline',
    'あ': 'A',
    'あい': 'Ai',
    '雨': ['A', 'PosAme', 'E'],
    'ある（点）': 'Aru(dot)',
    'あるｐ': 'Aru(dot)',
    'い': 'I',
    'いい': 'Ii',
    'いる': ['PosIru', 'I'],
    'う': 'U',
    'うち（交差）': ['PosUchi', 'U'],
    'うちｃ': ['PosUchi', 'U'],
    'たい': 'Tai',
    '多重音': ['PosTajuon', 'Tajuon'],
    'っ': 'SmallTsu',
    'え': 'E',
    'お': 'O',
    'か': 'Ka',
    '傘': ['Ka', 'Sa'],
    'か（点）': 'DotKa',
    'かｐ': 'DotKa',
    'かた（点）': 'DotKata',
    'かたｐ': 'DotKata',
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
    'けｒ': 'Ker',
    'こ': 'Ko',
    'こい': 'Koi',
    'こえ': 'Koi',
    'こく': 'Koi',
    '心': 'Kokoro',
    '事': 'Koto',
    'コン': 'Kon2',
    'さ': 'Sa',
    'さつ（交差）': ['PosTsuKousa', 'Sa'],
    'さつｃ': ['PosTsuKousa', 'Sa'],
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
    'するｐ': 'DotSuru',
    'た': 'Ta',
    '誰': 'Taxe',
    'た（え略）': 'Taxe',
    'たぇ': 'Taxe',
    'だけ': ['PosDake', 'Ta'],
    'たまに': ['Ta', 'PosTamani', 'Ni'],
    'つ': 'Tsu',
    'て（助詞）': 'TeJoshi',
    'てｊ': 'TeJoshi',
    'テｒ': 'Terx',
    'と': 'To',
    'と（助詞）': 'ToJoshi',
    'とｊ': 'ToJoshi',
    'ちゃ': 'Cha',
    'ちぇ': 'Che',
    'てｒ': 'Che',
    'な': 'Na',
    'なか（点）': 'DotNaka',
    'なかｐ': 'DotNaka',
    'なる': 'Naru',
    'なん': 'Nan',
    '何': 'Nan',
    '日本': 'Nihon',
    'ない（否定）': 'NaiHitei',
    'ないｘ': 'NaiHitei',
    'なく（否定）': ['PosNaku', 'NakuHitei'],
    'なくｘ': ['PosNaku', 'NakuHitei'],
    'に': 'Ni',
    'ぬ': 'Nu',
    'ぬれ': 'Nure',
    'の（助詞）': 'NoJoshi',
    'のｊ': 'NoJoshi',
    'は': 'Ha',
    'ひ': 'Hi',
    'ふ': 'Hu',
    'はな': 'Hu',
    'ふれ': 'Hure',
    'はなれ': 'Hure',
    'フ': 'Fu',
    'ふつ': 'Futsu',
    'ふｒ': 'Hur',
    '問題': 'Futsu',
    'ほ': 'Ho',
    'ほく': 'Hoku',
    'ま': 'Ma',
    'まつ（交差）': ['PosTsuKousa', 'Ma'],
    'まつｃ': ['PosTsuKousa', 'Ma'],
    'み': 'Mi',
    'め': 'Me',
    'も': 'Mo',
    'も（助詞）': 'MoJoshi',
    'もｊ': 'MoJoshi',
    '物': 'Mono',
    '者': 'Mono',
    'もの': 'Mono',
    'ら（点）': 'Ra(dot)',
    'らｐ': 'Ra(dot)',
    'られ': ['PosRare', 'Wa'],
    'ろう': ['PosRou', 'A'],
    'わ': 'Wa',
    'わが国': ['Wagaku', 'Ni'],
    'を': 'O',
    'ん': 'N',
}

def create_dot_glyph(x, y, r=0.08, key='default'):
    return create_glyph(f"({x}, {y + r}){{0}} ... ({x + r}, {y}) .. ({x}, {y - r}) .. ({x - r}, {y}) .. {{0}}({x}, {y + r})", key=key)

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
        'tag': {'null'},
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
    'Ra(dot)': {
        'tag': {
            'ra_dot',
            '@dot',
        },
        'default_glyph': create_dot_glyph(-4, 2),
        'glyphs': [
            create_dot_glyph(-7, 2, key='ho[-1]|hoku[-1]'),
        ],
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
        'default_glyph': create_glyph(pd['A']),
        'glyphs': [
            create_glyph(pd['AI'], key='i[1]')
        ],
    },
    'Ai': {
        'tag': {
            'ai',
            'cr4',
        },
        'default_glyph': create_glyph(pd['Ai'], ascent=-2),
        'glyphs': [
        ],
    },
    'I': {
        'tag': {
            'i',
            'er4',
        },
        'default_glyph': create_glyph(pd['I']),
        'glyphs': [
            create_glyph(pd['I(?=Ta)'], key='ta[1]'),
        ],
    },
    'Ii': {
        'tag': {
            'ii',
            '@head_er',
            '@head_er4',
            'er4cr1',
        },
        'default_glyph': create_glyph(pd['Ii']),
        'glyphs': [
             create_glyph(pd['Ii(?=S)']),
        ],
    },
    'U': {
        'tag': {
            'u',
            's4',
        },
        'default_glyph': create_glyph(pd['U']),
        'glyphs': [
        ],
    },
    'Tai': {
        'tag': {
            'tai',
            's4',
            '@head_s',
        },
        'default_glyph': create_glyph(pd['U']),
        'glyphs': [
        ],
    },
    'Shourai': {
        'tag': {
            'shourai',
            'e4-s4',
        },
        'default_glyph': create_glyph(pd['Shourai']),
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
        'default_glyph': create_glyph(pd['E']),
        'glyphs': [
            create_glyph(pd['E(?=SW)'], key='@head_sw[1]'),
        ],
    },
    'Shite': {
        'tag': {
            'shite',
            'se3',
        },
        'default_glyph': create_glyph(pd['Shite']),
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
        'default_glyph': create_glyph(pd['O']),
        'glyphs': [
            create_glyph(pd['O(jog)'], key='@head_sw[1]'),
        ],
    },
    'Oo': {
        'tag': {
            'oo',
            'sw4cl1',
            '@head_sw',
        },
        'default_glyph': create_glyph(pd['Oo'], name='Oo'),
        'glyphs': [
            create_glyph(pd['Oo'], name='Oo'),
        ],
    },
    'Ka': {
        'tag': {
            'ka',
            'e8',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Ka']),
        'glyphs': [
            create_glyph(pd['Ka(jog)'], key='@head_e[1]'),
        ],
    },
    'Kai': {
        'tag': {
            'kai',
            'e4',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Kai']),
        'glyphs': [
            create_glyph(pd['Kai(jog)'], key='@head_e[1]'),
        ],
    },
    'Karu': {
        'tag': {
            'karu',
            'e8s1f',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Karu'], post_offset=(0, -2.5)),
        'glyphs': [
        ],
    },
    'Ki': {
        'tag': {
            'ki',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Ki']),
        'glyphs': [
            create_glyph(pd['KiTa'], key='ta[1]'),
            create_glyph(pd['KiNa'], key='@head_el8[1]'),
        ],
    },
    'Kyou': {
        'tag': {
            'kyou',
        },
        'default_glyph': create_glyph(pd['Kyou'], ascent=2),
        'glyphs': [
        ],
    },
    'Ku': {
        'tag': {
            'ku',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Ku']),
        'glyphs': [
        ],
    },
    'Ke': { 
        'tag': {
            'ke',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Ke']),
        'glyphs': [
            create_glyph(pd["KeSaHenki"], key="sa_henki[1]"),
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
        'default_glyph': create_glyph(pd['Ketsu']),
        'glyphs': [
        ],
    },
    'Ker': {
        'tag': {
            'ker',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Ker']),
        'glyphs': [
        ],
    },
    'Ko': {
        'tag': {
            'ko',
            'e16',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Ko']),
        'glyphs': [
            create_glyph(pd['Ko(jog)'], key='@head_e[1]'),
        ],
    },
    'Koi': {
        'tag': {
            'koi',
            'ne4',
            '@head_ne',
        },
        'default_glyph': create_glyph(pd['Koi']),
        'glyphs': [
            #create_glyph(pd['Ko(jog)'], key='@head_e[1]'),
        ],
    },
    'Koto': {
        'tag': {
            'koto',
            's8',
            '@head_s',
            '@tail_s',
        },
        'default_glyph': create_glyph(pd['Koto']),
        'glyphs': [
            create_glyph(pd['Koto(jog)'], key='@head_s[1]'),
        ],
    },
    'Kon2': {
        'tag': {
            'kon',
            'e8s4f',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Kon2'], post_offset=(0, -3)),
        'glyphs': [
        ],
    },
    'Kokoro': {
        'tag': {
            'kokoro',
            'e8sw4f',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Kokoro'], post_offset=polar(-2.5, 60)),
        'glyphs': [
        ],
    },
    'Sa': {
        'tag': {
            'sa',
            '@head_nel',
        },
        'default_glyph': create_glyph(pd['Sa'], ascent=-1.5),
        'glyphs': [
            create_glyph(pd['SaHenki'], key="@head_e[-1]", name='SaHenki'),
        ],
    },
    'Satsu': {
        'tag': {
            'satsu',
        },
        'default_glyph': create_glyph(pd['Satsu'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'SaHenki': {
        'tag': {
            'sa_henki',
            '@head_swr',
        },
        'default_glyph': create_glyph(pd['SaHenki'], name='SaHenki'),
        'glyphs': [
        ],
    },
    'Shi': {
        'tag': {
            'shi',
            '@head_nel',
        },
        'default_glyph': create_glyph(pd['Shi'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'Shin': {
        'tag': {
            'shin',
            '@head_nel',
        },
        'default_glyph': create_glyph(pd['Shin'], ascent=-1.5, post_offset=polar(3, 30)),
        'glyphs': [
        ],
    },
    'Sha': {
        'tag': {
            'sha',
            '@head_sr',
        },
        'default_glyph': create_glyph(pd['Sha'], ascent=4),
        'glyphs': [
        ],
    },
    'Shimi': {
        'tag': {
            'shimi',
            '@head_ner',
        },
        'default_glyph': create_glyph(pd['Shimi'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'Shimiru': {
        'tag': {
            'shimiru',
            '@head_ner',
        },
        'default_glyph': create_glyph(pd['Shimiru'], ascent=-1.5, post_offset=(0, -2.5)),
        'glyphs': [
        ],
    },
    'Su': {
        'tag': {
            'su',
            '@head_nel',
        },
        'default_glyph': create_glyph(pd['Su'], ascent=-1.5),
        'glyphs': [
            create_glyph(pd['SuMa'], key='@head_er8[1]', ascent=-1.5),
        ],
    },
    'Se': {
        'tag': {
            'se',
            '@head_nel',
        },
        'default_glyph': create_glyph(pd['Se'], ascent=-8.0),
        'glyphs': [
        ],
    },
    'Sen': {
        'tag': {
            'sen',
            '@head_nel',
        },
        'default_glyph': create_glyph(pd['Sen'], ascent=-8.0, post_offset=polar(3, 30)),
        'glyphs': [
        ],
    },
    'So': {
        'tag': {
            'so',
            '@head_nel',
        },
        'default_glyph': create_glyph(pd['So'], ascent=-8.0),
        'glyphs': [
        ],
    },
    'Sore': {
        'tag': {
            'sore',
            '@head_swr',
        },
        'default_glyph': create_glyph(pd['Sore'], ascent=2.0, post_offset=(-2, -0.5)),
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
        'default_glyph': create_glyph(pd['Ta'], ascent=1.5),
        'glyphs': [
            create_glyph(pd['TaHenki'], key='(ta[-1]|@tail_s[-1])|(ta[-2].pos_dake[-1])', ascent=1.5, name='TaHenki'),
        ],
    },
    'Taxe': {
        'tag': {
            'taxe',
            '@head_sw',
        },
        'default_glyph': create_glyph(pd['Taxe'], ascent=1.5),
        'glyphs': [
            create_glyph(pd['Taxe.'], ascent=1.5, key='!@head_sw[1].!' + kdict['sp_or_eos']),
        ],
    },
    'Tajuon': {
        'tag': {
            'tajuon',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Tajuon'], post_offset=(2, 0)),
        'glyphs': [
        ],
    },
    'PosTajuon': {
        'tag': {
            'pos_tajuon',
        },
        'default_glyph': create_pos_glyph(0, 5),
        'glyphs': [
        ],
    },
    'ChaHenki': {
        'tag': {
            'cha_henki',
            '@head_sw',
        },
        'default_glyph': create_glyph(pd['ChaHenki'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'TaHenki': {
        'tag': {
            'ta_henki',
            '@head_ne',
        },
        'default_glyph': create_glyph(pd['TaHenki'], ascent=-1.5),
        'glyphs': [
        ],
    },
    'Cha': {
        'tag': {
            'cha',
            '@head_ne',
        },
        'default_glyph': create_glyph(pd['Cha'], ascent=-1),
        'glyphs': [
            create_glyph(pd['ChaHenki'], key='ta_henki[-1]|cha[-1]', ascent=-1, name='ChaHenki'),
        ],
    },
    'Che': {
        'tag': {
            'che',
            '@head_ne',
        },
        'default_glyph': create_glyph(pd['Che'], ascent=-1),
        'glyphs': [
        ],
    },
    'Tsu': {
        'tag': {
            'tsu',
            '@head_s',
        },
        'default_glyph': create_glyph(pd['Tsu'], ascent=2),
        'glyphs': [
            create_glyph(pd['TsuMo'], ascent=2, key='@head_er16[1]'),
        ],
    },
    'SmallTsu': {
        'tag': {
            'small_tsu',
        },
        'default_glyph': create_pos_glyph(0, -2),
        'glyphs': [
            create_pos_glyph(-2, 4, key='@tail_se8[-1].@head_sw4[1]'),
            create_pos_glyph(-1, 0, key='a[-1].@head_sw[1]'),
        ],
    },
    'TeJoshi': {
        'tag': {
            'te_joshi',
            '@head_sw',
        },
        'default_glyph': create_glyph(pd['TeJoshi'], ascent=-1),
        'glyphs': [
            create_glyph(pd['TeJoshi(?=Ha)'], ascent=-1, key='ha[1]'),
        ],
    },
    'Terx': {
        'tag': {
            'terx',
            '@head_sw',
            '@head_sw4',
        },
        'default_glyph': create_glyph(pd['Terx'], ascent=1, post_offset=(0, -0.5)),
        'glyphs': [
        ],
    },
    'To': {
        'tag': {
            'to',
            '@head_ne',
        },
        'default_glyph': create_glyph(pd['To'], ascent=-2.5),
        'glyphs': [
            create_glyph(pd['To(?=E)'], key='@head_e[1]', ascent=-2.5),
            create_glyph(pd['ToHenki'], key='@head_ne[-1]', ascent=2.5, name='ToHenki'),
        ],
    },
    'ToHenki': {
        'tag': {
            'to_henki',
            '@head_sw',
        },
        'default_glyph': create_glyph(pd['ToHenki'], ascent=-2.5, name='ToHenki'),
        'glyphs': [
            create_glyph(pd['ToHenki'], key='@head_e[1]', ascent=-2.5),
        ],
    },
    'ToJoshi': {
        'tag': {
            'to_joshi',
            '@head_sw',
        },
        'default_glyph': create_glyph(pd['ToJoshi'], ascent=-1.5),
        'glyphs': [
            create_glyph(pd['Oo'], key=f"!({kdict['sp_or_eos']}).!null[1]", name='Oo')
        ],
    },
    'Na': {
        'tag': {
            'na',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pd['Na']),
        'glyphs': [
        ],
    },
    'Naru': {
        'tag': {
            'naru',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pd['Naru'], post_offset=(0, -2)),
        'glyphs': [
        ],
    },
    'Nan': {
        'tag': {
            'nan',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pd['Nan'], post_offset=polar(2.5, 45)),
        'glyphs': [
        ],
    },
    'NaiHitei': {
        'tag': {
            'nai_hitei',
        },
        'default_glyph': create_glyph("1.5W + " + pd['NaiHitei']),
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
        'default_glyph': create_glyph(pd['NakuHitei']),
        'glyphs': [
        ],
    },
    'Ni': {
        'tag': {
            'ni',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pd['Ni']),
        'glyphs': [
        ],
    },
    'Nu': {
        'tag': {
            'nu',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pd['Nu']),
        'glyphs': [
            create_glyph(pd['Nu(?=S)'], key='@head_s[1]'),

        ],
    },
    'Nure': {
        'tag': {
            'nure'
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pd['Nure'], post_offset=polar(1.5, -30)),
        'glyphs': [
        ],
    },
    'Nihon': {
        'tag': {
            'nihon',
            '@head_e',
        },
        'default_glyph': create_glyph(pd['Nihon']),
        'glyphs': [
            create_glyph(pd['Nihon(jog)'], key='@head_e[1]'),
        ],
    },
    'NoJoshi': {
        'tag': {
            'no_joshi',
            '@head_el',
            '@head_el8',
        },
        'default_glyph': create_glyph(pd['NoJoshi']),
        'glyphs': [
            create_glyph(pd['Nu(?=S)'], key='@head_s[1]'),
        ],
    },
    'Ha': {
        'tag': {
            'ha',
            '@head_sel',
        },
        'default_glyph': create_glyph(pd['Ha']),
        'glyphs': [
        ],
    },
    'Hi': {
        'tag': {
            'hi',
            '@head_sel',
        },
        'default_glyph': create_glyph(pd['Hi']),
        'glyphs': [
        ],
    },
    'Hu': {
        'tag': {
            'hu',
            '@head_sel',
        },
        'default_glyph': create_glyph(pd['Hu']),
        'glyphs': [
        ],
    },
    'Hur': {
        'tag': {
            'hur',
            '@head_sel',
        },
        'default_glyph': create_glyph(pd['Hur'], ascent=4),
        'glyphs': [
        ],
    },
    'Hure': {
        'tag': {
            'hure',
            '@head_sel',
        },
        'default_glyph': create_glyph(pd['Hure']),
        'glyphs': [
        ],
    },
    'Ho': {
        'tag': {
            'ho',
            '@head_sel',
        },
        'default_glyph': create_glyph(pd['Ho'], ascent=6),
        'glyphs': [
            create_glyph(pd['Ho(up)'], ascent=6, key="@head_e[1]|@head_el[1]")
        ],
    },
    'Hoku': {
        'tag': {
            'hoku',
            '@head_sel',
        },
        'default_glyph': create_glyph(pd['Hoku'], ascent=6),
        'glyphs': [
            create_glyph(pd['Hoku(up)'], ascent=6, key="@head_e[1]|@head_el[1]")
        ],
    },
    'N': {
        'tag': {
            'n',
        },
        'default_glyph': create_glyph(pd['N'], key=kdict['sp_or_eos'], post_offset=polar(2, 45)),

        'glyphs': [
        ],
    },
    'Fu': {
        'tag': {
            'fu',
        },
        'default_glyph': create_glyph(pd['Fu'], post_offset=polar(2.5, 30)),
        'glyphs': [
        ],
    },
    'Futsu': {
        'tag': {
            'futsu',
        },
        'default_glyph': create_glyph(pd['Futsu'], post_offset=polar(2.5, 30)),
        'glyphs': [
        ],
    },
    'Ma': {
        'tag': {
            'ma',
            '@head_er',
            '@head_er8',
        },
        'default_glyph': create_glyph(pd['Ma']),
        'glyphs': [
            create_glyph(pd['MaNa'], key='@head_el8[1]'),
        ],
    },
    'Mi': {
        'tag': {
            'mi',
            '@head_er',
            '@head_er8',
        },
        'default_glyph': create_glyph(pd['Mi']),
        'glyphs': [
            create_glyph(pd['Mi(?=Na)'], key='@head_el8[1]'),
            create_glyph(pd["Mi(?='E')"], key='@head_se[1]'),
        ],
    },
    'Me': {
        'tag': {
            'me',
            '@head_er',
            '@head_er16',
        },
        'default_glyph': create_glyph(pd['Me']),
        'glyphs': [
            create_glyph(pd["Me(?=Na)"], key='@head_el8[1]'),
            create_glyph(pd["Me(?=S)"], key='@head_s[1]|@head_sw[1]'),
        ],
    },
    'Mo': {
        'tag': {
            'mo',
            '@head_er',
            '@head_er16',
        },
        'default_glyph': create_glyph(pd['Mo']),
        'glyphs': [
        ],
    },
    'MoJoshi': {
        'tag': {
            'mo_joshi',
            '@head_er',
        },
        'default_glyph': create_glyph(pd['MoJoshi']),
        'glyphs': [
        ],
    },
    'Mono': {
        'tag': {
            'mono',
        },
        'default_glyph': create_glyph(pd['Mono']),
        'glyphs': [
        ],
    },
    'Wa': {
        'tag': {
            'wa',
        },
        'default_glyph': create_glyph(pd['Wa'], ascent=1.0),
        'glyphs': [
            create_glyph(pd['Wa(?=E)'], ascent=1.0, key='@head_e[1]'),
        ],
    },
    'Wagaku': {
        'tag': {
            'wagaku',
        },
        'default_glyph': create_glyph(pd['WaNa'], ascent=1.0),
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
    'PosTamani': {
        'tag': {
            'pos_tamani',
        },
        'default_glyph': create_pos_glyph(0.5, 4.5),
        'glyphs': [
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

trie = {}
for key in wdict:
    node = trie
    for char in key:
        node = node.setdefault(char, {})
    node['word'] = key

tdict = {
    'waseda': {
        'dictionary': wdict,
        'trie': trie,
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
