from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypeVOA(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeVOA, self).__init__()
        self._append_ins_type(InstrumentType.VOA)
        # thresholds
        self._min_wl = None
        self._max_wl = None
        self._min_freq = None
        self._max_freq = None
        self._max_att = None
        self._min_offset = None
        self._max_offset = None

    # -- properties --
    # min_wavelength
    @ property
    def min_wavelength(self):
        if self._min_wl is None:
            self._raise_not_implemented()
        else:
            return self._min_wl

    @ min_wavelength.setter
    def min_wavelength(self, value):
        raise AttributeError('Attribute "min_wavelength" is read-only.')

    # max_wavelength
    @ property
    def max_wavelength(self):
        if self._max_wl is None:
            self._raise_not_implemented()
        else:
            return self._max_wl

    @ max_wavelength.setter
    def max_wavelength(self, value):
        raise AttributeError('Attribute "max_wavelength" is read-only.')

    # min_frequency
    @ property
    def min_frequency(self):
        if self._min_freq is None:
            self._raise_not_implemented()
        else:
            return self._min_freq

    @ min_frequency.setter
    def min_frequency(self, value):
        raise AttributeError('Attribute "min_frequency" is read-only.')

    # max_frequency
    @ property
    def max_frequency(self):
        if self._max_freq is None:
            self._raise_not_implemented()
        else:
            return self._max_freq

    @ max_frequency.setter
    def max_frequency(self, value):
        raise AttributeError('Attribute "max_frequency" is read-only.')

    # min_offset
    @ property
    def min_offset(self):
        if self._min_offset is None:
            self._raise_not_implemented()
        else:
            return self._min_offset

    @ min_offset.setter
    def min_offset(self, value):
        raise AttributeError('Attribute "min_offset" is read-only.')

    # max_offset
    @ property
    def max_offset(self):
        if self._max_offset is None:
            self._raise_not_implemented()
        else:
            return self._max_offset

    @ max_offset.setter
    def max_offset(self, value):
        raise AttributeError('Attribute "max_offset" is read-only.')

    # max_att
    @ property
    def max_att(self):
        if self._max_att is None:
            self._raise_not_implemented()
        else:
            return self._max_att

    @ max_att.setter
    def max_att(self, value):
        raise AttributeError('Attribute "max_att" is read-only.')

    # -- methods --
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
    
    def get_frequency(self):
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

    def set_frequency(self, value):
        self._raise_not_implemented()