from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeVOA
from .N7744A import ModelN7744A
from ..utils import check_range, check_type

class ModelN7752A(ModelN7744A, TypeVOA):
    model = "N7752A"
    details = {
        "Wavelength Range": "1260~1640 nm",
        "Att Range": "0~40 dB",
        "Att Safe Power": "+23dBm",
        "PM Power Range": "-80 ~ +10 dBm",
        "PM Safe Power": "+16 dBm",
        "AVG Time": "2 ms ~ 10 s"
    }
    params = [
        {
            "name": "channel",
            "type": "int",
            "options": [1, 3, 5, 6]
        }
    ]

    def __init__(self, resource_name, channel, max_channel=6, **kwargs):
        super(ModelN7752A, self).__init__(resource_name, channel, max_channel, **kwargs)
        self._max_att = 45.0
        self._min_avg_time = 2

    # param encapsulation

    # Methods
    def __is_att(self):
        if self.channel in (1, 2, 3, 4):
            return True
        else:
            return False

    def __check_is_att(self):
        if not self.__is_att():
            raise ValueError('channel '+str(self.channel)+' has no att function.')

    def get_max_att(self):
        """
        Get the max att setting value
        :return: (float) max att setting value
        """
        return self._max_att

    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        self.__check_is_att()
        check_type(status, bool, 'status')
        status_str = str(int(status))
        return self.command(":OUTP" + str(self.channel) + " " + status_str)

    def is_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        self.__check_is_att()
        status = self.query(":OUTP" + str(self.channel) + "?")
        if status:
            status = bool(int(status))
        return status

    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        self.__check_is_att()
        att_str = self.query(":INP" + str(self.channel) + ":ATT?")
        att = float(att_str)
        return att

    def get_offset(self):
        """
        Get att offset value in dB.
        :return: (float) att offset value in dB
        """
        self.__check_is_att()
        offset_str = self.query("INP" + str(self.channel) + ":OFFS?")
        offset = float(offset_str)
        return offset

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        if self.channel >= 5:
            return ModelN7744A.get_wavelength(self)
        wl_str = self.query(":INP"+str(self.channel)+":WAV?")
        wl = float(wl_str)*10**9
        return wl

    def get_cal(self):
        """
        :return: (float) power monitor calibration offset in dB
        """
        if self.channel >= 5:
            return ModelN7744A.get_cal(self)
        cal_str = self.query("OUTP" + str(self.channel) + ":POW:OFFS?")
        cal = float(cal_str)
        return cal

    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        self.__check_is_att()
        print('ATT: %.2f' % value)
        check_type(value, (int, float), 'value')
        check_range(value, 0, self._max_att)
        return self.command("INP" + str(self.channel) + ":ATT " + str(value) + "dB")

    def set_offset(self, value):
        """
        Set att offset value in dB.
        :param value: (float|int) att offset value in dB
        """
        self.__check_is_att()
        return self.command("INP"+str(self.channel)+":OFFS "+str(value)+"dB")

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        if self.channel >= 5:
            return ModelN7744A.set_wavelength(self, value)
        check_type(value, (float, int), 'value')
        check_range(value, self._min_wl, self._max_wl)
        return self.command(":INP"+str(self.channel)+":WAV " + str(value) + "NM")

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        if self.channel >= 5:
            return ModelN7744A.set_cal(self, value)
        return self.command("OUTP" + str(self.channel) + ":POW:OFFS " + str(value))
