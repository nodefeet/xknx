"""
Module for managing a light via KNX.
It provides functionality for
* switching light 'on' and 'off'.
* process relative dimming.
* setting the brightness.
* setting the color rgb.
* setting the color xyY.
* reading the current state from KNX bus.
"""
from .device import Device
from .remote_value_color_rgb import RemoteValueColorRGB
from .remote_value_color_xyY import RemoteValueColorXyY
from .remote_value_dpt3 import RemoteValueDpt3  # RemoteValueStartStopDimming
from .remote_value_scaling import RemoteValueScaling
from .remote_value_switch import RemoteValueSwitch


class Group(Device):
    """Class for managing a light."""

    # pylint: disable=too-many-locals

    def __init__(
        self,
        xknx,
        name,
        group_address_switch=None,
        group_address_switch_state=None,
        group_address_switch_status=None,
        group_address_dimming_in=None,
        group_address_dimming_out=None,
        group_address_brightness=None,
        group_address_brightness_status=None,
        group_address_rgb=None,
        group_address_rgb_status=None,
        group_address_xyY=None,
        group_address_xyY_status=None,
        group_address_H=None,
        group_address_S=None,
        group_address_CCT=None,
        ##
        switch_st=None,
        switch_RMs=None,
        dimming_in_dm=None,
        brightness_wt=None,
        brightness_RMw=None,
        color_rgb=None,
    ):

        """Initialize Light class."""
        # pylint: disable=too-many-arguments
        super().__init__(xknx, name)

        self.switch = RemoteValueSwitch(
            xknx,
            group_address_switch,
            group_address_switch_state,
            device_name=self.name,
            after_update_cb=switch_updated_cb,
        )

        self.switch_status = RemoteValueSwitch(xknx, group_address_switch_status, device_name=self.name)

        self.dimming_in = RemoteValueDpt3(
            xknx, group_address_dimming_in, device_name=self.name, after_update_cb=dimming_in_updated_cb
        )

        self.dimming_out = RemoteValueDpt3(xknx, group_address_dimming_out, device_name=self.name)

        self.brightness = RemoteValueScaling(
            xknx,
            group_address_brightness,
            device_name=self.name,
            after_update_cb=brightness_updated_cb,
            range_from=0,
            range_to=255,
        )

        self.brightness_status = RemoteValueScaling(
            xknx, group_address_brightness_status, device_name=self.name, range_from=0, range_to=255
        )

        self.color_rgb = RemoteValueColorRGB(
            xknx, group_address_color_rgb, device_name=self.name, after_update_cb=color_rgb_updated_cb
        )

        self.color_rgb_status = RemoteValueColorRGB(xknx, group_address_color_rgb_status, device_name=self.name)

        self.color_xyY = RemoteValueColorXyY(xknx, group_address_color_xyY, device_name=self.name)

    @property
    def supports_dimming(self):
        """Return if light supports brightness."""
        return self.dimming_in.initialized

    @property
    def supports_brightness(self):
        """Return if light supports brightness."""
        return self.brightness.initialized

    @property
    def supports_color(self):
        """Return if light supports color."""
        return self.color_rgb.initialized

    @property
    def supports_color_xyY(self):
        """Return if light supports xyY color space."""
        return self.color_xyY.initialized

    def has_group_address(self, group_address):
        """Test if device has given group address."""
        return (
            self.switch.has_group_address(group_address)
            or self.dimming_in.has_group_address(group_address)  # noqa W503
            or self.brightness.has_group_address(group_address)  # noqa W503
            or self.color_rgb.has_group_address(group_address)  # noqa W503
            or self.color_xyY.has_group_address(group_address)  # noqa W503
        )

    def __repr__(self):
        """Return object as readable string."""
        return (
            f"KNX_Group(name={self.name}, st:{self.switch.group_address}, RMs:{self.switch_status.group_address},"
            f"dm:{self.dimming_in.group_address}, wr:{self.brightness.group_address},"
            f" RMw:{self.brightness_status.group_address}, rgb:{self.color_rgb.group_address},"
            f"RMrgb:{self.color_rgb_status.group_address}, xyY:{self.color_xyY.group_address}"
        )

    @property
    def state(self):
        """Return the current switch state of the device."""
        return self.switch.value == RemoteValueSwitch.Value.ON

    async def set_on(self):
        await self.switch.on()

    async def set_off(self):
        await self.switch.off()

    async def set_dimming(self, value):
        await self.dimming_out.set(value)

    @property
    def current_brightness(self):
        """Return current brightness of light."""
        return self.brightness.value

    async def set_brightness(self, brightness):
        """Set brightness of light."""
        if not self.supports_brightness:
            self.xknx.logger.warning("Dimming not supported for device %s", self.get_name())
            return
        await self.brightness.set(brightness)

    async def set_brightness_status(self, brightness):
        await self.brightness_status.set(brightness)

    @property
    def current_color_rgb(self):
        """Return current color of light."""
        return self.color_rgb.value

    async def set_color_rgb_status(self, color):
        """Set color of light."""
        if not self.supports_color:
            self.xknx.logger.warning("Colors not supported for device %s", self.get_name())
            return
        await self.color_rgb_status.set(color)

    @property
    def current_color_xyY(self):
        """Return current CIE xyY color of light."""
        return self.color_xyY.value

    async def set_color_xyY(self, color_xyY):
        """Set xyY color of light."""
        if not self.supports_color_xyY:
            self.xknx.logger.warning("CIE xyY Color Space not supported for device %s", self.get_name())
            return
        await self.color_xyY.set(color_xyY)

    def state_addresses(self):
        """Return group addresses which should be requested to sync state."""
        state_addresses = []
        state_addresses.extend(self.switch.state_addresses())
        state_addresses.extend(self.brightness.state_addresses())
        state_addresses.extend(self.color_rgb.state_addresses())
        state_addresses.extend(self.color_xyY.state_addresses())
        return state_addresses

    async def process_group_write(self, telegram):
        """Process incoming GROUP WRITE telegram."""
        await self.switch.process(telegram)
        await self.dimming_in.process(telegram)
        await self.brightness.process(telegram)
        await self.color_rgb.process(telegram)
        # await self.color_xyY.process(telegram)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
