from ._BaseInstrument import BaseInstrument
from ..instrument_types import TypeOTF
from ..constants import LIGHT_SPEED
import serial
import re


class ModelBTF10011(BaseInstrument, TypeOTF):
    model = "BTF-100-11"
    brand = "OZ Optics"
    details = {
        "Wavelength Range": "1525-1565 nm",
        "Frequency Range": "191.56-196.58 THz",
        "Bandwidth @-3dB": "1-18 nm",
        "PDL": "Less than 0.3 dB"
    }
    params = []

    def __init__(self, resource_name, baudrate=115200, write_termination='\r\n', timeout=3, **kwargs):
        super(ModelBTF10011, self).__init__()
        self._min_wl = 1525
        self._max_wl = 1565
        self._min_freq = 191.56
        self._max_freq = 196.58
        self._min_bw = 1
        self._max_bw = 18

        self._resource_name = resource_name

        self.__serial = serial.Serial(resource_name, baudrate=baudrate, timeout=timeout)
        self.__write_termination = write_termination
    
    def close(self):
        self.__serial.close()
    
    def check_connection(self):
        self.__write('b?')
        line_count = 0
        while True:
            if line_count>=3:
                return False
            line_count += 1
            dataline = self.__readline().decode()
            if 'done' in dataline.lower():
                return True
    
    def __clear_input_buffer(self):
        self.__serial.reset_input_buffer()

    def __write(self, cmd):
        self.__clear_input_buffer()
        self.__serial.write(('%s%s' % (cmd, self.__write_termination)).encode())

    def __readline(self):
        return self.__serial.readline()

    def get_wavelength(self):
        """
        Reads out the setting value of the filter center wavelength.
        :return: (float) wavelength in nm.
        """
        self.__write('w?')
        line_count = 0
        data = ''
        while True:
            if line_count>=5:
                raise TimeoutError('No expected end message after 5 lines.')
            line_count += 1
            dataline = self.__readline().decode()
            if 'done' in dataline.lower():
                break
            else:
                data += dataline
        if 'unknown' in data.lower():
            raise ValueError('Unknown wavelength.')
        else:
            return float(re.search('.*WL\((.*?)\).*', data).group(1))

    def set_wavelength(self, value):
        """
        Sets the filter center wavelength.
        :param value: (float|int) wavelength in nm
        """
        if not isinstance(value, (int, float)):
            raise TypeError('wavelength value should be number')
        if not self._min_wl <= value <= self._max_wl:
            raise ValueError('Wavelength value out of range: %r' % value)
        self.__write('w%.2f' % value)
        line_count = 0
        while True:
            if line_count>=5:
                raise TimeoutError('No expected end message after 5 lines.')
            line_count += 1
            dataline = self.__readline().decode()
            if 'done' in dataline.lower():
                break
            if 'error' in dataline.lower():
                raise ValueError('Get error when operating OTF.')

    def get_frequency(self):
        """
        Reads out the filter center wavelength in optical frequency.
        :return: (float) optical frequency in THz
        """
        wl = self.get_wavelength()
        freq = round(LIGHT_SPEED/wl, 3)
        return freq

    def set_frequency(self, value):
        """
        Sets the filter center wavelength in frequency(THz).
        :param value: (float|int) optical frequency in THz
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Frequency value should be number')
        if not self.min_frequency <= value <= self.max_frequency:
            raise ValueError('Frequency value out of range')
        wl = round(LIGHT_SPEED/value, 3)
        return self.set_wavelength(wl)

    def get_bandwidth(self):
        """
        Reads out the filter bandwidth.
        :return: (float) bandwidth setting value in nm
        """
        self.__write('w?')
        line_count = 0
        data = ''
        while True:
            if line_count>=5:
                raise TimeoutError('No expected end message after 5 lines.')
            line_count += 1
            dataline = self.__readline().decode()
            if 'done' in dataline.lower():
                break
            else:
                data += dataline
        if 'unknown' in data.lower():
            raise ValueError('Unknown wavelength.')
        else:
            return float(re.search('.*LW\((.*?)nm\).*', data).group(1))

    def set_bandwidth(self, value):
        """
        Sets the filter bandwidth.
        :param value: (float|int) bandwidth setting value in nm
        """
        if not isinstance(value, (float, int)):
            raise TypeError('Bandwidth value should be number')
        if not self.min_bandwidth <= value <= self.max_bandwidth:
            raise ValueError('Bandwidth value out of range')
        wl = self.get_wavelength()
        self.__write('w%.2f,%.2f' % (wl, value))
        line_count = 0
        while True:
            if line_count>=5:
                raise TimeoutError('No expected end message after 5 lines.')
            line_count += 1
            dataline = self.__readline().decode()
            if 'done(a)' in dataline.lower():
                break
            if 'error' in dataline.lower():
                raise ValueError('Get error when operating OTF.')
