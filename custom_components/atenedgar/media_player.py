import logging

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry

from . import Aten, AtenEdgarConfigEntryRuntimeData

logger = logging.getLogger(__name__)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up the  HDMI Switch media player from a config entry."""
    runtime_data: AtenEdgarConfigEntryRuntimeData = entry.runtime_data

    async_add_entities([AtenHDMISwitch(runtime_data.aten)])


class AtenHDMISwitch(MediaPlayerEntity):
    def __init__(self, aten: Aten):
        self._aten = aten

        self._device_class = MediaPlayerDeviceClass.RECEIVER
        self._state = MediaPlayerState.PLAYING
        self._source = None
        self._source_list = ["1", "2", "3", "4"]

    _attr_supported_features = MediaPlayerEntityFeature.SELECT_SOURCE

    @property
    def device_class(self) -> MediaPlayerDeviceClass:
        return self._device_class

    @property
    def unique_id(self) -> str:
        return "aten_hdmi_switch"

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
