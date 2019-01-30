from .ins_type_bases import *


class TypeOPM(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeOPM, self).__init__()
        self._append_ins_type(InstrumentType.OPM)

    def get_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        self._raise_no_override()

    def get_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: (enum 'OpticalUnit') unit of optical power
        """
        self._raise_no_override()

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
        self._raise_no_override()

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        self._raise_no_override()

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
        self._raise_no_override()

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        self._raise_no_override()

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        self._raise_no_override()

    def set_to_reference(self):
        """
        Set current optical power as reference
        """
        dbm_value = self.get_dbm_value()
        cal = self.get_cal()
        self.set_cal(dbm_value + cal)

    def set_avg_time(self, value):
        """
        set avg time in ms
        """
        self._raise_no_override()
