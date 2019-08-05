from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeOMA(BaseInstrumentType):
    """
    Optical Modulation Analyser.
    """
    def __init__(self, *args, **kwargs):
        super(TypeOMA, self).__init__()
        self._append_ins_type(InstrumentType.OMA)

    def run(self):
        """
        Run OMA, the test data will refresh after OMA started running.
        """
        self._raise_not_implemented()

    def stop(self):
        """
        Pause OMA, the test data will stop refreshing.
        """
        self._raise_not_implemented()

    def get_trace_items(self, trace):
        """
        Get names of all test items for a specified trace.

        :Parameters: **trace** - index of trace, 1 based.

        :Returns: A list of trace item names.
        """
        self._raise_not_implemented()

    def get_trace_values(self, trace):
        """
        Get values of all test items for the specified trace.

        :Parameters: **trace** - index of trace, 1 based.

        :Returns: A list of values of all test items.

        :Return Type: list[float]
        """
        self._raise_not_implemented()

    def get_trace_units(self, trace):
        """
        Get units of all test items for the specified trace.

        :Parameters: **trace** - index of trace, 1 based.

        :Returns: A list of units of all test items.

        :Return Type: list[str]
        """
        self._raise_not_implemented()

    def get_formatted_data(self, trace):
        """
        Get formatted data include test items, values, and units, for a specified trace.

        :Parameters: **trace** - index of trace, 1 based.

        :Returns: Mapping of test item name to tuple(value, unit).

        :Return Type: dict{item_name => tuple(float value, str unit)}
        """
        self._raise_not_implemented()
