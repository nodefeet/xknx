"""Implementation of Basic KNX 2-Byte/octet values."""

from xknx.exceptions import ConversionError

from .dpt import DPTBase


class DPT2ByteUnsigned(DPTBase):
    """
    Abstraction for KNX 2 Byte "2-octet unsigned value".

    Contains smaller counters, timers  etc.

    DPT 7.***
    """

    value_min = 0
    value_max = 65535
    unit = ""
    resolution = 1
    payload_length = 2

    @classmethod
    def from_knx(cls, raw):
        """Parse/deserialize from KNX/IP raw data."""
        cls.test_bytesarray(raw, 2)
        return (raw[0] * 256) + raw[1]

    @classmethod
    def to_knx(cls, value):
        """Serialize to KNX/IP raw data."""
        try:
            knx_value = int(value)
            if not cls._test_boundaries(knx_value):
                raise ValueError
            return knx_value >> 8, knx_value & 0xff
        except ValueError:
            raise ConversionError("Cant serialize %s" % cls.__name__, value=value)

    @classmethod
    def _test_boundaries(cls, value):
        """Test if value is within defined range for this object."""
        return cls.value_min <= value <= cls.value_max


class DPT2Ucount(DPT2ByteUnsigned):
    """DPT 7.001 DPT_Value_2_Ucount."""

    unit = "pulses"


class DPTTimePeriodMsec(DPT2ByteUnsigned):
    """DPT 7.002 DPT_TimePeriodMsec (ms)."""

    unit = "ms"


class DPTTimePeriod10Msec(DPT2ByteUnsigned):
    """DPT 7.003 DPT_TimePeriod10Msec (ms)."""

    unit = "ms"
    resolution = 10


class DPTTimePeriod100Msec(DPT2ByteUnsigned):
    """DPT 7.004 DPT_TimePeriod100Msec (ms)."""

    unit = "ms"
    resolution = 100


class DPTTimePeriodSec(DPT2ByteUnsigned):
    """DPT 7.005 DPT_TimePeriodSec (s)."""

    unit = "s"


class DPTTimePeriodMin(DPT2ByteUnsigned):
    """DPT 7.006 DPT_TimePeriodMin (min)."""

    unit = "min"


class DPTTimePeriodHrs(DPT2ByteUnsigned):
    """DPT 7.007 DPT_TimePeriodHrs (h)."""

    unit = "h"


class DPTLengthMm(DPT2ByteUnsigned):
    """DPT 7.011 Abstraction for KNX 2 Byte DPT_Length_mm (mm)."""

    unit = "mm"


class DPTUElCurrentmA(DPT2ByteUnsigned):
    """DPT 7.012 Abstraction for KNX 2 Byte DPTUElCurrentmA."""

    unit = "mA"


class DPTBrightness(DPT2ByteUnsigned):
    """DPT 7.013 DPT_Brightness (lux)."""

    unit = "lx"


class DPTColorTemperature(DPT2ByteUnsigned):
    """DPT 7.600 DPT_Color_Temperature (K)."""

    unit = "K"
