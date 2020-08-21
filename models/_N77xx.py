from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOPM
from ..constants import OpticalUnit, LIGHT_SPEED
import math

class ModelN77xx(VisaInstrument):

    def __init__(self, resource_name, slot, max_slot, slot_type_define, **kwargs):
        if not isinstance(slot, int):
            raise TypeError('Parameter slot should be int')
        if not 1 <= slot <= max_slot:
            raise ValueError('slot out of range.')
        for slot_type, slots in slot_type_define.items():
            if slot in slots:
                self.__slot_type = slot_type
                break
        else:
            raise ValueError('Missing slot_type_define for slot: {slot:r}'.format(slot=slot))
        super(ModelN77xx, self).__init__(resource_name, **kwargs)
        self._is_pos_cal = False
        self.__slot = slot

    # param encapsulation
    @property
    def slot(self):
        return self.__slot

    @slot.setter
    def slot(self, value):
        raise AttributeError('attr "slot" is read-only.')

    def __check_is_voa(self):
        if not self.__slot_type in ['voa', 'voa_with_opm']:
            raise AttributeError('Slot {slot} of {model} has no VOA function.'.format(slot=self.slot, model=self.model))

    def __check_is_opm(self):
        if not self.__slot_type in ['voa_with_opm', 'opm']:
            raise AttributeError('Slot {slot} of {model} has no OPM function.'.format(slot=self.slot, model=self.model))

    # Rewrite TypeOPM Methods
    def get_power_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        self.__check_is_opm()
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
        self.__check_is_opm()
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
        self.__check_is_opm()
        avg_in_s = float(self.query(":sens" + str(self.slot) + ":pow:atim?"))
        avg_in_ms = avg_in_s*1E+3
        return avg_in_ms

    def set_power_unit(self, unit):
        """
        Set optical power unit
        """
        self.__check_is_opm()
        OpticalUnit(unit)  # check if unit is a valid value
        return self.command(":SENS" + str(self.slot) + ":POW:UNIT " + str(unit))

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
        self.__check_is_opm()
        if not isinstance(value, (float, int)):
            raise TypeError('Averaging time should be number')
        if not self.min_avg_time <= value <= self.max_avg_time:
            raise ValueError('Averaging time out of range')
        return self.command(":sens" + str(self.slot) + ":pow:atim " + str(value) + "MS")

    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        self.__check_is_voa()
        if not isinstance(status, bool):
            raise TypeError('Enable status should be bool')
        status_str = str(int(status))
        return self.command(":OUTP" + str(self.slot) + " " + status_str)

    def is_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        self.__check_is_voa()
        status = self.query(":OUTP" + str(self.slot) + "?")
        if status:
            status = bool(int(status))
        return status

    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        self.__check_is_voa()
        att_str = self.query(":INP" + str(self.slot) + ":ATT?")
        att = float(att_str)
        return att

    def get_offset(self):
        """
        Get att offset value in dB.
        :return: (float) att offset value in dB
        """
        self.__check_is_voa()
        offset_str = self.query("INP" + str(self.slot) + ":OFFS?")
        offset = float(offset_str)
        return offset

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        if self.__slot_type == 'opm':
            wl_str = self.query(":sens" + str(self.slot) + ":pow:wav?")
            wl = float(wl_str) * 10 ** 9
        else:
            wl_str = self.query(":INP"+str(self.slot)+":WAV?")
            wl = float(wl_str)*10**9
        return wl

    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def get_cal(self):
        """
        :return: (float) power monitor calibration offset in dB
        """
        self.__check_is_opm()
        if self.__slot_type == 'opm':
            cal_str = self.query(':sens' + str(self.slot) + ':corr?')
            cal = float(cal_str)
        else:
            cal_str = self.query("OUTP" + str(self.slot) + ":POW:OFFS?")
            cal = float(cal_str)
        return cal

    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        self.__check_is_voa()
        if not isinstance(value, (float, int)):
            raise TypeError('Att value should be number')
        if not 0 <= value <= self.max_att:
            raise ValueError('Att value out of range')
        return self.command("INP" + str(self.slot) + ":ATT " + str(value) + "dB")

    def set_offset(self, value):
        """
        Set att offset value in dB.
        :param value: (float|int) att offset value in dB
        """
        self.__check_is_voa()
        return self.command("INP"+str(self.slot)+":OFFS "+str(value)+"dB")

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """            
        if not isinstance(value, (int, float)):
            raise TypeError('Wavelength value should be number')
        if not self.min_wavelength <= value <= self.max_wavelength:
            raise ValueError('Wavelength value out of range')
        if self.__slot_type == 'opm':
            self.command(":sens" + str(self.slot) + ":pow:wav " + str(value) + "NM")
        else:
            self.command(":INP"+str(self.slot)+":WAV " + str(value) + "NM")

    def set_frequency(self, value):
        return self.set_wavelength(round(LIGHT_SPEED/value, 4))

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        self.__check_is_opm()
        if not isinstance(value, (float, int)):
            raise TypeError('Calibration value should be numbwer')
        if self.__slot_type == 'opm':
            self.command(':sens' + str(self.slot) + ':corr ' + str(value) + 'DB')
        else:
            self.command("OUTP" + str(self.slot) + ":POW:OFFS " + str(value))
