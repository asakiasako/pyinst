from ..base_models._VisaInstrument import VisaInstrument
from ..instrument_types import TypeWGEN
from string import ascii_lowercase


class ModelMSOX6000(VisaInstrument, TypeWGEN):
    model = ["MSO-X 6000 Series"]
    brand = "Keysight"

    def __init__(self, resource_name, wg_channel, **kwargs):
        # TODO: termination
        super(ModelMSOX6000, self).__init__(resource_name, **kwargs)
        self.wg_channel = wg_channel

    def set_frequency(self, frequency):
        return self.command(':WGEN{w:d}:FREQuency{frequency:.4e}'.format(
                                        w=self.wg_channel, frequency=frequency))

    def get_frequency(self):
        return round(float(self.query(':WGEN{w:d}:FREQuency?'.format(w=self.wg_channel))), 4)

    def set_function(self, signal:str):
        option_str = 'SINusoid | SQUare | RAMP | PULSe | NOISe | DC | SINC | '\
                     'EXPRise | EXPFall | CARDiac | GAUSsian | ARBitrary'
        options = [i.strip().strip(ascii_lowercase) for i in option_str.strip().split('|')]
        for i in options:
            if signal.upper().startswith(i):
                break
        else:
            raise ValueError('Invalid signal type. Options: %s' % option_str)

        return self.command(':WGEN{w:d}:FUNCtion {signal:s}'.format(
                                        w=self.wg_channel, signal=signal))

    def get_function(self):
        return self.query(':WGEN{w:d}:FUNCtion?'.format(w=self.wg_channel))

    def enable(self, enable=True):
        return self.command(':WGEN{w:d}:OUTPut {enable:d}'.format(
                                            w=self.wg_channel, enable=enable))

    def disable(self):
        return self.enable(enable=False)

    def is_enabled(self):
        return bool(int(self.query(':WGEN{w:d}:OUTPut?'.format(w=self.wg_channel))))
    
    def set_period(self, period):
        return self.command(':WGEN{w:d}:PERiod {period:.4e}'.format(
                                        w=self.wg_channel, period=period))

    def get_period(self):
        return float(self.query(':WGEN{w:d}:PERiod?'.format(w=self.wg_channel)))

    def set_voltage_amplitude(self, amplitude):
        return self.command(':WGEN{w:d}:VOLTage {amplitude:.4e}'.format(
                                    w=self.wg_channel, amplitude=amplitude))

    def get_voltage_amplitude(self):
        return float(self.query(':WGEN{w}:VOLTage?'.format(w=self.wg_channel)))

    def set_voltage_high(self, high):
        return self.command(
            ':WGEN{w:d}:VOLTage:HIGH {high:.4e}'.format(w=self.wg_channel, high=high))

    def get_voltage_high(self):
        return float(self.query(':WGEN{w:d}:VOLTage:HIGH?'.format(self.wg_channel)))

    def set_voltage_low(self, low):
        return self.command(
            ':WGEN{w:d}:VOLTage:LOW {low:.4e}'.format(w=self.wg_channel, low=low))

    def get_voltage_low(self):
        return float(self.query(':WGEN{w:d}:VOLTage:LOW?'.format(w=self.wg_channel)))

    def set_voltage_offset(self, offset):
        return self.command(
                ':WGEN{w:d}:VOLTage:OFFSet {offset:.4e}'.format(
                                    w=self.wg_channel, offset=offset))

    def get_voltage_offset(self):
        return float(self.query(':WGEN{w:d}:VOLTage:OFFSet?'.format(w=self.wg_channel)))