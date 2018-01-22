import visa
from .ins_types import *

# define const
VERSION = '0.0.0 origin'
UPDATED = '2018/1/17'
AUTHOR = 'Chongjun Lei'
AUTHOR_EMAIL = 'chongjun.lei@neophotonics.com'
OPEN_TIMEOUT = 0  # default open timeout for all instruments if not specified during init.
READ_TERMINATION = '\n'  # default read termination for all instruments if not specified during init.

# description
__doc__ = "Library of instruments.\n"\
    "Use visa as control method.\n" \
    "Version: %s\n"\
    "Updated: %s\n"\
    "Author: %s\n"\
    "E-mail: %s\n"\
    % (VERSION, UPDATED, AUTHOR, AUTHOR_EMAIL)

# globals
rm = visa.ResourceManager()  # VISA ResourceManager


def close():
    """
    Close the resource manager session.
    """
    rm.close()


def list_resources():
    """
    :return: (tuple of str) Returns a tuple of all connected devices.
    """
    return rm.list_resources()


def list_resources_info():
    """
    :return: (dict) Returns a dictionary mapping resource names to resource extended information of all connected \
    devices
    """
    return rm.list_resources_info()


def resource_info(resource_name):
    """
    Get the (extended) information of a particular resource.
    :param resource_name: (str) resource name of instrument.
    :return: (ResourceInfo) Returns information of a particular resource.
    """
    return rm.resource_info(resource_name)


# base class of visa instruments
class VisaInstrument(object):
    """
    Base class of visa instruments.
    __init__(self, resource_name, read_termination=READ_TERMINATION, open_timeout=OPEN_TIMEOUT)
    """
    def __init__(self, resource_name, read_termination=READ_TERMINATION, open_timeout=OPEN_TIMEOUT):
        self.__inst = rm.open_resource(resource_name, read_termination=read_termination, open_timeout=open_timeout)
        self.__resource_name = resource_name
        self.__idn = self.query('*IDN?')
        self.__brand = None
        self.__model = None
        super(VisaInstrument, self).__init__()

    def __str__(self):
        return 'InsType: ' + str(self.ins_type) + '\n'\
                'IDN: ' + self.idn + '\n'\
                'VISA_Address: ' + self.resource_name

    # support for context
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # param encapsulation
    @property
    def resource_name(self):
        return self.__resource_name

    @resource_name.setter
    def resource_name(self, value):
        raise AttributeError('attr "resource_name" is read-only.')

    @property
    def idn(self):
        return self.__idn

    @idn.setter
    def idn(self, value):
        raise AttributeError('attr "IDN" is read-only.')

    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, value):
        raise AttributeError('attr "brand" is read-only.')

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        raise AttributeError('attr "model" is read-only.')

    # methods
    def check_mismatch(self):
        """
        Check if idn matches model name.
        :return: (bool) if idn mismatches model name
        """
        idn = self.idn
        model = self.model
        if isinstance(model, str):
            model = [model]
        for i in model:
            if i in idn:
                return False
        return True

    def command(self, cmd):
        """
        Write a VISA command without read back.
        You can use chained calling, such as: instrument.command(cmd1).command(cmd2).command(cmd3)...
        :param cmd: (str) VISA command
        :return: (BaseInstrument) self
        """
        self.__inst.write(cmd)
        return self  # for chained calling

    def read(self):
        """
        Read VISA message from instrument.
        Since it's always used after a 'command' method, it's better to use 'query' method instead.
        :return: (str) message sent from instrument
        """
        return self.__inst.read()

    def query(self, cmd):
        """
        Send a command to instrument and read back immediately.
        :param cmd: (str) VISA command
        :return: (str) message sent from instrument
        """
        return self.__inst.query(cmd)

    def close(self):
        """
        Close the session of visa resource
        """
        self.__inst.close()


