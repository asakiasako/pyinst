from .ins_type_bases import *


class TypeOSA(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeOSA, self).__init__()
        self._append_ins_type(InstrumentType.OSA)

    # Methods
    def sweep(self, mode="REPEAT"):
        """
        Set OSA sweep mode. mode = "AUTO"|"REPEAT"|"SINGLE"|"STOP"
        :param mode: (str) "AUTO"|"REPEAT"|"SINGLE"|"STOP"
        """
        self._raise_no_rewrite()

    def set_analysis_cat(self, item):
        """
        Set OSA analysis item. Available item depends on specific instrument.
        :param item: (str) analysis item
        """
        self._raise_no_rewrite()

    def get_analysis_cat(self):
        """
        Get the current analysis item.
        :return: (str) analysis item
        """
        self._raise_no_rewrite()

    def analysis_setting(self, cat, param, value):
        """
        Analysis setting. param and value depends on specific instrument.
        :param cat: (str) setting category
        :param param: (str) setting item
        :param value: (str) setting value
        """
        self._raise_no_rewrite()

    def get_analysis_setting_map(self):
        """
        Get setting map for all analysis categories.
        :return: (dict) analysis setting map
        """
        self._raise_no_rewrite()

    def get_analysis_data(self):
        """
        Get data of current analysis item.
        :return: (str) data of current analysis item
        """
        self._raise_no_rewrite()

    def set_center(self, value, unit):
        """
        Set center wavelength/frequency
        :param value: (float) center value
        :param unit: (str) unit
        """
        self._raise_no_rewrite()

    def get_center(self):
        """
        Get center wavelength setting
        :return: (float) center wavelength in nm
        """
        self._raise_no_rewrite()

    def set_peak_to_center(self):
        """
        Set peak wavelength to center.
        """
        self._raise_no_rewrite()

    def set_span(self, value, unit):
        """
        Set span wavelength/frequency
        :param value: (float) span value
        :param unit: (str) unit
        """
        self._raise_no_rewrite()

    def set_start_stop_wavelength(self, start, stop):
        """
        Set start-stop wavelength.
        :param start: (float) start wavelength in nm
        :param stop: (float) stop wavelength in nm
        """
        self._raise_no_rewrite()

    def set_start_stop_frequency(self, start, stop):
        """
        Set start-stop frequency.
        :param start: (float) start frequency in THz
        :param stop: (float) stop frequency in THz
        """
        self._raise_no_rewrite()

    def set_ref_level(self, value, unit):
        """
        Set reference level.
        :param value: (float) reference level value
        :param unit: (str) unit
        """
        self._raise_no_rewrite()

    def set_peak_to_ref(self):
        """
        Set peak level to reference level
        """
        self._raise_no_rewrite()

    def setup(self, param, value):
        """
        Set setup settings.
        :param param: (str) param
        :param value: (str) setting value
        """
        self._raise_no_rewrite()

    def format_data(self, cat, data):
        """
        Format data into dict, depends on calculate category (Anasis Category)
        :param cat: (str) "DFB"|"FP"|"WDM"
        :param data: (str) data retruned by method: get_analysis_data
        :return: (dict) a dict of test_item=>value
        """
        self._raise_no_rewrite()

    def set_auto_zero(self, is_on):
        """
        Enable or disable auto zero
        """
        self._raise_no_rewrite()

    def zero_once(self):
        """
        perform zeroing once
        """
        self._raise_no_rewrite()

    def set_marker_x(self, num, value, unit):
        """
        set marker x
        unit: NM|THZ
        """
        self._raise_no_rewrite()

    def get_marker_x(self, num):
        """
        get marker x
        """
        self._raise_no_rewrite()

    def get_marker_y(self, num):
        """
        get marker y level
        """
        self._raise_no_rewrite()

    def clear_all_markers(self):
        """
        """
        self._raise_no_rewrite()