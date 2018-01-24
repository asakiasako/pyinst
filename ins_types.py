from enum import Enum, unique
from .unit_conv import *
from time import sleep

# define enums
# noinspection PyArgumentList
InstrumentType = Enum('InstrumentType', (
    'OPM',  # Optical Power Meter
    'VOA',  # Variable Optical Attenuator
    'OMA',  # Optical Modulation Analyser
    'OSA',  # Optical Spectrum Analyser
    'WM',   # Optical Wavelength Meter
    'OTF',  # Optical Tunable Filter
    'TEC',  # Temp Control
    'SW',   # Optical Switcher
    'PS',   # Power Supply
))


@unique
class OpticalUnit(Enum):
    DBM = 0
    W = 1


@unique
class WavelengthUnit(Enum):
    NM = 0
    HZ = 1

# --- Instrument Types ---

class TypeIns(object):
    # Base Class of Instrument Types
    def __init__(self):
        self._ins_type = []
        super(TypeIns, self).__init__()

    # param encapsulation
    @property
    def ins_type(self):
        return self._ins_type

    @ins_type.setter
    def ins_type(self, value):
        raise AttributeError('attr "ins_type" is read-only.')

    def _append_ins_type(self, i_type):
        """
        Append new instrument type into ins_type attr.
        :param i_type: (InstrumentType) instrument type
        """
        check_type(i_type, InstrumentType, "i_type")
        if i_type not in self._ins_type:
            self._ins_type.append(i_type)

    def _raise_no_rewrite(self):
        raise AttributeError('This function should be rewritten by extension class.')


