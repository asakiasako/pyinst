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
        self._raise_no_override()

    def set_wavelength(self, wavelength):
        """
        Set wavelength in nm.
        
        :Parameters: **wavelength** - float, wavelength in nm.
        """
        self._raise_no_override()
    
    def get_pdl_value(self):
        """
        Get current PDL value
        
        :Returns: float, PDL value in dB
        """
        self._raise_no_override()

    def set_pdl_value(self, value):
        """
        Set PDL value

        :Parameters: **value** - float|int, pdl value in dB
        """
        self._raise_no_override()