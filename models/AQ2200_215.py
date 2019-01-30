from ..model_bases.ins_base import *
from ..model_bases.ins_types import *


class ModelAQ2200_215(VisaInstrument, TypeWM):
    model = ["AQ6150", "AQ6151"]
    brand = "Yokogawa"
    detail = {
        "Wavelength Range": "1270 ~ 1650 nm",
        "Power Accuracy": "+/-0.5 dB",
        "Input Power Range": "-40 ~ 10 dBm",
        "Safe Power": "+18 dBm"
    }

    def __init__(self, resource_name, **kwargs):
        super(ModelAQ2200_215, self).__init__(resource_name, **kwargs)