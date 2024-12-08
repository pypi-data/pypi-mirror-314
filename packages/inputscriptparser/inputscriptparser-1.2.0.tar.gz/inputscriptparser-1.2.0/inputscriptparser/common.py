class Keyword():
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return f'<Keyword {self.val}>'

    def __eq__(self, other):
        return self.val == other.val


def flatten(lis):
    result = []
    for elem in lis:
        if isinstance(elem, list):
            result += flatten(elem)
        else:
            result.append(elem)
    return result
