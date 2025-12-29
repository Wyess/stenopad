# !/usr/bin/env python3

#from lark import Lark, Transformer
from text_grammer_lark import Lark_StandAlone, Transformer

class InputTextTransformer(Transformer):
    def __init__(self, dict_, visit_tokens=True):
        super().__init__(visit_tokens)
        self.dict = dict_
        self.dict.setdefault('\n', ['Newline'])
        self.sep = self.dict.get('SEPARATOR', '\x1F')

    def ensure_list(self, arg):
        if isinstance(arg, list):
            return arg
        else:
            return [arg]

    def start(self, args):
        return args[0]

    def text(self, args):
        ret = []
        buf = []
        for arg in args:
            if arg[0] in ('Space', 'Newline'):
                buf.extend(arg)
            else:
                ret.extend(buf)
                ret.extend(arg)
                buf = []
        # Leave trailing spaces in buf
        return ret

    def WORD(self, tok):
        if schars := self.dict.get(tok, None):
            return self.ensure_list(schars)

        if self.sep in tok:
            words = filter(None, tok.split(self.sep))
            schars = [schar for word in words for schar in self.WORD(word)]
            return schars

        schars = [schar for char in tok for schar in self.ensure_list(self.dict.get(char, ['Null']))]
        if any((schar != 'Null' for schar in schars)):
            return schars
        else:
            return ['Null']

    def WHITESPACE(self, tok):
        return self.ensure_list(self.dict.get(tok, ['Space']))

#parser = Lark.open(
#    "text_grammer.lark",
#    parser="lalr",
#)
parser = Lark_StandAlone()

def parse_text(text, wdict):
    tree = parser.parse(text)
    return InputTextTransformer(wdict).transform(tree)
if __name__ == "__main__":
    text = """
    あ-い  あい　うえ う-え お
    """
    wdict = {
        'あ': ['A'],
        'い': ['I'],
        'うえ': ['Ue'],
        'う': ['U'],
        'え': ['E'],
    }
    res = parse_text(text, wdict)
    print(res)

