from .instruments import *
import os.path

names = instruments.__dict__
DIR = os.path.dirname(__file__)


def get_model_lib():
    """
    Get the exist model information classified by type.
    :return: (dict) module information
    """
    mod_lib = {}
    for i in InstrumentType:
        mod_lib[i.name] = []
    for i in names:
        if 'Model' in i:
            model_obj = names[i]
            if not getattr(model_obj, 'model', None):
                pass
            else:
                model_str = model_obj.model
                if not isinstance(model_str, str):
                    model_str = '/'.join(model_obj.model)
                brand = model_obj.brand
                class_name = i
                params = model_obj.params
                detail = model_obj.detail
                type_str_list = [m.__name__[4:] for m in model_obj.mro() if
                                 ('Type' in m.__name__ and m.__name__ != 'TypeIns')]
                for type_str in type_str_list:
                    mod_lib[type_str].append({'model': model_str, 'brand': brand, 'class_name': class_name,
                                              'params': params, 'detail': detail})
    return mod_lib

