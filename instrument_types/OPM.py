from ._BaseInstrumentType import BaseInstrumentType, InstrumentType
from ..utils import dbm_to_w, w_to_dbm, format_unit


class TypeOPM(BaseInstrumentType):
    """Optical Power Meter."""
    def __init__(self, *args, **kwargs):
        super(TypeOPM, self).__init__()
        self._append_ins_type(InstrumentType.OPM)
        self._is_pos_cal = True

    def get_value(self):
        """
        The value of measured optical power, note that the power unit is not certain.

        :Returns: float, value of optical power
        """
        self._raise_not_implemented()

    def get_unit(self):
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
        return self.get_value(), self.get_unit()

    def get_dbm_value(self):
        """
        Get dBm value of measured optical power. The value will convert for unit dBm if it is in Watt.
        
        :Returns: float, optical power in dBm
        """
        unit = self.get_unit()
        value = self.get_value()
        if unit.value == 0:
            return value
        elif unit.value == 1:
            return w_to_dbm(value)

    def get_w_value(self):
        """
        Get Watt value of measured optical power. The value will convert for unit Watt if it is in dBm.
        
        :Returns: float, optical power in Watt
        """
        unit = self.get_unit()
        value = self.get_value()
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

    def get_formatted_w_power(self):
        """
        Return a formatted power in Watt based unit, such as: (34, 'mW'), (223, 'pW')

        :Return Type: tuple(float value, str unit)
        """
        w_value = self.get_w_value()
        value, unit = format_unit(w_value, 3)
        unit += 'W'
        return value, unit

    def get_avg_time(self, value):
        """
        Get averaging time in ms.
        """
        self._raise_not_implemented()

    def set_unit(self, unit):
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
