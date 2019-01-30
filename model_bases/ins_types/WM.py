from .ins_type_bases import *


class TypeWM(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeWM, self).__init__()
        self._append_ins_type(InstrumentType.WM)

    def start(self):
        """
        Start repeat measurement.
        """
        self._raise_no_rewrite()

    def stop(self):
        """
        Stop repeat measurement.
        """
        self._raise_no_rewrite()

    def is_started(self):
        """
        Get measurement state of WM.
        :return: (bool) if repeat measurement is started.
        """
        self._raise_no_rewrite()

    def get_frequency_array(self):
        """
        Get wavelength of all peaks in unit of frequency(Hz).
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        self._raise_no_rewrite()

    def get_wavelength_array(self):
        """
        Get wavelength of all peaks in unit of wavelength(m).
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        self._raise_no_rewrite()

    def get_power_array(self):
        """
        Get optical power of all peaks in selected unit.
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        self._raise_no_rewrite()

    def get_power_unit(self):
        """
        Get optical power unit.
        :return: (OpticalUnit) optical power unit.
        """
        self._raise_no_rewrite()

    def set_power_unit(self, unit):
        """
        Set optical power unit.
        :param unit: (OpticalUnit) optical power unit.
        """
        self._raise_no_rewrite()

    def get_frequency(self):
        """
        Get frequency of single peak in Hz
        :return: (float) frequency in Hz
        """
        self._raise_no_rewrite()

    def get_wavelength(self):
        """
        Get wavelength of single peak in m
        :return: (float) wavelength in m
        """
        self._raise_no_rewrite()

    def get_power(self):
        """
        Get wavelength of single peak in selected unit
        :return: (float) optical power in selected unit.
        """
        self._raise_no_rewrite()