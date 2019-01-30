from .ins_type_bases import *


class TypeSW(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypeSW, self).__init__()
        self._append_ins_type(InstrumentType.SW)

    def set_channel(self, channel):
        """
        Set channel.
        :param channel: (int) channel number (1 based)
        """
        self._raise_no_override()

    def get_channel(self):
        """
        Get selected channel.
        :return: (int) selected channel (1 based)
        """
        self._raise_no_override()