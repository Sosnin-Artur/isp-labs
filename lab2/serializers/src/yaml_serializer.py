from serializers.src.base_serializer import BaseSerializer, BaseDeserializer
import yaml
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
        yaml.dump(tmp, open(file, 'w'))                       
        
    def dumps(self, obj):
        t = type(obj)                    
        tmp = io.StringIO()
        if (t in self.dispatch_table):                        
            f = self.dispatch_table.get(t)      
            yaml.dump(f(obj), tmp)
        else:            
            yaml.dump(obj, tmp)
        
        return tmp.getvalue()
                               

class Decoder(BaseDeserializer):
    def load(self, file):
        obj = yaml.load(open(file, 'r'))        
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
        obj = yaml.load(src)     
        if isinstance(obj, dict):                      
            tp = obj.get('type')
            if tp == 'func':                
                obj = self.dict_to_function(obj)
            elif tp == 'class':                
                obj = self.dict_to_class(obj)
            elif tp == "object":                
                obj = self.dict_to_object(obj)
        return obj