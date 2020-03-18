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
from xknx.remote_value import (
    RemoteValueColorRGB,
    RemoteValueColorXyY,
    RemoteValueDpt3,
    RemoteValueScaling,
    RemoteValueSwitch,
)

from .device import Device


class Group(Device):
    """Class for managing a light."""

    # pylint: disable=too-many-locals

    def __init__(
        self,
        xknx,
        name,
        addresses,
        switch_cb=None,
        # switch_status_cb=None, <- no callback required
        switch_state_cb=None,
        dimming_val_cb=None,
        brightness_cb=None,
        # brightness_status_cb=None, <- no callback required
        color_rgb_cb=None,
        # color_xyY_status_cb=None, <- no callback required
        dimming_hue_cb=None,
        dimming_sat_cb=None,
        dimming_cct_cb=None,
    ):
        """Initialize Group class."""
        # pylint: disable=too-many-arguments
        super().__init__(xknx, name)
        self.xknx = xknx

        self.switch = RemoteValueSwitch(
            xknx, addresses["SW"], device_name=self.name, after_update_cb=switch_cb
        )

        self.switch_status = RemoteValueSwitch(xknx, addresses["SW_STAT"], device_name=self.name)

        self.dimming_val = RemoteValueDpt3(
            xknx, addresses["VAL_DIM"], device_name=self.name, after_update_cb=dimming_val_cb,
        )

        self.brightness = RemoteValueScaling(
            xknx,
            addresses["VAL"],
            device_name=self.name,
            after_update_cb=brightness_cb,
            range_from=0,
            range_to=255,
        )

        self.brightness_status = RemoteValueScaling(
            xknx, addresses["VAL_STAT"], device_name=self.name, range_from=0, range_to=255,
        )

        self.color_xyY = RemoteValueColorXyY(xknx, addresses["CLR_xyY"], device_name=self.name)

        self.color_xyY_status = RemoteValueColorXyY(
            xknx, addresses["CLR_xyY_STAT"], device_name=self.name
        )

        self.color_rgb = RemoteValueColorRGB(
            xknx, addresses["CLR_RGB"], device_name=self.name, after_update_cb=color_rgb_cb
        )

        self.color_rgb_status = RemoteValueColorRGB(
            xknx, addresses["CLR_RGB_STAT"], device_name=self.name
        )

        self.dimming_hue = RemoteValueDpt3(
            xknx, addresses["CLR_H_DIM"], device_name=self.name, after_update_cb=dimming_hue_cb,
        )

        self.dimming_sat = RemoteValueDpt3(
            xknx, addresses["CLR_S_DIM"], device_name=self.name, after_update_cb=dimming_sat_cb,
        )

        self.dimming_cct = RemoteValueDpt3(
            xknx, addresses["CLR_CCT_DIM"], device_name=self.name, after_update_cb=dimming_cct_cb,
        )

        self.dimming_hue_status = RemoteValueScaling(
            xknx, addresses["CLR_H_STAT"], device_name=self.name, range_from=0, range_to=360,
        )

        self.dimming_sat_status = RemoteValueScaling(
            xknx, addresses["CLR_S_STAT"], device_name=self.name, range_from=0, range_to=255,
        )

        self.dimming_cct_status = RemoteValueScaling(
            xknx, addresses["CLR_CCT_STAT"], device_name=self.name, range_from=0, range_to=255,
        )

    def update(self, addresses):
        self.switch.group_addresses = addresses["SW"]
        self.switch_status.group_addresses = addresses["SW_STAT"]
        self.dimming_val.group_addresses = addresses["VAL_DIM"]
        self.brightness.group_addresses = addresses["VAL"]
        self.brightness_status.group_addresses = addresses["VAL_STAT"]
        self.color_xyY.group_addresses = addresses["CLR_xyY"]
        self.color_xyY_status.group_addresses = addresses["CLR_xyY_STAT"]
        self.color_rgb.group_addresses = addresses["CLR_RGB"]
        self.color_rgb_status.group_addresses = addresses["CLR_RGB_STAT"]
        self.dimming_hue.group_addresses = addresses["CLR_H_DIM"]
        self.dimming_sat.group_addresses = addresses["CLR_S_DIM"]
        self.dimming_cct.group_addresses = addresses["CLR_CCT_DIM"]
        self.dimming_hue_status.group_addresses = addresses["CLR_H_STAT"]
        self.dimming_sat_status.group_addresses = addresses["CLR_S_STAT"]
        self.dimming_cct_status.group_addresses = addresses["CLR_CCT_STAT"]

    @property
    def supports_dimming(self):
        return self.dimming_val.initialized

    @property
    def supports_brightness(self):
        return self.brightness.initialized

    @property
    def supports_color(self):
        return self.color_rgb.initialized

    @property
    def supports_color_xyY(self):
        return self.color_xyY.initialized

    def has_group_address(self, group_address):
        """Test if device has given group address."""
        return (
            self.switch.has_group_address(group_address)
            or self.switch_status.has_group_address(group_address)  # noqa W503
            or self.dimming_val.has_group_address(group_address)  # noqa W503
            or self.brightness.has_group_address(group_address)  # noqa W503
            or self.brightness_status.has_group_address(group_address)  # noqa W503
            or self.color_xyY.has_group_address(group_address)  # noqa W503
            or self.color_xyY_status.has_group_address(group_address)  # noqa W503
            or self.color_rgb.has_group_address(group_address)  # noqa W503
            or self.color_rgb_status.has_group_address(group_address)  # noqa W503
            or self.dimming_hue.has_group_address(group_address)  # noqa W503
            or self.dimming_sat.has_group_address(group_address)  # noqa W503
            or self.dimming_cct.has_group_address(group_address)  # noqa W503
        )

    def __repr__(self):
        """Return object as readable string."""
        return (
            f"KNX_Group(name={self.name}, st:{self.switch.group_address}"
            f", dm:{self.dimming_val.group_address}, wr:{self.brightness.group_address}"
            f", xyY:{self.color_xyY.group_address},rgb:{self.color_rgb.group_address}"
            f", RMrgb:{self.color_rgb_status.group_address}"
        )

    @property
    def state(self):
        """Return the current switch state of the device."""
        return self.switch.value == RemoteValueSwitch.Value.ON

    async def process_group_write(self, telegram):
        """Process incoming GROUP WRITE telegram."""
        await self.switch.process(telegram)
        await self.dimming_val.process(telegram)
        await self.brightness.process(telegram)
        await self.color_xyY.process(telegram)
        await self.color_rgb.process(telegram)
        await self.dimming_hue.process(telegram)
        await self.dimming_sat.process(telegram)
        await self.dimming_cct.process(telegram)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
