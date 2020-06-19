from abc import abstractmethod
from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeOSC(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeOSC, self).__init__()
        self._append_ins_type(InstrumentType.OSC)

    def set_measurement_source(self, slot, source_idx, source):
        """
        source_idx: int, 1 or 2. most measurements has only 1 source.
        source: str, CH<x>|MATH<y>|REF<x>|HIStogram
        """
        
    @abstractmethod
    def set_measurement_type(self, slot, m_type):
        """
        set measurement type
        """

    @abstractmethod
    def start_measurement(self, slot, start=True):
        """
        start or stop measurement
        """

    def stop_measurement(self, slot):
        return self.start_measurement(slot, False)

    @abstractmethod
    def get_measurement(self, slot, category):
        """
        slot: int
        category: str, example: MIN, MEAN
        return: value, unit
        """
