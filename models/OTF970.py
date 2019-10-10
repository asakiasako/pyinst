from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOTF
from ..utils import check_type, check_range
from ..constants import OpticalUnit
from time import sleep


class ModelOTF970(VisaInstrument, TypeOTF):
    model = "OTF-970"
    brand = "Santec"
    details = {
        "Wavelength Range": "1530 ~ 1610 nm",
        "Frequency Range": "186.2 ~ 195.8 THz",
        "Bandwidth @-3dB": "0.08 ~ 4.0 nm",
        "Max Input Power": "+27 dBm"
    }

    def __init__(self, resource_name, read_termination='\r\n', write_termination='\r\n', **kwargs):
        super(ModelOTF970, self).__init__(resource_name, read_termination=read_termination,
                                          write_termination=write_termination, **kwargs)
        self._set_ranges()

    # param encapsulation

    # Methods
    def _set_ranges(self):
        self._min_wl = float(self.query(':WAV? MIN'))*10**9
        self._max_wl = float(self.query(':WAV? MAX'))*10**9
        self._min_freq = float(self.query(':FREQ? MIN'))/(10**12)
        self._max_freq = float(self.query(':FREQ? MAX'))/(10**12)
        self._min_bw = float(self.query(':BAND? MIN'))*10**9
        self._max_bw = float(self.query(':BAND? MAX'))*10**9
        self._min_wl_offs = float(self.query(':OFFS? MIN'))*10**9
        self._max_wl_offs = float(self.query(':OFFS? MAX'))*10**9
        self._min_bw_offs = float(self.query(':OFFS:Band? MIN'))*10**9
        self._max_bw_offs = float(self.query(':OFFS:Band? MAX'))*10**9

    def get_wavelength(self):
        """
        Reads out the setting value of the filter center wavelength.
        :return: (float) wavelength in nm.
        """
        wl_str = self.query(':WAV?')
        wl = float(wl_str)*10**9
        return wl

    def set_wavelength(self, value):
        """
        Sets the filter center wavelength.
        :param value: (float|int) wavelength in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_wl, self._max_wl)
        return self.command(':WAV '+str(value)+'nm')

    def get_wavelength_setting_state(self):
        """
        Reads out the operation state of the filter center wavelength.
        :return: (bool) if setting of the filter center wavelength is in operation.
        """
        state_str = self.query(':WAV:STAT?')
        state = bool(int(state_str))
        return state

    def get_frequency(self):
        """
        Reads out the filter center wavelength in optical frequency.
        :return: (float) optical frequency in THz
        """
        freq_str = self.query(":FREQ?")
        freq = float(freq_str)/(10**12)
        return freq

    def set_frequency(self, value):
        """
        Sets the filter center wavelength in frequency(THz).
        :param value: (float|int) optical frequency in THz
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_freq, self._max_freq)
        return self.command(':FREQ '+str(value)+'THz')

    def get_wavelength_offset(self):
        """
        Reads out the offset wavelength of the filter center wavelength.
        :return: (float) wavelength offset in nm
        """
        offset_str = self.query(':OFFS?')
        offset = float(offset_str)*10**9
        return offset

    def set_wavelength_offset(self, value):
        """
        Sets the offset to the filter center wavelength.
        :param value: (float|int) wavelength
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_wl_offs, self._max_wl_offs)
        return self.command(':OFFS '+str(value)+'nm')

    def get_bandwidth(self):
        """
        Reads out the filter bandwidth.
        :return: (float) bandwidth setting value in nm
        """
        bw_str = self.query(':BAND?')
        bw = float(bw_str)*10**9
        return bw

    def set_bandwidth(self, value):
        """
        Sets the filter bandwidth.
        :param value: (float|int) bandwidth setting value in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_bw, self._max_bw)
        return self.command(':BAND '+str(value)+'nm')

    def get_bandwidth_setting_state(self):
        """
        Reads out the setting state of the filter bandwidth.
        :return: (bool) if setting of the filter bandwidth is in operation
        """
        state_str = self.query(':BAND:STAT?')
        state = bool(int(state_str))
        return state

    def get_bandwidth_offset(self):
        """
        Reads out the offset bandwidth of filter bandwidth.
        :return: (float) bandwidth offset in nm
        """
        offset_str = self.query(':OFFS:Band?')
        offset = float(offset_str)*10**9
        return offset

    def set_bandwidth_offset(self, value):
        """
        Sets the offset to the filter bandwidth.
        :param value: (float|int) bandwidth offset in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_bw_offs, self._max_bw_offs)
        return self.command(':OFFS:Band '+str(value)+'nm')

    def get_power_unit(self):
        """
        Get optical power unit of power monitor.
        :return: int, value of enum (OpticalUnit) optical power unit of power monitor
        """
        unit_str = self.query(':POW:UNIT?')
        unit = int(unit_str.strip())
        return unit

    def set_power_unit(self, unit):
        """
        Set optical power unit of power monitor.
        :param unit: int, value of (OpticalUnit) optical power unit of power monitor
        """
        OpticalUnit(unit)  # check if unit is a valid value
        return self.command(":POW:UNIT "+str(unit))

    def get_power_value(self):
        """
        Get optical power value in selected unit. Range: -40dBm ~ 10dBm
        :return: (float) optical power in selected unit.
        """
        value_str = self.query(':POW?')
        value = float(value_str)
        return value

    def _set_peak_search_center(self, center):
        """
        Set peak search center in nm.
        :param center: (float|int) peak search center in nm
        """
        check_type(center, (int, float), 'center')
        check_range(center, self._min_wl, self._max_wl)
        return self.command(':CENT '+str(center)+'nm')

    def _set_peak_search_span(self, span):
        """
        Set peak search span in nm.
        :param span: (float|int) peak search span in nm
        """
        check_type(span, (float, int), 'span')
        check_range(span, 0, 2*(self._max_wl-self._min_wl))
        return self.command(':SPAN '+str(span)+'nm')

    def _run_peak_search(self, if_run):
        """
        Run or cancel peak search.
        :param if_run: (bool) if run or cancel
        """
        check_type(if_run, bool, 'if_run')
        return self.command(':PS '+str(int(if_run)))

    def _is_peak_search_complete(self):
        """
        If peak search is completed.
        :return: (bool) if peak search is completed.
        """
        status_str = self.query(':PS?')
        status = bool(int(status_str))
        return status

    def peak_search(self, center, span):
        self._set_peak_search_center(center)
        self._set_peak_search_span(span)
        self._run_peak_search(True)
        while True:
            sleep(0.5)
            if self._is_peak_search_complete():
                return self