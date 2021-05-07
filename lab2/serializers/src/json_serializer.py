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
                        

    def dumps(self, obj, nesting_lvl=0):                
        t = type(obj)                    
        if t in self.dispatch_table:
            f = self.dispatch_table.get(t)      
            if t in (types.FunctionType, types.MethodType, type):                                                 
                return self.dumps_dict(f(obj))            
            return f(obj)      
        else:
            return self.dumps_dict(self.dumps_object(obj))        
    
    def dump(self, obj, file):  
        dict_str = self.dumps(obj)
        if isinstance(file ,str):
            file = open(file, 'w')                      
        file.write(dict_str)
        
    def dumps_numb(self, obj):
        if obj != obj:
            return "NaN"
        if obj == float('inf'):
            return "Infinity"
        if obj == -float('inf'):
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
            if t in nested_types:
                res += f(value, nesting_lvl)
            elif t in [types.FunctionType, types.MethodType, type]:                
                res += self.dumps(value, nesting_lvl)
            elif f is None:
                res += self.dumps(value, nesting_lvl)
            else:
                res += f(value)
        if newline_indent is not None:
            nesting_lvl -= 1
            res += ' \n' + ' ' * self.indent * nesting_lvl
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
            if tv in nested_types:
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
WHITESPACE = re.compile(r'[ \t\n\r]*')
WHITESPACE_STR = ' \t\n\r'

class Scanner:
    def __init__(self, default_scan = None):
        self.default_scan = default_scan

    def scan(self, dict_str, ind):  
        nextchar = dict_str[ind]         
        if nextchar == '"':
            return self.parse_string(dict_str, ind + 1)
        elif nextchar == '{':
            return self.parse_object(dict_str, ind + 1)
        elif nextchar == '[':
            return self.parse_array(dict_str, ind + 1)
        elif dict_str[ind:ind + 4] == 'null':
            return None, ind + 4
        elif dict_str[ind:ind + 4] == 'true':
            return True, ind + 4
        elif dict_str[ind:ind + 5] == 'false':
            return False, ind + 5
        
        match_number = NUMBER_RE.match
        m = match_number(dict_str, ind)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = float(integer + (frac or '') + (exp or ''))
            else:
                res = int(integer)
            return res, m.end()
        elif dict_str[ind:ind + 3] == 'NaN':
            return float('nan'), ind + 3
        elif dict_str[ind:ind + 8] == 'Infinity':
            return float('inf'), ind + 8
        elif dict_str[ind:ind + 9] == '-Infinity':
            return float('-inf'), ind + 9
        else:
            raise StopIteration(ind)                            
        
    def parse_string(self, dict_str, ind):        
        prev = ind  
        ind = dict_str[prev:].find('"') + prev                                        
        return dict_str[prev : ind], ind + 1                

    def parse_object(self, dict_str, ind, _w=WHITESPACE.match, _ws=WHITESPACE_STR):        
        pairs = []
        pairs_append = pairs.append        
        nextchar = dict_str[ind]        
        if nextchar != '"':
            if nextchar in _ws:
                ind = _w(dict_str, ind).end()
                nextchar = dict_str[ind]
               
        ind += 1
        while True:            
            key, ind = self.parse_string(dict_str, ind)            
            if dict_str[ind] != ':':
                ind = _w(dict_str, ind).end()                
            ind += 1

            try:
                if dict_str[ind] in _ws:
                    ind += 1
                    if dict_str[ind] in _ws:
                        ind = _w(dict_str, ind + 1).end()
            except IndexError:
                raise IndexError(ind)
            
            value, ind = self.scan(dict_str, ind)
            pairs_append((key, value))            
            nextchar = dict_str[ind]
            if nextchar in _ws:
                ind = _w(dict_str, ind + 1).end()
                nextchar = dict_str[ind]            
            ind += 1

            if nextchar == '}':
                break                            
            ind = _w(dict_str, ind).end()
            nextchar = dict_str[ind]
            ind += 1            
        
        pairs = dict(pairs)        
        return pairs, ind

    def parse_array(self, dict_str, ind, _w=WHITESPACE.match, _ws=WHITESPACE_STR):        
        values = []
        nextchar = dict_str[ind]
        if nextchar in _ws:
            ind = _w(dict_str, ind + 1).end()
            nextchar = dict_str[ind]        
        if nextchar == ']':
            return values, ind + 1
        _append = values.append
        while True:            
            value, ind = self.scan(dict_str, ind)            
            _append(value)
            nextchar = dict_str[ind]
            if nextchar in _ws:
                ind = _w(dict_str, ind + 1).end()
                nextchar = dict_str[ind]
            ind += 1
            if nextchar == ']':
                break            
            if dict_str[ind] in _ws:
                ind += 1
                if dict_str[ind] in _ws:
                    ind = _w(dict_str, ind + 1).end()
        

        return values, ind

class Decoder(BaseDeserializer):                
    def __init__(self, loads_default=None):
        self.loads_default = loads_default

    def loads(self, dict_str):     
        if self.loads_default:
            return self.loads_default(dict_str)

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
