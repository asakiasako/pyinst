class BaseInstrument(object):
    """
    Base class of instruments.
    """
    # instrument information
    brand = ""
    model = ""
    details = {}
    params = []

    def __init__(self, *args, **kwargs):
        super(BaseInstrument, self).__init__()

    def __str__(self):
        return "<{} object>\n    Inst Type: {}\n    resource name: {}\n".format(
            self.__class__.__name__, str(self.ins_type), self.resource_name)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        raise NotImplementedError('This instrument model lacks "close" method.')

    @property
    def resource_name(self):
        return self._resource_name

    @resource_name.setter
    def resource_name(self, value):
        raise AttributeError('attr "resource_name" is read-only.')
    
    def check_connection(self):
        raise NotImplementedError('This instrument model lacks "check_connection" method.')
        