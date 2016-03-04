


# CHScheme
CHScheme is short for ChenHao Scheme.
## 运行
```git clone https://github.com/sicper/experiments.git
   cd experiments/my-scheme/xiaowa/src
   python ./CHScheme.py```
## 语言边界
CHScheme 可以运行四则运算、实现简单逻辑分支、函数定义等功能。
具体语法定义见2016_01_04_my-own-scheme.md
## 实现方法
1、用符号栈存储输入的符号，当括号闭合时构建一颗语法树AST（Abstract Syntax Tree）。AST拥有eval（）方法。
2、AST 用列表保存去除了括号的语法元素（字符、保留字、另一个AST）。在当前环境下查找列表的第一个元素，构成一个Cmd对象。剩余的元素构建成AST对象的列表。
3、Cmd父类有apply方法，它有四种子类：

     - Value:基础类型的封装（包括字符、数字、nil、true、false）
     - KeyWord:关键字（包括＋,-,*,/,null?,list,lambda,cons,car,cdr,if,def,and,or）
     - Symbol:符号（环境中定义的变量或者函数）
     - Func:匿名函数（lambda生成，包括一个参数名列表以及多个AST构成的函数体）
4、当符号栈只剩下一个AST时，调用AST的eval方法。
5、AST的eval方法会调用cmd的apply方法，根据不同类型的cmd，对当前AST的参数AST进行eval，并对参数的eval值进行运算。返回一个Value或None或一个Func
6、如此eval、apply循环。。。
## 经验与改进

 - 所有的返回值都是Value类型或者Func类型，不可和python的True、False、None混用
 - eval 和 apply无法完全分开。比如and操作，无法在apply之前知道需要eval多少个参数
 - list理论上是cons的语法糖衣，但是list的显示方式和pair的显示方式是不一样的，实现解析器可能要用不同的数据结构存储
 - 代码在不断优化中，争取解决python import混乱问题，会尽快加上注释，努力符合 python best practise😊
