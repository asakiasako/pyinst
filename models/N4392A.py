from ..model_bases.ins_base import *
from ..model_bases.ins_types import *


class ModelN4392A(VisaInstrument, TypeOMA):
    model = "N4392A"
    brand = "Keysight"
    detail = {
        "Optical receiver frequency range": "31 GHz",
        "Wavelength range (Option 100)": "1527.6 ~ 1565.5 nm (196.25 ~ 191.50 THz)",
        "Wavelength range (Option 110)": "1570.01 ~ 1608.76 nm (190.95 ~ 186.35 THz)"
    }

    def __init__(self, resource_name, **kwargs):
        super(ModelN4392A, self).__init__(resource_name, **kwargs)
        self._trace = None
        self._items = []
        self._units = []

    # param encapsulation

    # Methods
    def run(self):
        """
        Run OMA
        """
        self.command(':INIT:RES')
        
    def pause(self):
        """
        Pause OMA
        """
        self.command(':INIT:ABOR')
    
    def get_trace_items(self, trace):
        """
        Get all the test item names for the specified trace.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (list of str) trace item names.
        """
        check_type(trace, int, 'trace')
        check_range(trace, 1, float('inf'))
        item_str = self.query(':TRACe%d:DATA:TABLe:NAME?' % trace)
        item_list = item_str.split(',')
        item_list = list(map(lambda x: x.strip('"'), item_list))
        return item_list

    def get_trace_values(self, trace):
        """
        Get all the test values for the specified trace.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (list of float) trace item values.
        """
        check_type(trace, int, 'trace')
        check_range(trace, 1, float('inf'))
        value_str = self.query(':TRACe%d:DATA:TABLe?' % trace)
        value_list = value_str.split(',')
        value_list = list(map(lambda x: float(x), value_list))
        return value_list

    def get_trace_units(self, trace):
        """
        Get all the units for the specified trace.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (list of str) units of item values.
        """
        check_type(trace, int, 'trace')
        check_range(trace, 1, float('inf'))
        unit_str = self.query(':TRACe%d:DATA:TABLe:UNIT?' % trace)
        unit_list = unit_str.split(',')        
        unit_list = list(map(lambda x: x.strip('"'), unit_list))
        return unit_list

    def set_current_trace(self, trace):
        """
        Set current trace
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        """
        check_type(trace, int, 'trace')
        check_range(trace, 1, float('inf'))
        self._trace = trace
        self._items = self.get_trace_items(trace)
        self._units = self.get_trace_units(trace)

    def get_formatted_data(self, trace):
        """
        Get a formatted data include test items, values, and units.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (dict) { str:item1: (float:value, str:unit), ...}
        """
        if trace != self._trace:
            self.set_current_trace(trace)
            return self.get_formatted_data(trace)
        else:
            values = self.get_trace_values(trace)
            rdata = {}
            for i in range(len(self._items)):
                rdata[self._items[i]] = (values[i], self._units[i])
            return rdata

