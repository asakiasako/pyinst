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
    def __init__(self, resource_name, channel, max_channel=4, read_termination=READ_TERMINATION):
        check_type(channel, int, 'channel')
        if not 1 <= channel <= max_channel:
            raise ValueError('input channel not exist')
        super(ModelN7744A, self).__init__(resource_name, read_termination=read_termination)
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
        check_type(unit, OpticalUnits, 'unit')
        return self.command(":SENS" + str(self.channel) + ":POW:UNIT " + str(unit.value))

    def set_cal(self, value):
        """
        Set calibration offset in dB
        """
        check_type(value, (int, float), 'value')
        return self.command('sens' + str(self.channel) + ':corr ' + str(value) + 'DB')

    def set_wavelength(self, value):
        """
        Set optical wavelength in nm
        """
        check_type(value, (int, float), 'value')
        return self.command("sens" + str(self.channel) + ":pow:wav " + str(value) + "NM")


class ModelN7752A(ModelN7744A, TypeVOA):
    def __init__(self, resource_name, channel, max_channel=6, read_termination=READ_TERMINATION):
        super(ModelN7752A, self).__init__(resource_name, channel, max_channel, read_termination=read_termination)
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
        check_type(status, bool, 'status')
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
    def __init__(self, resource_name, read_termination=READ_TERMINATION):
        super(ModelAQ6150, self).__init__(resource_name, read_termination=read_termination)
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
        check_type(unit, OpticalUnits, 'unit')
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


