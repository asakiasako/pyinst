from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeTEC(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeTEC, self).__init__()
        self._append_ins_type(InstrumentType.TEC)

    def set_target_temp(self, value):
        """
        Set target temperature.

        :Parameter: **value** - float|int, target temperature value
        """
        self._raise_no_override()

    def get_target_temp(self):
        """
        Get target Temperature.

        :Returns: float, target temperature value.
        """
        self._raise_no_override()

    def get_current_temp(self):
        """
        Get measured current temperature.

        :Returns: float, current temperature value.
        """
        self._raise_no_override()

    def set_unit(self, unit):
        """
        Set temperature unit.

        :Parameters: **unit** - <enum 'TemperatureUnit'>
        """
        self._raise_no_override()

    def get_unit(self):
        """
        Get temperature unit.

        :Returns: <enum 'TemperatureUnit'>, unit
        """
        self._raise_no_override()