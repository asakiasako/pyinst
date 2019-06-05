from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeSW(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeSW, self).__init__()
        self._append_ins_type(InstrumentType.SW)

    def set_channel(self, channel):
        """
        Set channel.

        :Parameter: **channel** - int, channel number (1 based)
        """
        self._raise_not_implemented()

    def get_channel(self):
        """
        Get selected channel.

        :Returns: int, selected channel (1 based)
        """
        self._raise_not_implemented()