from .VSA89600 import ModelVSA89600
from ..instrument_types import TypeOMA


class ModelVsaOSA(ModelVSA89600, TypeOMA):

    def __init__(self, resource_name, **kwargs):
        super(ModelVsaOSA, self).__init__(resource_name, **kwargs)

    def smart_setup(self, execute=True, freq=None, symbol_rate=None, fine_tune_symbol_rate=None, demodulation_format=None, polarization=None, pre_set_layout=None):
        """
        execute: if execute after setup. if fause, settings will be set, but no execution will be done.
        """
        if freq:
            self.command(':OMA:SMartSEtup:CarrierFrequency:FRErequency ' + str(freq*10**12))
        if symbol_rate:
            self.command(':OMA:SMartSEtup:SYMBRate ' + str(symbol_rate*10**9))
        if fine_tune_symbol_rate is not None:
            if not isinstance(fine_tune_symbol_rate, bool):
                raise TypeError('fine_tune_symbol_rate should be bool.')
            self.command(':OMA:SMartSEtup:FINetuneSymbolRate %d' % int(fine_tune_symbol_rate))
        if demodulation_format:
            FORMATS = [
                "Qam16", "Qam32", "Qam64", "Qam256", "Qpsk", 
                "DifferentialQpsk", "Pi4DifferentialQpsk", 
                "OffsetQpsk", "Bpsk", "Psk8", "Msk", "Msk2", 
                "Fsk2", "Fsk4", "DvbQam16", "DvbQam32", 
                "DvbQam64", "Vsb8", "Vsb16", "Edge", "Fsk8", 
                "Fsk16", "Qam128", "DifferentialPsk8", 
                "Qam512", "Qam1024", "Apsk16", "Apsk16Dvb", 
                "Apsk32", "Apsk32Dvb", "DvbQam128", 
                "DvbQam256", "Pi8DifferentialPsk8", "CpmFM", 
                "Star16Qam", "Star32Qam", "CustomApsk", 
                "ShapedOffsetQpsk"
            ]
            if demodulation_format not in FORMATS:
                raise ValueError('Invalid modulation demodulation_format: %r' % demodulation_format)
            self.command(':OMA:SMartSEtup:FORMat "%s"' % format)
        if polarization:
            POLARIZATIONS = ["Single", "Dual", "Auto"]
            if not polarization in POLARIZATIONS:
                raise ValueError('Invalid polarization: %r' % polarization)
            self.command(':OMA:SMartSEtup:POLarization "%s"' % polarization)
        if pre_set_layout is None:
            if not isinstance(pre_set_layout, bool):
                raise TypeError('pre_set_layout should be bool.')
            self.command(':OMA:SMartSEtup:PREsetLAyout %s' + pre_set_layout)
        if execute:
            self.command(':OMA:SMartSEtup:PERformProposedActions')
