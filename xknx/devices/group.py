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
from xknx.remote_value import RemoteValueColorRGB as RV_RGB
from xknx.remote_value import RemoteValueColorXyY as RV_XYY
from xknx.remote_value import RemoteValueDpt2ByteUnsigned as RV_ABS
from xknx.remote_value import RemoteValueDpt3 as RV_DIM
from xknx.remote_value import RemoteValueScaling as RV_SCALE
from xknx.remote_value import RemoteValueSwitch as RV_SWITCH

from .device import Device


class Group(Device):
    """Class for managing a light."""

    # pylint: disable=too-many-locals

    def __init__(
        self,
        xknx,
        name,
        addr,
        sw_cb=None,
        #
        val_cb=None,
        val_dim_cb=None,
        #
        clr_rgb_cb=None,
        clr_rgb_bri_cb=None,
        clr_rgb_dim=None,
        #
        clr_r_cb=None,
        clr_r_bri_cb=None,
        clr_r_dim_cb=None,
        clr_r_sw_cb=None,
        #
        clr_g_cb=None,
        clr_g_bri_cb=None,
        clr_g_dim_cb=None,
        clr_g_sw_cb=None,
        #
        clr_b_cb=None,
        clr_b_bri_cb=None,
        clr_b_dim_cb=None,
        clr_b_sw_cb=None,
        #
        clr_cct_cb=None,
        clr_cct_dim_cb=None,
        #
        clr_h_cb=None,
        clr_h_dim_cb=None,
        #
        clr_s_cb=None,
        clr_s_dim_cb=None,
        #
        clr_cct_abs_in_cb=None,
    ):
        """Initialize Group class."""
        # pylint: disable=too-many-arguments
        super().__init__(xknx, name)
        self.xknx = xknx

        self.sw = RV_SWITCH(xknx, addr["SW"], None, self.name, sw_cb)
        self.sw_stat = RV_SWITCH(xknx, addr["SW_STAT"], None, self.name)

        self.val = RV_SCALE(xknx, addr["VAL"], None, self.name, val_cb, 0, 255,)
        self.val_dim = RV_DIM(xknx, addr["VAL_DIM"], None, self.name, val_dim_cb)
        self.val_stat = RV_SCALE(xknx, addr["VAL_STAT"], None, self.name, None, 0, 255)
        #
        self.clr_xyy = RV_XYY(xknx, addr["CLR_xyY"], None, self.name)
        self.clr_xyy_stat = RV_XYY(xknx, addr["CLR_xyY_STAT"], None, self.name)
        self.clr_cct_abs = RV_ABS(xknx, addr["CLR_CCT_ABS"], None, self.name)
        #
        self.clr_rgb = RV_RGB(xknx, addr["CLR_RGB"], None, self.name, clr_rgb_cb)
        self.clr_rgb_bri = RV_RGB(xknx, addr["CLR_RGB_BRI"], None, self.name, clr_rgb_bri_cb)
        self.clr_rgb_dim = RV_DIM(xknx, addr["CLR_RGB_DIM"], None, self.name, clr_rgb_dim)
        self.clr_rgb_stat = RV_RGB(xknx, addr["CLR_RGB_STAT"], None, self.name)
        #
        self.clr_r = RV_SCALE(xknx, addr["CLR_R"], None, self.name, clr_r_cb, 0, 255)
        self.clr_r_bri = RV_SCALE(xknx, addr["CLR_R_BRI"], None, self.name, clr_r_bri_cb, 0, 255)
        self.clr_r_dim = RV_DIM(xknx, addr["CLR_R_DIM"], None, self.name, clr_r_dim_cb)
        self.clr_r_stat = RV_SCALE(xknx, addr["CLR_R_STAT"], None, self.name, None, 0, 255)
        self.clr_r_sw = RV_SWITCH(xknx, addr["CLR_R_SW"], None, self.name, clr_r_sw_cb)
        self.clr_r_sw_stat = RV_SWITCH(xknx, addr["CLR_R_SW_STAT"], None, self.name)
        #
        self.clr_g = RV_SCALE(xknx, addr["CLR_G"], None, self.name, clr_g_cb, 0, 255)
        self.clr_g_bri = RV_SCALE(xknx, addr["CLR_G_BRI"], None, self.name, clr_g_bri_cb, 0, 255)
        self.clr_g_dim = RV_DIM(xknx, addr["CLR_G_DIM"], None, self.name, clr_g_dim_cb)
        self.clr_g_stat = RV_SCALE(xknx, addr["CLR_G_STAT"], None, self.name, None, 0, 255)
        self.clr_g_sw = RV_SWITCH(xknx, addr["CLR_G_SW"], None, self.name, clr_g_sw_cb)
        self.clr_g_sw_stat = RV_SWITCH(xknx, addr["CLR_G_SW_STAT"], None, self.name)
        #
        self.clr_b = RV_SCALE(xknx, addr["CLR_B"], None, self.name, clr_b_cb, 0, 255)
        self.clr_b_bri = RV_SCALE(xknx, addr["CLR_B_BRI"], None, self.name, clr_b_bri_cb, 0, 255)
        self.clr_b_dim = RV_DIM(xknx, addr["CLR_B_DIM"], None, self.name, clr_b_dim_cb)
        self.clr_b_stat = RV_SCALE(xknx, addr["CLR_B_STAT"], None, self.name, None, 0, 255)
        self.clr_b_sw = RV_SWITCH(xknx, addr["CLR_B_SW"], None, self.name, clr_b_sw_cb)
        self.clr_b_sw_stat = RV_SWITCH(xknx, addr["CLR_B_SW_STAT"], None, self.name)
        #
        self.clr_cct = RV_SCALE(xknx, addr["CLR_CCT"], None, self.name, clr_cct_cb, 0, 255)
        self.clr_cct_dim = RV_DIM(xknx, addr["CLR_CCT_DIM"], None, self.name, clr_cct_dim_cb)
        self.clr_cct_stat = RV_SCALE(xknx, addr["CLR_CCT_STAT"], None, self.name, None, 0, 255)
        #
        self.clr_cct_abs_in = RV_ABS(xknx, addr["CLR_CCT_ABS_IN"], None, self.name, clr_cct_abs_in_cb)
        self.clr_cct_abs_stat = RV_ABS(xknx, addr["CLR_CCT_ABS_STAT"], None, self.name)
        #
        self.clr_h = RV_SCALE(xknx, addr["CLR_H"], None, self.name, clr_h_cb, 0, 360,)
        self.clr_h_dim = RV_DIM(xknx, addr["CLR_H_DIM"], None, self.name, clr_h_dim_cb)
        self.clr_h_stat = RV_SCALE(xknx, addr["CLR_H_STAT"], None, self.name, None, 0, 360,)
        #
        self.clr_s = RV_SCALE(xknx, addr["CLR_S"], None, self.name, clr_s_cb, 0, 255)
        self.clr_s_dim = RV_DIM(xknx, addr["CLR_S_DIM"], None, self.name, clr_s_dim_cb)
        self.clr_s_stat = RV_SCALE(xknx, addr["CLR_S_STAT"], None, self.name, None, 0, 255)

        self.clr_tw_ww = RV_SCALE(xknx, addr["CLR_TW_WW"], None, self.name, None, 0, 255)
        self.clr_tw_cw = RV_SCALE(xknx, addr["CLR_TW_CW"], None, self.name, None, 0, 255)

    def update(self, addresses):
        self.sw.group_addresses = addresses["SW"]
        self.sw_stat.group_addresses = addresses["SW_STAT"]
        #
        self.val.group_addresses = addresses["VAL"]
        self.val_dim.group_addresses = addresses["VAL_DIM"]
        self.val_stat.group_addresses = addresses["VAL_STAT"]
        #
        self.clr_xyy.group_addresses = addresses["CLR_xyY"]
        self.clr_xyy_stat.group_addresses = addresses["CLR_xyY_STAT"]
        self.clr_cct_abs.group_addresses = addresses["CLR_CCT_ABS"]
        #
        self.clr_rgb.group_addresses = addresses["CLR_RGB"]
        self.clr_rgb_bri.group_addresses = addresses["CLR_RGB_BRI"]
        self.clr_rgb_dim.group_addresses = addresses["CLR_RGB_DIM"]
        self.clr_rgb_stat.group_addresses = addresses["CLR_RGB_STAT"]
        #
        self.clr_r.group_addresses = addresses["CLR_R"]
        self.clr_r_bri.group_addresses = addresses["CLR_R_BRI"]
        self.clr_r_dim.group_addresses = addresses["CLR_R_DIM"]
        self.clr_r_stat.group_addresses = addresses["CLR_R_STAT"]
        self.clr_r_sw.group_addresses = addresses["CLR_R_SW"]
        self.clr_r_sw_stat.group_addresses = addresses["CLR_R_SW_STAT"]
        #
        self.clr_g.group_addresses = addresses["CLR_G"]
        self.clr_g_bri.group_addresses = addresses["CLR_G_BRI"]
        self.clr_g_dim.group_addresses = addresses["CLR_G_DIM"]
        self.clr_g_stat.group_addresses = addresses["CLR_G_STAT"]
        self.clr_g_sw.group_addresses = addresses["CLR_G_SW"]
        self.clr_g_sw_stat.group_addresses = addresses["CLR_G_SW_STAT"]
        #
        self.clr_b.group_addresses = addresses["CLR_B"]
        self.clr_b_bri.group_addresses = addresses["CLR_B_BRI"]
        self.clr_b_dim.group_addresses = addresses["CLR_B_DIM"]
        self.clr_b_stat.group_addresses = addresses["CLR_B_STAT"]
        self.clr_b_sw.group_addresses = addresses["CLR_B_SW"]
        self.clr_b_sw_stat.group_addresses = addresses["CLR_B_SW_STAT"]
        #
        self.clr_cct.group_addresses = addresses["CLR_CCT"]
        self.clr_cct_dim.group_addresses = addresses["CLR_CCT_DIM"]
        self.clr_cct_stat.group_addresses = addresses["CLR_CCT_STAT"]
        #
        self.clr_cct_abs_in.group_addresses = addresses["CLR_CCT_ABS_IN"]       
        self.clr_cct_abs_stat.group_addresses = addresses["CLR_CCT_ABS_STAT"]
        #
        self.clr_h.group_addresses = addresses["CLR_H"]
        self.clr_h_dim.group_addresses = addresses["CLR_H_DIM"]
        self.clr_h_stat.group_addresses = addresses["CLR_H_STAT"]
        #
        self.clr_s.group_addresses = addresses["CLR_S"]
        self.clr_s_dim.group_addresses = addresses["CLR_S_DIM"]
        self.clr_s_stat.group_addresses = addresses["CLR_S_STAT"]
        #
        self.clr_tw_ww.group_addresses = addresses["CLR_TW_WW"]
        self.clr_tw_cw.group_addresses = addresses["CLR_TW_CW"]

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
            or self.val.has_group_address(group_address)  # noqa W503
            or self.val_dim.has_group_address(group_address)  # noqa W503
            #
            or self.clr_xyy.has_group_address(group_address)  # noqa W503
            or self.clr_cct_abs.has_group_address(group_address)  # noqa W503
            #
            or self.clr_rgb.has_group_address(group_address)  # noqa W503
            or self.clr_rgb_bri.has_group_address(group_address)  # noqa W503
            or self.clr_rgb_dim.has_group_address(group_address)  # noqa W503
            #
            or self.clr_r.has_group_address(group_address)  # noqa W503
            or self.clr_r_bri.has_group_address(group_address)  # noqa W503
            or self.clr_r_dim.has_group_address(group_address)  # noqa W503
            or self.clr_r_sw.has_group_address(group_address)  # noqa W503
            #
            or self.clr_g.has_group_address(group_address)  # noqa W503
            or self.clr_g_bri.has_group_address(group_address)  # noqa W503
            or self.clr_g_dim.has_group_address(group_address)  # noqa W503
            or self.clr_g_sw.has_group_address(group_address)  # noqa W503
            #
            or self.clr_b.has_group_address(group_address)  # noqa W503
            or self.clr_b_bri.has_group_address(group_address)  # noqa W503
            or self.clr_b_dim.has_group_address(group_address)  # noqa W503
            or self.clr_b_sw.has_group_address(group_address)  # noqa W503
            #
            or self.clr_h.has_group_address(group_address)  # noqa W503
            or self.clr_h_dim.has_group_address(group_address)  # noqa W503
            #
            or self.clr_s.has_group_address(group_address)  # noqa W503
            or self.clr_s_dim.has_group_address(group_address)  # noqa W503
            #
            or self.clr_cct.has_group_address(group_address)  # noqa W503
            or self.clr_cct_dim.has_group_address(group_address)  # noqa W503
            or self.clr_cct_abs_in.has_group_address(group_address)  # noqa W503
            # Status for group read requests
            # sw and val_stat needed in GW function
            or self.sw_stat.has_group_address(group_address)  # noqa W503
            or self.val_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_rgb_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_r_stat.has_group_address(group_address)  # noqa W503
            or self.clr_r_sw_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_g_stat.has_group_address(group_address)  # noqa W503
            or self.clr_g_sw_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_b_stat.has_group_address(group_address)  # noqa W503
            or self.clr_b_sw_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_h_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_s_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_cct_stat.has_group_address(group_address)  # noqa W503
            or self.clr_cct_abs_stat.has_group_address(group_address)  # noqa W503
            #
            or self.clr_tw_ww.has_group_address(group_address)  # noqa W503
            or self.clr_tw_cw.has_group_address(group_address)  # noqa W503
        )

    def __repr__(self):
        """Return object as readable string."""
        return (
            f"KNX_Group(name={self.name}, sw:{self.sw.group_address}"
            f", sw_stat: {self.sw_stat.group_address}"
            f", val_dim:{self.val_dim.group_address}, val:{self.val.group_address}"
            f", clr_xyy: {self.clr_xyy.group_address}, clr_rgb: {self.clr_rgb.group_address}"
            f", clr_rgb_stat:{self.clr_rgb_stat.group_address}"
        )

    async def process_group_write(self, telegram):
        """Process incoming GROUP WRITE telegram."""
        await self.sw.process(telegram)
        await self.val_dim.process(telegram)
        await self.val.process(telegram)
        #
        # await self.clr_xyy.process(telegram)
        #
        await self.clr_rgb.process(telegram)
        await self.clr_rgb_bri.process(telegram)
        await self.clr_rgb_dim.process(telegram)
        #
        await self.clr_r.process(telegram)
        await self.clr_r_bri.process(telegram)
        await self.clr_r_dim.process(telegram)
        await self.clr_r_sw.process(telegram)
        #
        await self.clr_g.process(telegram)
        await self.clr_g_bri.process(telegram)
        await self.clr_g_dim.process(telegram)
        await self.clr_g_sw.process(telegram)
        #
        await self.clr_b.process(telegram)
        await self.clr_b_bri.process(telegram)
        await self.clr_b_dim.process(telegram)
        await self.clr_b_sw.process(telegram)
        #
        await self.clr_h.process(telegram)
        await self.clr_h_dim.process(telegram)
        #
        await self.clr_s.process(telegram)
        await self.clr_s_dim.process(telegram)
        #
        await self.clr_cct.process(telegram)
        await self.clr_cct_dim.process(telegram)
        #
        await self.clr_cct_abs_in.process(telegram)

    async def process_group_read(self, telegram):
        """Process incoming GroupValueRead telegrams."""
        await self.sw_stat.process_read(telegram)
        await self.val_stat.process_read(telegram)
        #
        await self.clr_rgb_stat.process_read(telegram)
        #
        await self.clr_r_stat.process_read(telegram)
        await self.clr_r_sw_stat.process_read(telegram)
        #
        await self.clr_g_stat.process_read(telegram)
        await self.clr_g_sw_stat.process_read(telegram)
        #
        await self.clr_b_stat.process_read(telegram)
        await self.clr_b_sw_stat.process_read(telegram)
        #
        await self.clr_h_stat.process_read(telegram)
        #
        await self.clr_s_stat.process_read(telegram)
        #
        await self.clr_cct_stat.process_read(telegram)
        await self.clr_cct_abs_stat.process_read(telegram)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
