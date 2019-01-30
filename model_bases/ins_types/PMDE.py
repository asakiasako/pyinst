from .ins_type_bases import *


class TypePMDE(TypeIns):
    def __init__(self, *args, **kwargs):
        super(TypePMDE, self).__init__()
        self._append_ins_type(InstrumentType.PMDE)

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (float, int) wavelength in nm
        """
        self._raise_no_rewrite()
    
    def set_pmd_value(self, pmd, sopmd):
        """
        Set pmd (dgd) and sopmd target (ps, ps**2)
        :param pmd: (float, int) DGD value in ps
        :param sopmd: (float, int) 2nd order pmd in ps**2
        """
        self._raise_no_rewrite()