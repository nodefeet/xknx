"""
Module for managing a remote value on the KNX bus.

Remote value can be :
- a group address for writing a KNX value,
- a group address for reading a KNX value,
- or a group of both representing the same value.
"""
from xknx.exceptions import CouldNotParseTelegram
from xknx.telegram import GroupAddress, Telegram, TelegramType


class RemoteValue:
    """Class for managing remote knx value."""

    def __init__(
        self,
        xknx,
        group_address=None,
        group_address_state=None,
        sync_state=True,
        device_name=None,
        after_update_cb=None,
    ):
        """Initialize RemoteValue class."""
        # pylint: disable=too-many-arguments
        self.xknx = xknx
        try:
            group_address = (
                [GroupAddress(ga.val) for ga in group_address] if group_address else None
            )
        except AttributeError:
            # for type(group_address) == str
            group_address = [GroupAddress(group_address)]

        # if isinstance(group_address, (str, int)):
        # group_address = [GroupAddress(address) for address in group_address]
        if isinstance(group_address_state, (str, int)):
            group_address_state = GroupAddress(group_address_state)

        self.group_address = group_address
        self.group_address_state = group_address_state
        self.sync_state = sync_state
        self.device_name = "Unknown" if device_name is None else device_name
        self.after_update_cb = after_update_cb
        self.payload = None

    @property
    def initialized(self):
        """Evaluate if remote value is initialized with group address."""
        return bool(self.group_address_state or self.group_address)

    @property
    def readable(self):
        """Evaluate if remote value should be read from bus."""
        return self.sync_state and isinstance(self.group_address_state, GroupAddress)

    @property
    def writable(self):
        """Evaluate if remote value has a group_address set."""
        return isinstance(self.group_address[0], GroupAddress) if self.group_address else False

    def has_group_address(self, group_address):
        """Test if device has given group address."""
        try:
            return group_address in self.group_address or group_address == self.group_address_state
        except TypeError:
            return False

    def state_addresses(self):
        """Return group addresses which should be requested to sync state."""
        if self.readable:
            return [
                self.group_address_state,
            ]
        return []

    def payload_valid(self, payload):
        """Test if telegram payload may be parsed - to be implemented in derived class.."""
        # pylint: disable=unused-argument
        self.xknx.logger.warning("payload_valid not implemented for %s", self.__class__.__name__)
        return True

    def from_knx(self, payload):
        """Convert current payload to value - to be implemented in derived class."""
        # pylint: disable=unused-argument
        self.xknx.logger.warning("from_knx not implemented for %s", self.__class__.__name__)

    def to_knx(self, value):
        """Convert value to payload - to be implemented in derived class."""
        # pylint: disable=unused-argument
        self.xknx.logger.warning("to_knx not implemented for %s", self.__class__.__name__)

    async def process(self, telegram):
        """Process incoming telegram."""
        if not self.has_group_address(telegram.group_address):
            return False
        if not self.payload_valid(telegram.payload):
            raise CouldNotParseTelegram(
                "payload invalid",
                payload=telegram.payload,
                group_address=telegram.group_address,
                device_name=f"{self.device_name}->{type(self).__name__}",
            )

        self.payload = telegram.payload
        if self.after_update_cb is not None:
            await self.after_update_cb(self.value, telegram.group_address)
        return True

    async def process_read(self, telegram):
        """Process read telegram."""
        if not self.has_group_address(telegram.group_address):
            return False
        await self.send(response=True)
        return True

    @property
    def value(self):
        """Return current value."""
        if self.payload is None:
            return None
        return self.from_knx(self.payload)

    async def send(self, response=False):
        """Send payload as telegram to KNX bus."""
        telegram = Telegram()
        # always use the first group address to send
        telegram.group_address = self.group_address[0]
        telegram.telegramtype = (
            TelegramType.GROUP_RESPONSE if response else TelegramType.GROUP_WRITE
        )
        telegram.payload = self.payload
        # print("telegram", telegram)
        await self.xknx.telegrams.put(telegram)

    async def set(self, value):
        """Set new value."""
        if not self.initialized:
            self.xknx.logger.info(
                "Setting value of uninitialized device: %s (value: %s)", self.device_name, value
            )
            return
        if not self.writable:
            self.xknx.logger.warning(
                "Attempted to set value for non-writable device: %s (value: %s)",
                self.device_name,
                value,
            )
            return

        self.payload = self.to_knx(value)
        await self.send()

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return None

    def group_addr_str(self):
        """Return object as readable string."""
        return "{0}/{1}/{2}/{3}".format(
            self.group_address.__repr__(),
            self.group_address_state.__repr__(),
            self.payload,
            self.value,
        )

    @property
    def group_addresses(self):
        if not self.group_address:
            return None
        try:
            group_addresses = ", ".join([str(ga) for ga in self.group_address])
        except TypeError:
            group_addresses = str(self.group_address)
        return group_addresses

    @group_addresses.setter
    def group_addresses(self, group_address):
        try:
            self.group_address = (
                [GroupAddress(ga.val) for ga in group_address] if group_address else None
            )
        except AttributeError:
            # for type(group_address) == str
            self.group_address = [GroupAddress(group_address)]

    def __str__(self):
        """Return object as string representation."""
        return '<{} device_name="{}" {}/>'.format(
            self.__class__.__name__, self.device_name, self.group_addr_str()
        )

    def __eq__(self, other):
        """Equal operator."""
        for key, value in self.__dict__.items():
            if key == "after_update_cb":
                continue
            if key not in other.__dict__:
                return False
            if other.__dict__[key] != value:
                return False
        for key, value in other.__dict__.items():
            if key == "after_update_cb":
                continue
            if key not in self.__dict__:
                return False
        return True
