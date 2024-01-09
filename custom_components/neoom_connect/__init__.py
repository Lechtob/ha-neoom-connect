"""The neeom CONNECT Integration."""

import asyncio
from datetime import timedelta

from homeassistant.helpers.discovery import load_platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_KEY, CONF_SITE_ID, CONF_UPDATE_INTERVAL

DOMAIN = "neoom"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Neoom component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Neoom from a config entry."""
    # Hier können Sie auf die gespeicherten Konfigurationsdaten zugreifen
    api_key = entry.data[CONF_API_KEY]
    site_id = entry.data[CONF_SITE_ID]
    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_INTERVAL)

    # Fügen Sie die eigentliche Integration hier hinzu
    await setup_neoom(hass, api_key, site_id, update_interval)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Entladen Sie hier die Ressourcen der Integration
    # ...
    return True

async def setup_neoom(hass, api_key, site_id, update_interval):
    """Set up the Neoom integration."""
    # Hier können Sie die erforderlichen Plattformen initialisieren
    # ...

    # Aktualisiere die Daten basierend auf dem konfigurierten Intervall
    async def update_data(now):
        # Hier sollten Sie die Daten von der Neoom API abrufen und aktualisieren
        # ...

        # Planen Sie die nächste Aktualisierung basierend auf dem Intervall
        hass.helpers.event.async_track_point_in_utc_time(update_data, now + timedelta(minutes=update_interval))

    # Starten Sie den ersten Update-Prozess
    await update_data(hass.datetime.utcnow())

    return True
