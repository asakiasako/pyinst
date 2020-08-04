from ..instrument_types import TypeVOA, TypeOPM
from ..base_models._VisaInstrument import VisaInstrument
from ..constants import LIGHT_SPEED, OpticalUnit
from ..utils import dbm_to_w
import math


class ModelMAP200_mVoaC1(VisaInstrument, TypeVOA, TypeOPM):
    model = "MAP-200 mVoaC1"
    details = {
        "Wavelength Range": "1260~1650 nm",
        "Att Range": "70 dB",
        "Maximum Input Power": "+23dBm"
    }
    params = [
        {
            "name": "channel",
            "type": "int",
            "options": [1, 2, 3, 4]
        }
    ]

    def __init__(self, resource_name, channel, **kwargs):
        super(ModelMAP200_mVoaC1, self).__init__(resource_name, **kwargs)
        self.__channel = channel
        # thresholds
        self._min_wl = 1260
        self._max_wl = 1650
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
        self._max_att = 70
        self._min_offset = -200
        self._max_offset = 200
        self._min_avg_time = 2
        self._max_avg_time = 5000
        self._min_cal = -200
        self._max_cal = 200

    # -- methods --
    def enable(self, status=True):
        """
        Enable/disable VOA output.

        :Parameters: **status** - bool, True(default) -> enable, False -> disable
        """
        beam_block = not status
        cmd = ':OUTPut:BBLock {ch:d},{state:d}'.format(ch=self.__channel, state=beam_block)
        self.command(cmd)

    def is_enabled(self):
        """
        If VOA output is enabled.

        :Returns: bool, if VOA output is enabled.
        """
        cmd = ':OUTPut:BBLock? {ch:d}'.format(ch=self.__channel)
        beam_block = bool(int(self.query(cmd)))
        enabled = not beam_block
        return enabled

    def get_att(self):
        """
        Get ATT setting value in dB.

        :Returns: float, att value in dB.
        """
        cmd = ':OUTPut:ATTenuation? {ch:d}'.format(ch=self.__channel)
        att = float(self.query(cmd))
        return att

    def get_offset(self):
        """
        Get ATT offset value in dB.

        :Returns: float, offset value in dB.
        """
        cmd = ':OUTPut:POWer:OFFSet? {ch:d}'.format(ch=self.__channel)
        offset = float(self.query(cmd))
        return offset

    def get_wavelength(self):
        """
        :Returns: float, optical wavelength in nm
        """
        cmd = ':OUTPut:WAVelength? {ch:d}'.format(ch=self.__channel)
        wl = float(self.query(cmd))
        return wl
    
    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def set_att(self, value):
        """
        Set att value in dB.

        :Parameters: **value** - float|int, att value in dB.
        """
        if not 0 <= value <= self.max_att:
            raise ValueError('ATT value out of range.')
        cmd = ':OUTPut:ATTenuation {ch:d},{att:.4f}'.format(ch=self.__channel, att=value)
        self.command(cmd)

    def set_offset(self, value):
        """
        Set ATT offset value in dB.

        :Parameters: **value** - float|int, offset value in dB
        """
        if not self.min_offset <= value <= self.max_offset:
            raise ValueError('Att offset out of range.')
        cmd = ':OUTPut:POWer:OFFSet {ch:d},{offset:.4f}'.format(ch=self.__channel, offset=value)
        self.command(cmd)

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.

        :Parameters: **value** - float|int, wavelength value in nm.
        """
        if not self.min_wavelength <= value <= self.max_wavelength:
            raise ValueError('Wavelength out of range.')
        cmd = ':OUTPut:WAVelength {ch:d},{wl:.4f}'.format(ch=self.__channel, wl=value)
        self.command(cmd)

    def set_frequency(self, value):
        return self.set_wavelength(round(LIGHT_SPEED/value, 4))

    # -- methods --
    def get_power_value(self):
        """
        The value of measured optical power, note that the power unit is not certain.

        :Returns: float, value of optical power
        """
        cmd = ':FETch:POWer:OUTPut? {ch:d}'.format(ch=self.__channel)
        raw = self.query(cmd)
        if raw.startswith('-') and raw.endswith('-'):
            dbm_value = -100
        elif raw.startswith('+') and raw.endswith('+'):
            raise ValueError('OPM sensor value overload.')
        else:
            dbm_value = float(raw)
        return dbm_value

    def get_power_unit(self):
        """
        The unit of measured optical power.

        :Return Type: int, value of enum 'OpticalUnit'
        """
        return OpticalUnit.DBM.value

    def get_cal(self):
        """
        :Returns: float, calibration offset in dB
        """
        cmd = ':SENSe:POWer:OFFSet? {ch:d}'.format(ch=self.__channel)
        cal = float(self.query(cmd))
        return cal

    def get_avg_time(self):
        """
        Get averaging time in ms.
        """
        cmd = ':SENSe:POWer:ATIMe? {ch:d}'.format(ch=self.__channel)
        atime = float(self.query(cmd))
        return atime

    def set_power_unit(self, unit):
        """
        Set optical power unit.

        :Parameters: **unit** - int, value of <enum 'OpticalUnit'>, optical power unit
        """
        if unit == OpticalUnit.DBM.value:
            return
        else:
            raise ValueError('Optical Unit of mVoaC1 is fixed as dBm.')

    def set_cal(self, value): 
        """
        Set calibration offset in dB.

        :Parameters: **value** - float|int, calibration offset in dB.
        """
        if not self.min_cal <= value <= self.max_cal:
            raise ValueError('OPM Calibration out of range')
        cmd = ':SENSe:POWer:OFFSet {ch:d},{offset:.4f}'.format(ch=self.__channel, offset=value)
        self.command(cmd)

    def set_avg_time(self, value):
        """
        Set averaging time in ms.

        :Parameters: **value** - averaging time in ms.
        """
        if not self.min_avg_time <= value <= self.max_avg_time:
            raise ValueError('Averaging time out of range')
        cmd = ':SENSe:POWer:ATIMe {ch:d},{atime:.4f}'.format(ch=self.__channel, atime=value)
        self.command(cmd)