from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeOSA(BaseInstrumentType):
    """
    Optical Spectrum Analyser.

    The operating logic is different between different vendors/models, so no general methods is defined here.
    """
    def __init__(self, *args, **kwargs):
        super(TypeOSA, self).__init__()
        self._append_ins_type(InstrumentType.OSA)
