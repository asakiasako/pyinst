from enum import Enum, unique

__all__ = ['LIGHT_SPEED', 'InstrumentType', 'OpticalUnit', 'TemperatureUnit', 'WavelengthUnit']

# define constants
LIGHT_SPEED = 299792.458  # km/s

# define enums
# no inspection PyArgumentList
@unique
class InstrumentType(Enum):
    """
    Enum of instrument types.
    
    ::

        OPM:  Optical Power Meter
        VOA:  Variable Optical Attenuator
        OMA:  Optical Modulation Analyser
        OSA:  Optical Spectrum Analyser
        WM:   Optical Wavelength Meter
        OTF:  Optical Tunable Filter
        TEC:  Temp Control
        SW:   Optical Switcher
        PS:   Power Supply
        PDLE: PDL Emulator/Source
        POLC: Polarization Controller/Synthesizer
        PMDE: PMD Emulator/Source
    """
    OPM = 1     # Optical Power Meter
    VOA = 2     # Variable Optical Attenuator
    OMA = 3     # Optical Modulation Analyser
    OSA = 4     # Optical Spectrum Analyser
    WM = 5      # Optical Wavelength Meter
    OTF = 6     # Optical Tunable Filter
    TEC = 7     # Temp Control
    SW = 8      # Optical Switcher
    PS = 9      # Power Supply
    PDLE = 10   # PDL Emulator/Source
    POLC = 11   # Polarization Controller/Synthesizer
    PMDE = 12   # PMD Emulator/Source


@unique
class OpticalUnit(Enum):
    DBM = 0
    W = 1


@unique
class TemperatureUnit(Enum):
    F = 0
    C = 1


@unique
class WavelengthUnit(Enum):
    NM = 0
    HZ = 1
