from serializers.src.base_serializer import BaseSerializer, BaseDeserializer
from serializers.src.yaml_parser import load, dump
import io

class Encoder(BaseSerializer):
    
    def __init__(self, indent=0):
        super().__init__()

    def dump(self, obj, file):
        t = type(obj)                    
        tmp = obj
        if (t in self.dispatch_table):                        
            f = self.dispatch_table.get(t)      
            tmp = f(obj)
        
        if isinstance(file ,str):                                  
            dump(tmp, open(file, 'w'))                       
        else:
            dump(tmp, file)                       
        
    def dumps(self, obj):                      
        tmp = io.StringIO()
        self.dump(obj, tmp)        
        return tmp.getvalue()
                               

class Decoder(BaseDeserializer):
    def load(self, file):        
        return load(file)

    def loads(self, src):               
        obj = self.load(src)     
        if isinstance(obj, dict):                      
            tp = obj.get('type')
            if tp == 'func':                
                obj = self.dict_to_function(obj)
            elif tp == 'class':                
                obj = self.dict_to_class(obj)
            elif tp == "object":                
                obj = self.dict_to_object(obj)
        return obj