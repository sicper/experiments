#-*- encoding: utf-8 -*-
<<<<<<< HEAD

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
=======
'''
Created on Jan 7, 2016

@author: jerry
'''

class AST:
    def __init__(self, elements):
        pass
        # if len(elements) == 0:
        #     print 'not enough eles!'
        self.cmd, self.args = '', []
        self.elements = elements
        if len (elements) > 0:
            self.cmd = elements[0]
            self.args = elements[1:]
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b

    def __repr__(self):
        show = '(cmd:%s\targs:[%s])' % (self.cmd, ','.join(str(item) for item in self.args))
        return show

<<<<<<< HEAD
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



=======

    def get_cmd(self):
        return self.cmd

    def get_args(self):
        return self.args
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b


