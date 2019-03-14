from ..utils import check_type
from ..constants import InstrumentType


class BaseInstrumentType(object):
    # Base Class of Instrument Types
    def __init__(self):
        self._ins_type = []
        super(BaseInstrumentType, self).__init__()

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

    def _raise_no_override(self):
        raise NotImplementedError('This method should be overridden by instrument model class.')