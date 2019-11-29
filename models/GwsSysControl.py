from ..base_models._BaseInstrument import BaseInstrument
from ..instrument_types import TypeTEC
from ..utils import check_range, check_type
from ..constants import TemperatureUnit
from ..dependencies import DEPEND_PATH
import os.path
import enum
from ctypes import cdll, c_long, c_ulong, pointer, byref
import time

# Constants
class ERR_CODE(enum.Enum):
    ERR_SUCCEED             = 0
    ERR_FAIL                = 1000
    ERR_INITED              = 1001
    ERR_BUFFER_FULL         = 1002
    ERR_OPEN_SERIAL_PORT    = 1004
    ERR_INVALID_PARAM       = 1005
    ERR_NO_OPENED           = 1006
    ERR_INVALID_MACHID      = 1007

class MESSAGE_ID(enum.Enum):
    GWS_POWER_OFF = 0
    GWS_POWER_ON = 1
    GWS_GATHER = 2
    GWS_MODEM = 3
    GET_SEG_TIMER = 4
    GET_CHAMBER_STATE = 5
    GET_SET_TEMP = 6
    GET_SET_HUMI = 7
    GET_SET_PARA = 8
    GET_ACT_TEMP = 9
    GET_ACT_HUMI = 10
    GET_ACT_PARA = 11
    GET_SWITCH = 12
    GET_RUN_PRO = 13
    GET_RUN_TIME = 14
    GET_RUN_SEG = 15
    GET_RUN_CYCLE = 16
    GET_RUN_CYCLE_TIME = 17
    GET_ERROR_NO = 18
    GET_HIGH_TEMP = 19
    GET_LOW_TEMP = 20
    GET_HEAT_OUT = 21
    GET_HUMI_OUT = 22
    GET_SAMPLE_POWER = 23
    GET_OUTSIDE_ALARM = 24
    GET_AIR_CONTROL_FLAG = 25
    GET_PRINT_SPEED = 26
    GET_SET_VALUE = 27
    GET_HUMI_CONTROL_FLAG = 28
    GET_CHAMBER_PROTET_TEMP = 29
    SET_CHAMBER_PROTET_TEMP = 30
    GET_CHAMBER_PROTET_HUMI = 31
    GET_SAMPLE_PROTET_TEMP = 32
    GET_SPECIAL_PARAM_FOR_QIRI = 33
    GET_SPECIAL_PARAM_FOR_AERO_OIL = 34
    GET_SPECIAL_PARAM_FOR_RAIN = 35
    GET_SPECIAL_PARAM_FOR_NORMAL_SUN = 36
    UPLOAD_PROGRAM = 37
    GWS_REAL_TIME_DATA = 38

# pre-defined types
BufDWORD16 = c_ulong * 16
Buflong32 = c_long * 32

