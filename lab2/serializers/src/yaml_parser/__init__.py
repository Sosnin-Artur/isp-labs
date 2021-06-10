
from .error import *

from .tokens import *
from .events import *
from .nodes import *

from .loader import *
from .dumper import *

import io

def load(stream):        
    loader = Loader(stream)    
    return loader.get_single_data()    

def dump_all(documents, stream=None):    
    getvalue = None    
    dumper = Dumper(stream)
    try:
        dumper.open()
        for data in documents:
            dumper.represent(data)
        dumper.close()
    finally:
        dumper.states = []
        dumper.state = None
    if getvalue:
        return getvalue()

def dump(data, stream=None):    
    return dump_all([data], stream)