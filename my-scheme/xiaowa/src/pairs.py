import cmds
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return "[%s, %s]" % (self.first, self.second)

    def car(self):
        return self.first

    def cdr(self):
        return self.second


class MyList(Pair):
    def __init__(self, args):
        self.args = args
        self.first = args[0]
        if len(args) == 1:
            self.second = cmds.nil
        else:
            self.second = MyList(args[1:])

    def __repr__(self):
        eles = ','.join(str(item) for item in self.args)
        return "(%s)" % eles

