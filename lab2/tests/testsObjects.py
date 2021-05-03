class TestClass:    
    def __init__(self):
        self.num = 4
        self.rnum = -4
        self.numf = 4.5
        self.str = "fffff"        
        self.tr = True
        self.fl = True
        self.nn = None  
              
        self.infin = float('inf')
        self.rinfin = float('-inf')
        self.lst = ['1', '2', '3', '4'] 
        self.turp = (1, 2, 3, 4)
        self.dct = {'a' : self.lst}
                 
    kkk = "kkkkkkkkkkkkk"    
    
    def t(self):    
        return {'a': 'aaaa'}
    
    @classmethod
    def cl(cls):    
        return 'hello world'
    
    @staticmethod
    def st():    
        return 'hello world'

def test_func():
    return 'hello world'

def fact(i):
    if (i < 2):
        return 1
    return fact(i - 1) * i

x = lambda y: y * 2

lst = [3, 2, 1]
l = [lst, lst]
d = {'a': 'aaaa', 'b': 'bbbbb'}
dct = {'a': l, 'b': l, 'c': d, 'd': d}

