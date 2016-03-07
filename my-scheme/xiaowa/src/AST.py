#-*- encoding: utf-8 -*-
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

    def __repr__(self):
        show = '(cmd:%s\targs:[%s])' % (self.cmd, ','.join(str(item) for item in self.args))
        return show


    def get_cmd(self):
        return self.cmd

    def get_args(self):
        return self.args


