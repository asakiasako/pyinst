from ._VisaInstrument import VisaInstrument


class ModelVSA89600(VisaInstrument):
    """
    This is the base model of Keysight VSA89600 software
    """

    def __init__(self, resource_name, encoding='latin1', **kwargs):
        super(ModelVSA89600, self).__init__(resource_name, encoding=encoding, **kwargs)

    # param encapsulation

    # Methods
    def run(self):
        """
        Run OMA
        """
        self.command(':INIT:RES')
        
    def stop(self):
        """
        Pause OMA
        """
        self.command(':INIT:ABOR')
    
    def get_trace_item_names(self, trace):
        """
        Get all the test item names for the specified trace.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (list of str) trace item names.
        """
        if not isinstance(trace, int):
            raise TypeError('trace should be int')
        if not trace >= 1:
            raise ValueError('trace starts from 1')
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
        if not isinstance(trace, int):
            raise TypeError('trace should be int')
        if not trace >= 1:
            raise ValueError('trace starts from 1')
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
        if not isinstance(trace, int):
            raise TypeError('trace should be int')
        if not trace >= 1:
            raise ValueError('trace starts from 1')
        unit_str = self.query(':TRACe%d:DATA:TABLe:UNIT?' % trace)
        unit_list = unit_str.split(',')        
        unit_list = list(map(lambda x: x.strip('"'), unit_list))
        return unit_list

    def get_trace_data(self, trace):
        """
        Get a formatted data include test item_names, values, and units.
        :param trace: (int) index of trace, 1 based from A. For example: A->1, E->5
        :return: (dict) { str:item1: (float:value, str:unit), ...}
        """
        names = self.get_trace_item_names(trace)
        values = self.get_trace_values(trace)
        units = self.get_trace_units(trace)
        ilen = len(names)
        res = {}
        for i in range(ilen):
            res[names[i]] = (values[i], units[i])
        return res
