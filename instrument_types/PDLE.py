from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePDLE(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePDLE, self).__init__()
        self._append_ins_type(InstrumentType.PDLE)

    def get_wavelength(self):
        """
        Get current wavelength setting (nm)
        :return: (float) wavelength
        """
        self._raise_no_override()

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (float, int) wavelength in nm
        """
        self._raise_no_override()
    
    def get_pdl_value(self):
        """
        Get current pdl value
        :return: (float) pdl value in dB
        """
        self._raise_no_override()

    def set_pdl_value(self, value):
        """
        Set pdl value
        :param value: (float, int) pdl value in dB
        """
        self._raise_no_override()