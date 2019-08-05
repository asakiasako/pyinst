from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypePOLC
from ..utils import check_range, check_type
from ..constants import LIGHT_SPEED


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
        check_type(wavelength, (int, float), 'wavelength')
        check_range(wavelength, 1480, 1620)
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
                check_range(rate, 0.01, 20000)
            else:
                check_range(rate, 0.01, 2000)
        else:
            check_range(rate, 0.01, 2000)
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
            check_type(i, (int, float), 's1, s2, s3')
        return self.command(':CONT:SOP %.2f,%.2f,%.2f' % (s1, s2, s3))

    def set_sop_in_degree(self, theta, phi):
        """
        :param theta: (float) 0 to 360
        :param phi: (float) 0 to 180
        """
        for i in (theta, phi):
            check_type(i, (int, float), 'theta, phi')
        check_range(theta, 0, 360)
        check_range(phi, 0, 180)
        return self.command(':CONT:ANGL %.2f,%.2f' % (theta, phi))