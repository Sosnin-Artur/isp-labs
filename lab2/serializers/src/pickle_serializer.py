import pickle
import io
from serializers.src.base_serializer import BaseSerializer, BaseDeserializer

class Encoder(BaseSerializer):

    def dump(self, obj, file):
        with open(file, 'wb+') as fw:
            pickle.dump(obj, fw)

    def dumps(self, obj):
        return pickle.dumps(obj)

class Decoder(BaseDeserializer):
    def load(self, file):
        with open(file, "rb+") as fr:
            obj = fr.read()
        return pickle.loads(obj)

    def loads(self, src):
        return pickle.loads(src)