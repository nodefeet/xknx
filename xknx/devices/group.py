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

        self.sw = RemoteValueSwitch(
            xknx, addresses["SW"], device_name=self.name, after_update_cb=switch_cb
        )

        self.sw_stat = RemoteValueSwitch(xknx, addresses["SW_STAT"], device_name=self.name)

        self.val_dim = RemoteValueDpt3(
            xknx, addresses["VAL_DIM"], device_name=self.name, after_update_cb=dimming_val_cb,
        )

        self.val = RemoteValueScaling(
            xknx,
            addresses["VAL"],
            device_name=self.name,
            after_update_cb=brightness_cb,
            range_from=0,
            range_to=255,
        )

        self.val_stat = RemoteValueScaling(
            xknx, addresses["VAL_STAT"], device_name=self.name, range_from=0, range_to=255,
        )

        self.clr_xyy = RemoteValueColorXyY(xknx, addresses["CLR_xyY"], device_name=self.name)

        self.clr_xyy_stat = RemoteValueColorXyY(
            xknx, addresses["CLR_xyY_STAT"], device_name=self.name
        )

        self.clr_rgb = RemoteValueColorRGB(
            xknx, addresses["CLR_RGB"], device_name=self.name, after_update_cb=color_rgb_cb
        )

        self.clr_rgb_stat = RemoteValueColorRGB(
            xknx, addresses["CLR_RGB_STAT"], device_name=self.name
        )

        self.clr_h_dim = RemoteValueDpt3(
            xknx, addresses["CLR_H_DIM"], device_name=self.name, after_update_cb=dimming_hue_cb,
        )

        self.clr_s_dim = RemoteValueDpt3(
            xknx, addresses["CLR_S_DIM"], device_name=self.name, after_update_cb=dimming_sat_cb,
        )

        self.clr_cct_dim = RemoteValueDpt3(
            xknx, addresses["CLR_CCT_DIM"], device_name=self.name, after_update_cb=dimming_cct_cb,
        )

        self.clr_h_stat = RemoteValueScaling(
            xknx, addresses["CLR_H_STAT"], device_name=self.name, range_from=0, range_to=360,
        )

        self.clr_s_stat = RemoteValueScaling(
            xknx, addresses["CLR_S_STAT"], device_name=self.name, range_from=0, range_to=255,
        )

        self.clr_cct_stat = RemoteValueScaling(
            xknx, addresses["CLR_CCT_STAT"], device_name=self.name, range_from=0, range_to=255,
        )

    def update(self, addresses):
        self.sw.group_addresses = addresses["SW"]
        self.sw_stat.group_addresses = addresses["SW_STAT"]
        #
        self.val_dim.group_addresses = addresses["VAL_DIM"]
        self.val.group_addresses = addresses["VAL"]
        self.val_stat.group_addresses = addresses["VAL_STAT"]
        #
        self.clr_xyy.group_addresses = addresses["CLR_xyY"]
        self.clr_xyy_stat.group_addresses = addresses["CLR_xyY_STAT"]
        #
        self.clr_rgb.group_addresses = addresses["CLR_RGB"]
        self.clr_rgb_stat.group_addresses = addresses["CLR_RGB_STAT"]
        #
        self.clr_h_dim.group_addresses = addresses["CLR_H_DIM"]
        self.clr_s_dim.group_addresses = addresses["CLR_S_DIM"]
        self.clr_cct_dim.group_addresses = addresses["CLR_CCT_DIM"]
        self.clr_h_stat.group_addresses = addresses["CLR_H_STAT"]
        self.clr_s_stat.group_addresses = addresses["CLR_S_STAT"]
        self.clr_cct_stat.group_addresses = addresses["CLR_CCT_STAT"]

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
        """Test if device has given group address. Not used for Status"""
        return (
            self.sw.has_group_address(group_address)
            or self.val_dim.has_group_address(group_address)  # noqa W503
            or self.val.has_group_address(group_address)  # noqa W503
            or self.clr_xyy.has_group_address(group_address)  # noqa W503
            or self.clr_rgb.has_group_address(group_address)  # noqa W503
            or self.clr_h_dim.has_group_address(group_address)  # noqa W503
            or self.clr_s_dim.has_group_address(group_address)  # noqa W503
            or self.clr_cct_dim.has_group_address(group_address)  # noqa W503
        )

    def __repr__(self):
        """Return object as readable string."""
        return (
            f"KNX_Group(name={self.name}, st:{self.sw.group_address}"
            f", dm:{self.vaL_dim.group_address}, wr:{self.val.group_address}"
            f", xyY:{self.clr_xyy.group_address},rgb:{self.clr_rgb.group_address}"
            f", RMrgb:{self.clr_rgb_stat.group_address}"
        )

    @property
    def state(self):
        """Return the current switch state of the device."""
        return self.switch.value == RemoteValueSwitch.Value.ON

    async def process_group_write(self, telegram):
        """Process incoming GROUP WRITE telegram."""
        await self.sw.process(telegram)
        await self.val_dim.process(telegram)
        await self.val.process(telegram)
        await self.clr_xyy.process(telegram)
        await self.clr_rgb.process(telegram)
        await self.clr_h_dim.process(telegram)
        await self.clr_s_dim.process(telegram)
        await self.clr_cct_dim.process(telegram)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
