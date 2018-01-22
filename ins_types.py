from enum import Enum, unique
from .unit_conv import *

# define enums
# noinspection PyArgumentList
InstrumentTypes = Enum('InstrumentTypes', (
    'OPM',  # Optical Power Meter
    'VOA',  # Variable Optical Attenuator
    'OMA',  # Optical Modulation Analyser
    'OSA',  # Optical Spectrum Analyser
    'WM',   # Optical Wavelength Meter
    'OTF',  # Optical Tunable Filter
    'TEC',  # Temp Control
    'SW',   # Optical Switcher
))


@unique
class OpticalUnits(Enum):
    DBM = 0
    W = 1


# --- Instrument Types ---

class TypeIns(object):
    # Base Class of Instrument Types
    def __init__(self):
        self._ins_type = []

    # param encapsulation
    @property
    def ins_type(self):
        return self._ins_type

    @ins_type.setter
    def ins_type(self, value):
        raise AttributeError('attr "ins_type" is read-only.')

    def append_ins_type(self, i_type):
        """
        Append new instrument type into ins_type attr.
        :param i_type: (InstrumentTypes) instrument type
        """
        if not isinstance(i_type, InstrumentTypes):
            raise TypeError('i_type should be <enum InstrumentTypes>')
        if i_type not in self._ins_type:
            self._ins_type.append(i_type)

    def raise_no_rewrite(self):
        raise AttributeError('This function should be rewritten by extension class.')


class TypeOPM(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeOPM, self).__init__()
        self.append_ins_type(InstrumentTypes.OPM)

    def get_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        self.raise_no_rewrite()

    def get_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: (enum 'OpticalUnit') unit of optical power
        """
        self.raise_no_rewrite()

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
        self.raise_no_rewrite()

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        self.raise_no_rewrite()

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
        self.raise_no_rewrite()

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        self.raise_no_rewrite()

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        self.raise_no_rewrite()

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
        self.append_ins_type(InstrumentTypes.VOA)

    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        self.raise_no_rewrite()

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
        self.raise_no_rewrite()

    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        self.raise_no_rewrite()

    def get_offset(self):
        """
        Get offset value in dB.
        :return: (float) offset value in dB
        """
        self.raise_no_rewrite()

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        self.raise_no_rewrite()

    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        self.raise_no_rewrite()

    def set_offset(self, value):
        """
        Set offset value in dB.
        :param value: (float|int) offset value in dB
        """
        self.raise_no_rewrite()

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        self.raise_no_rewrite()

