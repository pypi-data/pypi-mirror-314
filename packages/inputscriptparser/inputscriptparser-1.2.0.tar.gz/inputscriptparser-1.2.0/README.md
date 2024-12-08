# inputscriptparser

A parser for script-style input data.

"script-style" means assembling input data (the internal representation of the input data) by executing commands one at a time.
A close example is the Dockerfile.

## Install

inputscriptparser can be installed with pip:

    $ pip install inputscriptparser

Or add it to your project using the package manager:

    $ poetry add inputscriptparser

## Usage

This parser converts text input into a list of tuples consisting of commands and their arguments.

```Python
from inputscriptparser import Parser

input_data = '''CMD1 "example data"
CMD2 1 2 3
NO-ARG-CMD
'''

parser = Parser()
script = parser.parse(input_data)
```

In the example above, the `script` parsing the input would be:

```Python
[
    ('CMD1', ['example data']),
    ('CMD2', [1.0, 2.0, 3.0]),
    ('NO-ARG-CMD', [])
]
```

The interpreter that executes each command must be provided by the user.

## Grammar

The grammar is as follows

1. A `script` representing the entire input data consists of one or more `statement`.
2. A `statement` consists of a `command` and zero or more `arg`.
3. The `command` and each `arg` are separated by whitespace characters.
4. The `command` always begins at the beginning of a line. If a line begins with a space character, it is considered a continuation of the previous line.
5. Lines from `//` to the end of the line are ignored as comments. Blank lines and lines containing only whitespace are also ignored.

### Command

The `command` consists of Latin uppercase letters, digits, and `-`; and must begin with a uppercase letter.

### Argument values

The following types can be used as argument values:

- number
- string
- boolean
- keyword

Numbers do not distinguish between integers and real numbers. All numbers are real numbers.

Strings are enclosed in `"` (double quotation marks).

Boolean can be lowercase words that can be considered true or false.

- `true` / `false`
- `yes` / `no`
- `on` / `off`

Keywords consist of Latin uppercase letters and digits and always begin with an uppercase letter.
They are similar to commands, but are distinguished by the fact that they do not appear at the beginning of a line.

## Interpreter

The `inputscriptparser.Interpreter` class is the base class of the interpreters.
To implement an interpreter, extend `inputscriptparser.Interpreter` and implement methods corresponding to each command. The correspondence between commands and methods is bound by the following rules:

1. Convert uppercase to lowercase
2. Replace `-` with `_`
3. Prefix `_` to the beginning

In short, the `NO-ARG-CMD` command is tied to the `_no_arg_cmd` method.

The input data interpreter for the first example is as follows:

```Python
from inputscriptparser import Interpreter

class ExampleInterpreter(Interpreter):
    def _cmd1(self, args):
        self.state['CMD1'] = args[0]

    def _cmd2(self, args):
        self.state['CMD2'] = sum(args)

    def _no_arg_cmd(self, args):
        self.state['NO-ARG-CMD'] = 'This is a no-argument-command.'
```

Create an instance of the interpreter and call the `run` method.

```Python
interpreter = ExampleInterpreter({})
state = interpreter.run(script)
for k, v in state.items():
    print(f'{k} = {v}')
```

The argument of the constructor is an object (here an empty `dict`) to store the state. It can be accessed from inside the interpreter as `self.state`.
The state object after executing the `script` is obtained as the return value of the `run` method.
And the following output is obtained:

```
CMD1 = example data
CMD2 = 6.0
NO-ARG-CMD = This is a no-argument-command.
```

## CLI tool `ispshow`

The CLI tool `ispshow` parses input data and displays the results (`command`s and `arg`s) in an easy-to-read format.

    $ ispshow examples/inputscript.dat

## License

MIT license.
