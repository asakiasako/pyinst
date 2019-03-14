from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeWM
from ..constants import OpticalUnit
from ..utils import check_type


class ModelAQ6150(VisaInstrument, TypeWM):
    model = ["AQ6150", "AQ6151"]
    brand = "Yokogawa"
    details = {
        "Wavelength Range": "1270 ~ 1650 nm",
        "Power Accuracy": "+/-0.5 dB",
        "Input Power Range": "-40 ~ 10 dBm",
        "Safe Power": "+18 dBm"
    }

    def __init__(self, resource_name, **kwargs):
        super(ModelAQ6150, self).__init__(resource_name, **kwargs)

    # param encapsulation

    # Methods
    def format_array_data(self, msg):
        """
        Format array data from AQ6150 to readable format.
        :param msg: array data str from AQ6150
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        msg_str = msg
        msg_str_list = msg_str.split(",")
        num = int(msg_str_list[0])
        value_list = [float(i) for i in msg_str_list[1:]]
        value_tuple = tuple(value_list)
        rtn_dict = {"num": num, "values": value_tuple}
        return rtn_dict

    def start(self):
        """
        Start repeat measurement.
        """
        return self.command(":INIT:CONT ON")

    def stop(self):
        """
        Stop repeat measurement.
        """
        return self.command(":ABOR")

    def is_started(self):
        """
        Get measurement state of WM.
        :return: (bool) if repeat measurement is started.
        """
        status_str = self.query(":INIT:CONT?")
        status = bool(int(status_str))
        return status

    def get_frequency_array(self):
        """
        Get wavelength of all peaks in unit of frequency.
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        msg_str = self.query(":FETC:ARR:POW:FREQ?")
        return self.format_array_data(msg_str)

    def get_wavelength_array(self):
        """
        Get wavelength of all peaks in unit of wavelength.
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        msg_str = self.query(":FETC:ARR:POW:WAV?")
        return self.format_array_data(msg_str)

    def get_power_array(self):
        """
        Get optical power of all peaks in selected unit.
        :return: (dict) {'num': (int), 'values': (tuple of floats)}
        """
        msg_str = self.query(":FETC:ARR:POW?")
        return self.format_array_data(msg_str)

    def get_power_unit(self):
        """
        Get optical power unit.
        :return: (OpticalUnit) optical power unit.
        """
        unit_str = self.query(":UNIT?")
        if unit_str.strip() == "DBM":
            return OpticalUnit.DBM
        if unit_str.strip() == "W":
            return OpticalUnit.W

    def set_power_unit(self, unit):
        """
        Set optical power unit.
        :param unit: (OpticalUnit) optical power unit.
        """
        check_type(unit, OpticalUnit, 'unit')
        unit_list = ["DBM", "W"]
        unit_str = unit_list[unit.value]
        return self.command(":UNIT "+unit_str)

    def get_frequency(self):
        """
        Get frequency of single peak in Hz
        :return: (float) frequency in Hz
        """
        freq_str = self.query(":FETC:POW:FREQ?")
        freq = float(freq_str)
        return freq

    def get_wavelength(self):
        """
        Get wavelength of single peak in m
        :return: (float) wavelength in m
        """
        wl_str = self.query(":FETC:POW:WAV?")
        wl = float(wl_str)
        return wl

    def get_power(self):
        """
        Get wavelength of single peak in selected unit
        :return: (float) optical power in selected unit.
        """
        pow_str = self.query(":FETC:POW?")
        pow_float = float(pow_str)
        return pow_float