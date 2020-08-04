from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypePOLC
from ..constants import LIGHT_SPEED
import math


class ModelPSY201(VisaInstrument, TypePOLC):
    model = "PSY-201"
    brand = "General Photonics"
    details = {
        "Wavelength Range": "1480-1620 nm",
        "Operating power range": "-35 to 10 dBm"
    }

    def __init__(self, resource_name, write_termination='\r\n', read_termination='\r\n', **kwargs):
        super(ModelPSY201, self).__init__(
            resource_name, write_termination=write_termination, read_termination=read_termination, **kwargs
        )
        # thresholds
        self._min_wl = 1480
        self._max_wl = 1620
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
            raise TypeError('wavelength should be number')
        if not self.min_wavelength <= wavelength <= self.max_wavelength:
            raise ValueError('wavelength out of range')
        wavelength = int(wavelength)
        return self.command(':CONF:WLEN %d' % wavelength)

    def set_frequency(self, freq):
        return self.set_wavelength(LIGHT_SPEED/freq)
    
    def set_scrambling_param(self, mode, *params):
        """
        Set scrambling params.
        :param mode: (str) Scrambling mode: DISCrete | TRIangle | TORNado
        :param params: (any, any, ...) Scrambling params.
        """
        rate = params[0]
        if len(mode) >= 4:
            if mode[0:4].upper() == 'DISC':
                if not 0.01 <= rate <= 20000:
                    raise ValueError('Param rate out of range')
            else:
                if not 0.01 <= rate <= 2000:
                    raise ValueError('Param rate out of range')
        else:
            if not 0.01 <= rate <= 2000:
                raise ValueError('Param rate out of range')
        self.command(':CONT:SCR:%s:RATE %.2f' % (mode, rate))
        if mode[0:4].upper() == 'TORN':
            type = params[1]
            self.command(':CONT:SCR:TORN:TYPE %d' % type)
    
    def set_scrambling_state(self, mode, is_on):
        """
        Start or pause scrambling.
        :param mode: (str) Scrambling mode.
        :param ison: (bool) True->start  False->stop
        """
        state_str = '1' if is_on else '0'
        return self.command(':CONT:SCR:%s:STAT %s' % (mode, state_str))

    def get_sop(self):
        """
        Get state of polarization, S1 S2 S3
        :return (S1, S2, S3)
        """
        sop_str = self.query(':MEAS:SOP?')
        return tuple((float(i) for i in sop_str.split(',')))

    def get_dop(self):
        """
        Query measured degree of polarization.
        """
        return float(self.query(':MEAS:DOP?'))

    def set_sop(self, s1, s2, s3):
        for i in (s1, s2, s3):
            if not isinstance(i, (int, float)):
                raise TypeError('Parameters s1, s2, s3 should be number')
        return self.command(':CONT:SOP %.2f,%.2f,%.2f' % (s1, s2, s3))

    def set_sop_in_degree(self, theta, phi):
        """
        :param theta: (float) 0 to 360
        :param phi: (float) 0 to 180
        """
        for i in (theta, phi):
            if not isinstance(i, (int, float)):
                raise TypeError('Parameters theta, phi should be number')
        if not 0 <= theta <= 360:
            raise ValueError('Parameter theta out of range')
        if not 0 <= phi <= 180:
            raise ValueError('Parameter phi out of range')
        return self.command(':CONT:ANGL %.2f,%.2f' % (theta, phi))