#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import copy
import pairs
from AST import AST

def add(env, args):
    rs = 0
    idx = 0
    for item in args:
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env)
        rs += tmp.get_value()
        idx += 1
    return rs


def sub(env, args):
    idx = 0
    cur_env = env.create_child(idx)
    rs = AST(args[0]).eval(cur_env).get_value()
    idx += 1
    for item in args[1:]:
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env)
        rs -= tmp.get_value()
        idx += 1
    return rs


def mul(env, args):
    rs = 1
    idx = 0
    for item in args:
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env)
        rs *= tmp.get_value()
        idx += 1
    return rs


def dvd(env, args):
    idx = 0
    cur_env = env.create_child(idx)
    rs = AST(args[0]).eval(cur_env)
    idx += 1
    for item in args[1:]:
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env).get_value()
        rs /= tmp
        idx += 1
    return rs


def my_and(env, args):
    idx = 0
    for item in args:
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env)
        if not tmp.get_value():
            return false
        idx += 1
    return true


def my_or(env, args):
    idx = 0
    for item in args:
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env)
        if tmp.get_value():
            return true
        idx += 1
    return false


def my_not(env, args):
    idx = 0
    cur_env = env.create_child(idx)
    rs = AST(args[0]).eval(cur_env)
    #是否正确?
    if rs.get_value(): return false
    return true


def compare(env, args, func):
    idx = 0
    cur_env = env.create_child(idx)
    pre = AST(args[0]).eval(cur_env)
    idx += 1
    while idx < len(args):
        item = args[idx]
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env)
        if not func(float(pre.get_value()), float(tmp.get_value())):
            return false
        pre = tmp
        idx += 1
    return true


def greater(env, args):
    return compare(env, args, lambda x, y: x > y)

def smaller(env, args):
    return compare(env, args, lambda x, y: x < y)

def equal(env, args):
    return compare(env, args, lambda x, y: x == y)

def cons(env, args):
    cur_env = env.create_child(0)
    first = AST(args[0]).eval(cur_env)
    cur_env = env.create_child(1)
    second = AST(args[1]).eval(cur_env)
    return pairs.Pair(first, second)

def car(env, args):
    cur_env = env.create_child(0)
    p = AST(args[0]).eval(cur_env)
    if not isinstance(p, pairs.Pair):
        raise Exception('car should be used to a pair!')
    return p.car()

def cdr(env, args):
    cur_env = env.create_child(0)
    p = AST(args[0]).eval(cur_env)
    if not isinstance(p, pairs.Pair):
        raise Exception('cdr should be used to a pair!')
    return p.cdr()

def my_list(env, args):
    if len(args) == 0:
        return nil
    rs_args = []
    for idx, item in enumerate(args):
        cur_env = env.create_child(idx)
        tmp = AST(item).eval(cur_env)
        rs_args.append(tmp)
    return pairs.MyList(rs_args)

def my_if(env, args):
    cur_env = env.create_child(0)
    cond = AST(args[0]).eval(cur_env)
    cur_env = env.create_child(1)
    if cond == true:
        rs = AST(args[1]).eval(cur_env)
    else:
        rs = AST(args[2]).eval(cur_env)
    return rs


def is_null(env, args):
    cur_env = env.create_child(0)
    rs = AST(args[0]).eval(cur_env)
    if rs == nil:
        return true
    return false

def define(env, args):
    symbol = args[0]
    cur_env = env.create_child(0)
    target = AST(args[1]).eval(cur_env)
    env.add_symbol(symbol, target)
    # print "add symbol %s as %s" % (symbol, target)

def my_lambda(env, args):
    arg = args[0]
    body = args[1:]
    func = Func(arg.elements, body, env)
    return func

class Cmd:
    arg_min_num_dict = {add: 2,
                        sub: 2,
                        mul: 2,
                        dvd: 2,
                        my_and: 2,
                        my_or: 2,
                        my_not: 1,
                        greater: 2,
                        smaller: 2,
                        equal: 2,
                        cons: 2,
                        car: 1,
                        cdr: 1,
                        my_if: 3,
                        is_null: 1,
                        define: 2,
                        my_lambda: 2
                        }

    arg_max_num_dict = {my_not: 1,
                        cons: 2,
                        car: 1,
                        cdr: 1,
                        my_if: 3,
                        is_null: 1,
                        define: 2
                        }

    def __init__(self, name):
        self.name = name

    def apply(self, env, args):
        print 'applying %s' % self.name
        return '\t'.join(args)



class KeyWord(Cmd):
    def __init__(self, name, func):
        Cmd.__init__(self, name)
        # print 'key words: %s' % self.name
        self.exec_func = func

    def apply(self, env, args):
        if Cmd.arg_min_num_dict.get(self.exec_func, 0) > len(args):
            raise Exception('not enough args!')
        if Cmd.arg_max_num_dict.get(self.exec_func, len(args)) < len(args):
            raise Exception('too many args!')
        # print 'applying keyword:%s' % self.name
        return self.exec_func(env, args)


class Func(Cmd):
    def __init__(self, args, body, env):
        self.args = args
        self.body = body
        self.env = env

    def apply(self, env, args):
        if len(args) > len(self.args):
            raise Exception('too many args!')
        cur_env = self.env.create_child(0)
        for symbol, target in zip(self.args, args):
            define(cur_env, [symbol, target])
        if len(args) < len(self.args):
            new_args = copy.copy(self.args[len(args):])
            new_func = Func(new_args, self.body, cur_env)
            return new_func
        rs = nil
        for tmp_body in self.body:
            rs = AST(tmp_body).eval(cur_env)
        return rs

    def __repr__(self):
        show = '''anonymous function\nparams:(%s)\nbody:%s''' % (','.join(self.args), self.body)
        return show

# base element of CHScheme
class Value(Cmd):
    def __init__(self, v, show=None):
        self.value = v
        self.show = str(v)
        if show is not None:
            self.show = show

    def get_value(self):
        return self.value

    def apply(self, env, args):
        return self

    def __repr__(self):
        return str(self.show)





#export KeyWords
add_keyword = KeyWord('add', add)
sub_keyword = KeyWord('sub', sub)
mul_keyword = KeyWord('mul', mul)
dvd_keyword = KeyWord('dvd', dvd)
and_keyword = KeyWord('and', my_and)
or_keyword = KeyWord('or', my_or)
not_keyword = KeyWord('not', my_not)
greater_keyword = KeyWord('greater', greater)
smaller_keyword = KeyWord('smaller', smaller)
equal_keyword = KeyWord('equal', equal)
cons_keyword = KeyWord('cons', cons)
car_keyword = KeyWord('car', car)
cdr_keyword = KeyWord('cdr', cdr)
list_keyword = KeyWord('list', my_list)
if_keyword = KeyWord('if', my_if)
isnull_keyword = KeyWord('null?', is_null)
def_keyword = KeyWord('def', define)
lambda_keyword = KeyWord('lambda', my_lambda)



#export Values
false = Value(False, 'false')
true = Value(True, 'true')
nil = Value(None, 'nil')








