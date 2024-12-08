from inputscriptparser import __version__, Parser as SParser
from inputscriptparser.parsers.labeledscript import Parser as LParser
from argparse import ArgumentParser


def main():
    args = parse_arguments()

    if args.parser == 'script':
        parser = SParser()
        print_script = print_input_script
    elif args.parser == 'labeled':
        parser = LParser()
        print_script = print_labeled_script

    with open(args.input_file, 'r') as f:
        input_data = f.read()
    script = parser.parse(input_data)
    print_script(script)


def parse_arguments():
    parser = ArgumentParser(
        description='Example for Input Script Parser'
    )
    parser.add_argument(
        'input_file',
        metavar='INPUT_FILE',
        help='input script file'
    )
    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'v{__version__}',
        help='show version and exit'
    )
    parser.add_argument(
        '-p', '--parser',
        action='store',
        choices=[ 'script', 'labeled' ],
        default='script',
        help='specify parser. default to `script`'
    )
    args = parser.parse_args()
    return args


def print_input_script(script):
    print('SCRIPT')
    for (cmd, args) in script:
        print('  COMMAND: ' + cmd)
        print('     ARGS: ' + repr(args))


def print_labeled_script(script):
    print('SCRIPT')
    for (cmd, args, substmnts) in script:
        print('  COMMAND: ' + cmd)
        print('    ARGS:  ' + repr(args))
        for (subcmd, subargs) in substmnts:
            print('    SUBCOMMAND: ' + subcmd)
            print('      ARGS:     ' + repr(subargs))
