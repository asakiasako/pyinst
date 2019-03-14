from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypePMDE
from ..utils import check_range, check_type


class ModelPMD1000(VisaInstrument, TypePMDE):
    model = "PMD-1000"
    brand = "General Photonics"
    details = {
        "Wavelength Range": "C Band",
        "Insertion Loss": "5.5 dB",
        "1st Order PMD Range": "0.36 to 182.4 ps",
        "2nd Order PMD Range": "8100 ps2"
    }

    def __init__(self, resource_name, write_termination='', read_termination='#', **kwargs):
        super(ModelPMD1000, self).__init__(
            resource_name, write_termination=write_termination, read_termination=read_termination, **kwargs
        )

    def _formatted_query(self, cmd):
        return self.query(cmd)[1:]

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (float, int) wavelength in nm
        """
        c = 299792.458
        freq = c/wavelength
        # Notice that the starting freq of channels of PMD is different from our module.
        ch = round((freq - 191.6)/0.05)+1
        return self.command('*CHC %03d#' % ch)
    
    def set_pmd_value(self, pmd, sopmd):
        """
        Set pmd (dgd) and sopmd target (ps, ps**2)
        :param pmd: (float, int) DGD value in ps
        :param sopmd: (float, int) 2nd order pmd in ps**2
        """
        check_type(pmd, (int, float), 'pmd')
        check_type(sopmd, (int, float), 'sopmd')
        check_range(pmd, 0.36, 182.4)
        check_range(sopmd, 0, 8319.9)
        return self.command('*PMD:CON %.2f,%.2f#' % (pmd, sopmd))