from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeVOA(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeVOA, self).__init__()
        self._append_ins_type(InstrumentType.VOA)

    def get_max_att(self):
        """
        Get the max att setting value.

        :Returns: float, max att setting value in dB.
        """
        self._raise_not_implemented()

    def enable(self, status=True):
        """
        Enable/disable VOA output.

        :Parameters: **status** - bool, True(default) -> enable, False -> disable
        """
        self._raise_not_implemented()

    def disable(self):
        """
        Disable VOA output.
        """
        return self.enable(False)

    def is_enabled(self):
        """
        If VOA output is enabled.

        :Returns: bool, if VOA output is enabled.
        """
        self._raise_not_implemented()

    def get_att(self):
        """
        Get ATT setting value in dB.

        :Returns: float, att value in dB.
        """
        self._raise_not_implemented()

    def get_offset(self):
        """
        Get ATT offset value in dB.

        :Returns: float, offset value in dB.
        """
        self._raise_not_implemented()

    def get_wavelength(self):
        """
        :Returns: float, optical wavelength in nm
        """
        self._raise_not_implemented()

    def set_att(self, value):
        """
        Set att value in dB.

        :Parameters: **value** - float|int, att value in dB.
        """
        self._raise_not_implemented()

    def set_offset(self, value):
        """
        Set ATT offset value in dB.

        :Parameters: **value** - float|int, offset value in dB
        """
        self._raise_not_implemented()

    def set_wavelength(self, value):
        """
        Set wavelength value in nm.

        :Parameters: **value** - float|int, wavelength value in nm.
        """
        self._raise_not_implemented()
