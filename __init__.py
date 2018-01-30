from .instruments import *
import os.path
import json

names = instruments.__dict__
DIR = os.path.dirname(__file__)


def get_model_lib():
    mod_lib = {}
    for i in InstrumentType:
        mod_lib[i.name] = []
    for i in names:
        if 'Model' in i:
            type_obj = instruments.__dict__[i]
            if not hasattr(type_obj, 'model'):
                pass
            else:
                mod_str = type_obj.model
                if not isinstance(mod_str, str):
                    mod_str = '/'.join(type_obj.model)
                brand = type_obj.brand
                type_str_list = [m.__name__[4:] for m in type_obj.mro() if
                                 ('Type' in m.__name__ and m.__name__ != 'TypeIns')]
                for type_str in type_str_list:
                    mod_lib[type_str].append({'model': mod_str, 'brand': brand})
    return mod_lib


file0 = open(os.path.join(DIR, 'model_lib.json'), 'w')
file0.write(json.dumps(get_model_lib()))
file0.close()
