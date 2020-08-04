from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypePDLE
from ..constants import LIGHT_SPEED
import pyvisa
import math


class ModelPDLE101(VisaInstrument, TypePDLE):
    model = "PDLE-101"
    brand = "General Photonics"
    details = {
        "Wavelength Range": "1520~1570 nm",
        "Insertion Loss (Max.)": "3 dB at PDL=0",
        "PDL Range": "0.1 to 20 dB",
        "PDL Resolution": "0.1 dB",
        "PDL Accuracy": "2 ± (0.1 dB +1% of PDL)"
    }

    def __init__(self, resource_name, write_termination='', read_termination='#', **kwargs):
        if resource_name.startswith('COM'):
            super(ModelPDLE101, self).__init__(
                resource_name, write_termination=write_termination, read_termination=read_termination, baud_rate=9600, data_bits=8,
                 flow_control=0, parity=pyvisa.constants.Parity.none, stop_bits=pyvisa.constants.StopBits.one, **kwargs
            )
        else:
            super(ModelPDLE101, self).__init__(
                resource_name, write_termination=write_termination, read_termination=read_termination, **kwargs
            )
        # thresholds
        self._min_wl = 1520
        self._max_wl = 1570
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000

    def _formatted_query(self, cmd):
        return self.query(cmd)[1:]
    
    def get_wavelength(self):
        """
        Get current wavelength setting (nm)
        :return: (float) wavelengthwavelength
        """
        wl_str = self._formatted_query('*WAV?')
        return float(wl_str)

    def get_frequency(self):
        return LIGHT_SPEED/self.get_wavelength()

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (int) wavelength in nm
        """
        if not isinstance(wavelength, (int, float)):
            raise TypeError('Param wavelength should be number')
        if not self.min_wavelength <= wavelength <= self.max_wavelength:
            raise ValueError('Param wavelength out of range')
        wavelength = round(wavelength)
        backcode = self._formatted_query('*WAV %d#' % wavelength)
        if backcode != 'E00':
            raise pyvisa.Error('PDLE-101 Error: %s' % backcode)

    def set_frequency(self, freq):
        return self.set_wavelength(round(LIGHT_SPEED/freq, 4))
    
    def get_pdl_value(self):
        """
        Get current pdl value
        :return: (float) pdl value in dB
        """
        return float(self._formatted_query('*PDL?'))

    def set_pdl_value(self, value):
        """
        Set pdl value
        :param value: (float, int) pdl value in dB
        """
        if not isinstance(value, (float, int)):
            raise TypeError('PDL value should be number')
        if not 0.1 <= value <= 20:
            raise ValueError('PDL value out of range')
        cmd_str = '*PDL %.1f#' % value
        backcode = self._formatted_query(cmd_str)
        if backcode != 'E00':
            raise pyvisa.Error('PDLE-101 Error: %s' % backcode)