class TypeOPM(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeOPM, self).__init__()
        self._append_ins_type(InstrumentType.OPM)

    def get_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        self._raise_no_rewrite()

    def get_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: (enum 'OpticalUnit') unit of optical power
        """
        self._raise_no_rewrite()

    def get_power(self):
        """
        Return a tuple of (value, unit)
        :return: (tuple) (float:value, OpticalUnit:unit)
        """
        return self.get_value(), self.get_unit()

    def get_dbm_value(self):
        """
        Return dBm value of optical power.
        If optical power unit is not dBm, the value will be calculated in math method.
        :return: (float) optical power in dBm
        """
        unit = self.get_unit()
        value = self.get_value()
        if unit.value == 0:
            return value
        elif unit.value == 1:
            return w_to_dbm(value)

    def get_w_value(self):
        """
        Return watt value of optical power.
        If optical power unit is not watt, the value will be calculated in math method.
        :return: (float) optical power in watt
        """
        unit = self.get_unit()
        value = self.get_value()
        if unit.value == 1:
            return value
        elif unit.value == 0:
            return dbm_to_w(value)

    def get_cal(self):
        """
        :return: (float) calibration offset in dB
        """
        self._raise_no_rewrite()

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        self._raise_no_rewrite()

    def get_formatted_w_power(self):
        """
        Return a formatted power in w based unit, such as: (34, 'mw'), (223, 'pw')
        :return: (tuple) (float:value, str:unit)
        """
        w_value = self.get_w_value()
        value, unit = format_unit(w_value, 3)
        unit += 'w'
        return value, unit

    def set_unit(self, unit):
        """
        Set optical power unit
        """
        self._raise_no_rewrite()

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        self._raise_no_rewrite()

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        self._raise_no_rewrite()

    def set_to_reference(self):
        """
        Set current optical power as reference
        """
        dbm_value = self.get_dbm_value()
        cal = self.get_cal()
        self.set_cal(dbm_value + cal)


class TypeVOA(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeVOA, self).__init__()
        self._append_ins_type(InstrumentType.VOA)

    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        self._raise_no_rewrite()

    def disable(self):
        """
        Set VOA output disabled.
        """
        return self.enable(False)

    def is_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        self._raise_no_rewrite()

    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        self._raise_no_rewrite()

    def get_offset(self):
        """
        Get offset value in dB.
        :return: (float) offset value in dB
        """
        self._raise_no_rewrite()

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        self._raise_no_rewrite()

    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        self._raise_no_rewrite()

    def set_offset(self, value):
        """
        Set offset value in dB.
        :param value: (float|int) offset value in dB
        """
        self._raise_no_rewrite()

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        self._raise_no_rewrite()


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


class TypeOTF(TypeIns):
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
        Reads out the setting range of the filter center wavelength.
        :return: (tuple) (float: min, float: max) in nm
        """
        return self._min_wl, self._max_wl

    def get_frequency_range(self):
        """
        Reads out the setting range of the filter center wavelength in THz.
        :return: (tuple) (float: min, float: max) in THz
        """
        return self._min_freq, self._max_freq

    def get_bandwidth_range(self):
        """
        Reads out the setting range of the filter bandwidth in nm
        :return: (tuple) (float: min, float: max) in nm
        """
        return self._min_bw, self._max_bw

    def get_wavelength_offset_range(self):
        """
        Reads out the setting range of the filter wavelength offset in nm
        :return: (tuple) (float: min, float: max) in nm
        """
        return self._min_wl_offs, self._max_wl_offs

    def get_bandwidth_offset_range(self):
        """
        Reads out the setting range of the filter bandwidth offset in nm
        :return: (tuple) (float: min, float: max) in nm
        """
        return self._min_bw_offs, self._max_bw_offs

    def get_wavelength(self):
        """
        Reads out the setting value of the filter center wavelength.
        :return: (float) wavelength in nm.
        """
        self._raise_no_rewrite()

    def set_wavelength(self, value):
        """
        Sets the filter center wavelength.
        :param value: (float|int) wavelength in nm
        """
        self._raise_no_rewrite()

    def get_wavelength_state(self):
        """
        Reads out the operation state of the filter center wavelength.
        :return: (bool) if setting of the filter center wavelength is in operation.
        """
        self._raise_no_rewrite()

    def get_frequency(self):
        """
        Reads out the filter center wavelength in optical frequency.
        :return: (float) optical frequency in THz
        """
        self._raise_no_rewrite()

    def set_frequency(self, value):
        """
        Sets the filter center wavelength in frequency(THz).
        :param value: (float|int) optical frequency in THz
        """
        self._raise_no_rewrite()

    def get_wavelength_offset(self):
        """
        Reads out the offset wavelength of the filter center wavelength.
        :return: (float) wavelength offset in nm
        """
        self._raise_no_rewrite()

    def set_wavelength_offset(self, value):
        """
        Sets the offset to the filter center wavelength.
        :param value: (float|int) wavelength
        """
        self._raise_no_rewrite()

    def get_bandwidth(self):
        """
        Reads out the filter bandwidth.
        :return: (float) bandwidth setting value in nm
        """
        self._raise_no_rewrite()

    def set_bandwidth(self, value):
        """
        Sets the filter bandwidth.
        :param value: (float|int) bandwidth setting value in nm
        """
        self._raise_no_rewrite()

    def get_bandwidth_state(self):
        """
        Reads out the setting state of the filter bandwidth.
        :return: (bool) if setting of the filter bandwidth is in operation
        """
        self._raise_no_rewrite()

    def get_bandwidth_offset(self):
        """
        Reads out the offset bandwidth of filter bandwidth.
        :return: (float) bandwidth offset in nm
        """
        self._raise_no_rewrite()

    def set_bandwidth_offset(self, value):
        """
        Sets the offset to the filter bandwidth.
        :param value: (float|int) bandwidth offset in nm
        """
        self._raise_no_rewrite()

    def get_power_unit(self):
        """
        Get optical power unit of power monitor.
        :return: (OpticalUnit) optical power unit of power monitor
        """
        self._raise_no_rewrite()

    def set_power_unit(self, unit):
        """
        Set optical power unit of power monitor.
        :param unit: (OpticalUnit) optical power unit of power monitor
        """
        self._raise_no_rewrite()

    def get_power_value(self):
        """
        Get optical power value in selected unit. Range: -40dBm ~ 10dBm
        :return: (float) optical power in selected unit.
        """
        self._raise_no_rewrite()

    def _set_peak_search_center(self, center):
        """
        Set peak search center in nm.
        :param center: (float|int) peak search center in nm
        """
        self._raise_no_rewrite()

    def _set_peak_search_span(self, span):
        """
        Set peak search span in nm.
        :param span: (float|int) peak search span in nm
        """
        self._raise_no_rewrite()

    def _run_peak_search(self, if_run):
        """
        Run or cancel peak search.
        :param if_run: (bool) if run or cancel
        """
        self._raise_no_rewrite()

    def _is_peak_search_complete(self):
        """
        If peak search is completed.
        :return: (bool) if peak search is completed.
        """
        self._raise_no_rewrite()

    def peak_search(self, center, span):
        self._set_peak_search_center(center)
        self._set_peak_search_span(span)
        self._run_peak_search(True)
        print('1')
        while True:
            print('2')
            sleep(0.5)
            print('3')
            if self._is_peak_search_complete():
                print('4')
                return self


