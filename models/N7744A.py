from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOPM
from ..constants import OpticalUnit, LIGHT_SPEED
import math

class ModelN7744A(VisaInstrument, TypeOPM):
    brand = "Keysight"
    model = "N7744A"
    details = {
        "Wavelength Range": "1250~1625 nm",
        "Power Range": "-80 ~ +10 dBm",
        "Safe Power": "+16 dBm",
        "AVG Time": "1 us ~ 10 s"
    }
    params = [
        {
            "name": "slot",
            "type": "int",
            "options": [1, 2, 3, 4]
        }
    ]

    def __init__(self, resource_name, slot, max_slot=4, **kwargs):
        if not isinstance(slot, int):
            raise TypeError('Parameter slot should be int')
        if not 1 <= slot <= max_slot:
            raise ValueError('slot out of range.')
        super(ModelN7744A, self).__init__(resource_name, **kwargs)
        self._is_pos_cal = False
        self.__slot = slot
        # thresholds
        self._max_wl = 1625.0
        self._min_wl = 1250.0
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
        self._min_avg_time = 0.001
        self._max_avg_time = 10000
        self._min_cal = float('-inf')
        self._max_cal = float('inf')

    # param encapsulation
    @property
    def slot(self):
        return self.__slot

    @slot.setter
    def slot(self, value):
        raise AttributeError('attr "slot" is read-only.')

    # Rewrite TypeOPM Methods
    def get_power_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        value_str = self.query(":FETC"+str(self.slot)+":POW?")
        if not value_str:
            raise ValueError('Empty return for get_power_value')
        value = float(value_str)
        return value

    def get_power_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: int, value of (enum 'OpticalUnit') unit of optical power
        """
        unit_int = int(self.query(":SENS" + str(self.slot) + ":POW:UNIT?"))
        if unit_int == 0:
            unit = OpticalUnit.DBM.value
        elif unit_int == 1:
            unit = OpticalUnit.W.value
        else:
            unit = None
        return unit

    def get_avg_time(self):
        """
        Get averaging time in ms.
        """
        avg_in_s = float(self.query(":sens" + str(self.slot) + ":pow:atim?"))
        avg_in_ms = avg_in_s*1E+3
        return avg_in_ms

    def get_cal(self):
        """
        :return: (float) calibration offset in dB
        """
        cal_str = self.query(':sens' + str(self.slot) + ':corr?')
        cal = float(cal_str)
        return cal

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query(":sens" + str(self.slot) + ":pow:wav?")
        wl = float(wl_str) * 10 ** 9
        return wl

    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def set_power_unit(self, unit):
        """
        Set optical power unit
        """
        OpticalUnit(unit)  # check if unit is a valid value
        return self.command(":SENS" + str(self.slot) + ":POW:UNIT " + str(unit))

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        if not isinstance(value, (float, int)):
            raise TypeError('Calibration value should be numbwer')
        return self.command(':sens' + str(self.slot) + ':corr ' + str(value) + 'DB')

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Wavelength value should be number')
        if not self.min_wavelength <= value <= self.max_wavelength:
            raise ValueError('Wavelength value out of range')
        return self.command(":sens" + str(self.slot) + ":pow:wav " + str(value) + "NM")

    def set_frequency(self, value):
        return self.set_wavelength(round(LIGHT_SPEED/value, 4))

    def get_wavelength_range(self):
        """
        Get wavelength range in nm.
        :return: <tuple: (<float: min>, <float: max>)>
        """
        return self._min_wl, self._max_wl

    def set_avg_time(self, value):
        """
        set avg time in ms
        """
        if not isinstance(value, (float, int)):
            raise TypeError('Averaging time should be number')
        if not self.min_avg_time <= value <= self.max_avg_time:
            raise ValueError('Averaging time out of range')
        return self.command(":sens" + str(self.slot) + ":pow:atim " + str(value) + "MS")