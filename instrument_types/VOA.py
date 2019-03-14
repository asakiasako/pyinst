from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeVOA(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeVOA, self).__init__()
        self._append_ins_type(InstrumentType.VOA)

    def get_max_att(self):
        """
        Get the max att setting value
        :return: (float) max att setting value
        """
        self._raise_no_override()

    def enable(self, status=True):
        """
        Set VOA output enabled/disabled.
        :param status: (bool=True)
        """
        self._raise_no_override()

    def disable(self):
        """
        Set VOA output disabled.
        """
        return self.enable(False)

    def is_enabled(self):
        """
        Get enable status of VOA.
        :return: (bool) if VOA output is enabled.
        """
        self._raise_no_override()

    def get_att(self):
        """
        Get att value in dB.
        :return: (float) att value in dB
        """
        self._raise_no_override()

    def get_offset(self):
        """
        Get offset value in dB.
        :return: (float) offset value in dB
        """
        self._raise_no_override()

    def get_wavelength(self):
        """
        :return: (float) optical wavelength in nm
        """
        self._raise_no_override()

    def set_att(self, value):
        """
        Set att value in dB.
        :param value: (float|int) att value in dB
        """
        self._raise_no_override()

    def set_offset(self, value):
        """
        Set offset value in dB.
        :param value: (float|int) offset value in dB
        """
        self._raise_no_override()

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.
        :param value: (float|int) wavelength value in nm
        """
        self._raise_no_override()
