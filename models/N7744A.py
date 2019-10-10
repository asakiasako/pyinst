from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOPM
from ..utils import check_range, check_type
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
            "name": "channel",
            "type": "int",
            "options": [1, 2, 3, 4]
        }
    ]

    def __init__(self, resource_name, channel, max_channel=4, **kwargs):
        check_type(channel, int, 'channel')
        if not 1 <= channel <= max_channel:
            raise ValueError('input channel not exist')
        super(ModelN7744A, self).__init__(resource_name, **kwargs)
        self._is_pos_cal = False
        self.__channel = channel
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
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, value):
        raise AttributeError('attr "channel" is read-only.')

    # Rewrite TypeOPM Methods
    def get_power_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        value_str = self.query(":FETC"+str(self.channel)+":POW?")
        if not value_str:
            raise ValueError('Empty return for get_power_value')
        value = float(value_str)
        return value

    def get_power_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: int, value of (enum 'OpticalUnit') unit of optical power
        """
        unit_int = int(self.query(":SENS" + str(self.channel) + ":POW:UNIT?"))
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
        avg_in_s = float(self.query(":sens" + str(self.channel) + ":pow:atim?"))
        avg_in_ms = avg_in_s*1E+3
        return avg_in_ms

    def get_cal(self):
        """
        :return: (float) calibration offset in dB
        """
        cal_str = self.query(':sens' + str(self.channel) + ':corr?')
        cal = float(cal_str)
        return cal

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query(":sens" + str(self.channel) + ":pow:wav?")
        wl = float(wl_str) * 10 ** 9
        return wl

    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def set_power_unit(self, unit):
        """
        Set optical power unit
        """
        OpticalUnit(unit)  # check if unit is a valid value
        return self.command(":SENS" + str(self.channel) + ":POW:UNIT " + str(unit))

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        check_type(value, (int, float), 'value')
        return self.command(':sens' + str(self.channel) + ':corr ' + str(value) + 'DB')

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_wl, self._max_wl)
        return self.command(":sens" + str(self.channel) + ":pow:wav " + str(value) + "NM")

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
        check_type(value, (int, float), 'value')
        check_range(value, self._min_avg_time, self._max_avg_time)
        return self.command(":sens" + str(self.channel) + ":pow:atim " + str(value) + "MS")