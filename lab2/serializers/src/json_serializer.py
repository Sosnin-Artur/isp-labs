import re
import dis
import types
from serializers.src.base_serializer import BaseSerializer, BaseDeserializer
from io import StringIO

nested_types = [list, tuple, dict]

class Encoder(BaseSerializer):            
    def __init__(self, indent=None):
        super().__init__()
        if not indent:
            indent = 0
        self.indent = indent                
        self.dispatch_table[int] = self.dumps_numb
        self.dispatch_table[float]= self.dumps_numb
        self.dispatch_table[str] = self.dumps_string
        self.dispatch_table[type(None)] = self.dumps_None
        self.dispatch_table[bool] = self.dumps_bool
        self.dispatch_table[list] = self.dumps_list
        self.dispatch_table[tuple] = self.dumps_list
        self.dispatch_table[dict] = self.dumps_dict    
        # if dumps_default is not None:
        #     self.dumps_default = dumps_default

    def dumps(self, obj, nesting_lvl = 0):        
        t = type(obj)                    
        if (t in self.dispatch_table):
            f = self.dispatch_table.get(t)      
            if (t in (types.FunctionType, types.MethodType, type)):                                                 
                return (self.dumps_dict(f(obj)))            
            return f(obj)      
        else:
            return self.dumps_dict(self.dumps_object(obj))        
    
    def dump(self, obj, file):  
        s = self.dumps(obj)
        if isinstance(file ,str):
            file = open(file, 'w')                      
        file.write(s)
        
    def dumps_numb(self, obj):
        if (obj != obj):
            return "NaN"
        if (obj == float('inf')):
            return "Infinity"
        if (obj == -float('inf')):
            return "-Infinity"        
        return str(obj)

    def dumps_None(self, obj):
        return "null"    

    def dumps_string(self, obj):
        return '"' + obj + '"'

    def dumps_bool(self, obj):
        return str(obj).lower()

    def dumps_list(self, lst, nesting_lvl = 0):
        if not lst:
            return '[]'
        res = '['
        if self.indent is not None:
            nesting_lvl += 1            
        else:            
            newline_indent = None 

        first = True       
        for value in lst:
            if first:
                first = False
                newline_indent = '\n' + ' ' * self.indent * nesting_lvl
            else :
                newline_indent = ',\n' + ' ' * self.indent * nesting_lvl
            res += newline_indent
            t = type(value)
            f = self.dispatch_table.get(t)
            if (t in nested_types):
                res += f(value, nesting_lvl)
            elif t in [types.FunctionType, types.MethodType, type]:                
                res += self.dumps(value, nesting_lvl)
            elif f is None:
                res += self.dumps(value, nesting_lvl)
            else:
                res += f(value)
        if newline_indent is not None:
            nesting_lvl -= 1
            res += ',\n' + ' ' * self.indent * nesting_lvl
        return res +  ']'

    def dumps_dict(self, obj, nesting_lvl = 0):
        if not obj:
            return '{}'            
        res  = '{'
        if self.indent is not None:
            nesting_lvl += 1
        else:
            newline_indent = None
        first = True
        for key, value in obj.items():
            if first:
                first = False
                newline_indent = '\n' + ' ' * self.indent * nesting_lvl
            else :
                newline_indent = ',\n' + ' ' * self.indent * nesting_lvl
            tk = type(key)
            fk = self.dispatch_table.get(tk)
            tv = type(value)
            fv = self.dispatch_table.get(tv)            

            res += newline_indent    
            tmp = fk(key)
            if (tk is str):            
                res += tmp + ': '
            elif (tk in nested_types):
                raise TypeError("unhandled type for key")
            else:
                res += '"' + tmp + '": '
            if (tv in nested_types):
                res += fv(value, nesting_lvl)
            elif tv in [types.FunctionType, types.MethodType, type]:                
                res += self.dumps(value, nesting_lvl)
            elif fv is None:
                res += self.dumps(value, nesting_lvl)
            else:
                res += fv(value)
        if newline_indent is not None:
            nesting_lvl -= 1
            res += '\n' + ' ' * self.indent * nesting_lvl
        return res +  '}'
    

NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?')

