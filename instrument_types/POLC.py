from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePOLC(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePOLC, self).__init__()
        self._append_ins_type(InstrumentType.POLC)

    def get_wavelength(self):
        """
        Get the setting value of wavelength in nm.
        
        :Returns: float, wavelength setting value in nm.
        """
        self._raise_not_implemented()

    def set_wavelength(self, wavelength):
        """
        Set wavelength in nm.
        
        :Parameters: **wavelength** - float, wavelength in nm.
        """
        self._raise_not_implemented()
    
    def get_frequency(self):
        self._raise_not_implemented()

    def set_frequency(self, wavelength):
        self._raise_not_implemented()
        
    def set_scrambling_param(self, mode, *params):
        """
        Set scrambling params.

        :Parameters:
            - **mode** - str, scrambling mode.
            - **params** - list(any), scrambling params.
        """
        self._raise_not_implemented()
    
    def set_scrambling_state(self, mode, is_on):
        """
        Start or pause scrambling.

        :Parameters:
            - **mode** - str, scrambling mode.
            - **is_on** - bool, True -> start, False -> stop.
        """
        self._raise_not_implemented()

    def get_sop(self):
        """
        Get state of polarization: S1, S2, S3

        :Returns: tuple(S1, S2, S3)
        """
        self._raise_not_implemented()

    def get_dop(self):
        """
        Get degree of polarization.

        :Returns: tuple(float theta, float phi)
        """
        self._raise_not_implemented()

    def set_sop(self, s1, s2, s3):
        """
        Set state of polarization: S1, S2, S3
        """
        self._raise_not_implemented()

    def set_sop_in_degree(self, theta, phi):
        """
        Set degree of polarization.

        :Parameters:
            - **theta** - float, 0 to 360
            - **phi** - float, 0 to 180
        """
        self._raise_not_implemented()