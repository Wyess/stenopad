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
        if self.current_token[0] == 'EOS':
            return [*ps]
        elif self.current_token[0] == 'LEFT_BRACE':
            ds = self.parse_direction_specifier()
            return [*ps, *ds]
        elif self.current_token[0] == 'CYCLE':
            # <path_join> is already parsed in path_subexpression
            self._consume('CYCLE')
            return [*ps, ('CYCLE', None)]

    def parse_path_subexpression(self):
        """<path_subexpression> := <path_knot>
                                 | <path_subexpression><path_join><path_knot>
        """
        res = []
        res.append(self.parse_path_knot())
        while True:
            if self.current_token[0] in ('DOUBLE_DASH', 'LEFT_BRACE', 'DOUBLE_DOT', 'TRIPLE_DOT'):
                res.append(self.parse_path_join())
                if self.current_token[0] == 'LEFT_PAREN':
                    res.append(self.parse_path_knot())
            else:
                break
        return res

    def parse_path_knot(self):
        self._consume("LEFT_PAREN")

        x = float(self.current_token[1])
        self._consume("NUMBER")

        self._consume("COMMA")

        y = float(self.current_token[1])
        self._consume("NUMBER")

        self._consume("RIGHT_PAREN")

        return ("KNOT", (x, y))

    def parse_tension(self):
        """
        <tension> := tension <numeric_primary>
                   | tension <numeric_primary> and <numeric_primary>
        """
        self._consume("TENSION")
        left_tension = float(self.current_token[1])
        self._consume("NUMBER")
        if self.current_token[0] == 'AND':
            self._consume('AND')
            right_tension = float(self.current_token[1])
            self._consume('NUMBER')
        else:
            right_tension = left_tension
        return ("TENSION", (left_tension, right_tension))

    def parse_controls(self):
        """
        <controls> := controls <pair_primary>
                    | controls <pair_primary> and <pair_primary>
        """
        self._consume('CONTROLS')
        self._consume('LEFT_PAREN')

        x0 = float(self.current_token[1])
        self._consume('NUMBER')

        self._consume('COMMA')

        y0 = float(self.current_token[1])
        self._consume('NUMBER')
        self._consume('RIGHT_PAREN')

        if self.current_token[0] == 'AND':
            self._consume('AND')

            self._consume('LEFT_PAREN')

            x1 = float(self.current_token[1])
            self._consume('NUMBER')

            self._consume('COMMA')

            y1 = float(self.current_token[1])
            self._consume('NUMBER')

            self._consume('RIGHT_PAREN')
        else:
            x1 = x0
            y1 = y0

        return ("CONTROLS", ((x0, y0), (x1, y1)))

    def parse_basic_path_join(self):
        """
        <basic_path_join> := ..
                           | ...
                           | .. <tension> ..
                           | .. <controls> ..
        """
        if self.current_token[0] == 'DOUBLE_DOT':
            self._consume('DOUBLE_DOT')
            if self.current_token[0] == 'TENSION':
                ret = ('BASIC_PATH_JOIN', self.parse_tension())
                self._consume('DOUBLE_DOT')
                return ret
            elif self.current_token[0] == 'CONTROLS':
                ret = ('BASIC_PATH_JOIN', self.parse_controls())
                self._consume('DOUBLE_DOT')
                return ret
            else:
                return ('BASIC_PATH_JOIN', 'CURVE')
        elif self.current_token[0] == 'TRIPLE_DOT':
            self._consume('TRIPLE_DOT')
            return ('BASIC_PATH_JOIN', 'CURVE_WITHOUT_INFLECTION')

    def parse_direction_specifier(self):
        """
        <direction_specifier> := empty
                               | { curl <numeric_expression> }
                               | { <pair_expression> }
                               | { <numeric_expression>, <numeric_expression> }
        """
        if self.current_token[0] == 'LEFT_BRACE':
            self._consume('LEFT_BRACE')
            if self.current_token[0] == 'CURL':
                self._consume('CURL')
                curl = float(self.current_token[1])
                self._consume('NUMBER')
                self._consume('RIGHT_BRACE')
                return ('DIRECTION_SPECIFIER', ('CURL', curl))
            else:
                x = float(self.current_token[1])
                self._consume('NUMBER')
                self._consume('COMMA')
                y = float(self.current_token[1])
                self._consume('NUMBER')
                self._consume('RIGHT_BRACE')
                return ('DIRECTION_SPECIFIER', ('PAIR', (x, y)))
        else:
            return ('DIRECTION_SPECIFIER', None)

    def parse_path_join(self):
        """
        <path_join> := --
                     | <direction_specifier><basic_path_join><direction_specifier>
        """
        if self.current_token[0] == 'DOUBLE_DASH':
            self._consume('DOUBLE_DASH')
            return ('PATH_JOIN', 'LINE')
        else:
            left_direction_specifier = self.parse_direction_specifier()
            if self.current_token[0] == 'EOS':
                return left_direction_specifier
            else:
                basic_path_join = self.parse_basic_path_join()
                right_direction_specifier = self.parse_direction_specifier()
                return ('PATH_JOIN', (left_direction_specifier, basic_path_join, right_direction_specifier))

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
