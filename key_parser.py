import re
from typing import NamedTuple

def parse(text, table, char):
    return Parser(text, table, char).parse()

class Parser:
    def __init__(self, text, table, char):
        self.table = table
        self.char = char
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        return self.parse_logical_or() 

    def consume(self, _type):
        tok = self.current_token
        if tok.type != _type:
            raise SyntaxError
        self.current_token = self.lexer.get_next_token()
        return tok

    def parse_logical_or(self):
        res = self.parse_logical_and()
        while self.current_token.type == 'LOGICAL_OR':
            self.consume('LOGICAL_OR')
            if self.parse_logical_and():
                res = True
        return res

    def parse_logical_and(self):
        res = self.parse_unary_expression()
        while self.current_token.type == 'LOGICAL_AND':
            self.consume('LOGICAL_AND')
            if not self.parse_unary_expression():
                res = False
        return res

    def parse_class_expression(self):
        self.consume('CLASS_REFERENCE')

        id_ = self.current_token.value
        self.consume('ID')

        self.consume('LEFT_BRACKET')

        offset = int(self.current_token.value)
        self.consume('INDEX')

        self.consume('RIGHT_BRACKET')

        char = self.char
        try:
            while offset < 0:
                char = char.prev
                offset += 1
            while offset > 0:
                char = char.next
                offset -= 1
            if id_ in ('sos', 'eos'):
                return char is None
            else:
                return char.name in self.table[id_]
        except (AttributeError, KeyError) as e:
            return False

    def parse_unary_expression(self):
        if self.current_token.type == 'NEGATION':
            self.consume('NEGATION')
            return not self.parse_class_expression()
        elif self.current_token.type == 'LEFT_PAREN':
            self.consume('LEFT_PAREN')
            res = self.parse()
            self.consume('RIGHT_PAREN')
            return res
        elif self.current_token.type == 'DEFAULT':
            self.consume('DEFAULT')
            return True
        else:
            return self.parse_class_expression()

class Token(NamedTuple):
    type: str
    value: str

class Lexer:
    token_spec = [
        ('WHITESPACE', r'\s+'),
        ('DEFAULT', r'default'),
        ('ID', r'[_a-zA-Z][_a-zA-Z\d]*'),
        ('INDEX', r'-?\d+'),
        ('LEFT_PAREN', r'\('),
        ('RIGHT_PAREN', r'\)'),
        ('LEFT_BRACKET', r'\['),
        ('RIGHT_BRACKET', r'\]'),
        ('CLASS_REFERENCE', r'\$'),
        ('ATTRIBUTE_REFERENCE', r'@'),
        ('NEGATION', r'!'),
        ('LOGICAL_AND', r'&'),
        ('LOGICAL_OR', r'\|'),
        ('ERROR', r'.')
    ]
    tok_regex = '|'.join(f"(?P<{kind}>{regex})" for kind, regex in token_spec)

    def __init__(self, text):
        self.token_iter = self.create_token_iterator(text)

    def create_token_iterator(self, text):
        for mo in re.finditer(Lexer.tok_regex, text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'WHITESPACE':
                continue
            yield Token(kind, value)

    def get_next_token(self):
        return next(self.token_iter, Token('EOS', 'EOS'))
