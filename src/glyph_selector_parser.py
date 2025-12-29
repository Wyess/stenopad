#!/usr/bin/env python3

#from lark import Lark, Transformer
from glyph_selector_lark import Lark_StandAlone, Transformer

class GlyphSelectorTransformer(Transformer):
    _op = {
        '&': lambda x, y: x and y,
        '.': lambda x, y: x and y,
        '-': lambda x, y: x and not y,
        '|': lambda x, y: x or y,
        '!': lambda x: not x,
    }

    def __init__(self, char, visit_tokens=True):
        super().__init__(visit_tokens)
        self.char = char

    def start(self, args):
        return args[0]

    def glyph_selector(self, args):
        return args[0]

    def term(self, args):
        tag, idx, _ = args
        char = self.char
        if idx > 0:
            for i in range(idx):
                if char is None:
                    return False
                char = char.next
            if char is None:
                return tag =='eos'
        elif idx < 0:
            for i in range(-idx):
                if char is None:
                    return False
                char = char.prev
            if char is None:
                return tag == 'sos'
        return tag in char.tag

    def paren_expr(self, args):
        return args[0]

    def default(self, args):
        return True

    def primary(self, args):
        try:
            op, value = args
            return op(value)
        except ValueError:
            return args[0]

    def secondary(self, args):
        lhs = args[0]
        rest = zip(args[1::2], args[2::2])
        for op, rhs in rest:
            lhs = op(lhs, rhs)
        return lhs

    def tertiary(self, args):
        lhs = args[0]
        rest = zip(args[1::2], args[2::2])
        for op, rhs in rest:
            lhs = op(lhs, rhs)
        return lhs

    def unary_op(self, args):
        op = args[0]
        return self._op[op]

    def primary_binop(self, args):
        op = args[0]
        return self._op[op]

    def secondary_binop(self, args):
        op = args[0]
        return self._op[op]

    def tag(self, args):
        return args[0].value

    def index(self, args):
        return int(args[0])

#parser = Lark.open(
#    "glyph_selector.lark",
#    parser="lalr",
#)
parser = Lark_StandAlone()

def parse_glyph_selector(code, char):
    tree = parser.parse(code)
    return GlyphSelectorTransformer(char).transform(tree)

if __name__ == "__main__":
    to_make_tree = False
    sdict = {
        'ya': {
            'tag': {
                'ya',
                '@head_ner',
            },
        },
        'shihenki': {
            'tag': {
                'sahenki',
                '@head_swr',
            },
        },
        'ka': {
            'tag': {
                'ka',
                '@head_e',
            },
        },
    }
    chars = [
        Character('ya', sdict),
        Character('shihenki', sdict),
        Character('ka', sdict),
    ]

    code = "ya[-1].@head_e[1]"
    if to_make_tree:
        parser = Lark.open("glyph_selector.lark", parser="lalr")
        tree = parser.parse(code)
        print(tree.pretty())
        res = GlyphSelectorTransformer(chars, 1).transform(tree)
        print(res)
    else:
        parser = Lark.open(
            "glyph_selector.lark",
            transformer=GlyphSelectorTransformer(chars, 1),
            parser="lalr",
        )
        
        res = parser.parse(code)
        print(res)

    print(code)
