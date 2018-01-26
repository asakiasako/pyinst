import visa
from .ins_types import *
from time import sleep

# define const
VERSION = '0.0.0 origin'
UPDATED = '2018/1/17'
AUTHOR = 'Chongjun Lei'
AUTHOR_EMAIL = 'chongjun.lei@neophotonics.com'
OPEN_TIMEOUT = 0  # default open timeout for all instruments if not specified during init.
TIMEOUT = 25000  # default timeout of operation for all instruments if not specified during init.
READ_TERMINATION = '\n'  # default read termination for all instruments if not specified during init.

# description
__doc__ = "Library of instruments.\n"\
    "Use visa as control method.\n" \
    "Version: %s\n"\
    "Updated: %s\n"\
    "Author: %s\n"\
    "E-mail: %s\n"\
    % (VERSION, UPDATED, AUTHOR, AUTHOR_EMAIL)


# enums
@unique
class ControlMethod(Enum):
    VISA = 1    # Control with VISA Interface, including VISA control over ethernet or serial.
    ETHERNET = 2  # Control directly with ethernet
    SERIAL = 3  # Control directly with serial port, usually RS-232

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
    def __init__(self, resource_name, read_termination=READ_TERMINATION, timeout=TIMEOUT,
                 control_method=ControlMethod.VISA, open_timeout=OPEN_TIMEOUT, *args, **kwargs):
        if control_method == ControlMethod.VISA:
            self.__inst = rm.open_resource(resource_name, read_termination=read_termination, open_timeout=open_timeout,
                                           timeout=timeout)
        self.__resource_name = resource_name
        self.__control_method = control_method
        self.__idn = self.query('*IDN?')
        self.__brand = None
        self.__model = None
        super(VisaInstrument, self).__init__()

    def __str__(self):
        return 'InsType: ' + str(self.ins_type) + '\n'\
                'IDN: ' + self.idn + '\n'\
                'Address: ' + self.resource_name + '\n'

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
        if self.__control_method == ControlMethod.VISA:
            self.__inst.write(cmd)
            return self  # for chained calling

    def read(self):
        """
        Read VISA message from instrument.
        Since it's always used after a 'command' method, it's better to use 'query' method instead.
        :return: (str) message sent from instrument
        """
        if self.__control_method == ControlMethod.VISA:
            return self.__inst.read()

    def query(self, cmd):
        """
        Send a command to instrument and read back immediately.
        :param cmd: (str) VISA command
        :return: (str) message sent from instrument
        """
        if self.__control_method == ControlMethod.VISA:
            return self.__inst.query(cmd)

    def close(self):
        """
        Close the session of visa resource
        """
        if self.__control_method == ControlMethod.VISA:
            self.__inst.close()

    def wait(self, duration):
        """
        Wait for duration in ms
        :param duration: (int|float) time to wait in ms
        """
        check_type(duration, (float, int), 'duration')
        check_range(duration, 0, 600000)
        sleep(duration/1000)
        return self


class ModelN7744A(VisaInstrument, TypeOPM):
    def __init__(self, resource_name, channel, max_channel=4, read_termination=READ_TERMINATION, timeout=TIMEOUT):
        check_type(channel, int, 'channel')
        if not 1 <= channel <= max_channel:
            raise ValueError('input channel not exist')
        super(ModelN7744A, self).__init__(resource_name, read_termination=read_termination, timeout=timeout)
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
            unit = OpticalUnit.DBM
        elif unit_int == 1:
            unit = OpticalUnit.W
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
        check_type(unit, OpticalUnit, 'unit')
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
    def __init__(self, resource_name, channel, max_channel=6, read_termination=READ_TERMINATION, timeout=TIMEOUT):
        super(ModelN7752A, self).__init__(resource_name, channel, max_channel, read_termination=read_termination,
                                          timeout=timeout)
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
    def __init__(self, resource_name, read_termination=READ_TERMINATION, timeout=TIMEOUT):
        super(ModelAQ6150, self).__init__(resource_name, read_termination=read_termination, timeout=timeout)
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


