from .ins_base import *
from .ins_types import *


class ModelAQ2200(VisaInstrument):
    def __init__(self, resource_name, slot, channel=None, **kwargs):
        check_type(slot, int, 'slot')
        check_type(channel, int, 'channel')
        super(ModelAQ2200, self).__init__(resource_name, **kwargs)
        self._slot = slot
        self._channel = channel
        self._min_wl = None
        self._max_wl = None
        self._min_avg_time = None
        self._max_avg_time = None
        self._max_att = None

        if self._channel is None:
            self.__ch_str = ''
        else:
            self.__ch_str = ':CHAN%d' % self._channel

    def _fec_sens_power(self):
        '''
        Reads out the currently displayed measurement value.
        The measurement value includes the power offset value.
        :param slot: (int) slot number
        :param channel: (int) channel number
        '''
        pwr_str = self.query(':FETC%d%s:POW?' % (self._slot, self.__ch_str))
        if not pwr_str:
            raise ValueError('Empty return for get_value')
        return float(pwr_str)

    def _get_sens_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: (enum 'OpticalUnit') unit of optical power
        """
        unit_int = int(self.query(":SENS%d%s:POW:UNIT?" % (self._slot, self.__ch_str)))
        if unit_int == 0:
            unit = OpticalUnit.DBM
        elif unit_int == 1:
            unit = OpticalUnit.W
        else:
            unit = None
        return unit

    def _get_sens_cal(self):
        """
        :return: (float) calibration offset in dB
        """
        cal_str = self.query(':sens%d%s:corr?' % (self._slot, self.__ch_str))
        cal = float(cal_str)
        return cal

    def _get_sens_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query(":sens%d%s:pow:wav?" % (self._slot, self.__ch_str))
        wl = float(wl_str) * 10 ** 9
        return wl

    def _set_sens_unit(self, unit):
        """
        Set optical power unit
        """
        check_type(unit, OpticalUnit, 'unit')
        return self.command(":SENS%d%s:POW:UNIT " % (self._slot, self.__ch_str) + str(unit.value))

    def _set_sens_cal(self, value):
        """
        Set calibration offset in dB
        """
        check_type(value, (int, float), 'value')
        return self.command(':sens%d%s:corr ' % (self._slot, self.__ch_str) + str(value) + 'DB')

    def _set_sens_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_wl, self._max_wl)
        return self.command(":sens%d%s:pow:wav " % (self._slot, self.__ch_str) + str(value) + "NM")

    def _set_sens_avg_time(self, value):
        """
        set avg time in ms
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_avg_time, self._max_avg_time)
        return self.command(":sens%d%s:pow:atim " % (self._slot, self.__ch_str) + str(value) + "MS")

    def _get_max_att(self):
        """
        Get the max att setting value
        :return: (float) max att setting value
        """
        if not self._max_att:
            raise AttributeError('_max_att has no value.')

    def _outp_enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        check_type(status, bool, 'status')
        status_str = str(int(status))
        return self.command(":OUTP%d%s " % (self._slot, self.__ch_str) + status_str)

    def _outp_disable(self):
        """
        Set VOA output disabled.
        """
        return self.enable(False)

    def _is_outp_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        status = self.query(":OUTP%d%s?" % (self._slot, self.__ch_str))
        if status:
            status = bool(int(status))
        return status

    def _get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        att_str = self.query(":INP%d%s:ATT?" % (self._slot, self.__ch_str))
        att = float(att_str)
        return att

    def _get_inp_offset(self):
        """
        Get att offset value in dB.
        :return: (float) att offset value in dB
        """
        offset_str = self.query("INP%d%s:OFFS?" % (self._slot, self.__ch_str))
        offset = float(offset_str)
        return offset

    def _get_inp_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query(":INP%s%d:WAV?" % (self._slot, self.__ch_str))
        wl = float(wl_str)*10**9
        return wl

    def _get_outp_cal(self):
        """
        :return: (float) power monitor calibration offset in dB
        """
        cal_str = self.query("OUTP%s%d:POW:OFFS?" % (self._slot, self.__ch_str))
        cal = float(cal_str)
        return cal

    def _set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        print('ATT: %.2f' % value)
        check_type(value, (int, float), 'value')
        check_range(value, 0, self._max_att)
        return self.command("INP%s%d:ATT " % (self._slot, self.__ch_str) + str(value) + "dB")

    def _set_inp_offset(self, value):
        """
        Set att offset value in dB.
        :param value: (float|int) att offset value in dB
        """
        return self.command("INP%d%s:OFFS " % (self._slot, self.__ch_str) + str(value) + "dB")

    def _set_inp_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        check_type(value, (float, int), 'value')
        check_range(value, self._min_wl, self._max_wl)
        return self.command(":INP%d%s:WAV " % (self._slot, self.__ch_str) + str(value) + "NM")

    def _set_outp_cal(self, value):
        """
        Set calibration offset in dB
        """
        return self.command("OUTP%d%s:POW:OFFS " % (self._slot, self.__ch_str) + str(value))