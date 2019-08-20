from ._BaseInstrumentType import BaseInstrumentType, InstrumentType
from time import sleep


class TypeOTF(BaseInstrumentType):
    """Optical Tunable Filter."""
    def __init__(self, *args, **kwargs):
        super(TypeOTF, self).__init__()
        self._append_ins_type(InstrumentType.OTF)
        # thresholds
        self._min_wl = None
        self._max_wl = None
        self._min_freq = None
        self._max_freq = None
        self._min_bw = None
        self._max_bw = None

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

    # min_bandwidth
    @ property
    def min_bandwidth(self):
        if self._min_bw is None:
            self._raise_not_implemented()
        else:
            return self._min_bw

    @ min_bandwidth.setter
    def min_bandwidth(self, value):
        raise AttributeError('Attribute "min_bandwidth" is read-only.')

    # max_bandwidth
    @ property
    def max_bandwidth(self):
        if self._max_bw is None:
            self._raise_not_implemented()
        else:
            return self._max_bw

    @ max_bandwidth.setter
    def max_bandwidth(self, value):
        raise AttributeError('Attribute "max_bandwidth" is read-only.')

    # -- methods --
    def get_wavelength(self):
        """
        Get the setting value of center wavelength in nm.
        
        :Returns: float, wavelength setting value in nm.
        """
        self._raise_not_implemented()

    def set_wavelength(self, value):
        """
        Set center wavelength in nm.
        
        :Parameters: **value** - float, center wavelength in nm.
        """
        self._raise_not_implemented()

    def get_frequency(self):
        """
        Get setting value of center frequency in THz.

        :Return Type: float
        """
        self._raise_not_implemented()

    def set_frequency(self, value):
        """
        Set center frequency in THz.

        :Parameters: **value** - float|int, optical frequency in THz
        """
        self._raise_not_implemented()

    def get_wavelength_offset(self):
        """
        Get setting value of wavelength offset in nm.

        :Return Type: float
        """
        self._raise_not_implemented()

    def set_wavelength_offset(self, value):
        """
        Set center wavelength offset in nm.

        :Parameters: **value** - float|int, wavelength offset in nm.
        """
        self._raise_not_implemented()

    def get_bandwidth(self):
        """
        Get filter bandwidth in nm.

        :Return Type: float
        """
        self._raise_not_implemented()

    def set_bandwidth(self, value):
        """
        Set filter bandwidth.

        :Parameters: **value** - float|int, bandwidth setting value in nm
        """
        self._raise_not_implemented()

    def get_bandwidth_offset(self):
        """
        Get setting value filter bandwidth in nm.

        :Return Type: float
        """
        self._raise_not_implemented()

    def set_bandwidth_offset(self, value):
        """
        Set filter bandwidth in nm.

        :Parameters: **value** - float|int, bandwidth offset in nm
        """
        self._raise_not_implemented()

    def peak_search(self, center, span):
        """
        Search peak near the given center wavelength.

        :Parameters:
            - **center** - int|float, center wavelength in nm.
            - **span** - int|float, span in nm.
        """
        self._raise_not_implemented()