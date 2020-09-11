from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOTF
from ..constants import OpticalUnit, LIGHT_SPEED
from pyvisa.constants import Parity, StopBits


class ModelXTA50(VisaInstrument, TypeOTF):
    model = "XTA-50"
    brand = "EXFO"

    def __init__(self, resource_name, read_termination='\r\n', write_termination='\r\n', **kwargs):
        RS232_CONFIG = {
            'baud_rate': 9600,
            'data_bits': 8,
            'parity': Parity.none,
            'stop_bits': StopBits.one
        }
        super(ModelXTA50, self).__init__(resource_name, read_termination=read_termination,
                                          write_termination=write_termination, **kwargs)
        self._set_ranges()

    # Methods
    def _set_ranges(self):
        self._min_wl = 1480
        self._max_wl = 1620
        self._min_freq = round(LIGHT_SPEED/self._max_wl, 3)
        self._max_freq = round(LIGHT_SPEED/self._min_wl, 3)
        self._min_bw = float(self.query('FWHM_MIN?').split('=')[1])
        self._max_bw = float(self.query('FWHM_MAX?').split('=')[1])

    def get_wavelength(self):
        """
        Reads out the setting value of the filter center wavelength.
        :return: (float) wavelength in nm.
        """
        return LIGHT_SPEED/self.get_frequency()

    def set_wavelength(self, value):
        """
        Sets the filter center wavelength.
        :param value: (float|int) wavelength in nm
        """
        freq = LIGHT_SPEED/value
        self.set_frequency(freq)

    def get_frequency(self):
        """
        Reads out the filter center wavelength in optical frequency.
        :return: (float) optical frequency in THz
        """
        freq = float(self.query('FREQ?').split('=')[1])
        return freq

    def set_frequency(self, value):
        """
        Sets the filter center wavelength in frequency(THz).
        :param value: (float|int) optical frequency in THz
        """
        if not isinstance(value, (float, int)):
            raise TypeError('Frequency value should be number.')
        if not self.min_frequency <= value <= self.max_frequency:
            raise ValueError('Frequency value out of range')
        self.query('FREQ={freq}'.format(freq=round(value, 5)))

    def get_bandwidth(self):
        """
        Reads out the filter bandwidth.
        :return: (float) bandwidth setting value in nm
        """
        bw = float(self.query('FWHM?').split('=')[1])
        return bw

    def set_bandwidth(self, value):
        """
        Sets the filter bandwidth.
        :param value: (float|int) bandwidth setting value in nm
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Bandwidth should be number')
        if not self.min_bandwidth <= value <= self.max_bandwidth:
            raise ValueError('Bandwidth value out of range')
        self.query('FWHM={bw}'.format(bw=round(value, 4)))
