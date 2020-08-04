from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypePOLC
from ..constants import LIGHT_SPEED
import math


class ModelMPC202(VisaInstrument, TypePOLC):
    model = "MPC-202"
    brand = "General Photonics"
    details = {
        'Wavelength Range': '1260-1650 nm',
        'Scrambling Types': 'Discrete, Tornado, Rayleigh, Triangle',
        'Tornado Rate': '0 to 60,000 Rev/s',
        'Rayleigh Rate': '0 to 2000 rad/s',
        'Triangle Rate': '0 to 2000 × 2π rad/s',
        'Discrete Rate': '0 to 20,000 points/s'
    }

    def __init__(self, resource_name, write_termination='\r\n', read_termination='\r\n', **kwargs):
        super(ModelMPC202, self).__init__(
            resource_name, write_termination=write_termination, read_termination=read_termination, **kwargs
        )
        # thresholds
        self._min_wl = 1260
        self._max_wl = 1650
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
    
    def get_wavelength(self):
        """
        Get current wavelength setting (nm)
        :return: (float) wavelength
        """
        return float(self.query(':CONF:WLEN?'))

    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (float, int) wavelength in nm
        """
        if not isinstance(wavelength, (float, int)):
            raise TypeError('Wavelength value should be number')
        if not self.min_wavelength <= wavelength <= self.max_wavelength:
            raise ValueError('Wavelength value out of range')
        return self.command(':CONF:WLEN %.1f' % wavelength)

    def set_frequency(self, freq):
        return self.set_wavelength(LIGHT_SPEED/freq)
    
    def set_scrambling_param(self, mode, *params):
        """
        Set scrambling params.
        :param mode: (str) Scrambling mode: DISCrete | TRIangle | RAYLeigh | TORNado
        :param params: (any, any, ...) Scrambling params.

        'Tornado Rate': '0 to 60,000 Rev/s',
        'Rayleigh Rate': '0 to 2000 rad/s',
        'Triangle Rate': '0 to 2000 × 2π rad/s',
        'Discrete Rate': '0 to 20,000 points/s'
        """
        rate = params[0]
        if len(mode) >= 4:
            if mode[0:4].upper() == 'TORN':
                if not 0 <= rate <= 60000:
                    raise ValueError('Parameter rate is out of range')
            elif mode[0:4].upper() == 'DISC':
                if not 0 <= rate <= 20000:
                    raise ValueError('Parameter rate is out of range')
            else:
                if not 0 <= rate <= 2000:
                    raise ValueError('Parameter rate is out of range')
        else:
            if not 0 <= rate <= 2000:
                raise ValueError('Parameter rate is out of range')
        self.command(':%s:RATE %.1f' % (mode, rate))
        if mode[0:4].upper() == 'TORN':
            type = params[1]
            self.command(':TORNado:TYPE %d' % type)
    
    def set_scrambling_state(self, mode, is_on):
        """
        Start or pause scrambling.
        :param mode: (str) Scrambling mode: DISCrete | TRIangle | RAYLeigh | TORNado
        :param ison: (bool) True->start  False->stop
        """
        state_str = 'ON' if is_on else 'OFF'
        return self.command(':%s:STAT %s' % (mode, state_str))
    