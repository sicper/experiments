#-*- encoding: utf-8 -*-

class AST:
    def __init__(self, elements):
        if isinstance(elements, AST):
            return self.copyAST(elements)
        if isinstance(elements, str):
            elements = [elements]
        self.elements = elements
        self.cmd = self.get_cmd()
        self.args = self.get_args()

    def copyAST(self, ast):
        self.elements = ast.elements
        self.cmd = ast.cmd
        self.args = ast.args

    def __repr__(self):
        show = '(cmd:%s\targs:[%s])' % (self.cmd, ','.join(str(item) for item in self.args))
        return show

    def get_cmd(self):
        if len(self.elements) > 0:
            return self.elements[0]
        return None

    def get_args(self):
        if len(self.elements) > 0:
            return self.elements[1:]
        return None

    def eval(self, env):
        if isinstance(self.cmd, AST):
            cur_env = env.create_child(0)
            opt = self.cmd.eval(cur_env)
        else:
            opt = env.search_symbol(self.cmd)
            if opt is None:
                print 'symbol %s not found!' % self.cmd
                return None
        rs = opt.apply(env, self.args)
        return rs





