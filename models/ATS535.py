from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypeTS
from ..utils import int_to_complement, complement_to_int, calc_check_sum
from ..constants import TemperatureUnit
import serial
import time


class ModelATS535(VisaInstrument, TypeTS):
    model = "ATS-535"
    brand = "Temptronic"

    def __init__(self, resource_name, read_termination='\r\n', **kwargs):
        super(ModelATS535, self).__init__(resource_name, read_termination=read_termination, **kwargs)
        self._ts_type = 'ThermoStream'
    
    def head_up(self):
        return self.command('HEAD 0')

    def head_down(self):
        return self.command('HEAD 1')

    def is_head_down(self):
        r = self.query('HEAD?')
        return bool(int(r))

    def get_dut_mode(self):
        r = self.query('DUTM?')
        return bool(int(r))

    def set_dut_mode(self, t_f):
        t = int(t_f)
        return self.command('DUTM %d' % t)

    def rst_operator(self):
        """
        Reset the system to the Operator screen
        """
        self.command('RSTO')
        time.sleep(0.3)

    def set_n(self, n):
        return self.command('SETN %d' % n)

    def set_p(self, p):
        return self.command('SETP %.1f' % p)
    
    def get_set_p(self):
        r = self.query('SETP?')
        return float(r)
    
    def set_ramp(self, ramp):
        if 0<= ramp <= 99.9:
            t = '%.1f' % ramp
        elif 99.9 < ramp <= 9999:
            t = '%d' % round(ramp)
        else:
            raise ValueError('ramp out of range')
        return self.command('RAMP %s' % t)

    def set_target_temp(self, value):
        """
        Set the target Temperature.
        :param value: <float|int> target temperature value
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Target temperature should be number')
        if value < 20:
            n = 2
        elif 20<= value <= 30:
            n = 1
        else:
            n = 0
        self.set_n(n)
        self.set_p(value)

    def get_target_temp(self):
        """
        Get the target Temperature
        :return: <float> target temperature value
        """
        return self.get_set_p()

    def get_current_temp(self):
        """
        Get the current measured temperature
        :return: <float> current measured temperature
        """
        r = self.query('TEMP?')
        temp = float(r)
        if temp > 400:
            raise ValueError('invalid current temperature.')
        return temp


    def set_unit(self, unit):
        """
        Set temperature unit
        :param unit: int, value of enum <TemperatureUnit> unit
        F=0 C=1
        """
        if unit == 1:
            return
        else:
            raise ValueError('temperature unit of this device is fixed to °C')

    def get_unit(self):
        """
        Get temperature unit
        :return: int, value of <TemperatureUnit> unit
        """
        return 1
