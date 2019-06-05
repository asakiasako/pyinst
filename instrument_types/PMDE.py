from ._BaseInstrumentType import BaseInstrumentType, InstrumentType


class TypePMDE(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypePMDE, self).__init__()
        self._append_ins_type(InstrumentType.PMDE)

    def set_wavelength(self, wavelength):
        """
        Set wavelength in nm.
        
        :Parameters: **wavelength** - float, wavelength in nm.
        """
        self._raise_not_implemented()
    
    def set_pmd_value(self, pmd, sopmd):
        """
        Set PMD(DGD) and SOPMD target value.

        :Parameters: 
            - **pmd** - float|int, DGD value in ps
            - **sopmd** - float|int, 2nd order pmd in ps**2
        """
        self._raise_not_implemented()