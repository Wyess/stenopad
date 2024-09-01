#!/usr/bin/env python3

import regex
from typing import NamedTuple

class Token(NamedTuple):
    type: str
    value: str

class Lexer:
    tr = str.maketrans('（）', '()')
    token_spec = [
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("HIRAGANA_SEQ", r"\p{Block=Hiragana}[ぁぃぅぇぉゃゅょ]?ー?ん?"),
        ("KATAKANA_SEQ", r"(\p{Block=Katakana}(?<!・))+"),
        ("KANJI_SEQ", r"\p{Script=Han}+"),
        ("SEP", r"[・|｜]"),
        ("CAPITAL_SEQ", r"[A-Z]+"),
        ("ELSE", r".")
    ]
    token_regex = regex.compile("|".join([rf"(?P<{kind}>{re})" for kind, re in token_spec]), regex.DOTALL)

    def __init__(self, text):
        self.tokenizer = self.create_tokenizer(text)

    def create_tokenizer(self, text):
        for mo in regex.finditer(Lexer.token_regex, text.translate(Lexer.tr)):
            yield Token(mo.lastgroup, mo.group())

    def get_next_token(self):
        return next(self.tokenizer, Token("EOS", "EOS"))


class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def consume(self, _type=None):
        tok = self.current_token
        if _type is not None and tok.type != _type:
            raise SyntaxError
        self.current_token = self.lexer.get_next_token()
        return tok

    def parse(self):
        words = []
        while self.current_token.type != "EOS":
            if self.current_token.type == 'LPAREN':
                self.consume('LPAREN')
                words.extend(self.parse_inside_paren())
                self.consume()
            elif self.current_token.type == 'SEP':
                self.consume('SEP')
            elif self.current_token.type == 'RPAREN':
                self.consume('RPAREN')
            else:
                words.append(self.current_token.value)
                self.consume()
        return words


    def parse_inside_paren(self):
        words = []
        while self.current_token.type not in ("RPAREN", "EOS"):
            if self.current_token.type != 'LPAREN':
                words.append(self.current_token.value)
            self.consume()
        if self.current_token.type == "RPAREN":
            return ["".join(words)]
        else:
            return words

def parse(text):
    return Parser(text).parse()
