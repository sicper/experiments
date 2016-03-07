<<<<<<< HEAD
from cmds import Value
from cmds import true, false, nil
from cmds import add_keyword
from cmds import sub_keyword
from cmds import mul_keyword
from cmds import dvd_keyword
from cmds import and_keyword
from cmds import or_keyword
from cmds import not_keyword
from cmds import greater_keyword
from cmds import smaller_keyword
from cmds import equal_keyword
from cmds import cons_keyword
from cmds import car_keyword
from cmds import cdr_keyword
from cmds import list_keyword
from cmds import if_keyword
from cmds import isnull_keyword
from cmds import def_keyword
from cmds import lambda_keyword
=======
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b



class Env:
    def __init__(self, name, father):
        self.name = name
        self.symbols = {}
        self.father = father
        # print self.name

    def add_symbol(self, symbol, cmd):
        self.symbols[symbol] = cmd

<<<<<<< HEAD
    def create_child(self, idx=0):
        return Env(self.name + '' + str(idx), self)

=======
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
    def __repr__(self):
        return self.name

    #search for cmd
    def search_symbol(self, symbol):
        # is the symbol a number?
<<<<<<< HEAD
        rs = get_num(symbol)
        if rs is not None:
            return rs
=======
        if get_num(symbol) is not None:
            return get_num(symbol)
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
        # is the symbol a string?
        if symbol.startswith("'"):
            return Value(symbol[1:])
        if symbol == 'true':
            return true
        if symbol == 'false':
            return false
        if symbol == 'nil':
            return nil
        # search the symbol in current env
        if self.symbols.has_key(symbol):
            return self.symbols.get(symbol)
        if self.father is None:
            return None
        return self.father.search_symbol(symbol)

<<<<<<< HEAD
=======
from cmds import Value
from cmds import true, false, nil
from cmds import add_keyword
from cmds import sub_keyword
from cmds import mul_keyword
from cmds import dvd_keyword
from cmds import and_keyword
from cmds import or_keyword
from cmds import not_keyword
from cmds import greater_keyword
from cmds import smaller_keyword
from cmds import equal_keyword
from cmds import cons_keyword
from cmds import car_keyword
from cmds import cdr_keyword
from cmds import list_keyword
from cmds import if_keyword
from cmds import isnull_keyword
from cmds import def_keyword
from cmds import lambda_keyword
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b



def get_num(symbol):
<<<<<<< HEAD
    # print 'get num'
=======
>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
    try:
        rs = int(symbol)
        return Value(rs)
    except ValueError:
        pass
        # print 'not int'
<<<<<<< HEAD
=======

>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
    try:
        rs = float(symbol)
        return Value(rs)
    except ValueError:
        # print 'not float'
        pass
    return None


<<<<<<< HEAD
=======








>>>>>>> 63c794f4207f12f3ff2da08852d4cdec6092784b
#define global env
global_env = Env('E0', None)
global_env.add_symbol('+', add_keyword)
global_env.add_symbol('-', sub_keyword)
global_env.add_symbol('*', mul_keyword)
global_env.add_symbol('/', dvd_keyword)
global_env.add_symbol('and', and_keyword)
global_env.add_symbol('or', or_keyword)
global_env.add_symbol('not', not_keyword)
global_env.add_symbol('>', greater_keyword)
global_env.add_symbol('<', smaller_keyword)
global_env.add_symbol('=', equal_keyword)
global_env.add_symbol('cons', cons_keyword)
global_env.add_symbol('car', car_keyword)
global_env.add_symbol('cdr', cdr_keyword)
global_env.add_symbol('list', list_keyword)
global_env.add_symbol('if', if_keyword)
global_env.add_symbol('null?', isnull_keyword)
global_env.add_symbol('def', def_keyword)
global_env.add_symbol('lambda', lambda_keyword)






