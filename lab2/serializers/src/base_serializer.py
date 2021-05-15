import inspect
import types

from abc import abstractmethod

class BaseSerializer:
    def __init__(self):
        self.dispatch_table = {        
            type : self.dumps_type,
            types.FunctionType : self.dumps_function,
            types.MethodType : self.dumps_function
        }

    @abstractmethod
    def dump(self, obj, file_path, convert=False):
        pass

    @abstractmethod
    def dumps(self, obj):
        pass

    def dumps_object(self, obj):        
        res = {'type': 'object', 'class': self.dumps_type(obj.__class__)}
        for attr in dir(obj):  
            if not attr.startswith('__'):
                attr_value = getattr(obj, attr)
                if callable(attr_value):                    
                    res[attr] = self.dumps_function(attr_value)                    
                elif ('__main__' in str(attr_value.__class__)): 
                    res[attr] = self.dumps_object(attr_value)
                else:
                    res[attr] = attr_value
        return res
    
    def dumps_type(self, obj):             
        res = {'type': 'class', 'class_name': str(obj)}
        for attr in dir(obj):            
            if attr == "__init__":
                attr_value = getattr(obj, attr)
                res[attr] = self.dumps_function(attr_value)       
            if not attr.startswith('__'):
                attr_value = getattr(obj, attr) 
                if 'type'  in str(attr_value.__class__): 
                    res[attr] = self.dumps_type(attr_value)
                if callable(attr_value):                    
                    res[attr] = self.dumps_function(attr_value)
                elif '__main__' in str(attr_value.__class__): 
                    res[attr] = self.dumps_object(attr_value)                    
                else:
                    res[attr] = attr_value
        return res

    def dumps_function(self, obj):     
        if hasattr(obj, '__code__'):            
            members = dir(obj.__code__)
            func_dict = {'type': 'func'}
            for item in members:
                if item.startswith('co_'):
                    func_dict[item] = getattr(obj.__code__, item)
            func_dict['co_code'] = list(func_dict["co_code"])
            func_dict['co_lnotab'] = list(func_dict["co_lnotab"])
                    
            return func_dict     
    
class BaseDeserializer:
    @abstractmethod
    def load(self, file_path, convert=False):
        pass

    @abstractmethod
    def loads(self, str_obj):
        pass
    
    def dict_to_function(self, dct):
        function_globals = globals()      
        code = types.CodeType(dct['co_argcount'],
                    dct['co_posonlyargcount'],
                    dct['co_kwonlyargcount'],
                    dct['co_nlocals'],
                    dct['co_stacksize'],
                    dct['co_flags'],
                    bytes(dct['co_code']),
                    tuple(dct['co_consts']),
                    tuple(dct['co_names']),
                    tuple(dct['co_varnames']),
                    dct['co_filename'],
                    dct['co_name'],
                    dct['co_firstlineno'],
                    bytes(dct['co_lnotab']),
                    tuple(dct['co_freevars']),
                    tuple(dct['co_cellvars']))

        temp = types.FunctionType(code, function_globals, dct['co_name'])
        name = dct['co_name']
        function_globals[name] = temp
        return types.FunctionType(code, function_globals, name)

    def dict_to_object(self, dct):                          
        klass = self.dict_to_class(dct['class'])        
        init_args = inspect.getargspec(klass).args        
        args = {}
        for arg in init_args:
            if arg in dct:
                args[arg] = dct[arg]        
        obj = klass(**args)                
        for attr in dct:            
            if hasattr(attr, 'startswith'):
                if not attr.startswith('__'):                                    
                    if isinstance(dct[attr], dict):
                        tmp = dct[attr].get('type')                                            
                        if tmp == 'func':                        
                            setattr(obj, attr, self.dict_to_function(dct[attr]))                        
                        elif tmp == 'object':
                            setattr(obj, attr, self.dict_to_object(dct[attr]))
                        elif tmp == 'class':
                            setattr(obj, attr, self.dict_to_class(dct[attr]))
                    else:
                        setattr(obj, attr, dct[attr])
            else:
                setattr(obj, attr, dct[attr])                        
        return obj

    def dict_to_class(self, dct):        
        args = {}                
        for attr in dct:                                      
            if isinstance(dct[attr], dict):                
                if dct[attr]['type'] == 'func':
                    args[attr] = self.dict_to_function(dct[attr])
                if dct[attr]['type'] == 'class':
                    args[attr] = self.dict_to_class(dct[attr])
                if dct[attr]['type'] == 'object':
                    args[attr] = self.dict_to_object(dct[attr])
            else:
                args[attr] = dct[attr]
        tmp = dct['class_name']        
        return type(tmp[tmp.find('.') + 1 : tmp.find("'>", 1)], (object,), args)
