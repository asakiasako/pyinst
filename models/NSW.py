from ..model_bases.ins_base import *
from ..model_bases.ins_types import *
import time
import usb


class ModelNSW(TypeSW):
    model = "Neo_SW"
    brand = "NeoPhotonics"
    params = [
        {
            "name": "channel",
            "type": "int",
            "range": [1, 2, 3]
        }
    ]
    detail = {
        "Note": "Valid channel depending on specific instrument."
    }
    _depend = os.path.join(os.path.dirname(__file__), '../dependency/neo_opswitch.exe')

    def __init__(self, resource_name, channel):
        super(ModelNSW, self).__init__()
        self.__resource_name = resource_name
        self.__index = channel - 1

    # param encapsulation
    @property
    def resource_name(self):
        return self.__resource_name

    @resource_name.setter
    def resource_name(self, value):
        raise AttributeError('param resource_name is read-only')

    @classmethod
    def get_usb_devices(cls, num=9):
        str_list = subprocess.check_output('%s %s %s' % (cls._depend, 'get_usb_devices', num))
        list0 = eval(str_list)
        return list0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
        serial_number = self.__resource_name
        dev = usb.core.find(serial_number=serial_number)
        if not dev:
            raise AttributeError('USB Device not found: SN = %s' % serial_number)

        dev.reset()
