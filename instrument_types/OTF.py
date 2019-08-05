from ._BaseInstrumentType import BaseInstrumentType, InstrumentType
from time import sleep


class TypeOTF(BaseInstrumentType):
    """Optical Tunable Filter."""
    def __init__(self, *args, **kwargs):
        super(TypeOTF, self).__init__()
        self._append_ins_type(InstrumentType.OTF)
        self._max_wl = 0
        self._min_wl = 0
        self._max_freq = 0
        self._min_freq = 0
        self._max_bw = 0
        self._min_bw = 0
        self._max_wl_offs = 0
        self._min_wl_offs = 0
        self._max_bw_offs = 0
        self._min_bw_offs = 0

    # Method
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