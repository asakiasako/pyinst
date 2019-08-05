from ._BaseInstrumentType import BaseInstrumentType, InstrumentType
from ..utils import dbm_to_w, w_to_dbm


class TypeWM(BaseInstrumentType):
    def __init__(self, *args, **kwargs):
        super(TypeWM, self).__init__()
        self._append_ins_type(InstrumentType.WM)

    def run(self):
        """
        Start repeat measurement.
        """
        self._raise_not_implemented()

    def stop(self):
        """
        Stop repeat measurement.
        """
        self._raise_not_implemented()

    def is_running(self):
        """
        Get measurement state of WM.

        :Returns: bool, if repeat measurement is started.
        """
        self._raise_not_implemented()

    def get_power_unit(self):
        """
        Get optical power unit.

        :Returns: <enum 'OpticalUnit'>, optical power unit.
        """
        self._raise_not_implemented()

    def set_power_unit(self, unit):
        """
        Set optical power unit.

        :Parameters: **unit** - <enum 'OpticalUnit'>, optical power unit.
        """
        self._raise_not_implemented()

    def get_frequency(self):
        """
        Get frequency of single peak in THz.

        :Returns: float, frequency in THz
        """
        self._raise_not_implemented()

    def get_wavelength(self):
        """
        Get wavelength of single peak in nm

        :Returns: float, wavelength in nm
        """
        self._raise_not_implemented()

    def get_power_value(self):
        """
        Get power value of single peak in selected unit.

        :Returns: float, optical power in selected unit.
        """
        self._raise_not_implemented()

    def get_dbm_value(self):
        """
        Get dBm value of measured optical power. The value will convert for unit dBm if it is in Watt.
        
        :Returns: float, optical power in dBm
        """
        unit = self.get_power_unit()
        value = self.get_power_value()
        if unit.value == 0:
            return value
        elif unit.value == 1:
            return w_to_dbm(value)

    def get_w_value(self):
        """
        Get Watt value of measured optical power. The value will convert for unit Watt if it is in dBm.
        
        :Returns: float, optical power in Watt
        """
        unit = self.get_power_unit()
        value = self.get_power_value()
        if unit.value == 1:
            return value
        elif unit.value == 0:
            return dbm_to_w(value)