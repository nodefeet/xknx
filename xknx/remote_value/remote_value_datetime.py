"""
Module for managing an KNX 3 Octet Time remote value.

10.001 DPT_TimeOfDay
11.001 DPT_Date
19.001 DPT_DateTime not used yet
"""
from enum import Enum

from xknx.dpt import DPTArray, DPTDate, DPTTime  # DPTDateTime

from .remote_value import RemoteValue


class DateTimeType(Enum):
    """Enum class for the broadcast type of the enum."""

    DATETIME = 1
    DATE = 2
    TIME = 3


class RemoteValueDateTime(RemoteValue):
    """Abstraction for remote value of KNX DPT 1.001 / DPT_Switch."""

    def __init__(
        self,
        xknx,
        group_address=None,
        group_address_state=None,
        device_name=None,
        after_update_cb=None,
        datetime_type=DateTimeType.TIME,
    ):
        """Initialize remote value of KNX DPT 1.001."""
        # pylint: disable=too-many-arguments
        super().__init__(
            xknx, group_address, group_address_state, device_name=device_name, after_update_cb=after_update_cb
        )
        self.datetime_type = datetime_type

    def payload_valid(self, payload):
        """Test if telegram payload may be parsed."""
        if self.datetime_type == DateTimeType.DATE or self.datetime_type == DateTimeType.TIME:
            return isinstance(payload, DPTArray) and len(payload.value) == 3
        # elif self.datetime_type == DateTimeType.DATETIME:
        #     return isinstance(payload, DPTArray) and len(payload.value) == 8

    def to_knx(self, value):
        """Convert value to payload."""
        pass

    def from_knx(self, payload):
        """Convert current payload to value."""
        # if self.datetime_type == DateTimeType.DATETIME:
        #     datetime_data = DPTDateTime.from_knx(payload.value)
        if self.datetime_type == DateTimeType.DATE:
            datetime_data = DPTDate.from_knx(payload.value)

        elif self.datetime_type == DateTimeType.TIME:
            datetime_data = DPTTime.from_knx(payload.value)

        return datetime_data