class ModelN7744A(VisaInstrument, TypeOPM):
    def __init__(self, resource_name, channel, max_channel=4):
        if not isinstance(channel, int):
            raise TypeError('channel should be int')
        if not 1 <= channel <= max_channel:
            raise ValueError('input channel not exist')
        super(ModelN7744A, self).__init__(resource_name)
        self.__brand = "Keysight"
        self.__model = "N7744A"
        self.__channel = channel

    # param encapsulation
    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, value):
        raise AttributeError('attr "brand" is read-only.')

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        raise AttributeError('attr "model" is read-only.')

    @property
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, value):
        raise AttributeError('attr "channel" is read-only.')

    # Rewrite TypeOPM Methods
    def get_value(self):
        """
        :return: (float) value of optical power, ignore power unit
        """
        value_str = self.query(":FETC"+str(self.channel)+":POW?")
        if not value_str:
            raise ValueError('Empty return for get_value')
        value = float(value_str)
        return value

    def get_unit(self):
        """
        OpticalUnit.DBM.value = 0, OpticalUnit.W.value = 1
        :return: (enum 'OpticalUnit') unit of optical power
        """
        unit_int = int(self.query(":SENS" + str(self.channel) + ":POW:UNIT?"))
        if unit_int == 0:
            unit = OpticalUnits.DBM
        elif unit_int == 1:
            unit = OpticalUnits.W
        else:
            unit = None
        return unit

    def get_cal(self):
        """
        :return: (float) calibration offset in dB
        """
        cal_str = self.query('sens' + str(self.channel) + ':corr?')
        cal = float(cal_str)
        return cal

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        wl_str = self.query("sens" + str(self.channel) + ":pow:wav?")
        wl = float(wl_str) * 10 ** 9
        return wl

    def set_unit(self, unit):
        """
        Set optical power unit
        """
        if not isinstance(unit, OpticalUnits):
            raise TypeError('Unit should be <enum OpticalUnits>')
        return self.command(":SENS" + str(self.channel) + ":POW:UNIT " + str(unit.value))

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Calibration value should be a number (int or float)')
        return self.command('sens' + str(self.channel) + ':corr ' + str(value) + 'DB')

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Calibration value should be a number (int or float)')
        return self.command("sens" + str(self.channel) + ":pow:wav " + str(value) + "NM")


class ModelN7752A(ModelN7744A, TypeVOA):
    def __init__(self, resource_name, channel, max_channel=6):
        super(ModelN7752A, self).__init__(resource_name, channel, max_channel)
        self.__model = "N7752A"

    # param encapsulation
    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        raise AttributeError('attr "model" is read-only.')

    # Methods
    def __is_att(self):
        if self.channel in (1, 2, 3, 4):
            return True
        else:
            return False

    def __check_is_att(self):
        if not self.__is_att():
            raise ValueError('channel '+str(self.channel)+' has no att function.')

    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        self.__check_is_att()
        if not isinstance(status, bool):
            raise TypeError('param "status" should be bool.')
        status_str = str(int(status))
        return self.command(":OUTP" + str(self.channel) + " " + status_str)

    def is_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        self.__check_is_att()
        status = self.query(":OUTP" + str(self.channel) + "?")
        if status:
            status = bool(int(status))
        return status

    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        self.__check_is_att()
        att_str = self.query(":INP" + str(self.channel) + ":ATT?")
        att = float(att_str)
        return att

    def get_offset(self):
        """
        Get att offset value in dB.
        :return: (float) att offset value in dB
        """
        self.__check_is_att()
        offset_str = self.query("INP" + str(self.channel) + ":OFFS?")
        offset = float(offset_str)
        return offset

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        if self.channel >= 5:
            return ModelN7744A.get_wavelength(self)
        wl_str = self.query(":INP"+str(self.channel)+":WAV?")
        wl = float(wl_str)
        return wl

    def get_cal(self):
        """
        :return: (float) power monitor calibration offset in dB
        """
        if self.channel >= 5:
            return ModelN7744A.get_cal(self)
        cal_str = self.query("OUTP" + str(self.channel) + ":POW:OFFS?")
        cal = float(cal_str)
        return cal

    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        self.__check_is_att()
        return self.command("INP" + str(self.channel) + ":ATT " + str(value) + "dB")

    def set_offset(self, value):
        """
        Set att offset value in dB.
        :param value: (float|int) att offset value in dB
        """
        self.__check_is_att()
        return self.command("INP"+str(self.channel)+":OFFS "+str(value)+"dB")

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        if self.channel >= 5:
            return ModelN7744A.set_wavelength(self, value)
        return self.command(":INP"+str(self.channel)+":WAV " + str(value) + "NM")

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        if self.channel >= 5:
            return ModelN7744A.set_cal(self, value)
        return self.command("OUTP" + str(self.channel) + ":POW:OFFS " + str(value))


class ModelAQ6150(VisaInstrument, TypeWM):
    def __init__(self, resource_name):
        super(ModelAQ6150, self).__init__(resource_name)
        self.__model = ["AQ6150", "AQ6151"]
        self.__brand = "Yokogawa"

    # param encapsulation
    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        raise AttributeError('attr "model" is read-only.')

    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, value):
        raise AttributeError('attr "brand" is read-only.')

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
        :return: (OpticalUnits) optical power unit.
        """
        unit_str = self.query(":UNIT?")
        if unit_str.strip() == "DBM":
            return OpticalUnits.DBM
        if unit_str.strip() == "W":
            return OpticalUnits.W

    def set_power_unit(self, unit):
        """
        Set optical power unit.
        :param unit: (OpticalUnits) optical power unit.
        """
        if not isinstance(unit, OpticalUnits):
            raise TypeError('unit should be <enum OpticalUnits>')
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
        pow = float(pow_str)
        return pow
