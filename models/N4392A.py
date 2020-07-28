from ._VsaOSA import ModelVsaOSA
from ..instrument_types import TypeOMA

class ModelN4392A(ModelVsaOSA):
    model = "N4392A"
    brand = "Keysight"
    details = {
        "Optical receiver frequency range": "31 GHz",
        "Wavelength range (Option 100)": "1527.6 ~ 1565.5 nm (196.25 ~ 191.50 THz)",
        "Wavelength range (Option 110)": "1570.01 ~ 1608.76 nm (190.95 ~ 186.35 THz)"
    }

    def __init__(self, resource_name, **kwargs):
        super(ModelN4392A, self).__init__(resource_name, **kwargs)
