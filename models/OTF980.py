from .OTF970 import ModelOTF970


class ModelOTF980(ModelOTF970):
    model = "OTF-980"
    brand = "Santec"
    details = {
        "Wavelength Range": "1525 ~ 1610 nm",
        "Frequency Range": "186.2 ~ 196.58 THz",
        "Bandwidth @-3dB": "0.1 ~ 15 nm",
        "Max Input Power": "+27 dBm"
    }

    def __init__(self, resource_name, read_termination='\r\n', write_termination='\r\n', **kwargs):
        super(ModelOTF980, self).__init__(resource_name, read_termination=read_termination,
                                          write_termination=write_termination, **kwargs)
