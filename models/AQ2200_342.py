from ..model_bases.AQ2200 import *


class ModelAQ2200_342(ModelAQ2200, TypeVOA, TypeOPM):
    model = "AQ2200-342"
    brand = "Yokogawa"
    detail = {
        "Wavelength Range": "1260 to 1640 nm",
        "Att Range": "0 to 40 dB",
        "Max Input Power": "+23 dBm",
    }
    params = [
        {
            "name": "slot",
            "type": "int"
        },
        {
            "name": "channel",
            "type": "int",
            "range": [1, 2]
        }
    ]

    def __init__(self, resource_name, slot, channel, **kwargs):
        func_type = ApplicationType.ATTN
        super(ModelAQ2200_342, self).__init__(self, resource_name, func_type, slot, channel, **kwargs)
        # ranges
        self._min_wl = 1260
        self._max_wl = 1640
        self._min_avg_time = 10
        self._max_avg_time = 1000*100
        self._max_att = 60
