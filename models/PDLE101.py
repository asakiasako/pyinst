from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypePDLE
from ..utils import check_range, check_type
import visa


class ModelPDLE101(VisaInstrument, TypePDLE):
    model = "PDLE-101"
    brand = "General Photonics"
    details = {
        "Insertion Loss (Max.)": "3 dB at PDL=0",
        "PDL Range": "0.1 to 20 dB",
        "PDL Resolution": "0.1 dB",
        "PDL Accuracy": "2 ± (0.1 dB +1% of PDL)"
    }

    def __init__(self, resource_name, write_termination='', read_termination='#', baud_rate=9600, data_bits=8,
                 flow_control=0, parity=visa.constants.Parity.none, stop_bits=visa.constants.StopBits.one, **kwargs):
        super(ModelPDLE101, self).__init__(
            resource_name, write_termination=write_termination, read_termination=read_termination, baud_rate=baud_rate,
            data_bits=data_bits, flow_control=flow_control, parity=parity, stop_bits=stop_bits, **kwargs
        )

    def _formatted_query(self, cmd):
        return self.query(cmd)[1:]
    
    def get_wavelength(self):
        """
        Get current wavelength setting (nm)
        :return: (float) wavelengthwavelength
        """
        wl_str = self._formatted_query('*WAV?')
        return float(wl_str)

    def set_wavelength(self, wavelength):
        """
        Set wavelength setting (nm)
        :param wavelength: (int) wavelength in nm
        """
        check_type(wavelength, int, 'wavelength')
        check_range(wavelength, 1520, 1570)
        backcode = self._formatted_query('*WAV %d#' % wavelength)
        if backcode != 'E00':
            raise visa.Error('PDLE-101 Error: %s' % backcode)
    
    def get_pdl_value(self):
        """
        Get current pdl value
        :return: (float) pdl value in dB
        """
        return float(self._formatted_query('*PDL?'))

    def set_pdl_value(self, value):
        """
        Set pdl value
        :param value: (float, int) pdl value in dB
        """
        check_type(value, (float, int), 'value')
        check_range(value, 0.1, 20)
        cmd_str = '*PDL %.1f#' % value
        backcode = self._formatted_query(cmd_str)
        if backcode != 'E00':
            raise visa.Error('PDLE-101 Error: %s' % backcode)
