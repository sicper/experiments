# -*- encoding: utf-8 -*-
import traceback
import re
from envs import global_env
from AST import AST



class Interpreter:
    # 语法分割符号
    SEP_PATTERN = r'\s+'

    def __init__(self):
        self.parse_stack = []

    def interpret(self, line):
        try:
            self.parse(line)
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    # 判断是否存在不合法字符,比如以数字开头,混杂字母
    def is_valid_symbol(symbol):
        return True

    def build_AST(self):
        tmp_list = []
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
