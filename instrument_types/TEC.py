from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeTEC(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeTEC, self).__init__()
        self._append_ins_type(InstrumentType.TEC)

    def set_target_temp(self, value):
        """
        Set the target Temperature.
        :param value: <float|int> target temperature value
        """
        self._raise_no_override()

    def get_target_temp(self):
        """
        Get the target Temperature
        :return: <float> target temperature value
        """
        self._raise_no_override()

    def get_current_temp(self):
        """
        Get the current measured temperature
        :return: <float> current measured temperature
        """
        self._raise_no_override()

    def set_unit(self, unit):
        """
        Set temperature unit
        :param unit: <TemperatureUnit> unit
        """
        self._raise_no_override()

    def get_unit(self):
        """
        Get temperature unit
        :return: <TemperatureUnit> unit
        """
        self._raise_no_override()