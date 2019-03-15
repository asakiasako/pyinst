from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePS(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePS, self).__init__()
        self._append_ins_type(InstrumentType.PS)
        self._max_volt = self._max_current = 0

    # Methods
    def enable(self, is_en=True):
        """
        Enable/disable power supply output.
        """
        self._raise_no_override()

    def disable(self):
        """
        Disable power supply output.
        """
        return self.enable(False)

    def is_enabled(self):
        """
        If the power supply output is enabled.
        """
        self._raise_no_override()

    def set_voltage(self, value):
        """
        Set voltage (limit).

        :Parameters: **value** - float|int, voltage value in V.
        """
        self._raise_no_override()

    def get_voltage(self):
        """
        Get voltage (limit) setting.

        :Returns: float|int, voltage value in V.
        """
        self._raise_no_override()

    def measure_voltage(self):
        """
        Get measured voltage.

        :Returns: float, voltage measured in V.
        """
        self._raise_no_override()

    def set_current(self, value):
        """
        Set current (limit).

        :Parameters: **value** - float|int, current value in A.
        """
        self._raise_no_override()

    def get_current(self):
        """
        Get current (limit) setting.

        :Returns: float, current value in A.
        """
        self._raise_no_override()

    def measure_current(self):
        """
        Get measured current value.

        :Returns: float, measured current value in A.
        """
        self._raise_no_override()

    def set_ocp(self, value):
        """
        :Parameters: **value** - float|int, OCP value in A.
        """
        self._raise_no_override()

    def get_ocp(self):
        """
        :Returns: float, OCP value in A.
        """
        self._raise_no_override()

    def set_ocp_status(self, status):
        """
        Enable/disable OCP function.

        :Parameters: **status** - True -> enable, False -> disable.
        """
        self._raise_no_override()

    def get_ocp_status(self):
        """
        :Returns: bool, if OCP function is enabled.
        """
        self._raise_no_override()

    def ocp_is_tripped(self):
        """
        Check if OCP is tripped and not cleared

        :Returns: bool, if OCP is tripped
        """
        self._raise_no_override()

    def clear_ocp(self):
        """
        Clear OCP tripped status.
        """
        self._raise_no_override()

    def set_ovp(self, value):
        """
        :Parameters: **value** - float|int, OVP value in V.
        """
        self._raise_no_override()

    def get_ovp(self):
        """
        :Returns: float, OVP value in V.
        """
        self._raise_no_override()

    def set_ovp_status(self, status):
        """
        Enable/disable OVP function.

        :Parameters: **status** - True -> enable, False -> disable.
        """
        self._raise_no_override()

    def get_ovp_status(self):
        """
        :Returns: bool, if OVP function is enabled.
        """
        self._raise_no_override()

    def ovp_is_tripped(self):
        """
        Check if OVP is tripped and not cleared

        :Returns: bool, if OVP is tripped
        """
        self._raise_no_override()

    def clear_ovp(self):
        """
        Clear OVP tripped status.
        """
        self._raise_no_override()