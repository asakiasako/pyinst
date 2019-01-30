from .ins_type_bases import *


class TypePOLC(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypePOLC, self).__init__()
        self._append_ins_type(InstrumentType.POLC)

    def get_wavelength(self):
        """
        Get current wavelength setting (nm)
        :return: (float) wavelength
        """
        self._raise_no_rewrite()

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (float, int) wavelength in nm
        """
        self._raise_no_rewrite()
    
    def set_scrambling_param(self, mode, *params):
        """
        Set scrambling params.
        :param mode: (str) Scrambling mode.
        :param *params: (any, any, ...) Scrambling params.
        """
        self._raise_no_rewrite()
    
    def set_scrambling_state(self, mode, is_on):
        """
        Start or pause scrambling.
        :param mode: (str) Scrambling mode.
        :param ison: (bool) True->start  False->stop
        """
        self._raise_no_rewrite()

    def get_sop(self):
        """
        Get state of polarization, S1 S2 S3
        :return (S1, S2, S3)
        """
        self._raise_no_rewrite()

    def get_dop(self):
        """
        Query measured degree of polarization.
        """
        self._raise_no_rewrite()

    def set_sop(self, s1, s2, s3):
        self._raise_no_rewrite()

    def set_sop_in_degree(self, theta, phi):
        """
        :param theta: (float) 0 to 360
        :param phi: (float) 0 to 180
        """
        self._raise_no_rewrite()