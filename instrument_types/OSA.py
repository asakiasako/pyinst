from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeOSA(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeOSA, self).__init__()
        self._append_ins_type(InstrumentType.OSA)

    # OSA operate logic is different among different OSA vendors, so no general methods will be provided.