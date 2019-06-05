from ..base_models.E36xx import ModelE36xx


class ModelE3633A(ModelE36xx):
    model = "E3633A"
    brand = "Keysight"
    details = {
        "Range": "20V,10A | 8V,20A"
    }
    params = [
        {
            "name": "range_level",
            "type": "str",
            "options": ["HIGH", "LOW"]
        }
    ]

    def __init__(self, resource_name, range_level, **kwargs):
        super(ModelE3633A, self).__init__(resource_name, **kwargs)
        self._ranges = {
            "HIGH": {
                'max_volt': 20.0,
                'max_current': 10.0
            },
            "LOW": {
                'max_volt': 8.0,
                'max_current': 20.0
            }
        }
        self._range_level = range_level
        self._range = self._ranges[self._range_level]
        self._set_range(self._range_level)

    # param encapsulation

    # Methods
    def _set_range(self, range_level):
        return self.command(":VOLT:RANG "+range_level)

    def get_range(self):
        range_str = self.query(":VOLT:RANG?")
        if "8" in range_str:
            return self._ranges["LOW"]
        if "20" in range_str:
            return self._ranges["HIGH"]
