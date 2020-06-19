from abc import abstractmethod
from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeWGEN(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeWGEN, self).__init__()
        self._append_ins_type(InstrumentType.WGEN)

    @abstractmethod
    def set_frequency(self, frequency):
        """
        frequency: float|int, in Hz
        """

    @abstractmethod
    def get_frequency(self):
        """
        return: float, frequency in Hz
        """

    @abstractmethod
    def set_period(self, period):
        """
        period: int|float
        """

    @abstractmethod
    def get_period(self):
        """
        return: float, period of waveform generator
        """

    @abstractmethod
    def set_function(self, signal):
        """
        signal: str, options depends on specific model.
        """
    
    @abstractmethod
    def get_function(self):
        """
        return: str, function of waveform generator.
        """

    @abstractmethod
    def enable(self, enable=True):
        """
        enable or disable waveform generator output
        """

    @abstractmethod
    def disable(self):
        """
        disable waveform generator output
        """

    @abstractmethod
    def is_enabled(self):
        """
        return bool
        """

    @abstractmethod
    def set_voltage_amplitude(self, amplitude):
        """
        voltage: int|float, 
        """

    @abstractmethod
    def get_voltage_amplitude(self):
        """
        return: float
        """

    def set_voltage(self, voltage):
        """
        alias of set_voltage_amplitude
        """
        return self.set_voltage_amplitude(voltage)

    def get_voltage(self):
        """
        alias of get_voltage_amplitude
        """
        return self.get_voltage_amplitude()

    @abstractmethod
    def set_voltage_offset(self, offset):
        """
        offset: int|float
        """

    @abstractmethod
    def get_voltage_offset(self):
        """
        return: float
        """
    
    @abstractmethod
    def set_voltage_high(self, high_voltage):
        """
        high_voltage: int|float
        """

    @abstractmethod
    def get_voltage_high(self):
        """
        return: float
        """

    @abstractmethod
    def set_voltage_low(self, low_voltage):
        """
        low_voltage: int|float
        """
        
    @abstractmethod
    def get_voltage_low(self):
        """
        return: float
        """

    