from serializers.src.base_serializer import BaseSerializer, BaseDeserializer
import toml

class Encoder(BaseSerializer):
    
    def __init__(self):
        super().__init__()

    def dump(self, obj, file):

        t = type(obj)                    
        if (t in self.dispatch_table):                        
            f = self.dispatch_table.get(t)      
            return (toml.dump(f(self, obj), open(file, 'w')))                        
        else:
            return (toml.dump(obj, open(file, 'w')))                       
        
    def dumps(self, obj):
        t = type(obj)                    
        if (t in self.dispatch_table):                        
            f = self.dispatch_table.get(t)      
            return (toml.dumps(f(self, obj)))                        
        else:
            return (toml.dumps(obj))                       

class Decoder(BaseDeserializer):
    
    def load(self, file):        
        obj = toml.load(open(file, 'r'))
        if isinstance(obj, dict):                      
            tp = obj.get('type')
            if tp == 'func':                
                obj = self.dict_to_function(obj)
            elif tp == 'class':                
                obj = self.dict_to_class(obj)
            elif tp == "object":                
                obj = self.dict_to_object(obj)
        return obj

    def loads(self, src):
        obj = toml.loads(src)
        if isinstance(obj, dict):                      
            tp = obj.get('type')
            if tp == 'func':                
                obj = self.dict_to_function(obj)
            elif tp == 'class':                
                obj = self.dict_to_class(obj)
            elif tp == "object":                
                obj = self.dict_to_object(obj)
        return obj