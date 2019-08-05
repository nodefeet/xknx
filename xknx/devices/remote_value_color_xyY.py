"""
Module for managing an RGB remote value.

DPT 242.600.
"""
from xknx.exceptions import ConversionError
from xknx.knx import DPTArray

from .remote_value import RemoteValue


class RemoteValueColorXyY(RemoteValue):
    """Abstraction for remote value of KNX DPT 242.600 (DPT_Color_xyY)."""

    def __init__(self, xknx, group_address=None, group_address_state=None, device_name=None, after_update_cb=None):
        """Initialize remote value of KNX DPT 242.600 (DPT_Color_xyY)."""
        # pylint: disable=too-many-arguments
        super().__init__(
            xknx, group_address, group_address_state, device_name=device_name, after_update_cb=after_update_cb
        )

    def payload_valid(self, payload):
        """Test if telegram payload may be parsed."""
        return isinstance(payload, DPTArray) and len(payload.value) == 6

    def to_knx(self, value):
        """Convert value to payload."""
        if not isinstance(value, (list, tuple)):
            raise ConversionError("Cant serialize RemoteValueColorXyY (wrong type)", value=value, type=type(value))
        if len(value) != 6:
            raise ConversionError("Cant serialize DPT 242.600 (wrong length)", value=value, type=type(value))
        if (
            any(not isinstance(xyY, int) for xyY in value)
            or any(xyY < 0 for xyY in value)  # noqa W503
            or any(xyY > 255 for xyY in value)  # noqa W503
        ):
            raise ConversionError("Cant serialize DPT 242.600 (wrong bytes)", value=value)

        return DPTArray(list(value))

    def from_knx(self, payload):
        """Convert current payload to value."""
        return (
            payload.value[0],
            payload.value[1],
            payload.value[2],
            payload.value[3],
            payload.value[4],
            payload.value[5],
        )
