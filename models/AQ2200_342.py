from ._AQ2200 import ModelAQ2200, ApplicationType
from ..instrument_types import TypeVOA, TypeOPM
from ..constants import LIGHT_SPEED
import math


class ModelAQ2200_342(ModelAQ2200, TypeVOA, TypeOPM):
    model = "AQ2200-342"
    brand = "Yokogawa"
    details = {
        "Wavelength Range": "1260 to 1640 nm",
        "Att Range": "0 to 60 dB",
        "Max Input Power": "+23 dBm",
    }
    params = [
        {
            "name": "slot",
            "type": "int",
            "min": 1,
            "max": 10
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
        # thresholds
        self._min_wl = 1260
        self._max_wl = 1640
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
        self._min_avg_time = 10
        self._max_avg_time = 1000*10
        self._min_cal = -180
        self._max_cal = 200
        self._max_att = 60
        self._min_offset = -200
        self._max_offset = 200
