## 前言

网上 Scheme 方言很多，但是大多数都是照着书中的代码敲出来的，没有自己的思想在里面，其实很多时候我们都觉得自己把代码敲出来后就以为自己懂了，其实不然，没有反复的推敲、揣摩，是很难做到理解的。
不信的话，现在给你一个小时，把 [KMP 算法](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)实现一下。

所以在正式阅读第四章之前，我们换一种阅读的方式，用实践驱动，亲手去实现一个 Scheme 方言，不要求多全面，旨在运用之前学习到的编程模式，探索编程语言的奥妙。之后再来看这个第四章，我相信，效果会好很多。

## 必备知识

现在编程语言大致可以分为两种：

1. 编译型，该类型语言源代码经由编译器（compiler）转化为机器语言，再由机器运行机器码。像 C/C++ 即属于这个范畴。
2. 解释型，该类型语言不转化为最终的机器语言，而是由解释器（interpreter）逐行解释执行。Python、JavaScript 属于这个范畴。

显然，开发第一种语言的成本高，我们这里实现的是第二种。即

> 实现一个解释器，该解释器执行符合我们自定义语法规则的程序。

## 语法规则

### 表达式定义
为了简单起见，我们的语法规则不会太复杂，具体有下面几点：

1. 数据类型：数字、字符串、bool
2. 数据结构：pair、list、function
3. 关键字：`define`、`cons`、`car`、`cdr`、`lambda`、`eq?`、`empty?`、`true`、`false`、`if`、`cond`、`nil`

上面的数据结构和关键字的含义与 MIT Scheme 保持一致，这里不再赘述。

### 求值规则

1. 采用教材P10 结束的应用序
2. 采用教材3.2小节介绍的环境模型，并且采用静态作用域（static/lexical scope）

### 其他
如果觉得有余力，可以思考下面几点：

1. 如何让你的语言实现递归（可参考习题4.21）
2. 如何让你的语言成为动态作用域语言
3. 如何让你的程序更高效（可参考4.1.7小节）
4. 如何让你的语言在进行复合过程调用时采用正则序（可参考4.2小节）
5. ......


## 示例

```
>> (* 2 3 4 5)
120
>> (def a 4)
null
>> (def b 5)
null
>> (if (> a b) a b)
5
>> (def max (lambda (a b) (if (> a b) a b)))
null
>> (def c (max a b))
null
>> c
5
>> ((lambda (a b) (if (> a b) a b)) 3 4)  # immediately invoked function
4
>> (cons 1 2)
[1, 2]
>> (car (cons 1 2))
1
>> (cdr (cons 1 2))
2
>> (list) # identical to nil
nil   
>> (list 1 2)
(1, 2)
>> (car (list 1 2))
1
>> (cdr (list 1 2)) #  aware of the difference between this and (cdr (cons 1 2))
(2)
>> (empty? (cdr (list 1 2)))
false
>> (empty? (cdr (cdr (list 1 2))))
true
>> (empty? nil)
true
>> (cons 1 nil)
(1)
>> (list 1)  # identical to (cons 1 nil)
(1)

# closure demo
>> (def adder (lambda (x) (lambda (y) (+ x y))))
null
>> (def add2 (adder 2))
null
>> (add2 3)
5
# currying demo
>> (def myadd (lambda (x y) (+ x y)))
null
>> (myadd 3)
Function :
        Args : [y]
        Body : [( + x y ) ]
>> ( (myadd 3) 4)
7
>> ((lambda () (def a 1) a))
1
>> a    # variable a isn't in global scope
Error token: a

# static scope demo
>> (def a1 1)
>> (def f1 (lambda () a1))
>> (def f2 (lambda () (def a1 2) (f1)))
>> (f2)
1
```
之上的 demo 也是我们的测试用例。

## 要求

- 可以用自己擅长的任意一门编程语言实现
- 时间限定在两周。（2016/01/06---2016/01/20）周二、周五讨论遇到的问题
