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
        self._ins_type = []
        self.__brand = None
        self.__model = None
        self._mismatch = False

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
    def ins_type(self):
        return self.__ins_type

    @ins_type.setter
    def ins_type(self, value):
        raise AttributeError('attr "ins_type" is read-only.')

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
    def mismatch(self):
        return self._mismatch

    @mismatch.setter
    def mismatch(self, value):
        raise AttributeError('attr "mismatch" is read-only.')

    # methods
    def check_mismatch(self):
        """
        Check if idn matches model name.
        """
        idn = self.idn
        model = self.model
        if model not in idn:
            self._mismatch = True
        else:
            self._mismatch = False

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
    def __init__(self, resource_name, channel):
        VisaInstrument.__init__(self, resource_name)
        TypeOPM.__init__(self)
        self.__brand = "Keysight"
        self.__model = "N7744A"
        self.__channel = channel
        self.check_mismatch()

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
