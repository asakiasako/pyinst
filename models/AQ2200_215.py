from ._AQ2200 import ModelAQ2200, ApplicationType
from ..instrument_types import TypeOPM
from ..constants import LIGHT_SPEED
import math


class ModelAQ2200_215(ModelAQ2200, TypeOPM):
    model = "AQ2200-215"
    brand = "Yokogawa"
    details = {
        "Wavelength Range": "970 to 1660 nm",
        "Input Power Range": "-70 to +30 dBm",
        "Average Time": "100us"
    }
    params = [
        {
            "name": "slot",
            "type": "int",
            "min": 1,
            "max": 10
        }
    ]

    def __init__(self, resource_name, slot, **kwargs):
        app_type = ApplicationType.Sensor
        super(ModelAQ2200_215, self).__init__(resource_name, app_type, slot, **kwargs)
        # thresholds
        self._min_wl = 970
        self._max_wl = 1660
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
        self._min_avg_time = 0.1
        self._max_avg_time = 1000*10
        self._min_cal = -180
        self._max_cal = 200