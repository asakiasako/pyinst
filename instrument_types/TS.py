from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeTS(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeTS, self).__init__()
        self._append_ins_type(InstrumentType.TS)
        self._ts_type = 'Undefined'
    
    @property
    def ts_type(self):
        return self._ts_type

    @ts_type.setter
    def ts_type(self, value):
        raise PermissionError('ts_type is immutable')

    def set_target_temp(self, value):
        """
        Set target temperature.

        :Parameter: **value** - float|int, target temperature value
        """
        self._raise_not_implemented()

    def get_target_temp(self):
        """
        Get target Temperature.

        :Returns: float, target temperature value.
        """
        self._raise_not_implemented()

    def get_current_temp(self):
        """
        Get measured current temperature.

        :Returns: float, current temperature value.
        """
        self._raise_not_implemented()

    def set_unit(self, unit):
        """
        Set temperature unit.

        :Parameters: **unit** - int, value of <enum 'TemperatureUnit'>
        """
        self._raise_not_implemented()

    def get_unit(self):
        """
        Get temperature unit.

        :Returns: int, value of <enum 'TemperatureUnit'>, unit
        """
        self._raise_not_implemented()