#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from interpreter import Interpreter
import readline
readline.parse_and_bind('tab: complete')


def interact():
    itp = Interpreter()
    while True:
        line = raw_input(">>")
        line = line.strip()
        itp.interpret(line)

if __name__ == '__main__':
    print "Welcome to the world of CHScheme!"
    interact()


test_cmds = '''
(* 2 3 4 5)
(def a 4)
(def b 5)
(if (> a b) a b)
(def max (lambda (a b) (if (> a b) a b)))
(def c (max a b))
c
((lambda (a b) (if (> a b) a b)) 3 4)
(cons 1 2)
(car (cons 1 2))
(cdr (cons 1 2))
(list)
(list 1 2)
(car (list 1 2))
(cdr (list 1 2))
(null? (cdr (list 1 2)))
(null? (cdr (cdr (list 1 2))))
(null? nil)
(cons 1 nil)
(list 1)
(def adder (lambda (x) (lambda (y) (+ x y))))
(def add2 (adder 2))
(add2 3)
(def myadd (lambda (x y) (+ x y)))
(myadd 3)
( (myadd 3) 4)
((lambda () (def tmp 1) tmp))
tmp
(def a1 1)
(def f1 (lambda () a1))
(def f2 (lambda () (def a1 2) (f1)))
(f2)
'''


