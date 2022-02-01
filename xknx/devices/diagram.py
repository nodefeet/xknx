"""Module for managing a KNX scene."""
from xknx.remote_value import RemoteValueSwitch as RV_SWITCH

from .device import Device


class Diagram(Device):
    """Class for managing a scene."""

    def __init__(self,
                 xknx,
                 name,
                 group_address=None,
                 sw_cb=None):
        """Initialize Sceneclass."""
        # pylint: disable=too-many-arguments
        super().__init__(xknx, name)

        self.sw = RV_SWITCH(xknx, group_address, None, self.name, sw_cb)

    def has_group_address(self, group_address):
        """Test if device has given group address."""
        return self.sw.has_group_address(group_address)

    def __str__(self):
        """Return object as readable string."""
        return f"KNX_Diagram(name={self.name}, sw:{self.sw.group_address})"

    def state_addresses(self):
        """Return group addresses which should be requested to sync state."""
        return []

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
    
    async def process_group_write(self, telegram):
        """Process incoming GROUP WRITE telegram."""
        await self.sw.process(telegram)