class ModelOTF970(VisaInstrument, TypeOTF):
    def __init__(self, resource_name, read_termination='\r\n', timeout=TIMEOUT):
        super(ModelOTF970, self).__init__(resource_name, read_termination=read_termination, timeout=timeout)
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
        :return: (OpticalUnit) optical power unit of power monitor
        """
        unit_str = self.query(':POW:UNIT?')
        unit_list = [OpticalUnit.DBM, OpticalUnit.W]
        unit = unit_list[int(unit_str.strip())]
        return unit

    def set_power_unit(self, unit):
        """
        Set optical power unit of power monitor.
        :param unit: (OpticalUnit) optical power unit of power monitor
        """
        check_type(unit, OpticalUnit, 'unit')
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


class ModelE36xx(VisaInstrument, TypePS):
    def __init__(self, resource_name, read_termination=READ_TERMINATION, timeout=TIMEOUT):
        super(ModelE36xx, self).__init__(resource_name, read_termination=read_termination, timeout=timeout)
        
    def enable(self, status=True):
        """
        Enable power supply output or not.
        :param status: (bool) enable status of power supply output
        """
        check_type(status, bool, 'status')
        status_list = ['OFF', 'ON']
        status_str = status_list[int(status)]
        return self.command(":OUTP "+status_str)

    def is_enabled(self):
        """
        Get the power supply output enable status.
        :return: (bool) if power supply output is enabled.
        """
        status_str = self.query(":OUTP?")
        status = bool(int(status_str))
        return status

    def set_voltage(self, value):
        """
        Set voltage (limit).
        :param value: (float|int) voltage value in V
        """
        check_type(value, (float, int), 'value')
        check_range(value, 0, self._range["max_volt"])
        return self.command(":VOLT "+str(value))

    def get_voltage(self):
        """
        Get voltage (limit) setting.
        :return: (float) voltage value in V
        """
        volt_str = self.query(':VOLT?')
        volt = float(volt_str)
        return volt

    def measure_voltage(self):
        """
        Query voltage measured
        :return: (float) voltage measured in V
        """
        volt_str = self.query(":MEAS?")
        volt = float(volt_str)
        return volt

    def set_current(self, value):
        """
        Set current (limit).
        :param value: (float|int) current value in A
        """
        check_type(value, (int, float), 'value')
        check_range(value, 0, self._range["max_current"])
        return self.command(":CURR "+str(value))

    def get_current(self):
        """
        Get current (limit) setting.
        :return: (float) current value in A
        """
        curr_str = self.query(":CURR?")
        curr = float(curr_str)
        return curr

    def measure_current(self):
        """
        Query current measured.
        :return: (float) current measured in A
        """
        curr_str = self.query(":MEAS:CURR?")
        curr = float(curr_str)
        return curr

    def set_ocp(self, value):
        """
        :param value: (float|int) ocp value in A
        """
        check_type(value, (float, int), 'value')
        check_range(value, 0, 22)
        return self.command(":CURR:PROT "+str(value))

    def get_ocp(self):
        """
        :return: (float) ocp value in A
        """
        ocp_str = self.query(":CURR:PROT?")
        ocp = float(ocp_str)
        return ocp

    def set_ocp_status(self, status):
        """
        :param status: (bool) if ocp is enabled
        """
        check_type(status, bool, 'status')
        return self.command(":CURR:PROT:STAT "+str(int(status)))

    def get_ocp_status(self):
        """
        :return: (bool) if ocp is enabled
        """
        status_str = self.query(":CURR:PROT:STAT?")
        status = bool(int(status_str))
        return status

    def ocp_is_tripped(self):
        """
        Check if the over-current protection circuit is tripped and not cleared
        :return: (bool) if ocp is tripped
        """
        trip_str = self.query(":CURR:PROT:TRIP?")
        trip = bool(int(trip_str))
        return trip

    def clear_ocp(self):
        """
        clear ocp status
        """
        return self.command(":CURR:PROT:CLE")

    def set_ovp(self, value):
        """
        :param value: (float|int) ovp value in V
        """
        check_type(value, (float, int), 'value')
        check_range(value, 0, 22)
        return self.command(":VOLT:PROT "+str(value))

    def get_ovp(self):
        """
        :return: (float) ovp value in V
        """
        ovp_str = self.query(":VOLT:PROT?")
        ovp = float(ovp_str)
        return ovp

    def set_ovp_status(self, status):
        """
        :param status: (bool) if ovp is enabled
        """
        check_type(status, bool, 'status')
        return self.command(":VOLT:PROT:STAT "+str(int(status)))

    def get_ovp_status(self):
        """
        :return: (bool) if ovp is enabled
        """
        status_str = self.query(":VOLT:PROT:STAT?")
        status = bool(int(status_str))
        return status

    def ovp_is_tripped(self):
        """
        Check if the over-voltage protection circuit is tripped and not cleared
        :return: (bool) if ovp is tripped
        """
        trip_str = self.query(":VOLT:PROT:TRIP?")
        trip = bool(int(trip_str))
        return trip

    def clear_ovp(self):
        """
        clear OVP status
        """
        return self.command(":VOLT:PROT:CLE")
        
    
class ModelE3633A(ModelE36xx):
    def __init__(self, resource_name, range_level, read_termination=READ_TERMINATION, timeout=TIMEOUT):
        super(ModelE3633A, self).__init__(resource_name, read_termination=read_termination, timeout=timeout)
        self.__model = "E3633A"
        self.__brand = "Keysight"
        self._ranges = {
            "HIGH": {
                'max_volt': 20.0,
                'max_current': 10.0
            },
            "LOW": {
                'max_volt': 8.0,
                'max_current': 20.0
            }
        }
        self._range_level = range_level
        self._range = self._ranges[self._range_level]
        self._set_range(self._range_level)

    # param encapsulation
    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        raise AttributeError('param model is read-only')

    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, value):
        raise AttributeError('param brand is read-only')

    # Methods
    def _set_range(self, range_level):
        return self.command(":VOLT:RANG "+range_level)

    def get_range(self):
        range_str = self.query(":VOLT:RANG?")
        if "8" in range_str:
            return self._ranges["LOW"]
        if "20" in range_str:
            return self._ranges["HIGH"]


class ModelE3631A(ModelE36xx):
    def __init__(self, resource_name, select, read_termination=READ_TERMINATION, timeout=TIMEOUT):
        super(ModelE3631A, self).__init__(resource_name, read_termination=read_termination, timeout=timeout)
        self.__model = "E3631A"
        self.__brand = "Keysight"
        self._ranges = {
            1: {
                'max_volt': 6.0,
                'max_current': 5.0
            },
            2: {
                'max_volt': 25.0,
                'max_current': 1.0
            },
            3: {
                'max_volt': -25.0,
                'max_current': 1.0
            }
        }
        self._select = select
        self._range = self._ranges[select]
        self._set_range(self._select)
        self._del_attr()

    # param encapsulation
    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, value):
        raise AttributeError('Param brand is read-only.')

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        raise AttributeError('Param model is read-only.')

    # Methods
    def _set_range(self, select):
        self.command(":INST:NSEL "+str(select))

    def get_range(self):
        sel_str = self.query(":INST:NSEL?")
        sel = int(sel_str)
        return self._ranges[sel]

    @staticmethod
    def _no_function(*args, **kwargs):
        raise AttributeError('Model E3631A do not have this function.')

    def _del_attr(self):
        # Model E3631 has no OCP or OVP function.
        attr_list = [
            'set_ocp',
            'get_ocp',
            'set_ocp_status',
            'get_ocp_status',
            'ocp_is_tripped',
            'clear_ocp',
            'set_ovp',
            'get_ovp',
            'set_ovp_status',
            'get_ovp_status',
            'ovp_is_tripped',
            'clear_ovp'
        ]
        for i in attr_list:
            self.__dict__[i] = self._no_function


class ModelAQ6370(VisaInstrument, TypeOSA):
    def __init__(self, resource_name, read_termination=READ_TERMINATION, timeout=TIMEOUT):
        super(ModelAQ6370, self).__init__(resource_name, read_termination=read_termination, timeout=timeout)
        self.__model = "AQ6370"
        self.__brand = "Yokogawa"
        self._analysis_cat = ["WDM", "DFBLD", "FPLD"]
        self._analysis_setting_map = {
            "WDM": ["TH", "MDIFF", "WDMASK", "NALGO", "NAREA", "MAREA", "FALGO", "NBW"],
            "DFBLD": {
                "SWIDTH": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
                "SMSR": ["SMODE", "SMASK", "MDIFF"],
                "RMS": ["ALGO", "TH", "K", "MDIFF"],
                "POWER": ["SPAN"],
                "OSNR": ["MDIFF", "NALGO", "NAREA", "MAREA", "FALGO", "NBW", "SPOWER", "IRANGE"],
            },
            "FPLD": {
                "SWIDTH": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
                "MWAVE": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
                "TPOWER": ["OFFSET"],
                "MNUMBER": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
            }
        }
        self._setup_map = ["BWIDTH:RES"]

    # param encapsulation
    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        raise AttributeError("param model is read-only.")

    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, value):
        raise AttributeError("param brand is read-only.")

    # Method
    def sweep(self, mode="REPEAT"):
        """
        Set OSA sweep mode. mode = "AUTO"|"REPEAT"|"SINGLE"|"STOP"
        :param mode: (str) "AUTO"|"REPEAT"|"SINGLE"|"STOP"
        """
        selection = ["AUTO", "REPEAT", "SINGLE", "STOP"]
        check_type(mode, str, 'mode')
        check_selection(mode, selection)
        if mode != "STOP":
            return self.command(':INIT:SMOD '+mode+';:INIT')
        else:
            return self.command(':ABOR')

    def auto_analysis(self, enable):
        """
        enable/disable auto analysis
        :param enable: (bool) enable/disable auto analysis
        """
        return self.command(":CALC:AUTO "+str(int(enable)))

    def set_analysis_cat(self, item):
        """
        Set OSA analysis item. Available item depends on specific instrument.
        item = "WDM"|"DFBLD"|"FPLD"
        :param item: (str) analysis item
        """
        check_type(item, str, 'item')
        check_selection(item, self._analysis_cat)
        return self.command(":CALC:CAT " + item)

    def get_analysis_cat(self):
        """
        Get the current analysis item.
        :return: (str) analysis item
        """
        cat_dict = {11: "WDM", 5: "DFBLD", 6: "FPLD"}
        cat_str = self.query(":CALC:CAT?")
        cat = cat_dict[int(cat_str)]
        return cat

    def analysis_setting(self, cat, param, value, subcat=None):
        """
        Analysis setting. param and value depends on specific instrument.
        :param cat: (str) setting category
        :param subcat: (str) setting sub category if there is one
        :param param: (str) setting item
        :param value: (str) setting value
        """
        check_type(cat, str, 'cat')
        check_type(param, str, 'param')
        check_type(subcat, (str, type(None)), 'subcat')
        check_selection(cat, self._analysis_cat)
        if subcat:
            check_selection(subcat, self._analysis_setting_map[cat])
            check_selection(param, self._analysis_setting_map[cat][subcat])
            route_str = " %s,%s," % (subcat, param)
        else:
            check_selection(param, self._analysis_setting_map[cat])
            route_str = ":%s " % param
        value = str(value)
        cmd_str = ":CALC:PAR:%s%s%s" % (cat, route_str, value)
        return self.command(cmd_str)

    def get_analysis_setting_map(self):
        """
        Get setting map for all analysis categories.
        :return: (dict) analysis setting map
        """
        return self._analysis_setting_map

    def get_analysis_data(self):
        """
        Get data of current analysis item.
        :return: (str) data of current analysis item
        """
        return self.query(':CALC:DATA?')

    def set_center(self, value, unit):
        """
        Set center wavelength/frequency
        :param value: (float|int) center value
        :param unit: (str) unit
        """
        check_type(value, (float, int), 'value')
        check_type(unit, str, 'unit')
        check_selection(unit, ['NM', 'THZ'])
        if unit == 'NM':
            return self.command(":SENS:WAV:CENT " + str(value) + 'NM')
        if unit == 'THZ':
            return self.command(":SENS:WAV:CENT " + str(value) + 'THZ')

    def set_peak_to_center(self):
        """
        Set peak wavelength to center.
        """
        return self.command(':CALC:MARK:MAX:SCEN')

    def set_span(self, value, unit="NM"):
        """
        Set span wavelength/frequency
        :param value: (float|int) span value
        :param unit: (str) unit
        """
        check_type(value, (float, int), 'value')
        return self.command(':SENS:WAV:SPAN ' + str(value) + unit)

    def set_start_stop_wavelength(self, start, stop):
        """
        Set start-stop wavelength.
        :param start: (float|int) start wavelength in nm
        :param stop: (float|int) stop wavelength in nm
        """
        check_type(start, (float, int), 'start')
        check_type(stop, (float, int), 'stop')
        check_range(start, 0, stop)
        return self.command(':SENS:WAV:STAR %fNM;:SENS:WAV:STOP %fNM' % (start, stop))

    def set_start_stop_frequency(self, start, stop):
        """
        Set start-stop frequency.
        :param start: (float|int) start frequency in THz
        :param stop: (float|int) stop frequency in THz
        """
        check_type(start, (float, int), 'start')
        check_type(stop, (float, int), 'stop')
        check_range(stop, 0, start)
        return self.command(':SENS:WAV:STAR %fTHZ;:SENS:WAV:STOP %fTHZ' % (start, stop))


    def set_ref_level(self, value, unit):
        """
        Set reference level.
        :param value: (float|int) reference level value
        :param unit: (str) unit = "DBM"|"MW
        """
        check_type(value, (float, int), 'value')
        check_type(unit, str, 'unit')
        check_selection(unit, ['DBM', 'MW', 'UM', 'NW'])
        return self.command(":DISPLAY:TRACE:Y1:RLEVEL %f%s" % (value, unit))


    def set_peak_to_ref(self):
        """
        Set peak level to reference level
        """
        return self.command(':CALC:MARK:MAX:SRL')

    def setup(self, param, value):
        """
        Set setup settings.
        :param param: (str) param
        :param value: (str) setting value
        """
        check_type(param, str, 'param')
        check_type(value, str, 'value')
        return self.command(':SENS:%s %s' % (param, value))

    def format_data(self, cat, data):
        """
        Format data into dict, depends on calculate category (Anasis Category)
        :param cat: (str) "DFB"|"FP"|"WDM"
        :param data: (str) data retruned by method: get_analysis_data
        :return: (dict) a dict of test_item=>value
        """
        check_type(cat, str, 'cat')
        check_type(data, str, 'data')
        check_selection(cat, self._analysis_cat)
        data_list = data.split(',')
        r_data = None
        if cat == 'DFBLD':
            r_data = {
                "spec_wd": data_list[0],
                "peak_wl": data_list[1],
                "peak_lvl": data_list[2],
                "mode_ofst": data_list[3],
                "smsr": data_list[4]
            }
        elif cat == 'FPLD':
            r_data = {
                "spec_wd": data_list[0],
                "peak_wl": data_list[1],
                "peak_lvl": data_list[2],
                "center_wl": data_list[3],
                "total_pow": data_list[4],
                "mode_num": data_list[5]
            }
        elif cat == 'WDM':
            #  <display type> = ABSolute|0, RELative|1, MDRift|2, GDRift|3
            d_type = int(self.query(':CALC:PAR:WDM:DTYP?'))
            # 0 = OFFSET, 1 = SPACING
            relation = int(self.query(':CALC:PAR:WDM:REL?'))
            if d_type == 0:
                if relation == 0:
                    r_data = {
                        "ch_num": data_list[0],
                        "center_wl": data_list[1],
                        "peak_lvl": data_list[2],
                        "offset_wl": data_list[3],
                        "offset_lvl": data_list[4],
                        "noise": data_list[5],
                        "snr": data_list[6]
                    }
                elif relation == 1:
                    r_data = {
                        "ch_num": data_list[0],
                        "center_wl": data_list[1],
                        "peak_lvl": data_list[2],
                        "spacing": data_list[3],
                        "lvl_diff": data_list[4],
                        "noise": data_list[5],
                        "snr": data_list[6]
                    }
            elif d_type == 1:
                r_data = {
                    "ch_num": data_list[0],
                    "grid_wl": data_list[1],
                    "center_wl": data_list[2],
                    "rel_wl": data_list[3],
                    "peak_lvl": data_list[4],
                    "noise": data_list[5],
                    "snr": data_list[6]
                }
            elif d_type == 2:
                r_data = {
                    "ch_num": data_list[0],
                    "grid_wl": data_list[1],
                    "center_wl": data_list[2],
                    "wl_diff_max": data_list[3],
                    "wl_diff_min": data_list[4],
                    "ref_lvl": data_list[5],
                    "peak_lvl": data_list[6],
                    "lvl_diff_max": data_list[7],
                    "lvl_diff_min": data_list[8]
                }
            elif d_type == 3:
                r_data = {
                    "ch_num": data_list[0],
                    "ref_wl": data_list[1],
                    "center_wl": data_list[2],
                    "wl_diff_max": data_list[3],
                    "wl_diff_min": data_list[4],
                    "ref_lvl": data_list[5],
                    "peak_lvl": data_list[6],
                    "lvl_diff_max": data_list[7],
                    "lvl_diff_min": data_list[8]
                }
        return r_data
