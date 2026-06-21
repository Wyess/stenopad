#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pytest
from metasteno import z, Op
from pyx.metapost.path import (
    beginknot,
    endknot,
    smoothknot,
    roughknot,
    tensioncurve,
    controlcurve,
    line,
)
import pyx



# 💡 2. データ駆動テストケースの定義 (入力式, 期待するSVGパス)
METASTENO_TEST_CASES = [
    # --- 基本的な点・パース確認 ---
    (z[1: 90], "Point(x=6.123233995736766e-17, y=1.0, neg_count=0, is_relative=False)"), # 💡 点単体はSVGパスがないため、これだけ個別にstrで検証するか、今回は除外も可能です
    (z[1, 0: 90], "Point(x=6.123233995736766e-17, y=1.0, neg_count=0, is_relative=False)"),

    # --- 過去に実装していた << 演算子のパタン (※もし現在廃止・移行済みならコメントアウトしてください) ---
    #(z[0] << {-30}, "M0 -0"),
    #(z[0] << 1, "M0 -0"),
    #(z[0] << 1 << {2}, "M0 -0"),
    #(z[0] << {1} << 2, "M0 -0"),

    # --- 基本的な接続パタン (>> 演算子) ---
    (z[0] >> z[1, 2], "M0 -0C0.333333 -0.666667 0.666667 -1.33333 1 -2"),
    (z[0] >> 1, "M0 -0"),
    (z[0] >> {1}, "M0 -0"),
    (z[0] >> 1 >> {2}, "M0 -0"),
    (z[0] >> {1} >> 2, "M0 -0"),

    # --- テンション・角度指定を伴う曲線接続 ---
    (z[0] >> 1 >> z[2, 3], "M0 -0C0.666667 -1 1.33333 -2 2 -3"),
    (z[0] >> {1} >> z[2, 3], "M0 -0C-0.56441 -1.42409 0.468372 -2.97327 2 -3"),
    (z[0] >> 1 >> {2} >> z[3, 4], "M0 -0C-0.504491 -1.98496 0.953185 -3.92852 3 -4"),

    # --- 直線接続 (-- 演算子 / Op.LINE2) ---
    (z[0, 1] -- z[2, 3], "M0 -1L2 -3"),

    # --- MetaPost流の高度な角度・テンション制御 ---
    (z[0]@{-30} >> 1 >> {2} >> z[3, 4], "M0 -0C2.88855 1.6677 1.40689 -3.94437 3 -4"),
    (z[0]@{-30} >> 1 >> {90}@z[3, 4], "M0 -0C1.57522 0.909453 3 -1.30054 3 -4"),

    # --- 複素数リテラル / タプルによるテンションの空中キャッチ ---
    (z[0]@{-30} >> 1+2j >> {90}@z[3, 4], "M0 -0C1.57522 0.909453 3 -2.65027 3 -4"),
    (z[0]@{-30} >> (1, 2) >> {90}@z[3, 4], "M0 -0C1.57522 0.909453 3 -2.65027 3 -4"),
    (z[0]@{-30} >> 1.2 >> {90}@z[4], "M0 -0C1.5789 0.911581 4 1.23646 4 -0"),

    # --- 本丸：過去パスの点参照（タイムトラベル）を含む大作 ---
    (
        z[0]@{-30} >> 1.2 >> {90}@z[4] >> z[1.7: 130]@-0.9 >> {-30}@+z[-1.7: 130],
        "M0 -0C1.5789 0.911581 4 1.23646 4 -0C4 -1.0811 2.73734 -1.33797 2.42189 -0.614522C2.16892 -0.034356 2.90504 0.335811 3.51463 0.687754"
    ),

    (
		z[0]@{2j} >> {4j}@z[1, 1]@{5j} >> {3j}@z[2, 0],
        pyx.metapost.path.path(
            [
                beginknot(0, 0, curl=1),
                tensioncurve(),
                roughknot(1, 1, lcurl=4, rcurl=5),
                tensioncurve(),
                endknot(2, 0, curl=3)
            ]
        ).returnSVGdata()
    ),
    (
        z[0]@{-30} >> 1.2 >> {90}@z[4],

        ((z[0]@{-30} >> 1.2 >> z[4])@{90}).resolve()
    ),
    (
        z[0]@{-30} >> 1.2 >> {2j}@z[4],

        ((z[0]@{-30} >> 1.2 >> z[4])@{2j}).resolve()
    ),
]


# 💡 3. テスト実行関数
@pytest.mark.parametrize("expr, expected_svg", METASTENO_TEST_CASES)
def test_metasteno_svg_outputs(expr, expected_svg):
    # 点単体ケースのときだけ個別にstrで比較し、それ以外はSVGパス文字列で検証する
    if isinstance(expected_svg, str) and expected_svg.startswith("Point"):
        assert str(expr) == expected_svg
    else:
        # 最終出力されるSVGのd属性が1ミリの狂いもなく一致するかチェック！
        assert expr.resolve() == expected_svg

