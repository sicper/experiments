<<<<<<< HEAD
# -*- encoding: utf-8 -*-
import traceback
import re
from envs import global_env
from AST import AST
=======
#-*- encoding: utf-8 -*-
'''
Created on Jan 6, 2016

@author: jerry
'''
import traceback


def doeval(ele, env):
    if type(ele) == str:
        ele = AST([ele])

    # print env, ele
    cmd = ele.get_cmd()
    args = ele.get_args()
    if isinstance(cmd, AST):
        cur_env = Env(env.name + '_0', env)
        opt = doeval(cmd, cur_env)
    else :
        opt = env.search_symbol(cmd)
        if opt is None:
            print 'symbol %s not found!' % cmd
            return None
    rs = opt.apply(env, args)
    # print 'eval result: %s' % str(rs)
    return rs

import re
from AST import AST
from envs import global_env
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b



class Interpreter:
<<<<<<< HEAD
    # 语法分割符号
    SEP_PATTERN = r'\s+'

    def __init__(self):
        self.parse_stack = []
=======
    SEP_PATTERN = r'\s+'

    def __init__(self):
        pass
        self.parse_stack = []
        self.cur_env = global_env


#         print 'interpreter!'
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b

    def interpret(self, line):
        try:
            self.parse(line)
<<<<<<< HEAD
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    # 判断是否存在不合法字符,比如以数字开头,混杂字母
=======
        except Exception,e:
            traceback.print_exc()


    @staticmethod
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
    def is_valid_symbol(symbol):
        return True

    def build_AST(self):
        tmp_list = []
<<<<<<< HEAD
=======
#         print self.parse_stack
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
        while len(self.parse_stack) > 0:
            tmp_ele = self.parse_stack.pop()
            if tmp_ele == '(':
                tmp_list.reverse()
                ast = AST(tmp_list)
                return ast
            tmp_list.append(tmp_ele)
        raise Exception('Syntax Error!')

    def parse(self, line):
        # print 'parsing %s ...' % line
        line = line.replace('(', '( ')
        line = line.replace(')', ' )')
        char_list = re.split(Interpreter.SEP_PATTERN, line)
        # print char_list
        for ele in char_list:
            if not self.is_valid_symbol(ele):
                raise Exception('Syntax Error!')
            if ele == ')':
                ast = self.build_AST()
                self.parse_stack.append(ast)
<<<<<<< HEAD
            else:
                self.parse_stack.append(ele)
            if len(self.parse_stack) == 1 and self.parse_stack[0] != '(':
                cur = self.parse_stack[0]
                if not isinstance(cur, AST):
                    cur = AST([cur])
                rs = cur.eval(global_env)
                print 'Value: %s' % str(rs)
                self.parse_stack.pop()
        return None
=======
            else: self.parse_stack.append(ele)
            if len(self.parse_stack) == 1 and self.parse_stack[0] != '(':
                rs = doeval(self.parse_stack[0], self.cur_env)
                print 'Value: %s' % str(rs)
                self.parse_stack.pop()
        return None

from envs import Env

>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
