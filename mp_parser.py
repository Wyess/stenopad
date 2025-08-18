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
            if mo.lastgroup == 'SPACE':
                continue
            else:
                yield (mo.lastgroup, mo.group())

class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def _consume(self, token_type):
        print(f"_consume:{self.current_token=}")
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"{self.current_token} found where {token_type} expected")

    def parse(self):
        if self.current_token[0] == 'EOS':
            return []
        return self.parse_path_expression()

    def parse_path_expression(self):
        """<path_expression>
            := <path_subexpression>
             | <path_subexpression><direction_specifier>
             | <path_subexpression><path_join> cycle
        """
        ps = self.parse_path_subexpression()
        return [ps]

    def parse_path_subexpression(self):
        """<path_subexpression> := <path_knot>
                                 | <path_expression><path_join><path_knot>
        """
        return self.parse_path_knot()

    def parse_path_knot(self):
        self._consume("LEFT_PAREN")

        x = int(self.current_token[1])
        self._consume("NUMBER")

        self._consume("COMMA")

        y = int(self.current_token[1])
        self._consume("NUMBER")

        self._consume("RIGHT_PAREN")

        return ("KNOT", (x, y))

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
