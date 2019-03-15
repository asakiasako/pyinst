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
    def get_wavelength_range(self):
        """
        Get valid setting range of center wavelength in nm.

        :Return Type: tuple(float min, float max)
        """
        return self._min_wl, self._max_wl

    def get_frequency_range(self):
        """
        Get valid setting range of center frequency in THz.

        :Return Type: tuple(float min, float max)
        """
        return self._min_freq, self._max_freq

    def get_bandwidth_range(self):
        """
        Get valid setting range of filter bandwidth in nm.

        :Return Type: tuple(float min, float max)
        """
        return self._min_bw, self._max_bw

    def get_wavelength_offset_range(self):
        """
        Get valid setting range of wavelength offset in nm.

        :Return Type: tuple(float min, float max)
        """
        return self._min_wl_offs, self._max_wl_offs

    def get_bandwidth_offset_range(self):
        """
        Get valid setting range of filter bandwidth offset in nm.

        :Return Type: tuple(float min, float max)
        """
        return self._min_bw_offs, self._max_bw_offs

    def get_wavelength(self):
        """
        Get the setting value of center wavelength in nm.
        
        :Returns: float, wavelength setting value in nm.
        """
        self._raise_no_override()

    def set_wavelength(self, value):
        """
        Set center wavelength in nm.
        
        :Parameters: **value** - float, center wavelength in nm.
        """
        self._raise_no_override()

    def get_frequency(self):
        """
        Get setting value of center frequency in THz.

        :Return Type: float
        """
        self._raise_no_override()

    def set_frequency(self, value):
        """
        Set center frequency in THz.

        :Parameters: **value** - float|int, optical frequency in THz
        """
        self._raise_no_override()

    def get_wavelength_offset(self):
        """
        Get setting value of wavelength offset in nm.

        :Return Type: float
        """
        self._raise_no_override()

    def set_wavelength_offset(self, value):
        """
        Set center wavelength offset in nm.

        :Parameters: **value** - float|int, wavelength offset in nm.
        """
        self._raise_no_override()

    def get_bandwidth(self):
        """
        Get filter bandwidth in nm.

        :Return Type: float
        """
        self._raise_no_override()

    def set_bandwidth(self, value):
        """
        Set filter bandwidth.

        :Parameters: **value** - float|int, bandwidth setting value in nm
        """
        self._raise_no_override()

    def get_bandwidth_offset(self):
        """
        Get setting value filter bandwidth in nm.

        :Return Type: float
        """
        self._raise_no_override()

    def set_bandwidth_offset(self, value):
        """
        Set filter bandwidth in nm.

        :Parameters: **value** - float|int, bandwidth offset in nm
        """
        self._raise_no_override()

    def _set_peak_search_center(self, center):
        """
        Set peak search center in nm.

        :Parameters: **center** - float|int, peak search center in nm
        """
        self._raise_no_override()

    def _set_peak_search_span(self, span):
        """
        Set peak search span in nm.

        :Parameters: **span** - float|int, peak search span in nm.
        """
        self._raise_no_override()

    def _run_peak_search(self, if_run):
        """
        Run or cancel peak search.

        :Parameters: **if_run** - bool, True -> run, False -> cancel.
        """
        self._raise_no_override()

    def _is_peak_search_complete(self):
        """
        If peak search is completed.

        :Returns: bool, if peak search is completed.
        """
        self._raise_no_override()

    def peak_search(self, center, span):
        """
        Search peak near the given center wavelength.

        :Parameters:
            - **center** - int|float, center wavelength in nm.
            - **span** - int|float, span in nm.
        """
        self._set_peak_search_center(center)
        self._set_peak_search_span(span)
        self._run_peak_search(True)
        while True:
            sleep(0.5)
            if self._is_peak_search_complete():
                return self