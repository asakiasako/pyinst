from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOPM
from ..utils import check_range, check_type
from ..constants import OpticalUnit


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
        self._max_wl = 1640.0
        self._min_wl = 1260.0
        self._min_avg_time = 0.001
        self._max_avg_time = 10000

    # param encapsulation
    @property
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, value):
        raise AttributeError('attr "channel" is read-only.')

    # Rewrite TypeOPM Methods
    def get_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        value_str = self.query(":FETC"+str(self.channel)+":POW?")
        if not value_str:
            raise ValueError('Empty return for get_value')
        value = float(value_str)
        return value

    def get_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: (enum 'OpticalUnit') unit of optical power
        """
        unit_int = int(self.query(":SENS" + str(self.channel) + ":POW:UNIT?"))
        if unit_int == 0:
            unit = OpticalUnit.DBM
        elif unit_int == 1:
            unit = OpticalUnit.W
        else:
            unit = None
        return unit

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

    def set_unit(self, unit):
        """
        Set optical power unit
        """
        check_type(unit, OpticalUnit, 'unit')
        return self.command(":SENS" + str(self.channel) + ":POW:UNIT " + str(unit.value))

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