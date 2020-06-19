from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeOSC


class ModelMSO5000(VisaInstrument, TypeOSC):
    model = ["MSO DPO 5000 Series"]
    brand = "Tektronix"

    def __init__(self, resource_name, **kwargs):
        # TODO: termination
        super(ModelMSO5000, self).__init__(resource_name, **kwargs)

    def set_measurement_source(self, slot, source_idx, source):
        """
        source_idx: int, 1 or 2. most measurements has only 1 source.
        source: str, CH<x>|MATH<y>|REF<x>|HIStogram
        """
        return self.command('MEASUrement:MEAS{slot:d}:SOUrce{idx:d} {source}'.format(slot=slot, idx=source_idx, source=source))

    def set_measurement_type(self, slot, m_type):
        """
        set measurement type
        AMPlitude|AREa|
        BURst|CARea|CMEan|CRMs|DELay|DISTDUty|
        EXTINCTDB|EXTINCTPCT|EXTINCTRATIO|EYEHeight|
        EYEWIdth|FALL|FREQuency|HIGH|HITs|LOW|
        MAXimum|MEAN|MEDian|MINImum|NCROss|NDUty|
        NOVershoot|NWIdth|PBASe|PCROss|PCTCROss|PDUty|
        PEAKHits|PERIod|PHAse|PK2Pk|PKPKJitter|
        PKPKNoise|POVershoot|PTOP|PWIdth|QFACtor|
        RISe|RMS|RMSJitter|RMSNoise|SIGMA1|SIGMA2|
        SIGMA3|SIXSigmajit|SNRatio|STDdev|UNDEFINED| WAVEFORMS
        """
        return self.command('MEASUrement:MEAS{slot}:TYPe {m_type}'.format(slot=slot, m_type=m_type))
        
    def start_measurement(self, slot, start=True):
        """
        start or stop measurement
        """
        return self.command('MEASUrement:MEAS{slot:d}:STATE {state:d}'.format(slot=slot, state=start))
    
    def get_measurement(self, slot, category:str):
        """
        slot: int
        category: str, VALue|MAXimum|MINImum|MEAN|UNIT
        return: float|str
        """
        r = self.query('MEASUrement:MEAS{slot}:{category}?'.format(slot=slot, category=category))
        if not r.startswith('"'):
            r = float(r)
        else:
            r = r.strip('"')
        return r