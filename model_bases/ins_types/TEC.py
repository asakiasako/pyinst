from .ins_type_bases import *


class TypeTEC(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeTEC, self).__init__()
        self._append_ins_type(InstrumentType.TEC)

    def set_target_temp(self, value):
        """
        Set the target tempreture.
        :param value: <float|int> target temperature value
        """
        self._raise_no_rewrite()

    def get_target_temp(self):
        """
        Get the target tempreture
        :return: <float> target temperature value
        """
        self._raise_no_rewrite()

    def get_current_temp(self):
        """
        Get the current measured temperature
        :return: <float> current measured temperature
        """
        self._raise_no_rewrite()

    def set_unit(self, unit):
        """
        Set temperature unit
        :param unit: <TempUnit> unit
        """
        self._raise_no_rewrite()

    def get_unit(self):
        """
        Get temperature unit
        :return: <TempUnit> unit
        """
        self._raise_no_rewrite()