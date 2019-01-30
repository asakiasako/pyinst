from ....utils import *
from .constants import *
from time import sleep


class TypeIns(object):
    # Base Class of Instrument Types
    def __init__(self):
        self._ins_type = []
        super(TypeIns, self).__init__()

    # param encapsulation
    @property
    def ins_type(self):
        return self._ins_type

    @ins_type.setter
    def ins_type(self, value):
        raise AttributeError('attr "ins_type" is read-only.')

    def _append_ins_type(self, i_type):
        """
        Append new instrument type into ins_type attr.
        :param i_type: (InstrumentType) instrument type
        """
        check_type(i_type, InstrumentType, "i_type")
        if i_type not in self._ins_type:
            self._ins_type.append(i_type)

    def _raise_no_rewrite(self):
        raise AttributeError('This function should be rewritten by extension class.')