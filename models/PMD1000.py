from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypePMDE
from ..constants import LIGHT_SPEED
import math


class ModelPMD1000(VisaInstrument, TypePMDE):
    model = "PMD-1000"
    brand = "General Photonics"
    details = {
        "Wavelength Range": "C Band",
        "Insertion Loss": "5.5 dB",
        "1st Order PMD Range": "0.36 to 182.4 ps",
        "2nd Order PMD Range": "8100 ps2"
    }

    def __init__(self, resource_name, write_termination='', read_termination='#', **kwargs):
        super(ModelPMD1000, self).__init__(
            resource_name, write_termination=write_termination, read_termination=read_termination, **kwargs
        )
        # thresholds
        self._min_freq = 191.6
        self._max_freq = 191.6 + (96-1)*0.05 # 96 channels
        self._min_wl = math.floor(LIGHT_SPEED*1000/self._max_freq)/1000 + 0.001
        self._max_wl = math.floor(LIGHT_SPEED*1000/self._min_freq)/1000

    def _formatted_query(self, cmd):
        return self.query(cmd)[1:]

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (float, int) wavelength in nm
        """
        return self.set_frequency(round(LIGHT_SPEED/wavelength, 4))

    def set_frequency(self, freq):
        ch = round((freq - 191.6)/0.05)+1
        return self.command('*CHC %03d#' % ch)

    def get_wavelength(self):
        return LIGHT_SPEED/self.get_frequency()

    def get_frequency(self):
        ch_str = self.query('*CHA?')
        # *C012#
        if ch_str[0] != 'C':
            raise ValueError('Unexpected Reply')
        ch = int(ch_str[1:])
        freq = 191.6 + (ch-1)*0.05
        return freq

    def set_pmd_value(self, pmd, sopmd):
        """
        Set pmd (dgd) and sopmd target (ps, ps**2)
        :param pmd: (float, int) DGD value in ps
        :param sopmd: (float, int) 2nd order pmd in ps**2
        """
        if not (isinstance(pmd, (float, int)) and isinstance(sopmd, (float, int))):
            raise TypeError('Param pmd and sopmd should be number')
        if not 0.36 <= pmd <= 182.4:
            raise ValueError('Param pmd out of range')
        if not 0 <= sopmd <= 8319.9:
            raise ValueError('Param sopmd out of range')
        return self.command('*PMD:CON %.2f,%.2f#' % (pmd, sopmd))
