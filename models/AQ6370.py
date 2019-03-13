from ..model_bases.ins_base import *
from ..model_bases.ins_types import *
import time


class ModelAQ6370(VisaInstrument, TypeOSA):
    model = "AQ6370"
    brand = "Yokogawa"
    detail = {
        "Wavelength Range": "600 ~ 1700 nm",
        "Max. Resolution": "0.02 nm"
    }

    def __init__(self, resource_name, username="anonymous", password="empty", **kwargs):
        super(ModelAQ6370, self).__init__(resource_name, **kwargs)
        self._analysis_cat = ["WDM", "DFBLD", "FPLD", "SMSR"]
        self._analysis_setting_map = {
            "WDM": ["TH", "MDIFF", "DMASK", "NALGO", "NAREA", "MAREA", "FALGO", "NBW"],
            "DFBLD": {
                "SWIDTH": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
                "SMSR": ["SMODE", "SMASK", "MDIFF"],
                "RMS": ["ALGO", "TH", "K", "MDIFF"],
                "POWER": ["SPAN"],
                "OSNR": ["MDIFF", "NALGO", "NAREA", "MAREA", "FALGO", "NBW", "SPOWER", "IRANGE"],
            },
            "FPLD": {
                "SWIDTH": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
                "MWAVE": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
                "TPOWER": ["OFFSET"],
                "MNUMBER": ["ALGO", "TH", "TH2", "K", "MFIT", "MDIFF"],
            }
        }
        self._setup_map = ["BWIDTH:RES"]
        # init LAN if connection method is TCPIP
        if self.resource_name.upper().startswith('TCPIP'):
            self.open_lan_port(username, password)

    # param encapsulation
    # Method
    def open_lan_port(self, user="anonymous", password="empty"):
        usr_rsp = self.query('OPEN "%s"' % user)
        if usr_rsp.strip() == "AUTHENTICATE CRAM-MD5.":
            psw_rsp = self.query(password)
            if psw_rsp.strip() == "ready":
                return
        raise PermissionError("Uncorrect LAN username or password for %s" % self.model)

    def close(self):
        self.command('CLOSE')
        VisaInstrument.close(self)

    def sweep(self, mode="REPEAT"):
        """
        Set OSA sweep mode. mode = "AUTO"|"REPEAT"|"SINGLE"|"STOP"
        :param mode: (str) "AUTO"|"REPEAT"|"SINGLE"|"STOP"
        """
        selection = ["AUTO", "REPEAT", "SINGLE", "STOP"]
        check_type(mode, str, 'mode')
        check_selection(mode, selection)
        if mode != "STOP":
            return self.command(':INIT:SMOD '+mode+';:INIT')
        else:
            return self.command(':ABOR')

    def set_auto_zero(self, is_on):
        """
        Enable or disable auto zero
        """
        check_type(is_on, bool, 'is_on')
        if is_on:
            flag = 'ON'
        else:
            flag = 'OFF'
        return self.command(":CAL:ZERO %s" % flag)

    def zero_once(self):
        """
        perform zeroing once
        """
        return self.command(":CAL:ZERO ONCE")

    def auto_analysis(self, enable):
        """
        enable/disable auto analysis
        :param enable: (bool) enable/disable auto analysis
        """
        return self.command(":CALC:AUTO "+str(int(enable)))

    def set_analysis_cat(self, item):
        """
        Set OSA analysis item. Available item depends on specific instrument.
        item = "WDM"|"DFBLD"|"FPLD"|"SMSR"
        :param item: (str) analysis item
        """
        check_type(item, str, 'item')
        check_selection(item, self._analysis_cat)
        return self.command(":CALC:CAT " + item)

    def get_analysis_cat(self):
        """
        Get the current analysis item.
        :return: (str) analysis item
        """
        cat_dict = {11: "WDM", 5: "DFBLD", 6: "FPLD"}
        cat_str = self.query(":CALC:CAT?")
        cat = cat_dict[int(cat_str)]
        return cat

    def analysis_setting(self, cat, param, value, subcat=None):
        """
        Analysis setting. param and value depends on specific instrument.
        :param cat: (str) setting category
        :param subcat: (str) setting sub category if there is one
        :param param: (str) setting item
        :param value: (str) setting value
        """
        check_type(cat, str, 'cat')
        check_type(param, str, 'param')
        check_type(subcat, (str, type(None)), 'subcat')
        check_selection(cat, self._analysis_cat)
        if subcat:
            check_selection(subcat, tuple(self._analysis_setting_map[cat].keys()))
            check_selection(param, self._analysis_setting_map[cat][subcat])
            route_str = " %s,%s," % (subcat, param)
        else:
            check_selection(param, self._analysis_setting_map[cat])
            route_str = ":%s " % param
        value = str(value)
        cmd_str = ":CALC:PAR:%s%s%s" % (cat, route_str, value)
        return self.command(cmd_str)

    def get_analysis_setting_map(self):
        """
        Get setting map for all analysis categories.
        :return: (dict) analysis setting map
        """
        return self._analysis_setting_map

    def get_analysis_data(self):
        """
        Get data of current analysis item.
        :return: (str) data of current analysis item
        """
        return self.query(':CALC:DATA?')

    def set_center(self, value, unit):
        """
        Set center wavelength/frequency
        :param value: (float|int) center value
        :param unit: (str) unit
        """
        check_type(value, (float, int), 'value')
        check_type(unit, str, 'unit')
        check_selection(unit, ['NM', 'THZ'])
        if unit.upper() == 'NM':
            return self.command(":SENS:WAV:CENT " + str(value) + 'NM')
        if unit.upper() == 'THZ':
            return self.command(":SENS:WAV:CENT " + str(value) + 'THZ')

    def get_center(self):
        """
        Get center wavelength setting
        :return: (float) center wavelength in nm
        """
        return float(self.query(":SENS:WAV:CENT?")) * 10**9

    def set_marker_x(self, num, value, unit):
        """
        set marker x
        unit: NM|THZ
        """
        check_type(num, int, 'num')
        check_range(num, 1, 4)
        check_type(value, (float, int), 'value')
        check_type(unit, str, 'unit')
        check_selection(unit, ['NM', 'THZ'])
        return self.command(':CALC:AMARKER%d:X %.3f%s' % (num, value, unit))

    def get_marker_x(self, num):
        """
        get marker x
        unit: Advanced marker position
        """
        check_type(num, int, 'num')
        check_range(num, 1, 4)
        return float(self.query(':CALCULATE:AMARKER%d:X?' % num))

    def get_marker_y(self, num):
        """
        get marker y level
        """
        check_type(num, int, 'num')
        check_range(num, 1, 4)
        return float(self.query(':CALCULATE:AMARKER%d:Y?' % num))

    def set_peak_to_center(self):
        """
        Set peak wavelength to center.
        """
        return self.command(':CALC:MARK:MAX:SCEN')

    def set_span(self, value, unit="NM"):
        """
        Set span wavelength/frequency
        :param value: (float|int) span value
        :param unit: (str) unit
        """
        check_type(value, (float, int), 'value')
        cmd = ':SENS:WAV:SPAN ' + str(value) + unit
        return self.command(cmd)

    def set_start_stop_wavelength(self, start, stop):
        """
        Set start-stop wavelength.
        :param start: (float|int) start wavelength in nm
        :param stop: (float|int) stop wavelength in nm
        """
        check_type(start, (float, int), 'start')
        check_type(stop, (float, int), 'stop')
        check_range(start, 0, stop)
        return self.command(':SENS:WAV:STAR %.2fNM;:SENS:WAV:STOP %.2fNM' % (start, stop))

    def set_start_stop_frequency(self, start, stop):
        """
        Set start-stop frequency.
        :param start: (float|int) start frequency in THz
        :param stop: (float|int) stop frequency in THz
        """
        check_type(start, (float, int), 'start')
        check_type(stop, (float, int), 'stop')
        check_range(stop, 0, start)
        return self.command(':SENS:WAV:STAR %fTHZ;:SENS:WAV:STOP %fTHZ' % (start, stop))

    def set_ref_level(self, value, unit):
        """
        Set reference level.
        :param value: (float|int) reference level value
        :param unit: (str) unit = "DBM"|"MW
        """
        check_type(value, (float, int), 'value')
        check_type(unit, str, 'unit')
        check_selection(unit, ['DBM', 'MW', 'UM', 'NW'])
        return self.command(":DISPLAY:TRACE:Y1:RLEVEL %f%s" % (value, unit))

    def set_peak_to_ref(self):
        """
        Set peak level to reference level
        """
        return self.command(':CALC:MARK:MAX:SRL')

    def set_auto_ref_level(self, is_on):
        """
        Enable/Disable auto peak -> ref level
        """
        
        return self.command(':CALC:MARK:MAX:SRL:AUTO %s' % 'ON' if is_on else 'OFF')

    def setup(self, param, value):
        """
        Set setup settings.
        :param param: (str) param
        :param value: (str) setting value
        """
        check_type(param, str, 'param')
        check_type(value, str, 'value')
        return self.command(':SENS:%s %s' % (param, value))

    def format_data(self, cat, data):
        """
        Format data into dict, depends on calculate category (Anasis Category)
        :param cat: (str) "DFB"|"FP"|"WDM"
        :param data: (str) data retruned by method: get_analysis_data
        :return: (dict) a dict of test_item=>value
        """
        check_type(cat, str, 'cat')
        check_type(data, str, 'data')
        check_selection(cat, self._analysis_cat)
        data_list = data.split(',')
        r_data = None
        if cat == 'DFBLD':
            r_data = {
                "spec_wd": data_list[0],
                "peak_wl": data_list[1],
                "peak_lvl": data_list[2],
                "mode_ofst": data_list[3],
                "smsr": data_list[4]
            }
        elif cat == 'FPLD':
            r_data = {
                "spec_wd": data_list[0],
                "peak_wl": data_list[1],
                "peak_lvl": data_list[2],
                "center_wl": data_list[3],
                "total_pow": data_list[4],
                "mode_num": data_list[5]
            }
        elif cat == 'WDM':
            #  <display type> = ABSolute|0, RELative|1, MDRift|2, GDRift|3
            d_type = int(self.query(':CALC:PAR:WDM:DTYP?'))
            # 0 = OFFSET, 1 = SPACING
            relation = int(self.query(':CALC:PAR:WDM:REL?'))
            if d_type == 0:
                if relation == 0:
                    r_data = {
                        "ch_num": data_list[0],
                        "center_wl": data_list[1],
                        "peak_lvl": data_list[2],
                        "offset_wl": data_list[3],
                        "offset_lvl": data_list[4],
                        "noise": data_list[5],
                        "snr": data_list[6]
                    }
                elif relation == 1:
                    r_data = {
                        "ch_num": data_list[0],
                        "center_wl": data_list[1],
                        "peak_lvl": data_list[2],
                        "spacing": data_list[3],
                        "lvl_diff": data_list[4],
                        "noise": data_list[5],
                        "snr": data_list[6]
                    }
            elif d_type == 1:
                r_data = {
                    "ch_num": data_list[0],
                    "grid_wl": data_list[1],
                    "center_wl": data_list[2],
                    "rel_wl": data_list[3],
                    "peak_lvl": data_list[4],
                    "noise": data_list[5],
                    "snr": data_list[6]
                }
            elif d_type == 2:
                r_data = {
                    "ch_num": data_list[0],
                    "grid_wl": data_list[1],
                    "center_wl": data_list[2],
                    "wl_diff_max": data_list[3],
                    "wl_diff_min": data_list[4],
                    "ref_lvl": data_list[5],
                    "peak_lvl": data_list[6],
                    "lvl_diff_max": data_list[7],
                    "lvl_diff_min": data_list[8]
                }
            elif d_type == 3:
                r_data = {
                    "ch_num": data_list[0],
                    "ref_wl": data_list[1],
                    "center_wl": data_list[2],
                    "wl_diff_max": data_list[3],
                    "wl_diff_min": data_list[4],
                    "ref_lvl": data_list[5],
                    "peak_lvl": data_list[6],
                    "lvl_diff_max": data_list[7],
                    "lvl_diff_min": data_list[8]
                }
        return r_data

    def clear_all_markers(self):
        """
        """
        return self.command(':CALCULATE:AMARKER:AOFF')