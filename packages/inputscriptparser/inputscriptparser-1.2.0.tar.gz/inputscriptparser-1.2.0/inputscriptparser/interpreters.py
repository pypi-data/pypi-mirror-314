class Interpreter():
    def __init__(self, state):
        self.state = state

    def exec(self, cmd, args):
        try:
            f_name = '_' + cmd.lower().replace('-', '_')
            f = getattr(self, f_name)
            f(args)
        except AttributeError:
            self.command_mnissing(cmd)

    def result(self):
        return self.state

    def run(self, statements):
        for (cmd, args) in statements:
            self.exec(cmd, args)
        return self.state

    def command_mnissing(self, cmd):
        print(f'Command not found: {cmd}')
        exit(1)
