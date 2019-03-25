from ..base_models.AQ2200 import ModelAQ2200, ApplicationType
from ..instrument_types import TypeVOA, TypeOPM


class ModelAQ2200_342(ModelAQ2200, TypeVOA, TypeOPM):
    model = "AQ2200-342"
    brand = "Yokogawa"
    details = {
        "Wavelength Range": "1260 to 1640 nm",
        "Att Range": "0 to 40 dB",
        "Max Input Power": "+23 dBm",
    }
    params = [
        {
            "name": "slot",
            "type": "int",
            "min": 1
        },
        {
            "name": "channel",
            "type": "int",
            "options": [1, 2]
        }
    ]

    def __init__(self, resource_name, slot, channel, **kwargs):
        func_type = ApplicationType.ATTN
        super(ModelAQ2200_342, self).__init__(resource_name, func_type, slot, channel, **kwargs)
        # ranges
        self._min_wl = 1260
        self._max_wl = 1640
        self._min_avg_time = 10
        self._max_avg_time = 1000*10
        self._max_att = 60
