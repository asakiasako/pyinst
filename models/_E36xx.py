from ._VisaInstrument import VisaInstrument
from ..instrument_types import TypePS


class ModelE36xx(VisaInstrument, TypePS):
    def __init__(self, resource_name, **kwargs):
        super(ModelE36xx, self).__init__(resource_name, **kwargs)
        self._range = None
        
    def enable(self, status=True):
        """
        Enable power supply output or not.
        :param status: (bool) enable status of power supply output
        """
        if not isinstance(status, bool):
            raise TypeError('Enable status should be bool')
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
        if not isinstance(value, (float, int)):
            raise TypeError('Voltage value should be number')
        if not 0 <= value <= self._range['max_volt']:
            raise ValueError('Exceed max voltage limit')
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
        if not isinstance(value, (int, float)):
            raise TypeError('Current value should be number')
        if not 0 <= value <= self._range["max_current"]:
            raise ValueError('Current value out of range')
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
        if not isinstance(value, (float, int)):
            raise TypeError('OCP value should be number')
        if not 0 <= value <= 22:
            raise ValueError('OCP value out of range')
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
        if not isinstance(status, bool):
            raise TypeError('OCP status should be bool')
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
        if not isinstance(value, (float, int)):
            raise TypeError('OVP value should be number')
        if not 0 <= value <= 22:
            raise ValueError('OVP value out of range')
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
        if not isinstance(status, bool):
            raise TypeError('OVP status should be bool')
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
