from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePDLE(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePDLE, self).__init__()
        self._append_ins_type(InstrumentType.PDLE)
        # thresholds
        self._min_wl = None
        self._max_wl = None
        self._min_freq = None
        self._max_freq = None

    # -- properties --
    # min_wavelength
    @ property
    def min_wavelength(self):
        if self._min_wl is None:
            self._raise_not_implemented()
        else:
            return self._min_wl

    @ min_wavelength.setter
    def min_wavelength(self, value):
        raise AttributeError('Attribute "min_wavelength" is read-only.')

    # max_wavelength
    @ property
    def max_wavelength(self):
        if self._max_wl is None:
            self._raise_not_implemented()
        else:
            return self._max_wl

    @ max_wavelength.setter
    def max_wavelength(self, value):
        raise AttributeError('Attribute "max_wavelength" is read-only.')

    # min_frequency
    @ property
    def min_frequency(self):
        if self._min_freq is None:
            self._raise_not_implemented()
        else:
            return self._min_freq

    @ min_frequency.setter
    def min_frequency(self, value):
        raise AttributeError('Attribute "min_frequency" is read-only.')

    # max_frequency
    @ property
    def max_frequency(self):
        if self._max_freq is None:
            self._raise_not_implemented()
        else:
            return self._max_freq

    @ max_frequency.setter
    def max_frequency(self, value):
        raise AttributeError('Attribute "max_frequency" is read-only.')

    # -- methods --
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