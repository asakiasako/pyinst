from ..model_bases.ins_base import *
from ..model_bases.ins_types import *


class ModelTC3625(VisaInstrument, TypeTEC):
    model = "TC-36-25"
    brand = "TE Technology"

    def __init__(self, resource_name, write_termination='\r', read_termination='^', baud_rate=9600, data_bits=8,
                 flow_control=0, parity=visa.constants.Parity.none, stop_bits=visa.constants.StopBits.one, **kwargs):
        super(ModelTC3625, self).__init__(
            resource_name, write_termination=write_termination, read_termination=read_termination, baud_rate=baud_rate,
            data_bits=data_bits, flow_control=flow_control, parity=parity, stop_bits=stop_bits, no_idn=True, **kwargs
        )

    # param enconsulation

    def formed_query(self, cmd, value=0):
        """
        Send a command to instrument and read back immediately.
        :param cmd: (str) VISA command
        :return: (str) message sent from instrument
        """
        check_type(cmd, str, 'cmd')
        check_type(value, int, 'value')
        val_str = int_to_complement(value, 4)
        cmd_content = ('00%s%s' % (cmd, val_str)).lower()
        check_sum = calc_check_sum(cmd_content)
        check_sum_str = ('%02X' % check_sum)[-2:]
        cmd_str = ('*%s%s' % (cmd_content, check_sum_str)).lower()
        result_str = self.query(cmd_str)[1:]
        result_content = result_str[0:-2]
        result_check_sum = result_str[-2:]
        calced_check_sum = ('%02X' % calc_check_sum(result_content))[-2:]
        if result_check_sum.lower() != calced_check_sum.lower():
            raise ValueError("Response checksum not correct.")
        if result_content.lower() == ("X"*8).lower():
            raise ValueError("Command checksum not correct.")
        result_value = complement_to_int(int(result_content, 16), 4)
        return result_value

    def check_connection(self):
        unit = self.get_unit()
        if isinstance(unit, TempUnit):
            return True
        else:
            return False

    def set_target_temp(self, value):
        """
        Set the target tempreture.
        :param value: <float|int> target temperature value
        """
        check_type(value, (float, int), 'value')
        value = int(round(value*100))
        rtn_value = self.formed_query('1c', value)
        if value == rtn_value:
            return True
        else:
            return False

    def get_target_temp(self):
        """
        Get the target tempreture
        :return: <float> target temperature value
        """
        rtn_value = self.formed_query('03')
        temp_value = rtn_value/100
        return temp_value

    def get_current_temp(self):
        """
        Get the current measured temperature
        :return: <float> current measured temperature
        """
        rtn_value = self.formed_query('01')
        temp_value = rtn_value/100
        return temp_value

    def set_unit(self, unit):
        """
        Set temperature unit
        :param unit: <TempUnit> unit
        """
        rtn_value = self.formed_query('32', unit.value)
        if rtn_value == unit.value:
            return True
        else:
            return False

    def get_unit(self):
        """
        Get temperature unit
        :return: <TempUnit> unit
        """
        rtn_value = self.formed_query('4b')
        if rtn_value == 1:
            return TempUnit.C
        else:
            return TempUnit.F