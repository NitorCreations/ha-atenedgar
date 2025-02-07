import logging

from attr import dataclass
from homeassistant import config_entries
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from custom_components.atenedgar.aten import Aten
from custom_components.atenedgar.edgar import Edgar, EdgarSettings


@dataclass
class AtenEdgarConfigEntryRuntimeData:
    aten: Aten
    edgar_settings: EdgarSettings


logger = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """
    Setup from a config entry
    """
    # Verify that the Edgar serial server is reachable
    edgar = Edgar(entry.data["host"], entry.data["port"])
    if not await edgar.is_reachable():
        raise ConfigEntryNotReady("Unable to connect")

    # Query Edgar settings so we can build device information
    settings = await edgar.get_settings()
    if settings is None:
        raise ConfigEntryNotReady("Unable to fetch device settings")

    # Create device
    aten = Aten(edgar, entry.data["name"])
    entry.runtime_data = AtenEdgarConfigEntryRuntimeData(aten, settings)

    hass.async_create_task(hass.config_entries.async_forward_entry_setups(entry, [Platform.MEDIA_PLAYER]))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, Platform.MEDIA_PLAYER)
