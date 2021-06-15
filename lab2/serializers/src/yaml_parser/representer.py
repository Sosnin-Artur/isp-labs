from .nodes import *

class Representer:

    yaml_representers = {}
    yaml_multi_representers = {}

    def __init__(self, default_style=None, default_flow_style=False, sort_keys=True):
        self.default_style = default_style
        self.sort_keys = sort_keys
        self.default_flow_style = default_flow_style
        self.represented_objects = {}
        self.object_keeper = []
        self.alias_key = None

    def represent(self, data):
        node = self.represent_data(data)
        self.serialize(node)
        self.represented_objects = {}
        self.object_keeper = []
        self.alias_key = None

    def represent_data(self, data): # pragma: no cover
        if self.ignore_aliases(data):
            self.alias_key = None
        else:
            self.alias_key = id(data)
        if self.alias_key is not None:
            if self.alias_key in self.represented_objects:
                node = self.represented_objects[self.alias_key]                
                return node
            self.object_keeper.append(data)
        data_types = type(data).__mro__
        if data_types[0] in self.yaml_representers:
            node = self.yaml_representers[data_types[0]](self, data)
        else:
            for data_type in data_types:
                if data_type in self.yaml_multi_representers:
                    node = self.yaml_multi_representers[data_type](self, data)
                    break
            else:
                if None in self.yaml_multi_representers:
                    node = self.yaml_multi_representers[None](self, data)
                elif None in self.yaml_representers:
                    node = self.yaml_representers[None](self, data)
                else:
                    node = ScalarNode(None, str(data))
        return node

    @classmethod
    def add_representer(cls, data_type, representer):
        if not 'yaml_representers' in cls.__dict__:
            cls.yaml_representers = cls.yaml_representers.copy()
        cls.yaml_representers[data_type] = representer

    def represent_scalar(self, tag, value, style=None):
        if style is None:
            style = self.default_style
        node = ScalarNode(tag, value, style=style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        return node

    def represent_sequence(self, tag, sequence, flow_style=None): # pragma: no cover
        value = []
        node = SequenceNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        for item in sequence:
            node_item = self.represent_data(item)
            if not (isinstance(node_item, ScalarNode) and not node_item.style):
                best_style = False
            value.append(node_item)
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def represent_mapping(self, tag, mapping, flow_style=None):  # pragma: no cover
        value = []
        node = MappingNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        if hasattr(mapping, 'items'):
            mapping = list(mapping.items())
            if self.sort_keys:
                try:
                    mapping = sorted(mapping)
                except TypeError:
                    pass
        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            if not (isinstance(node_key, ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, ScalarNode) and not node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def ignore_aliases(self, data):
        if data is None:
            return True
        if isinstance(data, tuple) and data == ():
            return True
        if isinstance(data, (str, bytes, bool, int, float)):
            return True

    def represent_none(self, data):
        return self.represent_scalar('tag:yaml.org,2002:null', 'null')

    def represent_str(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data)    

    def represent_bool(self, data):
        if data:
            value = 'true'
        else:
            value = 'false'
        return self.represent_scalar('tag:yaml.org,2002:bool', value)

    def represent_int(self, data):
        return self.represent_scalar('tag:yaml.org,2002:int', str(data))

    inf_value = 1e300
    while repr(inf_value) != repr(inf_value*inf_value):
        inf_value *= inf_value

    def represent_float(self, data): # pragma: no cover
        if data != data or (data == 0.0 and data == 1.0):
            value = '.nan'
        elif data == self.inf_value:
            value = '.inf'
        elif data == -self.inf_value:
            value = '-.inf'
        else:
            value = repr(data).lower()            
            if '.' not in value and 'e' in value:
                value = value.replace('e', '.0e', 1)
        return self.represent_scalar('tag:yaml.org,2002:float', value)

    def represent_list(self, data):        
        return self.represent_sequence('tag:yaml.org,2002:seq', data)

    def represent_dict(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data)

    def represent_undefined(self, data):
        raise ValueError("cannot represent an object", data)

    def represent_name(self, data):
        name = '%s.%s' % (data.__module__, data.__name__)
        return self.represent_scalar('tag:yaml.org,2002:python/name:'+name, '')

Representer.add_representer(type(None),
        Representer.represent_none)

Representer.add_representer(str,
        Representer.represent_str)

Representer.add_representer(bool,
        Representer.represent_bool)

Representer.add_representer(int,
        Representer.represent_int)

Representer.add_representer(float,
        Representer.represent_float)

Representer.add_representer(list,
        Representer.represent_list)

Representer.add_representer(tuple,
        Representer.represent_list)

Representer.add_representer(dict,
        Representer.represent_dict)

Representer.add_representer(None,
        Representer.represent_undefined)

Representer.add_representer(type,
        Representer.represent_name)

