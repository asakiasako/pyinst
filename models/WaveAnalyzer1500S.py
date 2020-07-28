from ..instrument_types import TypeOSA
import requests
import subprocess
import threading
import time


class ModelWaveAnalyzer1500S(TypeOSA):
    model = "WaveAnalyzer 1500S"
    brand = "Finisar"
    details = {
        "Wavelength Range": "1526.9 to 1568.5 nm",
        "Frequency Range": "191.15 to 196.35 THz",
        "Max Input Power (Normal)": "+23 dBm",
        "Max Input Power (HighSens)": "+3dBm"
    }
    params = []

    def __init__(self, resource_name, analysis_port = 8002, analysis_exe_path = 'C:/Program Files (x86)/Finisar/WaveAnalyzer/AnalysisServer/WA-AnalysisServer.exe', timeout=5, **kwargs):
        super(ModelWaveAnalyzer1500S, self).__init__()
        self._min_wl = 1526.9
        self._max_wl = 1568.5
        self._min_freq = 191.15
        self._max_freq = 196.35
        self._resource_name = resource_name
        self.__analysis_addr = '127.0.0.1'
        self.__analysis_port = analysis_port
        self.__analysis_exe_path = analysis_exe_path
        self.__timeout = timeout

     # param encapsulation
    @property
    def resource_name(self):
        return self._resource_name

    @resource_name.setter
    def resource_name(self, value):
        raise AttributeError('Param "resource_name" is read-only')

    def __get(self, route, parseJson=True):
        url = 'http://%s/%s' % (self.resource_name, route)
        m = requests.get(url, timeout=self.__timeout)
        status_code = m.status_code
        if status_code != 200:
            raise ConnectionError('Request Responsed Error Code %d. URL = %s' % (status_code, url))
        if parseJson:
            return m.json()
        else:
            return m.content

    def __analysis(self, route, parseJson=True):
        url = 'http://%s:%d/analysis/%s' % (self.__analysis_addr, self.__analysis_port, route)
        m = requests.get(url, timeout=self.__timeout)
        status_code = m.status_code
        if status_code != 200:
            raise ConnectionError('Request Responsed Error Code %d. URL = %s' % (status_code, url))
        if parseJson:
            return m.json()
        else:
            return m.content

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        pass
    
    def check_connection(self):
        try:
            self.__get('wanl/info')
        except Exception:
            return False
        else:
            return True
    
    def set_scan_configurations(self, center, span, tag):
        """
        center: THz,
        span: GHz,
        tag: Normal, Normal20MHz, HighSens, HighSens20MHz
        """
        if not isinstance(center, (int, float)):
            raise TypeError('Parameter center should be number')
        if not isinstance(span, (int, float)):
            raise TypeError('Parameter span should be number')
        if tag not in ['Normal', 'Normal20MHz', 'HighSens', 'HighSens20MHz']:
            raise ValueError('Invalid tag: %r' % tag)
        msg = self.__get('wanl/scan/%d/%d/%s' % (center*10**6, span*10**3, tag))
        rc = msg['rc']
        if rc == 0:
            return self
        else:
            raise ValueError('Responsed Error Code: Rc = %d' % rc)

    def get_scan_configurations(self):
        """
        :return: [center(THz), span(GHz), port]
        """
        msg = self.__get('wanl/scan/info')
        center = msg['center']/10**6
        span = msg['span']/10**3
        port = msg['port']
        return center, span, port

    def launch_analysis_server(self):
        server_path = self.__analysis_exe_path
        def launch_server_action():
            subprocess.run(server_path)
        t_server = threading.Thread(target=launch_server_action, daemon=True)
        t_server.start()
        time.sleep(2)

    def analysis_scan(self, rbw, shape='flattop', averages=1, scantype='measure'):
        """
        rbw: MHz
        """
        if not isinstance(rbw, (int, float)):
            raise TypeError('Parameter rbw should be number')
        if not isinstance(averages, int):
            raise TypeError('Parameter avarages should be int')
        if shape not in ['flattop', 'gaussian']:
            raise ValueError('Invalid shape: %r' % shape)
        msg = self.__analysis('data?ip=%s&averages=%d&scantype=%s&rbw=%d&shape=%s' % (self.resource_name, averages, scantype, rbw, shape), False)
        return msg

    def measure_osnr(self, *frequencies, averages=1, scantype='measure'):
        """
        3 or 6 ints, MHz
        return: osnr(dB)
        """
        if len(frequencies) not in (3, 6):
            raise ValueError('Measure frequencies must be 3-point or 6-point')
        frequencies = [str(int(i)) for i in frequencies]
        frequencies_str = ','.join(frequencies)
        msg = self.__analysis('osnr?ip=%s&averages=%d&scantype=%s&frequencies=%s' % (self.resource_name, averages, scantype, frequencies_str))
        if msg['rc'] != 0:
            raise ValueError('Responsed Error Code: Rc = %d' % msg['rc'])
        print('OSNR: %f' % (msg['osnr']/1000))
        return msg['osnr']/1000
