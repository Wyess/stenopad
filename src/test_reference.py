#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pytest
from reference import Reference as ref

class MatmulTest:
    def __init__(self, val):
        self.val = val

    def __matmul__(self, other):
        return self.val * other

    def __rmatmul__(self, other):
        return -self.val * other


REFERENCE_TEST_CASES = [
    (ref("foo"), "bar", {"foo": "bar"}),

    ### 1. 比較演算子 (Comparison Operators)
    ## __lt__(self, other) | < (未満) |
    #(ref("foo") < 1, True, {"foo": 0}),
    #(ref("foo") < 1, False, {"foo": 1}),
    #(ref("foo") < 1, False, {"foo": 2}),

    ## __le__(self, other) | <= (以下) |
    #(ref("foo") <= 1, True, {"foo": 0}),
    #(ref("foo") <= 1, True, {"foo": 1}),
    #(ref("foo") <= 1, False, {"foo": 2}),

    ## __eq__(self, other) | == (等価) |
    #(ref("foo") == 0, True, {"foo": 0}),
    #(ref("foo") == 1, False, {"foo": 0}),

    ## __ne__(self, other) | != (不等価) |
    #(ref("foo") != 0, True, {"foo": 1}),
    #(ref("foo") != 1, False, {"foo": 1}),

    ## __gt__(self, other) | > (超過) |
    #(ref("foo") > 1, False, {"foo": 0}),
    #(ref("foo") > 1, False, {"foo": 1}),
    #(ref("foo") > 1, True, {"foo": 2}),

    ## __ge__(self, other) | >= (以上) |
    #(ref("foo") >= 1, False, {"foo": 0}),
    #(ref("foo") >= 1, True, {"foo": 1}),
    #(ref("foo") >= 1, True, {"foo": 2}),

## 2. 算術演算子 (Arithmetic Operators)
    # __add__(self, other) | + (加算) |
    (ref("foo") + 1, 2, {"foo": 1}),
    (ref("foo") + ref("bar"), 3, {"foo": 1, "bar": 2}),

    # __radd__(self, other) | + (右辺からの加算)
    (1 + ref("foo"), 2, {"foo": 1}),

    # __sub__(self, other) | - (減算) |
    (ref("foo") - 1, 1, {"foo": 2}),

    # __rsub__(self, other) | - (右辺からの減算)
    (1 - ref("foo"), -1, {"foo": 2}),

    # __mul__(self, other) | * (乗算) |
    (ref("foo") * 2, 4, {"foo": 2}),

    # __rmul__(self, other) | * (右辺からの乗算)
    (2 * ref("foo"), 4, {"foo": 2}),

    # __matmul__(self, other) | @ (行列乗算) |
    (ref("foo") @ MatmulTest(2), -4, {"foo": 2}),

    # __rmatmul__(self, other) | @ (右辺からの行列乗算)
    (MatmulTest(2) @ ref("foo"), 4, {"foo": 2}),

    # __truediv__(self, other) | / (除算) |
    (ref("foo") / 2, 2.5, {"foo": 5}),

    # __rtruediv__(self, other) | / (右辺からの除算)
    (5 / ref("foo"), 2.5, {"foo": 2}),

    # __floordiv__(self, other) | // (切り捨て除算) |
    (ref("foo") // 2, 2, {"foo": 5}),

    # __rfloordiv__(self, other) | //
    (5 // ref("foo"), 2, {"foo": 2}),

    # __mod__(self, other) | % (剰余)
    (ref("foo") % 2, 1, {"foo": 5}),

    # __rmod__(self, other) | % (右辺からの剰余)
    (5 % ref("foo"), 1, {"foo": 2}),

    # __divmod__(self, other) | divmod() 組み込み関数 |
    (divmod(ref("foo"), 3), (1, 2), {"foo": 5}),

    # __rdivmod__(self, other) | divmod() (右辺から)
    (divmod(5, ref("foo")), (2, 1), {"foo": 2}),

    # __pow__(self, other[, modulo]) | **, pow()
    (ref("foo") ** 3, 8, {"foo": 2}),

    # __rpow__(self, other[, modulo]) | **
    #(2 ** ref("foo"), 8, {"foo": 3}),

## 4. 単項演算子 (Unary Operators)
    # __neg__(self) | - (符号反転・マイナス)
    (-ref("foo"), -1, {"foo": 1}),

    # __pos__(self) | + (プラス)
    (ref("foo"), 1, {"foo": 1}),

    # __abs__(self) | abs() (絶対値)
    (abs(ref("foo")), 1, {"foo": 1}),
    (abs(ref("foo")), 1, {"foo": -1}),

    # __invert__(self) | ~ (ビット反転)
    (~ref("foo"), -1, {"foo": 0}),

## 5. ビット演算子 (Bitwise Operators)
    # 左シフト <<
    # __lshift__
    (ref("foo") << 1, 6, {"foo": 3}),

    # __rlshift__
    (1 << ref("foo"), 4, {"foo": 2}),

    # 右シフト >>

    # __rshift__
    (ref("foo") >> 1, 3, {"foo": 6}),

    # __rrshift__
    (6 >> ref("foo"), 3, {"foo": 1}),

    # 論理積 &

    # __and__
    (ref("foo") & 0b0011, 0b0001, {"foo": 0b0101}),

    # __rand__
    (0b0011 & ref("foo"), 0b0001, {"foo": 0b0101}),

    # 排他的論理和 ^
    # __xor__
    (ref("foo") ^ 0b0011, 0b0110, {"foo": 0b0101}),

    # __rxor__
    (0b0011 ^ ref("foo"), 0b0110, {"foo": 0b0101}),

    # 論理和 |
    # __or__
    (0b0011 | ref("foo"), 0b0111, {"foo": 0b0101}),

    # __ror__
    (ref("foo") | 0b0011, 0b0111, {"foo": 0b0101}),

## 6. コンテナ・シーケンス演算子 (Container / Sequence Operators)
    # __len__(self) | len()
    # __getitem__(self, key) | obj[key]
    # __setitem__(self, key, value) | obj[key] = value
    # __delitem__(self, key) | del obj[key]
    # __contains__(self, item) | item in obj

## 7. 型変換・その他の演算子 (Type Conversion & Other Operators)
    # __bool__(self) | bool()
    # __int__(self) | int()
    # __float__(self) | float()
    # __complex__(self) | complex()
    # __index__(self) | スライスのインデックスや bin(), hex() での整数化 |
    # __round__(self[, n]) | round() (四捨五入・丸め) |
    # __trunc__(self) | math.trunc() (切り捨て) |
    # __floor__(self) | math.floor() (床関数) |
    # __ceil__(self) | math.ceil() (天井関数) |
]

@pytest.mark.parametrize("expr, exp, env", REFERENCE_TEST_CASES)
def test_reference_expressions(expr, exp, env):
    assert expr.resolve(env) == exp

