import pyvisa
from ._BaseInstrument import BaseInstrument
from ..utils import check_type, check_range
from time import sleep
import subprocess
import os.path

# define const
OPEN_TIMEOUT = 0  # default open timeout for all instruments if not specified during init.
TIMEOUT = 8000  # default timeout of operation in ms for all instruments if not specified during init.
QUERY_DELAY = 0.001  # the default time in seconds to wait after each write operation for all if not specified.
READ_TERMINATION = '\n'  # default read termination for all instruments if not specified during init.
WRITE_TERMINATION = '\n'  # default write termination for all instruments if not specified during init.

# globals
rm = pyvisa.ResourceManager()

# base class of visa instruments
class VisaInstrument(BaseInstrument):
    """
    Base class of visa instruments.
    __init__(self, resource_name, read_termination=READ_TERMINATION, open_timeout=OPEN_TIMEOUT, **kwargs)

    * You may need to change several params such as read_termination and write_termination,
    to fit the API defined for the instrument.

    === General ===
    Always remember to make sure that read_termination & write_termination matches your instrument setting.

    === Connect as NI-VISA ===
    resource_name: visa address

    === Serial Connection ===
    resource_name: port name, such as 'COM1'
    When using serial connection, these kwargs are available:
        <int: baud_rate>
        <int: data_bits> (5<=data_bits<=8)
        <int: flow_control> (in visa.constants: VI_ASRL_FLOW_NONE = 0, VI_ASRL_FLOW_XON_XOFF = 1,
                            VI_ASRL_FLOW_RTS_CTS = 2, VI_ASRL_FLOW_DTR_DSR = 4)
        <Parity: parity> (in visa.constants.Parity: none, odd, even, mark, space)
        <StopBits: stop_bits> (in visa.constants.StopBits: one, one_and_a_half, two)

    === TCP/IP Socket Connection ===
    resource_name: TCPIP::host address::port::SOCKET
    """

    def __init__(self, resource_name, read_termination=READ_TERMINATION, write_termination=WRITE_TERMINATION,
                 timeout=TIMEOUT, open_timeout=OPEN_TIMEOUT, query_delay=QUERY_DELAY, *args, **kwargs):
        self.__inst = rm.open_resource(resource_name, read_termination=read_termination,
                                       write_termination=write_termination, open_timeout=open_timeout,
                                       timeout=timeout, query_delay=query_delay, **kwargs)
        self._resource_name = resource_name
        super(VisaInstrument, self).__init__()

    @property
    def resource_info(self):
        return self.__inst.resource_info

    @resource_info.setter
    def resource_info(self, value):
        raise AttributeError('attr "resource_info" is read-only.')

    @property
    def idn(self):
        return self.query('*IDN?')

    @idn.setter
    def idn(self, value):
        raise AttributeError('attr "IDN" is read-only.')

    # methods
    def check_connection(self):
        """
        Check if instrument is connected and able to query.
        :return: <bool> if instrument is connected.
        """
        try:
            idn = self.idn
            if idn:
                return True
            else:
                return False
        except pyvisa.VisaIOError:
            return False

    def command(self, cmd):
        """
        Write a VISA command without read back.
        You can use chained calling, such as: instrument.command(cmd1).command(cmd2).command(cmd3)...
        :param cmd: (str) VISA command
        :return: (BaseInstrument) self
        """
        self.__inst.write(cmd)
        return self  # reserved for chained calling

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

    def wait(self, duration):
        """
        Wait for duration in ms
        :param duration: (int|float) time to wait in ms
        """
        check_type(duration, (float, int), 'duration')
        check_range(duration, 0, 600000)
        sleep(duration/1000)
        return self
