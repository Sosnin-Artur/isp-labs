from serializers.src.base_serializer import BaseSerializer, BaseDeserializer
import serializers.src.toml_parser.parser as toml_parser
import serializers.src.toml_parser.writer as toml_writer
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
            return toml_writer.dumps(f(self, obj))                               
        return toml_writer.dumps(obj)                       
                

class Decoder(BaseDeserializer):
    
    def load(self, file):                
        with open(file, "r") as fr:
            return self.loads(fr.read())
        
    def loads(self, src):
        obj = toml_parser.loads(src)
        if isinstance(obj, dict):                      
            tp = obj.get('type')
            if tp == 'func':                
                obj = self.dict_to_function(obj)
            elif tp == 'class':                
                obj = self.dict_to_class(obj)
            elif tp == "object":                
                obj = self.dict_to_object(obj)
        return obj