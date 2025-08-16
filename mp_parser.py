#!/usr/bin/env python3

import pyx
import re

class Lexer:
    token_spec = (
        ("LEFT_PAREN", r"\("),
        ("RIGHT_PAREN", r"\)"),
        ("LEFT_BRACE", r"\{"),
        ("RIGHT_BRACE", r"\}"),
        ("COMMA", r","),
        ("TRIPLE_DOT", r"[.]{3}"),
        ("DOUBLE_DOT", r"[.]{2}"),
        ("DOUBLE_DASH", r"-{2}"),
        ("NUMBER", r"[-+]?(0|[1-9]\d*)(?:[.]\d+)?"),
        ("DIR", r"dir"),
        ("TENSION", r"tension"),
        ("CURL", r"curl"),
        ("CONTROLS", r"controls"),
        ("CYCLE", r"cycle"),
        ("AND", r"and"),
        ("SPACE", r"\s+"),
        ("ERROR", r".")
    )

    def __init__(self, text):
        pattern = re.compile("|".join([
            f"(?P<{kind}>{regex})" for kind, regex in Lexer.token_spec
        ]))
        self.iter = self.create_token_iterator(pattern, text)

    def get_next_token(self):
        return next(self.iter, ("EOS", "EOS"))

    def create_token_iterator(self, pattern, text):
        for mo in re.finditer(pattern, text):
            yield (mo.lastgroup, mo.group())

class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)

    def parse(self):
        return self.parse_path_expression()

    def parse_path_expression(self):
        """<path_expression> := <path_subexpression>
                              | <path_subexpression><direction_specifier>
                              | <path_subexpression><path_join> cycle"""
        return self.parse_path_subexpression()

    def parse_path_subexpression(self):
        return parse_path_kot()

    def parse_path_knot(self):
        pass

    """
    <path_expression> := <path_subexpression>
                       | <path_subexpression><direction_specifier>
                       | <path_subexpression><path_join> cycle
    <path_subexpression> := <path_knot>
                          | <path_expression><path_join><path_knot>
    <path_join> := --
                 | <direction_specifier><basic_path_join><direction_specifier>
    <direction_specifier> := empty
                           | { curl <numeric_expression> }
                           | { <pair_expression> }
                           | { <numeric_expression>, <numeric_expression> }
    <basic_path_join> := ..
                       | ...
                       | .. <tension> ..
                       | .. <controls> ..
    <tension> := tension <numeric_primary>
               | tension <numeric_primary> and <numeric_primary>
    <controls> := controls <pair_primary>
                | controls <pair_primary> and <pair_primary>

    <path_knot> := <pair_primary>
    <pair_primary> := (<numeric_primary>, <numeric_primary>)
    <pair_expression> :=
    <numeric_primary> :=
    <numeric_expression> :=
    """
