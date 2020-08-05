from abc import ABC, abstractmethod

class BaseInstrument(ABC):
    """
    Base class of instruments.
    """
    # instrument information
    brand = "No Brand"
    model = "No Model"
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

    @abstractmethod
    def resource_name(self):
        """
        Visa Resource Name or other address.
        """
    
    @abstractmethod
    def check_connection(self):
        """
        Check connection
        """