from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePDLE(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePDLE, self).__init__()
        self._append_ins_type(InstrumentType.PDLE)

    def get_wavelength(self):
        """
        Get the setting value of wavelength in nm.
        
        :Returns: float, wavelength setting value in nm.
        """
        self._raise_not_implemented()

    def set_wavelength(self, wavelength):
        """
        Set wavelength in nm.
        
        :Parameters: **wavelength** - float, wavelength in nm.
        """
        self._raise_not_implemented()

    def get_frequency(self):
        """
        Get the setting value of frequency in THz.
        """
        self._raise_not_implemented()

    def set_frequency(self, freq):
        """
        Set frequency in THz
        """
        self._raise_not_implemented()
    
    def get_pdl_value(self):
        """
        Get current PDL value
        
        :Returns: float, PDL value in dB
        """
        self._raise_not_implemented()

    def set_pdl_value(self, value):
        """
        Set PDL value

        :Parameters: **value** - float|int, pdl value in dB
        """
        self._raise_not_implemented()