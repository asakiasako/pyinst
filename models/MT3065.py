from ..base_models._BaseInstrument import BaseInstrument
from ..instrument_types import TypeTS
from ..constants import TemperatureUnit
import serial
import time

class ModelMT3065(BaseInstrument, TypeTS):
    model = "MT3065"
    brand = "Espec"

    def __init__(self, resource_name, dev_id=0, baud_rate=19200, **kwargs):
        super(ModelMT3065, self).__init__()
        self._ts_type = 'Chamber'
        if dev_id not in range(16):
            raise ValueError('Device ID should between 0 ~ 15')
        self.__dev_id = dev_id
        self.__serial = serial.Serial(port=resource_name, baudrate=baud_rate, timeout=0.5)
        self.__serial.setRTS()
        self.__serial.setDTR()
        self.__serial.reset_input_buffer()

    def write_cmd(self, cmd):
        pre = b'\x05'
        b_id = '{dev_id:02X}'.format(dev_id=self.__dev_id).encode()
        cmd_body = b_id + cmd
        checksum = '{:02X}'.format(sum(cmd_body))[-2:].encode()
        t = pre+cmd_body+checksum
        self.__serial.reset_input_buffer()
        self.__serial.write(t)

    def read_reply(self):
        r = self.__serial.read(10240)
        if not r:
            raise ValueError('No reply. Please check device ID.')
        return r

    def close(self):
        self.__serial.close()

    def check_connection(self):
        try:
            self.get_target_temp()
            return True
        except Exception:
            return False

    def set_target_temp(self, value):
        """
        Set the target Temperature.
        :param value: <float|int> target temperature value
        """
        value = round(value*10)
        if value < 0:
            value = 65536 + value
        cmd = 'FFWW0D119705{temp:04X}0000000000000000'.format(temp=value).encode()
        self.write_cmd(cmd)
        time.sleep(0.5)
        r = self.read_reply()
        if not r.startswith(b'\x06'):
            raise ValueError('Unexpected reply: %r' % r)

    def get_target_temp(self):
        """
        Get the target Temperature
        :return: <float> target temperature value
        """
        cmd = b'FFWR0D111401'
        self.write_cmd(cmd)
        time.sleep(0.5)
        r = self.read_reply()
        if not r.startswith(b'\x02'):
            raise ValueError('Unexpected reply: %r' % r)
        raw_val = int(r[5:9].decode(), 16)
        signed_val = (raw_val - 65536) if raw_val >= 65536/2 else raw_val
        return signed_val/10

    def get_current_temp(self):
        """
        Get the current measured temperature
        :return: <float> current measured temperature
        """
        cmd = b'FFWR0D111701'
        self.write_cmd(cmd)
        time.sleep(0.5)
        r = self.read_reply()
        if not r.startswith(b'\x02'):
            raise ValueError('Unexpected reply: %r' % r)
        raw_val = int(r[5:9].decode(), 16)
        signed_val = (raw_val - 65536) if raw_val >= 65536/2 else raw_val
        return signed_val/10

    def set_unit(self, unit):
        """
        Set temperature unit
        :param unit: int, value of <TemperatureUnit> unit
        """
        TemperatureUnit(unit)
        if unit == TemperatureUnit.C.value:
            return
        else:
            raise ValueError('Chamber temperature unit is fixed as "C".')

    def get_unit(self):
        """
        Get temperature unit
        :return: int, value of <TemperatureUnit> unit
        """
        return TemperatureUnit.C.value