class TypePS(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypePS, self).__init__()
        self._append_ins_type(InstrumentType.PS)
        self._max_volt = self._max_current = 0

    # Methods
    def enable(self, status=True):
        """
        Enable power supply output or not.
        :param status: (bool) enable status of power supply output
        """
        self._raise_no_rewrite()

    def disable(self):
        """
        Disable power supply output.
        """
        return self.enable(False)

    def is_enabled(self):
        """
        Get the power supply output enable status.
        :return: (bool) if power supply output is enabled.
        """
        self._raise_no_rewrite()

    def set_voltage(self, value):
        """
        Set voltage (limit).
        :param value: (float|int) voltage value in V
        """
        self._raise_no_rewrite()

    def get_voltage(self):
        """
        Get voltage (limit) setting.
        :return: (float) voltage value in V
        """
        self._raise_no_rewrite()

    def measure_voltage(self):
        """
        Query voltage measured
        :return: (float) voltage measured in V
        """
        self._raise_no_rewrite()

    def set_current(self, value):
        """
        Set current (limit).
        :param value: (float|int) current value in A
        """
        self._raise_no_rewrite()

    def get_current(self):
        """
        Get current (limit) setting.
        :return: (float) current value in A
        """
        self._raise_no_rewrite()

    def measure_current(self):
        """
        Query current measured.
        :return: (float) current measured in A
        """
        self._raise_no_rewrite()

    def set_ocp(self, value):
        """
        :param value: (float|int) ocp value in A
        """
        self._raise_no_rewrite()

    def get_ocp(self):
        """
        :return: (float) ocp value in A
        """
        self._raise_no_rewrite()

    def set_ocp_status(self, status):
        """
        :param status: (bool) if ocp is enabled
        """
        self._raise_no_rewrite()

    def get_ocp_status(self):
        """
        :return: (bool) if ocp is enabled
        """
        self._raise_no_rewrite()

    def ocp_is_tripped(self):
        """
        Check if the over-current protection circuit is tripped and not cleared
        :return: (bool) if ocp is tripped
        """
        self._raise_no_rewrite()

    def clear_ocp(self):
        """
        clear ocp status
        """
        self._raise_no_rewrite()

    def set_ovp(self, value):
        """
        :param value: (float|int) ovp value in V
        """
        self._raise_no_rewrite()

    def get_ovp(self):
        """
        :return: (float) ovp value in V
        """
        self._raise_no_rewrite()

    def set_ovp_status(self, status):
        """
        :param status: (bool) if ovp is enabled
        """
        self._raise_no_rewrite()

    def get_ovp_status(self):
        """
        :return: (bool) if ovp is enabled
        """
        self._raise_no_rewrite()

    def ovp_is_tripped(self):
        """
        Check if the over-voltage protection circuit is tripped and not cleared
        :return: (bool) if ovp is tripped
        """
        self._raise_no_rewrite()

    def clear_ovp(self):
        """
        clear OVP status
        """
        self._raise_no_rewrite()
