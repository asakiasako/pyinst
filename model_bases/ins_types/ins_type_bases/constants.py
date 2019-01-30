from enum import Enum, unique


# define enums
# no inspection PyArgumentList
@unique
class InstrumentType(Enum):
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
class TempUnit(Enum):
    F = 0
    C = 1


@unique
class WavelengthUnit(Enum):
    NM = 0
    HZ = 1
