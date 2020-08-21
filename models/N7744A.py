from ..instrument_types import TypeOPM
from ..constants import OpticalUnit, LIGHT_SPEED
from ._N77xx import ModelN77xx
import math

class ModelN7744A(ModelN77xx, TypeOPM):
    brand = "Keysight"
    model = "N7744A"
    details = {
        "Wavelength Range": "1250~1625 nm",
        "Power Range": "-80 ~ +10 dBm",
        "Safe Power": "+16 dBm",
        "AVG Time": "1 us ~ 10 s"
    }
    params = [
        {
            "name": "slot",
            "type": "int",
            "options": [1, 2, 3, 4]
        }
    ]

    def __init__(self, resource_name, slot, **kwargs):
        super(ModelN7744A, self).__init__(resource_name, slot, max_slot=4, slot_type_define={'opm': [1,2,3,4]})
        # thresholds
        self._max_wl = 1625.0
        self._min_wl = 1250.0
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
        self._min_avg_time = 0.001
        self._max_avg_time = 10000
        self._min_cal = float('-inf')
        self._max_cal = float('inf')
