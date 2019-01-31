from ..model_bases.AQ2200 import *


class ModelAQ2200_311A(ModelAQ2200, TypeVOA):
    model = "AQ2200-311A"
    brand = "Yokogawa"
    detail = {
        "Wavelength Range": "1200 to 1700 nm",
        "Att Range": "0 to 60 dB"
    }
    params = [
        {
            "name": "slot",
            "type": "int"
        }
    ]

    def __init__(self, resource_name, slot, **kwargs):
        func_type = ApplicationType.ATTN
        super(ModelAQ2200_311A, self).__init__(self, resource_name, func_type, slot, **kwargs)
        # ranges
        self._min_wl = 1200
        self._max_wl = 1700
        self._max_att = 60