class Scanner:
    def __init__(self, default_scan = None):
        self.default_scan = default_scan

    def scan(self, string, idx):  
        nextchar = string[idx]
        
        if nextchar == '"':
            return self.parse_string(string, idx + 1)
        elif nextchar == '{':
            return self.parse_object((string, idx + 1))
        elif nextchar == '[':
            return self.parse_array((string, idx + 1))
        elif string[idx:idx + 4] == 'null':
            return None, idx + 4
        elif string[idx:idx + 4] == 'true':
            return True, idx + 4
        elif string[idx:idx + 5] == 'false':
            return False, idx + 5
        
        match_number = NUMBER_RE.match
        m = match_number(string, idx)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = float(integer + (frac or '') + (exp or ''))
            else:
                res = int(integer)
            return res, m.end()
        elif string[idx:idx + 3] == 'NaN':
            return float('nan'), idx + 3
        elif string[idx:idx + 8] == 'Infinity':
            return float('inf'), idx + 8
        elif string[idx:idx + 9] == '-Infinity':
            return float('-inf'), idx + 9
        else:
            raise StopIteration(idx)                            
        
    def parse_string(self, s, end):        
        prev = end  
        end = s[prev:].find('"') + prev                                        
        return s[prev : end], end + 1
        
    # Use speedup if available    

    WHITESPACE = re.compile(r'[ \t\n\r]*')
    WHITESPACE_STR = ' \t\n\r'

    def parse_object(self, s_and_end, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
        s, end = s_and_end
        pairs = []
        pairs_append = pairs.append        
        nextchar = s[end:end + 1]        
        if nextchar != '"':
            if nextchar in _ws:
                end = _w(s, end).end()
                nextchar = s[end:end + 1]
               
        end += 1
        while True:            
            key, end = self.parse_string(s, end)            
            if s[end:end + 1] != ':':
                end = _w(s, end).end()                
            end += 1

            try:
                if s[end] in _ws:
                    end += 1
                    if s[end] in _ws:
                        end = _w(s, end + 1).end()
            except IndexError:
                pass
            
            value, end = self.scan(s, end)
            pairs_append((key, value))            
            nextchar = s[end]
            if nextchar in _ws:
                end = _w(s, end + 1).end()
                nextchar = s[end]            
            end += 1

            if nextchar == '}':
                break                            
            end = _w(s, end).end()
            nextchar = s[end:end + 1]
            end += 1            
        
        pairs = dict(pairs)        
        return pairs, end

    def parse_array(self, s_and_end, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
        s, end = s_and_end
        values = []
        nextchar = s[end:end + 1]
        if nextchar in _ws:
            end = _w(s, end + 1).end()
            nextchar = s[end:end + 1]        
        if nextchar == ']':
            return values, end + 1
        _append = values.append
        while True:
            nextchar = s[end:end + 1]
            if nextchar == ']':
                return values, end + 1            
            value, end = self.scan(s, end)
            _append(value)
            nextchar = s[end:end + 1]
            if nextchar in _ws:
                end = _w(s, end + 1).end()
                nextchar = s[end:end + 1]
            end += 1
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    end = _w(s, end + 1).end()            

        return values, end

class Decoder(BaseDeserializer):                
    def loads(self, dict_str):                
        obj = Scanner().scan(dict_str, 0)[0]    
        if isinstance(obj, dict):                      
            tp = obj.get('type')
            if tp == 'func':                
                obj = self.dict_to_function(obj)
            elif tp == 'class':                
                obj = self.dict_to_class(obj)
            elif tp == "object":                
                obj = self.dict_to_object(obj)
        return obj
    
    def load(self, file):
        if isinstance(file, str):
            with open(file, "r") as fr:
                return self.loads(fr.read())
        else:
           return self.loads(file.read())

# class TestClass:
#     kkk = "kkkkkkkkkkkkk"
#     def __init__(self):
#         self.num = 4
#         self.numf = 4.5
#         self.str = "fffff"        
#         self.b = True        
#         self.lst = [1, 2, 3, 4]         
#         self.dct = {1 : self.lst}
#         # self.dd = {'a': self.d, 'b': self.d}
    
#     def t(self):    
#         return nnn

# def t():        
#     return nnn

# nnn = 5
# g = TestClass()
# i = 5
# f = 5.5
# st = "[3, 4, 5]"
# l = [4 , 3]
# k = (5, 6)
# d = {"a" : l, "b" : "ggggggggggg"}
# dd = {'a': d, 'b': d}
# x = lambda y : y * y
# # print(inspect.getmembers(g.t))
# # print(inspect.getmembers(t))
# # print(Encoder(indent=4).dumps(g))
# g.num = 5
# data = ((Encoder(indent=4).dumps(g)))
# di = Decoder().loads(data)
# # print(di.b)
