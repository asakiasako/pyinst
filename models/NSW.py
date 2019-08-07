from ..base_models._BaseInstrument import BaseInstrument
from ..instrument_types import TypeSW
import subprocess
import os
import time
import usb


class ModelNSW(BaseInstrument, TypeSW):
    model = "Neo_SW"
    brand = "NeoPhotonics"
    params = [
        {
            "name": "channel",
            "type": "int",
            "options": [1, 2, 3]
        }
    ]
    details = {
        "Note": "Valid channel depending on specific instrument."
    }

    # if python is running on 64-bit, we need a dependency, because driver for this instrument is a com component on 32-bit and no source code.
    _depend = os.path.join(os.path.dirname(__file__), '../dependency/neo_opswitch.exe')

    def __init__(self, resource_name, channel):
        super(ModelNSW, self).__init__()
        self._resource_name = resource_name
        self.__index = channel - 1

    @classmethod
    def get_usb_devices(cls, num=9):
        str_list = subprocess.check_output('%s %s %s' % (cls._depend, 'get_usb_devices', num))
        list0 = eval(str_list)
        return list0

    def close(self):
        pass

    def check_connection(self):
        channel = self.get_channel()
        if channel > 0:
            return True
        return False

    def set_channel(self, channel, retry=3):
        """
        Set channel.
        :param channel: (int) channel number (1 based)
        """
        tried = 0
        while tried <= retry:
            back_str = subprocess.check_output('%s %s %s %s %s' % (self._depend,
                                                            'select_channel', self.resource_name, self.__index, channel))
            if "True" in str(back_str):
                return self
            else:
                self.reset()
                time.sleep(10)
                tried += 1
        else:
            raise ChildProcessError('Switch select failed.', 'NSW_USB_ERROR')

    def get_channel(self):
        """
        Get selected channel.
        :return: (int) selected channel (1 based)
        """
        channel_str = subprocess.check_output('%s %s %s %s' % (self._depend,
                                              'get_selected_channel', self.resource_name, self.__index))
        channel = int(channel_str)
        return channel

    def reset(self):
        """
        Neo Optical Switch may lose USB control during auto test.
        This method reset the USB port to solve the connection issue.
        """
        serial_number = self._resource_name
        dev = usb.core.find(serial_number=serial_number)
        if not dev:
            raise AttributeError('USB Device not found: SN = %s' % serial_number)

        dev.reset()
