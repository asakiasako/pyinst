from ..base_models._BaseInstrument import BaseInstrument
from ..instrument_types import TypeWM
from ..constants import OpticalUnit
from ..utils import check_type
import zerorpc


__all__ = ['ModelRemoteAQ6150']


def set_switch(func):
    def wrapper(self, *args, **kwargs):
        self.__client.set_switch(self.__osw_ch)
        return func(self, *args, **kwargs)
    return wrapper


class ModelRemoteAQ6150(BaseInstrument, TypeWM):
    model = "Remote AQ6150"
    brand = "Yokogawa"
    params = [
        {
            "name": "osw_ch",
            "type": "int",
            "options": [1, 2, 3, 4, 5]
        }
    ]
    details = {
        "Wavelength Range": "1270 ~ 1650 nm",
        "Power Accuracy": "+/-0.5 dB",
        "Input Power Range": "-40 ~ 10 dBm",
        "Safe Power": "+18 dBm"
    }

    def __init__(self, resource_name, osw_ch, **kwargs):
        super(ModelRemoteAQ6150, self).__init__(resource_name, **kwargs)
        self.__client = zerorpc.Client()
        self.__client.connect(resource_name)
        self.__osw_ch = osw_ch
        self._resource_name = resource_name

    def close(self):
        self.__client.close()

    def check_connection(self):
        return self.__client.call_method('check_connection')

    # param encapsulation
    def run(self):
        """
        Start repeat measurement.
        """
        return self.__client.call_method('run')

    def stop(self):
        """
        Stop repeat measurement.
        """
        return self.__client.call_method('stop')

    def is_running(self):
        """
        Get measurement state of WM.
        :return: (bool) if repeat measurement is started.
        """
        return self.__client.call_method('is_running')

    @ set_switch
    def get_frequency_array(self):
        """
        Get wavelength of all peaks in unit of frequency.
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        return self.__client.call_method('get_frequency_array')

    @ set_switch
    def get_wavelength_array(self):
        """
        Get wavelength of all peaks in unit of wavelength.
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        return self.__client.call_method('get_wavelength_array')

    @ set_switch
    def get_power_array(self):
        """
        Get optical power of all peaks in selected unit.
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        return self.__client.call_method('get_power_array')

    def get_power_unit(self):
        """
        Get optical power unit.
        :return: int, value of <enum 'OpticalUnit'>, optical power unit.
        """
        return self.__client.call_method('get_power_unit')

    def set_power_unit(self, unit):
        """
        Set optical power unit.
        :Parameters: **unit** - int, value of <enum 'OpticalUnit'>, optical power unit.
        """
        return self.__client.call_method('set_power_unit', unit)

    @ set_switch
    def get_frequency(self):
        """
        Get frequency of single peak in THz.

        :Returns: float, frequency in THz
        """
        return self.__client.call_method('get_frequency')

    @ set_switch
    def get_wavelength(self):
        """
        Get wavelength of single peak in nm

        :Returns: float, wavelength in nm
        """
        return self.__client.call_method('get_wavelength')

    @ set_switch
    def get_power_value(self):
        """
        Get wavelength of single peak in selected unit
        :return: (float) optical power in selected unit.
        """
        return self.__client.call_method('get_power_value')
