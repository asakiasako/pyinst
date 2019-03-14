import visa
from .base_models._VisaInstrument import rm
from .constants import InstrumentType
from . import models


__all__ = ['get_resource_manager', 'close_resource_manager', 'list_resources', 'list_resources_info', 'resource_info', 'get_instrument_lib']


def get_resource_manager():
    """
    Get the visa.ResourceManager instance that is used globally by py-inst.
    """
    return rm


def close_resource_manager():
    """
    Close the resource manager session.
    """
    rm.close()


def list_resources():
    """
    Returns a tuple of all connected devices.
    Return type: tuple[str]
    """
    return rm.list_resources()


def list_resources_info():
    """
    Returns a dictionary mapping resource names to resource extended information of all connected devices.
    Returns: Mapping of resource name to ResourceInfo
    Return type: dict{str => pyvisa.highlevel.ResourceInfo}
    """
    return rm.list_resources_info()


def resource_info(resource_name, extended=True):
    """
    Get the (extended) information of a particular resource.
    Parameters: resource_name – Unique symbolic name of a resource.
    Return type: pyvisa.highlevel.ResourceInfo
    """
    return rm.resource_info(resource_name, extended)

def get_instrument_lib():
    """
    Get instrument model lib classified by type.
    Return: model information classified by its type.
    Return Type: dict{instrument_type => [{model => str, brand => str, class_name => str, params => list, details => dict}]}
    """
    model_lib = {}
    model_dict = models.__dict__
    for i in InstrumentType:
        model_lib[i.name] = []
    for i in model_dict:
        if i.startswith('Model'):
            model_cls = model_dict[i]
            model_str = model_cls.model
            if isinstance(model_str, (tuple, list)):
                model_str = '/'.join(model_cls.model)
            brand = model_cls.brand
            class_name = i
            params = model_cls.params
            details = model_cls.details
            type_str_list = [m.__name__.replace('Type', '') for m in model_cls.mro() if m.__name__.startswith('Type')]
            for type_str in type_str_list:
                model_lib[type_str].append({'model': model_str, 'brand': brand, 'class_name': class_name,
                                            'params': params, 'details': details})
    return model_lib
