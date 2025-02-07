import logging

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo, format_mac

from . import Aten, AtenEdgarConfigEntryRuntimeData, EdgarSettings
from .const import DOMAIN

logger = logging.getLogger(__name__)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up the  HDMI Switch media player from a config entry."""
    runtime_data: AtenEdgarConfigEntryRuntimeData = entry.runtime_data

    async_add_entities([AtenHDMISwitch(runtime_data.aten, runtime_data.edgar_settings)])


class AtenHDMISwitch(MediaPlayerEntity):
    def __init__(self, aten: Aten, edgar_settings: EdgarSettings):
        self._aten = aten
        self._edgar_settings = edgar_settings

        self._device_class = MediaPlayerDeviceClass.RECEIVER
        self._state = MediaPlayerState.PLAYING
        self._source = None
        self._source_list = ["1", "2", "3", "4"]

    _attr_supported_features = MediaPlayerEntityFeature.SELECT_SOURCE

    @property
    def device_class(self) -> MediaPlayerDeviceClass:
        return self._device_class

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, format_mac(self._edgar_settings.mac))},
            configuration_url=f"http://{self._edgar_settings.ip}/",
            manufacturer="Papouch",
            model=self._edgar_settings.type,
            sw_version=self._edgar_settings.fw,
        )

    @property
    def unique_id(self) -> str:
        mac = format_mac(self._edgar_settings.mac)
        return f"aten_hdmi_switch_via_edgar_{mac}"

    @property
    def state(self) -> MediaPlayerState:
        return self._state

    @property
    def name(self) -> str:
        return self._aten.name

    @property
    def source(self) -> str:
        return self._source

    @property
    def source_list(self) -> list[str]:
        return self._source_list

    async def async_select_source(self, source: str) -> None:
        logger.info(f"Switching source to {source}")
        await self._aten.select_source(int(source))
