from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePS(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePS, self).__init__()
        self._append_ins_type(InstrumentType.PS)
        self._max_volt = self._max_current = 0

    # Methods
    def enable(self, status=True):
        """
        Enable power supply output or not.
        :param status: (bool) enable status of power supply output
        """
        self._raise_no_override()

    def disable(self):
        """
        Disable power supply output.
        """
        return self.enable(False)

    def is_enabled(self):
        """
        Get the power supply output enable status.
        :return: (bool) if power supply output is enabled.
        """
        self._raise_no_override()

    def set_voltage(self, value):
        """
        Set voltage (limit).
        :param value: (float|int) voltage value in V
        """
        self._raise_no_override()

    def get_voltage(self):
        """
        Get voltage (limit) setting.
        :return: (float) voltage value in V
        """
        self._raise_no_override()

    def measure_voltage(self):
        """
        Query voltage measured
        :return: (float) voltage measured in V
        """
        self._raise_no_override()

    def set_current(self, value):
        """
        Set current (limit).
        :param value: (float|int) current value in A
        """
        self._raise_no_override()

    def get_current(self):
        """
        Get current (limit) setting.
        :return: (float) current value in A
        """
        self._raise_no_override()

    def measure_current(self):
        """
        Query current measured.
        :return: (float) current measured in A
        """
        self._raise_no_override()

    def set_ocp(self, value):
        """
        :param value: (float|int) ocp value in A
        """
        self._raise_no_override()

    def get_ocp(self):
        """
        :return: (float) ocp value in A
        """
        self._raise_no_override()

    def set_ocp_status(self, status):
        """
        :param status: (bool) if ocp is enabled
        """
        self._raise_no_override()

    def get_ocp_status(self):
        """
        :return: (bool) if ocp is enabled
        """
        self._raise_no_override()

    def ocp_is_tripped(self):
        """
        Check if the over-current protection circuit is tripped and not cleared
        :return: (bool) if ocp is tripped
        """
        self._raise_no_override()

    def clear_ocp(self):
        """
        clear ocp status
        """
        self._raise_no_override()

    def set_ovp(self, value):
        """
        :param value: (float|int) ovp value in V
        """
        self._raise_no_override()

    def get_ovp(self):
        """
        :return: (float) ovp value in V
        """
        self._raise_no_override()

    def set_ovp_status(self, status):
        """
        :param status: (bool) if ovp is enabled
        """
        self._raise_no_override()

    def get_ovp_status(self):
        """
        :return: (bool) if ovp is enabled
        """
        self._raise_no_override()

    def ovp_is_tripped(self):
        """
        Check if the over-voltage protection circuit is tripped and not cleared
        :return: (bool) if ovp is tripped
        """
        self._raise_no_override()

    def clear_ovp(self):
        """
        clear OVP status
        """
        self._raise_no_override()