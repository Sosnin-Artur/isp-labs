from .error import *
from .nodes import *

import collections.abc, datetime, base64, binascii, re, sys, types

class BaseConstructor:

    yaml_Constructors = {}
    yaml_multi_Constructors = {}

    def __init__(self):
        self.constructed_objects = {}
        self.recursive_objects = {}
        self.state_generators = []
        self.deep_construct = False

    def check_data(self):
        return self.check_node()

    def check_state_key(self, key):        
        if self.get_state_keys_blacklist_regexp().match(key):
            raise ValueError(None, None,
                "blacklisted key '%s' in instance state found" % (key,), None)

    def get_data(self):
        if self.check_node():
            return self.construct_document(self.get_node())

    def get_single_data(self):
        node = self.get_single_node()
        if node is not None:
            return self.construct_document(node)
        return None

    def construct_document(self, node): 
        data = self.construct_object(node)
        while self.state_generators:
            state_generators = self.state_generators
            self.state_generators = []
            for generator in state_generators:
                for dummy in generator:
                    pass
        self.constructed_objects = {}
        self.recursive_objects = {}
        self.deep_construct = False
        return data

    def construct_object(self, node, deep=False): # pragma: no cover
        if node in self.constructed_objects:
            return self.constructed_objects[node]
        if deep:
            old_deep = self.deep_construct
            self.deep_construct = True
        if node in self.recursive_objects:
            raise ValueError(None, None,
                    "found unconstructable recursive node", node.start_mark)
        self.recursive_objects[node] = None
        Constructor = None
        tag_suffix = None
        if node.tag in self.yaml_Constructors:
            Constructor = self.yaml_Constructors[node.tag]
        else:
            for tag_prefix in self.yaml_multi_Constructors:
                if tag_prefix is not None and node.tag.startswith(tag_prefix):
                    tag_suffix = node.tag[len(tag_prefix):]
                    Constructor = self.yaml_multi_Constructors[tag_prefix]
                    break
            else:
                if None in self.yaml_multi_Constructors:
                    tag_suffix = node.tag
                    Constructor = self.yaml_multi_Constructors[None]
                elif None in self.yaml_Constructors:
                    Constructor = self.yaml_Constructors[None]
                elif isinstance(node, ScalarNode):
                    Constructor = self.__class__.construct_scalar
                elif isinstance(node, SequenceNode):
                    Constructor = self.__class__.construct_sequence
                elif isinstance(node, MappingNode):
                    Constructor = self.__class__.construct_mapping
        if tag_suffix is None:
            data = Constructor(self, node)
        else:
            data = Constructor(self, tag_suffix, node)
        if isinstance(data, types.GeneratorType):
            generator = data
            data = next(generator)
            if self.deep_construct:
                for dummy in generator:
                    pass
            else:
                self.state_generators.append(generator)
        self.constructed_objects[node] = data
        del self.recursive_objects[node]
        if deep:
            self.deep_construct = old_deep
        return data

    def construct_scalar(self, node): # pragma: no cover
        if not isinstance(node, ScalarNode):
            raise ValueError(None, None,
                    "expected a scalar node, but found %s" % node.id,
                    node.start_mark)
        return node.value

    def construct_sequence(self, node, deep=False): # pragma: no cover
        if not isinstance(node, SequenceNode):
            raise ValueError(None, None,
                    "expected a sequence node, but found %s" % node.id,
                    node.start_mark)
        return [self.construct_object(child, deep=deep)
                for child in node.value]

    def construct_mapping(self, node, deep=False): # pragma: no cover
        if not isinstance(node, MappingNode):
            raise ValueError(None, None,
                    "expected a mapping node, but found %s" % node.id,
                    node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.abc.Hashable):
                raise ValueError("while constructing a mapping", node.start_mark,
                        "found unhashable key", key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

    def construct_pairs(self, node, deep=False): # pragma: no cover
        if not isinstance(node, MappingNode):
            raise ValueError(None, None,
                    "expected a mapping node, but found %s" % node.id,
                    node.start_mark)
        pairs = []
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            value = self.construct_object(value_node, deep=deep)
            pairs.append((key, value))
        return pairs

    @classmethod
    def add_Constructor(cls, tag, Constructor):
        if not 'yaml_Constructors' in cls.__dict__:
            cls.yaml_Constructors = cls.yaml_Constructors.copy()
        cls.yaml_Constructors[tag] = Constructor    

class Constructor(BaseConstructor):

    def construct_scalar(self, node): # pragma: no cover
        if isinstance(node, MappingNode):
            for key_node, value_node in node.value:
                if key_node.tag == 'tag:yaml.org,2002:value':
                    return self.construct_scalar(value_node)
        return super().construct_scalar(node)
 
    def flatten_mapping(self, node): # pragma: no cover
        merge = []
        index = 0
        while index < len(node.value):
            key_node, value_node = node.value[index]
            if key_node.tag == 'tag:yaml.org,2002:merge':
                del node.value[index]
                if isinstance(value_node, MappingNode):
                    self.flatten_mapping(value_node)
                    merge.extend(value_node.value)
                elif isinstance(value_node, SequenceNode):
                    submerge = []
                    for subnode in value_node.value:
                        if not isinstance(subnode, MappingNode):
                            raise ValueError("while constructing a mapping",
                                    node.start_mark,
                                    "expected a mapping for merging, but found %s"
                                    % subnode.id, subnode.start_mark)
                        self.flatten_mapping(subnode)
                        submerge.append(subnode.value)
                    submerge.reverse()
                    for value in submerge:
                        merge.extend(value)
                else:
                    raise ValueError("while constructing a mapping", node.start_mark,
                            "expected a mapping or list of mappings for merging, but found %s"
                            % value_node.id, value_node.start_mark)
            elif key_node.tag == 'tag:yaml.org,2002:value':
                key_node.tag = 'tag:yaml.org,2002:str'
                index += 1
            else:
                index += 1
        if merge:
            node.value = merge + node.value    

    def construct_yaml_null(self, node):
        self.construct_scalar(node)
        return None

    bool_values = {
        'yes':      True,
        'no':       False,
        'true':     True,
        'false':    False,
        'on':       True,
        'off':      False,
    }

    def construct_yaml_bool(self, node): # pragma: no cover
        value = self.construct_scalar(node)
        return self.bool_values[value.lower()]

    def construct_yaml_int(self, node): # pragma: no cover
        value = self.construct_scalar(node)
        value = value.replace('_', '')
        sign = +1
        if value[0] == '-':
            sign = -1
        if value[0] in '+-':
            value = value[1:]
        if value == '0':
            return 0
        elif value.startswith('0b'):
            return sign*int(value[2:], 2)
        elif value.startswith('0x'):
            return sign*int(value[2:], 16)
        elif value[0] == '0':
            return sign*int(value, 8)
        elif ':' in value:
            digits = [int(part) for part in value.split(':')]
            digits.reverse()
            base = 1
            value = 0
            for digit in digits:
                value += digit*base
                base *= 60
            return sign*value
        else:
            return sign*int(value)

    inf_value = 1e300
    while inf_value != inf_value*inf_value:
        inf_value *= inf_value
    nan_value = -inf_value/inf_value   

    def construct_yaml_float(self, node): # pragma: no cover
        value = self.construct_scalar(node)
        value = value.replace('_', '').lower()
        sign = +1
        if value[0] == '-':
            sign = -1
        if value[0] in '+-':
            value = value[1:]
        if value == '.inf':
            return sign*self.inf_value
        elif value == '.nan':
            return self.nan_value
        elif ':' in value:
            digits = [float(part) for part in value.split(':')]
            digits.reverse()
            base = 1
            value = 0.0
            for digit in digits:
                value += digit*base
                base *= 60
            return sign*value
        else:
            return sign*float(value)

    def construct_yaml_str(self, node):
        return self.construct_scalar(node)

    def construct_yaml_seq(self, node):
        data = []
        yield data
        data.extend(self.construct_sequence(node))

    def construct_yaml_map(self, node):
        data = {}
        yield data
        value = self.construct_mapping(node)
        data.update(value)
    
    def construct_undefined(self, node):
        raise ValueError(None, None,
                "could not determine a Constructor for the tag %r" % node.tag,
                node.start_mark)
    
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

Constructor.add_Constructor(
        'tag:yaml.org,2002:null',
        Constructor.construct_yaml_null)

Constructor.add_Constructor(
        'tag:yaml.org,2002:bool',
        Constructor.construct_yaml_bool)

Constructor.add_Constructor(
        'tag:yaml.org,2002:int',
        Constructor.construct_yaml_int)

Constructor.add_Constructor(
        'tag:yaml.org,2002:float',
        Constructor.construct_yaml_float)

Constructor.add_Constructor(
        'tag:yaml.org,2002:str',
        Constructor.construct_yaml_str)

Constructor.add_Constructor(
        'tag:yaml.org,2002:seq',
        Constructor.construct_yaml_seq)

Constructor.add_Constructor(
        'tag:yaml.org,2002:map',
        Constructor.construct_yaml_map)

Constructor.add_Constructor(None,
        Constructor.construct_undefined)

Constructor.add_Constructor(
    'tag:yaml.org,2002:python/tuple',
    Constructor.construct_python_tuple)
