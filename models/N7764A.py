from ..instrument_types import TypeVOA, TypeOPM
from ._N77xx import ModelN77xx
from ..constants import LIGHT_SPEED
import math

class ModelN7764A(ModelN77xx, TypeVOA, TypeOPM):
    model = "N7764A"
    details = {
        "Wavelength Range": "1260~1640 nm",
        "Att Range": "0~45 dB",
        "Att Safe Power": "+23dBm",
        "PM Power Range": "-80 ~ +10 dBm",
        "PM Safe Power": "+16 dBm",
        "AVG Time": "2 ms ~ 10 s"
    }
    params = [
        {
            "name": "slot",
            "type": "int",
            "options": [1, 3, 5, 7]
        }
    ]

    def __init__(self, resource_name, slot, **kwargs):
        super(ModelN7764A, self).__init__(resource_name, slot, max_slot=8, slot_type_define={'voa_with_opm': [1,2,3,4,5,6,7,8]})
        self._max_att = 45.0
        self._min_offset = float('-inf')
        self._max_offset = float('inf')
        self._max_wl = 1625.0
        self._min_wl = 1250.0
        self._min_freq = math.floor(LIGHT_SPEED*1000/self._max_wl)/1000 + 0.001
        self._max_freq = math.floor(LIGHT_SPEED*1000/self._min_wl)/1000
        self._min_avg_time = 2
        self._max_avg_time = 10000
        self._min_cal = float('-inf')
        self._max_cal = float('inf')
