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
    """
    OPM = 1     # Optical Power Meter
    VOA = 2     # Variable Optical Attenuator
    OMA = 3     # Optical Modulation Analyser
    OSA = 4     # Optical Spectrum Analyser
    WM = 5      # Optical Wavelength Meter
    OTF = 6     # Optical Tunable Filter
    TS = 7      # Temperature Source
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
