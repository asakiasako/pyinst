import pyvisa
from ._BaseInstrument import BaseInstrument

# define const
OPEN_TIMEOUT = 0  # default open timeout for all instruments if not specified during init.
TIMEOUT = 2000  # default timeout of operation in ms for all instruments if not specified during init.
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
    kwargs are directly passed to rm.open_resource
    """

    def __init__(self, resource_name, read_termination=READ_TERMINATION, write_termination=WRITE_TERMINATION,
                 timeout=TIMEOUT, open_timeout=OPEN_TIMEOUT, query_delay=QUERY_DELAY, **kwargs):
        self.__inst = rm.open_resource(resource_name, read_termination=read_termination,
                                       write_termination=write_termination, open_timeout=open_timeout,
                                       timeout=timeout, query_delay=query_delay, **kwargs)
        self.__resource_name = resource_name
        super(VisaInstrument, self).__init__()

    @property
    def resource_name(self):
        return self.__resource_name

    @property
    def resource_info(self):
        """
        Get extended information of visa resource.
        """
        return self.__inst.resource_info()

    @property
    def idn(self):
        """
        Get module IDN
        """
        return self.query('*IDN?')

    @property
    def opc(self):
        return self.query('*OPC?')

    # methods
    def check_connection(self):
        """
        Check if instrument is connected and able to communicate with.
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

    def read(self, bin=False):
        """
        Read VISA message from instrument.
        Since it's always used after a 'command' method, it's better to use 'query' method instead of 2 separate 'command' and 'read'.
        :return: (str) message sent from instrument
        """
        return self.__inst.read_binary_values('B') if bin else self.__inst.read()

    def query(self, cmd, bin=False):
        """
        Send a command to instrument and read back immediately.
        :param cmd: (str) VISA command
        :param bin: (bool) if true, get data in binary.
        :return: (str) message sent from instrument
        """
        return self.__inst.query_binary_values(cmd, 'B') if bin else self.__inst.query(cmd)

    def close(self):
        """
        Close the session of visa resource
        """
        self.__inst.close()

