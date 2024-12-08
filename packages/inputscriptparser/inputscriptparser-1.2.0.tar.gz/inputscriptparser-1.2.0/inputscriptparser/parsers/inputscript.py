from lark import Lark
from lark.exceptions import UnexpectedInput
from lark.visitors import Transformer
from inputscriptparser.common import Keyword, flatten
from os import path

here = path.dirname(path.abspath(__file__))
grammer_file = path.join(here, '../../grammers/inputscript.lark')
with open(grammer_file) as f:
    SCRIPT_GRAMMER = f.read()


class Parser():
    def __init__(self):
        self.parser = Lark(SCRIPT_GRAMMER, start='script')

    def parse(self, input_data):
        try:
            tree = self.parser.parse(input_data)
        except UnexpectedInput as e:
            context = e.get_context(input_data)
            print(f'Syntax error:  line = {e.line}  column = {e.column}\n')
            print(context)
            exit(1)

        script = ScriptTransformer().transform(tree)
        return script


class ScriptTransformer(Transformer):
    def script(self, tokens):
        return list(tokens)

    def statement(self, tokens):
        (cmd, args) = tokens[0]
        if len(tokens) > 1:
            args.extend(tokens[1:])
        return (cmd, flatten(args))

    def line(self, tokens):
        if len(tokens) == 1:
            (cmd,) = tokens
            args = []
        else:
            (cmd, args) = tokens
        return (cmd, args)

    def continued(self, tokens):
        (args,) = tokens
        return args

    def command(self, tokens):
        (cmd,) = tokens
        return str(cmd)

    def arglist(self, tokens):
        return list(tokens)

    def arg(self, tokens):
        (a,) = tokens
        return a

    def number(self, tokens):
        (num,) = tokens
        return float(num)

    def string(self, tokens):
        (s,) = tokens
        return s.strip('"')

    def keyword(self, tokens):
        (kw,) = tokens
        return Keyword(kw)

    def boolean(self, tokens):
        (b,) = tokens
        return b

    def true(self, tokens):
        return True

    def false(self, tokens):
        return False
