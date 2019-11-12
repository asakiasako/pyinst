from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeVOA
from ..constants import LIGHT_SPEED
from ..utils import check_range, check_type
import math

class Model81571A(VisaInstrument, TypeVOA):
    model = "81571A"
    brand = "Keysight"
    details = {
        "Wavelength Range": "1200~1700 nm",
        "Att Range": "0~60 dB",
        "Att Safe Power": "+33dBm"
    }
    params = [
        {
            "name": "slot",
            "type": "int",
            "options": [1, 3, 5, 6]
        }
    ]

    def __init__(self, resource_name, slot, **kwargs):
        check_type(slot, int, 'slot')
        self.__slot = slot
        super(Model81571A, self).__init__(resource_name, slot, **kwargs)
        self._max_att = 60.0
        self._min_offset = float('-inf')
        self._max_offset = float('inf')
        self._min_wl = 1200.0
        self._max_wl = 1700.0
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000

    # param encapsulation
    @property
    def slot(self):
        return self.__slot

    @slot.setter
    def slot(self, value):
        raise AttributeError('attr "slot" is read-only.')

    # Methods

    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        check_type(status, bool, 'status')
        status_str = str(int(status))
        return self.command(":OUTP" + str(self.slot) + " " + status_str)

    def is_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        status = self.query(":OUTP" + str(self.slot) + "?")
        if status:
            status = bool(int(status))
        return status

    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        att_str = self.query(":INP" + str(self.slot) + ":ATT?")
        att = float(att_str)
        return att

    def get_offset(self):
        """
        Get att offset value in dB.
        :return: (float) att offset value in dB
        """
        offset_str = self.query("INP" + str(self.slot) + ":OFFS?")
        offset = float(offset_str)
        return offset

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query(":INP"+str(self.slot)+":WAV?")
        wl = float(wl_str)*10**9
        return wl

    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def get_cal(self):
        """
        :return: (float) power monitor calibration offset in dB
        """
        cal_str = self.query("OUTP" + str(self.slot) + ":POW:OFFS?")
        cal = float(cal_str)
        return cal

    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        print('ATT: %.2f' % value)
        check_type(value, (int, float), 'value')
        check_range(value, 0, self._max_att)
        return self.command("INP" + str(self.slot) + ":ATT " + str(value) + "dB")

    def set_offset(self, value):
        """
        Set att offset value in dB.
        :param value: (float|int) att offset value in dB
        """
        return self.command("INP"+str(self.slot)+":OFFS "+str(value)+"dB")

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        check_type(value, (float, int), 'value')
        check_range(value, self._min_wl, self._max_wl)
        return self.command(":INP"+str(self.slot)+":WAV " + str(value) + "NM")

    def set_frequency(self, value):
        return self.set_wavelength(round(LIGHT_SPEED/value, 4))

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        return self.command("OUTP" + str(self.slot) + ":POW:OFFS " + str(value))
