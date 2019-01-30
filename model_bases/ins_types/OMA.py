from .ins_type_bases import *


class TypeOMA(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeOMA, self).__init__()
        self._append_ins_type(InstrumentType.OMA)

    def run(self):
        self._raise_no_override()

    def pause(self):
        self._raise_no_override()

    def get_trace_items(self, trace):
        """
        Get all the test item names for the specified trace.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (list of str) trace item names.
        """
        self._raise_no_override()

    def get_trace_values(self, trace):
        """
        Get all the test values for the specified trace.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (list of float) trace item values.
        """
        self._raise_no_override()

    def get_trace_units(self, trace):
        """
        Get all the units for the specified trace.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (list of str) units of item values.
        """
        self._raise_no_override()

    def get_formatted_data(self, trace):
        """
        Get a formatted data include test items, values, and units.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (dict) { str:item1: (float:value, str:unit), ...}
        """
        self._raise_no_override()
