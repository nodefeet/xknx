from .device import Device
from .remote_value_datetime import DateTimeType, RemoteValueDateTime


class System(Device):
    """Class for managing the system."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods

    def __init__(
        self,
        xknx,
        name,
        group_address_datetime=None,
        group_address_date=None,
        group_address_time=None,
        device_updated_cb=None,
        # datetime_updated_cb=None,
        date_updated_cb=None,
        time_updated_cb=None,
    ):
        """Initialize System class."""
        # pylint: disable=too-many-arguments
        super().__init__(xknx, name, device_updated_cb)

        # self.datetime = RemoteValueDateTime(
        #     xknx,
        #     group_address_datetime,
        #     device_name=self.name,
        #     after_update_cb=datetime_updated_cb,
        #     datetime_type=DateTimeType.DATETIME,
        # )

        self.date = RemoteValueDateTime(
            xknx,
            group_address_date,
            device_name=self.name,
            after_update_cb=date_updated_cb,
            datetime_type=DateTimeType.DATE,
        )

        self.time = RemoteValueDateTime(
            xknx,
            group_address_time,
            device_name=self.name,
            after_update_cb=time_updated_cb,
            datetime_type=DateTimeType.TIME,
        )

    def has_group_address(self, group_address):
        """Test if device has given group address."""
        return (
            # self.datetime.has_group_address(group_address)
            self.date.has_group_address(group_address)
            or self.time.has_group_address(group_address)  # noqa W503
        )

    def __str__(self):
        """Return object as readable string."""
        return f"""<System name={self.name}, date={self.date.group_addr_str()}, time={self.time.group_addr_str()}>"""

    def state_addresses(self):
        """Return group addresses which should be requested to sync state."""
        state_addresses = []
        # state_addresses.extend(self.speed.state_addresses())
        return state_addresses

    async def process_group_write(self, telegram):
        """Process incoming GROUP WRITE telegram."""
        # await self.datetime.process(telegram)
        await self.date.process(telegram)
        await self.time.process(telegram)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
