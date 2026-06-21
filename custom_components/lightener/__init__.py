"""Lightener Integration."""

import logging
from types import MappingProxyType
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_BRIGHTNESS, CONF_ENTITIES, CONF_FRIENDLY_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .config_flow import LightenerConfigFlow

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up platform from a config entry."""

    if not await async_migrate_entry(hass, entry):
        return False

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    # Forward the unloading of the entry to the platform.
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Update old versions of the configuration to the current format."""

    version = config_entry.version
    data = config_entry.data

    # Lightener 1.x didn't have config entries, just manual configuration.yaml. We consider this the no-version option.
    if version is None or version == 1:
        new_data = await async_migrate_data(data, version)

        hass.config_entries.async_update_entry(
            config_entry, data=new_data, version=LightenerConfigFlow.VERSION
        )

        return True

    if config_entry.version == LightenerConfigFlow.VERSION:
        return True

    _LOGGER.error('Unknown configuration version "%i"', version)
    return False


async def async_migrate_data(
    data: MappingProxyType[str, Any], version: int | None = None
) -> MappingProxyType[str, Any]:
    """Update data from old versions of the configuration to the current format."""

    # Lightener 1.x didn't have config entries, just manual configuration.yaml. We consider this the no-version option.
    if version is None or version == 1:
        new_data: dict = {CONF_ENTITIES: {}}

        if data.get(CONF_FRIENDLY_NAME) is not None:
            new_data[CONF_FRIENDLY_NAME] = data[CONF_FRIENDLY_NAME]

        for entity, brightness in data.get(CONF_ENTITIES, {}).items():
            new_data[CONF_ENTITIES][entity] = {CONF_BRIGHTNESS: brightness}

        return new_data

    # Otherwise return a copy of the data.
    return dict(data)


async def async_remove_config_entry_device(
    _hass: HomeAssistant, _config_entry: ConfigEntry, _device_entry: DeviceEntry
) -> bool:
    """Remove a config entry from a device."""

    return True
