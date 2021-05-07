import pickle
import io
from serializers.src.base_serializer import BaseSerializer, BaseDeserializer

class Encoder(BaseSerializer):

    def dump(self, obj, file):
        with open(file, 'wb+') as fw:
            pickle.dump(obj, fw)

    def dumps(self, obj):
        t = type(obj)                    
        if t in self.dispatch_table:                        
            f = self.dispatch_table.get(t)      
            return pickle.dumps(f(obj))                               
        return pickle.dumps(obj)                       

class Decoder(BaseDeserializer):
    def load(self, file):
        with open(file, "rb+") as fr:
            obj = fr.read()
        return pickle.loads(obj)

    def loads(self, src):
        obj = pickle.loads(src)
        if isinstance(obj, dict):                      
            tp = obj.get('type')
            if tp == 'func':                
                obj = self.dict_to_function(obj)
            elif tp == 'class':                
                obj = self.dict_to_class(obj)
            elif tp == "object":                
                obj = self.dict_to_object(obj)
        return obj