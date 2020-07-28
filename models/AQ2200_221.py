from ._AQ2200 import ModelAQ2200, ApplicationType
from ..instrument_types import TypeOPM
from ..constants import LIGHT_SPEED
import math


class ModelAQ2200_221(ModelAQ2200, TypeOPM):
    model = "AQ2200-221"
    brand = "Yokogawa"
    details = {
        "Wavelength Range": "800 nm - 1700 nm",
        "Input Power Range": "+10 dBm",
        "Average Time": "200 us"
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
        app_type = ApplicationType.Sensor
        super(ModelAQ2200_221, self).__init__(resource_name, app_type, slot, channel, **kwargs)
        # thresholds
        self._min_wl = 800
        self._max_wl = 1700
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
        self._min_avg_time = 0.2
        self._max_avg_time = 1000*10
        self._min_cal = -180
        self._max_cal = 200