from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePMDE(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePMDE, self).__init__()
        self._append_ins_type(InstrumentType.PMDE)
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
        self._raise_not_implemented()

    def get_frequency(self):
        self._raise_not_implemented()

    def set_wavelength(self, wavelength):
        """
        Set wavelength in nm.
        
        :Parameters: **wavelength** - float, wavelength in nm.
        """
        self._raise_not_implemented()

    def set_frequency(self, freq):
        """
        set frequency in THz
        """
        self._raise_not_implemented()
    
    def set_pmd_value(self, pmd, sopmd):
        """
        Set PMD(DGD) and SOPMD target value.

        :Parameters: 
            - **pmd** - float|int, DGD value in ps
            - **sopmd** - float|int, 2nd order pmd in ps**2
        """
        self._raise_not_implemented()