class ModelGwsSysControl(BaseInstrument, TypeTEC):
    model = "GWS System Control"
    brand = "GWS"
    # load dll
    GWSdll = None
    ReadMsgdll = None
    MsgProc = None

    @classmethod
    def __load_dlls(cls):
        if not (cls.GWSdll and cls.ReadMsgdll and cls.MsgProc):
            try:
                cls.GWSdll = cdll.LoadLibrary(os.path.join(DEPEND_PATH, 'dll', 'GWSDll.dll'))
                cls.ReadMsgdll = cdll.LoadLibrary(os.path.join(DEPEND_PATH, 'dll', 'ReadMessage.dll'))
                # Message Process
                cls.MsgProc = cls.ReadMsgdll.GetMessageProAddr()
            except OSError as e:
                cls.GWSdll = cls.ReadMsgdll = cls.MsgProc = None
                raise e

    def __init__(self, resource_name, **kwargs):
        # load dlls to class attributes if none.
        self.__load_dlls()
        super(ModelGwsSysControl, self).__init__(resource_name, **kwargs)
        select_id = 0
        if not resource_name.upper().startswith('COM'):
            raise ValueError('invalid COM port name')
        self._resource_name = resource_name
        check_type(select_id, int, 'select_id')
        check_range(select_id, 0, 15)

        com_id = int(resource_name[3:])

        selectFlag = BufDWORD16(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        Flag2000A = BufDWORD16(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        selectFlag[select_id] = 1
        result = self.GWSdll.GWS_Init(com_id, 19200, 78, 8, 1, 0, pointer(selectFlag), pointer(Flag2000A), self.MsgProc)
        self.__connected = False
        if result != 0:
            raise ValueError("Init Failed. Error code: %d - %s" % (result, ERR_CODE(result).name))
        else:
            self.__connected = True
            # clear chamber message after init
            self.__clear_chamber_message()

    def close(self):
        self.__connected = False
        self.GWSdll.GWS_Close()
        # serial port needs some time to release
        time.sleep(5)

    def check_connection(self):
        return self.__connected

    def __read_chamber_message_action(self):
        MessageID  = c_ulong()
        MacID = c_ulong()
        mParam = Buflong32()        
        # Add time delay, chamber needs time
        time.sleep(0.5)

        result = self.ReadMsgdll.GetGWSMessage(byref(MessageID), byref(MacID), pointer(mParam))
        
        if result == 0:
            msg_id = mac_id = m_param = None
        else:
            msg_id = MessageID.value
            mac_id = MacID.value
            m_param = list(mParam)

        return result, msg_id, mac_id, m_param

    def __read_chamber_message(self, expected_msg_id=None):
        check_type(expected_msg_id, (None.__class__, MESSAGE_ID), 'expected_msg_id')

        count = 0
        max_try = 20  # 10 sec in total
        msg_id_record = []

        while True:
            result, msg_id, mac_id, m_param = self.__read_chamber_message_action()

            if expected_msg_id is None:
                return m_param
    
            if result != 0 and msg_id == expected_msg_id.value:
                return m_param
            else:
                msg_id_record.append(msg_id)
                count += 1
                if count > max_try:
                    raise ValueError('No expected reply after %d reading attempts. \nmsg_id = %r' % (max_try, msg_id_record))

    def __clear_chamber_message(self):
        count = 0
        max_count = 50
        while True:
            MessageID  = c_ulong()
            MacID = c_ulong()
            mParam = Buflong32()

            result = self.ReadMsgdll.GetGWSMessage(byref(MessageID), byref(MacID), pointer(mParam))

            if result == 0:
                break
            else:
                count += 1
                time.sleep(0.1)
                if count >= max_count:
                    raise ValueError('Can\'t clear chamber message after 50 read operations.')

    def set_target_temp(self, value):
        """
        Set the target Temperature.
        :param value: <float|int> target temperature value
        """
        check_type(value, (int, float), 'value')
        temp_set_param = round(value * 10)
        result =self.GWSdll.GWS_SetSetValue(0, temp_set_param, 0, 0, 0, 0)
        if result != 0:
            raise ValueError('Set temp fail. Error Code: %d - %s' % (result, ERR_CODE(result).name))
        time.sleep(8)

    def get_target_temp(self):
        """
        Get the target Temperature
        :return: <float> target temperature value
        """
        result = self.GWSdll.GWS_GetSetTemp(0)
        if result != 0:
            raise ValueError('Get target temp fail. Error Code: %d - %s' % (result, ERR_CODE(result).name))
        m_param = self.__read_chamber_message(expected_msg_id=MESSAGE_ID.GET_SET_TEMP)
        return m_param[0]/10

    def get_current_temp(self):
        """
        Get the current measured temperature
        :return: <float> current measured temperature
        """
        result = self.GWSdll.GWS_GetActTemp(0)
        if result != 0:
            raise ValueError('Get current temp monitor fail. Error Code: %d - %s' % (result, ERR_CODE(result).name))
        m_param = self.__read_chamber_message(expected_msg_id=MESSAGE_ID.GET_ACT_TEMP)
        return m_param[0]/10

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