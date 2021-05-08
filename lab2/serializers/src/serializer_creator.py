from serializers.src.json_serializer import Encoder as json_encoder, Decoder as json_decoder
from serializers.src.toml_serializer import Encoder as toml_encoder, Decoder as toml_decoder
from serializers.src.yaml_serializer import Encoder as yaml_encoder, Decoder as yaml_decoder

from serializers.src.pickle_serializer import Encoder as pickle_encoder
from serializers.src.pickle_serializer import Decoder as pickle_decoder

class Creator(object):
    @staticmethod
    def create_serializer(serialize_type, indent=4):
        if serialize_type == 'yaml':
            return yaml_encoder(indent)
        if serialize_type == 'pickle':
            return pickle_encoder()
        if serialize_type == 'toml':
            return toml_encoder()
        if serialize_type == 'json':
            return json_encoder(indent)
    @staticmethod
    def create_deserializer(serialize_type):
        if serialize_type == 'yaml':
            return yaml_decoder()
        if serialize_type == 'pickle':
            return pickle_decoder()
        if serialize_type == 'toml':
            return toml_decoder()
        if serialize_type == 'json':
            return json_decoder()

