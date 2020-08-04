from ._VisaInstrument import VisaInstrument
from ..constants import OpticalUnit, LIGHT_SPEED
from enum import unique, Enum


@unique
class ApplicationType(Enum):
    ATTN = 1
    Sensor = 2


def checkAppType(*app_types):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if self._app_type not in app_types:
                raise AttributeError('This plugin module does not have this application.')
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
        

class ModelAQ2200(VisaInstrument):
    def __init__(self, resource_name, app_type, slot, channel=1, *args, **kwargs):
        # super
        super(ModelAQ2200, self).__init__(resource_name, read_termination='', *args, **kwargs)
        # attributes
        self._app_type = app_type
        self._slot = slot
        self._channel = channel
        # thresholds
        self._min_wl = None
        self._max_wl = None
        self._min_freq = None
        self._max_freq = None
        self._min_avg_time = None
        self._max_avg_time = None
        self._min_cal = None
        self._max_cal = None
        self._max_att = None
        self._min_offset = None
        self._max_offset = None

    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def get_power_value(self):
        '''
        Reads out the currently displayed measurement value.
        The measurement value includes the power offset value.
        :param slot: (int) slot number
        :param channel: (int) channel number
        '''
        pwr_str = self.query(':FETC%d:CHAN%d:POW?' % (self._slot, self._channel))
        if not pwr_str:
            raise ValueError('Empty return for get_power_value')
        return float(pwr_str)

    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def get_power_unit(self):
        if ApplicationType.ATTN == self._app_type:
            return self._get_outp_unit()
        elif ApplicationType.Sensor == self._app_type:
            return self._get_sens_unit()

    def _get_sens_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: int, value of enum 'OpticalUnit', unit of optical power
        """
        unit_int = int(self.query(":SENS%d:CHAN%d:POW:UNIT?" % (self._slot, self._channel)))
        if unit_int == 0:
            unit = OpticalUnit.DBM.value
        elif unit_int == 1:
            unit = OpticalUnit.W.value
        else:
            unit = None
        return unit

    def _get_outp_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: int, value of (enum 'OpticalUnit') unit of optical power
        """
        unit_int = int(self.query(":OUTP%d:CHAN%d:POW:UNIT?" % (self._slot, self._channel)))
        if unit_int == 0:
            unit = OpticalUnit.DBM.value
        elif unit_int == 1:
            unit = OpticalUnit.W.value
        else:
            unit = None
        return unit

    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def get_cal(self):
        if ApplicationType.ATTN == self._app_type:
            return self._get_outp_cal()
        elif ApplicationType.Sensor == self._app_type:
            return self._get_sens_cal()

    def _get_sens_cal(self):
        """
        :return: (float) calibration offset in dB
        """
        cal_str = self.query(':sens%d:chan%d:corr?' % (self._slot, self._channel))
        cal = float(cal_str)
        return cal

    def _get_outp_cal(self):
        """
        :return: (float) calibration offset in dB
        """
        cal_str = self.query(':outp%d:chan%d:pow:offs?' % (self._slot, self._channel))
        cal = float(cal_str)
        return cal

    @ checkAppType(ApplicationType.ATTN, ApplicationType.Sensor)
    def get_wavelength(self):
        if ApplicationType.ATTN == self._app_type:
            return self._get_inp_wavelength()
        elif ApplicationType.Sensor == self._app_type:
            return self._get_sens_wavelength()

    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def _get_sens_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query(":sens%d:chan%d:pow:wav?" % (self._slot, self._channel))
        wl = float(wl_str) * 10 ** 9
        return wl

    def _get_inp_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query(":INP%d:CHAN%d:WAV?" % (self._slot, self._channel))
        wl = float(wl_str)*10**9
        return wl

    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def get_avg_time(self):
        if ApplicationType.ATTN == self._app_type:
            return self._get_outp_avg_time()
        elif ApplicationType.Sensor == self._app_type:
            return self._get_sens_avg_time()

    def _get_sens_avg_time(self):
        """
        set avg time in ms
        """
        result_str = self.query(":sens%d:CHAN%d:pow:atim?" % (self._slot, self._channel))
        value = float(result_str) * 1000
        return value

    def _get_outp_avg_time(self):
        """
        set avg time in ms
        """
        result_str = self.query(":OUTP%d:CHAN%d:atim?" % (self._slot, self._channel))
        value = float(result_str) * 1000
        return value

    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def set_power_unit(self, unit):
        if ApplicationType.ATTN == self._app_type:
            return self._set_outp_unit(unit)
        elif ApplicationType.Sensor == self._app_type:
            return self._set_sens_unit(unit)

    def _set_outp_unit(self, unit):
        """
        Set optical power unit
        """
        OpticalUnit(unit)  # check if unit is a valid value
        return self.command(":OUTP%d:CHAN%d:POW:UNIT " % (self._slot, self._channel) + str(unit))

    def _set_sens_unit(self, unit):
        """
        Set optical power unit
        """
        OpticalUnit(unit)  # check if unit is a valid value
        return self.command(":SENS%d:CHAN%d:POW:UNIT " % (self._slot, self._channel) + str(unit))

    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def set_cal(self, value):
        value = round(value, 3)
        if ApplicationType.ATTN == self._app_type:
            return self._set_outp_cal(value)
        elif ApplicationType.Sensor == self._app_type:
            return self._set_sens_cal(value)

    def _set_outp_cal(self, value):
        """
        Set calibration offset in dB
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Calibration value should be float or int.')
        return self.command(':outp%d:chan%d:pow:offs ' % (self._slot, self._channel) + str(value) + 'DB')

    def _set_sens_cal(self, value):
        """
        Set calibration offset in dB
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Calibration value should be float or int.')
        return self.command(':sens%d:chan%d:corr ' % (self._slot, self._channel) + str(value) + 'DB')
    
    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def set_wavelength(self, value):
        value = round(value, 1)
        if ApplicationType.ATTN == self._app_type:
            return self._set_inp_wavelength(value)
        elif ApplicationType.Sensor == self._app_type:
            return self._set_sens_wavelength(value)

    def set_frequency(self, value):
        return self.set_wavelength(round(LIGHT_SPEED/value, 4))

    def _set_sens_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Wavelength value should be float or int.')
        if not self._min_wl <= value <= self._max_wl:
            raise ValueError('Wavelength value out of range')
        return self.command(":sens%d:chan%d:pow:wav " % (self._slot, self._channel) + str(value) + "NM")

    def _set_inp_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Wavelength value should be float or int.')
        if not self._min_wl <= value <= self._max_wl:
            raise ValueError('Wavelength value out of range')
        return self.command(":INP%d:CHAN%d:WAV " % (self._slot, self._channel) + str(value) + "NM")

    @ checkAppType(ApplicationType.Sensor, ApplicationType.ATTN)
    def set_avg_time(self, value):
        if ApplicationType.ATTN == self._app_type:
            return self._set_outp_avg_time(value)
        elif ApplicationType.Sensor == self._app_type:
            return self._set_sens_avg_time(value)

    def _set_outp_avg_time(self, value):
        """
        set avg time in ms
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Averaging time value should be float or int.')
        if not self._min_avg_time <= value <= self._max_avg_time:
            raise ValueError('Averaging time value out of range.')
        return self.command(":OUTP%d:CHAN%d:atim " % (self._slot, self._channel) + str(value) + "MS")

    def _set_sens_avg_time(self, value):
        """
        set avg time in ms
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Averaging time value should be float or int.')
        if not self._min_avg_time <= value <= self._max_avg_time:
            raise ValueError('Averaging time value out of range.')
        return self.command(":sens%d:CHAN%d:pow:atim " % (self._slot, self._channel) + str(value) + "MS")

    @ checkAppType(ApplicationType.ATTN)
    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        if not isinstance(status, bool):
            raise TypeError('Enable status should be bool')
        status_str = str(int(status))
        return self.command(":OUTP%d:CHAN%d " % (self._slot, self._channel) + status_str)

    @ checkAppType(ApplicationType.ATTN)
    def disable(self):
        """
        Set VOA output disabled.
        """
        return self.enable(False)

    @ checkAppType(ApplicationType.ATTN)
    def is_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        status = self.query(":OUTP%d:CHAN%d?" % (self._slot, self._channel))
        if status:
            status = bool(int(status))
        return status

    @ checkAppType(ApplicationType.ATTN)
    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        att_str = self.query(":INP%d:CHAN%d:ATT?" % (self._slot, self._channel))
        att = float(att_str)
        return att

    @ checkAppType(ApplicationType.ATTN)
    def get_offset(self):
        """
        Get att offset value in dB.
        :return: (float) att offset value in dB
        """
        offset_str = self.query("INP%d:CHAN%d:OFFS?" % (self._slot, self._channel))
        offset = float(offset_str)
        return offset

    @ checkAppType(ApplicationType.ATTN)
    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        value = round(value, 3)
        print('ATT: %.f' % value)
        if not isinstance(value, (int, float)):
            raise TypeError('Att value should be float or int.')
        if not 0 <= value <= self._max_att:
            raise ValueError('Averaging time value out of range.')
        return self.command(":INP%d:CHAN%d:ATT " % (self._slot, self._channel) + str(value) + "dB")

    @ checkAppType(ApplicationType.ATTN)
    def set_offset(self, value):
        """
        Set att offset value in dB.
        :param value: (float|int) att offset value in dB
        """
        value = round(value, 3)
        return self.command(":INP%d:CHAN%d:OFFS " % (self._slot, self._channel) + str(value) + "dB")
