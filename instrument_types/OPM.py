from ._BaseInstrumentType import BaseInstrumentType, InstrumentType
from ..utils import dbm_to_w, w_to_dbm, format_unit


class TypeOPM(BaseInstrumentType):
    """Optical Power Meter."""
    def __init__(self, *args, **kwargs):
        super(TypeOPM, self).__init__()
        self._append_ins_type(InstrumentType.OPM)
        self._is_pos_cal = True
        # thresholds
        self._min_wl = None
        self._max_wl = None
        self._min_freq = None
        self._max_freq = None
        self._min_avg_time = None
        self._max_avg_time = None
        self._min_cal = None
        self._max_cal = None

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

    # min_avg_time
    @ property
    def min_avg_time(self):
        if self._min_avg_time is None:
            self._raise_not_implemented()
        else:
            return self._min_avg_time

    @ min_avg_time.setter
    def min_avg_time(self, value):
        raise AttributeError('Attribute "min_avg_time" is read-only.')

    # max_avg_time
    @ property
    def max_avg_time(self):
        if self._max_avg_time is None:
            self._raise_not_implemented()
        else:
            return self._max_avg_time

    @ max_avg_time.setter
    def max_avg_time(self, value):
        raise AttributeError('Attribute "max_avg_time" is read-only.')

    # min_cal
    @ property
    def min_cal(self):
        if self._min_cal is None:
            self._raise_not_implemented()
        else:
            return self._min_cal

    @ min_cal.setter
    def min_cal(self, value):
        raise AttributeError('Attribute "min_cal" is read-only.')

    # max_cal
    @ property
    def max_cal(self):
        if self._max_cal is None:
            self._raise_not_implemented()
        else:
            return self._max_cal

    @ max_cal.setter
    def max_cal(self, value):
        raise AttributeError('Attribute "max_cal" is read-only.')

    # -- methods --
    def get_power_value(self):
        """
        The value of measured optical power, note that the power unit is not certain.

        :Returns: float, value of optical power
        """
        self._raise_not_implemented()

    def get_power_unit(self):
        """
        The unit of measured optical power.

        :Return Type: <enum 'OpticalUnit'>
        """
        self._raise_not_implemented()

    def get_power(self):
        """
        Get the measured power value and unit.

        :Return Type: tuple(float value, <enum 'OpticalUnit'> unit)
        """
        return self.get_power_value(), self.get_power_unit()

    def get_dbm_value(self):
        """
        Get dBm value of measured optical power. The value will convert for unit dBm if it is in Watt.
        
        :Returns: float, optical power in dBm
        """
        unit = self.get_power_unit()
        value = self.get_power_value()
        if unit.value == 0:
            return value
        elif unit.value == 1:
            return w_to_dbm(value)

    def get_w_value(self):
        """
        Get Watt value of measured optical power. The value will convert for unit Watt if it is in dBm.
        
        :Returns: float, optical power in Watt
        """
        unit = self.get_power_unit()
        value = self.get_power_value()
        if unit.value == 1:
            return value
        elif unit.value == 0:
            return dbm_to_w(value)

    def get_cal(self):
        """
        :Returns: float, calibration offset in dB
        """
        self._raise_not_implemented()

    def get_wavelength(self):
        """
        :Returns: float, optical wavelength in nm
        """
        self._raise_not_implemented()

    def get_frequency(self):
        """
        :Returns: float, optical frequency in THz
        """
        self._raise_not_implemented()

    def get_avg_time(self):
        """
        Get averaging time in ms.
        """
        self._raise_not_implemented()

    def set_power_unit(self, unit):
        """
        Set optical power unit.

        :Parameters: **unit** - <enum 'OpticalUnit'>, optical power unit
        """
        self._raise_not_implemented()

    def set_cal(self, value): 
        """
        Set calibration offset in dB.

        :Parameters: **value** - float|int, calibration offset in dB.
        """
        self._raise_not_implemented()

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm.

        :Parameters: **value** - float|int, optical wavelength in dB.
        """
        self._raise_not_implemented()

    def set_frequency(self, value):
        """
        Set optical frequency in THz.

        :Parameters: **value** - float|int, optical frequency in THz
        """
        self._raise_not_implemented()

    def set_to_reference(self):
        """
        Set current optical power to reference power. This action will change calibration offset value.
        """
        dbm_value = self.get_dbm_value()
        cal = self.get_cal()
        sign = 1 if self._is_pos_cal else -1
        self.set_cal(-sign*dbm_value + cal)

    def set_avg_time(self, value):
        """
        Set averaging time in ms.

        :Parameters: **value** - averaging time in ms.
        """
        self._raise_not_implemented()
