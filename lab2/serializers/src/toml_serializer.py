from serializers.src.base_serializer import BaseSerializer, BaseDeserializer
import toml
import types

class Encoder(BaseSerializer):
    
    def __init__(self):
        super().__init__()

    def dump(self, obj, file):
        dict_str = self.dumps(obj)
        with open(file ,'w') as fr:
            fr.write(dict_str)
        
    def dumps(self, obj):
        t = type(obj)                    
        if t in self.dispatch_table:                        
            f = self.dispatch_table.get(t)      
            return toml.dumps(f(self, obj))                               
        return toml.dumps(obj)                       
                

class Decoder(BaseDeserializer):
    
    def load(self, file):                
        with open(file, "r") as fr:
            return self.loads(fr.read())
        

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