class ModelOTF970(VisaInstrument, TypeOTF):
    def __init__(self, resource_name, read_termination='\r\n'):
        super(ModelOTF970, self).__init__(resource_name, read_termination=read_termination)
        self.__model = "OTF-970"
        self.__brand = "Santec"
        self._set_ranges()

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
    def _set_ranges(self):
        self._min_wl = float(self.query(':WAV? MIN'))*10**9
        self._max_wl = float(self.query(':WAV? MAX'))*10**9
        self._min_freq = float(self.query(':FREQ? MIN'))/(10**12)
        self._max_freq = float(self.query(':FREQ? MAX'))/(10**12)
        self._min_bw = float(self.query(':BAND? MIN'))*10**9
        self._max_bw = float(self.query(':BAND? MAX'))*10**9
        self._min_wl_offs = float(self.query(':OFFS? MIN'))*10**9
        self._max_wl_offs = float(self.query(':OFFS? MAX'))*10**9
        self._min_bw_offs = float(self.query(':OFFS:Band? MIN'))*10**9
        self._max_bw_offs = float(self.query(':OFFS:Band? MAX'))*10**9

    def get_wavelength(self):
        """
        Reads out the setting value of the filter center wavelength.
        :return: (float) wavelength in nm.
        """
        wl_str = self.query(':WAV?')
        wl = float(wl_str)*10**9
        return wl

    def set_wavelength(self, value):
        """
        Sets the filter center wavelength.
        :param value: (float|int) wavelength in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_wl, self._max_wl)
        return self.command(':WAV '+str(value)+'nm')

    def get_wavelength_state(self):
        """
        Reads out the operation state of the filter center wavelength.
        :return: (bool) if setting of the filter center wavelength is in operation.
        """
        state_str = self.query(':WAV:STAT?')
        state = bool(int(state_str))
        return state

    def get_frequency(self):
        """
        Reads out the filter center wavelength in optical frequency.
        :return: (float) optical frequency in THz
        """
        freq_str = self.query(":FREQ?")
        freq = float(freq_str)/(10**12)
        return freq

    def set_frequency(self, value):
        """
        Sets the filter center wavelength in frequency(THz).
        :param value: (float|int) optical frequency in THz
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_freq, self._max_freq)
        return self.command(':FREQ '+str(value)+'THz')

    def get_wavelength_offset(self):
        """
        Reads out the offset wavelength of the filter center wavelength.
        :return: (float) wavelength offset in nm
        """
        offset_str = self.query(':OFFS?')
        offset = float(offset_str)*10**9
        return offset

    def set_wavelength_offset(self, value):
        """
        Sets the offset to the filter center wavelength.
        :param value: (float|int) wavelength
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_wl_offs, self._max_wl_offs)
        return self.command(':OFFS '+str(value)+'nm')

    def get_bandwidth(self):
        """
        Reads out the filter bandwidth.
        :return: (float) bandwidth setting value in nm
        """
        bw_str = self.query(':BAND?')
        bw = float(bw_str)*10**9
        return bw

    def set_bandwidth(self, value):
        """
        Sets the filter bandwidth.
        :param value: (float|int) bandwidth setting value in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_bw, self._max_bw)
        return self.command(':BAND '+str(value)+'nm')

    def get_bandwidth_state(self):
        """
        Reads out the setting state of the filter bandwidth.
        :return: (bool) if setting of the filter bandwidth is in operation
        """
        state_str = self.query(':BAND:STAT?')
        state = bool(int(state_str))
        return state

    def get_bandwidth_offset(self):
        """
        Reads out the offset bandwidth of filter bandwidth.
        :return: (float) bandwidth offset in nm
        """
        offset_str = self.query(':OFFS:Band?')
        offset = float(offset_str)*10**9
        return offset

    def set_bandwidth_offset(self, value):
        """
        Sets the offset to the filter bandwidth.
        :param value: (float|int) bandwidth offset in nm
        """
        check_type(value, (int, float), 'value')
        check_range(value, self._min_bw_offs, self._max_bw_offs)
        return self.command(':OFFS:Band '+str(value)+'nm')

    def get_power_unit(self):
        """
        Get optical power unit of power monitor.
        :return: (OpticalUnits) optical power unit of power monitor
        """
        unit_str = self.query(':POW:UNIT?')
        unit_list = [OpticalUnits.DBM, OpticalUnits.W]
        unit = unit_list[int(unit_str.strip())]
        return unit

    def set_power_unit(self, unit):
        """
        Set optical power unit of power monitor.
        :param unit: (OpticalUnits) optical power unit of power monitor
        """
        check_type(unit, OpticalUnits, 'unit')
        return self.command(":POW:UNIT "+str(unit.value))

    def get_power_value(self):
        """
        Get optical power value in selected unit. Range: -40dBm ~ 10dBm
        :return: (float) optical power in selected unit.
        """
        value_str = self.query(':POW?')
        value = float(value_str)
        return value

    def _set_peak_search_center(self, center):
        """
        Set peak search center in nm.
        :param center: (float|int) peak search center in nm
        """
        check_type(center, (int, float), 'center')
        check_range(center, self._min_wl, self._max_wl)
        return self.command(':CENT '+str(center)+'nm')

    def _set_peak_search_span(self, span):
        """
        Set peak search span in nm.
        :param span: (float|int) peak search span in nm
        """
        check_type(span, (float, int), 'span')
        check_range(span, 0, 2*(self._max_wl-self._min_wl))
        return self.command(':SPAN '+str(span)+'nm')

    def _run_peak_search(self, if_run):
        """
        Run or cancel peak search.
        :param if_run: (bool) if run or cancel
        """
        check_type(if_run, bool, 'if_run')
        return self.command(':PS '+str(int(if_run)))

    def _is_peak_search_complete(self):
        """
        If peak search is completed.
        :return: (bool) if peak search is completed.
        """
        status_str = self.query(':PS?')
        status = bool(int(status_str))
        return status

    def peak_search(self, center, span):
        self._set_peak_search_center(center)
        self._set_peak_search_span(span)
        self._run_peak_search(True)
        print('1')
        while True:
            print('2')
            sleep(0.5)
            print('3')
            if self._is_peak_search_complete():
                print('4')
                return self
