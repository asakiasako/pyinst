class EmptyInstrument(object):
    def __init__(self, inst_name=None):
        self.__inst_name = inst_name

    def __getattr__(self, attr):
        err_str = 'Empty Instrument: %s' % self.__inst_name if self.__inst_name else 'Empty Instrument'
        raise RuntimeError(err_str, 'Empty Instrument')