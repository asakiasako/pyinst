from ._VsaOMA import ModelVsaOMA

class ModelM8292A(ModelVsaOMA):
    model = "M8292A"
    brand = "Keysight"
    details = {
        "Maximum detectable symbol rate": "74 GHz",
        "Wavelength range": "1527.60 to 1570.01 nm (196.25 to 190.95 THz)",
        }

    def __init__(self, resource_name, **kwargs):
        super(ModelM8292A, self).__init__(resource_name, **kwargs)
        
    