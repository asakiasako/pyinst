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


# Instrument Types

class TypeIns(object):
    # Base Class of Instrument Types
    def __init__(self, ins_type):
        if not hasattr(self, '_ins_type'):
            self._ins_type = []
        if ins_type not in self._ins_type:
            self._ins_type.append(ins_type)

    def raise_no_rewrite(self):
        raise AttributeError('This function should be rewritten by extension class.')


class TypeOPM(TypeIns):
    def __init__(self):
        super(TypeOPM, self).__init__(InstrumentTypes.OPM)

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
        :return: (tuple) (float value, OpticalUnit unit)
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

    def set_unit(self):
        """
        Set optical power unit
        """
        self.raise_no_rewrite()

    def set_cal(self):
        """
        Set calibration offset in dB
        """
        self.raise_no_rewrite()

    def set_wavelength(self):
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
