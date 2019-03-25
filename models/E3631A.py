from ..base_models.E36xx import ModelE36xx


class ModelE3631A(ModelE36xx):
    model = "E3631A"
    brand = "Keysight"
    details = {
        "Range": "CH1: 6V,5A | CH2: 25V,1A | CH3: -25V,1A"
    }
    params = [
        {
            "name": "select",
            "type": "int",
            "options": [1, 2, 3]
        }
    ]

    def __init__(self, resource_name, select, **kwargs):
        super(ModelE3631A, self).__init__(resource_name, **kwargs)
        self._ranges = {
            1: {
                'max_volt': 6.0,
                'max_current': 5.0
            },
            2: {
                'max_volt': 25.0,
                'max_current': 1.0
            },
            3: {
                'max_volt': -25.0,
                'max_current': 1.0
            }
        }
        self._select = select
        self._range = self._ranges[select]
        self._set_range(self._select)
        self._del_attr()

    # param encapsulation

    # Methods
    def _set_range(self, select):
        self.command(":INST:NSEL "+str(select))

    def get_range(self):
        sel_str = self.query(":INST:NSEL?")
        sel = int(sel_str)
        return self._ranges[sel]

    @staticmethod
    def _no_function(*args, **kwargs):
        raise AttributeError('Model E3631A do not have this function.')

    def _del_attr(self):
        # Model E3631 has no OCP or OVP function.
        attr_list = [
            'set_ocp',
            'get_ocp',
            'set_ocp_status',
            'get_ocp_status',
            'ocp_is_tripped',
            'clear_ocp',
            'set_ovp',
            'get_ovp',
            'set_ovp_status',
            'get_ovp_status',
            'ovp_is_tripped',
            'clear_ovp'
        ]
        for i in attr_list:
            self.__dict__[i] = self._no_function
