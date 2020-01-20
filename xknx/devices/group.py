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
from xknx.telegram import GroupAddress

from .device import Device


class Group(Device):
    """Class for managing a light."""

    # pylint: disable=too-many-locals

    def __init__(
        self,
        xknx,
        db,
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
        """Initialize Light class."""
        # pylint: disable=too-many-arguments
        super().__init__(xknx, str(db.id))
        self.xknx = xknx
        self.switch_state_cb = switch_state_cb
        self.address_switch = db.address_switch
        self.addresses_switch_state = db.addresses_switch_state
        self.address_switch_status = db.address_switch_status
        self.address_dimming_val = db.address_dimming_val
        self.address_brightness = db.address_brightness
        self.address_brightness_status = db.address_brightness_status
        self.address_color_xyY = db.address_color_xyY
        self.address_color_xyY_status = db.address_color_xyY_status
        self.address_color_rgb = db.address_color_rgb
        self.address_color_rgb_status = db.address_color_rgb_status
        self.address_dimming_hue = db.address_dimming_hue
        self.address_dimming_sat = db.address_dimming_sat
        self.address_dimming_cct = db.address_dimming_cct
        self.address_dimming_hue_status = db.address_dimming_hue_status
        self.address_dimming_sat_status = db.address_dimming_sat_status
        self.address_dimming_cct_status = db.address_dimming_cct_status

        self.switch = RemoteValueSwitch(
            xknx, db.address_switch, device_name=self.name, after_update_cb=switch_cb
        )
        if db.addresses_switch_state:
            self.switch_states = [
                RemoteValueSwitch(
                    xknx, address.strip(), device_name=self.name, after_update_cb=switch_state_cb
                )
                for address in db.addresses_switch_state.split(",")
            ]

        self.switch_status = RemoteValueSwitch(
            xknx, db.address_switch_status, device_name=self.name
        )

        self.dimming_val = RemoteValueDpt3(
            xknx, db.address_dimming_val, device_name=self.name, after_update_cb=dimming_val_cb
        )

        self.brightness = RemoteValueScaling(
            xknx,
            db.address_brightness,
            device_name=self.name,
            after_update_cb=brightness_cb,
            range_from=0,
            range_to=255,
        )

        self.brightness_status = RemoteValueScaling(
            xknx, db.address_brightness_status, device_name=self.name, range_from=0, range_to=255
        )

        self.color_xyY = RemoteValueColorXyY(xknx, db.address_color_xyY, device_name=self.name)

        self.color_xyY_status = RemoteValueColorXyY(
            xknx, db.address_color_xyY_status, device_name=self.name
        )

        self.color_rgb = RemoteValueColorRGB(
            xknx, db.address_color_rgb, device_name=self.name, after_update_cb=color_rgb_cb
        )

        self.color_rgb_status = RemoteValueColorRGB(
            xknx, db.address_color_rgb_status, device_name=self.name
        )

        self.dimming_hue = RemoteValueDpt3(
            xknx, db.address_dimming_hue, device_name=self.name, after_update_cb=dimming_hue_cb
        )

        self.dimming_sat = RemoteValueDpt3(
            xknx, db.address_dimming_sat, device_name=self.name, after_update_cb=dimming_sat_cb
        )

        self.dimming_cct = RemoteValueDpt3(
            xknx, db.address_dimming_cct, device_name=self.name, after_update_cb=dimming_cct_cb
        )

        self.dimming_hue_status = RemoteValueScaling(
            xknx, db.address_dimming_hue_status, device_name=self.name, range_from=0, range_to=360
        )

        self.dimming_sat_status = RemoteValueScaling(
            xknx, db.address_dimming_sat_status, device_name=self.name, range_from=0, range_to=255
        )

        self.dimming_cct_status = RemoteValueScaling(
            xknx, db.address_dimming_cct_status, device_name=self.name, range_from=0, range_to=255
        )

    def update(self, db):

        self.switch.group_address = (
            GroupAddress(db.address_switch) if db.address_switch is not None else None
        )
        self.switch_status.group_address = (
            GroupAddress(db.address_switch_status)
            if db.address_switch_status is not None
            else None
        )
        self.dimming_val.group_address = (
            GroupAddress(db.address_dimming_val) if db.address_dimming_val is not None else None
        )
        self.brightness.group_address = (
            GroupAddress(db.address_brightness) if db.address_brightness is not None else None
        )
        self.brightness_status.group_address = (
            GroupAddress(db.address_brightness_status)
            if db.address_brightness_status is not None
            else None
        )
        self.color_xyY.group_address = (
            GroupAddress(db.address_color_xyY) if db.address_color_xyY is not None else None
        )
        self.color_xyY_status.group_address = (
            GroupAddress(db.address_color_xyY_status)
            if db.address_color_xyY_status is not None
            else None
        )
        self.color_rgb.group_address = (
            GroupAddress(db.address_color_rgb) if db.address_color_rgb is not None else None
        )
        self.color_rgb_status.group_address = (
            GroupAddress(db.address_color_rgb_status)
            if db.address_color_rgb_status is not None
            else None
        )
        self.dimming_hue.group_address = (
            GroupAddress(db.address_dimming_hue) if db.address_dimming_hue is not None else None
        )
        self.dimming_sat.group_address = (
            GroupAddress(db.address_dimming_sat) if db.address_dimming_sat is not None else None
        )
        self.dimming_cct.group_address = (
            GroupAddress(db.address_dimming_cct) if db.address_dimming_cct is not None else None
        )
        self.dimming_hue_status.group_address = (
            GroupAddress(db.address_dimming_hue_status)
            if db.address_dimming_hue_status is not None
            else None
        )
        self.dimming_sat_status.group_address = (
            GroupAddress(db.address_dimming_sat_status)
            if db.address_dimming_sat_status is not None
            else None
        )
        self.dimming_cct_status.group_address = (
            GroupAddress(db.address_dimming_cct_status)
            if db.address_dimming_cct_status is not None
            else None
        )
        self.address_switch = db.address_switch
        self.addresses_switch_state = db.addresses_switch_state
        self.address_switch_status = db.address_switch_status
        self.address_dimming_val = db.address_dimming_val
        self.address_brightness = db.address_brightness
        self.address_brightness_status = db.address_brightness_status
        self.address_color_xyY = db.address_color_xyY
        self.address_color_xyY_status = db.address_color_xyY_status
        self.address_color_rgb = db.address_color_rgb
        self.address_color_rgb_status = db.address_color_rgb_status
        self.address_dimming_hue = db.address_dimming_hue
        self.address_dimming_sat = db.address_dimming_sat
        self.address_dimming_cct = db.address_dimming_cct
        self.address_dimming_hue_status = db.address_dimming_hue_status
        self.address_dimming_sat_status = db.address_dimming_sat_status
        self.address_dimming_cct_status = db.address_dimming_cct_status

        if db.addresses_switch_state:
            self.switch_states = [
                RemoteValueSwitch(
                    self.xknx,
                    address.strip(),
                    device_name=self.name,
                    after_update_cb=self.switch_state_cb,
                )
                for address in db.addresses_switch_state.split(",")
            ]

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
