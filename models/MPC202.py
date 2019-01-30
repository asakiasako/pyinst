from ..model_bases.ins_base import *
from ..model_bases.ins_types import *


class ModelMPC202(VisaInstrument, TypePOLC):
    model = "MPC-202"
    brand = "General Photonics"
    detail = {
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
    
    def get_wavelength(self):
        """
        Get current wavelength setting (nm)
        :return: (float) wavelength
        """
        return float(self.query(':CONF:WLEN?'))

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (float, int) wavelength in nm
        """
        check_type(wavelength, (int, float), wavelength)
        check_range(wavelength, 1260, 1650)
        return self.command(':CONF:WLEN %.1f' % wavelength)
    
    def set_scrambling_param(self, mode, *params):
        """
        Set scrambling params.
        :param mode: (str) Scrambling mode: DISCrete | TRIangle | RAYLeigh | TORNado
        :param *params: (any, any, ...) Scrambling params.

        'Tornado Rate': '0 to 60,000 Rev/s',
        'Rayleigh Rate': '0 to 2000 rad/s',
        'Triangle Rate': '0 to 2000 × 2π rad/s',
        'Discrete Rate': '0 to 20,000 points/s'
        """
        rate = params[0]
        if len(mode) >= 4:
            if mode[0:4].upper() == 'TORN':
                check_range(rate, 0, 60000)
            elif mode[0:4].upper() == 'DISC':
                check_range(rate, 0, 20000)
            else:
                check_range(rate, 0, 2000)
        else:
            check_range(rate, 0, 2000)
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
    