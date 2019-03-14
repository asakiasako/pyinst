from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOTF
from ..utils import check_range, check_type
import serial
import re


class ModelBTF10011(TypeOTF):
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

        self.__resource_name = resource_name
        self.__light_speed = 299792.458

        self.serial = serial.Serial(resource_name, baudrate=baudrate, timeout=timeout)
        self.write_termination = write_termination

     # param encapsulation
    @property
    def resource_name(self):
        return self.__resource_name

    @resource_name.setter
    def resource_name(self, value):
        raise AttributeError('param resource_name is read-only')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        self.serial.close()
    
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
        self.serial.reset_input_buffer()

    def __write(self, cmd):
        self.__clear_input_buffer()
        self.serial.write(('%s%s' % (cmd, self.write_termination)).encode())

    def __readline(self):
        return self.serial.readline()

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
        check_type(value, (int, float), 'value')
        check_range(value, self._min_wl, self._max_wl)
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
        freq = round(self.__light_speed/wl, 3)
        return freq

    def set_frequency(self, value):
        """
        Sets the filter center wavelength in frequency(THz).
        :param value: (float|int) optical frequency in THz
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_freq, self._max_freq)
        wl = round(self.__light_speed/value, 3)
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
        check_type(value, (int, float), 'value')
        check_range(value, self._min_bw, self._max_bw)
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
