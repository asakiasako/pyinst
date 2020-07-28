from ._BaseInstrument import BaseInstrument
from ..instrument_types import TypeSW
import subprocess
import os
import time
import usb
import win32com.client


class ModelNSW(BaseInstrument, TypeSW):
    model = "Neo_SW"
    brand = "NeoPhotonics"
    params = [
        {
            "name": "slot_or_type",
            "type": "str",
            "options": ['1', '2', '3', '1*8', '1*16']
        }
    ]
    details = {
        "Note": "Valid slot depending on specific instrument."
    }

    try:
        _ops = win32com.client.Dispatch('Neo_SmartOpticalSwitch.SmartOpticalSwitch')
    except Exception:
        _ops = None

    def __init__(self, resource_name, slot_or_type):
        """
        slot_or_type: 1, 2, 3, '1*8', '1*16'
        """
        super(ModelNSW, self).__init__()
        self._resource_name = resource_name
        if isinstance(slot_or_type, int):
            self.__index = slot_or_type - 1
        else:
            index_map = {
                '1': 0,
                '2': 1,
                '3': 2,
                '1*8': 3,
                '1*16': 4,
            }
            try:
                self.__index = index_map[slot_or_type]
            except KeyError:
                raise KeyError('Invalid value for slot_or_type: %r' % slot_or_type)
        if not self._ops:
            raise ModuleNotFoundError('Neo_SmartOpticalSwitch.SmartOpticalSwitch')

    @classmethod
    def get_usb_devices(cls, num=9):
        if not cls._ops:
            raise ModuleNotFoundError('Neo_SmartOpticalSwitch.SmartOpticalSwitch')
        cls._ops.InitIntefaceType = 3
        dev_list = [cls._ops.GetMultiUSBDeviceName(i) for i in range(num) if cls._ops.GetMultiUSBDeviceName(i) != 'NoDevice']
        return dev_list

    def close(self):
        pass

    def check_connection(self):
        channel = self.get_channel()
        if channel > 0:
            return True
        return False

    def _select_device(self):
        dev_list = self.get_usb_devices()
        if self.resource_name not in dev_list:
            raise ValueError('Invalid device name: %s' % self.resource_name)
        self._ops.USBDeviceName = self.resource_name
        self._ops.InitIntefaceType = 2

    def set_channel(self, channel, retry=3):
        """
        Set channel.
        :param channel: (int) channel number (1 based)
        """

        index = self.__index
        self._select_device()
        self._ops.SetSelectChannel(index, channel)
        count = 0
        tried = 0
        while True:
            current_channel = self.get_channel()
            if current_channel != channel:
                time.sleep(0.4)
                count += 1
                if count % 5 == 0:
                    tried += 1
                    if tried >= retry:
                        raise RuntimeError('Unable to select Neo_Opswitch channel. DeviceName: %s' % self._resource_name)
                    else:
                        self.reset()
            else:
                break

    def get_channel(self):
        """
        Get selected channel.
        :return: (int) selected channel (1 based)
        """
        index = self.__index
        self._select_device()
        channel = self._ops.GetSelectChannel(index)
        return channel

    def reset(self):
        """
        Neo Optical Switch may lose USB control during auto test.
        This method reset the USB port to solve the connection issue.
        """
        serial_number = self._resource_name
        dev = usb.core.find(serial_number=serial_number)
        if not dev:
            raise AttributeError('Error on Reset: USB Device not found. SN = %s' % serial_number)
        dev.reset()
